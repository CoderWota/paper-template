"""Tests for scripts/credentials.py: private entry, Git exclusion, and passing values on."""

from __future__ import annotations

import hashlib
import importlib.util
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parent.parent / "credentials.py"
SECRET = 'test-value "quoted" \\ back = # hash ü'  # A synthetic test value, not a real credential.
GIT = shutil.which("git")


class CredentialTests(unittest.TestCase):
    def setUp(self) -> None:
        # A workspace path with a space and a non-ASCII character, as researchers often have.
        self.root = Path(tempfile.mkdtemp(prefix="cred test ä "))
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        (self.root / "scripts").mkdir()
        shutil.copy2(SCRIPT, self.root / "scripts" / "credentials.py")
        (self.root / ".gitignore").write_text(".env\n.env.*\n!.env.example\n", encoding="utf-8")
        self.env_file = self.root / ".env.local"

    def cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(self.root / "scripts" / "credentials.py"), *args],
            capture_output=True, text=True, encoding="utf-8", timeout=60,
        )

    def start_form(self, name: str = "DEMO_TOKEN") -> tuple[subprocess.Popen, str]:
        process = subprocess.Popen(
            [sys.executable, str(self.root / "scripts" / "credentials.py"), "set", name, "--no-browser", "--timeout", "30"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8",
        )
        self.addCleanup(process.kill)
        url = process.stdout.readline().rsplit(" ", 1)[-1].strip()
        self.assertTrue(url.startswith("http://127.0.0.1:"), url)
        return process, url

    @staticmethod
    def request(url: str, value: str | None = None, headers: dict | None = None) -> int:
        data = urllib.parse.urlencode({"value": value}).encode() if value is not None else None
        try:
            with urllib.request.urlopen(urllib.request.Request(url, data=data, headers=headers or {}), timeout=10) as response:
                return response.status
        except urllib.error.HTTPError as error:
            return error.code

    def test_browser_entry_saves_value_and_never_prints_it(self) -> None:
        process, url = self.start_form()
        origin = url.rsplit("/", 1)[0]
        with urllib.request.urlopen(url, timeout=10) as response:
            self.assertIn('type="password"', response.read().decode("utf-8"))
            # Browsers send "Origin: null" under "no-referrer", which the origin check rejects.
            self.assertEqual(response.headers["Referrer-Policy"], "same-origin")
        self.assertEqual(self.request(origin + "/wrong"), 404)
        self.assertEqual(self.request(url, "x", {"Origin": "http://evil.example"}), 404)
        self.assertEqual(self.request(url, "x", {"Origin": "null"}), 404)
        self.assertEqual(self.request(url, "x", {"Host": "evil.example"}), 404)
        self.assertEqual(self.request(url, "   ", {"Origin": origin}), 400)
        # A browser submits the form with its own origin.
        self.assertEqual(self.request(url, SECRET, {"Origin": origin}), 200)
        stdout, stderr = process.communicate(timeout=30)
        self.assertEqual(process.returncode, 0, stdout + stderr)
        self.assertNotIn(SECRET, stdout + stderr)
        self.assertIn(f"Saved DEMO_TOKEN ({len(SECRET)} characters)", stdout)
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(self.env_file.stat().st_mode), 0o600)
        self.assertEqual(sorted(path.name for path in self.root.glob(".env.local.*")), [])  # no temporary file is left

        consumer = "import hashlib, os; print(hashlib.sha256(os.environ['DEMO_TOKEN'].encode()).hexdigest())"
        result = self.cli("run", "--only", "DEMO_TOKEN", "--", sys.executable, "-c", consumer)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), hashlib.sha256(SECRET.encode()).hexdigest())

        status = self.cli("status")
        self.assertIn(f"DEMO_TOKEN: set ({len(SECRET)} characters)", status.stdout)
        self.assertNotIn(SECRET, status.stdout + status.stderr)

    def save_through_form(self, name: str, value: str) -> str:
        """Save one value the way a researcher does, on the one-time page; return what the command printed."""
        process, url = self.start_form(name)
        self.assertEqual(self.request(url, value, {"Origin": url.rsplit("/", 1)[0]}), 200)
        stdout, stderr = process.communicate(timeout=30)
        self.assertEqual(process.returncode, 0, stdout + stderr)
        self.assertNotIn(value, stdout + stderr)
        return stdout

    def load_module(self):
        """The copied script as a module, to call its functions in this process."""
        spec = importlib.util.spec_from_file_location("credentials_under_test", self.root / "scripts" / "credentials.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_saving_a_second_service_keeps_the_first(self) -> None:
        self.assertIn("Saved FIRST_SERVICE_TOKEN (11 characters)", self.save_through_form("FIRST_SERVICE_TOKEN", "first-value"))
        self.assertIn("Saved SECOND_SERVICE_KEY (12 characters)", self.save_through_form("SECOND_SERVICE_KEY", "second-value"))
        lines = self.env_file.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[1:], ['FIRST_SERVICE_TOKEN="first-value"', 'SECOND_SERVICE_KEY="second-value"'])
        status = self.cli("status")
        self.assertIn("FIRST_SERVICE_TOKEN: set (11 characters)", status.stdout)
        self.assertIn("SECOND_SERVICE_KEY: set (12 characters)", status.stdout)
        consumer = "import os; print(os.environ['FIRST_SERVICE_TOKEN'], os.environ['SECOND_SERVICE_KEY'])"
        result = self.cli("run", "--", sys.executable, "-c", consumer)
        self.assertEqual(result.stdout.strip(), "first-value second-value")
        # The lock lives in the ignored .tmp folder, not beside the credentials.
        self.assertTrue((self.root / ".tmp" / "credentials.lock").is_file())
        self.assertEqual(sorted(path.name for path in self.root.glob(".env.local.*")), [])

    def test_replacing_one_value_keeps_the_other_values_and_every_other_line(self) -> None:
        self.env_file.write_text('# my note\n\nexport KEPT_EXPORT="x y"\nFIRST_SERVICE_TOKEN="old"\nSECOND_SERVICE_KEY=\'second\'\n'
                                 '   # indented FIRST_SERVICE_TOKEN="a comment"\nwords that are no setting\n', encoding="utf-8")
        self.assertIn("Replaced FIRST_SERVICE_TOKEN", self.save_through_form("FIRST_SERVICE_TOKEN", "new-value"))
        self.assertEqual(self.env_file.read_text(encoding="utf-8").splitlines(), [
            "# my note", "", 'export KEPT_EXPORT="x y"', "SECOND_SERVICE_KEY='second'", '   # indented FIRST_SERVICE_TOKEN="a comment"',
            "words that are no setting", 'FIRST_SERVICE_TOKEN="new-value"'])

    def test_windows_line_endings_and_a_byte_order_mark_do_not_cost_a_value(self) -> None:
        self.env_file.write_bytes('﻿FIRST_SERVICE_TOKEN="1"\r\n# note\r\nSECOND_SERVICE_KEY="2"\r\n'.encode("utf-8"))
        self.save_through_form("THIRD_SERVICE_KEY", "3")
        status = self.cli("status").stdout
        for name in ("FIRST_SERVICE_TOKEN", "SECOND_SERVICE_KEY", "THIRD_SERVICE_KEY"):
            self.assertIn(f"{name}: set (1 characters)", status)

    def test_overlapping_writers_do_not_lose_each_others_values(self) -> None:
        # Ten processes save ten different names at the same moment, as two services could be saved at once.
        self.env_file.write_text('# note\nEXISTING_KEY="kept"\n', encoding="utf-8")
        child = ("import importlib.util, sys\nfrom pathlib import Path\n"
                 "spec = importlib.util.spec_from_file_location('credentials', sys.argv[1])\n"
                 "module = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"
                 "while not Path(sys.argv[4]).exists():\n    pass\n"
                 "module.write_value(Path(sys.argv[2]), sys.argv[3], 'value-' + sys.argv[3])\n")
        names = [f"SERVICE_{number}_KEY" for number in range(10)]
        start = self.root / "start-now"
        children = [subprocess.Popen([sys.executable, "-c", child, str(self.root / "scripts" / "credentials.py"), str(self.root), name, str(start)],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for name in names]
        self.addCleanup(lambda: [process.kill() for process in children if process.poll() is None])
        time.sleep(0.5)
        start.write_text("go", encoding="utf-8")
        failures = []
        for process in children:
            _, stderr = process.communicate(timeout=60)
            if process.returncode != 0:
                failures.append(stderr.strip().splitlines()[-1] if stderr.strip() else "failed")
        self.assertEqual(failures, [])
        lines = self.env_file.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[:2], ["# note", 'EXISTING_KEY="kept"'])
        for name in names:
            self.assertEqual(lines.count(f'{name}="value-{name}"'), 1, name)
        self.assertEqual(len(lines), 2 + len(names))
        self.assertEqual(sorted(path.name for path in self.root.glob(".env.local.*")), [])

    def test_a_writer_waits_while_another_holds_the_file_and_gives_up_cleanly(self) -> None:
        module = self.load_module()
        self.env_file.write_text('FIRST_SERVICE_TOKEN="1"\n', encoding="utf-8")
        waiting = ("import importlib.util, sys\nfrom pathlib import Path\n"
                   "spec = importlib.util.spec_from_file_location('credentials', sys.argv[1])\n"
                   "module = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n"
                   "module.write_value(Path(sys.argv[2]), 'SECOND_SERVICE_KEY', '2')\n")
        with module.exclusive(self.root):
            writer = subprocess.Popen([sys.executable, "-c", waiting, str(self.root / "scripts" / "credentials.py"), str(self.root)],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.addCleanup(lambda: writer.poll() is None and writer.kill())
            time.sleep(1.0)
            self.assertIsNone(writer.poll(), "the second writer must wait for the lock")
            self.assertEqual(self.env_file.read_text(encoding="utf-8"), 'FIRST_SERVICE_TOKEN="1"\n')
            with mock.patch.object(module, "LOCK_WAIT", 0.3):
                with self.assertRaises(module.Busy):
                    module.write_value(self.root, "THIRD_SERVICE_KEY", "3")
        _, stderr = writer.communicate(timeout=30)
        self.assertEqual(writer.returncode, 0, stderr)
        self.assertEqual(sorted(module.load_env_local(self.root)), ["FIRST_SERVICE_TOKEN", "SECOND_SERVICE_KEY"])

    def test_a_failed_replacement_keeps_the_old_file_and_leaves_no_temporary_file(self) -> None:
        module = self.load_module()
        self.env_file.write_text('FIRST_SERVICE_TOKEN="1"\n', encoding="utf-8")
        before = self.env_file.read_bytes()
        with mock.patch.object(module.os, "replace", side_effect=OSError("disk full (simulated)")):
            with self.assertRaises(OSError):
                module.write_value(self.root, "SECOND_SERVICE_KEY", "2")
        self.assertEqual(self.env_file.read_bytes(), before)
        self.assertEqual(sorted(path.name for path in self.root.glob(".env.local.*")), [])
        self.assertFalse(module.write_value(self.root, "SECOND_SERVICE_KEY", "2"))  # the lock is free again; the name was not set before
        self.assertTrue(module.write_value(self.root, "SECOND_SERVICE_KEY", "3"))
        self.assertEqual(sorted(module.load_env_local(self.root)), ["FIRST_SERVICE_TOKEN", "SECOND_SERVICE_KEY"])

    def test_refuses_before_asking_when_gitignore_does_not_exclude_the_file(self) -> None:
        (self.root / ".gitignore").write_text("*.pyc\n", encoding="utf-8")
        result = self.cli("set", "DEMO_TOKEN", "--no-browser", "--timeout", "1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Not saved", result.stdout)
        self.assertNotIn("http://", result.stdout)
        self.assertFalse(self.env_file.exists())

    @unittest.skipUnless(GIT, "Git is not installed")
    def test_refuses_when_git_already_tracks_the_file(self) -> None:
        subprocess.run([GIT, "init", "-q", str(self.root)], check=True)
        self.env_file.write_text("# placeholder\n", encoding="utf-8")
        subprocess.run([GIT, "-C", str(self.root), "add", "-f", ".env.local"], check=True)
        result = self.cli("set", "DEMO_TOKEN", "--no-browser", "--timeout", "1")
        self.assertEqual(result.returncode, 1)
        self.assertIn("already tracks", result.stdout)

    @unittest.skipUnless(GIT, "Git is not installed")
    def test_status_reports_git_protection(self) -> None:
        subprocess.run([GIT, "init", "-q", str(self.root)], check=True)
        result = self.cli("status")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Git ignores .env.local", result.stdout)

    def test_timeout_saves_nothing(self) -> None:
        result = self.cli("set", "DEMO_TOKEN", "--no-browser", "--timeout", "2")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Nothing was saved", result.stdout)
        self.assertFalse(self.env_file.exists())

    def test_remove_keeps_other_lines(self) -> None:
        self.env_file.write_text('# kept comment\nFIRST="1"\nSECOND="2"\n', encoding="utf-8")
        result = self.cli("remove", "FIRST")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.env_file.read_text(encoding="utf-8"), '# kept comment\nSECOND="2"\n')

    def test_run_refuses_missing_names(self) -> None:
        result = self.cli("run", "--only", "MISSING", "--", sys.executable, "-c", "print('ran')")
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("ran", result.stdout)

    def test_invalid_name_is_refused(self) -> None:
        result = self.cli("set", "lower-case", "--no-browser", "--timeout", "1")
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.env_file.exists())


if __name__ == "__main__":
    unittest.main()
