#!/usr/bin/env python3
"""Check record links and run integrity, set up code folders, import repositories, and record research runs.

The check reports broken local links, missing or changed checksummed files, and unreadable or inconsistent run
records. It does not validate the wording or form of researcher-written records. Unknown labels and statuses are
ignored; new records should use the suggested layouts in the relevant directory README.

Usage:
  python scripts/research.py check
  python scripts/research.py code-init [--part src|data|runs|outputs|notebooks ...] [--venv] [--python PATH]
  python scripts/research.py code-import --source ADDRESS_OR_PATH --name NAME [--data exclude|include]
      [--output-dir NAME ...] [--max-size-mb N] [--timeout SECONDS]
  python scripts/research.py code-attach --path code/NAME [--output-dir NAME ...]
  python scripts/research.py run --name NAME [--input PATH ...] [--output PATH ...] [--code PATH ...]
      [--cwd PATH] [--note TEXT] [--freeze] [--timeout SECONDS] -- COMMAND [ARG ...]
  python scripts/research.py runs
Paths are relative to the workspace root. A run's command starts in the workspace root, or in --cwd; the
command's arguments are passed unchanged, so they are relative to that directory.
Exit status: 0 done (reported record facts do not fail the command); 1 the run failed; 2 a result is stale
(an input, output, or recorded code version changed); 3 refused. Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import string
import subprocess
import sys
import tarfile
import time
import urllib.parse
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ingestion.common import (checksum, read_json, relative, sha256_file, slug,  # noqa: E402
                              write_json_atomic, write_text_atomic)

ROOT = Path(__file__).resolve().parent.parent
FIELD = re.compile(r"^[-*] ([^:：\[\]`]{1,40}?)\s*[:：]\s*(.*)$")
NESTED = re.compile(r"^\s{2,}[-*] (.*)$")
LINK = re.compile(r"\]\(([^)\s]+)\)")
TICKED = re.compile(r"`([^`]+)`")
CHECKSUM = re.compile(r"`([^`]+)`[^`]*?sha256:([0-9a-f]{64})")
SKIP = ("README.md", "index.md")
NONE_WORDS = ("none", "not yet", "n/a", "no check", "无", "尚无", "暂无", "未检查")


class Refused(Exception):
    pass


TEMPLATES = Path(__file__).resolve().parent / "research_templates"


def render(template: str, /, **values) -> str:
    """Fill a template file from scripts/research_templates/. Each ${placeholder} takes the value given for it; trailing newlines are dropped."""
    return string.Template((TEMPLATES / template).read_text(encoding="utf-8")).substitute(values).rstrip("\n")


# Recognized labels let this check follow links and provenance; unknown labels and statuses are ignored.

DECISION_LABELS = {"date": ("date", "日期"), "status": ("status", "状态"), "choice": ("choice", "选择", "决定"),
                   "scope": ("scope", "适用范围", "范围"), "confirmed": ("confirmed", "确认"),
                   "replaces": ("replaces", "取代"), "replaced_by": ("replaced by", "被取代", "取代者")}
DECISION_STATUS = {"active": ("active", "有效"), "replaced": ("replaced", "已被取代", "已取代"), "withdrawn": ("withdrawn", "已撤回")}

FEEDBACK_LABELS = {"from": ("from", "提出者", "来自"), "source": ("source", "出处", "来源"), "kind": ("kind", "类型"),
                   "suggestion": ("suggestion", "建议", "内容"), "affects": ("affects", "涉及"), "status": ("status", "状态"),
                   "decision": ("decision", "决定"), "change": ("change", "改动", "修改")}
FEEDBACK_KIND = {"exact statement": ("exact statement", "原话"),
                 "researcher recollection": ("researcher recollection", "研究者回忆", "研究者的回忆"),
                 "agent summary": ("agent summary", "智能体摘要", "代理摘要", "ai 摘要", "ai摘要")}
FEEDBACK_STATUS = {"received": ("received", "已收到"), "under discussion": ("under discussion", "讨论中"),
                   "adopted in part": ("adopted in part", "部分采纳"), "adopted": ("adopted", "已采纳"),
                   "declined": ("declined", "未采纳", "已拒绝"), "implemented": ("implemented", "已实施", "已落实")}
IDEA_STATUS = {"exploratory": ("exploratory", "探索中"), "developed": ("developed", "已发展", "已深化"),
               "incorporated": ("incorporated", "已纳入"), "abandoned": ("abandoned", "已放弃")}

RESULT_LABELS = {"status": ("status", "状态"), "inputs": ("inputs", "输入"), "outputs": ("outputs", "输出"), "run": ("run", "运行"),
                 "used_by": ("used by", "用于")}
RESULT_STATUS = {"observed": ("observed", "已观察"), "checked": ("checked", "已检查")}


# Reading records

def parse_fields(text: str, labels: dict) -> dict:
    """Map each label key to a list of (value, nested lines) for top-level "- Label: value" bullets."""
    names = {name.lower(): key for key, aliases in labels.items() for name in aliases}
    found: dict = {}
    current = None
    for line in text.splitlines():
        match = FIELD.match(line)
        if match:
            key = names.get(match.group(1).strip().lower())
            current = None
            if key:
                current = [match.group(2).strip(), []]
                found.setdefault(key, []).append(current)
            continue
        nested = NESTED.match(line)
        if nested and current is not None:
            current[1].append(nested.group(1).strip())
        elif line.strip() and not line.startswith(" "):
            current = None
    return {key: [(value, lines) for value, lines in entries] for key, entries in found.items()}


def one(fields: dict, key: str) -> str | None:
    entries = fields.get(key) or []
    return entries[0][0] if len(entries) == 1 else None


def full_text(fields: dict, key: str) -> str:
    return "\n".join(value + "\n" + "\n".join(lines) for value, lines in fields.get(key) or [])


def status_of(value: str | None, statuses: dict) -> str | None:
    """The status whose word starts the value; longer words win, so "adopted in part" is not "adopted"."""
    if not value:
        return None
    text = value.strip().strip("*").lower()
    best = None
    for status, words in statuses.items():
        for word in words:
            if text.startswith(word) and (best is None or len(word) > best[1]):
                best = (status, len(word))
    return best[0] if best else None


def sections(text: str) -> list:
    """(heading, body) for each "## " section."""
    return [(block.partition("\n")[0].strip(), block.partition("\n")[2]) for block in re.split(r"^## ", text, flags=re.M)[1:]]


def link_targets(text: str) -> list:
    return [target.split("#", 1)[0] for target in LINK.findall(text) if not target.startswith(("http://", "https://", "mailto:", "#"))]


def is_empty(value: str | None) -> bool:
    text = (value or "").strip().strip(".。").lower()
    return not text or any(text == word or text.startswith(word + " ") for word in NONE_WORDS)


# Checks by record type

def check_decisions(root: Path) -> list:
    """Check only relationships between recorded choices, not their writing format."""
    folder = root / "research" / "decisions"
    if not folder.is_dir():
        return []
    problems, records = [], {}
    for path in sorted(folder.glob("*.md")):
        if path.name not in SKIP:
            records[path.name] = parse_fields(path.read_text(encoding="utf-8"), DECISION_LABELS)
            problems.extend(f"{path.relative_to(root).as_posix()}: links to {target}, which does not exist"
                            for target in broken_links(path, root))
    statuses = {name: status_of(one(fields, "status"), DECISION_STATUS) for name, fields in records.items()}
    index = folder / "index.md"
    if index.is_file():
        problems.extend(f"research/decisions/index.md: links to {target}, which does not exist" for target in broken_links(index, root))
    for name, fields in records.items():
        where = f"research/decisions/{name}"
        replaced_by = [Path(t).name for t in link_targets(full_text(fields, "replaced_by") + full_text(fields, "status")) if t.endswith(".md")]
        replaces = [Path(t).name for t in link_targets(full_text(fields, "replaces")) if t.endswith(".md")]
        for target in replaced_by + replaces:
            if target not in records:
                problems.append(f"{where}: links to {target}, which does not exist")
        if statuses[name] == "replaced":
            for target in replaced_by:
                if target in records and name not in [Path(t).name for t in link_targets(full_text(records[target], "replaces"))]:
                    problems.append(f"{where}: {target} does not link back in its Replaces field")
        for target in replaces:
            if target in records and statuses.get(target) not in ("replaced", None):
                problems.append(f"{where}: links to {target}, which is not marked replaced")
    return problems


def local_link_exists(target: str, base: Path, root: Path) -> bool:
    candidate = (base / target) if not target.startswith("/") else root / target.lstrip("/")
    return candidate.exists() or (root / target).exists()


def broken_links(path: Path, root: Path) -> list[str]:
    """Return missing local Markdown link targets in one file."""
    return [target for target in link_targets(path.read_text(encoding="utf-8"))
            if not local_link_exists(target, path.parent, root)]


def check_feedback(root: Path) -> list:
    """Check links behind implemented feedback claims without enforcing a record template."""
    base = root / "research" / "feedback"
    if not base.is_dir():
        return []
    problems = []
    for event in sorted(p for p in base.iterdir() if p.is_dir()):
        actions = event / "actions.md"
        if not actions.is_file():
            continue
        problems.extend(f"research/feedback/{event.name}/actions.md: links to {target}, which does not exist"
                        for target in broken_links(actions, root))
        for heading, body in sections(actions.read_text(encoding="utf-8")):
            fields = parse_fields(body, FEEDBACK_LABELS)
            status = status_of(one(fields, "status"), FEEDBACK_STATUS)
            if status != "implemented":
                continue
            change = full_text(fields, "change")
            targets = link_targets(change) + [t for t in TICKED.findall(change) if "/" in t or t.endswith(".md")]
            if not targets:
                problems.append(f"research/feedback/{event.name}/actions.md {heading}: marked implemented but no change location is given")
            for target in dict.fromkeys(targets):
                if not local_link_exists(target, event, root):
                    problems.append(f"research/feedback/{event.name}/actions.md {heading}: the change location {target} does not exist")
    return problems


def check_ideas(root: Path) -> list:
    """Check links in the optional ideas index; omit naming, status, and registration rules."""
    folder = root / "ideas"
    index = folder / "index.md"
    if not folder.is_dir():
        return []
    problems = []
    files = [p for p in folder.glob("*.md") if p.name not in SKIP]
    for path in files + ([index] if index.is_file() else []):
        problems.extend(f"{path.relative_to(root).as_posix()}: links to {target}, which does not exist"
                        for target in broken_links(path, root))
    return problems


def check_results(root: Path) -> tuple:
    folder = root / "research" / "results"
    if not folder.is_dir():
        return [], []
    problems, stale = [], []
    for path in sorted(folder.glob("*.md")):
        if path.name in SKIP:
            continue
        where = f"research/results/{path.name}"
        stale_start = len(stale)
        problems.extend(f"{where}: links to {target}, which does not exist" for target in broken_links(path, root))
        fields = parse_fields(path.read_text(encoding="utf-8"), RESULT_LABELS)
        status = status_of(one(fields, "status"), RESULT_STATUS)
        for key in ("inputs", "outputs"):
            for target, expected in CHECKSUM.findall(full_text(fields, key)):
                file = root / target
                if not file.exists():
                    problems.append(f"{where}: the {key[:-1]} {target} does not exist")
                elif checksum(file) != expected:
                    stale.append(f"{where}: the {key[:-1]} {target} changed after the result was recorded")
        for target in dict.fromkeys(TICKED.findall(full_text(fields, "run")) + link_targets(full_text(fields, "run"))):
            if "runs/" not in target:
                continue
            run_path = folder / target
            if not run_path.exists():
                run_path = root / target.lstrip("/") if target.startswith("/") else root / target
            if not run_path.is_file():
                problems.append(f"{where}: the run record {target} does not exist")
                continue
            if run_path.name != "run.json":
                continue
            try:
                run = json.loads(run_path.read_text(encoding="utf-8"))
                if not isinstance(run, dict) or not isinstance(run.get("code", []), list):
                    raise ValueError("expected a run object with a code list")
                if status in ("observed", "checked") and run.get("status") != "complete":
                    problems.append(f"{where}: the run did not complete: {target}")
                for entry in run.get("code", []):
                    code_path, expected = entry["path"], entry.get("sha256")
                    if entry.get("kind") == "git":
                        if not shutil.which("git"):
                            problems.append(f"{where}: Git is needed to check the recorded repository code {code_path}, and it was not found")
                            continue
                        current = repository_identity(root, code_path)
                        if current is None:
                            stale.append(f"{where}: the recorded code {code_path} is missing, or is no longer a separate Git repository")
                        elif identity_of(current) != identity_of(entry):
                            stale.append(f"{where}: the recorded code {code_path} changed after the run")
                        continue
                    if not expected:
                        continue
                    current = resolve(root, code_path)
                    if not current.exists():
                        stale.append(f"{where}: the recorded code {code_path} is missing")
                    elif checksum(current) != expected:
                        stale.append(f"{where}: the recorded code {code_path} changed after the run")
            except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
                problems.append(f"{where}: cannot read run record {target}: {error}")
        if len(stale) > stale_start:
            uses = full_text(fields, "used_by").strip()
            suffix = (f"; recheck recorded dependents: {uses}" if uses and not is_empty(uses)
                      else "; dependent passages and exhibits are not recorded; inspect the manuscript before reuse")
            stale[stale_start:] = [item + suffix for item in stale[stale_start:]]
    index = folder / "index.md"
    if index.is_file():
        problems.extend(f"research/results/index.md: links to {target}, which does not exist" for target in broken_links(index, root))
    return problems, stale


def check_venues(root: Path) -> list:
    """Check local links in venue notes and their optional index."""
    folder = root / "research" / "venues"
    if not folder.is_dir():
        return []
    problems = []
    files = [p for p in folder.glob("*.md") if p.name not in SKIP]
    index = folder / "index.md"
    for path in files + ([index] if index.is_file() else []):
        problems.extend(f"{path.relative_to(root).as_posix()}: links to {target}, which does not exist"
                        for target in broken_links(path, root))
    return problems


def command_check(args, root: Path) -> int:
    problems = check_decisions(root) + check_feedback(root) + check_ideas(root)
    result_problems, stale = check_results(root)
    problems += result_problems + check_venues(root)
    for problem in problems:
        print(problem)
    for item in stale:
        print(f"stale: {item}")
    if stale:
        print(f"Stale evidence: {len(stale)} input(s), output(s), or recorded code version(s) changed; these results cannot be treated as current.")
        return 2
    if problems:
        print(f"Research record facts: {len(problems)} issue(s) reported.")
    else:
        print("No broken research-record links or run-integrity issues were found.")
    return 0


# The research code folder

PARTS = ("src", "data", "runs", "outputs", "notebooks")


def command_code_init(args, root: Path) -> int:
    code = root / "code"
    parts = list(dict.fromkeys(args.part or []))
    created = []
    for name in parts:
        folder = code / name
        if not folder.is_dir():
            folder.mkdir(parents=True, exist_ok=True)
            created.append(folder.relative_to(root).as_posix())
        if name == "data":
            for sub in ("raw", "derived"):
                path = folder / sub
                if not path.is_dir():
                    path.mkdir(parents=True, exist_ok=True)
                    created.append(path.relative_to(root).as_posix())
    if args.venv:
        venv = code / ".venv"
        if venv.exists():
            print("code/.venv already exists; it was left unchanged.")
        else:
            python = args.python or sys.executable
            completed = subprocess.run([python, "-m", "venv", str(venv)], capture_output=True, text=True)
            if completed.returncode != 0:
                print(f"Creating code/.venv failed: {completed.stderr.strip()[-400:]}")
                return 1
            created.append("code/.venv (research environment, ignored by Git)")
    print("Created: " + (", ".join(created) if created else "no new directories."))
    return 0


# Code repositories: a separate Git repository under code/, imported or attached. Its .git folder is the boundary
# that separates Codex sessions. Claude sessions must start at the repository root for the verified exclusions to keep paper instructions out.

REPOSITORY_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
REMOTE_ADDRESS = re.compile(r"^(?:[A-Za-z][A-Za-z0-9+.-]*://|[\w.-]+@[\w.-]+:)")
ARCHIVE_SUFFIXES = (".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tar.xz")
ENVIRONMENT_FILES = ("renv.lock", "DESCRIPTION", "requirements.txt", "environment.yml", "pyproject.toml")
OUTPUT_FOLDERS = ("output", "outputs")
# An imported copy leaves these behind: local histories, caches, environments, and secrets are not the code.
LOCAL_FILES = frozenset({".Rhistory", ".RData", ".DS_Store", "Thumbs.db", "desktop.ini"})
LOCAL_FOLDERS = frozenset({".git", ".Rproj.user", ".venv", "venv", "__pycache__", "node_modules", ".ipynb_checkpoints"})
LOCAL_TREES = ("renv/library", "renv/staging")
DATA_SUFFIXES = (".csv", ".tsv", ".xlsx", ".xls", ".rds", ".rdata", ".rda", ".parquet", ".feather", ".arrow", ".fst",
                 ".sav", ".dta", ".sas7bdat", ".sqlite", ".sqlite3", ".db", ".h5", ".hdf5")


def is_secret_file(name: str) -> bool:
    if name == ".Renviron":
        return True
    return (name == ".env" or name.startswith(".env.")) and not name.endswith((".example", ".sample", ".template"))


def in_folder(rel: str, folders: list) -> bool:
    return any(rel == folder or rel.startswith(folder + "/") for folder in folders)


def is_data_file(rel: str, output_folders: list) -> bool:
    """Research data by its file type, except inside the repository's output folders."""
    return rel.lower().endswith(DATA_SUFFIXES) and not in_folder(rel, output_folders)


def normalize_folders(values: list | None) -> list | None:
    """Output folders as repository-relative POSIX paths; None when none were given."""
    if values is None:
        return None
    folders = []
    for value in values:
        folder = value.replace("\\", "/").strip().strip("/")
        if not folder or "/../" in f"/{folder}/" or Path(folder).is_absolute():
            raise Refused(f"the output folder {value!r} must be a folder inside the repository")
        folders.append(folder)
    return list(dict.fromkeys(folders))


def public_remote(address: str) -> str:
    """A repository address without a password or token."""
    if "://" not in address:
        return address
    try:
        parts = urllib.parse.urlsplit(address)
        host = (parts.hostname or "") + (f":{parts.port}" if parts.port else "")
    except ValueError:
        return address.rsplit("@", 1)[-1]
    user = f"{parts.username}@" if parts.username and parts.scheme not in ("http", "https") else ""
    return urllib.parse.urlunsplit((parts.scheme, user + host, parts.path, "", ""))


def ensure_block(path: Path, block: str) -> bool:
    """Add the entries of a block of lines that a text file lacks, after the block's comment lines; True when the file changed."""
    lines = [line.rstrip() for line in block.splitlines()]
    comments = [line for line in lines if line.startswith("#")]
    entries = [line for line in lines if line and not line.startswith("#")]
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    present = {line.strip() for line in text.splitlines()}
    missing = [line for line in entries if line not in present]
    if not missing:
        return False
    addition = [line for line in comments if line not in present] + missing
    base = text if not text or text.endswith("\n") else text + "\n"
    if base and addition[0].startswith("#"):
        base += "\n"
    write_text_atomic(path, base + "\n".join(addition) + "\n")
    return True


def glob_literal(path: str) -> str:
    """A path as a glob that matches only itself: characters that a glob treats as special go in bracket classes."""
    return "".join("[[]" if char == "[" else f"[{char}]" if char in "*?(){}" else char for char in path.replace("\\", "/"))


def run_git(arguments: list, folder: Path | None = None, timeout: float | None = None):
    """Run Git without ever waiting for a password, and capture its output as text."""
    command = ["git"] + (["-C", str(folder)] if folder else []) + arguments
    return subprocess.run(command, capture_output=True, text=True, env=dict(os.environ, GIT_TERMINAL_PROMPT="0"), timeout=timeout)


def is_git_root(path: Path) -> bool:
    if not (path / ".git").exists():
        return False
    top = git_text(path, "rev-parse", "--show-toplevel")
    return bool(top) and Path(top).resolve() == path.resolve()


def require_git_root(path: Path, label: str) -> None:
    if not shutil.which("git"):
        raise Refused("Git is needed to attach a repository, and it was not found")
    if (path / ".git").is_file():
        raise Refused(f"{label} has a .git file (a submodule or a linked worktree); use an independent clone with its own .git folder")
    if not (path / ".git").is_dir():
        raise Refused(f"{label} is not a Git repository; use code-import to bring a folder in as one")
    top = git_text(path, "rev-parse", "--show-toplevel")
    if not top or Path(top).resolve() != path.resolve():
        raise Refused(f"{label} is not the root of its Git repository")


def repository_path(root: Path, value: str) -> Path:
    """The folder of a repository that sits directly under code/."""
    path = resolve(root, value)
    if path.is_symlink():
        raise Refused("give the repository folder itself, not a symbolic link to it")
    if path.parent.resolve() != (root / "code").resolve():
        raise Refused("the repository must sit directly under code/, for example code/analysis")
    if path.name in PARTS or not REPOSITORY_NAME.match(path.name):
        raise Refused(f"{path.name!r} cannot name a repository folder; start with a letter or digit, and avoid {', '.join(sorted(PARTS))}")
    return path


def write_claude_exclusions(root: Path, repository: Path) -> str:
    """Keep this workspace's CLAUDE.md and AGENTS.md out of Claude Code sessions started inside the repository."""
    settings, name = repository / ".claude" / "settings.local.json", ".claude/settings.local.json"
    shown = relative(settings, root)
    if git_output(repository, "ls-files", "--error-unmatch", "--", name) is not None:
        return f"Warning: {shown} is tracked by the repository, so the Claude Code exclusions were not written"
    ensure_block(repository / ".git" / "info" / "exclude", render("git-exclude-claude-settings.txt"))
    wanted = [line for line in render("claude-md-excludes.txt", workspace=glob_literal(root.resolve().as_posix())).splitlines() if line.strip()]
    data = {}
    if settings.is_file():
        try:
            data = json.loads(settings.read_text(encoding="utf-8"))
        except ValueError:
            raise Refused(f"{shown} is not valid JSON; fix or remove it, then run the command again")
        if not isinstance(data, dict) or not isinstance(data.get("claudeMdExcludes", []), list):
            raise Refused(f"{shown} has an unexpected form; fix or remove it, then run the command again")
    current = data.get("claudeMdExcludes", [])
    merged = current + [pattern for pattern in wanted if pattern not in current]
    changed = merged != current or "claudeMdExcludes" not in data
    if changed:
        data["claudeMdExcludes"] = merged
        write_json_atomic(settings, data)
    bridge = ""
    own = [repository / "CLAUDE.md", repository / ".claude" / "CLAUDE.md", repository / "CLAUDE.local.md"]
    if (repository / "AGENTS.md").is_file() and not any(path.exists() for path in own):
        # Claude Code reads a repository's AGENTS.md only when no CLAUDE.md applies, so a local CLAUDE.md passes it on.
        write_text_atomic(repository / "CLAUDE.md", render("claude-import-agents.md") + "\n")
        ensure_block(repository / ".git" / "info" / "exclude", render("git-exclude-claude-import.txt"))
        bridge = " and a local CLAUDE.md that imports the repository's AGENTS.md"
    return ((f"wrote the Claude Code exclusions to {shown}" if changed else f"the Claude Code exclusions in {shown} were already in place")
            + bridge + "; neither is part of the repository's history. They hold absolute paths, so run code-attach again after moving the workspace")



def update_registry(root: Path, name: str, entry: dict) -> None:
    """Record repository facts in code/repositories.json."""
    registry = root / "code" / "repositories.json"
    data = read_json(registry, None)
    if not isinstance(data, dict) or not isinstance(data.get("repositories"), dict):
        data = {"schema": "paper-template.code-repositories/1", "repositories": {}}
    earlier = data["repositories"].get(name, {})
    for key in ("source", "output_folders", "data_left_behind"):
        if entry.get(key) is None and earlier.get(key) is not None:
            entry[key] = earlier[key]
    if entry.get("output_folders") is None:
        entry["output_folders"] = []
    data["repositories"][name] = {key: value for key, value in entry.items() if value is not None}
    write_json_atomic(registry, data)


def attach_repository(root: Path, repository: Path, source: str | None, declared: list | None, data_left: int | None = None) -> list:
    """Make a Git repository that sits directly under code/ part of the workspace. Returns what happened, one line each."""
    name = repository.name
    notes = []
    for secret in (".Renviron", ".env", ".env.local"):
        if git_output(repository, "ls-files", "--error-unmatch", "--", secret) is not None:
            raise Refused(f"{relative(repository / secret, root)} is tracked by the repository's Git history; remove it from the "
                          "history first (its content was not read)")
    exposed = [secret for secret in (".Renviron", ".env", ".env.local")
               if (repository / secret).exists() and git_output(repository, "check-ignore", "-q", "--", secret) is None]
    if exposed:
        notes.append(f"Warning: {', '.join(exposed)} in code/{name} is not ignored by the repository; add it to the repository's "
                     ".gitignore in a session opened there, so that a commit cannot include it")
    if ensure_block(root / ".gitignore", render("workspace-gitignore.txt", name=name)):
        notes.append(f"added code/{name}/ to .gitignore")
    remotes = (git_text(repository, "remote") or "").split()
    remote = "origin" if "origin" in remotes else (remotes[0] if remotes else None)
    address = git_text(repository, "remote", "get-url", remote) if remote else None
    folders = declared if declared is not None else ([folder for folder in OUTPUT_FOLDERS if (repository / folder).is_dir()] or None)
    update_registry(root, name, {
        "remote": public_remote(address) if address else None, "source": source,
        "commit": git_text(repository, "rev-parse", "--short=12", "HEAD"),
        "environment": [item for item in ENVIRONMENT_FILES if (repository / item).is_file()],
        "output_folders": folders, "data_left_behind": data_left, "attached": datetime.now().strftime("%Y-%m-%d")})
    notes.append("recorded its repository facts in code/repositories.json")
    notes.append(write_claude_exclusions(root, repository))
    if not remotes:
        notes.append("Warning: the repository has no remote, so its only copy is this folder; ask the researcher where it should be backed up")
    if git_text(repository, "status", "--porcelain"):
        notes.append("Warning: the repository has uncommitted changes; commit them in a session opened there before a run that supports a claim")
    return notes


def session_advice(name: str) -> list:
    return render("code-session-advice.txt", name=name).splitlines()


def command_code_attach(args, root: Path) -> int:
    path = repository_path(root, args.path)
    if not path.is_dir():
        raise Refused(f"{args.path} does not exist; bring the repository in with code-import first")
    require_git_root(path, args.path)
    notes = attach_repository(root, path, None, normalize_folders(args.output_dir))
    print(f"Attached code/{path.name}.")
    for note in notes + session_advice(path.name):
        print(f"- {note}")
    return 0


def classify_source(source: str, root: Path) -> tuple:
    """What a source is: ("remote", None) for a Git address, or (kind, path) for an archive, a Git folder, or a plain folder."""
    if source.startswith("-"):
        raise Refused("the source cannot start with a dash")
    local = Path(source).expanduser()
    if local.exists():
        local, workspace = local.resolve(), root.resolve()
        if local == workspace or local in workspace.parents:
            raise Refused("the source contains this workspace; give the repository's own folder")
        if local.is_file():
            if local.name.lower().endswith(ARCHIVE_SUFFIXES):
                return "archive", local
            raise Refused(f"{local.name} is a file but not an archive ({', '.join(ARCHIVE_SUFFIXES)})")
        return ("git" if is_git_root(local) else "folder"), local
    if REMOTE_ADDRESS.match(source):
        return "remote", None
    raise Refused(f"cannot find {source}; give a folder, an archive, or a Git address such as https://host/owner/repo.git")


def clone_repository(address: str, target: Path, timeout: float | None) -> None:
    try:
        completed = run_git(["clone", "--quiet", "--", address, str(target)], timeout=timeout or 900)
    except subprocess.TimeoutExpired:
        raise Refused("git clone took too long and was stopped")
    if completed.returncode != 0:
        message = completed.stderr.strip().replace(address, public_remote(address))[-300:] or "no message"
        raise Refused(f"git clone failed: {message}. A private repository needs credentials that Git already holds; "
                      "this tool never asks for a password.")


def fix_origin(target: Path, address: str | None) -> None:
    """Point origin at the original address without credentials, or remove it when the source had none."""
    if address:
        run_git(["remote", "set-url", "origin", public_remote(address)], target)
    else:
        run_git(["remote", "remove", "origin"], target)


def extract_archive(archive: Path, destination: Path, limit: int) -> Path:
    """Unpack an archive into a new empty folder without trusting its member names; return the folder that holds the code."""
    destination.mkdir(parents=True)
    base = destination.resolve()
    allowed, total, count = max(limit * 5, 1 << 30), 0, 0

    def place(name: str) -> Path:
        path = (base / name).resolve()
        if path != base and base not in path.parents:
            raise Refused(f"the archive holds an unsafe path: {name}")
        return path

    def account(size: int) -> None:
        nonlocal total, count
        total, count = total + size, count + 1
        if total > allowed or count > 200000:
            raise Refused("the archive expands to far more than the import limit; unpack it yourself and give the folder instead")

    try:
        if archive.name.lower().endswith(".zip"):
            with zipfile.ZipFile(archive) as bundle:
                for member in bundle.infolist():
                    account(member.file_size)
                    if (member.external_attr >> 16) & 0o170000 == 0o120000:
                        continue
                    path = place(member.filename)
                    if member.is_dir():
                        path.mkdir(parents=True, exist_ok=True)
                    else:
                        path.parent.mkdir(parents=True, exist_ok=True)
                        with bundle.open(member) as stream, open(path, "wb") as out:
                            shutil.copyfileobj(stream, out)
        else:
            with tarfile.open(archive) as bundle:
                for member in bundle:
                    account(member.size)
                    if not (member.isfile() or member.isdir()):
                        continue
                    path = place(member.name)
                    if member.isdir():
                        path.mkdir(parents=True, exist_ok=True)
                        continue
                    path.parent.mkdir(parents=True, exist_ok=True)
                    stream = bundle.extractfile(member)
                    if stream is not None:
                        with stream, open(path, "wb") as out:
                            shutil.copyfileobj(stream, out)
    except (zipfile.BadZipFile, tarfile.TarError, OSError, EOFError) as error:
        raise Refused(f"cannot read the archive: {error}")
    entries = [entry for entry in destination.iterdir() if entry.name != "__MACOSX"]
    return entries[0] if len(entries) == 1 and entries[0].is_dir() else destination


def collect_files(source: Path, outputs: list, keep_data: bool) -> tuple:
    """The files to copy from a folder as (relative path, size) pairs, how many were left behind for each reason, and the data files left behind."""
    kept, data_left = [], []
    left = {"secret files": 0, "local history and caches": 0, "symbolic links": 0}
    for folder, names, files in os.walk(source):
        here = Path(folder)
        base = here.relative_to(source).as_posix()
        prefix = "" if base == "." else base + "/"
        remaining = []
        for name in sorted(names):
            if (here / name).is_symlink():
                left["symbolic links"] += 1
            elif name in LOCAL_FOLDERS or prefix + name in LOCAL_TREES:
                left["local history and caches"] += 1
            else:
                remaining.append(name)
        names[:] = remaining
        for name in sorted(files):
            path, rel = here / name, prefix + name
            if path.is_symlink():
                left["symbolic links"] += 1
            elif is_secret_file(name):
                left["secret files"] += 1
            elif name in LOCAL_FILES:
                left["local history and caches"] += 1
            elif not keep_data and is_data_file(rel, outputs):
                data_left.append(rel)
            else:
                kept.append((rel, path.stat().st_size))
    return kept, left, data_left


def untracked_data_files(source: Path, outputs: list) -> list:
    """Data files in a Git folder that a clone leaves behind, because Git does not track them."""
    listing = git_output(source, "ls-files", "-z", "--others") or b""
    names = [item for item in listing.decode("utf-8", errors="replace").split("\0") if item]
    return [name for name in names if is_data_file(name, outputs) and not in_folder(name, list(LOCAL_TREES))
            and not any(part in LOCAL_FOLDERS for part in name.split("/")[:-1])]


def listed_files(files: list, limit: int = 15) -> str:
    return ", ".join(f"`{item}`" for item in files[:limit]) + (f", and {len(files) - limit} more" if len(files) > limit else "")


def protective_block(outputs: list) -> str:
    """The new repository's .git/info/exclude block, so that a commit cannot take in secrets, local history, or research data."""
    return render("git-exclude-import.txt", data_patterns="\n".join(f"*{suffix}" for suffix in DATA_SUFFIXES),
                  output_patterns="\n".join(f"!/{folder}/**" for folder in outputs))


def commit_options(repository: Path, root: Path) -> list:
    """Git options that give a commit the researcher's name and e-mail when the new repository has none of its own."""
    options = []
    for key in ("user.name", "user.email"):
        if git_text(repository, "config", key):
            continue
        value = git_text(root, "config", key)
        if not value:
            raise Refused(f"no Git {key} is set; ask the researcher for it and save it with python scripts/versions.py identity")
        options += ["-c", f"{key}={value}"]
    return options


def import_folder(root: Path, source: Path, target: Path, outputs: list, keep_data: bool, limit: int, name: str, commit_message: str | None) -> tuple:
    """Copy a folder that has no Git history into target as a new repository with one initial commit. Returns notes and the data files left behind."""
    if not commit_message or not commit_message.strip():
        raise Refused("a plain-folder import needs an initial commit message supplied by the agent")
    kept, left, data_left = collect_files(source, outputs, keep_data)
    if not kept:
        raise Refused("that folder holds no files to import once local history, caches, secrets, and data files are left out")
    total = sum(size for _, size in kept)
    if total > limit:
        raise Refused(f"the folder holds {total / 1048576:.0f} MB to copy, above the limit of {limit / 1048576:.0f} MB; leave large "
                      "files behind, or raise --max-size-mb after the researcher agrees")
    target.mkdir(parents=True)
    started = run_git(["init", "--quiet", "--initial-branch=main", str(target)])
    if started.returncode != 0:
        started = run_git(["init", "--quiet", str(target)])
    if started.returncode != 0:
        raise Refused("git init failed: " + started.stderr.strip()[-300:])
    ensure_block(target / ".git" / "info" / "exclude", protective_block(outputs))
    for rel, _ in kept:
        destination = target / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / rel, destination)
    options = commit_options(target, root)
    added = run_git(["add", "-A"], target)
    message = commit_message.strip()
    committed = run_git(["-c", "commit.gpgsign=false", *options, "commit", "--quiet", "--no-verify", "-m", message], target) \
        if added.returncode == 0 else added
    if committed.returncode != 0:
        raise Refused("the initial commit failed: " + (committed.stderr.strip() or committed.stdout.strip())[-300:])
    notes = [f"copied {len(kept)} file(s) ({total / 1048576:.1f} MB) and made the initial commit {git_text(target, 'rev-parse', '--short=12', 'HEAD')}"]
    notes += [f"left behind {count} {reason}" for reason, count in left.items() if count]
    return notes, data_left


def command_code_import(args, root: Path) -> int:
    name = args.name
    if name in PARTS or not REPOSITORY_NAME.match(name):
        raise Refused(f"{name!r} cannot name a repository folder; start with a letter or digit, and avoid {', '.join(sorted(PARTS))}")
    if not shutil.which("git"):
        raise Refused("Git is needed to import a repository, and it was not found")
    target = root / "code" / name
    if target.exists() or target.is_symlink():
        raise Refused(f"code/{name} already exists; choose another name, or use code-attach for a repository that is already there")
    kind, local = classify_source(args.source, root)
    declared = normalize_folders(args.output_dir)
    limit = int(args.max_size_mb * 1024 * 1024)
    temporary = None
    (root / "code").mkdir(exist_ok=True)
    try:
        if kind == "archive":
            label = f"{local.name} sha256:{sha256_file(local)[:12]}"
            temporary = root / ".tmp" / f"code-import-{name}-{datetime.now():%Y%m%d%H%M%S}"
            local = extract_archive(local, temporary, limit)
            kind = "git" if is_git_root(local) else "folder"
        elif kind == "remote":
            label = public_remote(args.source)
        elif kind == "git":
            label = local.name
        else:
            label = local.name
        notes, data_left = [], None
        if kind == "remote":
            clone_repository(args.source, target, args.timeout)
            fix_origin(target, args.source)
            notes.append(render("import-data-left-behind-unknown.txt"))
        elif kind == "git":
            outputs = declared if declared is not None else [folder for folder in OUTPUT_FOLDERS if (local / folder).is_dir()]
            if git_text(local, "status", "--porcelain"):
                notes.append("Warning: the source has uncommitted changes, which were not imported; commit them in the source first "
                             "if they matter")
            leftover = untracked_data_files(local, outputs)
            clone_repository(str(local), target, args.timeout)
            fix_origin(target, git_text(local, "remote", "get-url", "origin"))
            data_left = len(leftover)
            if leftover:
                notes.append(render("import-data-left-behind-git.txt", count=len(leftover), files=listed_files(leftover)))
        else:
            outputs = declared if declared is not None else [folder for folder in OUTPUT_FOLDERS if (local / folder).is_dir()]
            copied, leftover = import_folder(root, local, target, outputs, args.data == "include", limit, name, args.commit_message)
            notes += copied
            data_left = len(leftover)
            if leftover:
                notes.append(render("import-data-left-behind-folder.txt", count=len(leftover), files=listed_files(leftover)))
        tracked = [item for item in (git_text(target, "ls-files") or "").splitlines()
                   if is_data_file(item, declared if declared is not None else list(OUTPUT_FOLDERS))]
        if tracked and kind != "folder":
            notes.append(f"Note: the history tracks {len(tracked)} data file(s) outside the output folders; they are in the copy, and "
                         "workspace sessions leave them unread unless the researcher asks")
        notes += attach_repository(root, target, label, declared, data_left)
    except (Refused, OSError, subprocess.SubprocessError):
        shutil.rmtree(target, ignore_errors=True)
        raise
    finally:
        if temporary is not None:
            shutil.rmtree(temporary, ignore_errors=True)
    print(f"Imported code/{name} ({'Git repository' if kind in ('git', 'remote') else 'folder without Git history, now a new repository'}).")
    for note in notes + session_advice(name):
        print(f"- {note}")
    return 0


# Recorded runs

R_PACKAGES = 'ip <- installed.packages(); write.table(ip[, c("Package", "Version")], quote = FALSE, row.names = FALSE, sep = "\\t")'


def resolve(root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    return path if path.is_absolute() else root / path


def describe(paths: list, root: Path) -> list:
    entries = []
    for value in paths:
        path = resolve(root, value)
        entry = {"path": relative(path, root), "exists": path.exists()}
        if path.exists():
            entry.update(kind="folder" if path.is_dir() else "file", sha256=checksum(path))
            if path.is_file():
                entry["bytes"] = path.stat().st_size
        entries.append(entry)
    return entries


def git_state(root: Path) -> dict:
    if not shutil.which("git"):
        return {"available": False}
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True)
    if head.returncode != 0:
        return {"available": True, "repository": False}
    dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--", "code"], capture_output=True, text=True)
    return {"available": True, "repository": True, "commit": head.stdout.strip(), "code_uncommitted": bool(dirty.stdout.strip())}


def git_output(folder: Path, *arguments: str) -> bytes | None:
    """The standard output of a Git command run in folder, or None when Git is missing or the command fails."""
    if not shutil.which("git"):
        return None
    completed = subprocess.run(["git", "-C", str(folder), *arguments], capture_output=True, env=dict(os.environ, GIT_TERMINAL_PROMPT="0"))
    return completed.stdout if completed.returncode == 0 else None


def git_text(folder: Path, *arguments: str) -> str | None:
    output = git_output(folder, *arguments)
    return output.decode("utf-8", errors="replace").strip() if output is not None else None


def separate_repository(root: Path, path: Path) -> Path | None:
    """The root of the Git repository that holds path, when it is a repository of its own, apart from the workspace."""
    top = git_text(path if path.is_dir() else path.parent, "rev-parse", "--show-toplevel")
    if not top:
        return None
    repository, workspace = Path(top).resolve(), root.resolve()
    return None if repository == workspace or repository in workspace.parents else repository


def uncommitted_digest(repository: Path, spec: str, committed: bool) -> str | None:
    """A digest of the changes under spec since the last commit, with new files that Git does not ignore; None when there are none."""
    digest, changed = hashlib.sha256(), False
    if committed:
        diff = git_output(repository, "diff", "HEAD", "--binary", "--no-color", "--no-ext-diff", "--", spec)
        if diff:
            digest.update(diff)
            changed = True
    flags = ["--others"] if committed else ["--cached", "--others"]
    listing = git_output(repository, "ls-files", "-z", *flags, "--exclude-standard", "--", spec) or b""
    for name in sorted(item for item in listing.decode("utf-8", errors="replace").split("\0") if item):
        file = repository / name
        if file.is_file():
            digest.update(f"{name}\t{sha256_file(file)}\n".encode("utf-8"))
            changed = True
    return digest.hexdigest() if changed else None


def repository_identity(root: Path, value: str) -> dict | None:
    """What identifies code that lives in a separate Git repository: the commit, the content of the named path at that
    commit, and any change since. None for code that is not in a separate repository."""
    path = resolve(root, value)
    if not path.exists():
        return None
    repository = separate_repository(root, path)
    if repository is None:
        return None
    try:
        spec = path.resolve().relative_to(repository).as_posix()
    except ValueError:
        return None
    commit = git_text(repository, "rev-parse", "--verify", "HEAD") or None
    tree = git_text(repository, "rev-parse", "HEAD^{tree}" if spec == "." else f"HEAD:{spec}") if commit else None
    digest = uncommitted_digest(repository, spec, commit is not None)
    return {"path": relative(path, root), "kind": "git", "repository": relative(repository, root), "commit": commit, "tree": tree,
            "uncommitted": digest is not None, "uncommitted_sha256": digest, "exists": True}


def identity_of(entry: dict) -> tuple:
    return entry.get("tree"), entry.get("uncommitted_sha256")


def code_entries(paths: list, root: Path) -> list:
    """Describe the code of a run: code in a separate Git repository by its Git state, any other code by checksum."""
    entries = []
    for value in paths:
        identity = repository_identity(root, value)
        entries.extend([identity] if identity else describe([value], root))
    return entries


def code_changed(root: Path, entry: dict) -> bool:
    """True when recorded code no longer matches: a different Git state, a changed checksum, or code that is gone."""
    if entry.get("kind") == "git":
        current = repository_identity(root, entry["path"])
        return current is None or identity_of(current) != identity_of(entry)
    path = resolve(root, entry["path"])
    return bool(entry.get("sha256")) and (not path.exists() or checksum(path) != entry["sha256"])


def environment_files(cwd: Path, code: list, root: Path) -> list:
    """The renv.lock files that fix the R packages of a run: beside the working directory and in each code repository."""
    folders = [cwd] + [resolve(root, entry["repository"]) for entry in code if entry.get("kind") == "git"]
    locks = [folder / "renv.lock" for folder in dict.fromkeys(folders) if (folder / "renv.lock").is_file()]
    return describe([relative(lock, root) for lock in locks], root)


def executable_of(command: list, root: Path) -> str:
    """The program to start: a path is taken relative to the workspace root, a bare name is looked up on PATH."""
    first = command[0]
    if "/" in first or "\\" in first:
        candidate = resolve(root, first)
        return str(candidate) if candidate.exists() else first
    return shutil.which(first) or first


def interpreter(command: list, executable: str) -> dict:
    info = {"program": command[0], "resolved": executable}
    name = Path(executable).name.lower()
    name = name[:-4] if name.endswith(".exe") else name
    if "python" in name:
        info["language"] = "python"
    elif name in ("rscript", "r"):
        info["language"] = "r"
    if "language" in info:
        try:
            version = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=30)
            lines = (version.stdout or version.stderr).strip().splitlines()
        except (OSError, subprocess.TimeoutExpired):
            lines = []
        info["version"] = lines[0].strip() if lines else ""
    return info


def command_run(args, root: Path) -> int:
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        raise Refused("give the command after --, for example: -- code/.venv/bin/python code/src/analysis.py")
    name = slug(args.name, limit=40, fallback="run")
    missing = [value for value in args.input or [] if not resolve(root, value).exists()]
    if missing:
        raise Refused("these inputs do not exist: " + ", ".join(missing))
    cwd = resolve(root, args.cwd) if args.cwd else root
    if not cwd.is_dir():
        raise Refused(f"the working directory does not exist: {args.cwd}")
    code_paths = args.code or (["code/src"] if (root / "code" / "src").is_dir() else [])
    runs = root / "code" / "runs"
    run_id = f"{datetime.now(timezone.utc):%Y%m%d-%H%M%S}-{name}"
    number = 2
    while (runs / run_id).exists():
        run_id, number = f"{datetime.now(timezone.utc):%Y%m%d-%H%M%S}-{name}-{number}", number + 1
    folder = runs / run_id
    folder.mkdir(parents=True)
    executable = executable_of(command, root)
    record = {
        "schema": "paper-template.research-run/1", "run_id": run_id, "name": args.name, "note": args.note or "",
        "command": command, "working_directory": relative(cwd, root), "inputs": describe(args.input or [], root),
        "code": code_entries(code_paths, root), "git": git_state(root), "interpreter": interpreter(command, executable),
        "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine(),
                     "python_of_this_script": platform.python_version()},
        "started_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    for entry in record["code"]:
        if entry.get("uncommitted"):
            print(f"Warning: {entry['path']} has uncommitted changes. The run records them by digest, and committing them later "
                  "makes the result stale; commit the code in a session opened in its repository before a run that supports a claim.")
    locks = environment_files(cwd, record["code"], root)
    if locks:
        record["environment_files"] = locks
    language = record["interpreter"].get("language")
    if args.freeze and language in ("python", "r"):
        listing = ["-m", "pip", "freeze"] if language == "python" else ["-e", R_PACKAGES]
        frozen = subprocess.run([record["interpreter"]["resolved"]] + listing, capture_output=True, text=True, cwd=cwd)
        write_text_atomic(folder / "environment.txt", frozen.stdout)
        record["environment"] = "environment.txt"
    began = time.monotonic()
    try:
        with open(folder / "stdout.txt", "w", encoding="utf-8", errors="replace") as out, \
                open(folder / "stderr.txt", "w", encoding="utf-8", errors="replace") as err:
            completed = subprocess.run([executable] + command[1:], cwd=cwd, stdout=out, stderr=err, timeout=args.timeout)
        record["exit_code"] = completed.returncode
    except subprocess.TimeoutExpired:
        record["exit_code"] = None
        record["error"] = f"stopped after {args.timeout} seconds"
    except OSError as error:
        record["exit_code"] = None
        record["error"] = f"the command could not start: {error}"
    record["seconds"] = round(time.monotonic() - began, 3)
    record["finished_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    record["outputs"] = describe(args.output or [], root)
    absent = [entry["path"] for entry in record["outputs"] if not entry["exists"]]
    if absent and record.get("exit_code") == 0:
        record["error"] = "declared outputs are missing: " + ", ".join(absent)
    record["status"] = "complete" if record.get("exit_code") == 0 and not absent else "failed"
    write_json_atomic(folder / "run.json", record)
    print(f"Run {run_id}: {record['status']}" + (f" ({record['error']})" if record.get("error") else "") +
          f". Record: code/runs/{run_id}/run.json")
    if record["status"] == "complete":
        print("For the result record:")
        print("- Inputs:")
        for entry in record["inputs"]:
            print(f"  - `{entry['path']}` sha256:{entry['sha256']}")
        print("- Outputs:")
        for entry in record["outputs"]:
            print(f"  - `{entry['path']}` sha256:{entry['sha256']}")
        print(f"- Run: `code/runs/{run_id}/run.json`")
        repositories = [entry for entry in record["code"] if entry.get("kind") == "git"]
        if repositories:
            print("- Code (name the commit in the Method line):")
            for entry in repositories:
                print(f"  - `{entry['path']}` commit {entry['commit']} tree {entry['tree']}"
                      + (" with uncommitted changes" if entry["uncommitted"] else ""))
    return 0 if record["status"] == "complete" else 1


def command_runs(args, root: Path) -> int:
    runs = root / "code" / "runs"
    records = sorted(runs.glob("*/run.json")) if runs.is_dir() else []
    if not records:
        print("No recorded runs.")
        return 0
    for path in records:
        record = json.loads(path.read_text(encoding="utf-8"))
        changed = [e["path"] for e in record.get("outputs", []) + record.get("inputs", [])
                   if e.get("sha256") and (not resolve(root, e["path"]).exists() or checksum(resolve(root, e["path"])) != e["sha256"])]
        changed += [e["path"] for e in record.get("code", []) if code_changed(root, e)]
        print(f"{record['run_id']}: {record['status']}" + (f"; changed since the run: {', '.join(changed)}" if changed else ""))
    return 0


def main(argv: list | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Report record links and run integrity, manage code folders, and record research runs.")
    parser.add_argument("--root", type=Path, default=ROOT, help="workspace root (default: the parent of the scripts folder)")
    commands = parser.add_subparsers(dest="name_of_command", required=True)
    commands.add_parser("check", help="report broken links, run-integrity facts, and stale results")
    init = commands.add_parser("code-init", help="create the research code folder with the parts that the research needs")
    init.add_argument("--part", action="append", choices=sorted(PARTS))
    init.add_argument("--venv", action="store_true", help="create the research environment code/.venv")
    init.add_argument("--python", help="interpreter for code/.venv (default: the one running this script)")
    run = commands.add_parser("run", help="run research code and record its provenance in code/runs/")
    run.add_argument("--name", required=True)
    run.add_argument("--input", action="append")
    run.add_argument("--output", action="append")
    run.add_argument("--code", action="append", help="code files or folders that identify the code version (default: code/src); "
                     "code in a separate Git repository is identified by its commit and uncommitted changes, other code by checksum")
    run.add_argument("--cwd", help="folder in which the command starts (default: the workspace root); the command's arguments are relative to it")
    run.add_argument("--note")
    run.add_argument("--freeze", action="store_true", help="also record the installed Python or R packages of the interpreter")
    run.add_argument("--timeout", type=float)
    run.add_argument("command", nargs=argparse.REMAINDER)
    imported = commands.add_parser("code-import", help="import an external code repository into code/NAME as its own Git repository")
    imported.add_argument("--source", required=True, help="a Git address, a folder (with or without Git), or an archive (.zip, .tar.gz, ...)")
    imported.add_argument("--name", required=True, help="folder name under code/")
    imported.add_argument("--data", choices=("exclude", "include"), default="exclude",
                          help="for a folder without Git history: leave data files behind (default) or copy them, keeping them out of the history")
    imported.add_argument("--output-dir", action="append", help="repository folder that holds outputs (default: output and outputs when present)")
    imported.add_argument("--max-size-mb", type=float, default=100, help="refuse to copy more than this many MB (default: 100)")
    imported.add_argument("--timeout", type=float, help="seconds allowed for cloning (default: 900)")
    imported.add_argument("--commit-message", help="agent-written initial commit message for a folder without Git history")
    attached = commands.add_parser("code-attach", help="register a Git repository that already sits in code/NAME")
    attached.add_argument("--path", required=True, help="the repository folder, for example code/analysis")
    attached.add_argument("--output-dir", action="append", help="repository folder that holds outputs (default: keep or detect output and outputs)")
    commands.add_parser("runs", help="list recorded runs and whether their files changed since")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    handlers = {"check": command_check, "code-init": command_code_init, "code-import": command_code_import,
                "code-attach": command_code_attach, "run": command_run, "runs": command_runs}
    try:
        return handlers[args.name_of_command](args, root)
    except Refused as error:
        print(f"Refused: {error}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
