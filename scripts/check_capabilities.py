#!/usr/bin/env python3
"""Check that the "Available now" table in AGENTS.md matches the skills folder.

Every skill in .agents/skills/ must appear in the table. A row marked "Available now" must name
a skill or a script that exists. A row marked "Not available yet" must name no skill that exists.
This keeps the list of what works in one place, checked against the files.

Usage: python scripts/check_capabilities.py [WORKSPACE_ROOT]
Exit status: 0 when the table matches the folder, 1 otherwise. Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADING = "## Available now"
TICKED = re.compile(r"`([^`]+)`")
AVAILABLE = "Available now"
NOT_AVAILABLE = "Not available yet"


def table_rows(agents_text: str) -> list[list[str]]:
    """Return the body rows (capability, where, status) of the table under the heading."""
    lines = agents_text.splitlines()
    if HEADING not in lines:
        raise ValueError(f"no '{HEADING}' heading")
    rows = []
    for line in lines[lines.index(HEADING) + 1:]:
        if line.startswith("## "):
            break
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells[0] == "Capability" or set(cells[0]) <= set("-: "):
            continue
        rows.append(cells)
    if not rows:
        raise ValueError(f"the '{HEADING}' heading has no table rows")
    return rows


def check(root: Path) -> list[str]:
    problems: list[str] = []
    try:
        rows = table_rows((root / "AGENTS.md").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return [f"AGENTS.md: {error}"]

    skills_dir = root / ".agents" / "skills"
    skills = {p.name for p in skills_dir.iterdir() if p.is_dir()} if skills_dir.is_dir() else set()
    named_skills: set[str] = set()

    for cells in rows:
        if len(cells) != 3:
            problems.append(f"AGENTS.md: a table row has {len(cells)} cells, expected 3: {cells[0]!r}")
            continue
        capability, where, status = cells
        if not (status.startswith(AVAILABLE) or status == NOT_AVAILABLE):
            problems.append(f"AGENTS.md: {capability!r} has an unknown status {status!r}")
            continue
        available = status.startswith(AVAILABLE)
        names = TICKED.findall(where)
        if where == "—" or not names:
            if available:
                problems.append(f"AGENTS.md: {capability!r} is available but names no skill or script")
            continue
        if not available:
            for name in names:
                if name in skills:
                    problems.append(f"AGENTS.md: {capability!r} is not available yet, but skill {name!r} exists")
            continue
        for name in names:
            if "/" in name:
                if not (root / name).exists():
                    problems.append(f"AGENTS.md: {capability!r} names {name!r}, which does not exist")
            else:
                named_skills.add(name)
                if name not in skills:
                    problems.append(f"AGENTS.md: {capability!r} names skill {name!r}, which is not in .agents/skills/")

    for skill in sorted(skills - named_skills):
        problems.append(f"AGENTS.md: skill {skill!r} is not in the 'Available now' table")
    return problems


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Check the 'Available now' table in AGENTS.md against the skills folder.")
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
        print("Availability table check failed:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    print("Availability table matches the skills folder.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
