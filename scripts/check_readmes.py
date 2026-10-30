#!/usr/bin/env python3
"""Check that every project directory has a meaningful README.md.

Each designed directory, including nested and newly created ones, needs a
short, directory-specific English README. Runtime caches, environments, and
received or generated content are excluded.

Usage: python scripts/check_readmes.py [WORKSPACE_ROOT]
Exit status: 0 when every check passes, 1 when problems are found.
Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
from pathlib import Path

# Runtime, cache, environment, and editor directories are not project directories.
SKIPPED_NAMES = frozenset({
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".cache", ".tmp", ".tools", ".local", ".idea", ".vscode",
})

# These directories need their own README, but they hold received or generated
# material (originals, parser outputs, staged or frozen packages). Nothing is
# added inside them, so their subdirectories are not checked.
OPAQUE_PATTERNS = (
    ".claude/skills/*",  # generated copies; scripts/sync_skills.py --check covers their contents
    "inbox/imports/*",
    "references/originals/*",
    "references/extracted/*/native",
    "requirements/profiles/*/originals",
    "requirements/profiles/*/templates",
    "research/feedback/*/originals",
    "reviews/*/*/originals",
    "revisions/*/candidate",
    "revisions/*/baseline",
    "revisions/*/replaced",
    "code/data/raw",
    "code/data/derived",
    "code/outputs",
    "outputs/releases/*",
)

# In these areas only the listed children are designed directories. Other
# children are intake material awaiting organization or rebuildable previews.
DESIGNED_CHILDREN = {
    "inbox": frozenset({"imports"}),
    "outputs/preview": frozenset(),
}

MIN_WORDS = 20
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD|FIXME)\b|(?i:lorem ipsum)")


def is_opaque(rel: str) -> bool:
    return any(fnmatch.fnmatchcase(rel, pattern) for pattern in OPAQUE_PATTERNS)


def project_directories(root: Path):
    """Yield (relative POSIX path, path) for every directory that needs a README."""
    pending = [root]
    while pending:
        directory = pending.pop()
        rel = directory.relative_to(root).as_posix()
        if rel == ".":
            rel = ""
        yield rel, directory
        if rel and is_opaque(rel):
            continue
        designed = DESIGNED_CHILDREN.get(rel)
        for child in directory.iterdir():
            if not child.is_dir() or child.is_symlink():
                continue
            if child.name in SKIPPED_NAMES:
                continue
            if designed is not None and child.name not in designed:
                continue
            pending.append(child)


def has_readme(directory: Path) -> bool:
    # Compare names exactly: case-insensitive file systems would also accept readme.md.
    return any(entry.name == "README.md" and entry.is_file() for entry in directory.iterdir())


def readme_problems(text: str) -> list[str]:
    lines = text.splitlines()
    problems = []
    if not lines or not lines[0].startswith("# "):
        problems.append("does not start with a level-1 heading")
    words = len(re.findall(r"\w+", "\n".join(lines[1:])))
    if words < MIN_WORDS:
        problems.append(
            f"has {words} words after the heading; a useful description needs at least {MIN_WORDS}"
        )
    if PLACEHOLDER.search(re.sub(r"`[^`\n]*`", " ", text)):  # quoted syntax, such as a documented marker, is not a placeholder
        problems.append("contains a placeholder marker (TODO, TBD, FIXME, or lorem ipsum)")
    return problems


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")

    parser = argparse.ArgumentParser(
        description="Check that every project directory has a meaningful README.md."
    )
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="workspace root (default: the parent of the scripts directory)",
    )
    root = parser.parse_args(argv).root.resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    checked = 0
    missing: list[str] = []
    weak: list[str] = []
    texts: dict[str, list[str]] = {}
    for rel, directory in project_directories(root):
        checked += 1
        if not has_readme(directory):
            missing.append(f"{rel}/" if rel else "./")
            continue
        label = f"{rel}/README.md" if rel else "README.md"
        try:
            text = (directory / "README.md").read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            weak.append(f"{label} is not valid UTF-8 text")
            continue
        weak.extend(f"{label} {problem}" for problem in readme_problems(text))
        texts.setdefault(" ".join(text.split()).lower(), []).append(label)
    duplicates = sorted(sorted(labels) for labels in texts.values() if len(labels) > 1)

    if not (missing or weak or duplicates):
        print(f"README check passed: {checked} project directories.")
        return 0
    if missing:
        print("Directories without README.md:")
        for label in sorted(missing):
            print(f"  {label}")
    if weak:
        print("README.md files that do not yet describe their directory:")
        for line in sorted(weak):
            print(f"  {line}")
    if duplicates:
        print("Identical README.md files (write a description specific to each directory):")
        for labels in duplicates:
            print("  " + ", ".join(labels))
    print(f"README check failed ({checked} project directories checked).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
