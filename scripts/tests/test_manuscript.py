"""Tests for scripts/manuscript.py: convention checks, assembly, check records, and major-revision baselines.

The manuscript fixtures are synthetic and mix English and Chinese, as researchers' manuscripts do.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parent.parent
MANUSCRIPT = SCRIPTS / "manuscript.py"
sys.path.insert(0, str(SCRIPTS))

import manuscript  # noqa: E402
from export import tools  # noqa: E402

PANDOC = tools.find(SCRIPTS.parent)["pandoc"]

MANIFEST_HEADER = "# Manuscript assembly manifest, maintained by the agent.\n# Only listed files are assembled.\n"
INTRO = """# 引言

城市热岛研究很多 [@doe2021synthetic]。@zhang2019fixture 给出了手册。见 @sec:methods-and-data 与 @fig:gradient。

![合成的梯度图。](assets/gradient.png){#fig:gradient width=60%}

A price of US\\$5 stays text, and $y = \\alpha x$ is math.
"""
METHODS = """# Methods and data

The mean is

$$
\\hat{\\mu} = \\frac{1}{n}\\sum_{i=1}^{n} x_i
$$

{#eq:mean}

| Item | Value |
|------|------:|
| Alpha | 1.5 |

: Values used in the test. {#tbl:values}

```mermaid
flowchart LR
    N1["阅读文献"] --> N2["Examine evidence"]
```

: The workflow. {#fig:flow}

See @eq:mean, @tbl:values, @fig:flow, and @sec:引言.
"""
BIB = """@article{doe2021synthetic,
  title = {A Synthetic Study}, author = {Doe, Jane}, year = {2021}
}
@book{zhang2019fixture,
  title = {Fixtures}, author = {Zhang, Wei}, year = {2019}
}
"""


class ManuscriptTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="manuscript test ä "))
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)
        self.root = self.base / "论文 workspace"
        self.write("manuscript/manifest.yaml", MANIFEST_HEADER + "version: 1\nmetadata: metadata.yaml\nsections:\n  - 01-introduction.md\n  - 02-methods.md\n")
        self.write("manuscript/metadata.yaml", "title: \"A synthetic paper\"\nlang: zh-CN\n")
        self.write("manuscript/01-introduction.md", INTRO)
        self.write("manuscript/02-methods.md", METHODS)
        self.write("manuscript/outline.md", "# Outline\n\nNot body text.\n")
        self.write("manuscript/README.md", "# Manuscript\n")
        (self.root / "manuscript" / "assets").mkdir(parents=True, exist_ok=True)
        (self.root / "manuscript" / "assets" / "gradient.png").write_bytes(b"\x89PNG\r\n\x1a\n")
        self.write("references/bibliography.bib", BIB)
        self.write("requirements/writing.md", "# Writing\n\nNo rules yet.\n")

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run_script(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(MANUSCRIPT), "--root", str(self.root), *args], capture_output=True,
                              text=True, encoding="utf-8", timeout=120)


class CheckTests(ManuscriptTestCase):
    def test_multilingual_vocabulary_is_external_to_python_rule_code(self) -> None:
        source = (SCRIPTS / "text_rules.py").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]", source))

    def test_mixed_word_and_cjk_counts_keep_japanese_as_characters(self) -> None:
        words, cjk = manuscript.count_words("English paper. 日本語の論文。中文论文。")
        self.assertEqual(words, 2)
        self.assertEqual(cjk, 10)

    def test_language_rules_cover_english_chinese_japanese_and_fullwidth_digits(self) -> None:
        text = INTRO + "\nFigure 2; figure 3; 图2；圖2；図２。\n図 @fig:gradient。\n"
        self.write("manuscript/01-introduction.md", text)
        result = self.run_script("check")
        self.assertEqual(result.returncode, 0, result.stdout)
        for phrase in ("Figure 2", "figure 3", "图2", "圖2", "図2", "図 @fig:"):
            self.assertIn(f"“{phrase}", result.stdout)

    def test_latex_commands_in_prose_are_problems_and_escapes_are_not(self) -> None:
        self.write("manuscript/01-introduction.md", INTRO + "\nPrior work \\cite{doe2021synthetic} shows \\textbf{large} gains "
                   "(see \\ref{fig:gradient}). It costs 95\\% for R\\&D, with $\\beta$ and `\\cite{code}`.\n\n"
                   "<!-- \\todo{private note} -->\n")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("“\\cite{doe2021synthetic}” is dropped from the Word file; write [@key]", result.stdout)
        self.assertIn("“\\textbf{large}” is dropped from the Word file", result.stdout)
        self.assertIn("“\\ref{fig:gradient}” is dropped from the Word file; write @fig:id", result.stdout)
        for kept in ("\\%", "\\&", "\\beta", "\\cite{code}", "\\todo"):
            self.assertNotIn("“" + kept, result.stdout)

    def test_halfwidth_punctuation_after_chinese_or_japanese_text_is_a_warning(self) -> None:
        self.write("manuscript/01-introduction.md", INTRO + "\n夜间热岛更强,白天较弱.\n\n結果は明確である,次に述べる。\n\n"
                   "결과는, 명확하다. Results, however, vary by 3.5 degrees.\n")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("“,” (usually “，”), “.” (usually “。”)", result.stdout)
        self.assertIn("“,” (usually “、 or ，”)", result.stdout)
        self.assertEqual(result.stdout.count("half-width punctuation"), 2, result.stdout)

    def test_citations_allow_adjacent_cjk_and_japanese_text_without_hiding_unknown_keys(self) -> None:
        self.write("manuscript/01-introduction.md", INTRO.replace(
            "城市热岛研究很多 [@doe2021synthetic]。@zhang2019fixture 给出了手册。",
            "见@fig:gradient。@zhang2019fixtureを参照。"))
        self.assertEqual(self.run_script("check").returncode, 0, self.run_script("check").stdout)
        self.write("manuscript/01-introduction.md", INTRO + "\n见@zhang2019fixturexを参照。\n")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("the citation key @zhang2019fixturex", result.stdout)

    def test_non_english_open_markers_are_explicit_and_ordinary_prose_is_allowed(self) -> None:
        self.write("manuscript/01-introduction.md", INTRO + "\n普通叙述：结果尚未定稿。\n（要確認：补充实验）\n")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Open items (1)", result.stdout)
        self.write("manuscript/01-introduction.md", INTRO + "\n結果は未定ではない。\n")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("Open items", result.stdout)

    def test_ai_signatures_are_reported_with_locations(self) -> None:
        for signature in ("Generated by ChatGPT", "— Claude", "署名：Codex", "由ChatGPT生成", "ChatGPTによる生成"):
            with self.subTest(signature=signature):
                self.write("manuscript/01-introduction.md", INTRO + "\n" + signature + "\n")
                result = self.run_script("check")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("manuscript/01-introduction.md:", result.stdout)
                self.assertIn("possible AI signature", result.stdout)

    def test_ai_author_metadata_is_blocked_but_disclosure_is_allowed(self) -> None:
        for authors in ("author: ChatGPT", "author: [Jane Doe, Claude]", "author:\n  - Jane Doe\n  - Codex"):
            with self.subTest(authors=authors):
                self.write("manuscript/metadata.yaml", "title: A study\n" + authors + "\n")
                result = self.run_script("check")
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("manuscript/metadata.yaml:", result.stdout)
        self.write("manuscript/metadata.yaml", "title: A study of ChatGPT\nauthor: Jane Doe\nabstract: We evaluated Claude.\n")
        self.write("manuscript/01-introduction.md", INTRO + "\nThe authors used ChatGPT to improve language.\n")
        self.assertEqual(self.run_script("check").returncode, 0)

    def test_a_conforming_manuscript_passes(self) -> None:
        result = self.run_script("check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("2 section file(s)", result.stdout)
        self.assertIn("6 label(s), 2 cited key(s), 1 diagram(s)", result.stdout)
        self.assertIn("Citation keys resolve; whether each source supports its claim is a separate check", result.stdout)
        self.assertNotIn("Problems", result.stdout)
        self.assertNotIn("Warnings", result.stdout)

    def test_convention_breaks_are_problems(self) -> None:
        broken = METHODS.replace("$$\n\n{#eq:mean}", "$$ {#eq:mean}") + (
            "\n$$\nx = 1 \\label{eq:x}\n$$\n\n$$\na = b\n\nc = d\n$$\n\n{#eq:stray-after-text}\n\n"
            "See @fig:missing and [@nokey2020].\n\n![Lost](assets/lost.png){#fig:lost}\n\n![Again](assets/gradient.png){#fig:gradient}\n\n$$\nunclosed\n")
        self.write("manuscript/02-methods.md", broken)
        result = self.run_script("check")
        self.assertEqual(result.returncode, 1)
        for fragment in ("the label is on the closing $$ line", "\\label or \\tag inside a formula", "contains a blank line",
                         "@eq:mean refers to no figure", "@fig:missing refers to no figure", "the citation key @nokey2020",
                         "the image assets/lost.png does not exist", "the label fig:gradient is also defined",
                         "a display formula is not closed"):
            self.assertIn(fragment, result.stdout)

    def test_a_label_paragraph_without_a_formula_is_a_problem(self) -> None:
        self.write("manuscript/02-methods.md", METHODS + "\nSome text.\n\n{#eq:orphan}\n")
        result = self.run_script("check")
        self.assertIn("{#eq:orphan} does not follow a display formula", result.stdout)

    def test_manifest_problems_and_drafts(self) -> None:
        self.write("manuscript/manifest.yaml", "version: 1\nsections:\n  - README.md\n  - 01-introduction.md\n  - 01-introduction.md\n  - 09-missing.md\n")
        self.write("manuscript/drafts/alternative-intro.md", "# Draft\n")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("README.md is not a section file and must not be assembled", result.stdout)
        self.assertIn("01-introduction.md is listed twice", result.stdout)
        self.assertIn("manuscript/09-missing.md does not exist", result.stdout)
        self.assertIn("Not assembled (not in the manifest): 02-methods.md, drafts/alternative-intro.md", result.stdout)

    def test_warnings_and_open_items(self) -> None:
        self.write("manuscript/01-introduction.md", INTRO + "\nAs Figure 2 shows, it costs $5. 如图 3 所示。 $$x$$\n\n[TODO: 补充 2023 年的数据]\n")
        result = self.run_script("check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("“Figure 2” looks hand-numbered", result.stdout)
        self.assertIn("“图 3” looks hand-numbered", result.stdout)
        self.assertIn("a dollar sign before a number is read as math", result.stdout)
        self.assertIn("write a display formula with $$ on separate lines", result.stdout)
        self.assertIn("Open items (1)", result.stdout)

    def test_a_missing_bibliography_is_reported(self) -> None:
        (self.root / "references" / "bibliography.bib").unlink()
        result = self.run_script("check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("references/bibliography.bib does not exist", result.stdout)

    def test_set_sections_keeps_the_header_and_refuses_non_sections(self) -> None:
        result = self.run_script("set-sections", "02-methods.md", "01-introduction.md")
        self.assertEqual(result.returncode, 0, result.stdout)
        text = (self.root / "manuscript" / "manifest.yaml").read_text(encoding="utf-8")
        self.assertTrue(text.startswith(MANIFEST_HEADER))
        self.assertIn("metadata: metadata.yaml", text)
        self.assertEqual(manuscript.read_manifest(self.root)["sections"], ["02-methods.md", "01-introduction.md"])
        self.assertEqual(self.run_script("set-sections", "outline.md").returncode, 3)
        self.assertEqual(self.run_script("set-sections", "07-none.md").returncode, 3)

    def test_assemble_joins_only_listed_sections_with_metadata(self) -> None:
        self.write("manuscript/drafts/alternative-intro.md", "# Draft that must not appear\n")
        result = self.run_script("assemble")
        self.assertEqual(result.returncode, 0, result.stdout)
        text = (self.root / "outputs" / "preview" / "manuscript.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\ntitle: \"A synthetic paper\""))
        self.assertLess(text.index("# 引言"), text.index("# Methods and data"))
        self.assertNotIn("Draft that must not appear", text)
        self.assertNotIn("Not body text", text)
        self.assertIn("CJK characters", result.stdout)

    def test_metadata_yaml_is_used_even_when_the_manifest_does_not_name_it(self) -> None:
        self.write("manuscript/manifest.yaml", MANIFEST_HEADER + "version: 1\nsections:\n  - 01-introduction.md\n  - 02-methods.md\n")
        assembled = self.run_script("assemble")
        self.assertEqual(assembled.returncode, 0, assembled.stdout)
        self.assertTrue((self.root / "outputs" / "preview" / "manuscript.md").read_text(encoding="utf-8").startswith("---\ntitle: \"A synthetic paper\""))
        self.write("manuscript/metadata.yaml", "lang: zh-CN\n")
        self.assertIn("manuscript/metadata.yaml: no title", self.run_script("check").stdout)
        self.write("manuscript/manifest.yaml", MANIFEST_HEADER + "version: 1\nmetadata: front.yaml\nsections:\n  - 01-introduction.md\n")
        self.assertIn("the metadata file manuscript/front.yaml does not exist", self.run_script("check").stdout)


class CheckRecordTests(ManuscriptTestCase):
    def test_a_changed_input_makes_a_recorded_check_stale(self) -> None:
        self.write("outputs/checks/audit-1.md", "# 审查\n\n无问题。\n")
        recorded = self.run_script("record-check", "--name", "Audit of methods", "--kind", "audit", "--input", "manuscript/02-methods.md",
                                   "--input", "references/bibliography.bib", "--result", "passed", "--summary", "No findings",
                                   "--report", "outputs/checks/audit-1.md")
        self.assertEqual(recorded.returncode, 0, recorded.stdout)
        self.assertTrue((self.root / "outputs" / "checks" / "README.md").is_file())
        listing = self.run_script("checks")
        self.assertEqual(listing.returncode, 0)
        self.assertIn("(current)", listing.stdout)
        self.write("manuscript/02-methods.md", METHODS + "\nA new claim.\n")
        listing = self.run_script("checks")
        self.assertEqual(listing.returncode, 2)
        self.assertIn("stale: manuscript/02-methods.md changed", listing.stdout)
        self.assertEqual(self.run_script("record-check", "--name", "x", "--kind", "audit", "--input", "nothing.md", "--result", "passed",
                                         "--summary", "x").returncode, 3)


class RevisionTests(ManuscriptTestCase):
    def test_baseline_candidate_conflict_reconciliation_and_restore(self) -> None:
        started = self.run_script("revision-start", "--id", "2026-11-argument")
        self.assertEqual(started.returncode, 0, started.stdout)
        folder = self.root / "revisions" / "2026-11-argument"
        baseline = json.loads((folder / "baseline.json").read_text(encoding="utf-8"))
        self.assertIn("manuscript/01-introduction.md", baseline["files"])
        self.assertIn("references/bibliography.bib", baseline["files"])
        self.assertNotIn("manuscript/README.md", baseline["files"])
        self.assertTrue((folder / "baseline" / "manuscript" / "02-methods.md").is_file())
        self.assertEqual(self.run_script("revision-start", "--id", "2026-11-argument").returncode, 3)
        self.assertEqual(self.run_script("revision-start", "--id", "Bad ID").returncode, 3)
        candidate = folder / "candidate"
        shutil.copytree(self.root / "manuscript", candidate, ignore=shutil.ignore_patterns("README.md", "outline.md", "assets"))
        (candidate / "01-introduction.md").write_text(INTRO.replace("城市热岛研究很多", "修订后的论证"), encoding="utf-8")
        self.write("manuscript/01-introduction.md", INTRO + "\n作者在修订期间加的一句。\n")
        status = self.run_script("revision-status", "--id", "2026-11-argument")
        self.assertIn("Changed since the baseline: manuscript/01-introduction.md", status.stdout)
        self.assertIn("to reconcile before applying: manuscript/01-introduction.md", status.stdout)
        refused = self.run_script("revision-apply", "--id", "2026-11-argument")
        self.assertEqual(refused.returncode, 3)
        self.assertIn("not reconciled with the candidate: manuscript/01-introduction.md", refused.stdout)
        (candidate / "01-introduction.md").write_text(INTRO.replace("城市热岛研究很多", "修订后的论证") + "\n作者在修订期间加的一句。\n", encoding="utf-8")
        applied = self.run_script("revision-apply", "--id", "2026-11-argument", "--reconciled", "manuscript/01-introduction.md")
        self.assertEqual(applied.returncode, 0, applied.stdout)
        text = (self.root / "manuscript" / "01-introduction.md").read_text(encoding="utf-8")
        self.assertIn("修订后的论证", text)
        self.assertIn("作者在修订期间加的一句", text)
        kept = list((folder / "replaced").glob("*/manuscript/01-introduction.md"))
        self.assertEqual(len(kept), 1)
        self.assertIn("作者在修订期间加的一句", kept[0].read_text(encoding="utf-8"))
        self.assertTrue((self.root / "revisions/2026-11-argument/replaced/README.md").is_file())
        self.assertEqual(self.run_script("revision-apply", "--id", "2026-11-argument").returncode, 3)
        restored = self.run_script("revision-restore", "--id", "2026-11-argument")
        self.assertEqual(restored.returncode, 0, restored.stdout)
        self.assertEqual((self.root / "manuscript" / "01-introduction.md").read_text(encoding="utf-8"), INTRO)
        readmes = subprocess.run([sys.executable, str(SCRIPTS / "check_readmes.py"), str(self.root)], capture_output=True, text=True, encoding="utf-8")
        self.assertNotIn("revisions/2026-11-argument/baseline/", readmes.stdout)

    def test_an_in_place_revision_is_closed_with_a_record_that_shows_what_is_left(self) -> None:
        self.assertEqual(self.run_script("revision-start", "--id", "r1").returncode, 0)
        folder = self.root / "revisions" / "r1"
        self.assertEqual(self.run_script("record-check", "--name", "Audit of methods", "--kind", "audit", "--input", "manuscript/02-methods.md",
                                         "--result", "passed", "--summary", "No findings").returncode, 0)
        self.write("manuscript/01-introduction.md", INTRO.replace("城市热岛研究很多", "修订后的论证"))
        self.write("manuscript/02-methods.md", METHODS + "\nA new claim. [TODO: add the evidence]\n")
        self.assertFalse((folder / "closed.json").exists())
        done = self.run_script("revision-complete", "--id", "r1", "--note", "scope narrowed to cities")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertIn("recorded as completed (in place)", done.stdout)
        self.assertIn("0 problem(s) and 1 open marker(s), and 1 recorded check(s) are stale", done.stdout)
        self.assertIn("does not hide this", done.stdout)
        record = json.loads((folder / "closed.json").read_text(encoding="utf-8"))
        self.assertEqual((record["outcome"], record["mode"], record["note"]), ("completed", "in place", "scope narrowed to cities"))
        self.assertEqual(record["remaining"], {"problems": 0, "open_markers": 1, "stale_checks": 1})
        self.assertIn("Closed: completed on", self.run_script("revision-status", "--id", "r1").stdout)
        again = self.run_script("revision-complete", "--id", "r1")
        self.assertEqual(again.returncode, 3)
        self.assertIn("already completed", again.stdout)
        self.assertEqual(self.run_script("revision-complete", "--id", "never-started").returncode, 3)

    def test_a_revision_with_an_unapplied_candidate_or_an_interrupted_application_is_not_completed(self) -> None:
        self.assertEqual(self.run_script("revision-start", "--id", "r2").returncode, 0)
        folder = self.root / "revisions" / "r2"
        (folder / "candidate").mkdir()
        (folder / "candidate" / "01-introduction.md").write_text("# New introduction\n", encoding="utf-8")
        refused = self.run_script("revision-complete", "--id", "r2")
        self.assertEqual(refused.returncode, 3)
        self.assertIn("1 file(s) that were not applied", refused.stdout)
        self.assertFalse((folder / "closed.json").exists())
        (folder / "apply.json").write_text(json.dumps({"status": "in progress", "operations": []}), encoding="utf-8")
        interrupted = self.run_script("revision-complete", "--id", "r2")
        self.assertEqual(interrupted.returncode, 3)
        self.assertIn("interrupted", interrupted.stdout)
        (folder / "apply.json").unlink()
        self.assertEqual(self.run_script("revision-apply", "--id", "r2").returncode, 0)
        done = self.run_script("revision-complete", "--id", "r2")
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual(json.loads((folder / "closed.json").read_text(encoding="utf-8"))["mode"], "candidate")

    def test_restoring_the_baseline_records_the_revision_as_abandoned(self) -> None:
        self.assertEqual(self.run_script("revision-start", "--id", "r3").returncode, 0)
        self.write("manuscript/01-introduction.md", INTRO + "\nAn edit that the researcher drops.\n")
        restored = self.run_script("revision-restore", "--id", "r3")
        self.assertEqual(restored.returncode, 0, restored.stdout)
        self.assertIn("recorded as abandoned", restored.stdout)
        record = json.loads((self.root / "revisions" / "r3" / "closed.json").read_text(encoding="utf-8"))
        self.assertEqual((record["outcome"], record["mode"]), ("abandoned", "in place"))
        self.assertIn("Closed: abandoned on", self.run_script("revision-status", "--id", "r3").stdout)
        self.assertEqual(self.run_script("revision-complete", "--id", "r3").returncode, 3)
        readmes = subprocess.run([sys.executable, str(SCRIPTS / "check_readmes.py"), str(self.root)], capture_output=True, text=True, encoding="utf-8")
        self.assertNotIn("revisions/r3", readmes.stdout)

    def test_an_interrupted_application_is_detected_and_resumed(self) -> None:
        self.assertEqual(self.run_script("revision-start", "--id", "r1").returncode, 0)
        folder = self.root / "revisions" / "r1"
        candidate = folder / "candidate"
        candidate.mkdir()
        (candidate / "01-introduction.md").write_text("# New introduction\n", encoding="utf-8")
        (candidate / "02-methods.md").write_text("# New methods\n", encoding="utf-8")
        (candidate / "03-discussion.md").write_text("# Discussion\n", encoding="utf-8")
        real_copy, calls = shutil.copy2, []

        def failing_copy(source, target, *args, **kwargs):
            if Path(target).name.startswith(".applying-"):
                calls.append(target)
                if len(calls) == 2:
                    raise OSError("simulated interruption")
            return real_copy(source, target, *args, **kwargs)

        with mock.patch.object(manuscript.shutil, "copy2", side_effect=failing_copy):
            with self.assertRaises(OSError):
                manuscript.main(["--root", str(self.root), "revision-apply", "--id", "r1"])
        log = json.loads((folder / "apply.json").read_text(encoding="utf-8"))
        self.assertEqual(log["status"], "in progress")
        self.assertEqual([op["done"] for op in log["operations"]], [True, False, False])
        status = self.run_script("revision-status", "--id", "r1")
        self.assertIn("interrupted after 1 of 3 file(s)", status.stdout)
        self.assertNotIn("Edited in manuscript/", status.stdout)
        completed = self.root / "manuscript/01-introduction.md"
        completed.write_text("# An intervening edit after application\n", encoding="utf-8")
        self.assertIn("Edited in manuscript/", self.run_script("revision-status", "--id", "r1").stdout)
        refused_completed = self.run_script("revision-apply", "--id", "r1", "--resume")
        self.assertNotEqual(refused_completed.returncode, 0)
        self.assertEqual(completed.read_text(encoding="utf-8"), "# An intervening edit after application\n")
        completed.write_text("# New introduction\n", encoding="utf-8")
        self.assertIn("continue it with --resume", self.run_script("revision-apply", "--id", "r1").stdout)
        pending = self.root / "manuscript/02-methods.md"
        previous = pending.read_text(encoding="utf-8")
        pending.write_text("# A new author edit\n", encoding="utf-8")
        refused = self.run_script("revision-apply", "--id", "r1", "--resume")
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("without overwriting", refused.stdout)
        self.assertEqual(pending.read_text(encoding="utf-8"), "# A new author edit\n")
        pending.write_text(previous, encoding="utf-8")
        # Crash after replacement but before the operation log was updated.
        pending.write_text("# New methods\n", encoding="utf-8")
        resumed = self.run_script("revision-apply", "--id", "r1", "--resume")
        self.assertEqual(resumed.returncode, 0, resumed.stdout)
        self.assertEqual((self.root / "manuscript" / "02-methods.md").read_text(encoding="utf-8"), "# New methods\n")
        self.assertTrue((self.root / "manuscript" / "03-discussion.md").is_file())
        self.assertEqual(json.loads((folder / "apply.json").read_text(encoding="utf-8"))["status"], "applied")


@unittest.skipUnless(PANDOC, "Pandoc is not installed")
class AdoptionTests(ManuscriptTestCase):
    """An editable manuscript is converted with Pandoc into its import record, then adopted."""

    def setUp(self) -> None:
        super().setUp()
        self.write("manuscript/manifest.yaml", MANIFEST_HEADER + "version: 1\nsections: []\n")
        for name in ("01-introduction.md", "02-methods.md", "metadata.yaml"):
            (self.root / "manuscript" / name).unlink()
        for folder in ("inbox", "inbox/imports", "references", "requirements"):
            (self.root / folder).mkdir(parents=True, exist_ok=True)
        self.write("requirements/privacy.md", "# Privacy\n\nNothing confirmed.\n")
        self.write("references/index.md", "# Reference Index\n\nNo sources.\n")
        self.inputs = self.base / "received files"
        self.inputs.mkdir()
        if (SCRIPTS.parent / ".tools").is_dir():
            os.symlink(SCRIPTS.parent / ".tools", self.root / ".tools")

    def ingest(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SCRIPTS / "ingest.py"), "--root", str(self.root), *args], capture_output=True,
                              text=True, encoding="utf-8", timeout=300)

    def word_file(self, name: str, markdown: str) -> Path:
        source = self.base / f"{name}.md"
        source.write_text(markdown, encoding="utf-8")
        target = self.inputs / f"{name}.docx"
        subprocess.run([PANDOC, str(source), "-o", str(target), "--resource-path", str(self.base)], check=True, capture_output=True)
        return target

    def import_id(self) -> str:
        return sorted(p.name for p in (self.root / "inbox" / "imports").iterdir() if p.is_dir())[-1]

    def test_a_word_manuscript_becomes_sections_with_assets_metadata_and_a_mapping(self) -> None:
        (self.base / "figure.png").write_bytes((self.root / "manuscript" / "assets" / "gradient.png").read_bytes())
        docx = self.word_file("draft", "---\ntitle: 城市热与睡眠\n---\n\n# 引言\n\n城市变暖[^1]，见 $y = \\alpha x$。\n\n[^1]: 脚注里的公式 $a^2$。\n\n"
                              "# Methods\n\n$$\n\\hat{\\mu} = \\frac{1}{n}\\sum_{i=1}^{n} x_i\n$$\n\n![A figure.](figure.png)\n\n| A | B |\n|---|---|\n| 1 | 2 |\n")
        result = self.ingest("run", "--to", "manuscript", "--route", "pandoc", str(docx))
        self.assertEqual(result.returncode, 0, result.stdout)
        folder = self.root / "inbox" / "imports" / self.import_id()
        self.assertTrue((folder / "originals" / "draft.docx").is_file())
        adopted = self.run_script("adopt", "--import-id", self.import_id())
        self.assertEqual(adopted.returncode, 0, adopted.stdout)
        self.assertEqual(manuscript.read_manifest(self.root)["sections"], ["01-section.md", "02-methods.md"])
        introduction = (self.root / "manuscript" / "01-section.md").read_text(encoding="utf-8")
        self.assertIn("# 引言", introduction)
        self.assertIn("[^1]: 脚注里的公式 $a^{2}$。", introduction)
        methods = (self.root / "manuscript" / "02-methods.md").read_text(encoding="utf-8")
        self.assertIn("$$\n\\hat{\\mu} = \\frac{1}{n}\\sum_{i = 1}^{n}x_{i}\n$$", methods)
        self.assertRegex(methods, r"!\[A figure\.\]\(assets/draft--media-[^)]+\.png\)")
        self.assertIn("| A ", methods)
        self.assertIn("title: 城市热与睡眠", (self.root / "manuscript" / "metadata.yaml").read_text(encoding="utf-8"))
        self.assertIn("| `02-methods.md` |", (folder / "mapping.md").read_text(encoding="utf-8"))
        self.assertEqual(self.run_script("check").returncode, 0)
        again = self.run_script("adopt", "--import-id", self.import_id())
        self.assertIn("never over the current manuscript", again.stdout)
        self.assertEqual(self.run_script("revision-start", "--id", "r1").returncode, 0)
        staged = self.run_script("adopt", "--import-id", self.import_id(), "--into", "candidate", "--revision-id", "r1")
        self.assertEqual(staged.returncode, 0, staged.stdout)
        self.assertTrue((self.root / "revisions" / "r1" / "candidate" / "02-methods.md").is_file())

    def test_tracked_changes_stop_adoption_until_the_researcher_decides(self) -> None:
        docx = self.word_file("review", "# Intro\n\nThe claim is strong.\n")
        import zipfile
        patched = self.inputs / "review with changes.docx"
        with zipfile.ZipFile(docx) as source, zipfile.ZipFile(patched, "w") as target:
            for info in source.infolist():
                data = source.read(info.filename)
                if info.filename == "word/document.xml":
                    text = data.decode("utf-8")
                    old = '<w:t xml:space="preserve">The claim is strong.</w:t></w:r>'
                    self.assertIn(old, text)
                    text = text.replace(old, '<w:t xml:space="preserve">The claim is </w:t></w:r>'
                                        '<w:del w:id="91" w:author="Chen" w:date="2026-10-28T09:00:00Z"><w:r><w:delText>strong</w:delText></w:r></w:del>'
                                        '<w:ins w:id="92" w:author="Chen" w:date="2026-10-28T09:00:00Z"><w:r><w:t>moderate</w:t></w:r></w:ins>'
                                        '<w:r><w:t>.</w:t></w:r>')
                    data = text.encode("utf-8")
                target.writestr(info, data)
        first = self.ingest("run", "--to", "manuscript", "--route", "pandoc", str(patched))
        self.assertEqual(first.returncode, 0, first.stdout)
        markdown = self.root / "inbox" / "imports" / self.import_id() / "extracted" / "markdown"
        self.assertIn("1 insertion(s), and 1 deletion(s)", (markdown / "review-with-changes.annotations.md").read_text(encoding="utf-8"))
        refused = self.run_script("adopt", "--import-id", self.import_id())
        self.assertEqual(refused.returncode, 3)
        self.assertIn("tracked-change or comment mark(s)", refused.stdout)
        accepted = self.ingest("run", "--to", "manuscript", "--route", "pandoc", "--track-changes", "accept", "--reconvert", str(patched))
        self.assertEqual(accepted.returncode, 0, accepted.stdout)
        self.assertEqual(self.run_script("adopt", "--import-id", self.import_id()).returncode, 0)
        self.assertIn("The claim is moderate.", (self.root / "manuscript" / "01-intro.md").read_text(encoding="utf-8"))

    def test_a_latex_manuscript_arrives_in_workspace_syntax(self) -> None:
        tex = self.inputs / "paper.tex"
        tex.write_text("\\documentclass{article}\n\\begin{document}\n\\section{Introduction}\\label{intro}\n"
                       "Rising temperatures \\cite[p.~12]{doe2021synthetic}; see Section~\\ref{methods} and \\eqref{mean}.\n"
                       "\\section{Methods}\\label{methods}\n\\begin{equation}\\label{mean}\n\\hat{\\mu} = \\frac{1}{n}\\sum_{i=1}^{n} x_i\n\\end{equation}\n"
                       "\\end{document}\n", encoding="utf-8")
        result = self.ingest("run", "--to", "manuscript", "--route", "pandoc", str(tex))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.run_script("adopt", "--import-id", self.import_id()).returncode, 0)
        introduction = (self.root / "manuscript" / "01-introduction.md").read_text(encoding="utf-8")
        self.assertIn("# Introduction {#sec:intro}", introduction)
        self.assertIn("@sec:methods", introduction)
        self.assertIn("@eq:mean", introduction)
        self.assertIn("$$\n\n{#eq:mean}", (self.root / "manuscript" / "02-methods.md").read_text(encoding="utf-8"))
        check = self.run_script("check")
        self.assertEqual(check.returncode, 0, check.stdout)
        self.assertIn("repeats the word that the output puts before the number", check.stdout)

    def test_the_pandoc_route_is_only_for_the_researchers_manuscript(self) -> None:
        docx = self.word_file("reference", "# A reference\n\nText.\n")
        refused = self.ingest("run", "--route", "pandoc", str(docx))
        self.assertEqual(refused.returncode, 3)
        self.assertIn("only for the researcher's own manuscript", refused.stdout)
        (self.inputs / "scan.pdf").write_bytes(b"%PDF-1.7\n%%EOF\n")
        pdf = self.ingest("run", "--to", "manuscript", "--route", "pandoc", str(self.inputs / "scan.pdf"))
        self.assertIn("converted with MinerU", (self.root / "inbox" / "imports" / self.import_id() / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
