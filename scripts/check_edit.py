#!/usr/bin/env python3
"""Compare a revised text with its original and report what a prose edit must keep.

A translation, a polish, a shortening, or a revision for natural prose may change the wording, but it must keep
the items that the workspace conventions protect: the YAML front matter, code, math, labels, citation keys and
cross-references, image and link targets, footnote references, open markers such as [TODO: ...], headings, and
numbers. This script lists every protected item that disappeared or appeared. For an edit within one language it
also counts hedges, negations, and limiting words (scope and conditions) from check_edit.json: a changed count
is a warning that needs a reading, because these words carry the strength and conditions of a claim.

Usage:
  python scripts/check_edit.py ORIGINAL REVISED [--translation]
With --translation the revised text is in another language: open markers and headings are compared by count and
level only, and no words are counted.
Exit status: 0 when every protected item is kept, 1 when protected items differ, 2 for a usage error.
Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from text_rules import citation_keys, detection_text, normalize_reference, open_marker  # noqa: E402

VOCABULARY = json.loads(Path(__file__).with_name("check_edit.json").read_text(encoding="utf-8"))
CROSSREF = ("fig", "tbl", "eq", "sec", "lst")

KANA = re.compile(r"[\u3040-\u30ff]")
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
HANGUL = re.compile(r"[\uac00-\ud7af]")
LATIN = re.compile(r"[A-Za-z]")
EAST_ASIAN = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uac00-\ud7af]")

FRONT_MATTER = re.compile(r"\A---[ \t]*\n.*?\n(?:---|\.\.\.)[ \t]*(?:\n|\Z)", re.S)
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")
FENCE_CLOSE = re.compile(r"^ {0,3}(`{3,}|~{3,})[ \t]*$")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
DISPLAY_MATH = re.compile(r"\$\$(.+?)\$\$", re.S)
INLINE_MATH = re.compile(r"(?<![\\$])\$(?!\s)([^$\n]+?)(?<![\s\\])\$(?!\d)")
IMAGE = re.compile(r"(!\[[^\]]*\]\()\s*<?([^)\s>]+)>?([^)]*\))")
LINK = re.compile(r"(?<!!)(\[[^\]]*\]\()\s*<?([^)\s>]+)>?([^)]*\))")
URL = re.compile(r"https?://[^\s<>()\[\]\"']+")
LABEL = re.compile(r"\{#((?:fig|tbl|eq|sec|lst):[^\s{}]+)[^{}]*\}")
ATTRIBUTES = re.compile(r"\s*\{[^{}]*\}\s*$")
FOOTNOTE = re.compile(r"\[\^([^\]\s]+)\]")
HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$", re.M)
LIST_MARKER = re.compile(r"^[ \t]*\d+[.)][ \t]", re.M)
BRACKETED = re.compile(r"\[[^\[\]\n]*\]|\u3010[^\u3010\u3011\n]*\u3011|\uff08[^\uff08\uff09\n]*\uff09|\([^()\n]*\)")
THOUSANDS = re.compile(r"(?<=\d),(?=\d{3}(?!\d))")
PERCENT = re.compile(r"(?<=\d)[ \t\u00a0\u202f]+%")
NUMBER = re.compile(r"\d+(?:\.\d+)*%?")


def language_of(text: str) -> str:
    """Name the word list that fits the text: ja, zh, ko, en, or none."""
    if KANA.search(text):
        return "ja"
    if HAN.search(text):
        return "zh"
    if HANGUL.search(text):
        return "ko"
    return "en" if LATIN.search(text) else "none"


def split_code(text: str) -> tuple[str, list[str]]:
    """Return the text without fenced code blocks, and the blocks themselves."""
    prose: list[str] = []
    blocks: list[str] = []
    current: list[str] | None = None
    fence = ""
    for line in text.splitlines(keepends=True):
        if current is None:
            opening = FENCE_OPEN.match(line)
            if opening:
                current, fence = [line], opening.group(1)
            else:
                prose.append(line)
            continue
        current.append(line)
        closing = FENCE_CLOSE.match(line.rstrip("\r\n"))
        if closing and closing.group(1)[0] == fence[0] and len(closing.group(1)) >= len(fence):
            blocks.append("".join(current))
            prose.append("\n")
            current = None
    if current is not None:
        blocks.append("".join(current))
    return "".join(prose), blocks


def extract(text: str) -> dict:
    """Collect the protected items of a text and the prose left after masking them."""
    text = text.replace("\r\n", "\n")
    items: dict = {}
    front = FRONT_MATTER.match(text)
    items["front matter"] = [front.group(0).strip()] if front else []
    body = text[front.end():] if front else text
    body, items["code blocks"] = split_code(body)
    items["inline code"] = INLINE_CODE.findall(body)
    body = INLINE_CODE.sub(" ", body)
    items["math"] = ["".join(m.split()) for m in DISPLAY_MATH.findall(body)]
    body = DISPLAY_MATH.sub(" ", body)
    items["math"] += ["".join(m.split()) for m in INLINE_MATH.findall(body)]
    body = INLINE_MATH.sub(" ", body)
    items["image targets"] = [m.group(2) for m in IMAGE.finditer(body)]
    body = IMAGE.sub(lambda m: m.group(1) + " )", body)
    items["link targets"] = [m.group(2) for m in LINK.finditer(body)]
    body = LINK.sub(lambda m: m.group(1) + " )", body)
    items["link targets"] += [u.rstrip(".,;:!?") for u in URL.findall(body)]
    body = URL.sub(" ", body)
    items["labels"] = LABEL.findall(body)
    body = LABEL.sub(" ", body)
    items["footnotes"] = FOOTNOTE.findall(body)
    body = FOOTNOTE.sub(" ", body)
    citations, references = [], []
    for raw in citation_keys(body):
        key = normalize_reference(EAST_ASIAN.split(raw, 1)[0], set())
        if not key:
            continue
        prefix = key.split(":", 1)[0]
        (references if ":" in key and prefix in CROSSREF else citations).append(key)
    items["citation keys"], items["cross-references"] = citations, references
    for key in sorted(set(citations + references), key=len, reverse=True):
        body = body.replace("@" + key, " ")
    headings = [(len(level), ATTRIBUTES.sub("", title).strip()) for level, title in HEADING.findall(body)]
    items["headings"] = [f"{'#' * level} {title}" for level, title in headings]
    items["heading levels"] = ["#" * level for level, _ in headings]
    items["open markers"] = [span for span in BRACKETED.findall(body) if open_marker(span)]
    numbers_text = PERCENT.sub("%", THOUSANDS.sub("", detection_text(LIST_MARKER.sub(" ", body))))
    items["numbers"] = NUMBER.findall(numbers_text)
    items["_prose"] = body
    return items


def count_words(prose: str, language: str) -> dict[str, Counter]:
    """Count the hedges, negations, and limiting words of one language in the prose."""
    lists = VOCABULARY.get(language)
    if not lists:
        return {}
    text = detection_text(prose).replace("\u2019", "'")
    counts: dict[str, Counter] = {}
    for category, entry in lists.items():
        if category.startswith("_"):
            continue
        counter: Counter = Counter()
        for word in entry["words"]:
            if word == "n't":
                found = text.lower().count(word)
            elif language == "en":
                found = len(re.findall(r"(?<![A-Za-z'])" + re.escape(word) + r"(?![A-Za-z])", text, re.I))
            else:
                found = text.count(word) - sum(text.count(longer) for longer in entry["except"] if word in longer)
            if found:
                counter[word] = found
        counts[category] = counter
    return counts


COMPARED = ("front matter", "code blocks", "inline code", "math", "labels", "citation keys", "cross-references",
            "image targets", "link targets", "footnotes", "open markers", "headings", "numbers")
COUNTED_IN_TRANSLATION = {"open markers", "headings"}


def line_of(text: str, item: str) -> str:
    for number, line in enumerate(text.splitlines(), 1):
        if item in line:
            return f" (line {number})"
    return ""


def compare(original_text: str, revised_text: str, translation: bool) -> tuple[list[str], list[str], list[str]]:
    """Return the report lines for protected items, the word-count warnings, and notes."""
    before, after = extract(original_text), extract(revised_text)
    report, warnings, notes = [], [], []
    for category in COMPARED:
        if translation and category in COUNTED_IN_TRANSLATION:
            key = "heading levels" if category == "headings" else category
            old, new = len(before[key]), len(after[key])
            if category == "headings" and before[key] != after[key]:
                report.append(f"  {category}: levels changed from {' '.join(before[key]) or 'none'} to {' '.join(after[key]) or 'none'}")
            elif old != new:
                report.append(f"  {category}: {old} in the original, {new} in the revision")
            continue
        missing = Counter(before[category]) - Counter(after[category])
        added = Counter(after[category]) - Counter(before[category])
        if not missing and not added:
            continue
        parts = []
        if missing:
            parts.append("missing " + "; ".join(f"{item}{line_of(original_text, item)}" for item in missing.elements()))
        if added:
            parts.append("added " + "; ".join(f"{item}{line_of(revised_text, item)}" for item in added.elements()))
        report.append(f"  {category}: " + ", ".join(parts))
    language = language_of(before["_prose"])
    if not translation:
        revised_language = language_of(after["_prose"])
        if revised_language != language and "none" not in (language, revised_language):
            notes.append(f"The original reads as {language} and the revision as {revised_language}; for a translation, run again with --translation.")
        else:
            old_counts, new_counts = count_words(before["_prose"], language), count_words(after["_prose"], language)
            if not old_counts:
                notes.append(f"No list of hedges, negations, or limiting words exists for this language ({language}); read the changed sentences for them.")
            for category, old in old_counts.items():
                new = new_counts.get(category, Counter())
                changed = [f'"{word}" {old[word]} -> {new[word]}' for word in sorted(set(old) | set(new)) if old[word] != new[word]]
                if changed:
                    warnings.append(f"  {category}: " + ", ".join(changed))
    return report, warnings, notes


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Compare a revised text with its original and report what a prose edit must keep.")
    parser.add_argument("original", type=Path, help="the text before the edit")
    parser.add_argument("revised", type=Path, help="the text after the edit")
    parser.add_argument("--translation", action="store_true", help="the revision is a translation into another language")
    args = parser.parse_args(argv)
    texts = []
    for path in (args.original, args.revised):
        try:
            texts.append(path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeDecodeError) as error:
            print(f"Cannot read {path}: {error}")
            return 1
    report, warnings, notes = compare(texts[0], texts[1], args.translation)
    print(f"Compared {args.original} with {args.revised}{' as a translation' if args.translation else ''}.")
    if report:
        print("Protected items that differ:")
        print("\n".join(report))
    else:
        print("Protected items: all kept.")
    if warnings:
        print("Hedges, negations, and limiting words whose count changed (read these sentences; the claim may have changed):")
        print("\n".join(warnings))
    for note in notes:
        print(note)
    print(f"Result: {len(report)} protected difference(s) and {len(warnings)} wording warning(s) reported.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
