"""Tests for scripts/credentials.py: private entry, Git exclusion, and passing values on."""

from __future__ import annotations

import hashlib
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

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
        self.assertFalse((self.root / ".env.local.tmp").exists())

        consumer = "import hashlib, os; print(hashlib.sha256(os.environ['DEMO_TOKEN'].encode()).hexdigest())"
        result = self.cli("run", "--only", "DEMO_TOKEN", "--", sys.executable, "-c", consumer)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(result.stdout.strip(), hashlib.sha256(SECRET.encode()).hexdigest())

        status = self.cli("status")
        self.assertIn(f"DEMO_TOKEN: set ({len(SECRET)} characters)", status.stdout)
        self.assertNotIn(SECRET, status.stdout + status.stderr)

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
