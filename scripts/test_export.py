"""Exercise demonstrated export failures with synthetic material and local tools only."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from export import docx, tools

SCRIPT = Path(__file__).with_name("export.py")
spec = importlib.util.spec_from_file_location("paper_export", SCRIPT)
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        self.output = self.root / "paper.docx"
        self.output.write_bytes(b"synthetic DOCX for mocked application calls")
        self.info = {"word": True, "libreoffice": "soffice"}

    def tearDown(self):
        self.temporary.cleanup()

    def render(self, run, selected="libreoffice"):
        with patch.object(tools, "find", return_value=self.info), \
                patch.object(subprocess, "run", side_effect=run), contextlib.redirect_stdout(io.StringIO()):
            return exporter.render(self.root, self.output, selected)

    def successful_run(self, command, **kwargs):
        self.assertIn("--headless", command)
        self.assertTrue(any(c.startswith("-env:UserInstallation=file:") for c in command))
        target = Path(command[command.index("--outdir") + 1]) / "paper.pdf"
        target.write_bytes(b"%PDF-1.7 synthetic application result")
        return subprocess.CompletedProcess(command, 0, "converted", "")

    def test_explicit_libreoffice_bypasses_available_word_and_tracks_hashes(self):
        self.assertEqual(self.render(self.successful_run), self.output.with_suffix(".pdf"))
        self.assertTrue(exporter.current_render(self.output))
        self.output.write_bytes(b"changed DOCX")
        self.assertFalse(exporter.current_render(self.output))

    def test_previous_pdf_cannot_mask_no_output_or_nonzero_exit(self):
        self.render(self.successful_run)
        for code in (0, 1):
            with self.subTest(code=code):
                self.assertIsNone(self.render(lambda command, **kw: subprocess.CompletedProcess(command, code, "", "")))
                self.assertFalse(exporter.current_render(self.output))

    def test_timeout_is_reported_without_accepting_previous_pdf(self):
        self.render(self.successful_run)

        def timeout(command, **kwargs):
            raise subprocess.TimeoutExpired(command, 55)

        self.assertIsNone(self.render(timeout))
        self.assertFalse(exporter.current_render(self.output))

    def test_changed_docx_during_render_is_rejected(self):
        def change(command, **kwargs):
            result = self.successful_run(command, **kwargs)
            self.output.write_bytes(b"edited during render")
            return result

        self.assertIsNone(self.render(change))
        self.assertFalse(exporter.current_render(self.output))

    def test_modified_pdf_invalidates_receipt(self):
        self.render(self.successful_run)
        self.output.with_suffix(".pdf").write_bytes(b"another PDF")
        self.assertFalse(exporter.current_render(self.output))

    def test_unavailable_selected_renderer_does_not_switch(self):
        self.info["libreoffice"] = None
        with patch.object(tools, "find", return_value=self.info), \
                patch.object(subprocess, "run") as run, contextlib.redirect_stdout(io.StringIO()):
            self.assertIsNone(exporter.render(self.root, self.output, "libreoffice"))
            run.assert_not_called()


class LocalBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.info = tools.find(SCRIPT.parent.parent)
        if not cls.info["pandoc"] or not cls.info["crossref"]:
            raise unittest.SkipTest("installed Pandoc and pandoc-crossref are required")

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name).resolve()
        (self.root / "manuscript").mkdir()
        (self.root / "manuscript/manifest.yaml").write_text("version: 1\nsections: [01-test.md]\n")
        self.section = self.root / "manuscript/01-test.md"
        self.section.write_text("# Results\n\nSynthetic material.\n")
        self.assertEqual(self.cli("profile-init", "--id", "test", "--name", "Test output"), 0)
        self.preview = self.root / "outputs/preview/test"

    def tearDown(self):
        self.temporary.cleanup()

    def cli(self, *args):
        with patch.object(tools, "find", return_value=self.info), contextlib.redirect_stdout(io.StringIO()):
            return exporter.main(["--root", str(self.root), *args])

    def record(self):
        return json.loads((self.preview / "build.json").read_text())

    def test_raw_html_table_without_reference_is_blocked(self):
        self.section.write_text("# Results\n\n<table>\n<tr><th colspan=\"2\">Group</th></tr>\n"
                                "<tr><td>Estimate</td><td>-0.42</td></tr>\n</table>\n")
        self.assertEqual(self.cli("build", "--profile", "test"), 1)
        raw = next(c for c in self.record()["checks"] if c["name"] == "raw content")
        self.assertTrue(raw["blocking"])
        self.assertFalse(raw["passed"])
        self.assertIn("html", raw["detail"])
        self.assertEqual(self.cli("verify", "--profile", "test"), 1)
        readme = self.root / "release-README.md"
        readme.write_text("Synthetic failed-build release.\n")
        self.assertEqual(self.cli("release", "--profile", "test", "--id", "failed",
                                  "--readme", str(readme)), 3)

    def test_native_table_caption_and_reference_survive(self):
        self.section.write_text("# Results\n\nSee @tbl:estimates.\n\n"
                                "| Variable | Estimate |\n|---|---:|\n| Sample A | -0.42 |\n\n"
                                ": Estimates {#tbl:estimates}\n")
        self.assertEqual(self.cli("build", "--profile", "test"), 0)
        citations = next(c for c in self.record()["checks"] if c["name"] == "citations")
        self.assertIn("no keyed citations", citations["detail"])
        text = docx.text_of(self.preview / "manuscript.docx")
        self.assertIn("-0.42", text)
        self.assertNotIn("¿", text)
        self.assertEqual(self.cli("verify", "--profile", "test"), 0)
        self.section.write_text(self.section.read_text() + "\nA new current edit.\n")
        self.assertEqual(self.cli("verify", "--profile", "test"), 1)

    def test_render_failure_fails_requested_build_but_keeps_mechanical_record(self):
        with patch.object(exporter, "render", return_value=None):
            self.assertEqual(self.cli("build", "--profile", "test", "--render", "--renderer", "word"), 1)
        self.assertEqual(self.record()["status"], "passed")
        self.assertTrue((self.preview / "manuscript.docx").is_file())

    def test_exporter_change_invalidates_build(self):
        script = self.root / "scripts/export.py"
        script.parent.mkdir()
        script.write_text("# exporter version one\n")
        self.assertEqual(self.cli("build", "--profile", "test"), 0)
        script.write_text("# exporter version two\n")
        self.assertEqual(self.cli("verify", "--profile", "test"), 1)

    def test_html_comment_is_not_output_loss(self):
        self.section.write_text("# Results\n\n<!-- editorial note -->\n\nVisible text.\n")
        self.assertEqual(self.cli("build", "--profile", "test"), 0)

    def test_comments_cannot_hide_intervening_raw_content(self):
        ast = {"blocks": [{"t": "RawBlock", "c": ["html", "<!-- before --><table></table><!-- after -->"]}]}
        self.assertTrue(docx.ast_facts(ast)["raw_content"])

    def test_release_does_not_include_old_pdf_without_matching_receipt(self):
        self.assertEqual(self.cli("build", "--profile", "test"), 0)
        (self.preview / "manuscript.pdf").write_bytes(b"old PDF")
        readme = self.root / "release-README.md"
        readme.write_text("Synthetic DOCX release; PDF was not checked.\n")
        self.assertEqual(self.cli("release", "--profile", "test", "--id", "checked",
                                  "--readme", str(readme)), 0)
        release = self.root / "outputs/releases/checked"
        self.assertTrue((release / "manuscript.docx").is_file())
        self.assertFalse((release / "manuscript.pdf").exists())


if __name__ == "__main__":
    unittest.main()
