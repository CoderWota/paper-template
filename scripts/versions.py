#!/usr/bin/env python3
"""Version history for the workspace, operated by the agent: inspect, set up, save, compare, retrieve, restore,
practice, and back up with Git, with checks that protect the researcher's work and secrets.

Nothing here leaves this computer except `backup`, which pushes only to a destination that
requirements/privacy.md names, never with force, and then checks that the remote holds the saved version.

Usage:
  python scripts/versions.py inspect [--json]
  python scripts/versions.py scope
  python scripts/versions.py init
  python scripts/versions.py identity --name NAME --email EMAIL
  python scripts/versions.py save --message TEXT (--path PATH ... | --all) [--allow-large]
  python scripts/versions.py history [--path PATH] [--limit N]
  python scripts/versions.py compare [--from REV] [--to REV] [--path PATH ...] [--words]
  python scripts/versions.py retrieve --rev REV --path PATH [--to FOLDER]
  python scripts/versions.py restore --rev REV --path PATH
  python scripts/versions.py untrack --path PATH
  python scripts/versions.py practice [--reset]
  python scripts/versions.py remotes
  python scripts/versions.py detach-template [--apply]
  python scripts/versions.py backup --remote NAME [--branch BRANCH]
All commands take --root WORKSPACE (default: the parent of the scripts folder).
Exit status: 0 done; 1 a check failed or a backup could not be verified; 3 refused. Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT_COMMIT = "4c89942ae14b3e2cfa42ba2a6bc19b8bf2978a1a"
TEMPLATE_REPOSITORY = ("github.com", "coderwota", "paper-template")
WARN_BYTES, LIMIT_BYTES = 50 * 1024 * 1024, 100 * 1024 * 1024
SECRET_NAME = re.compile(r"(^|/)(\.env(\.(?!example$)[^/]+)?|[^/]+\.(pem|p12|pfx)|id_(rsa|ed25519|ecdsa)[^/]*)$", re.I)
SECRET_LINE = re.compile(r"^\s*(export\s+)?[A-Z][A-Z0-9_]*(TOKEN|KEY|SECRET|PASSWORD)[A-Z0-9_]*\s*=\s*['\"]?[^\s'\"#]{12,}"
                         r"|-----BEGIN [A-Z ]*PRIVATE KEY-----", re.M)
# This exact source declaration contains the public environment-variable name, not its value.
PUBLIC_ENV_DECLARATION = re.compile(r'^\s*API_KEY_NAME\s*=\s*["\']SCIVERSE_API_KEY["\']\s*$', re.M)
AREAS = (
    ("manuscript/", "manuscript"), ("references/originals/", "reference originals"), ("references/", "references"),
    ("requirements/", "requirements"), ("research/", "research records"), ("ideas/", "ideas"), ("reviews/", "reviews"),
    ("revisions/", "revisions"), ("outputs/releases/", "releases"), ("outputs/", "outputs"), ("code/", "research code"),
    ("inbox/", "inbox"), ("state/", "project state"),
)
FRAMEWORK = (".agents/", ".claude/", "scripts/", "docs/", "AGENTS.md", "CLAUDE.md", "README.md", "CONTEXT.md", ".gitignore",
             ".gitattributes", ".env.example")
# Paths that only a research project creates: the template itself ships none of them.
RESEARCH_CONTENT = re.compile(
    r"^(manuscript/(?!README\.md$|outline\.md$|manifest\.yaml$|assets/README\.md$).+"
    r"|references/(originals|extracted)/src-.+|references/notes/(?!README\.md$).+"
    r"|research/(decisions|results)/(?!README\.md$|index\.md$).+|research/feedback/[^/]+/.+|research/(plan|impact)\.md"
    r"|ideas/(?!README\.md$|index\.md$).+|reviews/[^/]+/.+|revisions/[^/]+/.+|outputs/releases/[^/]+/.+|code/.+)$")
IN_PROGRESS = {"MERGE_HEAD": "a merge", "rebase-merge": "a rebase", "rebase-apply": "a rebase or patch",
               "CHERRY_PICK_HEAD": "a cherry-pick", "REVERT_HEAD": "a revert", "BISECT_LOG": "a bisection"}


class Refused(Exception):
    pass


def git(root: Path, *args: str, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    if not shutil.which("git"):
        raise Refused("Git is not installed on this computer. Install it with the researcher's consent (environment-management).")
    completed = subprocess.run(["git", "-c", "core.quotepath=false", "-C", str(root), *args], capture_output=True, text=text,
                               encoding="utf-8" if text else None, errors="replace" if text else None)
    if check and completed.returncode != 0:
        raise Refused(f"git {args[0]} failed: {redact((completed.stderr or '').strip())[-400:]}")
    return completed


def redact(text: str) -> str:
    return re.sub(r"(https?://)[^/@\s]+@", r"\1[redacted]@", text)


def area_of(path: str) -> str:
    for prefix, name in AREAS:
        if path.startswith(prefix):
            return name
    if path.startswith(FRAMEWORK) or path in FRAMEWORK:
        return "workspace framework"
    return "other"


def is_repository(root: Path) -> bool:
    if not shutil.which("git"):
        return False
    completed = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    return completed.returncode == 0 and Path(completed.stdout.strip()).resolve() == root.resolve()


def require_repository(root: Path) -> None:
    if not is_repository(root):
        raise Refused("this workspace has no version history yet; set it up first (versions.py init, through git-setup)")


def in_progress(root: Path) -> list:
    found = []
    for name, words in IN_PROGRESS.items():
        path = Path(git(root, "rev-parse", "--git-path", name).stdout.strip())
        if (path if path.is_absolute() else root / path).exists() and words not in found:
            found.append(words)
    return found


def has_commits(root: Path) -> bool:
    return git(root, "rev-parse", "--verify", "--quiet", "HEAD", check=False).returncode == 0


def status_entries(root: Path, paths: list | None = None) -> list:
    """(code, path) for every changed, new, or deleted file, untracked files included, ignored files excluded."""
    output = git(root, "status", "--porcelain=v1", "-z", "--untracked-files=all", "--", *(paths or [])).stdout
    entries, parts, index = [], output.split("\0"), 0
    while index < len(parts):
        item = parts[index]
        index += 1
        if len(item) < 4:
            continue
        code, path = item[:2], item[3:]
        if code[0] in "RC":
            index += 1  # the original name of a rename follows
        entries.append((code, path))
    return entries


def describe_code(code: str) -> str:
    if code == "??":
        return "new"
    if "D" in code:
        return "deleted"
    if "R" in code:
        return "renamed"
    if "A" in code:
        return "added"
    return "changed"


def risks(root: Path, paths: list) -> tuple:
    """(secrets, too large, large) among files that would be saved."""
    secrets, too_large, large = [], [], []
    for path in paths:
        file = root / path
        if not file.is_file():
            continue
        size = file.stat().st_size
        if SECRET_NAME.search(path):
            secrets.append(path)
        elif size <= 2 * 1024 * 1024:
            try:
                content = file.read_text(encoding="utf-8", errors="ignore")
                if path == "scripts/literature/search.py":
                    content = PUBLIC_ENV_DECLARATION.sub("", content)
                if SECRET_LINE.search(content):
                    secrets.append(path)
            except OSError:
                pass
        if size > LIMIT_BYTES:
            too_large.append(f"{path} ({size // (1024 * 1024)} MB)")
        elif size > WARN_BYTES:
            large.append(f"{path} ({size // (1024 * 1024)} MB)")
    return secrets, too_large, large


def research_commits(root: Path, ref: str = "HEAD") -> list:
    """Commits reachable from ref that changed research content, newest first: (hash, date, subject)."""
    if git(root, "rev-parse", "--verify", "--quiet", ref, check=False).returncode != 0:
        return []
    output = git(root, "log", ref, "--format=%x00%H%x09%ad%x09%s", "--date=short", "--name-only").stdout
    found = []
    for block in output.split("\0")[1:]:
        header, _, names = block.partition("\n")
        commit, date, subject = (header.split("\t") + ["", ""])[:3]
        if any(RESEARCH_CONTENT.match(name.strip()) for name in names.splitlines() if name.strip()):
            found.append((commit, date, subject))
    return found


def remote_heads(root: Path, name: str) -> list:
    output = git(root, "for-each-ref", "--format=%(refname)", f"refs/remotes/{name}/").stdout
    return [ref for ref in output.split() if not ref.endswith("/HEAD")]


# Commands

def inspect_facts(root: Path) -> dict:
    facts: dict = {"git": None, "repository": False}
    if not shutil.which("git"):
        return facts
    facts["git"] = git(root, "--version").stdout.strip()
    if not is_repository(root):
        facts["inside_other_repository"] = git(root, "rev-parse", "--is-inside-work-tree", check=False).returncode == 0
        return facts
    facts["repository"] = True
    facts["branch"] = git(root, "branch", "--show-current").stdout.strip() or None
    facts["has_versions"] = has_commits(root)
    if facts["has_versions"]:
        facts["versions"] = int(git(root, "rev-list", "--count", "HEAD").stdout.strip())
        last = git(root, "log", "-1", "--format=%h%x09%ad%x09%s", "--date=short").stdout.strip().split("\t")
        facts["last_version"] = {"id": last[0], "date": last[1], "message": last[2] if len(last) > 2 else ""}
        facts["template_history"] = git(root, "merge-base", "--is-ancestor", TEMPLATE_ROOT_COMMIT, "HEAD", check=False).returncode == 0
        commits = research_commits(root)
        facts["research_versions"] = len(commits)
        if commits:
            facts["first_research_version"] = {"id": commits[-1][0][:7], "date": commits[-1][1], "message": commits[-1][2]}
    identity = {key: git(root, "config", f"user.{key}", check=False).stdout.strip() for key in ("name", "email")}
    facts["identity_set"] = bool(identity["name"] and identity["email"])
    entries = status_entries(root)
    by_area: dict = {}
    for code, path in entries:
        by_area.setdefault(area_of(path), {}).setdefault(describe_code(code), 0)
        by_area[area_of(path)][describe_code(code)] += 1
    facts["unsaved"] = {"files": len(entries), "by_area": by_area}
    facts["in_progress"] = in_progress(root)
    remotes = []
    for name in git(root, "remote").stdout.split():
        url = redact(git(root, "remote", "get-url", name, check=False).stdout.strip())
        heads = remote_heads(root, name)
        held = sum(len(research_commits(root, ref)) for ref in heads)
        remotes.append({"name": name, "url": url, "known_branches": [ref.split("/", 3)[-1] for ref in heads],
                        "research_versions_seen_there": held})
    facts["remotes"] = remotes
    tracked_ignored = git(root, "ls-files", "-ci", "--exclude-standard").stdout.split()
    facts["tracked_but_ignored"] = tracked_ignored
    facts["secrets_tracked"] = [p for p in git(root, "ls-files").stdout.splitlines() if SECRET_NAME.search(p)]
    facts["env_local_ignored"] = git(root, "check-ignore", "-q", ".env.local", check=False).returncode == 0
    return facts


def command_inspect(args, root: Path) -> int:
    facts = inspect_facts(root)
    if args.json:
        print(json.dumps(facts, indent=2, ensure_ascii=False))
        return 0
    if not facts["git"]:
        print("Git is not installed on this computer, so there is no version history. Nothing was changed.")
        return 0
    if not facts["repository"]:
        inside = " This folder sits inside another Git repository." if facts.get("inside_other_repository") else ""
        print(f"{facts['git']}. This workspace has no version history of its own yet.{inside} Nothing was changed.")
        return 0
    lines = [f"{facts['git']}. Branch: {facts['branch'] or 'none (a detached version is checked out)'}."]
    if facts["has_versions"]:
        last = facts["last_version"]
        lines.append(f"Saved versions: {facts['versions']}; the last one is {last['id']} of {last['date']}: {last['message']}")
        if facts["template_history"]:
            lines.append("The history includes the template's own development history.")
        if facts["research_versions"]:
            first = facts["first_research_version"]
            lines.append(f"{facts['research_versions']} version(s) contain research material; the first is {first['id']} of {first['date']}: {first['message']}")
        else:
            lines.append("No saved version contains research material yet.")
    else:
        lines.append("The repository has no saved version yet.")
    unsaved = facts["unsaved"]
    if unsaved["files"]:
        parts = [f"{area} ({', '.join(f'{n} {kind}' for kind, n in kinds.items())})" for area, kinds in sorted(unsaved["by_area"].items())]
        lines.append(f"Not yet saved: {unsaved['files']} file(s): " + "; ".join(parts) + ".")
    else:
        lines.append("Everything is saved.")
    for remote in facts["remotes"]:
        lines.append(f"External copy '{remote['name']}': {remote['url']}; research versions seen there in the last fetch: "
                     f"{remote['research_versions_seen_there']} (not contacted now).")
    if not facts["remotes"]:
        lines.append("No external copy is configured: all versions exist only on this computer.")
    if facts["in_progress"]:
        lines.append("An unfinished operation is in progress: " + ", ".join(facts["in_progress"]) + ".")
    if not facts["identity_set"]:
        lines.append("No author name and e-mail are set for saving versions.")
    if facts["secrets_tracked"]:
        lines.append("Warning: files that look like secrets are in the history: " + ", ".join(facts["secrets_tracked"]))
    if not facts["env_local_ignored"]:
        lines.append("Warning: .env.local is not excluded from version history.")
    print("\n".join(lines))
    return 0


def command_scope(args, root: Path) -> int:
    require_repository(root)
    tracked = git(root, "ls-files").stdout.splitlines()
    untracked = [path for code, path in status_entries(root) if code == "??"]
    ignored = git(root, "ls-files", "--others", "-i", "--exclude-standard", "--directory").stdout.splitlines()
    summary: dict = {}
    for name, paths in (("tracked", tracked), ("new, not yet saved", untracked), ("excluded by ignore rules", ignored)):
        for path in paths:
            summary.setdefault(area_of(path), {}).setdefault(name, 0)
            summary[area_of(path)][name] += 1
    for area in sorted(summary):
        print(f"{area}: " + ", ".join(f"{count} {name}" for name, count in summary[area].items()))
    tracked_ignored = git(root, "ls-files", "-ci", "--exclude-standard").stdout.splitlines()
    if tracked_ignored:
        print("Already tracked although the ignore rules exclude them (ignore rules cannot remove them): " + ", ".join(tracked_ignored))
    secrets, too_large, large = risks(root, tracked + untracked)
    for label, items in (("Look like secrets", secrets), ("Larger than 100 MB", too_large), ("Larger than 50 MB", large)):
        if items:
            print(f"{label}: " + ", ".join(items))
    return 1 if secrets or too_large or tracked_ignored else 0


def command_init(args, root: Path) -> int:
    if is_repository(root):
        raise Refused("this workspace already has a version history; inspect it instead of creating a new one")
    if git(root, "rev-parse", "--is-inside-work-tree", check=False).returncode == 0:
        raise Refused("this folder is inside another Git repository; ask the researcher before creating a nested history")
    gitignore = root / ".gitignore"
    added = []
    text = gitignore.read_text(encoding="utf-8") if gitignore.is_file() else ""
    for rule in (".env", ".env.*", "!.env.example", ".local/", ".venv/", ".tools/", ".cache/", ".tmp/"):
        if rule not in text.split("\n"):
            added.append(rule)
    if added:
        gitignore.write_text(text.rstrip("\n") + ("\n" if text else "") + "\n# Added by versions.py init: secrets and local files\n" + "\n".join(added) + "\n", encoding="utf-8")
    completed = git(root, "init", "-b", "main", check=False)
    if completed.returncode != 0:
        git(root, "init")
        git(root, "symbolic-ref", "HEAD", "refs/heads/main")
    print("Created an empty version history on branch main. Nothing is saved yet." +
          (f" Added ignore rules: {', '.join(added)}." if added else " The ignore rules already exclude secrets and local files."))
    return 0


def command_identity(args, root: Path) -> int:
    require_repository(root)
    git(root, "config", "--local", "user.name", args.name)
    git(root, "config", "--local", "user.email", args.email)
    print("Set the author name and e-mail for versions saved in this workspace only.")
    return 0


def command_save(args, root: Path) -> int:
    require_repository(root)
    if bool(args.path) == bool(args.all):
        raise Refused("name what to save with --path (one or more files or folders), or --all for every change")
    busy = in_progress(root)
    if busy:
        raise Refused(f"{', '.join(busy)} is unfinished; resolve it before saving a version")
    if not all(git(root, "config", f"user.{key}", check=False).stdout.strip() for key in ("name", "email")):
        raise Refused("no author name and e-mail are set; ask the researcher which to use, then run versions.py identity")
    scope = [] if args.all else args.path
    for value in scope:
        if not (root / value).exists() and not git(root, "ls-files", "--", value).stdout.strip():
            raise Refused(f"{value} does not exist and has no saved version")
    entries = status_entries(root, scope)
    if not entries:
        print("Nothing to save: the requested files have no unsaved changes.")
        return 0
    secrets, too_large, large = risks(root, [path for code, path in entries if "D" not in code])
    if secrets:
        raise Refused("these files look like secrets and were not saved: " + ", ".join(secrets) +
                      ". Keep credentials in .env.local, which is excluded from version history.")
    if too_large and not args.allow_large:
        raise Refused("these files are larger than 100 MB, which online hosts such as GitHub reject: " + ", ".join(too_large) +
                      ". Ask the researcher whether to keep them out of version history.")
    if scope:
        staged = [p for p in git(root, "diff", "--cached", "--name-only", "-z").stdout.split("\0") if p]
        elsewhere = [p for p in staged if not any(p == s.rstrip("/") or p.startswith(s.rstrip("/") + "/") for s in scope)]
        if elsewhere:
            raise Refused("other changes are already prepared for saving: " + ", ".join(elsewhere[:10]) +
                          "; include them in this version or save them separately first")
    # Stage exactly the files listed by status; a change that is already staged (such as an untracked file) stays as it is.
    pending = [path for code, path in entries if code == "??" or code[1] != " "]
    for start in range(0, len(pending), 200):
        git(root, "add", "-A", "--", *pending[start:start + 200])
    git(root, "commit", "-q", "-m", args.message)
    commit = git(root, "log", "-1", "--format=%h").stdout.strip()
    by_area: dict = {}
    for code, path in entries:
        by_area.setdefault(area_of(path), []).append(f"{path} ({describe_code(code)})")
    print(f"Saved version {commit}: {args.message}")
    for area, items in sorted(by_area.items()):
        print(f"  {area}: " + ", ".join(items[:12]) + (f", and {len(items) - 12} more" if len(items) > 12 else ""))
    if large:
        print("Note: large files saved: " + ", ".join(large))
    left = len(status_entries(root))
    print("Everything is saved." if not left else f"{left} other changed file(s) were not part of this version.")
    print("The version exists only on this computer; nothing was sent anywhere.")
    return 0


def command_history(args, root: Path) -> int:
    require_repository(root)
    if not has_commits(root):
        print("No saved versions yet.")
        return 0
    output = git(root, "log", f"-{args.limit}", "--format=%h%x09%ad%x09%s", "--date=short", "--", *([args.path] if args.path else [])).stdout
    print(output.strip() or "No saved version changed that path.")
    return 0


def command_compare(args, root: Path) -> int:
    require_repository(root)
    if not has_commits(root):
        raise Refused("there is no saved version to compare with yet")
    ends = [args.from_rev] + ([args.to_rev] if args.to_rev else [])
    for rev in ends:
        if git(root, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}", check=False).returncode != 0:
            raise Refused(f"there is no saved version called {rev}")
    paths = args.path or []
    if args.words:
        output = git(root, "diff", "--word-diff=plain", "-M", *ends, "--", *paths).stdout
        print(output.strip() or "No differences.")
        return 0
    counts, tokens = {}, git(root, "diff", "-z", "-M", "--numstat", *ends, "--", *paths).stdout.split("\0")
    index = 0
    while index < len(tokens) - 1:
        added, removed, path = (tokens[index].split("\t", 2) + ["", ""])[:3]
        if path == "":  # a rename: the old and the new name follow
            path, index = tokens[index + 2], index + 3
        else:
            index += 1
        counts[path] = (added, removed)
    by_area: dict = {}
    tokens, index = git(root, "diff", "-z", "-M", "--name-status", *ends, "--", *paths).stdout.split("\0"), 0
    while index < len(tokens) - 1:
        code = tokens[index]
        old = tokens[index + 1] if code[:1] in "RC" else None
        path = tokens[index + 2] if old else tokens[index + 1]
        index += 3 if old else 2
        kind = {"A": "added", "D": "deleted", "M": "changed", "R": "renamed", "C": "copied", "T": "changed"}.get(code[:1], code)
        added, removed = counts.get(path, ("?", "?"))
        detail = "binary file" if added == "-" else f"+{added} −{removed} lines"
        moved = f" from {old}" if old else ""
        by_area.setdefault(area_of(path), []).append(f"{path} ({kind}{moved}, {detail})")
    if not args.to_rev:
        for code, path in status_entries(root, paths):
            if code == "??":
                by_area.setdefault(area_of(path), []).append(f"{path} (new, never saved)")
    label = f"{args.from_rev} → {args.to_rev or 'current files'}"
    if not by_area:
        print(f"No differences ({label}).")
        return 0
    print(f"Differences ({label}):")
    for area, items in sorted(by_area.items()):
        print(f"  {area}:")
        for item in items:
            print(f"    {item}")
    return 0


def files_at(root: Path, rev: str, path: str) -> list:
    if git(root, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}", check=False).returncode != 0:
        raise Refused(f"there is no saved version called {rev}")
    files = git(root, "ls-tree", "-r", "--name-only", rev, "--", path).stdout.splitlines()
    if not files:
        raise Refused(f"{path} does not exist in version {rev}")
    return files


def write_blob(root: Path, rev: str, name: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(git(root, "show", f"{rev}:{name}", text=False).stdout)


def short(root: Path, rev: str) -> str:
    return git(root, "rev-parse", "--short", rev).stdout.strip()


def command_retrieve(args, root: Path) -> int:
    require_repository(root)
    files = files_at(root, args.rev, args.path)
    folder = (root / args.to) if args.to else root / ".tmp" / "recovered" / short(root, args.rev)
    written = []
    for name in files:
        target = folder / name
        if target.exists():
            target = target.with_name(f"{target.stem} (retrieved {datetime.now():%Y%m%d-%H%M%S}){target.suffix}")
        write_blob(root, args.rev, name, target)
        written.append(target)
    print(f"Retrieved {len(written)} file(s) from version {short(root, args.rev)} without changing the current files:")
    for target in written:
        try:
            print(f"  {target.resolve().relative_to(root).as_posix()}")
        except ValueError:
            print(f"  {target}")
    return 0


def command_restore(args, root: Path) -> int:
    require_repository(root)
    busy = in_progress(root)
    if busy:
        raise Refused(f"{', '.join(busy)} is unfinished; resolve it before restoring")
    files = files_at(root, args.rev, args.path)
    backup = root / ".tmp" / "recovered" / f"before-restore-{datetime.now():%Y%m%d-%H%M%S}"
    kept, replaced = [], []
    for name in files:
        current = root / name
        if current.is_file():
            target = backup / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(current, target)
            kept.append(name)
        write_blob(root, args.rev, name, current)
        replaced.append(name)
    extra = []
    if (root / args.path).is_dir():
        wanted = set(files)
        extra = [p.relative_to(root).as_posix() for p in (root / args.path).rglob("*") if p.is_file() and p.relative_to(root).as_posix() not in wanted]
    print(f"Restored {len(replaced)} file(s) from version {short(root, args.rev)}: " + ", ".join(replaced[:10]) + (" ..." if len(replaced) > 10 else ""))
    if kept:
        print(f"The previous content was copied first to {backup.relative_to(root).as_posix()}/; copy it back to undo.")
    if extra:
        print("Files that did not exist in that version were left in place: " + ", ".join(extra[:10]))
    print("Nothing was saved as a new version; review the result, then save it if wanted.")
    return 0


def command_untrack(args, root: Path) -> int:
    require_repository(root)
    if not git(root, "ls-files", "--", args.path).stdout.strip():
        raise Refused(f"{args.path} is not in the version history")
    git(root, "rm", "-r", "-q", "--cached", "--", args.path)
    print(f"{args.path} will leave the version history at the next save; the files stay on this computer. "
          "Earlier versions still contain it.")
    return 0


def command_practice(args, root: Path) -> int:
    folder = root / ".tmp" / "git-practice"
    marker = folder / ".practice"
    if folder.exists():
        if not args.reset:
            print(f"The practice copy exists at {folder.relative_to(root).as_posix()}/. Use --reset to start it again.")
            return 0
        if not marker.is_file():
            raise Refused(f"{folder} was not created by this script; it was left unchanged")
        shutil.rmtree(folder)
    folder.mkdir(parents=True)
    marker.write_text("practice repository created by scripts/versions.py\n", encoding="utf-8")
    practice = ["git", "-C", str(folder)]
    subprocess.run(practice + ["init", "-q", "-b", "main"], check=True)
    subprocess.run(practice + ["config", "--local", "user.name", "Practice"], check=True)
    subprocess.run(practice + ["config", "--local", "user.email", "practice@localhost"], check=True)
    (folder / ".git" / "info" / "exclude").write_text(".practice\n", encoding="utf-8")
    print(f"Created an empty practice repository at {folder.relative_to(root).as_posix()}/. "
          f"Write a short README and practice note there, then save versions with --root {folder.relative_to(root).as_posix()}.")
    return 0


def confirmed_destinations(root: Path) -> str:
    privacy = root / "requirements" / "privacy.md"
    return privacy.read_text(encoding="utf-8") if privacy.is_file() else ""


def destination_confirmed(url: str, record: str) -> bool:
    """Only a dedicated marker confirms an exact backup destination."""
    if not url:
        return False
    prefix = "<!-- confirmed-backup-destination: "
    return any(line.strip() == f"{prefix}{url} -->" for line in record.splitlines())


def repository_address(url: str) -> str:
    """Classify a resolved Git address as template, other, or uncertain."""
    url = url.strip()
    if not url:
        return "uncertain"
    if "://" in url:
        parsed = urlsplit(url)
        if parsed.scheme.lower() == "file":
            return "other" if parsed.path and not parsed.query and not parsed.fragment else "uncertain"
        if parsed.scheme.lower() not in {"https", "http", "ssh", "git"} or not parsed.hostname or parsed.query or parsed.fragment:
            return "uncertain"
        host, path = parsed.hostname.lower().rstrip("."), parsed.path
    elif re.match(r"^[^/\s]+@?[^/\s]*:[^/].*$", url) and not re.match(r"^[A-Za-z]:[\\/]", url):
        host_part, path = url.split(":", 1)
        host = host_part.rsplit("@", 1)[-1].lower().rstrip(".")
    elif url.startswith(("/", "./", "../")) or re.match(r"^[A-Za-z]:[\\/]", url):
        return "other"
    elif ":" not in url and "@" not in url and not any(char.isspace() for char in url):
        return "other"  # a relative local repository path
    else:
        return "uncertain"
    if host.endswith(".github.com"):
        # A GitHub subdomain may redirect or proxy to the canonical host.
        return "uncertain"
    if host != TEMPLATE_REPOSITORY[0]:
        # An SSH host alias could resolve to GitHub, so do not infer its target.
        return "uncertain" if "@" in url or url.startswith("ssh://") else "other"
    parts = path.strip("/").removesuffix(".git").lower().split("/")
    if len(parts) != 2 or not all(parts):
        return "uncertain"
    return "template" if tuple(parts) == TEMPLATE_REPOSITORY[1:] else "other"


def remote_urls(root: Path, name: str, *, push: bool = False) -> list[str]:
    args = ("remote", "get-url", "--push", "--all", name) if push else ("remote", "get-url", "--all", name)
    result = git(root, *args, check=False)
    return result.stdout.splitlines() if result.returncode == 0 else []


def shared_remote_config(root: Path) -> bool:
    """Remote configuration is shared by all worktrees of one repository."""
    paths = git(root, "rev-parse", "--git-dir", "--git-common-dir").stdout.splitlines()
    if len(paths) != 2:
        return True
    resolved = [(root / value).resolve() for value in paths]
    if resolved[0] != resolved[1]:
        return True
    return sum(line.startswith("worktree ") for line in git(root, "worktree", "list", "--porcelain").stdout.splitlines()) > 1


def clear_removed_remote_defaults(root: Path, name: str) -> None:
    """Clear local default-push pointers that Git may leave after remote removal."""
    pattern = r"^(remote\.pushDefault|branch\..*\.(pushRemote|remote))$"
    entries = git(root, "config", "--local", "--null", "--get-regexp", pattern, check=False).stdout
    for item in entries.split("\0"):
        if not item or "\n" not in item:
            continue
        key, value = item.split("\n", 1)
        if value == name:
            git(root, "config", "--local", "--unset-all", key)


def command_detach_template(args, root: Path) -> int:
    if not shutil.which("git"):
        if (root / ".git").exists():
            raise Refused("Git is unavailable but this workspace has Git configuration; install Git before completing the template-remote check")
        print("Git is unavailable and this folder has no Git configuration; nothing needs disconnecting.")
        return 0
    if not is_repository(root):
        if (root / ".git").exists():
            raise Refused("this workspace has Git configuration that could not be inspected safely; do not mark setup complete")
        print("This folder has no Git repository of its own; no template remote was changed.")
        return 0
    names = git(root, "remote").stdout.splitlines()
    if not names:
        print("No remote is configured; nothing needs disconnecting.")
        return 0
    matches, blocked = [], []
    for name in names:
        fetch, push = remote_urls(root, name), remote_urls(root, name, push=True)
        kinds = {repository_address(url) for url in fetch + push} if fetch and push else {"uncertain"}
        if "uncertain" in kinds:
            blocked.append(f"{name}: an address could not be identified; inspect its fetch and push URLs")
        elif "template" in kinds and "other" in kinds:
            blocked.append(f"{name}: template and other destinations are mixed; choose how to separate them")
        elif kinds == {"template"}:
            matches.append(name)
    if args.apply and matches and shared_remote_config(root):
        blocked.append("remote configuration is shared with another Git worktree; choose a safe workspace-specific action")
        matches = []
    if matches:
        if args.apply:
            for name in matches:
                git(root, "remote", "remove", name)
                clear_removed_remote_defaults(root, name)
            print("Disconnected template remote(s): " + ", ".join(matches) + ". Local files, branches, and commits remain.")
        else:
            print("Template remote(s) to disconnect: " + ", ".join(matches) + ". Run with --apply during confirmed project setup.")
    else:
        print("No unambiguous template remote needs disconnecting.")
    for item in blocked:
        print("Needs a researcher decision: " + item + ".")
    return 3 if blocked else 0


def command_remotes(args, root: Path) -> int:
    require_repository(root)
    names = git(root, "remote").stdout.split()
    if not names:
        print("No external copy is configured: all versions exist only on this computer.")
        return 0
    confirmed = confirmed_destinations(root)
    for name in names:
        url = git(root, "remote", "get-url", name).stdout.strip()
        status = "confirmed in requirements/privacy.md" if destination_confirmed(url, confirmed) else "not confirmed as a backup destination"
        print(f"{name}: {redact(url)} ({status})")
    return 0


def command_backup(args, root: Path) -> int:
    require_repository(root)
    if not has_commits(root):
        raise Refused("there is no saved version to back up")
    if args.remote not in git(root, "remote").stdout.split():
        raise Refused(f"there is no external copy called {args.remote}; set it up with the researcher's confirmed destination first")
    fetch_urls = remote_urls(root, args.remote)
    push_urls = remote_urls(root, args.remote, push=True)
    if not fetch_urls or not push_urls:
        raise Refused("the remote's fetch or push destination cannot be identified; nothing was sent")
    if any(repository_address(url) == "template" for url in fetch_urls + push_urls):
        raise Refused("this remote reaches the template repository; it cannot be a research backup destination")
    if any(repository_address(url) == "uncertain" for url in fetch_urls + push_urls):
        raise Refused("a remote address cannot be identified safely; resolve its fetch and push destinations first")
    confirmed = confirmed_destinations(root)
    if any(not destination_confirmed(url, confirmed) for url in fetch_urls + push_urls):
        raise Refused("every actual fetch and push address must be recorded as a confirmed destination in requirements/privacy.md; "
                      "confirm visibility and what may leave this computer first")
    if len(fetch_urls) != 1 or len(push_urls) != 1 or fetch_urls[0] != push_urls[0]:
        raise Refused("this remote has different or multiple fetch and push addresses; a verified backup needs one identical confirmed address")
    url = push_urls[0]
    branch = args.branch or git(root, "branch", "--show-current").stdout.strip()
    if not branch:
        raise Refused("no branch is checked out; name the branch to back up with --branch")
    known = [ref for ref in remote_heads(root, args.remote) if ref.endswith(f"/{branch}")]
    new_range = f"{known[0]}..{branch}" if known else branch
    names = set(git(root, "log", "--format=", "--name-only", new_range).stdout.split())
    secrets = sorted(name for name in names if SECRET_NAME.search(name))
    if secrets:
        raise Refused("the versions to back up contain files that look like secrets: " + ", ".join(secrets) +
                      ". Removing them from history is a separate decision; nothing was sent")
    pushed = git(root, "push", args.remote, f"refs/heads/{branch}:refs/heads/{branch}", check=False)
    if pushed.returncode != 0:
        print("The backup failed; nothing is confirmed as copied. " + redact(pushed.stderr.strip())[-400:])
        return 1
    local = git(root, "rev-parse", branch).stdout.strip()
    remote = git(root, "ls-remote", args.remote, f"refs/heads/{branch}", check=False).stdout.split()
    if remote and remote[0] == local:
        print(f"Backed up branch {branch} to {redact(url)} and checked that the copy holds version {local[:7]}.")
        return 0
    print(f"The push finished, but the copy at {redact(url)} could not be checked; treat the backup as unverified.")
    return 1


def main(argv: list | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Operate the workspace's version history safely.")
    parser.add_argument("--root", type=Path, default=ROOT, help="workspace root (default: the parent of the scripts folder)")
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="report the version history and unsaved work without changing anything")
    inspect.add_argument("--json", action="store_true")
    commands.add_parser("scope", help="show what the history tracks, what is new, and what the ignore rules exclude")
    commands.add_parser("init", help="create an empty version history, with ignore rules for secrets")
    identity = commands.add_parser("identity", help="set the author name and e-mail for this workspace only")
    identity.add_argument("--name", required=True)
    identity.add_argument("--email", required=True)
    save = commands.add_parser("save", help="save a version of the named files or of every change")
    save.add_argument("--message", required=True)
    save.add_argument("--path", action="append")
    save.add_argument("--all", action="store_true")
    save.add_argument("--allow-large", action="store_true")
    history = commands.add_parser("history", help="list saved versions")
    history.add_argument("--path")
    history.add_argument("--limit", type=int, default=20)
    compare = commands.add_parser("compare", help="compare a saved version with another or with the current files")
    compare.add_argument("--from", dest="from_rev", default="HEAD")
    compare.add_argument("--to", dest="to_rev")
    compare.add_argument("--path", action="append")
    compare.add_argument("--words", action="store_true", help="show the changed words")
    retrieve = commands.add_parser("retrieve", help="copy files from a saved version without changing the current files")
    retrieve.add_argument("--rev", required=True)
    retrieve.add_argument("--path", required=True)
    retrieve.add_argument("--to")
    restore = commands.add_parser("restore", help="replace current files with a saved version, keeping a copy of the current content")
    restore.add_argument("--rev", required=True)
    restore.add_argument("--path", required=True)
    untrack = commands.add_parser("untrack", help="stop tracking a file or folder while keeping it on this computer")
    untrack.add_argument("--path", required=True)
    practice = commands.add_parser("practice", help="create a disposable practice copy with its own history")
    practice.add_argument("--reset", action="store_true")
    commands.add_parser("remotes", help="list external copies and whether each is a confirmed destination")
    detach = commands.add_parser("detach-template", help="inspect or disconnect remotes to the original template repository")
    detach.add_argument("--apply", action="store_true", help="remove unambiguous template remotes from this local repository")
    backup = commands.add_parser("backup", help="copy saved versions to a confirmed external destination and check the copy")
    backup.add_argument("--remote", required=True)
    backup.add_argument("--branch")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    handlers = {"inspect": command_inspect, "scope": command_scope, "init": command_init, "identity": command_identity,
                "save": command_save, "history": command_history, "compare": command_compare, "retrieve": command_retrieve,
                "restore": command_restore, "untrack": command_untrack, "practice": command_practice,
                "remotes": command_remotes, "detach-template": command_detach_template, "backup": command_backup}
    try:
        return handlers[args.command](args, root)
    except Refused as error:
        print(f"Refused: {error}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
