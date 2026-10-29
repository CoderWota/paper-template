"""A scripted integration pass over the complete path: source → idea → result → manuscript → output → review → revision.

It runs the workspace scripts in sequence on a copy of the template's records, with synthetic, clearly labeled
material, and checks that each stage's output is what the next stage reads. It exercises the deterministic layer only:
the agent's judgment, a researcher's decisions, and fresh sessions of either agent are not part of it. The build stage
needs Pandoc and pandoc-crossref and is skipped without them.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
REPOSITORY = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from export import tools  # noqa: E402

TEMPLATE_FOLDERS = ("requirements", "research", "ideas", "manuscript", "references", "outputs", "reviews", "revisions", "state", "inbox")
INFO = tools.find(REPOSITORY)
HAVE_PANDOC = bool(INFO["pandoc"] and INFO["crossref"]) and not tools.problems(INFO, False)


class CompletePathTest(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="complete path ä "))
        self.addCleanup(self.cleanup)
        self.root = self.base / "论文 workspace (synthetic test)"
        for folder in TEMPLATE_FOLDERS:
            shutil.copytree(REPOSITORY / folder, self.root / folder, ignore=shutil.ignore_patterns("*.docx", "*.pdf", "preview"))
        (self.root / "outputs" / "preview").mkdir()
        shutil.copy2(REPOSITORY / ".gitignore", self.root / ".gitignore")
        if (REPOSITORY / ".tools").is_dir():
            os.symlink(REPOSITORY / ".tools", self.root / ".tools")
        empty = self.base / "empty gitconfig"
        empty.write_text("", encoding="utf-8")
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=str(empty), GIT_CONFIG_NOSYSTEM="1")
        self.env.pop("MINERU_API_TOKEN", None)

    def cleanup(self) -> None:
        for path in self.base.rglob("*"):
            if path.is_file() and not path.is_symlink():
                os.chmod(path, 0o644)
        shutil.rmtree(self.base, ignore_errors=True)

    def script(self, name: str, *args: str, ok: tuple = (0,)) -> str:
        result = subprocess.run([sys.executable, str(SCRIPTS / name), "--root", str(self.root), *args], capture_output=True,
                                text=True, encoding="utf-8", env=self.env, timeout=600)
        self.assertIn(result.returncode, ok, f"{name} {' '.join(args)}\n{result.stdout}\n{result.stderr}")
        return result.stdout

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_the_stages_connect_through_the_shared_records(self) -> None:
        # Literature: a synthetic source read directly, with citation metadata.
        source = self.base / "inputs" / "synthetic heat study.md"
        source.parent.mkdir()
        source.write_text("# A synthetic heat study (test material)\n\nNight temperatures in the synthetic city rose by 1.2 degrees.\n", encoding="utf-8")
        self.script("ingest.py", "run", str(source))
        source_id = next(p.name for p in (self.root / "references" / "originals").iterdir() if p.name.startswith("src-"))
        self.script("ingest.py", "metadata", source_id, "--type", "article", "--title", "A synthetic heat study", "--author",
                    "Doe, Jane", "--year", "2024", "--key", "doe2024heat")
        self.write(f"references/notes/{source_id}.md", "# 证据笔记\n\n- 主张：夜间温度上升\n- 引文：\"Night temperatures in the synthetic city rose by 1.2 degrees.\"\n")

        # Ideas, plan, decision, venue.
        self.write("ideas/heat-and-sleep.md", "# 城市热与睡眠\n\n- Status: developed\n- Retained: 2026-10-29; “保留这个想法”\n")
        self.write("ideas/index.md", "# 想法索引\n\n- [城市热与睡眠](heat-and-sleep.md)：developed\n")
        self.write("research/plan.md", "# 研究计划（合成测试）\n\n## 工作项\n\n| ID | 工作 | 状态 |\n| --- | --- | --- |\n| W1 | 计算平均值 | done |\n")
        self.write("research/venues/journal-of-synthetic-tests.md", "# Journal of Synthetic Tests\n\n- Checked: 2026-10-29\n"
                   "- Sources:\n  - https://example.org/journal-of-synthetic-tests/guide (synthetic author guide)\n")
        self.write("research/venues/index.md", "# Venues\n\n- [Journal of Synthetic Tests](journal-of-synthetic-tests.md)\n")
        self.write("research/decisions/0001-target-journal-of-synthetic-tests.md", "# 0001 投稿目标\n\n- Date: 2026-10-29\n- Status: active\n"
                   "- Choice: Journal of Synthetic Tests\n- Scope: 投稿目标\n- Confirmed: 2026-10-29; “就投这个期刊”\n")
        self.write("research/decisions/index.md", "# 决定索引\n\n- [0001](0001-target-journal-of-synthetic-tests.md) 投稿目标：有效\n")

        # A result from a recorded run.
        self.script("research.py", "code-init", "--part", "src", "--part", "data", "--part", "runs", "--part", "outputs")
        self.write("code/data/raw/temperatures.csv", "night,temperature\n1,20.1\n2,21.3\n3,21.0\n")
        self.write("code/src/mean.py", "import json,sys\nrows=[float(l.split(',')[1]) for l in open(sys.argv[1]).read().splitlines()[1:]]\n"
                   "json.dump({'mean': round(sum(rows)/len(rows), 2)}, open(sys.argv[2], 'w'))\n")
        run = self.script("research.py", "run", "--name", "night mean", "--note", "synthetic test data", "--input", "code/data/raw/temperatures.csv",
                          "--output", "code/outputs/mean.json", "--", sys.executable, "code/src/mean.py", "code/data/raw/temperatures.csv", "code/outputs/mean.json")
        lines = [line for line in run.splitlines() if line.startswith(("  - `", "- Run:"))]
        self.write("research/results/r001-night-mean.md", "# r001 夜间平均温度（合成测试）\n\n- Status: checked\n- Kind: computational\n- Question: 平均值\n"
                   "- Method: `code/src/mean.py`\n- Inputs:\n" + lines[0] + "\n- Outputs:\n" + lines[1] + "\n" + lines[2] +
                   "\n- Checks: 手算 20.8，一致\n- Limitations: 合成数据\n- Used by: manuscript/02-results.md\n")
        self.write("research/results/index.md", "# 结果\n\n- [r001](r001-night-mean.md)：checked\n")
        self.assertIn("required form", self.script("research.py", "check"))

        # The manuscript cites the source and reports the checked result.
        self.write("manuscript/metadata.yaml", "title: \"A synthetic test manuscript\"\nlang: en-GB\n")
        self.write("manuscript/01-introduction.md", "# Introduction\n\nNight temperatures rose [@doe2024heat]. @sec:results reports the mean in @eq:mean.\n")
        self.write("manuscript/02-results.md", "# Results\n\nThe mean night temperature was 20.8 degrees.\n\n$$\n\\bar{t} = \\frac{1}{3}\\sum_{i=1}^{3} t_i\n$$\n\n{#eq:mean}\n")
        self.script("manuscript.py", "set-sections", "01-introduction.md", "02-results.md")
        self.write("manuscript/manifest.yaml", (self.root / "manuscript" / "manifest.yaml").read_text(encoding="utf-8").replace("version: 1\n", "version: 1\nmetadata: metadata.yaml\n", 1))
        self.assertIn("Citation keys resolve", self.script("manuscript.py", "check"))
        self.write("outputs/checks/2026-10-29-audit.md", "# 审查（合成测试）\n\n无阻断问题。\n")
        self.script("manuscript.py", "record-check", "--name", "Audit", "--kind", "audit", "--input", "manuscript/01-introduction.md",
                    "--input", "manuscript/02-results.md", "--result", "passed", "--summary", "synthetic audit", "--report", "outputs/checks/2026-10-29-audit.md")

        # Output and release.
        if HAVE_PANDOC:
            self.script("export.py", "profile-init", "--id", "journal-of-synthetic-tests", "--name", "Journal of Synthetic Tests (synthetic)")
            built = self.script("export.py", "build", "--profile", "journal-of-synthetic-tests")
            self.assertIn("[pass] native equations: 1 formula(s)", built)
            self.script("export.py", "release", "--profile", "journal-of-synthetic-tests", "--id", "2026-10-round-1")
            self.assertTrue((self.root / "outputs" / "releases" / "2026-10-round-1" / "release.json").is_file())

        # A review round, answered with a recorded change.
        letter = self.base / "inputs" / "decision letter.md"
        letter.write_text("# Decision\n\nReviewer 1\n\n1. Please state the number of nights.\n", encoding="utf-8")
        self.script("ingest.py", "run", "--to", "reviews/journal-of-synthetic-tests/round-1", str(letter))
        self.write("manuscript/02-results.md", (self.root / "manuscript" / "02-results.md").read_text(encoding="utf-8").replace(
            "was 20.8 degrees.", "was 20.8 degrees over three nights."))
        self.write("reviews/journal-of-synthetic-tests/round-1/changes.md", "# Changes\n\n## C1 Number of nights\n\n- Items: R1.1\n"
                   "- Location: `manuscript/02-results.md`\n- Change: stated the number of nights\n- Status: done\n")
        self.write("reviews/journal-of-synthetic-tests/round-1/response.md", "# Response\n\n## R1.1 Number of nights\n\n- Reviewer: Reviewer 1\n"
                   "- Source: `extracted/markdown/decision-letter.md`, item 1\n- Comment: \"Please state the number of nights.\"\n"
                   "- Status: addressed\n- Response: We now state that the mean covers three nights.\n- Change: C1\n")
        self.assertIn("no problems", self.script("review.py", "check"))
        self.assertIn("stale", self.script("manuscript.py", "checks", ok=(2,)))

        # A major revision with a recoverable baseline, then a saved version.
        self.script("manuscript.py", "revision-start", "--id", "2026-11-scope")
        candidate = self.root / "revisions" / "2026-11-scope" / "candidate"
        candidate.mkdir()
        (candidate / "01-introduction.md").write_text("# Introduction\n\nNight temperatures rose [@doe2024heat], with consequences for sleep. "
                                                      "@sec:results reports the mean in @eq:mean.\n", encoding="utf-8")
        self.script("manuscript.py", "revision-apply", "--id", "2026-11-scope")
        self.assertIn("consequences for sleep", (self.root / "manuscript" / "01-introduction.md").read_text(encoding="utf-8"))
        self.script("versions.py", "init")
        self.script("versions.py", "identity", "--name", "Test Researcher", "--email", "test@localhost")
        saved = self.script("versions.py", "save", "--message", "合成测试：完整路径", "--all")
        self.assertIn("nothing was sent anywhere", saved)

        status = json.loads(self.script("status.py", "--json"))
        self.assertEqual(status["results"], {"checked": 1})
        self.assertEqual(status["review_rounds"][0]["answered"], 1)
        self.assertEqual(status["revisions"], ["2026-11-scope: applied"])
        if HAVE_PANDOC:
            self.assertIn("rebuild the formatted output (submission-assembly)", status["next_steps"])

        # A revision made in place stays open in the project status until it is completed.
        self.script("manuscript.py", "revision-start", "--id", "2026-12-wording")
        self.assertIn("continue the open major revision (manuscript-revision)", json.loads(self.script("status.py", "--json"))["next_steps"])
        self.script("manuscript.py", "revision-complete", "--id", "2026-12-wording", "--note", "wording only")
        status = json.loads(self.script("status.py", "--json"))
        self.assertEqual(status["revisions"], ["2026-11-scope: applied", "2026-12-wording: completed"])
        self.assertNotIn("continue the open major revision (manuscript-revision)", status["next_steps"])


if __name__ == "__main__":
    unittest.main()
