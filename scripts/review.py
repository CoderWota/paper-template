#!/usr/bin/env python3
"""Report missing change targets and inconsistent completion claims, and reconcile a coauthor's Word edits.

`check` reports only concrete link and status inconsistencies. It does not require headings, IDs, labels, or a fixed
record form; unknown labels and statuses are left for the agent to interpret.

`reconcile` compares a Word file that a coauthor edited with the version they received (its tracked-change view, or
a separate file) and with the current manuscript. It lists each edited paragraph with its changed words, where the
paragraph is in manuscript/, and whether that manuscript paragraph also changed since the file was sent; it lists
Word comments with their authors. It never changes the manuscript.

Usage:
  python scripts/review.py check [--round reviews/<venue-id>/<round-id>]
  python scripts/review.py reconcile --docx FILE [--base FILE] [--to REPORT.md]
All commands take --root WORKSPACE. Exit status: 0 done (reported facts do not fail the command); 3 refused. Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import manuscript  # noqa: E402
from ingestion import reviews  # noqa: E402
from ingestion.common import write_text_atomic  # noqa: E402
from research import full_text, link_targets, one, parse_fields, sections, status_of  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
ITEM_LABELS = {"reviewer": ("reviewer", "审稿人"), "source": ("source", "出处", "来源"), "comment": ("comment", "意见", "评论"),
               "status": ("status", "状态"), "response": ("response", "回复"), "change": ("change", "改动", "修改")}
ITEM_STATUS = {"planned": ("planned", "计划中"), "partly addressed": ("partly addressed", "部分处理"), "addressed": ("addressed", "已处理"),
               "declined": ("declined", "不采纳", "未采纳"), "needs research": ("needs research", "需研究", "需要研究")}
CHANGE_LABELS = {"items": ("items", "对应意见"), "location": ("location", "位置"), "change": ("change", "改动", "修改"),
                 "status": ("status", "状态"), "revision": ("revision", "修订")}
CHANGE_STATUS = {"done": ("done", "已完成"), "planned": ("planned", "计划中")}


class Refused(Exception):
    pass


# Response records

def check_round(root: Path, folder: Path) -> list:
    """Report missing linked files and reviewer items marked complete before their change."""
    where = folder.relative_to(root).as_posix()
    response, changes = folder / "response.md", folder / "changes.md"
    if not response.is_file():
        return []
    problems = []
    change_fields = {}
    if changes.is_file():
        for heading, body in sections(changes.read_text(encoding="utf-8")):
            fields = parse_fields(body, CHANGE_LABELS)
            change_fields[heading] = fields
            match = re.match(r"^(C\d+)\b", heading)
            if match:
                change_fields[match.group(1)] = fields
            for target in link_targets(full_text(fields, "location")) + re.findall(r"`([^`]+\.md)`", full_text(fields, "location")):
                path = (folder / target) if not target.startswith(("manuscript/", "revisions/")) else root / target
                if not path.exists() and not (root / target).exists():
                    problems.append(f"{where}/changes.md {heading}: the linked location {target} does not exist")
                resolved = path.resolve()
                if target.startswith("../") and "reviews/" in resolved.as_posix() and folder.resolve() not in resolved.parents:
                    problems.append(f"{where}/changes.md {heading}: the location {target} points into another review round")
    for heading, body in sections(response.read_text(encoding="utf-8")):
        fields = parse_fields(body, ITEM_LABELS)
        status = status_of(one(fields, "status"), ITEM_STATUS)
        if status not in ("addressed", "partly addressed"):
            continue
        for change in dict.fromkeys(re.findall(r"\bC\d+\b", full_text(fields, "change"))):
            target = change_fields.get(change)
            if target is None:
                problems.append(f"{where}/response.md {heading}: the referenced change {change} is not in changes.md")
                continue
            target_status = status_of(one(target, "status"), CHANGE_STATUS)
            if target_status == "planned":
                problems.append(f"{where}/response.md {heading}: marked {status}, but change {change} is still planned")
    return problems


def command_check(args, root: Path) -> int:
    if args.round:
        folders = [root / args.round]
        if not folders[0].is_dir():
            raise Refused(f"{args.round} does not exist")
    else:
        folders = sorted(p for p in (root / "reviews").glob("*/*") if p.is_dir()) if (root / "reviews").is_dir() else []
    problems = []
    for folder in folders:
        problems += check_round(root, folder)
    for problem in problems:
        print(problem)
    print(f"Checked the response records of {len(folders)} round(s): " + ("no linked-target issues found." if not problems else f"{len(problems)} fact(s) reported."))
    return 0


# Reconciling a coauthor's Word file

def paragraphs(path: Path) -> list:
    """(original text, edited text) per body paragraph: the version before and after the tracked changes."""
    try:
        package = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        raise Refused(f"{path.name} is not a readable Word file") from None
    with package:
        root = ET.fromstring(package.read("word/document.xml"))
    result = []
    body = root.find(W + "body")
    for paragraph in body.iter(W + "p") if body is not None else []:
        original, edited = [], []

        def walk(node, inserted=False, deleted=False):
            for child in node:
                tag = child.tag
                if tag == W + "ins":
                    walk(child, True, deleted)
                elif tag == W + "del":
                    walk(child, inserted, True)
                elif tag in (W + "t", M + "t"):
                    if not deleted:
                        edited.append(child.text or "")
                    if not inserted:
                        original.append(child.text or "")
                elif tag == W + "delText":
                    if not inserted:
                        original.append(child.text or "")
                elif tag == W + "tab":
                    if not deleted:
                        edited.append(" ")
                    if not inserted:
                        original.append(" ")
                else:
                    walk(child, inserted, deleted)

        walk(paragraph)
        result.append(("".join(original).strip(), "".join(edited).strip()))
    return [pair for pair in result if pair[0] or pair[1]]


def plain(markdown_text: str) -> str:
    text = re.sub(r"`([^`]*)`", r"\1", markdown_text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)(\{[^}]*\})?", r"\1", text)
    text = re.sub(r"\[-?@[^\]]+\]|-?@[\w:.#$%&+?<>~/-]+", " ", text)
    text = re.sub(r"\{#[^}]+\}", " ", text)
    text = re.sub(r"[*_#>|]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def manuscript_paragraphs(root: Path) -> list:
    """(location, plain text) for each paragraph of the listed section files."""
    manifest = manuscript.read_manifest(root)
    paths, _ = manuscript.section_paths(root, manifest)
    found = []
    for name, path in paths:
        for kind, _, lines, start in manuscript.blocks_of(path.read_text(encoding="utf-8")):
            if kind in ("para", "heading"):
                text = plain(" ".join(lines))
                if text:
                    found.append((f"manuscript/{name}:{start}", text))
    return found


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\([^)]*\d{4}[^)]*\)", " ", text)).strip().lower()


def best_match(text: str, candidates: list) -> tuple:
    target = normalized(text)
    best = (None, 0.0, "")
    for location, candidate in candidates:
        ratio = difflib.SequenceMatcher(None, target, normalized(candidate), autojunk=False).ratio()
        if ratio > best[1]:
            best = (location, ratio, candidate)
    return best


def word_diff(before: str, after: str) -> str:
    out = []
    for token in difflib.ndiff(before.split(), after.split()):
        if token.startswith("- "):
            out.append(f"[-{token[2:]}-]")
        elif token.startswith("+ "):
            out.append(f"{{+{token[2:]}+}}")
        elif token.startswith("  "):
            out.append(token[2:])
    return " ".join(out)


def command_reconcile(args, root: Path) -> int:
    edited_file = Path(args.docx).expanduser()
    if not edited_file.is_file():
        raise Refused(f"{args.docx} does not exist")
    pairs = paragraphs(edited_file)
    if args.base:
        base_file = Path(args.base).expanduser()
        if not base_file.is_file():
            raise Refused(f"{args.base} does not exist")
        base = [edited for _, edited in paragraphs(base_file)]
        theirs = [edited for _, edited in pairs]
        changes = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, base, theirs, autojunk=False).get_opcodes():
            if tag == "equal":
                continue
            before, after = " ".join(base[i1:i2]), " ".join(theirs[j1:j2])
            changes.append((before, after))
    else:
        changes = [(original, edited) for original, edited in pairs if original != edited]
    current = manuscript_paragraphs(root)
    structures = reviews.docx_structures(edited_file)
    lines = [f"# Reconciliation of {edited_file.name}", "",
             f"Compared with {'`' + Path(args.base).name + '`' if args.base else 'the version before its tracked changes'} and with the "
             "current manuscript. Nothing was applied; each change needs the researcher's decision.", ""]
    clean = conflicts = unlocated = 0
    for number, (before, after) in enumerate(changes, start=1):
        location, ratio, current_text = best_match(before or after, current)
        if before and location and ratio >= 0.6:
            unchanged = difflib.SequenceMatcher(None, normalized(before), normalized(current_text), autojunk=False).ratio() >= 0.97
            state = "applies cleanly: the manuscript paragraph is unchanged since the file was sent" if unchanged else \
                "conflict: the manuscript paragraph also changed since the file was sent"
            clean, conflicts = clean + unchanged, conflicts + (not unchanged)
        else:
            state = "new paragraph" if not before else "not located in the current manuscript"
            unlocated += 1
            location = location if not before and location and ratio >= 0.6 else None
        lines += [f"## Change {number}", "", f"- Location: {location or 'unknown'}" + (f" (match {ratio:.0%})" if location else ""),
                  f"- State: {state}", f"- Words: {word_diff(before, after)}", ""]
    comments = structures.get("comments", []) if isinstance(structures, dict) else []
    if comments:
        lines += ["## Comments", ""]
        for comment in comments:
            reply = f", a reply to comment {comment['reply_to']}" if comment.get("reply_to") else ""
            anchor = f" on “{comment['anchor']}”" if comment.get("anchor") else ""
            lines.append(f"- Comment {comment['number']} ({comment['author'] or 'author not stated'}{reply}){anchor}: “{comment['text']}”")
        lines.append("")
    report = "\n".join(lines) + "\n"
    if args.to:
        target = Path(args.to)
        write_text_atomic(target if target.is_absolute() else root / target, report)
    else:
        print(report)
    print(f"{len(changes)} edited paragraph(s): {clean} apply cleanly, {conflicts} conflict with later manuscript changes, "
          f"{unlocated} not located; {len(comments)} comment(s). Nothing was applied.")
    return 0


def main(argv: list | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Check response records and reconcile coauthor Word edits.")
    parser.add_argument("--root", type=Path, default=ROOT, help="workspace root (default: the parent of the scripts folder)")
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="check the response and change records of review rounds")
    check.add_argument("--round")
    reconcile = commands.add_parser("reconcile", help="compare a coauthor's edited Word file with the version sent and the manuscript")
    reconcile.add_argument("--docx", required=True)
    reconcile.add_argument("--base")
    reconcile.add_argument("--to")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        return {"check": command_check, "reconcile": command_reconcile}[args.command](args, root)
    except (Refused, manuscript.Refused) as error:
        print(f"Refused: {error}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
