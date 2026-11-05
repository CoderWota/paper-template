"""Exercise argument-map version tracking without research material or external services."""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import logic_map
import manuscript
import status as project_status


class LogicMapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        self.target = self.root / "manuscript"
        self.write("manuscript/manifest.yaml", "version: 1\nsections:\n  - 01-argument.md\n")
        self.write("manuscript/01-argument.md", "# Argument\n\nA stated premise supports a conditional conclusion.\n")
        self.write("manuscript/outline.md", "# Outline\n\nPremise, inference, conclusion.\n")
        self.write("manuscript/logic-map.md", '# Argument map\n\n```mermaid\nflowchart TD\n P1["Premise"] -->|is used by| R1["Inference"]\n```\n')
        self.write("requirements/project.md", "# Project\n\nQuestion and scope.\n")
        self.write("requirements/writing.md", "# Writing\n")
        self.write("references/bibliography.bib", "")

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def record(self, inputs=None, target=None, replace=False):
        target = target or self.target
        return logic_map.record(self.root, target, manuscript.logic_map_inputs(self.root, target), inputs or [], replace)

    def state(self, target=None):
        return manuscript.logic_map_state(self.root, target or self.target)

    def cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = manuscript.main(["--root", str(self.root), *args])
        return code, output.getvalue()

    def test_missing_scaffold_unrecorded_and_current(self):
        path = self.target / logic_map.MAP
        original = path.read_text()
        path.unlink()
        self.assertEqual(self.state()["state"], "missing")
        path.write_text(logic_map.SCAFFOLD)
        self.assertEqual(self.state()["state"], "scaffold")
        with self.assertRaises(ValueError):
            self.record()
        path.write_text("# No diagram\n")
        self.assertEqual(self.state()["state"], "invalid")
        path.write_text(original)
        self.assertEqual(self.state()["state"], "unrecorded")
        self.assertEqual(self.record()["state"], "current")

    def test_direct_draft_and_map_edits_are_detected(self):
        self.record()
        self.write("manuscript/01-argument.md", "# Argument\n\nA revised conclusion.\n")
        state = self.state()
        self.assertEqual(state["state"], "stale")
        self.assertIn("target/01-argument.md (changed)", state["changed"])
        self.record()
        with (self.target / logic_map.MAP).open("a") as stream:
            stream.write("\nAuthor's revised interpretation.\n")
        self.assertIn("target/logic-map.md (map edited)", self.state()["changed"])

    def test_planned_argument_before_body_text_can_be_synchronized(self):
        self.write("manuscript/manifest.yaml", "version: 1\nsections: []\n")
        (self.target / "01-argument.md").unlink()
        self.assertEqual(self.record()["state"], "current")
        self.write("manuscript/outline.md", "# Outline\n\nA revised conditional deduction.\n")
        self.assertEqual(self.state()["state"], "stale")

    def test_section_selection_metadata_and_outline_changes(self):
        self.record()
        self.write("manuscript/02-judgment.md", "# Judgment\n")
        self.write("manuscript/manifest.yaml", "version: 1\nsections: [02-judgment.md, 01-argument.md]\n")
        self.assertIn("target/02-judgment.md (added)", self.state()["changed"])
        self.record()
        self.write("manuscript/metadata.yaml", "title: Changed scope\nabstract: A broader claim\n")
        self.assertIn("target/metadata.yaml (added)", self.state()["changed"])
        self.record()
        self.write("manuscript/outline.md", "# Outline\n\nChanged assumption.\n")
        self.assertIn("target/outline.md (changed)", self.state()["changed"])
        self.record()
        self.write("manuscript/manifest.yaml", "version: 1\nsections: [01-argument.md]\n")
        self.assertIn("target/02-judgment.md (no longer selected)", self.state()["changed"])

    def test_shared_dependencies_change_or_disappear(self):
        evidence = self.write("research/results/derivation.md", "# Derivation\n\nPremises imply the conclusion.\n")
        inputs = ["research/results/derivation.md"]
        self.record(inputs)
        self.record()
        self.assertEqual(self.state()["dependencies"], [{"base": "workspace", "path": inputs[0]}])
        evidence.write_text("# Derivation\n\nA missing condition was found.\n")
        self.assertIn("workspace/research/results/derivation.md (changed)", self.state()["changed"])
        self.record(inputs)
        evidence.unlink()
        self.assertIn("workspace/research/results/derivation.md (missing)", self.state()["changed"])
        with self.assertRaises(ValueError):
            self.record(inputs)
        self.record([], replace=True)
        self.assertEqual(self.state()["state"], "current")

    def test_project_requirements_and_bibliography_are_tracked(self):
        self.write("docs/logic-map-guide.md", "# Argument guide\n")
        for name in logic_map.SHARED_INPUTS:
            with self.subTest(name=name):
                self.record()
                with (self.root / name).open("a") as stream:
                    stream.write("\nChanged input.\n")
                self.assertIn(f"workspace/{name} (changed)", self.state()["changed"])

    def test_invalid_record_and_escaping_inputs_are_reported(self):
        self.record()
        record_path = self.target / logic_map.RECORD
        record_path.write_text("{broken")
        self.assertEqual(self.state()["state"], "invalid")
        with self.assertRaises(ValueError):
            self.record()
        self.record(replace=True)
        malformed = json.loads(record_path.read_text())
        malformed["dependencies"] = [{"path": "research/missing-scope.md"}]
        record_path.write_text(json.dumps(malformed))
        self.assertEqual(self.state()["state"], "invalid")
        with self.assertRaises(ValueError):
            self.record()
        self.record(replace=True)
        for name in ("../outside.md", ".env.local", "manuscript/logic-map.md", "manuscript/logic-map.sync.json"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.record([name])
        outside = self.root.parent / (self.root.name + "-outside.md")
        try:
            outside.write_text("Outside the project.\n")
            (self.root / "escaped.md").symlink_to(outside)
            with self.assertRaises(ValueError):
                self.record(["escaped.md"])
            (self.target / logic_map.MAP).unlink()
            (self.target / logic_map.MAP).symlink_to(outside)
            self.assertEqual(self.state()["state"], "invalid")
        finally:
            outside.unlink(missing_ok=True)

    def test_escaping_sync_record_and_invalid_metadata_are_reported(self):
        self.record()
        record_path = self.target / logic_map.RECORD
        outside = self.root.parent / (self.root.name + "-record.json")
        try:
            shutil.copy2(record_path, outside)
            record_path.unlink()
            record_path.symlink_to(outside)
            self.assertEqual(self.state()["state"], "invalid")
            with self.assertRaises(ValueError):
                self.record()
        finally:
            record_path.unlink(missing_ok=True)
            outside.unlink(missing_ok=True)
        self.write("manuscript/manifest.yaml", "version: 1\nmetadata: missing.yaml\nsections: [01-argument.md]\n")
        self.assertEqual(self.state()["state"], "invalid")

    def test_project_status_exposes_sync_state(self):
        self.record()
        self.assertEqual(project_status.facts(self.root)["logic_map_sync"]["state"], "current")
        self.write("manuscript/outline.md", "# Outline\n\nThe author changed an assumption.\n")
        self.assertEqual(project_status.facts(self.root)["logic_map_sync"]["state"], "stale")

    def test_cli_and_check_surface_staleness_without_rewriting_map(self):
        code, output = self.cli("logic-status", "--json")
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output)["state"], "unrecorded")
        self.assertEqual(self.cli("logic-record")[0], 0)
        previous = (self.target / logic_map.MAP).read_bytes()
        self.write("manuscript/01-argument.md", "# Argument\n\nChanged reasoning.\n")
        code, output = self.cli("check")
        self.assertEqual(code, 0)
        self.assertIn("Logic map synchronization: stale", output)
        self.assertEqual((self.target / logic_map.MAP).read_bytes(), previous)

    def test_cli_retains_dependencies_until_explicit_replacement(self):
        evidence = self.write("research/results/argument.md", "# Conditional derivation\n")
        self.assertEqual(self.cli("logic-record", "--input", "research/results/argument.md")[0], 0)
        self.assertEqual(self.cli("logic-record")[0], 0)
        evidence.unlink()
        self.assertEqual(self.cli("logic-record")[0], 3)
        self.assertEqual(self.cli("logic-record", "--replace-inputs")[0], 0)
        self.assertEqual(self.state()["dependencies"], [])

    def test_candidate_map_and_record_apply_together(self):
        self.record()
        self.assertEqual(self.cli("revision-start", "--id", "argument")[0], 0)
        candidate = self.root / "revisions/argument/candidate"
        shutil.copytree(self.target, candidate)
        (candidate / "01-argument.md").write_text("# Argument\n\nA revised, conditional argument.\n")
        with (candidate / logic_map.MAP).open("a") as stream:
            stream.write("\nRevised conditions.\n")
        self.assertEqual(self.state(candidate)["state"], "stale")
        self.assertEqual(self.cli("logic-record", "--revision-id", "argument")[0], 0)
        self.assertEqual(self.state(candidate)["state"], "current")
        self.assertEqual(self.state()["state"], "current")
        self.assertEqual(self.cli("revision-apply", "--id", "argument")[0], 0)
        self.assertEqual(self.state()["state"], "current")

    def test_assembly_excludes_map_and_synchronization_record(self):
        self.record()
        self.assertEqual(self.cli("assemble")[0], 0)
        output = (self.root / "outputs/preview/manuscript.md").read_text()
        self.assertIn("A stated premise", output)
        self.assertNotIn("Argument map", output)
        self.assertNotIn(logic_map.SCHEMA, output)
        self.assertEqual(self.cli("set-sections", "logic-map.md")[0], 3)


if __name__ == "__main__":
    unittest.main()
