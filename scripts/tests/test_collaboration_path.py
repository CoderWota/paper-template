"""Deterministic handoffs for researcher-led collaboration, using original synthetic fixtures.

Questions, choices, interpretations and prose below are scripted test inputs, not model decisions or real consent.
These cases test artifact compatibility, freshness, negative evidence and author-edit protection, not research quality.
No acceptance records, agent memories, external services or researcher's files enter the temporary workspaces.
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
REPOSITORY = SCRIPTS.parent


class CollaborationPathTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="collaboration 合成 test "))
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)
        self.root = self.base / "paper workspace"
        for folder in ("requirements", "research", "ideas", "manuscript", "references", "outputs", "state", "revisions"):
            shutil.copytree(REPOSITORY / folder, self.root / folder,
                            ignore=shutil.ignore_patterns("*.docx", "*.pdf", "preview"))
        self.write("requirements/project.md", "# Synthetic project\n\nStatus: initialized.\n\n"
                   "Fixture only: interaction and manuscript language English; no venue selected.\n")

    def write(self, name: str, text: str) -> Path:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def read(self, name: str) -> str:
        return (self.root / name).read_text(encoding="utf-8")

    def script(self, name: str, *args: str, code: int = 0) -> str:
        completed = subprocess.run([sys.executable, str(SCRIPTS / name), "--root", str(self.root), *args],
                                   capture_output=True, text=True, encoding="utf-8", timeout=60)
        self.assertEqual(completed.returncode, code, completed.stdout + completed.stderr)
        return completed.stdout

    def digest(self, name: str) -> str:
        return hashlib.sha256((self.root / name).read_bytes()).hexdigest()

    def audit(self, name: str, result: str, inputs: list[str], report: str) -> None:
        path = f"outputs/checks/{name}.md"
        self.write(path, report)
        arguments = [arg for item in inputs for arg in ("--input", item)]
        self.script("manuscript.py", "record-check", "--name", name, "--kind", "audit", *arguments,
                    "--result", result, "--summary", "synthetic evidence and wording check", "--report", path)

    def test_computation_negative_result_resume_and_author_edit(self) -> None:
        # A fixture question/choice is kept separate from an unsupported causal interpretation.
        self.write("research/plan.md", "# Synthetic plan\n\nQuestion: What is the paired mean change?\n\n"
                   "Fixture choice: compute the arithmetic mean of the listed pairs; no causal conclusion.\n\n"
                   "W1 agent: compute change, check by hand, produce result and figure.\n"
                   "W2 researcher: decide whether a broader causal study is worth proposing; pending.\n")
        self.script("research.py", "code-init", "--part", "src", "--part", "data", "--part", "outputs")
        self.write("code/data/raw/pairs.csv", "before,after\n1,2\n2,1\n3,3\n")
        self.write("code/src/change.py", "raise ValueError('synthetic parser failure')\n")
        arguments = ("run", "--name", "paired change", "--input", "code/data/raw/pairs.csv",
                     "--output", "code/outputs/change.json", "--output", "manuscript/assets/change.svg",
                     "--timeout", "10", "--", sys.executable, "code/src/change.py")
        self.script("research.py", *arguments, code=1)
        failed = next((self.root / "code/runs").glob("*/run.json"))
        failed_bytes = failed.read_bytes()
        self.assertIn("synthetic parser failure", (failed.parent / "stderr.txt").read_text(encoding="utf-8"))

        self.write("code/src/change.py", "import csv,json\nfrom pathlib import Path\n"
                   "rows=list(csv.DictReader(Path('code/data/raw/pairs.csv').open()))\n"
                   "delta=sum(float(r['after'])-float(r['before']) for r in rows)/len(rows)\n"
                   "Path('code/outputs/change.json').write_text(json.dumps({'mean_change':delta,'n':len(rows)}))\n"
                   "Path('manuscript/assets/change.svg').write_text("
                   "'<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"240\" height=\"60\">"
                   "<text x=\"5\" y=\"30\">Mean change: '+str(delta)+'</text></svg>')\n")
        self.script("research.py", *arguments)
        self.assertEqual(json.loads(self.read("code/outputs/change.json")), {"mean_change": 0.0, "n": 3})
        self.assertEqual(failed.read_bytes(), failed_bytes)
        run = next(p for p in (self.root / "code/runs").glob("*/run.json") if p != failed)
        result_path = "research/results/r001-change.md"
        self.write(result_path, "# r001 Synthetic paired change\n\n- Status: checked\n- Kind: computational\n"
                   "- Question: paired mean change\n- Method: arithmetic mean; code/src/change.py\n- Inputs:\n"
                   f"  - `code/data/raw/pairs.csv` sha256:{self.digest('code/data/raw/pairs.csv')}\n- Outputs:\n"
                   f"  - `code/outputs/change.json` sha256:{self.digest('code/outputs/change.json')}\n"
                   f"  - `manuscript/assets/change.svg` sha256:{self.digest('manuscript/assets/change.svg')}\n"
                   f"- Run: `{run.relative_to(self.root).as_posix()}`\n"
                   "- Checks: hand calculation (1 - 1 + 0) / 3 = 0, matches output and figure.\n"
                   "- Limitations: original synthetic pairs; no inference to populations or causality.\n"
                   "- Used by: `manuscript/01-results.md`, `manuscript/assets/change.svg`, result audit\n"
                   "- Researcher review: not yet (all choices above are fixture inputs)\n\n"
                   "Observation: mean change is zero. Interpretation: these pairs do not show a positive mean change.\n"
                   "Hypothesis: an effect in another population remains untested.\n\n"
                   f"Technical repair: original failure preserved at `{failed.relative_to(self.root).as_posix()}`; one parser repair.\n")
        self.write("research/results/index.md", "# Results\n\n- [r001](r001-change.md): checked\n")
        self.script("research.py", "check")
        self.write("manuscript/01-results.md", "# Results\n\nThe paired mean change was 0 across 3 synthetic pairs.\n\n"
                   "![Paired mean change in the synthetic fixture.](assets/change.svg){#fig:change}\n\n"
                   "[TODO: a causal claim needs a separately chosen study design and evidence]\n")
        self.script("manuscript.py", "set-sections", "01-results.md")
        inputs = ["manuscript/01-results.md", result_path, "code/src", "code/data/raw/pairs.csv", "manuscript/assets/change.svg"]
        self.audit("initial-result-audit", "findings", inputs, "# Synthetic audit\n\n"
                   "F1: the causal extension has no evidence. Keep it as a gap; do not replace the agreed descriptive claim.\n")
        self.write("state/current.md", "# Synthetic checkpoint\n\nGoal: descriptive result and checked paragraph.\n"
                   f"Done: [{result_path}](../{result_path}), initial-result-audit.\n"
                   "Pending choice W2: a different causal study; no authorization.\n"
                   "Next: check current descriptive text and its open marker; no rerun needed.\n")
        run_count = len(list((self.root / "code/runs").glob("*/run.json")))
        plan_before = self.read("research/plan.md")
        # A fresh CLI process reads existing state; it neither starts work nor consumes the pending choice.
        status = json.loads(self.script("status.py", "--json"))
        self.assertEqual((status["results"], status["stale_results"], status["manuscript"]["open_items"]), ({"checked": 1}, 0, 1))
        self.assertEqual(len(list((self.root / "code/runs").glob("*/run.json"))), run_count)
        self.assertEqual(self.read("research/plan.md"), plan_before)

        # The scripted author's local edit must survive a staged, bounded wording revision.
        self.script("manuscript.py", "revision-start", "--id", "wording")
        before = self.read("manuscript/01-results.md")
        candidate = "revisions/wording/candidate/01-results.md"
        revised = before.replace("The paired mean change", "The observed paired mean change")
        self.write(candidate, revised)
        author_note = "\nThese synthetic observations describe only the listed pairs.\n"
        self.write("manuscript/01-results.md", before + author_note)
        self.script("manuscript.py", "revision-apply", "--id", "wording", code=3)
        self.assertEqual(self.read("manuscript/01-results.md"), before + author_note)
        self.write(candidate, revised + author_note)
        self.script("manuscript.py", "revision-apply", "--id", "wording", "--reconciled", "manuscript/01-results.md")
        self.assertIn(author_note, self.read("manuscript/01-results.md"))
        self.audit("rechecked-result", "findings", inputs, "# Follow-up synthetic audit\n\n"
                   "F1 remains a visible research gap. The descriptive observation and figure match the checked output; author wording retained.\n")
        # An upstream data change must name affected prose and exhibit and invalidate recorded checks.
        self.write("code/data/raw/pairs.csv", "before,after\n1,2\n2,1\n3,6\n")
        stale = self.script("research.py", "check", code=2)
        self.assertIn("manuscript/01-results.md", stale)
        self.assertIn("manuscript/assets/change.svg", stale)
        self.assertIn("code/data/raw/pairs.csv", self.script("manuscript.py", "checks", code=2))
        self.assertGreater(json.loads(self.script("status.py", "--json"))["stale_results"], 0)
        self.assertIn(author_note, self.read("manuscript/01-results.md"))

    def test_documentary_comparison_correction_and_changed_source(self) -> None:
        # Original, rights-cleared test sources, not fabricated publications or a claimed literature search.
        documents = {
            "a": "# Synthetic record A\n\n## Finding\nIn the north sample, 2 of 4 entries mention shade.\n",
            "b": "# Synthetic record B\n\n## Finding\nIn the south sample, 0 of 4 entries mention shade.\n",
        }
        source_paths = []
        for name, content in documents.items():
            source = self.base / f"synthetic-record-{name}.md"
            source.write_text(content, encoding="utf-8")
            self.script("ingest.py", "run", str(source))
        ids = sorted(p.name for p in (self.root / "references/originals").glob("src-*") if p.is_dir())
        self.assertEqual(len(ids), 2)
        for source_id in ids:
            source_path = f"references/extracted/{source_id}/document.md"
            source_paths.append(source_path)
            text = self.read(source_path)
            self.assertTrue("2 of 4" in text or "0 of 4" in text)
            self.write(f"references/notes/{source_id}.md", "# Synthetic evidence note\n\n"
                       f"Source: `{source_path}`, section Finding; original Markdown inspected.\n"
                       "Observed source statement: " + text.split("## Finding\n", 1)[1].strip() + "\n\n"
                       "Interpretation: occurrence of a word is not evidence of cooling or causal efficacy.\n"
                       "Search scope: only the two supplied test records; no novelty conclusion.\n")
        self.write("research/plan.md", "# Synthetic comparison plan\n\n"
                   "Fixture choice: compare mentions in the two supplied records, not effectiveness.\n"
                   "Pending: whether to study actual cooling; no new question has been adopted.\n")
        output = self.write("research/comparison.md", "# Synthetic comparison\n\n"
                            "Observation: north 2/4, south 0/4.\n"
                            "Interpretation: the records differ in mentions.\n"
                            "Hypothesis: climate may explain the difference; not tested.\n"
                            "Alternative: reporting practices may differ; not tested.\n")
        result = "research/results/r001-records.md"
        self.write(result, "# r001 Synthetic comparison\n\n- Status: checked\n- Kind: documentary\n"
                   "- Question: how do mentions differ?\n- Method: compare the Finding sections of two original synthetic records\n- Inputs:\n" +
                   "".join(f"  - `{p}` sha256:{self.digest(p)}\n" for p in source_paths) +
                   f"- Outputs:\n  - `research/comparison.md` sha256:{self.digest('research/comparison.md')}\n"
                   "- Checks: compared both original Markdown statements to the extraction and comparison; contrary south observation retained\n"
                   "- Limitations: two synthetic records; no causal inference or exhaustive literature search\n"
                   "- Used by: `manuscript/01-comparison.md`, source-support audit\n- Researcher review: not yet\n")
        self.write("research/results/index.md", "# Results\n\n- [r001](r001-records.md): checked\n")
        self.script("research.py", "check")
        initial = "# Comparison\n\nThe supplied records report shade mentions in 2 of 4 north entries and 0 of 4 south entries.\n\n"
        self.write("manuscript/01-comparison.md", initial + "[TODO: cooling effectiveness needs different evidence]\n")
        self.script("manuscript.py", "set-sections", "01-comparison.md")
        self.audit("source-support", "findings", ["manuscript/01-comparison.md", result, *source_paths],
                   "# Synthetic audit\n\nF1: mentions do not measure cooling. Retain the comparison; remove the proposed efficacy extension if requested.\n")
        self.write("state/current.md", "# Synthetic checkpoint\n\nGoal: compare the supplied records and revise wording.\n"
                   f"Result: {result}; source-support audit has F1.\n"
                   "Next: bounded wording correction; a cooling study remains a separate pending choice.\n")
        self.assertEqual(json.loads(self.script("status.py", "--json"))["sources"], 2)
        # Scripted fixture authorization for this local wording correction, not new research consent.
        corrected = initial + "These mentions do not establish cooling effectiveness.\n"
        self.write("manuscript/01-comparison.md", corrected)
        self.script("manuscript.py", "check")
        self.audit("source-support-rechecked", "passed", ["manuscript/01-comparison.md", result, *source_paths],
                   "# Follow-up synthetic audit\n\nF1 addressed: comparison retained, unsupported extension replaced with its limitation. Both originals rechecked.\n")
        self.assertEqual(self.read("manuscript/01-comparison.md"), corrected)
        self.assertFalse((self.root / "code").exists())
        self.assertTrue(output.is_file())
        originals = {p: p.read_bytes() for p in (self.root / "references/originals").rglob("*.md")}
        self.write(source_paths[0], self.read(source_paths[0]) + "\nDerived extraction changed.\n")
        self.assertIn("manuscript/01-comparison.md", self.script("research.py", "check", code=2))
        self.script("manuscript.py", "checks", code=2)
        self.assertTrue(all(p.read_bytes() == content for p, content in originals.items()))
        self.assertEqual(self.read("manuscript/01-comparison.md"), corrected)


if __name__ == "__main__":
    unittest.main()
