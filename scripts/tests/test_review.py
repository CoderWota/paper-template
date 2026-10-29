"""Tests for scripts/review.py: review-round response records and the reconciliation of a coauthor's Word edits."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
REVIEW = SCRIPTS / "review.py"
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'

RESPONSE = """# 回复：Journal A 第 1 轮

## R1.1 样本量

- Reviewer: Reviewer 1
- Source: `extracted/markdown/report-1.md`, item 1
- Comment: "The sample size is not justified."
- Status: addressed
- Response: We added a power analysis in the methods.
- Change: C1

## R1.2 Additional experiment

- Reviewer: Reviewer 1
- Source: `extracted/markdown/report-1.md`, item 2
- Comment: "Please add a field experiment."
- Status: declined
- Response: A field experiment is outside the scope; we state this limitation in the discussion.

## R2.1 Terminology

- Reviewer: Reviewer 2
- Source: `extracted/markdown/report-2.md`, comment 3
- Comment: summary: asks for consistent terms
- Status: planned
"""
CHANGES = """# 改动

## C1 Power analysis

- Items: R1.1
- Location: `manuscript/02-methods.md`
- Change: added a paragraph with the power analysis
- Status: done
"""


def run(text: str) -> str:
    return f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r>'


def make_docx(path: Path, paragraphs: list, comments: bool = False) -> Path:
    body = "".join(f"<w:p>{p}</w:p>" for p in paragraphs)
    with zipfile.ZipFile(path, "w") as package:
        package.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        package.writestr("word/document.xml", f"<w:document {W}><w:body>{body}</w:body></w:document>")
        if comments:
            package.writestr("word/comments.xml", f'<w:comments {W}><w:comment w:id="0" w:author="Chen (coauthor)" w:date="2026-10-28T09:00:00Z">'
                                                  f'<w:p>{run("Is this claim too strong?")}</w:p></w:comment></w:comments>')
    return path


class ReviewTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="review test ä "))
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)
        self.root = self.base / "论文 workspace"
        self.round = self.root / "reviews" / "journal-a" / "round-1"
        self.round.mkdir(parents=True)
        self.write("manuscript/manifest.yaml", "version: 1\nsections:\n  - 01-introduction.md\n  - 02-methods.md\n")
        self.write("manuscript/01-introduction.md", "# Introduction\n\nCities are warming faster than rural areas [@doe2021].\n\n"
                   "The effect on sleep is not well understood.\n")
        self.write("manuscript/02-methods.md", "# Methods\n\nWe surveyed 120 households in two districts.\n")

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run_review(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(REVIEW), "--root", str(self.root), *args], capture_output=True, text=True,
                              encoding="utf-8", timeout=120)


class ResponseRecordTests(ReviewTestCase):
    def test_complete_records_pass(self) -> None:
        self.write("reviews/journal-a/round-1/response.md", RESPONSE)
        self.write("reviews/journal-a/round-1/changes.md", CHANGES)
        result = self.run_review("check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("1 round(s): no problems", result.stdout)

    def test_unsupported_completion_claims_are_reported(self) -> None:
        response = (RESPONSE.replace("- Change: C1\n", "")
                    .replace("- Response: A field experiment is outside the scope; we state this limitation in the discussion.\n", "")
                    .replace("- Status: planned", "- Status: done")
                    + "\n## Minor points\n\n- Reviewer: Reviewer 3\n")
        changes = CHANGES.replace("- Status: done", "- Status: planned").replace("- Items: R1.1", "- Items: R1.1, R9.9").replace(
            "`manuscript/02-methods.md`", "`manuscript/09-missing.md`")
        self.write("reviews/journal-a/round-1/response.md", response)
        self.write("reviews/journal-a/round-1/changes.md", changes)
        result = self.run_review("check", "--round", "reviews/journal-a/round-1")
        self.assertEqual(result.returncode, 1)
        for fragment in ("R1.1: an addressed item links the change", "R1.2: a declined item needs the Response to the reviewer with its justification",
                         "R2.1: unknown status", "must start with an item ID", "C1: names R9.9, which is not in response.md",
                         "the location manuscript/09-missing.md does not exist"):
            self.assertIn(fragment, result.stdout)
        self.write("reviews/journal-a/round-1/response.md", RESPONSE)
        self.write("reviews/journal-a/round-1/changes.md", CHANGES.replace("- Status: done", "- Status: planned"))
        self.assertIn("R1.1: is marked addressed, but C1 is not done", self.run_review("check").stdout)


    def test_a_change_recorded_only_in_a_revision_is_reported_with_the_remedy(self) -> None:
        self.write("reviews/journal-a/round-1/response.md", RESPONSE)
        self.write("reviews/journal-a/round-1/changes.md", "# 改动\n")
        self.write("revisions/2026-11-scope/changes.md", CHANGES)  # the revision's own file holds C1; the round's does not
        result = self.run_review("check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("reviews/journal-a/round-1/response.md R1.1: the change C1 is not in reviews/journal-a/round-1/changes.md.", result.stdout)
        self.assertIn("also when a revision made the change (with a Revision: line); the changes.md inside a revision folder does not count", result.stdout)
        # The remedy that the message names makes the round pass.
        self.write("reviews/journal-a/round-1/changes.md", CHANGES.replace("- Status: done", "- Revision: `revisions/2026-11-scope/`\n- Status: done"))
        result = self.run_review("check")
        self.assertEqual(result.returncode, 0, result.stdout)


class ReconcileTests(ReviewTestCase):
    def tracked_docx(self) -> Path:
        edited = (run("Cities are warming ") + '<w:del w:id="1" w:author="Chen"><w:r><w:delText>faster</w:delText></w:r></w:del>'
                  + '<w:ins w:id="2" w:author="Chen">' + run("much faster") + "</w:ins>" + run(" than rural areas (Doe 2021)."))
        return make_docx(self.base / "intro edited by Chen.docx", [
            run("Introduction"), edited, run("The effect on sleep is not well understood."),
            '<w:ins w:id="3" w:author="Chen">' + run("A wholly new paragraph from the coauthor.") + "</w:ins>"], comments=True)

    def test_tracked_changes_are_located_and_reported_without_applying(self) -> None:
        before = (self.root / "manuscript" / "01-introduction.md").read_text(encoding="utf-8")
        result = self.run_review("reconcile", "--docx", str(self.tracked_docx()), "--to", "reviews/reconcile-chen.md")
        self.assertEqual(result.returncode, 0, result.stdout)
        report = (self.root / "reviews" / "reconcile-chen.md").read_text(encoding="utf-8")
        self.assertIn("- Location: manuscript/01-introduction.md:3", report)
        self.assertIn("applies cleanly", report)
        self.assertIn("Cities are warming {+much+} faster than rural areas", report)
        self.assertIn("new paragraph", report)
        self.assertIn("Comment 1 (Chen (coauthor))", report)
        self.assertIn("Nothing was applied", result.stdout)
        self.assertEqual((self.root / "manuscript" / "01-introduction.md").read_text(encoding="utf-8"), before)

    def test_a_paragraph_changed_on_both_sides_is_a_conflict(self) -> None:
        self.write("manuscript/01-introduction.md", "# Introduction\n\nCities are warming faster than surrounding rural areas, "
                   "especially at night [@doe2021].\n\nThe effect on sleep is not well understood.\n")
        result = self.run_review("reconcile", "--docx", str(self.tracked_docx()))
        self.assertIn("conflict: the manuscript paragraph also changed since the file was sent", result.stdout)
        self.assertIn("1 conflict with later manuscript changes", result.stdout)

    def test_a_separate_base_file_without_tracked_changes(self) -> None:
        sent = make_docx(self.base / "sent.docx", [run("Methods"), run("We surveyed 120 households in two districts.")])
        edited = make_docx(self.base / "returned.docx", [run("Methods"), run("We surveyed 120 households in three districts.")])
        result = self.run_review("reconcile", "--docx", str(edited), "--base", str(sent))
        self.assertIn("manuscript/02-methods.md:3", result.stdout)
        self.assertIn("[-two-] {+three+}", result.stdout)
        self.assertIn("1 apply cleanly", result.stdout)


if __name__ == "__main__":
    unittest.main()
