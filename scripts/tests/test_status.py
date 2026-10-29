"""Tests for scripts/status.py: stage recognition from the project's records."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent


class StatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="status test ä "))
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)
        self.root = self.base / "论文 workspace"
        self.write("requirements/project.md", "# Project\n\nStatus: not initialized.\n")
        self.write("manuscript/manifest.yaml", "version: 1\nsections: []\n")
        self.write("manuscript/outline.md", "# Outline\n\nNo outline yet.\n")

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def status(self) -> dict:
        result = subprocess.run([sys.executable, str(SCRIPTS / "status.py"), "--root", str(self.root), "--json"], capture_output=True,
                                text=True, encoding="utf-8", timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_a_new_workspace_starts_with_setup_and_literature(self) -> None:
        data = self.status()
        self.assertFalse(data["initialized"])
        self.assertEqual(data["next_steps"][:2], ["set up the project (project-onboarding)", "find and import literature (literature-discovery, source-ingestion)"])

    def test_a_drafted_paper_with_open_review_items_and_feedback(self) -> None:
        self.write("requirements/project.md", "# 项目要求\n\n状态：已初始化（2026-10-28）。\n\n- 投稿目标：Journal A\n")
        self.write("research/plan.md", "# Plan\n")
        self.write("research/results/r001-x.md", "# r001\n\n- Status: checked\n")
        self.write("manuscript/outline.md", "# Outline\n\n1. Introduction\n")
        self.write("manuscript/01-intro.md", "# Introduction\n\nText with an open point. [TODO: add the 2023 data]\n")
        self.write("manuscript/manifest.yaml", "version: 1\nsections:\n  - 01-intro.md\n")
        self.write("reviews/journal-a/round-1/response.md", "# Response\n\n## R1.1 Size\n\n- Status: addressed\n\n## R1.2 Scope\n\n- Status: planned\n")
        self.write("research/feedback/2026-10-20-meeting/actions.md", "# Actions\n\n## F1 x\n\n- Status: received\n")
        data = self.status()
        self.assertTrue(data["initialized"])
        self.assertTrue(data["target_venue_recorded"])
        self.assertEqual(data["results"], {"checked": 1})
        self.assertEqual(data["manuscript"]["open_items"], 1)
        self.assertEqual(data["review_rounds"], [{"round": "journal-a/round-1", "response": True, "items": 2, "answered": 1}])
        steps = "\n".join(data["next_steps"])
        self.assertIn("answer the open review items (review-response)", steps)
        self.assertIn("decide on 1 open feedback suggestion(s)", steps)
        self.assertIn("audit the current manuscript (manuscript-audit)", steps)
        self.assertIn("build a formatted preview (submission-assembly)", steps)
        self.assertNotIn("project-onboarding", steps)

    def test_open_items_are_not_recorded_settings(self) -> None:
        # The venue is listed as still open, and the onboarding of another copy is still in progress.
        self.write("requirements/project.md", "# 项目要求\n\n状态：已初始化（2026-10-29）。目标期刊待定。\n\n## 尚未确定\n\n- 目标期刊\n- 文章类型\n")
        data = self.status()
        self.assertTrue(data["initialized"])
        self.assertFalse(data["target_venue_recorded"])
        self.assertIn("compare possible venues (journal-selection)", data["next_steps"])
        self.write("requirements/project.md", "# 项目要求\n\n状态：初始化进行中（尚未完成）。\n\n- 目标期刊：待定\n")
        data = self.status()
        self.assertFalse(data["initialized"])
        self.assertFalse(data["target_venue_recorded"])
        self.assertEqual(data["next_steps"][0], "set up the project (project-onboarding)")
        self.write("requirements/project.md", "# Project\n\nStatus: initialized on 2026-10-29.\n\n## Target venue\n\nJournal of Synthetic Tests\n")
        self.assertTrue(self.status()["target_venue_recorded"])


if __name__ == "__main__":
    unittest.main()
