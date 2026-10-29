"""Tests for scripts/research.py: research record checks, the research code folder, and recorded runs.

The records are synthetic and written in Chinese and English, the way an agent writes them for a researcher.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
RESEARCH = SCRIPTS / "research.py"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ResearchTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="research test ä "))
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)
        self.root = self.base / "workspace é"
        for folder in ("research/decisions", "research/feedback", "research/results", "research/venues", "ideas"):
            (self.root / folder).mkdir(parents=True)

    def research(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(RESEARCH), "--root", str(self.root), *args], capture_output=True,
                              text=True, encoding="utf-8", timeout=120)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def assertCheck(self, code: int, *fragments: str) -> str:
        result = self.research("check")
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        for fragment in fragments:
            self.assertIn(fragment, result.stdout)
        return result.stdout


DECISION_1 = """# 0001 将语料限定为 2010–2024 年

- Date: 2026-10-20
- Status: replaced
- Replaced by: [0002](0002-extend-corpus-to-2000.md)
- Choice: 只分析 2010–2024 年的报道
- Scope: 语料范围
- Confirmed: 2026-10-20；“就用 2010 到 2024 年的报道”

## Context

早期报道的数字化程度不一。
"""

DECISION_2 = """# 0002 将语料扩展到 2000 年

- 日期：2026-10-27
- 状态：有效
- 选择：语料扩展到 2000–2024 年
- 适用范围：语料范围
- 确认：2026-10-27；“改用 2000 年以后的全部报道”
- 取代：[0001](0001-limit-corpus-to-2010.md)
"""

INDEX = """# 决定索引

| 编号 | 决定 | 范围 | 状态 |
| --- | --- | --- | --- |
| [0001](0001-limit-corpus-to-2010.md) | 语料限定为 2010–2024 年 | 语料范围 | 已被 [0002](0002-extend-corpus-to-2000.md) 取代 |
| [0002](0002-extend-corpus-to-2000.md) | 语料扩展到 2000 年 | 语料范围 | 有效 |
"""


class DecisionTests(ResearchTestCase):
    def test_replacement_chain_in_chinese_and_english_labels_passes(self) -> None:
        self.write("research/decisions/0001-limit-corpus-to-2010.md", DECISION_1)
        self.write("research/decisions/0002-extend-corpus-to-2000.md", DECISION_2)
        self.write("research/decisions/index.md", INDEX)
        self.assertCheck(0, "required form")

    def test_missing_quote_one_sided_replacement_and_index_gaps_are_reported(self) -> None:
        self.write("research/decisions/0001-limit-corpus-to-2010.md", DECISION_1.replace("“就用 2010 到 2024 年的报道”", "研究者同意"))
        self.write("research/decisions/0002-extend-corpus-to-2000.md", DECISION_2.replace("- 取代：[0001](0001-limit-corpus-to-2010.md)\n", ""))
        self.write("research/decisions/index.md", INDEX.replace("已被 [0002](0002-extend-corpus-to-2000.md) 取代", "已被取代")
                   .replace("| [0002](0002-extend-corpus-to-2000.md) | 语料扩展到 2000 年 | 语料范围 | 有效 |\n", ""))
        self.write("research/decisions/Decision three.md", "# x\n")
        self.assertCheck(1, "0001-limit-corpus-to-2010.md: the Confirmed line must quote",
                         "0002-extend-corpus-to-2000.md does not name it in its Replaces line",
                         "index.md: 0002-extend-corpus-to-2000.md is not listed",
                         "the line for 0001-limit-corpus-to-2010.md must link to the decision that replaces it",
                         "Decision three.md: name a decision record NNNN-short-title.md")

    def test_unknown_status_and_missing_fields_are_reported(self) -> None:
        self.write("research/decisions/0001-choose-method.md", "# 0001 x\n\n- Date: yesterday\n- Status: pending\n- Choice: survey\n")
        self.write("research/decisions/index.md", "# Index\n\n- [0001](0001-choose-method.md)\n")
        self.assertCheck(1, "unknown status", "expected one Scope line", "expected one Confirmed line", "needs a date")


ACTIONS = """# 行动：2026-10-20 组会

## F1 收窄研究问题

- From: 王老师
- Source: 会议记录第 2 段
- Kind: 研究者回忆
- Suggestion: 把问题收窄到城市样本
- Affects: requirements/project.md 的研究问题
- Status: 已采纳
- Decision: 2026-10-21；“就按王老师的建议收窄到城市”

## F2 Add a robustness check

- From: Li (co-researcher)
- Source: `originals/comments.docx`, comment 3
- Kind: exact statement
- Suggestion: "Please add a placebo test."
- Status: implemented
- Decision: 2026-10-22; "Yes, add the placebo test"
- Change: [the result record](../../results/r002-placebo.md)

## F3 Use a different outline

- From: Chen (coauthor)
- Source: `originals/outline.docx`
- Kind: agent summary
- Suggestion: move the case study before the theory section
- Status: under discussion
"""


class FeedbackTests(ResearchTestCase):
    def test_attributed_actions_with_decisions_and_changes_pass(self) -> None:
        self.write("research/feedback/2026-10-20-group-meeting/actions.md", ACTIONS)
        self.write("research/results/r002-placebo.md", "# r002\n")
        self.write("research/results/index.md", "# Results\n\n- [r002](r002-placebo.md)\n")
        output = self.research("check").stdout
        self.assertNotIn("research/feedback", output)

    def test_adoption_without_the_researchers_words_and_unlinked_changes_are_reported(self) -> None:
        text = (ACTIONS.replace("- Decision: 2026-10-21；“就按王老师的建议收窄到城市”\n", "")
                .replace("[the result record](../../results/r002-placebo.md)", "done")
                .replace("- Kind: agent summary", "- Kind: paraphrase")
                .replace("## F3 Use", "## Use"))
        self.write("research/feedback/2026-10-20-group-meeting/actions.md", text)
        self.write("research/feedback/Group Meeting/README.md", "# x\n")
        self.assertCheck(1, "F1: the suggestion is adopted, so it needs a Decision line",
                         "F2: the suggestion is implemented, so it needs a Change line",
                         "must start with a suggestion ID",
                         "research/feedback/Group Meeting: name a feedback folder",
                         "research/feedback/Group Meeting: actions.md is missing")

    def test_a_change_link_must_exist_and_statuses_are_known(self) -> None:
        text = ACTIONS.replace("- Status: under discussion", "- Status: accepted")
        self.write("research/feedback/2026-10-20-group-meeting/actions.md", text)
        self.assertCheck(1, "the change ../../results/r002-placebo.md does not exist", "F3: unknown status")


class IdeaTests(ResearchTestCase):
    def test_index_statuses_and_links(self) -> None:
        self.write("ideas/urban-sample.md", "# 城市样本\n\n- Status: 探索中\n- Question: ...\n")
        self.write("ideas/placebo.md", "# Placebo\n\n- Status: maybe\n")
        self.write("ideas/index.md", "# 想法索引\n\n- [城市样本](urban-sample.md)：探索中\n- 农村对照：已放弃\n- [缺失](missing.md)\n")
        self.assertCheck(1, "ideas/placebo.md: not listed", "ideas/placebo.md: unknown status",
                         "links to missing.md, which does not exist", "names no status")

    def test_valid_index_passes(self) -> None:
        self.write("ideas/urban-sample.md", "# 城市样本\n\n- Status: developed\n")
        self.write("ideas/index.md", "# Ideas\n\n- [Urban sample](urban-sample.md) — developed\n")
        self.assertCheck(0)


class ResultAndRunTests(ResearchTestCase):
    def make_analysis(self) -> None:
        (self.root / "code" / "outputs").mkdir(parents=True, exist_ok=True)
        self.write("code/data/raw/测试 数据.csv", "x,y\n1,2\n3,4\n")
        self.write("code/src/mean.py", (
            "import json, sys\n"
            "rows = [line.split(',') for line in open(sys.argv[1], encoding='utf-8').read().splitlines()[1:]]\n"
            "mean = sum(float(r[1]) for r in rows) / len(rows)\n"
            "json.dump({'mean_y': mean}, open(sys.argv[2], 'w', encoding='utf-8'))\n"
            "print('mean computed')\n"))

    def run_analysis(self) -> subprocess.CompletedProcess:
        return self.research("run", "--name", "Mean of y", "--note", "smoke test on labeled test data",
                             "--input", "code/data/raw/测试 数据.csv", "--output", "code/outputs/mean.json", "--",
                             sys.executable, "code/src/mean.py", "code/data/raw/测试 数据.csv", "code/outputs/mean.json")

    def test_code_init_creates_only_requested_parts_and_keeps_added_text(self) -> None:
        result = self.research("code-init", "--part", "src", "--part", "data")
        self.assertEqual(result.returncode, 0, result.stdout)
        for folder in ("code", "code/src", "code/data", "code/data/raw", "code/data/derived"):
            self.assertTrue((self.root / folder / "README.md").is_file(), folder)
        self.assertFalse((self.root / "code" / "notebooks").exists())
        readme = self.root / "code" / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8") + "\nResearcher note: the survey data stay on the lab server.\n", encoding="utf-8")
        self.research("code-init", "--part", "runs")
        text = readme.read_text(encoding="utf-8")
        self.assertIn("Researcher note: the survey data stay on the lab server.", text)
        self.assertIn("[`runs/`](runs/README.md)", text)
        self.assertIn("maintained by scripts/research.py", text)
        readmes = subprocess.run([sys.executable, str(SCRIPTS / "check_readmes.py"), str(self.root)], capture_output=True, text=True, encoding="utf-8")
        self.assertNotIn("code", readmes.stdout)

    def test_a_run_records_command_code_inputs_outputs_and_logs(self) -> None:
        self.research("code-init", "--part", "src", "--part", "data", "--part", "runs", "--part", "outputs")
        self.make_analysis()
        result = self.run_analysis()
        self.assertEqual(result.returncode, 0, result.stdout)
        folder = next((self.root / "code" / "runs").glob("*-mean-of-y"))
        record = json.loads((folder / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(record["status"], "complete")
        self.assertEqual(record["exit_code"], 0)
        self.assertEqual(record["command"][1:], ["code/src/mean.py", "code/data/raw/测试 数据.csv", "code/outputs/mean.json"])
        self.assertEqual(record["inputs"][0]["sha256"], sha(self.root / "code/data/raw/测试 数据.csv"))
        self.assertEqual(record["outputs"][0]["sha256"], sha(self.root / "code/outputs/mean.json"))
        self.assertEqual(record["code"][0]["path"], "code/src")
        self.assertIn("version", record["interpreter"])
        self.assertIn("mean computed", (folder / "stdout.txt").read_text(encoding="utf-8"))
        self.assertTrue((folder / "README.md").is_file())
        self.assertIn(f"`code/outputs/mean.json` sha256:{record['outputs'][0]['sha256']}", result.stdout)
        self.assertEqual(json.loads((self.root / "code/outputs/mean.json").read_text(encoding="utf-8")), {"mean_y": 3.0})

    def test_the_research_environment_is_separate_and_recorded_with_the_run(self) -> None:
        result = self.research("code-init", "--part", "src", "--part", "outputs", "--venv")
        self.assertEqual(result.returncode, 0, result.stdout)
        python = self.root / "code" / ".venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        self.assertTrue(python.exists())
        self.write("code/src/smoke.py", "import sys\nopen('code/outputs/smoke.txt', 'w').write(sys.prefix)\n")
        relative_python = python.relative_to(self.root).as_posix()
        run = self.research("run", "--name", "smoke", "--note", "labeled test data", "--output", "code/outputs/smoke.txt",
                            "--freeze", "--", relative_python, "code/src/smoke.py")
        self.assertEqual(run.returncode, 0, run.stdout)
        record = json.loads(next((self.root / "code" / "runs").glob("*-smoke/run.json")).read_text(encoding="utf-8"))
        self.assertEqual(record["command"][0], relative_python)
        self.assertIn(".venv", record["interpreter"]["resolved"])
        self.assertIn(".venv", (self.root / "code/outputs/smoke.txt").read_text(encoding="utf-8"))
        self.assertTrue((next((self.root / "code" / "runs").glob("*-smoke")) / "environment.txt").is_file())
        self.assertIn("environment.txt", (next((self.root / "code" / "runs").glob("*-smoke")) / "README.md").read_text(encoding="utf-8"))
        again = self.research("code-init", "--venv")
        self.assertIn("already exists", again.stdout)

    def test_failures_and_missing_outputs_are_recorded_and_missing_inputs_refused(self) -> None:
        self.make_analysis()
        failing = self.research("run", "--name", "broken", "--", sys.executable, "-c", "import sys; sys.exit(4)")
        self.assertEqual(failing.returncode, 1)
        record = json.loads(next((self.root / "code" / "runs").glob("*-broken/run.json")).read_text(encoding="utf-8"))
        self.assertEqual((record["status"], record["exit_code"]), ("failed", 4))
        silent = self.research("run", "--name", "silent", "--output", "code/outputs/none.json", "--", sys.executable, "-c", "pass")
        self.assertEqual(silent.returncode, 1)
        self.assertIn("declared outputs are missing: code/outputs/none.json", silent.stdout)
        refused = self.research("run", "--name", "x", "--input", "code/data/raw/absent.csv", "--", sys.executable, "-c", "pass")
        self.assertEqual(refused.returncode, 3)
        self.assertIn("these inputs do not exist", refused.stdout)

    def result_record(self, status: str = "checked", checks: str = "重新运行一次，结果一致；与手算均值 3.0 一致") -> str:
        run = next((self.root / "code" / "runs").glob("*-mean-of-y"))
        record = json.loads((run / "run.json").read_text(encoding="utf-8"))
        return (f"# r001 y 的均值（冒烟测试）\n\n- Status: {status}\n- Kind: computational\n- Question: 测试数据中 y 的均值\n"
                f"- Method: `code/src/mean.py`\n- Inputs:\n  - `code/data/raw/测试 数据.csv` sha256:{record['inputs'][0]['sha256']}\n"
                f"- Outputs:\n  - `code/outputs/mean.json` sha256:{record['outputs'][0]['sha256']}\n"
                f"- Run: `code/runs/{run.name}/run.json`\n- Checks: {checks}\n- Limitations: 测试数据，不是研究数据\n"
                "- Used by: none yet\n- Researcher review: not yet\n")

    def test_result_records_detect_stale_inputs_and_unsupported_checked_status(self) -> None:
        self.make_analysis()
        self.assertEqual(self.run_analysis().returncode, 0)
        self.write("research/results/r001-mean-smoke.md", self.result_record())
        self.write("research/results/index.md", "# 结果索引\n\n- [r001](r001-mean-smoke.md)：已检查\n")
        self.assertCheck(0)
        self.write("code/data/raw/测试 数据.csv", "x,y\n1,2\n3,5\n")
        self.assertCheck(2, "stale: research/results/r001-mean-smoke.md: the input code/data/raw/测试 数据.csv changed")
        self.write("research/results/r001-mean-smoke.md", self.result_record(checks="none").replace("- Run: `code/runs/", "- Run: `code/runs/x"))
        self.write("research/results/r002-orphan.md", "# r002\n\n- Status: observed\n- Kind: computational\n- Question: q\n- Method: m\n- Limitations: l\n")
        self.assertCheck(1, "a checked result says which checks were made", "the run record code/runs/x", "r002-orphan.md is not listed",
                         "an observed result lists its outputs with checksums", "an observed result lists its inputs")

    def test_runs_listing_shows_changed_files(self) -> None:
        self.make_analysis()
        self.run_analysis()
        self.write("code/outputs/mean.json", "{}")
        listing = self.research("runs")
        self.assertIn("complete; changed since the run: code/outputs/mean.json", listing.stdout)

    def test_changed_or_deleted_run_code_makes_the_result_stale_and_names_its_uses(self) -> None:
        self.make_analysis()
        self.assertEqual(self.run_analysis().returncode, 0)
        text = self.result_record().replace("- Used by: none yet", "- 用于：`manuscript/02-results.md`, `manuscript/assets/mean.svg`, audit of results")
        self.write("research/results/r001-mean-smoke.md", text)
        self.write("research/results/index.md", "# Results\n\n- [r001](r001-mean-smoke.md)\n")
        self.assertCheck(0)
        code = self.root / "code/src/mean.py"
        code.write_text(code.read_text(encoding="utf-8") + "\n# changed procedure\n", encoding="utf-8")
        self.assertCheck(2, "code/src changed", "recheck recorded dependents", "manuscript/02-results.md", "manuscript/assets/mean.svg")
        self.assertIn("code/src", self.research("runs").stdout)
        shutil.rmtree(code.parent)
        self.assertCheck(2, "code/src is missing", "recheck recorded dependents")
        self.assertEqual((self.root / "research/results/r001-mean-smoke.md").read_text(encoding="utf-8"), text)

    def test_broken_or_failed_run_is_not_usable_as_a_checked_result(self) -> None:
        self.make_analysis()
        self.assertEqual(self.run_analysis().returncode, 0)
        self.write("research/results/r001-mean-smoke.md", self.result_record())
        self.write("research/results/index.md", "# Results\n\n- [r001](r001-mean-smoke.md)\n")
        path = next((self.root / "code/runs").glob("*/run.json"))
        record = json.loads(path.read_text(encoding="utf-8"))
        path.write_text("{interrupted", encoding="utf-8")
        self.assertCheck(1, "cannot read run record")
        record["status"] = "failed"
        path.write_text(json.dumps(record), encoding="utf-8")
        self.assertCheck(1, "run did not complete")


class VenueTests(ResearchTestCase):
    def test_venue_notes_need_a_date_and_official_addresses(self) -> None:
        self.write("research/venues/journal-a.md", "# Journal A\n\n- Checked: 2026-10-28\n- Sources:\n  - https://example.org/journal-a/guide (author guide)\n")
        self.write("research/venues/journal-b.md", "# Journal B\n\n- Checked: last week\n- Sources: the journal website\n")
        self.write("research/venues/index.md", "# Venues\n\n| Venue | Fit |\n| --- | --- |\n| [A](journal-a.md) | good |\n")
        self.assertCheck(1, "journal-b.md: the Checked line needs the date", "journal-b.md: the Sources line lists the official pages",
                         "research/venues/index.md: journal-b.md is not listed")


if __name__ == "__main__":
    unittest.main()
