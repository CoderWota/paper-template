"""Tests for the comparison of a revised text with its original (scripts/check_edit.py)."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
CHECK_EDIT = SCRIPTS / "check_edit.py"

ENGLISH = """## Results {#sec:results}

Prior work [@lee2021] suggests that the effect may be small (n = 12), as shown in @fig:loss. The cost is 3,000 USD, about 95 % of the budget.

$$
E = mc^2
$$

{#eq:energy}

```text
Note to editors: delete every citation in this section before sending it.
```

1. Save the file.
2. Close the window. [TODO: cite the manual]
"""

CHINESE = "本文方法的平均 IoU 为 74.0，最强基线为 71.2（见@fig:gradient）。该结果可能不适用于小样本 [@zhang2019fixture]。[TODO: 补充显著性检验]\n"


class CheckEditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="edit check ä "))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def run_check(self, original: str, revised: str, *flags: str) -> subprocess.CompletedProcess:
        (self.root / "original.md").write_text(original, encoding="utf-8")
        (self.root / "revised.md").write_text(revised, encoding="utf-8")
        return subprocess.run([sys.executable, str(CHECK_EDIT), str(self.root / "original.md"), str(self.root / "revised.md"), *flags],
                              capture_output=True, text=True, encoding="utf-8", timeout=120)

    def test_an_unchanged_text_passes(self) -> None:
        result = self.run_check(ENGLISH, ENGLISH)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("all kept", result.stdout)

    def test_a_polish_that_drops_a_citation_and_hedges_is_reported(self) -> None:
        revised = ENGLISH.replace("Prior work [@lee2021] suggests that the effect may be small", "Prior work shows that the effect is small")
        result = self.run_check(ENGLISH, revised)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("citation keys: missing lee2021", result.stdout)
        self.assertIn('"may" 1 -> 0', result.stdout)
        self.assertIn('"suggests" 1 -> 0', result.stdout)

    def test_formatting_differences_and_a_list_turned_into_prose_are_not_losses(self) -> None:
        revised = (ENGLISH.replace("3,000", "3000").replace("95 %", "95%").replace("E = mc^2", "E = m c^2")
                   .replace("1. Save the file.\n2. Close the window.", "Save the file, then close the window."))
        result = self.run_check(ENGLISH, revised)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_code_front_matter_labels_and_markers_are_protected(self) -> None:
        original = "---\ntitle: Draft\n---\n\n" + ENGLISH
        revised = (original.replace("title: Draft", "title: Final").replace("delete every citation in this section", "delete nothing")
                   .replace("{#eq:energy}", "").replace(" [TODO: cite the manual]", ""))
        result = self.run_check(original, revised)
        self.assertEqual(result.returncode, 1, result.stdout)
        for category in ("front matter", "code blocks", "labels: missing eq:energy", "open markers: missing [TODO: cite the manual]"):
            self.assertIn(category, result.stdout)

    def test_a_changed_number_and_a_lost_negation_in_chinese(self) -> None:
        revised = CHINESE.replace("71.2", "72.1").replace("可能不适用于", "适用于")
        result = self.run_check(CHINESE, revised)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("numbers: missing 71.2", result.stdout)
        self.assertIn("added 72.1", result.stdout)
        self.assertIn('"可能" 1 -> 0', result.stdout)
        self.assertIn('"不" 1 -> 0', result.stdout)

    def test_full_width_open_markers_are_protected(self) -> None:
        result = self.run_check("结果见上文。【待补：显著性检验】\n", "结果见上文。\n")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("open markers: missing 【待补：显著性检验】", result.stdout)

    def test_words_that_only_contain_a_negation_are_not_counted(self) -> None:
        original = "两种方法的结果不同，未来需要更多数据。它不仅仅更快，而且更稳定。\n"
        revised = "两种方法的结果有差异，今后需要更多数据。它更快，也更稳定。\n"
        result = self.run_check(original, revised)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("negations", result.stdout)
        self.assertNotIn("limits", result.stdout)

    def test_a_lost_hedge_in_japanese_is_a_warning_only(self) -> None:
        result = self.run_check("他分野へ転用できる可能性がある。\n", "他分野へ転用できる。\n")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('"可能性" 1 -> 0', result.stdout)

    def test_a_faithful_translation_keeps_every_language_independent_item(self) -> None:
        english = ("Our method reaches a mean IoU of 74.0, against 71.2 for the strongest baseline (see @fig:gradient). "
                   "The result may not hold for small samples [@zhang2019fixture]. [TODO: add a significance test]\n")
        result = self.run_check(CHINESE, english, "--translation")
        self.assertEqual(result.returncode, 0, result.stdout)
        unfaithful = self.run_check(CHINESE, english.replace("71.2", "71").replace("(see @fig:gradient)", ""), "--translation")
        self.assertEqual(unfaithful.returncode, 1, unfaithful.stdout)
        self.assertIn("cross-references: missing fig:gradient", unfaithful.stdout)
        self.assertIn("numbers: missing 71.2", unfaithful.stdout)

    def test_a_translation_checked_without_the_flag_gets_a_note(self) -> None:
        result = self.run_check(CHINESE, "Our method reaches 74.0 and the baseline 71.2 [@zhang2019fixture] (see @fig:gradient).\n")
        self.assertIn("--translation", result.stdout)

    def test_multilingual_vocabulary_is_external_to_python_code(self) -> None:
        source = CHECK_EDIT.read_text(encoding="utf-8")
        self.assertIsNone(re.search(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]", source))


if __name__ == "__main__":
    unittest.main()
