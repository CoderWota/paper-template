#!/usr/bin/env python3
"""Report where the research project stands, read from its records, without changing anything.

Reads the project requirements, the reference library and searches, evidence notes, ideas, the research plan, result
records, venue notes, the outline and manuscript, output profiles and builds, releases, review rounds, revisions,
research feedback, and the version history, and lists the gaps that suggest a next task. The paper-hands-on skill
uses it to recognize the stage of a project in a fresh session; the researcher's own account and state/current.md
take precedence over these signals.

Usage: python scripts/status.py [--json] [--root WORKSPACE]
Exit status: 0. Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import manuscript  # noqa: E402
import research  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NOT_INITIALIZED = re.compile(r"not (yet )?initialized|未初始化|初始化进行中|尚未完成|in progress", re.I)
OPEN_HEADING = re.compile(r"尚未确定|待定|未定|open items|open questions|not yet decided|undecided|to be decided", re.I)
OPEN_VALUE = re.compile(r"^\W*(待定|未定|尚未|未确定|暂无|无$|not yet|undecided|to be decided|tbd|none)", re.I)
VENUE_LABEL = r"(?:target venue|target journal|目标期刊|投稿目标)"


def initialized(text: str) -> bool:
    """The project's status line says initialized; an onboarding in progress or not started does not count."""
    found = re.search(r"(?im)^\s*(?:status|状态)\s*[:：]\s*(.+)$", text)
    if not found:
        return bool(text) and "not initialized" not in text.lower() and "尚未初始化" not in text
    value = found.group(1)
    return bool(re.search(r"initialized|已初始化|初始化完成", value, re.I)) and not NOT_INITIALIZED.search(value)


def target_venue(text: str) -> bool:
    """A venue label with a value, as in "- 目标期刊：<venue>" or a "## Target venue" heading followed by the venue.

    A bare label in a list of open items, or a value such as 待定 or "not yet decided", is not a recorded target.
    """
    lines = text.splitlines()
    open_section = False
    for number, line in enumerate(lines):
        if line.startswith("#"):
            open_section = bool(OPEN_HEADING.search(line))
            if re.search(VENUE_LABEL, line, re.I) and not open_section:
                following = next((l.strip() for l in lines[number + 1:] if l.strip()), "")
                if following and not following.startswith("#") and not OPEN_VALUE.search(following.lstrip("-* ")):
                    return True
            continue
        found = re.match(rf"^\s*(?:[-*]\s*)?(?:\*\*)?{VENUE_LABEL}(?:\*\*)?\s*[:：]\s*(\S.*)$", line, re.I)
        if found and not open_section and not OPEN_VALUE.search(found.group(1)):
            return True
    return False


def count(folder: Path, pattern: str, skip=("README.md", "index.md")) -> int:
    return sum(1 for p in folder.glob(pattern) if p.is_file() and p.name not in skip) if folder.is_dir() else 0


def statuses(folder: Path, words: dict) -> dict:
    found: dict = {}
    if not folder.is_dir():
        return found
    for path in folder.glob("*.md"):
        if path.name in ("README.md", "index.md"):
            continue
        fields = research.parse_fields(path.read_text(encoding="utf-8"), {"status": ("status", "状态")})
        state = research.status_of(research.one(fields, "status"), words) or "unknown"
        found[state] = found.get(state, 0) + 1
    return found


def facts(root: Path) -> dict:
    data: dict = {}
    project = root / "requirements" / "project.md"
    text = project.read_text(encoding="utf-8") if project.is_file() else ""
    data["initialized"] = initialized(text)
    data["target_venue_recorded"] = target_venue(text)
    references = root / "references"
    data["sources"] = sum(1 for p in (references / "originals").glob("src-*") if p.is_dir()) if (references / "originals").is_dir() else 0
    data["searches"] = sum(1 for p in (references / "searches").iterdir() if p.is_dir()) if (references / "searches").is_dir() else 0
    data["evidence_notes"] = count(references / "notes", "*.md")
    data["ideas"] = statuses(root / "ideas", research.IDEA_STATUS)
    data["plan"] = (root / "research" / "plan.md").is_file()
    data["results"] = statuses(root / "research" / "results", research.RESULT_STATUS)
    data["stale_results"] = len(research.check_results(root)[1])
    data["venues"] = count(root / "research" / "venues", "*.md")
    data["decisions"] = count(root / "research" / "decisions", "*.md")
    feedback = root / "research" / "feedback"
    open_items = 0
    for actions in feedback.glob("*/actions.md") if feedback.is_dir() else []:
        open_items += len(re.findall(r"(?im)^- (status|状态)\s*[:：]\s*(received|under discussion|已收到|讨论中)", actions.read_text(encoding="utf-8")))
    data["feedback_events"] = sum(1 for p in feedback.iterdir() if p.is_dir()) if feedback.is_dir() else 0
    data["feedback_open"] = open_items
    outline = root / "manuscript" / "outline.md"
    data["outline"] = outline.is_file() and "No outline yet" not in outline.read_text(encoding="utf-8")
    try:
        analysis = manuscript.analyse(root)
        data["manuscript"] = {"sections": len(analysis["paths"]), "words": analysis["words"], "cjk": analysis["cjk"],
                              "problems": len(analysis["problems"]), "open_items": len(analysis["open_items"])}
    except manuscript.Refused:
        data["manuscript"] = {"sections": 0, "words": 0, "cjk": 0, "problems": 0, "open_items": 0}
    checks = manuscript.load_checks(root)["checks"]
    stale = 0
    for entry in checks:
        if any(not (root / i["path"]).exists() or manuscript.checksum(root / i["path"]) != i["sha256"] for i in entry["inputs"]):
            stale += 1
    data["checks"] = {"recorded": len(checks), "stale": stale}
    profiles = root / "requirements" / "profiles"
    data["profiles"] = sorted(p.name for p in profiles.iterdir() if (p / "profile.yaml").is_file()) if profiles.is_dir() else []
    builds = {}
    for profile in data["profiles"]:
        record = root / "outputs" / "preview" / profile / "build.json"
        if record.is_file():
            build = json.loads(record.read_text(encoding="utf-8"))
            changed = [i for i in build["inputs"] if not (root / i["path"]).is_file() or manuscript.sha256_file(root / i["path"]) != i["sha256"]]
            builds[profile] = f"{build['status']}, " + ("out of date" if changed else "current")
    data["builds"] = builds
    releases = root / "outputs" / "releases"
    data["releases"] = sorted(p.name for p in releases.iterdir() if p.is_dir() and not p.name.startswith(".")) if releases.is_dir() else []
    rounds = []
    for folder in sorted((root / "reviews").glob("*/*")) if (root / "reviews").is_dir() else []:
        if folder.is_dir():
            response = folder / "response.md"
            entry = {"round": f"{folder.parent.name}/{folder.name}", "response": response.is_file(), "items": 0, "answered": 0}
            if response.is_file():
                text = response.read_text(encoding="utf-8")
                entry["items"] = len(re.findall(r"(?m)^## [RE]\d", text))
                entry["answered"] = len(re.findall(r"(?im)^- (status|状态)\s*[:：]\s*(addressed|declined|已处理|不采纳|未采纳)", text))
            rounds.append(entry)
    data["review_rounds"] = rounds
    revisions = []
    for folder in sorted((root / "revisions").iterdir()) if (root / "revisions").is_dir() else []:
        if (folder / "baseline.json").is_file():
            # The closing record (completed or abandoned) wins; else the application log; else the work is still open.
            closed, log = folder / "closed.json", folder / "apply.json"
            if closed.is_file():
                state = json.loads(closed.read_text(encoding="utf-8"))["outcome"]
            elif log.is_file():
                state = json.loads(log.read_text(encoding="utf-8"))["status"]
            else:
                state = "in progress"
            revisions.append(f"{folder.name}: {state}")
    data["revisions"] = revisions
    git = subprocess.run(["git", "-C", str(root), "status", "--porcelain"], capture_output=True, text=True) if (root / ".git").exists() else None
    data["unsaved_files"] = len(git.stdout.splitlines()) if git and git.returncode == 0 else None
    return data


def next_steps(data: dict) -> list:
    """Gaps that suggest a next task, in the usual order of a paper; the researcher decides."""
    steps = []
    manuscript_facts = data["manuscript"]
    if not data["initialized"]:
        steps.append("set up the project (project-onboarding)")
    if any(r.endswith("in progress") for r in data["revisions"]):
        steps.append("continue the open major revision (manuscript-revision)")
    if any(not r["response"] or r["answered"] < r["items"] for r in data["review_rounds"]):
        steps.append("answer the open review items (review-response)")
    if data["feedback_open"]:
        steps.append(f"decide on {data['feedback_open']} open feedback suggestion(s) (research-feedback)")
    if data["stale_results"]:
        steps.append("rerun the results whose inputs changed (research-code-setup or research-investigation)")
    if not data["sources"] and not data["searches"]:
        steps.append("find and import literature (literature-discovery, source-ingestion)")
    if not data["ideas"] and not data["plan"] and not manuscript_facts["sections"]:
        steps.append("develop research directions (research-ideation)")
    elif not data["plan"] and not manuscript_facts["sections"]:
        steps.append("plan the research (research-planning)")
    if data["plan"] and not data["results"] and not manuscript_facts["sections"]:
        steps.append("carry out the planned work and record results (research-code-setup, research-investigation)")
    if not data["venues"] and not data["target_venue_recorded"]:
        steps.append("compare possible venues (journal-selection)")
    if not data["outline"] and (data["results"] or data["plan"]):
        steps.append("outline the paper (manuscript-outline)")
    if data["outline"] and not manuscript_facts["sections"]:
        steps.append("draft the sections (manuscript-writing)")
    if manuscript_facts["problems"]:
        steps.append(f"fix {manuscript_facts['problems']} manuscript problem(s) (manuscript-writing)")
    if manuscript_facts["sections"] and (not data["checks"]["recorded"] or data["checks"]["stale"]):
        steps.append("audit the current manuscript (manuscript-audit)")
    if manuscript_facts["sections"] and not data["builds"]:
        steps.append("build a formatted preview (submission-assembly)")
    elif any("out of date" in b or b.startswith("failed") for b in data["builds"].values()):
        steps.append("rebuild the formatted output (submission-assembly)")
    if data["builds"] and manuscript_facts["sections"]:
        steps.append("assess readiness for the target venue (submission-readiness)")
    if data["unsaved_files"]:
        steps.append("save the current state as a version (git-save)")
    return steps


def main(argv: list | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Report where the research project stands.")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    data = facts(root)
    data["next_steps"] = next_steps(data)
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0
    m = data["manuscript"]
    lines = [
        f"Project set up: {'yes' if data['initialized'] else 'no'}; target venue recorded: {'yes' if data['target_venue_recorded'] else 'no'}.",
        f"Literature: {data['sources']} source(s) in the library, {data['searches']} search record(s), {data['evidence_notes']} evidence note(s).",
        f"Ideas: {data['ideas'] or 'none'}; research plan: {'yes' if data['plan'] else 'no'}; results: {data['results'] or 'none'}"
        + (f" ({data['stale_results']} stale input or output)" if data["stale_results"] else "") + ".",
        f"Venues examined: {data['venues']}; decisions recorded: {data['decisions']}; feedback events: {data['feedback_events']}"
        + (f" ({data['feedback_open']} open suggestion(s))" if data["feedback_open"] else "") + ".",
        f"Outline: {'yes' if data['outline'] else 'no'}; manuscript: {m['sections']} section file(s), {m['words']} words"
        + (f", {m['cjk']} CJK characters" if m["cjk"] else "") + f", {m['problems']} problem(s), {m['open_items']} open marker(s).",
        f"Checks recorded: {data['checks']['recorded']} ({data['checks']['stale']} stale); profiles: {', '.join(data['profiles']) or 'none'}; "
        f"builds: {', '.join(f'{k} {v}' for k, v in data['builds'].items()) or 'none'}; releases: {', '.join(data['releases']) or 'none'}.",
        "Review rounds: " + ("; ".join(f"{r['round']} ({r['answered']} of {r['items']} item(s) answered)" if r["response"]
                                       else f"{r['round']} (no response yet)" for r in data["review_rounds"]) or "none")
        + f"; revisions: {'; '.join(data['revisions']) or 'none'}.",
        f"Unsaved files in the version history: {data['unsaved_files'] if data['unsaved_files'] is not None else 'no version history'}.",
    ]
    print("\n".join(lines))
    if data["next_steps"]:
        print("Gaps that suggest a next task:")
        for step in data["next_steps"]:
            print(f"  - {step}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
