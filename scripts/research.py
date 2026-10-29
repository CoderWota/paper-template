#!/usr/bin/env python3
"""Check research records, set up a research code folder, and run research code with recorded provenance.

Research records are files that the researcher reads and confirms, written in the interaction language:
decision records (research/decisions/), feedback actions (research/feedback/<feedback-id>/actions.md),
retained ideas (ideas/), venue notes (research/venues/), and result records (research/results/). Their
labels and status words stay as the README of each folder lists them, so that this check can read them;
the Chinese labels and status words listed in this file are accepted as well.

Usage:
  python scripts/research.py check
  python scripts/research.py code-init [--part src|data|runs|outputs|notebooks ...] [--venv] [--python PATH]
  python scripts/research.py run --name NAME [--input PATH ...] [--output PATH ...] [--code PATH ...]
      [--note TEXT] [--freeze] [--timeout SECONDS] -- COMMAND [ARG ...]
  python scripts/research.py runs
Paths are relative to the workspace root, and a run's command starts in the workspace root.
Exit status: 0 done; 1 problems found, or the run failed; 2 the records are valid but a result is stale
(an input or output changed after the result was recorded); 3 refused. Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ingestion.common import checksum, relative, slug, update_readme, write_json_atomic, write_text_atomic  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FIELD = re.compile(r"^[-*] ([^:：\[\]`]{1,40}?)\s*[:：]\s*(.*)$")
NESTED = re.compile(r"^\s{2,}[-*] (.*)$")
QUOTE = re.compile(r"[\"“「『][^\"”」』]{2,}[\"”」』]")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
LINK = re.compile(r"\]\(([^)\s]+)\)")
TICKED = re.compile(r"`([^`]+)`")
CHECKSUM = re.compile(r"`([^`]+)`[^`]*?sha256:([0-9a-f]{64})")
URL = re.compile(r"https?://\S+")
SLUG_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SKIP = ("README.md", "index.md")
NONE_WORDS = ("none", "not yet", "n/a", "no check", "无", "尚无", "暂无", "未检查")


class Refused(Exception):
    pass


# Labels and status words. Values are written in the interaction language; these words stay fixed.

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
DECIDED = ("adopted in part", "adopted", "declined", "implemented")

IDEA_STATUS = {"exploratory": ("exploratory", "探索中"), "developed": ("developed", "已发展", "已深化"),
               "incorporated": ("incorporated", "已纳入"), "abandoned": ("abandoned", "已放弃")}

RESULT_LABELS = {"status": ("status", "状态"), "kind": ("kind", "类型"), "question": ("question", "问题"),
                 "method": ("method", "方法"), "inputs": ("inputs", "输入"), "parameters": ("parameters", "参数"),
                 "run": ("run", "运行"), "outputs": ("outputs", "输出"), "checks": ("checks", "检查"),
                 "limitations": ("limitations", "局限"), "used_by": ("used by", "用于"),
                 "review": ("researcher review", "研究者审阅")}
RESULT_STATUS = {"proposed": ("proposed", "已提议"), "attempted": ("attempted", "已尝试"), "observed": ("observed", "已观察"),
                 "checked": ("checked", "已检查"), "failed": ("failed", "失败")}

VENUE_LABELS = {"checked": ("checked", "核查日期", "查阅日期"), "sources": ("sources", "来源", "官方来源")}


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


def words_of(statuses: dict) -> str:
    return ", ".join(statuses)


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
    folder = root / "research" / "decisions"
    if not folder.is_dir():
        return []
    problems, records, numbers = [], {}, {}
    for path in sorted(folder.glob("*.md")):
        if path.name in SKIP:
            continue
        match = re.match(r"^(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$", path.name)
        if not match:
            problems.append(f"research/decisions/{path.name}: name a decision record NNNN-short-title.md, in lowercase ASCII letters, digits, and hyphens")
            continue
        if match.group(1) in numbers:
            problems.append(f"research/decisions/{path.name}: number {match.group(1)} is also used by {numbers[match.group(1)]}")
        numbers[match.group(1)] = path.name
        records[path.name] = parse_fields(path.read_text(encoding="utf-8"), DECISION_LABELS)
    statuses = {}
    for name, fields in records.items():
        where = f"research/decisions/{name}"
        for key in ("date", "status", "choice", "scope", "confirmed"):
            if one(fields, key) is None:
                problems.append(f"{where}: expected one {DECISION_LABELS[key][0].capitalize()} line (accepted labels: {', '.join(DECISION_LABELS[key])})")
        if one(fields, "date") and not DATE.search(one(fields, "date")):
            problems.append(f"{where}: the Date line needs a date such as 2026-10-28")
        if one(fields, "confirmed") and not QUOTE.search(one(fields, "confirmed")):
            problems.append(f"{where}: the Confirmed line must quote the researcher's words")
        status = status_of(one(fields, "status"), DECISION_STATUS)
        statuses[name] = status
        if one(fields, "status") and status is None:
            problems.append(f"{where}: unknown status; use one of: {words_of(DECISION_STATUS)}")
    for name, fields in records.items():
        where = f"research/decisions/{name}"
        replaced_by = [Path(t).name for t in link_targets(full_text(fields, "replaced_by") + full_text(fields, "status")) if t.endswith(".md")]
        replaces = [Path(t).name for t in link_targets(full_text(fields, "replaces")) if t.endswith(".md")]
        if statuses[name] == "replaced":
            if not replaced_by:
                problems.append(f"{where}: a replaced decision links to the decision that replaces it (Replaced by: [NNNN](NNNN-....md))")
            for target in replaced_by:
                if target not in records:
                    problems.append(f"{where}: links to {target}, which does not exist")
                elif name not in [Path(t).name for t in link_targets(full_text(records[target], "replaces"))]:
                    problems.append(f"{where}: {target} does not name it in its Replaces line")
        for target in replaces:
            if target not in records:
                problems.append(f"{where}: replaces {target}, which does not exist")
            elif statuses.get(target) != "replaced":
                problems.append(f"{where}: replaces {target}, but {target} is not marked as replaced")
    index = folder / "index.md"
    text = index.read_text(encoding="utf-8") if index.is_file() else ""
    if records and not index.is_file():
        problems.append("research/decisions/index.md is missing")
    lines = text.splitlines()
    listed = {Path(t).name for t in link_targets(text) if t.endswith(".md")}
    for target in sorted(listed):
        if not (folder / target).is_file():
            problems.append(f"research/decisions/index.md: links to {target}, which does not exist")
    for name in records:
        if name not in listed:
            problems.append(f"research/decisions/index.md: {name} is not listed")
        elif statuses[name] == "replaced":
            replacement = [Path(t).name for t in link_targets(full_text(records[name], "replaced_by") + full_text(records[name], "status"))]
            row = next((line for line in lines if f"({name})" in line or f"/{name})" in line), "")
            if replacement and not any(r in row for r in replacement):
                problems.append(f"research/decisions/index.md: the line for {name} must link to the decision that replaces it")
    return problems


def local_link_exists(target: str, base: Path, root: Path) -> bool:
    candidate = (base / target) if not target.startswith("/") else root / target.lstrip("/")
    return candidate.exists() or (root / target).exists()


def check_feedback(root: Path) -> list:
    base = root / "research" / "feedback"
    if not base.is_dir():
        return []
    problems = []
    for event in sorted(p for p in base.iterdir() if p.is_dir()):
        where = f"research/feedback/{event.name}"
        if not SLUG_NAME.match(event.name):
            problems.append(f"{where}: name a feedback folder <YYYY-MM-DD>-<short-title>, in lowercase ASCII letters, digits, and hyphens")
        actions = event / "actions.md"
        if not actions.is_file():
            problems.append(f"{where}: actions.md is missing; list each suggestion with its attribution (research-feedback)")
            continue
        seen = set()
        for heading, body in sections(actions.read_text(encoding="utf-8")):
            match = re.match(r"^(F\d+)\b", heading)
            if not match:
                problems.append(f"{where}/actions.md: the heading {heading!r} must start with a suggestion ID such as F1")
                continue
            item = f"{where}/actions.md {match.group(1)}"
            if match.group(1) in seen:
                problems.append(f"{item}: the ID is used twice")
            seen.add(match.group(1))
            fields = parse_fields(body, FEEDBACK_LABELS)
            for key in ("from", "source", "kind", "status"):
                if one(fields, key) is None:
                    problems.append(f"{item}: expected one {FEEDBACK_LABELS[key][0].capitalize()} line (accepted labels: {', '.join(FEEDBACK_LABELS[key])})")
            for key in ("from", "source", "suggestion"):
                if fields.get(key) and not full_text(fields, key).strip():
                    problems.append(f"{item}: the {FEEDBACK_LABELS[key][0].capitalize()} line is empty")
            if not fields.get("suggestion"):
                problems.append(f"{item}: expected a Suggestion line (accepted labels: {', '.join(FEEDBACK_LABELS['suggestion'])})")
            if one(fields, "kind") and status_of(one(fields, "kind"), FEEDBACK_KIND) is None:
                problems.append(f"{item}: unknown kind; use one of: {words_of(FEEDBACK_KIND)}")
            status = status_of(one(fields, "status"), FEEDBACK_STATUS)
            if one(fields, "status") and status is None:
                problems.append(f"{item}: unknown status; use one of: {words_of(FEEDBACK_STATUS)}")
            if status in DECIDED:
                decision = full_text(fields, "decision")
                linked = [t for t in link_targets(decision) if "decisions/" in t or "requirements/" in t]
                if not (QUOTE.search(decision) or linked):
                    problems.append(f"{item}: the suggestion is {status}, so it needs a Decision line that quotes the researcher or links the decision record or requirement")
            if status == "implemented":
                change = full_text(fields, "change")
                targets = link_targets(change) + [t for t in TICKED.findall(change) if "/" in t or t.endswith(".md")]
                if not targets:
                    problems.append(f"{item}: the suggestion is implemented, so it needs a Change line that links the actual change")
                for target in targets:
                    if not local_link_exists(target, event, root):
                        problems.append(f"{item}: the change {target} does not exist")
    return problems


def check_ideas(root: Path) -> list:
    folder = root / "ideas"
    if not folder.is_dir():
        return []
    problems = []
    notes = {p.name for p in folder.glob("*.md") if p.name not in SKIP}
    index = folder / "index.md"
    if not index.is_file():
        return ["ideas/index.md is missing"] if notes else []
    linked = set()
    for line in index.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^[-*] ", line):
            continue
        lowered = line.lower()
        if not any(word in lowered for words in IDEA_STATUS.values() for word in words):
            problems.append(f"ideas/index.md: the line {line.strip()!r} names no status ({words_of(IDEA_STATUS)})")
        for target in link_targets(line):
            if target.endswith(".md"):
                if not (folder / target).is_file():
                    problems.append(f"ideas/index.md: links to {target}, which does not exist")
                linked.add(Path(target).name)
    for note in sorted(notes):
        if note not in linked:
            problems.append(f"ideas/{note}: not listed in ideas/index.md")
        fields = parse_fields((folder / note).read_text(encoding="utf-8"), {"status": ("status", "状态")})
        value = one(fields, "status")
        if value and status_of(value, IDEA_STATUS) is None:
            problems.append(f"ideas/{note}: unknown status; use one of: {words_of(IDEA_STATUS)}")
    return problems


def check_results(root: Path) -> tuple:
    folder = root / "research" / "results"
    if not folder.is_dir():
        return [], []
    problems, stale = [], []
    names = []
    for path in sorted(folder.glob("*.md")):
        if path.name in SKIP:
            continue
        where = f"research/results/{path.name}"
        if not SLUG_NAME.match(path.stem):
            problems.append(f"{where}: name a result record with lowercase ASCII letters, digits, and hyphens, for example r001-smoke-test.md")
        names.append(path.name)
        fields = parse_fields(path.read_text(encoding="utf-8"), RESULT_LABELS)
        for key in ("status", "kind", "question", "method", "limitations"):
            if one(fields, key) is None:
                problems.append(f"{where}: expected one {RESULT_LABELS[key][0].capitalize()} line (accepted labels: {', '.join(RESULT_LABELS[key])})")
        status = status_of(one(fields, "status"), RESULT_STATUS)
        if one(fields, "status") and status is None:
            problems.append(f"{where}: unknown status; use one of: {words_of(RESULT_STATUS)}")
        if status in ("observed", "checked") and not CHECKSUM.search(full_text(fields, "outputs")):
            problems.append(f"{where}: an {status} result lists its outputs with checksums (`path` sha256:...)")
        if status in ("observed", "checked", "failed") and not fields.get("inputs"):
            problems.append(f"{where}: an {status} result lists its inputs")
        if status == "checked" and is_empty(full_text(fields, "checks").strip()):
            problems.append(f"{where}: a checked result says which checks were made and what they found")
        for key in ("inputs", "outputs"):
            for target, expected in CHECKSUM.findall(full_text(fields, key)):
                file = root / target
                if not file.exists():
                    problems.append(f"{where}: the {key[:-1]} {target} does not exist")
                elif checksum(file) != expected:
                    stale.append(f"{where}: the {key[:-1]} {target} changed after the result was recorded")
        for target in TICKED.findall(full_text(fields, "run")) + link_targets(full_text(fields, "run")):
            if "runs/" in target and not local_link_exists(target, folder, root):
                problems.append(f"{where}: the run record {target} does not exist")
    index = folder / "index.md"
    listed = {Path(t).name for t in link_targets(index.read_text(encoding="utf-8"))} if index.is_file() else set()
    if names and not index.is_file():
        problems.append("research/results/index.md is missing")
    for name in names:
        if index.is_file() and name not in listed:
            problems.append(f"research/results/index.md: {name} is not listed")
    for target in sorted(listed):
        if target.endswith(".md") and not (folder / target).is_file():
            problems.append(f"research/results/index.md: links to {target}, which does not exist")
    return problems, stale


def check_venues(root: Path) -> list:
    folder = root / "research" / "venues"
    if not folder.is_dir():
        return []
    problems, names = [], []
    for path in sorted(folder.glob("*.md")):
        if path.name in SKIP:
            continue
        where = f"research/venues/{path.name}"
        names.append(path.name)
        if not SLUG_NAME.match(path.stem):
            problems.append(f"{where}: name a venue note with lowercase ASCII letters, digits, and hyphens")
        fields = parse_fields(path.read_text(encoding="utf-8"), VENUE_LABELS)
        if not one(fields, "checked") or not DATE.search(one(fields, "checked") or ""):
            problems.append(f"{where}: the Checked line needs the date on which the official sources were read")
        if not URL.search(full_text(fields, "sources")):
            problems.append(f"{where}: the Sources line lists the official pages read, with their addresses")
    index = folder / "index.md"
    listed = {Path(t).name for t in link_targets(index.read_text(encoding="utf-8"))} if index.is_file() else set()
    for name in names:
        if name not in listed:
            problems.append(f"research/venues/index.md: {name} is not listed")
    return problems


def command_check(args, root: Path) -> int:
    problems = check_decisions(root) + check_feedback(root) + check_ideas(root)
    result_problems, stale = check_results(root)
    problems += result_problems + check_venues(root)
    for problem in problems:
        print(problem)
    for item in stale:
        print(f"stale: {item}")
    if problems:
        print(f"Research records: {len(problems)} problem(s)" + (f" and {len(stale)} stale result input(s) or output(s)." if stale else "."))
        return 1
    if stale:
        print(f"Research records have the required form, but {len(stale)} result input(s) or output(s) changed; run the work again or mark the result stale.")
        return 2
    print("Research records have the required form.")
    return 0


# The research code folder

CODE_README = (
    "Research code for this project: analyses, simulations, data processing, and figure generation. It is kept apart "
    "from [`scripts/`](../scripts/README.md), which holds workspace tools, so that research dependencies and workspace "
    "tools never break each other. The research environment, when one is needed, is `code/.venv/` (ignored by Git); "
    "the exact package versions are listed in `requirements.txt` here.\n\n"
    "Every analysis whose output may support a result is run through `python scripts/research.py run`, which records "
    "the command, the code version, the inputs, and the outputs in [`runs/`](runs/README.md) when that folder exists. "
    "Results and what they support are recorded in [`research/results/`](../research/results/README.md).")
OWNER = "scripts/research.py"
PARTS = {
    "src": ("Research Source Code", "the analysis code", "The code of the analyses, simulations, or data processing. The agent writes and maintains it on "
            "request; you can read or edit it. A run records a checksum of this code, so every result can be traced to the "
            "exact version that produced it."),
    "data": ("Research Data", "raw and derived data", "Data used by the research code. Inputs that must stay unchanged are in [`raw/`](raw/README.md); data "
             "that the code produces from them are in [`derived/`](derived/README.md). Whether data may be kept in version "
             "history is decided with you; large or sensitive data can stay outside the workspace and be referenced by path "
             "and checksum."),
    "runs": ("Research Runs", "the recorded runs", "One folder per recorded run of the research code: the exact command, the code checksum, the "
             "interpreter, the inputs and outputs with their checksums, the logs, the exit status, and, when asked for, the versions of the installed packages (`environment.txt`). Runs are written by "
             "`python scripts/research.py run` and are never edited; a new run gets a new folder."),
    "outputs": ("Research Outputs", "figures, tables, and other run outputs", "Figures, tables, and other files produced by recorded runs. A file here is a result only "
                "after its result record in `research/results/` says what it shows and how it was checked."),
    "notebooks": ("Research Notebooks", "exploratory notebooks", "Exploratory notebooks. A notebook result is not a recorded result until the analysis "
                  "is run through `python scripts/research.py run` and its result record is written."),
}
DATA_PARTS = {
    "raw": ("Raw Research Data", "Input data exactly as received or collected, never edited. Record where each file came from, "
            "its license or permission, and any sensitivity; derived versions go to [`../derived/`](../derived/README.md)."),
    "derived": ("Derived Research Data", "Data produced by the research code from the raw data. Everything here can be rebuilt "
                "by a recorded run; the run record in `code/runs/` names the inputs and the command."),
}


def command_code_init(args, root: Path) -> int:
    code = root / "code"
    parts = list(dict.fromkeys(args.part or []))
    created = []
    code.mkdir(exist_ok=True)
    present = [name for name in PARTS if (code / name).is_dir() or name in parts]
    listing = "\n".join(f"- [`{name}/`]({name}/README.md): {PARTS[name][1]}." for name in present)
    if update_readme(code / "README.md", "Research Code", CODE_README + ("\n\n## Contents\n\n" + listing if listing else ""), OWNER):
        created.append("code/README.md")
    for name in parts:
        title, _, body = PARTS[name]
        if update_readme(code / name / "README.md", title, body, OWNER):
            created.append(f"code/{name}/README.md")
        if name == "data":
            for sub, (sub_title, sub_body) in DATA_PARTS.items():
                if update_readme(code / "data" / sub / "README.md", sub_title, sub_body, OWNER):
                    created.append(f"code/data/{sub}/README.md")
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
    print("Created or updated: " + (", ".join(created) if created else "nothing; the folders already exist."))
    return 0


# Recorded runs

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


def executable_of(command: list, root: Path) -> str:
    """The program to start: a path is taken relative to the workspace root, a bare name is looked up on PATH."""
    first = command[0]
    if "/" in first or "\\" in first:
        candidate = resolve(root, first)
        return str(candidate) if candidate.exists() else first
    return shutil.which(first) or first


def interpreter(command: list, executable: str) -> dict:
    info = {"program": command[0], "resolved": executable}
    if "python" in Path(executable).name.lower():
        version = subprocess.run([executable, "--version"], capture_output=True, text=True)
        info["version"] = (version.stdout or version.stderr).strip()
    return info


def command_run(args, root: Path) -> int:
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        raise Refused("give the command after --, for example: -- code/.venv/bin/python code/src/analysis.py")
    name = slug(args.name, limit=40, fallback="run")
    missing = [value for value in args.input or [] if not resolve(root, value).exists()]
    if missing:
        raise Refused("these inputs do not exist: " + ", ".join(missing))
    code_paths = args.code or (["code/src"] if (root / "code" / "src").is_dir() else [])
    runs = root / "code" / "runs"
    if not runs.is_dir():
        update_readme(runs / "README.md", PARTS["runs"][0], PARTS["runs"][2], OWNER)
    run_id = f"{datetime.now(timezone.utc):%Y%m%d-%H%M%S}-{name}"
    number = 2
    while (runs / run_id).exists():
        run_id, number = f"{datetime.now(timezone.utc):%Y%m%d-%H%M%S}-{name}-{number}", number + 1
    folder = runs / run_id
    folder.mkdir(parents=True)
    executable = executable_of(command, root)
    record = {
        "schema": "paper-template.research-run/1", "run_id": run_id, "name": args.name, "note": args.note or "",
        "command": command, "working_directory": ".", "inputs": describe(args.input or [], root),
        "code": describe(code_paths, root), "git": git_state(root), "interpreter": interpreter(command, executable),
        "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine(),
                     "python_of_this_script": platform.python_version()},
        "started_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    if args.freeze and "version" in record["interpreter"]:
        frozen = subprocess.run([record["interpreter"]["resolved"], "-m", "pip", "freeze"], capture_output=True, text=True)
        write_text_atomic(folder / "environment.txt", frozen.stdout)
        record["environment"] = "environment.txt"
    began = time.monotonic()
    try:
        with open(folder / "stdout.txt", "w", encoding="utf-8", errors="replace") as out, \
                open(folder / "stderr.txt", "w", encoding="utf-8", errors="replace") as err:
            completed = subprocess.run([executable] + command[1:], cwd=root, stdout=out, stderr=err, timeout=args.timeout)
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
    versions = "; the versions of the installed packages are in `environment.txt`" if record.get("environment") else ""
    lines = [f"Recorded run of `{args.name}`" + (f": {args.note}" if args.note else "") + ". The record is "
             "[`run.json`](run.json); the program's output is in `stdout.txt` and `stderr.txt`" + versions + ". Runs are never edited; "
             "repeat the command below to reproduce it, and compare the checksums.",
             "", f"- Status: {record['status']}" + (f" ({record['error']})" if record.get("error") else ""),
             f"- Command: `{' '.join(command)}` (started in the workspace root)"]
    lines += [f"- Input: `{e['path']}`" + (f" sha256:{e['sha256']}" if e.get("sha256") else " (missing)") for e in record["inputs"]]
    lines += [f"- Output: `{e['path']}`" + (f" sha256:{e['sha256']}" if e.get("sha256") else " (missing)") for e in record["outputs"]]
    update_readme(folder / "README.md", f"Run {run_id}", "\n".join(lines), OWNER)
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
        print(f"{record['run_id']}: {record['status']}" + (f"; changed since the run: {', '.join(changed)}" if changed else ""))
    return 0


def main(argv: list | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Check research records and record research runs.")
    parser.add_argument("--root", type=Path, default=ROOT, help="workspace root (default: the parent of the scripts folder)")
    commands = parser.add_subparsers(dest="name_of_command", required=True)
    commands.add_parser("check", help="check the form of the research records and find stale results")
    init = commands.add_parser("code-init", help="create the research code folder with the parts that the research needs")
    init.add_argument("--part", action="append", choices=sorted(PARTS))
    init.add_argument("--venv", action="store_true", help="create the research environment code/.venv")
    init.add_argument("--python", help="interpreter for code/.venv (default: the one running this script)")
    run = commands.add_parser("run", help="run research code and record its provenance in code/runs/")
    run.add_argument("--name", required=True)
    run.add_argument("--input", action="append")
    run.add_argument("--output", action="append")
    run.add_argument("--code", action="append", help="code files or folders whose checksum identifies the code version (default: code/src)")
    run.add_argument("--note")
    run.add_argument("--freeze", action="store_true", help="also record the Python packages of the interpreter")
    run.add_argument("--timeout", type=float)
    run.add_argument("command", nargs=argparse.REMAINDER)
    commands.add_parser("runs", help="list recorded runs and whether their files changed since")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    handlers = {"check": command_check, "code-init": command_code_init, "run": command_run, "runs": command_runs}
    try:
        return handlers[args.name_of_command](args, root)
    except Refused as error:
        print(f"Refused: {error}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
