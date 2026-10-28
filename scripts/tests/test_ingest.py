"""Tests for document ingestion with the local route, review rounds, citation metadata, and the checks.

The local parser is replaced by fake_mineru_kit.py, so these tests need no models and no network.
They prove the workspace behaviour; they do not prove that MinerU itself converts a document well.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
import zlib
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

from ingestion import extraction, pdf, reviews  # noqa: E402

FAKE = Path(__file__).resolve().parent / "fake_mineru_kit.py"
STATIC = ("", "references", "references/originals", "references/extracted", "references/notes", "inbox", "inbox/imports",
          "reviews", "requirements", "manuscript", "state")
W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def make_pdf(path: Path, pages: int, annotation: bytes | None = None, compressed: bool = False) -> Path:
    """A small synthetic PDF: enough structure for page counting and annotation scans, not for rendering."""
    kids = " ".join(f"{3 + n} 0 R" for n in range(pages))
    objects = {1: b"<< /Type /Catalog /Pages 2 0 R >>", 2: f"<< /Type /Pages /Kids [{kids}] /Count {pages} >>".encode()}
    for n in range(pages):
        annots = f" /Annots [{3 + pages} 0 R]" if annotation and n == 0 else ""
        objects[3 + n] = f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]{annots} >>".encode()
    if annotation:
        objects[3 + pages] = b"<< /Type /Annot /Subtype /Text /Rect [10 10 50 50] " + annotation + b" >>"
    body = b"%PDF-1.7\n"
    if compressed:
        inner = b"".join(objects[number] + b"\n" for number in sorted(objects))
        stream = zlib.compress(inner)
        body += b"9 0 obj\n<< /Type /ObjStm /N 3 /First 0 /Filter /FlateDecode /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream\nendobj\n"
    else:
        for number in sorted(objects):
            body += f"{number} 0 obj\n".encode() + objects[number] + b"\nendobj\n"
    path.write_bytes(body + b"trailer << /Root 1 0 R >>\n%%EOF\n")
    return path


def run_xml(text: str) -> str:
    return f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r>'


def make_docx(path: Path) -> Path:
    """A Word review: two comments (the second a reply), one insertion, and one deletion."""
    body = (f"<w:p>{run_xml('Reviewer 1')}</w:p>"
            f'<w:p>{run_xml("1. The ")}<w:commentRangeStart w:id="0"/>{run_xml("claim is too strong")}<w:commentRangeEnd w:id="0"/>'
            f'<w:r><w:commentReference w:id="0"/></w:r><w:r><w:commentReference w:id="1"/></w:r></w:p>'
            f'<w:p>{run_xml("2. Report the size ")}<w:ins w:id="5" w:author="Reviewer 1" w:date="2026-09-01T10:00:00Z">{run_xml("per group")}</w:ins>'
            f'<w:del w:id="6" w:author="Reviewer 1" w:date="2026-09-01T10:00:00Z"><w:r><w:delText> overall</w:delText></w:r></w:del></w:p>')
    w14 = 'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"'
    comments = (f'<w:comments {W} {w14}>'
                f'<w:comment w:id="0" w:author="Reviewer 1" w:date="2026-09-01T09:00:00Z"><w:p w14:paraId="0000000A">{run_xml("Please qualify it.")}</w:p></w:comment>'
                f'<w:comment w:id="1" w:author="Author" w:date="2026-09-03T09:00:00Z"><w:p w14:paraId="0000000B">{run_xml("We will.")}</w:p></w:comment>'
                "</w:comments>")
    extended = ('<w15:commentsEx xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml">'
                '<w15:commentEx w15:paraId="0000000A" w15:done="0"/><w15:commentEx w15:paraId="0000000B" w15:paraIdParent="0000000A" w15:done="0"/>'
                "</w15:commentsEx>")
    with zipfile.ZipFile(path, "w") as package:
        package.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        package.writestr("word/document.xml", f"<w:document {W}><w:body>{body}</w:body></w:document>")
        package.writestr("word/comments.xml", comments)
        package.writestr("word/commentsExtended.xml", extended)
    return path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class WorkspaceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="ingest test ä "))
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)
        self.root = self.base / "workspace é"
        for rel in STATIC:
            folder = self.root / rel
            folder.mkdir(parents=True, exist_ok=True)
            title = rel or "workspace"
            (folder / "README.md").write_text(f"# {title}\n\nThis folder belongs to the disposable test workspace; its name is {title}, so that each description differs from all the others.\n", encoding="utf-8")
        (self.root / "references" / "index.md").write_text("# Reference Index\n\nA compact list.\n\nNo sources have been collected yet.\n", encoding="utf-8")
        (self.root / "requirements" / "privacy.md").write_text("# Privacy\n\nNo confirmed processing choices yet.\n", encoding="utf-8")
        self.inputs = self.base / "papers to import"
        self.inputs.mkdir()
        self.log = self.base / "fake-calls.jsonl"
        self.behaviour: dict = {}

    def ingest(self, *args: str) -> subprocess.CompletedProcess:
        env = dict(os.environ, INGEST_MINERU_KIT=json.dumps([sys.executable, str(FAKE)]), FAKE_MINERU_LOG=str(self.log),
                   FAKE_MINERU_BEHAVIOUR=json.dumps(self.behaviour))
        env.pop("MINERU_API_TOKEN", None)
        return subprocess.run([sys.executable, str(SCRIPTS / "ingest.py"), "--root", str(self.root), *args], capture_output=True,
                              text=True, encoding="utf-8", env=env, timeout=300)

    def calls(self) -> list:
        if not self.log.is_file():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines() if '"parse"' in line]

    def record(self, import_id: str | None = None) -> dict:
        folder = self.root / "inbox" / "imports"
        names = sorted(p.name for p in folder.iterdir() if p.is_dir())
        return json.loads((folder / (import_id or names[-1]) / "import.json").read_text(encoding="utf-8"))

    def statuses(self, record: dict) -> dict:
        return {item["name"]: item["status"] for item in record["items"]}


class LocalImportTests(WorkspaceTestCase):
    def test_imports_a_folder_and_records_every_item(self) -> None:
        report = make_pdf(self.inputs / "long report.pdf", 12)
        shutil.copy2(report, self.inputs / "重复 副本.pdf")
        (self.inputs / "figure.png").write_bytes(b"\x89PNG synthetic")
        (self.inputs / "notes.md").write_text("# Notes\n\n![A figure](figure.png)\n\nInline \\(x\\).\n", encoding="utf-8")
        (self.inputs / "old.doc").write_bytes(b"old office")
        (self.inputs / "data.xyz").write_text("unsupported", encoding="utf-8")
        before = sorted(p.name for p in self.inputs.iterdir())
        result = self.ingest("run", "--route", "local", "--tier", "flash", str(self.inputs))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        statuses = self.statuses(self.record())
        self.assertEqual(statuses["long report.pdf"], "converted")
        self.assertEqual(statuses["重复 副本.pdf"], "duplicate")
        self.assertEqual(statuses["notes.md"], "converted")
        self.assertEqual(statuses["old.doc"], "unsupported")
        self.assertEqual(statuses["data.xyz"], "unsupported")
        self.assertIn("old Office formats", " ".join(i["notes"][0] for i in self.record()["items"] if i["name"] == "old.doc"))
        # The input folder is untouched: no README or other file was added to it.
        self.assertEqual(sorted(p.name for p in self.inputs.iterdir()), before)
        source_id = "src-" + sha(report)[:12]
        archived = self.root / "references" / "originals" / source_id / "long report.pdf"
        self.assertEqual(sha(archived), sha(report))
        folder = self.root / "references" / "extracted" / source_id
        provenance = json.loads((folder / "provenance.json").read_text(encoding="utf-8"))
        self.assertEqual(provenance["coverage"]["expected"], 12)
        self.assertEqual(provenance["coverage"]["missing_pages"], [])
        self.assertEqual(provenance["conversion"]["tier"], "flash")
        document = (folder / "document.md").read_text(encoding="utf-8")
        self.assertIn("![](assets/page_0_image_3.jpg)", document)
        self.assertTrue((folder / "assets" / "page_0_image_3.jpg").is_file())
        self.assertTrue((folder / "native" / "middle_json.json").is_file())
        # The running header repeats on every page, so it is not reported as lost text.
        self.assertEqual(provenance["checks"]["omitted_text"]["unique_passages"], 0)
        call = next(call for call in self.calls() if call["argv"][1].endswith("long report.pdf"))
        self.assertIn("--pages", call["argv"])
        self.assertEqual(call["model_source"], "local")
        notes_id = next(i["target"] for i in self.record()["items"] if i["name"] == "notes.md")
        notes = (self.root / "references" / "extracted" / notes_id / "document.md").read_text(encoding="utf-8")
        self.assertIn("assets/001-figure.png", notes)
        self.assertIn("Inline $x$.", notes)
        index = (self.root / "references" / "index.md").read_text(encoding="utf-8")
        self.assertIn(f"| {source_id} | (file) long report.pdf |", index)
        self.assertNotIn("No sources have been collected yet.", index)
        readmes = subprocess.run([sys.executable, str(SCRIPTS / "check_readmes.py"), str(self.root)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(readmes.returncode, 0, readmes.stdout)
        verify = self.ingest("verify")
        self.assertEqual(verify.returncode, 0, verify.stdout)

    def test_a_stop_keeps_finished_work_and_the_import_continues(self) -> None:
        make_pdf(self.inputs / "a.pdf", 2)
        make_pdf(self.inputs / "b.pdf", 3)
        self.behaviour = {"b.pdf": {"models_missing": True}}
        result = self.ingest("run", "--route", "local", "--tier", "basic", str(self.inputs))
        self.assertEqual(result.returncode, 2, result.stdout)
        record = self.record()
        self.assertEqual(self.statuses(record), {"a.pdf": "converted", "b.pdf": "pending"})
        self.assertEqual(record["stopped"]["code"], "models-missing")
        self.behaviour = {}
        resumed = self.ingest("run", "--import-id", record["import_id"])
        self.assertEqual(resumed.returncode, 0, resumed.stdout)
        self.assertEqual(self.statuses(self.record()), {"a.pdf": "converted", "b.pdf": "converted"})
        converted = [Path(call["argv"][1]).name for call in self.calls()]
        self.assertEqual(converted.count("a.pdf"), 1, "a finished item must not be converted again")

    def test_a_corrupt_file_fails_alone(self) -> None:
        make_pdf(self.inputs / "good.pdf", 1)
        (self.inputs / "corrupt.pdf").write_bytes(b"%PDF-1.7\n1 0 obj")
        self.behaviour = {"corrupt.pdf": {"fail": True}}
        result = self.ingest("run", "--route", "local", "--tier", "flash", str(self.inputs))
        self.assertEqual(result.returncode, 1)
        record = self.record()
        self.assertEqual(self.statuses(record), {"corrupt.pdf": "failed", "good.pdf": "converted"})
        self.assertIn("Data format error", next(i["error"] for i in record["items"] if i["name"] == "corrupt.pdf"))

    def test_matching_results_are_reused_and_a_settings_change_is_detected(self) -> None:
        make_pdf(self.inputs / "paper.pdf", 2)
        self.assertEqual(self.ingest("run", "--route", "local", "--tier", "flash", str(self.inputs)).returncode, 0)
        self.assertEqual(self.ingest("run", "--route", "local", "--tier", "flash", str(self.inputs)).returncode, 0)
        self.assertEqual(self.statuses(self.record()), {"paper.pdf": "already-imported"})
        self.ingest("run", "--route", "local", "--tier", "basic", str(self.inputs))
        item = self.record()["items"][0]
        self.assertEqual(item["status"], "already-imported")
        self.assertIn("other settings", item["notes"][0])
        self.assertEqual(len(self.calls()), 1)
        self.assertEqual(self.ingest("run", "--route", "local", "--tier", "basic", "--reconvert", str(self.inputs)).returncode, 0)
        source_id = item["target"]
        provenance = json.loads((self.root / "references" / "extracted" / source_id / "provenance.json").read_text(encoding="utf-8"))
        self.assertEqual(provenance["revision"], 2)
        self.assertEqual(provenance["conversion"]["tier"], "basic")
        self.assertEqual(len(provenance["previous"]), 1)

    def test_problems_are_flagged_and_partial_results_stay_partial(self) -> None:
        make_pdf(self.inputs / "partial.pdf", 5)
        make_pdf(self.inputs / "flagged.pdf", 3)
        self.behaviour = {"partial.pdf": {"processed": 3}, "flagged.pdf": {"blank": [2], "lost_header": True, "unlinked_image": True, "math": True}}
        self.ingest("run", "--route", "local", "--tier", "flash", str(self.inputs))
        record = self.record()
        self.assertEqual(self.statuses(record), {"flagged.pdf": "needs-review", "partial.pdf": "partial"})
        partial = json.loads((self.root / "references" / "extracted" / record["items"][1]["target"] / "provenance.json").read_text(encoding="utf-8"))
        self.assertEqual(partial["coverage"]["missing_pages"], [4, 5])
        # The text itself shows that it is incomplete, and the note is marked as the workspace's.
        partial_text = (self.root / "references" / "extracted" / record["items"][1]["target"] / "document.md").read_text(encoding="utf-8")
        self.assertTrue(partial_text.startswith("> [!WARNING]\n> Incomplete extraction, noted by the workspace: pages 4-5 of 5 were not converted."))
        self.assertEqual(partial["outputs"]["document_sha256"], sha(self.root / "references" / "extracted" / record["items"][1]["target"] / "document.md"))
        self.assertEqual({item["role"] for item in record["items"]}, {"reference"})
        flagged = json.loads((self.root / "references" / "extracted" / record["items"][0]["target"] / "provenance.json").read_text(encoding="utf-8"))
        codes = {warning["code"] for warning in flagged["warnings"]}
        self.assertTrue({"pages-without-text", "omitted-text", "unreferenced-images", "formulas-unverified"} <= codes, codes)
        self.assertEqual(flagged["coverage"]["pages_without_text"], [2])
        document = (self.root / "references" / "extracted" / record["items"][0]["target"] / "document.md").read_text(encoding="utf-8")
        self.assertIn("\n\n$$\nx^2 + y^2\n$$\n", document)
        self.assertIn("Inline $a+b$", document)

    def test_hand_edits_are_never_overwritten_silently(self) -> None:
        make_pdf(self.inputs / "paper.pdf", 1)
        self.ingest("run", "--route", "local", "--tier", "flash", str(self.inputs))
        source_id = self.record()["items"][0]["target"]
        document = self.root / "references" / "extracted" / source_id / "document.md"
        document.write_text(document.read_text(encoding="utf-8") + "A correction typed by hand.\n", encoding="utf-8")
        self.assertEqual(self.ingest("run", "--route", "local", "--tier", "basic", "--reconvert", str(self.inputs)).returncode, 1)
        item = self.record()["items"][0]
        self.assertEqual((item["status"], item["error_code"]), ("failed", "edited"))
        self.assertIn("A correction typed by hand.", document.read_text(encoding="utf-8"))
        self.assertEqual(self.ingest("run", "--route", "local", "--tier", "basic", "--reconvert", "--overwrite-edited", str(self.inputs)).returncode, 0)

    def test_the_reading_status_and_added_readme_text_survive_reconversion(self) -> None:
        make_pdf(self.inputs / "paper.pdf", 1)
        self.ingest("run", "--route", "local", "--tier", "flash", str(self.inputs))
        source_id = self.record()["items"][0]["target"]
        index = self.root / "references" / "index.md"
        index.write_text(index.read_text(encoding="utf-8").replace("| collected |", "| relevant |"), encoding="utf-8")
        readme = self.root / "references" / "extracted" / source_id / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\nChecked against the printed copy by the researcher.\n", encoding="utf-8")
        self.ingest("run", "--route", "local", "--tier", "basic", "--reconvert", str(self.inputs))
        self.assertIn("| relevant |", index.read_text(encoding="utf-8"))
        self.assertIn("Checked against the printed copy", readme.read_text(encoding="utf-8"))
        self.assertIn("revision 2", readme.read_text(encoding="utf-8"))

    def test_plan_changes_nothing_and_a_route_is_required(self) -> None:
        make_pdf(self.inputs / "paper.pdf", 1)
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*"))
        plan = self.ingest("plan", "--route", "local", str(self.inputs))
        self.assertEqual(plan.returncode, 0)
        self.assertIn("to convert", plan.stdout)
        self.assertEqual(sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*")), before)
        refused = self.ingest("run", str(self.inputs))
        self.assertEqual(refused.returncode, 3)
        self.assertIn("processing route", refused.stdout)

    def test_a_running_import_blocks_a_second_one(self) -> None:
        make_pdf(self.inputs / "paper.pdf", 1)
        lock = self.root / ".tmp" / "ingest.lock"
        lock.parent.mkdir(parents=True)
        lock.write_text(f"{os.getpid()} now\n", encoding="utf-8")
        result = self.ingest("run", "--route", "local", "--tier", "flash", str(self.inputs))
        self.assertEqual(result.returncode, 3)
        self.assertIn("another import", result.stdout)


class MetadataTests(WorkspaceTestCase):
    def setUp(self) -> None:
        super().setUp()
        make_pdf(self.inputs / "paper.pdf", 1)
        self.ingest("run", "--route", "local", "--tier", "flash", str(self.inputs))
        self.source_id = self.record()["items"][0]["target"]
        self.bib = self.root / "references" / "bibliography.bib"

    def test_entry_key_escaping_and_index(self) -> None:
        result = self.ingest("metadata", self.source_id, "--type", "article", "--title", "Ünder 50% of cases & more_things",
                             "--author", "Müller, Anna", "--author", "Lee, B.", "--year", "2024", "--doi", "10.1000/a_b")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("muller2024under", result.stdout)
        text = self.bib.read_text(encoding="utf-8")
        self.assertIn("title = {Ünder 50\\% of cases \\& more\\_things}", text)
        self.assertIn("doi = {10.1000/a_b}", text)
        self.assertIn(f"sourceid = {{{self.source_id}}}", text)
        self.assertIn("metadatasource = {document}", text)
        self.assertIn("| Müller, Anna; Lee, B. | 2024 |", (self.root / "references" / "index.md").read_text(encoding="utf-8"))
        self.ingest("metadata", self.source_id, "--field", "volume=3", "--field", "relatedsource=src-000000000000")
        text = self.bib.read_text(encoding="utf-8")
        self.assertEqual(text.count("@article{muller2024under,"), 1)
        self.assertIn("volume = {3}", text)
        self.assertIn("relatedsource = {src-000000000000}", text)

    def test_a_cited_key_is_kept(self) -> None:
        self.ingest("metadata", self.source_id, "--title", "First Title", "--author", "Smith, J.", "--year", "2020")
        (self.root / "manuscript" / "01-introduction.md").write_text("As shown before [@smith2020first].\n", encoding="utf-8")
        result = self.ingest("metadata", self.source_id, "--key", "smith2020renamed")
        self.assertIn("kept the key smith2020first", result.stdout)
        self.assertIn("@misc{smith2020first,", self.bib.read_text(encoding="utf-8"))


class ReviewTests(WorkspaceTestCase):
    def test_a_review_round_keeps_comments_changes_and_annotations(self) -> None:
        make_docx(self.inputs / "decision letter.docx")
        make_pdf(self.inputs / "report 2.pdf", 1, annotation=b"/Contents (Please add a scale bar \\(see Fig. 1\\).) /T <FEFF00520032>")
        result = self.ingest("run", "--route", "local", "--tier", "flash", "--to", "reviews/test-journal/round-1", str(self.inputs))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        round_folder = self.root / "reviews" / "test-journal" / "round-1"
        letter = (round_folder / "extracted" / "markdown" / "decision-letter.md").read_text(encoding="utf-8")
        self.assertIn("Reviewer 1", letter)
        self.assertIn("### Comment 1 (Reviewer 1, 2026-09-01)", letter)
        self.assertIn("On the text: \u201cclaim is too strong\u201d", letter)
        self.assertIn("### Comment 2 (Author, 2026-09-03), a reply to comment 1", letter)
        self.assertIn("Inserted by Reviewer 1, 2026-09-01, paragraph 3: \u201cper group\u201d", letter)
        self.assertIn("Deleted by Reviewer 1, 2026-09-01, paragraph 3: \u201c overall\u201d", letter)
        report = (round_folder / "extracted" / "markdown" / "report-2.md").read_text(encoding="utf-8")
        self.assertIn("Text annotation by R2: \u201cPlease add a scale bar (see Fig. 1).\u201d", report)
        self.assertTrue((round_folder / "extracted" / "assets" / "report-2--page_0_image_3.jpg").is_file())
        self.assertIn("](../assets/report-2--page_0_image_3.jpg)", report)
        for folder in ("reviews/test-journal", "reviews/test-journal/round-1", "reviews/test-journal/round-1/originals",
                       "reviews/test-journal/round-1/extracted", "reviews/test-journal/round-1/extracted/markdown",
                       "reviews/test-journal/round-1/extracted/assets"):
            self.assertTrue((self.root / folder / "README.md").is_file(), folder)
        self.assertEqual({item["role"] for item in self.record()["items"]}, {"review"})
        self.assertNotIn("Incomplete extraction", letter)
        again = self.ingest("run", "--route", "local", "--tier", "flash", "--to", "reviews/test-journal/round-1", str(self.inputs))
        self.assertEqual(again.returncode, 0)
        self.assertEqual(set(self.statuses(self.record()).values()), {"already-imported"})
        self.assertEqual(sorted(p.name for p in (round_folder / "originals").iterdir()), ["README.md", "decision letter.docx", "report 2.pdf"])
        readmes = subprocess.run([sys.executable, str(SCRIPTS / "check_readmes.py"), str(self.root)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(readmes.returncode, 0, readmes.stdout)


class UnitTests(unittest.TestCase):
    def test_math_normalization_changes_delimiters_only(self) -> None:
        text = "A \\(x_1\\) b.\n\\[\ny = 1\n\n\\]\nAfter.\n$$z$$\n```\n$ not math \\(\n```\nCost $5 only.\n$\\bm{v}$\n"
        result, stats = extraction.normalize_math(text)
        self.assertIn("A $x_1$ b.", result)
        self.assertIn("\n\n$$\ny = 1\n$$\n\nAfter.", result)
        self.assertIn("\n\n$$\nz\n$$\n", result)
        self.assertIn("```\n$ not math \\(\n```", result)
        self.assertEqual(len(stats["unbalanced_lines"]), 1)
        self.assertEqual(stats["unsupported"][0]["command"], "\\bm{")
        self.assertEqual(stats["display"], 2)

    def test_pdf_page_count_and_annotations(self) -> None:
        folder = Path(tempfile.mkdtemp(prefix="pdf test "))
        self.addCleanup(shutil.rmtree, folder, ignore_errors=True)
        self.assertEqual(pdf.page_count(make_pdf(folder / "plain.pdf", 7)), 7)
        self.assertEqual(pdf.page_count(make_pdf(folder / "packed.pdf", 4, compressed=True)), 4)
        self.assertIsNone(pdf.page_count(folder / "missing.pdf"))
        notes = pdf.annotations(make_pdf(folder / "notes.pdf", 1, annotation=b"/Contents <FEFF00C40062> /T (Rev \\050A\\051)"))
        self.assertEqual(notes, [{"type": "Text", "text": "Äb", "author": "Rev (A)"}])
        packed = pdf.annotations(make_pdf(folder / "packed notes.pdf", 1, annotation=b"/Contents (Hidden in a stream)", compressed=True))
        self.assertEqual(packed[0]["text"], "Hidden in a stream")

    def test_word_structures(self) -> None:
        folder = Path(tempfile.mkdtemp(prefix="docx test "))
        self.addCleanup(shutil.rmtree, folder, ignore_errors=True)
        found = reviews.docx_structures(make_docx(folder / "review.docx"))
        self.assertEqual([c["anchor"] for c in found["comments"]], ["claim is too strong", ""])
        self.assertEqual(found["comments"][1]["reply_to"], 1)
        self.assertEqual([c["text"] for c in found["insertions"]], ["per group"])
        self.assertEqual([c["text"] for c in found["deletions"]], [" overall"])
        (folder / "broken.docx").write_bytes(b"not a zip")
        self.assertIn("error", reviews.docx_structures(folder / "broken.docx"))

    def test_review_destinations_are_validated(self) -> None:
        self.assertEqual(reviews.parse_destination("reviews/j-x/round-2/"), ("j-x", "round-2"))
        for bad in ("reviews/J X/r1", "reviews/../r1", "references/x", "reviews/a"):
            with self.assertRaises(ValueError):
                reviews.parse_destination(bad)


if __name__ == "__main__":
    unittest.main()
