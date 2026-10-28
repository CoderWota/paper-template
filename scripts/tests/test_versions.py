"""Tests for scripts/versions.py in disposable repositories.

Each test runs Git with an empty global configuration, so the maintainer's own settings (signing, hooks, default
branch) cannot change the result. A bare repository on this computer stands in for an external backup destination;
it proves the mechanics, not access to an online provider.
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
VERSIONS = SCRIPTS / "versions.py"
sys.path.insert(0, str(SCRIPTS))

import versions  # noqa: E402


class VersionsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="versions test ä "))
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)
        empty = self.base / "empty gitconfig"
        empty.write_text("", encoding="utf-8")
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=str(empty), GIT_CONFIG_NOSYSTEM="1")
        self.old_env = dict(os.environ)
        os.environ.update(GIT_CONFIG_GLOBAL=str(empty), GIT_CONFIG_NOSYSTEM="1")
        self.addCleanup(self.restore_env)
        self.root = self.base / "论文 workspace"
        self.root.mkdir()
        (self.root / ".gitignore").write_text(".env\n.env.*\n!.env.example\n.local/\n.venv/\n.tools/\n.cache/\n.tmp/\n", encoding="utf-8")
        self.write("manuscript/01-introduction.md", "# Introduction\n\nThe first draft of the introduction.\n")
        self.write("references/notes/src-a.md", "# Notes\n\nA note.\n")
        self.write("requirements/privacy.md", "# Privacy\n\nNo external copies confirmed yet.\n")

    def restore_env(self) -> None:
        os.environ.clear()
        os.environ.update(self.old_env)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run_versions(self, *args: str, root: Path | None = None) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(VERSIONS), "--root", str(root or self.root), *args], capture_output=True,
                              text=True, encoding="utf-8", env=self.env, timeout=120)

    def git(self, *args: str, cwd: Path | None = None) -> str:
        return subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@localhost", "-C", str(cwd or self.root), *args],
                              capture_output=True, text=True, encoding="utf-8", env=self.env, check=True).stdout

    def setup_history(self) -> None:
        self.assertEqual(self.run_versions("init").returncode, 0)
        self.assertEqual(self.run_versions("identity", "--name", "Researcher", "--email", "researcher@localhost").returncode, 0)
        saved = self.run_versions("save", "--message", "First version", "--all")
        self.assertEqual(saved.returncode, 0, saved.stdout)


class SetupAndSaveTests(VersionsTestCase):
    def test_inspect_changes_nothing_and_init_creates_a_protected_history(self) -> None:
        before = self.run_versions("inspect")
        self.assertIn("no version history of its own yet", before.stdout)
        self.assertFalse((self.root / ".git").exists())
        self.assertEqual(self.run_versions("init").returncode, 0)
        self.assertEqual(self.git("branch", "--show-current").strip(), "main")
        self.assertIn("already has a version history", self.run_versions("init").stdout)
        facts = json.loads(self.run_versions("inspect", "--json").stdout)
        self.assertTrue(facts["env_local_ignored"])
        self.assertFalse(facts["has_versions"])
        self.assertFalse(facts["identity_set"])

    def test_save_needs_an_identity_and_saves_only_the_requested_scope(self) -> None:
        self.run_versions("init")
        refused = self.run_versions("save", "--message", "x", "--all")
        self.assertEqual(refused.returncode, 3)
        self.assertIn("no author name and e-mail", refused.stdout)
        self.run_versions("identity", "--name", "Researcher", "--email", "researcher@localhost")
        saved = self.run_versions("save", "--message", "Save the introduction", "--path", "manuscript")
        self.assertEqual(saved.returncode, 0, saved.stdout)
        self.assertIn("manuscript: manuscript/01-introduction.md (new)", saved.stdout)
        self.assertIn("nothing was sent anywhere", saved.stdout)
        self.assertEqual(self.git("ls-files").split(), ["manuscript/01-introduction.md"])
        self.assertIn("other changed file(s) were not part of this version", saved.stdout)
        (self.root / "manuscript" / "01-introduction.md").unlink()
        self.write("manuscript/02-methods.md", "# Methods\n")
        removed = self.run_versions("save", "--message", "Replace the introduction", "--path", "manuscript")
        self.assertEqual(removed.returncode, 0, removed.stdout)
        self.assertIn("(deleted)", removed.stdout)
        self.assertEqual(self.git("ls-files", "manuscript").split(), ["manuscript/02-methods.md"])
        self.assertIn("Nothing to save", self.run_versions("save", "--message", "again", "--path", "manuscript").stdout)

    def test_secrets_and_oversized_files_are_refused(self) -> None:
        self.setup_history()
        self.write("notes/keys.txt", "SCIVERSE_API_KEY=abcdefghijklmnop1234\n")
        refused = self.run_versions("save", "--message", "x", "--path", "notes")
        self.assertEqual(refused.returncode, 3)
        self.assertIn("look like secrets", refused.stdout)
        (self.root / "notes" / "keys.txt").unlink()
        self.write("ssh/id_rsa", "anything")
        self.assertIn("ssh/id_rsa", self.run_versions("save", "--message", "x", "--path", "ssh").stdout)
        shutil.rmtree(self.root / "ssh")
        self.write(".env.example", "MINERU_API_TOKEN=\n")
        self.write(".env.local", "MINERU_API_TOKEN=abcdefghijklmnop1234\n")
        allowed = self.run_versions("save", "--message", "Example settings", "--all")
        self.assertEqual(allowed.returncode, 0, allowed.stdout)
        self.assertNotIn(".env.local", self.git("ls-files"))
        big = self.root / "references" / "originals" / "huge.pdf"
        big.parent.mkdir(parents=True, exist_ok=True)
        with open(big, "wb") as stream:
            stream.truncate(101 * 1024 * 1024)
        too_large = self.run_versions("save", "--message", "x", "--path", "references")
        self.assertEqual(too_large.returncode, 3)
        self.assertIn("larger than 100 MB", too_large.stdout)

    def test_a_scoped_save_never_takes_other_prepared_changes_along(self) -> None:
        self.setup_history()
        self.write("references/notes/src-a.md", "# Notes\n\nChanged and prepared elsewhere.\n")
        self.git("add", "references/notes/src-a.md")
        self.write("manuscript/01-introduction.md", "# Introduction\n\nA new draft.\n")
        refused = self.run_versions("save", "--message", "Only the manuscript", "--path", "manuscript")
        self.assertEqual(refused.returncode, 3)
        self.assertIn("references/notes/src-a.md", refused.stdout)
        self.assertEqual(self.git("rev-list", "--count", "HEAD").strip(), "1")

    def test_an_unfinished_merge_blocks_saving(self) -> None:
        self.setup_history()
        merge_head = self.root / ".git" / "MERGE_HEAD"
        merge_head.write_text(self.git("rev-parse", "HEAD"), encoding="utf-8")
        self.write("manuscript/01-introduction.md", "changed\n")
        refused = self.run_versions("save", "--message", "x", "--all")
        self.assertEqual(refused.returncode, 3)
        self.assertIn("a merge is unfinished", refused.stdout)

    def test_scope_reports_tracked_files_that_ignore_rules_cannot_remove_and_untrack_keeps_them(self) -> None:
        self.setup_history()
        self.write("outputs/preview/draft.docx", "preview")
        self.git("add", "-f", "outputs/preview/draft.docx")
        self.git("commit", "-q", "-m", "Track a preview by mistake")
        with open(self.root / ".gitignore", "a", encoding="utf-8") as stream:
            stream.write("outputs/preview/*\n")
        scope = self.run_versions("scope")
        self.assertEqual(scope.returncode, 1)
        self.assertIn("ignore rules cannot remove them): outputs/preview/draft.docx", scope.stdout)
        untracked = self.run_versions("untrack", "--path", "outputs/preview/draft.docx")
        self.assertEqual(untracked.returncode, 0, untracked.stdout)
        self.assertTrue((self.root / "outputs/preview/draft.docx").is_file())
        self.run_versions("save", "--message", "Stop tracking the preview", "--all")
        self.assertNotIn("outputs/preview/draft.docx", self.git("ls-files"))


class CompareAndRecoveryTests(VersionsTestCase):
    def test_compare_summarizes_by_area_with_renames_new_files_and_words(self) -> None:
        self.setup_history()
        self.write("manuscript/01-introduction.md", "# Introduction\n\nThe second draft of the introduction.\n")
        self.git("mv", "references/notes/src-a.md", "references/notes/src-b.md")
        self.write("ideas/新想法.md", "# 想法\n")
        result = self.run_versions("compare")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("manuscript/01-introduction.md (changed, +1 −1 lines)", result.stdout)
        self.assertIn("references/notes/src-b.md (renamed from references/notes/src-a.md", result.stdout)
        self.assertIn("ideas/新想法.md (new, never saved)", result.stdout)
        words = self.run_versions("compare", "--words", "--path", "manuscript/01-introduction.md")
        self.assertIn("[-first-]{+second+}", words.stdout)

    def test_history_retrieve_and_restore_keep_current_work_recoverable(self) -> None:
        self.setup_history()
        first = self.git("rev-parse", "--short", "HEAD").strip()
        self.write("manuscript/01-introduction.md", "# Introduction\n\nThe second draft.\n")
        self.run_versions("save", "--message", "Second draft", "--path", "manuscript")
        self.write("manuscript/01-introduction.md", "# Introduction\n\nUnsaved third draft.\n")
        history = self.run_versions("history", "--path", "manuscript/01-introduction.md")
        self.assertIn("Second draft", history.stdout)
        self.assertIn("First version", history.stdout)
        retrieved = self.run_versions("retrieve", "--rev", first, "--path", "manuscript/01-introduction.md")
        self.assertEqual(retrieved.returncode, 0, retrieved.stdout)
        copy = self.root / ".tmp" / "recovered" / first / "manuscript" / "01-introduction.md"
        self.assertIn("first draft", copy.read_text(encoding="utf-8"))
        self.assertIn("Unsaved third draft", (self.root / "manuscript/01-introduction.md").read_text(encoding="utf-8"))
        self.write("manuscript/99-extra.md", "extra\n")
        restored = self.run_versions("restore", "--rev", first, "--path", "manuscript")
        self.assertEqual(restored.returncode, 0, restored.stdout)
        self.assertIn("first draft", (self.root / "manuscript/01-introduction.md").read_text(encoding="utf-8"))
        backups = list((self.root / ".tmp" / "recovered").glob("before-restore-*/manuscript/01-introduction.md"))
        self.assertEqual(len(backups), 1)
        self.assertIn("Unsaved third draft", backups[0].read_text(encoding="utf-8"))
        self.assertIn("manuscript/99-extra.md", restored.stdout)
        self.assertTrue((self.root / "manuscript/99-extra.md").is_file())
        self.assertIn("Refused", self.run_versions("retrieve", "--rev", "nosuchversion", "--path", "manuscript").stdout)

    def test_practice_copy_is_separate_and_resettable(self) -> None:
        self.setup_history()
        before = self.git("rev-list", "--count", "HEAD").strip()
        made = self.run_versions("practice")
        self.assertEqual(made.returncode, 0, made.stdout)
        practice = self.root / ".tmp" / "git-practice"
        self.assertEqual(self.git("rev-list", "--count", "HEAD", cwd=practice).strip(), "3")
        self.assertEqual(self.git("rev-list", "--count", "HEAD").strip(), before)
        (practice / "practice-note.md").write_text("# Practice note\n\nMy own edit.\n", encoding="utf-8")
        practiced = self.run_versions("save", "--message", "My practice edit", "--all", root=practice)
        self.assertEqual(practiced.returncode, 0, practiced.stdout)
        self.assertIn("first paragraph", self.run_versions("compare", "--from", "HEAD~1", "--to", "HEAD", "--words", root=practice).stdout)
        self.assertEqual(self.git("rev-list", "--count", "HEAD").strip(), before)
        self.assertEqual(self.run_versions("practice", "--reset").returncode, 0)
        shutil.rmtree(practice)
        practice.mkdir(parents=True)
        (practice / "mine.txt").write_text("not a practice copy", encoding="utf-8")
        self.assertEqual(self.run_versions("practice", "--reset").returncode, 3)
        self.assertTrue((practice / "mine.txt").is_file())


class InheritedHistoryAndBackupTests(VersionsTestCase):
    def test_inherited_template_history_and_research_versions_are_recognized(self) -> None:
        template = self.base / "template"
        template.mkdir()
        self.git("init", "-q", "-b", "main", cwd=template)
        (template / "README.md").write_text("# Template\n", encoding="utf-8")
        (template / "manuscript").mkdir()
        (template / "manuscript" / "README.md").write_text("# Manuscript folder\n", encoding="utf-8")
        self.git("add", "-A", cwd=template)
        self.git("commit", "-q", "-m", "Template scaffold", cwd=template)
        root_commit = self.git("rev-parse", "HEAD", cwd=template).strip()
        copy = self.base / "copied paper"
        subprocess.run(["git", "clone", "-q", str(template), str(copy)], env=self.env, check=True)
        versions.TEMPLATE_ROOT_COMMIT = root_commit
        facts = versions.inspect_facts(copy)
        self.assertTrue(facts["template_history"])
        self.assertEqual(facts["research_versions"], 0)
        self.assertEqual([r["name"] for r in facts["remotes"]], ["origin"])
        self.assertEqual(facts["remotes"][0]["research_versions_seen_there"], 0)
        (copy / "manuscript" / "01-introduction.md").write_text("# Introduction\n", encoding="utf-8")
        self.git("add", "-A", cwd=copy)
        self.git("commit", "-q", "-m", "Draft the introduction", cwd=copy)
        facts = versions.inspect_facts(copy)
        self.assertEqual(facts["research_versions"], 1)
        self.assertEqual(facts["first_research_version"]["message"], "Draft the introduction")

    def test_backup_needs_a_confirmed_destination_and_is_checked_after_the_push(self) -> None:
        self.setup_history()
        destination = self.base / "backup destination.git"
        subprocess.run(["git", "init", "-q", "--bare", str(destination)], env=self.env, check=True)
        self.git("remote", "add", "backup", str(destination))
        refused = self.run_versions("backup", "--remote", "backup")
        self.assertEqual(refused.returncode, 3)
        self.assertIn("is not named as a confirmed destination", refused.stdout)
        self.assertEqual(subprocess.run(["git", "-C", str(destination), "rev-parse", "--verify", "--quiet", "main"],
                                        capture_output=True, env=self.env).returncode, 1)
        self.write("requirements/privacy.md", f"# Privacy\n\n- External copy: {destination}; confirmed 2026-10-28; “备份到这个文件夹”\n")
        self.run_versions("save", "--message", "Confirm the backup destination", "--all")
        listing = self.run_versions("remotes")
        self.assertIn("confirmed in requirements/privacy.md", listing.stdout)
        backed_up = self.run_versions("backup", "--remote", "backup")
        self.assertEqual(backed_up.returncode, 0, backed_up.stdout)
        self.assertIn("checked that the copy holds version", backed_up.stdout)
        self.assertEqual(self.git("rev-parse", "main", cwd=destination).strip(), self.git("rev-parse", "HEAD").strip())
        restored = self.base / "restored from backup"
        subprocess.run(["git", "clone", "-q", "-b", "main", str(destination), str(restored)], env=self.env, check=True)
        self.assertEqual((restored / "manuscript" / "01-introduction.md").read_text(encoding="utf-8"),
                         (self.root / "manuscript" / "01-introduction.md").read_text(encoding="utf-8"))

    def test_an_unreachable_destination_is_reported_as_not_backed_up(self) -> None:
        self.setup_history()
        missing = self.base / "no such drive" / "paper.git"
        self.git("remote", "add", "backup", str(missing))
        self.write("requirements/privacy.md", f"# Privacy\n\n- External copy: {missing}\n")
        failed = self.run_versions("backup", "--remote", "backup")
        self.assertEqual(failed.returncode, 1)
        self.assertIn("The backup failed; nothing is confirmed as copied", failed.stdout)

    def test_backup_refuses_history_with_secret_files(self) -> None:
        self.setup_history()
        destination = self.base / "backup.git"
        subprocess.run(["git", "init", "-q", "--bare", str(destination)], env=self.env, check=True)
        self.git("remote", "add", "backup", str(destination))
        self.write("requirements/privacy.md", f"# Privacy\n\n- External copy: {destination}\n")
        self.write("old/.env.production", "TOKEN=abcdefghijklmnopqrstuv\n")
        self.git("add", "-f", "-A")
        self.git("commit", "-q", "-m", "A version with a secret file")
        refused = self.run_versions("backup", "--remote", "backup")
        self.assertEqual(refused.returncode, 3)
        self.assertIn("old/.env.production", refused.stdout)
        facts = json.loads(self.run_versions("inspect", "--json").stdout)
        self.assertIn("old/.env.production", facts["secrets_tracked"])


if __name__ == "__main__":
    unittest.main()
