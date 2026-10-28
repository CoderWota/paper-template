"""Tests for scripts/check_capabilities.py and scripts/check_requirements.py: each must catch the drift it is for."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent

AGENTS_GOOD = """# AGENTS.md

## Roles

text

## Available now

| Capability | Where | Status |
| --- | --- | --- |
| Set up the project | `project-onboarding` | Available now |
| Import documents | — | Not available yet |

## Decisions and questions

text
"""


class WorkspaceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="records test ä "))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        (self.root / ".agents" / "skills" / "project-onboarding").mkdir(parents=True)
        (self.root / ".agents" / "skills" / "project-onboarding" / "SKILL.md").write_text("x", encoding="utf-8")
        (self.root / "requirements").mkdir()

    def run_script(self, script: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / script), str(self.root)],
            capture_output=True, text=True, encoding="utf-8", timeout=60,
        )


class CapabilityTableTests(WorkspaceTestCase):
    def write_agents(self, text: str) -> None:
        (self.root / "AGENTS.md").write_text(text, encoding="utf-8")

    def test_matching_table_passes(self) -> None:
        self.write_agents(AGENTS_GOOD)
        self.assertEqual(self.run_script("check_capabilities.py").returncode, 0)

    def test_skill_missing_from_table_fails(self) -> None:
        (self.root / ".agents" / "skills" / "literature-discovery").mkdir()
        self.write_agents(AGENTS_GOOD)
        result = self.run_script("check_capabilities.py")
        self.assertEqual(result.returncode, 1)
        self.assertIn("literature-discovery", result.stdout)

    def test_available_row_naming_a_missing_skill_fails(self) -> None:
        self.write_agents(AGENTS_GOOD.replace("`project-onboarding` | Available now", "`ingest-pdfs` | Available now"))
        result = self.run_script("check_capabilities.py")
        self.assertEqual(result.returncode, 1)
        self.assertIn("ingest-pdfs", result.stdout)

    def test_not_available_row_can_name_an_implemented_draft_skill(self) -> None:
        self.write_agents(AGENTS_GOOD.replace("| — | Not available yet", "| `project-onboarding` | Not available yet"))
        result = self.run_script("check_capabilities.py")
        self.assertEqual(result.returncode, 0)

    def test_unknown_status_fails(self) -> None:
        self.write_agents(AGENTS_GOOD.replace("Available now |\n| Import", "Maybe |\n| Import"))
        self.assertEqual(self.run_script("check_capabilities.py").returncode, 1)

    def test_missing_heading_fails(self) -> None:
        self.write_agents("# AGENTS.md\n\nno table here\n")
        self.assertEqual(self.run_script("check_capabilities.py").returncode, 1)


class RequirementRecordTests(WorkspaceTestCase):
    def write_writing(self, text: str) -> None:
        (self.root / "requirements" / "writing.md").write_text(text, encoding="utf-8")

    def rule(self, confirmed: str = "- 确认：2026-10-27；研究者的明确指示（\"以后这篇论文统一用英式拼写。\"）",
             scope: str = "- 适用范围：整篇稿件", extra: str = "") -> str:
        return f"# Writing\n\nIntro text.\n\n## 英式拼写\n\n- 规则：统一使用英式拼写。\n{scope}\n{confirmed}\n{extra}"

    def test_template_text_passes(self) -> None:
        self.write_writing("# Writing Requirements\n\nNo confirmed writing requirements yet.\n")
        self.assertEqual(self.run_script("check_requirements.py").returncode, 0)

    def test_complete_rule_passes(self) -> None:
        self.write_writing(self.rule())
        self.assertEqual(self.run_script("check_requirements.py").returncode, 0)

    def test_confirmed_without_quotation_fails(self) -> None:
        self.write_writing(self.rule(confirmed="- 确认：2026-10-27；研究者的明确指示"))
        result = self.run_script("check_requirements.py")
        self.assertEqual(result.returncode, 1)
        self.assertIn("must quote", result.stdout)

    def test_missing_scope_fails(self) -> None:
        self.write_writing(self.rule(scope=""))
        self.assertEqual(self.run_script("check_requirements.py").returncode, 1)

    def test_missing_scope_names_the_accepted_labels(self) -> None:
        self.write_writing(self.rule(scope=""))
        result = self.run_script("check_requirements.py")
        self.assertEqual(result.returncode, 1)
        self.assertIn("accepted labels", result.stdout)
        self.assertIn("适用范围", result.stdout)

    def test_unlisted_scope_label_fails(self) -> None:
        self.write_writing(self.rule(scope="- 范围：整篇稿件"))
        self.assertEqual(self.run_script("check_requirements.py").returncode, 1)

    def test_exception_without_quotation_fails(self) -> None:
        self.write_writing(self.rule(extra="- 例外：引文保持原拼写。\n"))
        result = self.run_script("check_requirements.py")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Exceptions", result.stdout)

    def test_exception_with_quotation_passes(self) -> None:
        self.write_writing(self.rule(extra="- 例外：\"直接引文保持原拼写。\"\n"))
        self.assertEqual(self.run_script("check_requirements.py").returncode, 0)


if __name__ == "__main__":
    unittest.main()
