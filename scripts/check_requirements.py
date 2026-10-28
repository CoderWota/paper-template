#!/usr/bin/env python3
"""Check the form of the writing rules in requirements/writing.md.

Every rule is a "##" section with Rule, Scope, and Confirmed lines. The Confirmed line must quote
the researcher's words, so that a rule can be traced to what they said. Examples and Exceptions
lines are allowed only with a quotation, so that none can be invented. Other requirement files are
free text and are not checked here.

Usage: python scripts/check_requirements.py [WORKSPACE_ROOT]
Exit status: 0 when every rule has the required form, 1 otherwise. Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED = {"rule": ("规则", "Rule"), "scope": ("适用范围", "Scope"), "confirmed": ("确认", "Confirmed")}
OPTIONAL_WITH_QUOTE = {"examples": ("示例", "Examples"), "exceptions": ("例外", "Exceptions")}
LINE = re.compile(r"^- (.+?)[:：]\s*(.*)$")
QUOTE = re.compile(r"[\"“「][^\"”」]{2,}[\"”」]")


def sections(text: str) -> list[tuple[str, list[str]]]:
    """Return (heading, bullet lines) for each "##" section."""
    result: list[tuple[str, list[str]]] = []
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        heading, _, body = block.partition("\n")
        result.append((heading.strip(), [line for line in body.splitlines() if line.startswith("- ")]))
    return result


def values(bullets: list[str]) -> dict[str, list[str]]:
    """Map each recognized label to the values found for it."""
    found: dict[str, list[str]] = {}
    for line in bullets:
        match = LINE.match(line)
        if not match:
            continue
        label, value = match.group(1).strip(), match.group(2)
        for key, names in {**REQUIRED, **OPTIONAL_WITH_QUOTE}.items():
            if label in names:
                found.setdefault(key, []).append(value)
    return found


def check(root: Path) -> list[str]:
    path = root / "requirements" / "writing.md"
    if not path.is_file():
        return ["requirements/writing.md does not exist"]
    problems: list[str] = []
    for heading, bullets in sections(path.read_text(encoding="utf-8")):
        found = values(bullets)
        for key, names in REQUIRED.items():
            count = len(found.get(key, []))
            if count != 1:
                problems.append(f"rule {heading!r}: expected one {names[1]} line (accepted labels: {', '.join(names)}), found {count}")
        for value in found.get("confirmed", []):
            if not QUOTE.search(value):
                problems.append(f"rule {heading!r}: the Confirmed line must quote the researcher's words")
        for key, names in OPTIONAL_WITH_QUOTE.items():
            for value in found.get(key, []):
                if not QUOTE.search(value):
                    problems.append(f"rule {heading!r}: the {names[1]} line needs a quotation from the researcher")
    return problems


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Check the form of the writing rules in requirements/writing.md.")
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="workspace root (default: the parent of the scripts directory)",
    )
    root = parser.parse_args(argv).root.resolve()
    problems = check(root)
    if problems:
        print("Writing rule check failed:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print("Writing rules have the required form.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
