#!/usr/bin/env python3
"""Check, assemble, and revise the manuscript with the workspace's Markdown conventions.

The manuscript is the files that manuscript/manifest.yaml lists, in that order, with optional Pandoc metadata
(title, authors, abstract, keywords) in manuscript/metadata.yaml, or in the file that the manifest's `metadata` key
names. `check` applies the conventions in
docs/markdown-and-export-conventions.md: math delimiters, equation labels, figure, table, equation, and section
labels and the references to them, citation keys against references/bibliography.bib, image links, hand-numbered
references, and open markers. `assemble` joins the listed files for a preview. Check records in outputs/checks/
remember which inputs a check examined, so that a changed input makes the result stale. Major revisions keep a
baseline snapshot in revisions/<revision-id>/baseline/, apply a staged candidate with a resumable log, and end with a
closing record (closed.json) when the revision is completed, in place or after the candidate, or abandoned.

Usage:
  python scripts/manuscript.py check
  python scripts/manuscript.py set-sections FILE ...
  python scripts/manuscript.py assemble [--to PATH]
  python scripts/manuscript.py record-check --name NAME --kind audit|evidence|format|readiness|other --input PATH ...
      --result passed|findings|failed --summary TEXT [--scope TEXT] [--report PATH]
  python scripts/manuscript.py checks
  python scripts/manuscript.py adopt --import-id ID [--document NAME] [--into manuscript|candidate --revision-id ID]
  python scripts/manuscript.py revision-start --id ID [--include PATH ...]
  python scripts/manuscript.py revision-status --id ID
  python scripts/manuscript.py revision-apply --id ID [--reconciled PATH ...] [--resume]
  python scripts/manuscript.py revision-complete --id ID [--note TEXT]
  python scripts/manuscript.py revision-restore --id ID
All commands take --root WORKSPACE. Exit status: 0 done; 1 problems found or an application stopped; 2 the
records are valid but some are stale; 3 refused. Uses only the Python standard library.
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

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ingestion.common import checksum, sha256_file, slug, update_readme, write_json_atomic, write_text_atomic  # noqa: E402
from text_rules import (CJK, WORD, citation_keys, doubled_reference, hand_numbered, normalize_reference, open_marker,
                        signature_problems)  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OWNER = "scripts/manuscript.py"
NOT_SECTIONS = {"README.md", "outline.md", "manifest.yaml"}
CROSSREF = ("fig", "tbl", "eq", "sec", "lst")
FENCE = re.compile(r"^(\s{0,3})(`{3,}|~{3,})\s*([^\s`{]*)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
ATTRIBUTES = re.compile(r"\s*\{([^{}]*)\}\s*$")
IMAGE = re.compile(r"!\[([^\]]*)\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)(\{[^}]*\})?")
CAPTION = re.compile(r"^(?::|Table:)\s+(.*?)\s*(\{([^{}]*)\})?\s*$")
EQ_LABEL = re.compile(r"^\{#(eq:[^\s{}]+)\}$")
INLINE_CODE = re.compile(r"`+[^`]*`+")
INLINE_MATH = re.compile(r"(?<![\\$])\$(?!\s)([^$\n]+?)(?<![\s\\])\$(?!\d)")
CURRENCY = re.compile(r"(?<![\\$])\$\d")


class Refused(Exception):
    pass


# The manifest

def read_manifest(root: Path) -> dict:
    path = root / "manuscript" / "manifest.yaml"
    if not path.is_file():
        raise Refused("manuscript/manifest.yaml is missing")
    data: dict = {"sections": []}
    current = None
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = re.sub(r"\s+#.*$", "", raw) if not raw.lstrip().startswith("#") else ""
        if not line.strip():
            continue
        if line[0] not in " -" and ":" in line:
            key, _, value = line.partition(":")
            key, value = key.strip(), value.strip()
            current = key
            if key == "sections":
                if value not in ("", "[]"):
                    data["sections"] = [unquote(v) for v in value.strip("[]").split(",") if v.strip()]
            else:
                data[key] = unquote(value)
        elif line.lstrip().startswith("- ") and current == "sections":
            data["sections"].append(unquote(line.lstrip()[2:]))
        else:
            raise Refused(f"manuscript/manifest.yaml line {number} cannot be read: {raw.strip()!r}")
    return data


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


METADATA = "metadata.yaml"


def metadata_name(root: Path, manifest: dict) -> str | None:
    """The Pandoc metadata file (title, authors, abstract, keywords): the file the manifest names, else manuscript/metadata.yaml."""
    named = manifest.get("metadata")
    if named:
        return named
    return METADATA if (root / "manuscript" / METADATA).is_file() else None


def command_set_sections(args, root: Path) -> int:
    path = root / "manuscript" / "manifest.yaml"
    old = path.read_text(encoding="utf-8") if path.is_file() else ""
    header = [line for line in old.splitlines() if line.startswith("#")] or [
        "# Manuscript assembly manifest, maintained by the agent.",
        "# Lists the section files (paths relative to this directory) in reading order.",
        "# Only listed files are assembled; README.md, outline.md, notes, and drafts never are."]
    data = read_manifest(root) if path.is_file() else {"version": "1", "sections": []}
    for name in args.files:
        if name in NOT_SECTIONS or not name.endswith(".md") or name.startswith(("/", "..")):
            raise Refused(f"{name} cannot be a manuscript section")
        if not (root / "manuscript" / name).is_file():
            raise Refused(f"manuscript/{name} does not exist")
    lines = header + [f"version: {data.get('version', '1')}"]
    for key, value in data.items():
        if key not in ("version", "sections"):
            lines.append(f"{key}: {value}")
    lines.append("sections:" + ("" if args.files else " []"))
    lines += [f"  - {name}" for name in args.files]
    write_text_atomic(path, "\n".join(lines) + "\n")
    print(f"The manuscript now consists of {len(args.files)} section file(s): " + ", ".join(args.files))
    return 0


# Scanning the Markdown

def blocks_of(text: str) -> list:
    """Split Markdown into blocks: ("fence", lang, lines, start), ("math", None, lines, start), ("para", None, lines, start)."""
    lines, blocks, index = text.splitlines(), [], 0
    while index < len(lines):
        line = lines[index]
        fence = FENCE.match(line)
        if fence:
            marker, start = fence.group(2), index
            index += 1
            while index < len(lines) and not lines[index].strip().startswith(marker[0] * len(marker)):
                index += 1
            blocks.append(("fence", fence.group(3).lower(), lines[start:index + 1], start + 1))
            index += 1
        elif line.strip().startswith("$$") and not (line.strip().endswith("$$") and len(line.strip()) > 4):
            start = index
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("$$"):
                index += 1
            blocks.append(("math", None, lines[start:index + 1], start + 1))
            index += 1
        elif not line.strip():
            index += 1
        elif HEADING.match(line):
            blocks.append(("heading", None, [line], index + 1))
            index += 1
        else:
            start = index
            while index < len(lines) and lines[index].strip() and not FENCE.match(lines[index]) \
                    and not lines[index].strip().startswith("$$") and not HEADING.match(lines[index]):
                index += 1
            blocks.append(("para", None, lines[start:index], start + 1))
    return blocks


def auto_identifier(text: str) -> str:
    """Pandoc's automatic heading identifier, for the common cases."""
    text = re.sub(r"\[\^[^\]]*\]", "", text)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*`]", "", text).lower()
    kept = "".join(ch if ch.isalnum() or ch in "_-." else "-" if ch.isspace() else "" for ch in text)
    first = re.search(r"[^\W\d_]", kept)
    return kept[first.start():] if first else ""


def prose(line: str) -> str:
    return INLINE_MATH.sub(" ", INLINE_CODE.sub(" ", line))


def count_words(text: str) -> tuple:
    words = cjk = 0
    for kind, _, lines, _ in blocks_of(text):
        if kind not in ("para", "heading"):
            continue
        for line in lines:
            line = re.sub(r"<!--.*?-->", " ", prose(IMAGE.sub(lambda m: m.group(1), line)))
            cjk += len(CJK.findall(line))
            words += len(WORD.findall(CJK.sub(" ", line)))
    return words, cjk


class Scan:
    def __init__(self) -> None:
        self.labels: dict = {}
        self.references: list = []
        self.citations: list = []
        self.citation_occurrences: list = []
        self.problems: list = []
        self.warnings: list = []
        self.open_items: list = []
        self.used_ids: dict = {}
        self.mermaid = 0

    def define(self, label: str, where: str) -> None:
        if label in self.labels:
            self.problems.append(f"{where}: the label {label} is also defined at {self.labels[label]}")
        else:
            self.labels[label] = where

    def heading_id(self, text: str) -> str:
        base = auto_identifier(text) or "section"
        count = self.used_ids.get(base, 0)
        self.used_ids[base] = count + 1
        return base if count == 0 else f"{base}-{count}"


def scan_file(path: Path, display: str, scan: Scan, folder: Path) -> None:
    text = path.read_text(encoding="utf-8")
    scan.problems.extend(signature_problems(text, display))
    blocks = blocks_of(text)
    for position, (kind, lang, lines, start) in enumerate(blocks):
        where = f"{display}:{start}"
        following = blocks[position + 1] if position + 1 < len(blocks) else None
        if kind == "fence":
            if lang == "mermaid":
                scan.mermaid += 1
                if following and following[0] == "para":
                    caption = CAPTION.match(following[2][0])
                    if caption and caption.group(3) and "#fig:" in caption.group(3):
                        scan.define(re.search(r"#(fig:[^\s}]+)", caption.group(3)).group(1), f"{display}:{following[3]}")
            if not lines[-1].strip().startswith(("```", "~~~")) or len(lines) < 2:
                scan.problems.append(f"{where}: a code block is not closed")
            continue
        if kind == "math":
            body = "\n".join(lines)
            closing = lines[-1].strip() if len(lines) > 1 else ""
            if len(lines) < 2 or not closing.startswith("$$"):
                scan.problems.append(f"{where}: a display formula is not closed with $$")
            elif closing != "$$":
                if "{#eq:" in closing:
                    scan.problems.append(f"{where}: the label is on the closing $$ line, which stops GitHub from showing the formula; "
                                         "put {#eq:...} in its own paragraph after a blank line")
                else:
                    scan.warnings.append(f"{where}: put the closing $$ on its own line")
            if lines[0].strip() != "$$":
                scan.warnings.append(f"{where}: put the opening $$ on its own line")
            if "\\label{" in body or "\\tag{" in body:
                scan.problems.append(f"{where}: \\label or \\tag inside a formula is not workspace syntax; write {{#eq:...}} after the formula")
            if any(not line.strip() for line in lines[1:-1]):
                scan.problems.append(f"{where}: a display formula contains a blank line, which ends it on GitHub")
            if following and following[0] == "para" and len(following[2]) == 1 and EQ_LABEL.match(following[2][0].strip()):
                scan.define(EQ_LABEL.match(following[2][0].strip()).group(1), f"{display}:{following[3]}")
            continue
        if kind == "heading":
            match = HEADING.match(lines[0])
            text, attributes = match.group(2), ATTRIBUTES.search(match.group(2))
            explicit = None
            if attributes:
                text = text[:attributes.start()]
                found = re.search(r"#([^\s}]+)", attributes.group(1))
                explicit = found.group(1) if found else None
            identifier = explicit or scan.heading_id(text)
            scan.define(identifier if identifier.startswith("sec:") else f"sec:{identifier}", where)
        if kind == "para" and len(lines) == 1 and EQ_LABEL.match(lines[0].strip()):
            previous = blocks[position - 1] if position else None
            if not previous or previous[0] != "math":
                scan.problems.append(f"{where}: the equation label {lines[0].strip()} does not follow a display formula")
            continue
        for offset, line in enumerate(lines):
            at = f"{display}:{start + offset}"
            if re.search(r"\$\$.+\$\$", line):
                scan.warnings.append(f"{at}: write a display formula with $$ on separate lines")
            for image in IMAGE.finditer(line):
                target = image.group(2)
                if not re.match(r"^[a-z]+://", target) and not (folder / target).exists():
                    scan.problems.append(f"{at}: the image {target} does not exist")
                if image.group(3) and "#fig:" in image.group(3):
                    scan.define(re.search(r"#(fig:[^\s}]+)", image.group(3)).group(1), at)
            caption = CAPTION.match(line) if offset == 0 else None
            if caption and caption.group(3) and "#tbl:" in caption.group(3):
                scan.define(re.search(r"#(tbl:[^\s}]+)", caption.group(3)).group(1), at)
            text = prose(line)
            if CURRENCY.search(INLINE_CODE.sub(" ", line)):
                scan.warnings.append(f"{at}: a dollar sign before a number is read as math; write a literal amount as \\$")
            for key in citation_keys(text):
                scan.citation_occurrences.append((key, at))
            for match in doubled_reference(text):
                scan.warnings.append(f"{at}: “{match}” repeats the word that the output puts before the number; write the @-reference alone")
            for match in hand_numbered(text):
                scan.warnings.append(f"{at}: “{match.strip()}” looks hand-numbered; refer with @fig:, @tbl:, @eq:, or @sec: instead")
            if open_marker(line):
                scan.open_items.append(f"{at}: {line.strip()[:120]}")


def bibliography_keys(root: Path) -> set | None:
    path = root / "references" / "bibliography.bib"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    return {key for kind, key in re.findall(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text) if kind.lower() not in ("comment", "string", "preamble")}


def section_paths(root: Path, manifest: dict) -> tuple:
    folder = root / "manuscript"
    paths, problems, seen = [], [], set()
    for name in manifest["sections"]:
        if name in seen:
            problems.append(f"manuscript/manifest.yaml: {name} is listed twice")
        seen.add(name)
        path = (folder / name).resolve()
        if name in NOT_SECTIONS or Path(name).name in NOT_SECTIONS or not name.endswith(".md"):
            problems.append(f"manuscript/manifest.yaml: {name} is not a section file and must not be assembled")
        elif folder.resolve() not in path.parents:
            problems.append(f"manuscript/manifest.yaml: {name} is outside manuscript/")
        elif not path.is_file():
            problems.append(f"manuscript/manifest.yaml: manuscript/{name} does not exist")
        else:
            paths.append((name, path))
    return paths, problems


def analyse(root: Path) -> dict:
    """Everything the check reports: problems, warnings, open items, unlisted drafts, and counts."""
    manifest = read_manifest(root)
    paths, problems = section_paths(root, manifest)
    scan = Scan()
    metadata = metadata_name(root, manifest)
    if metadata:
        meta = root / "manuscript" / metadata
        if not meta.is_file():
            problems.append(f"manuscript/manifest.yaml: the metadata file manuscript/{metadata} does not exist")
        else:
            text = meta.read_text(encoding="utf-8")
            scan.problems.extend(signature_problems(text, f"manuscript/{metadata}", metadata=True))
            if not re.search(r"^title\s*:", text, re.M):
                scan.warnings.append(f"manuscript/{metadata}: no title")
    totals = [0, 0]
    for name, path in paths:
        scan_file(path, f"manuscript/{name}", scan, root / "manuscript")
        words, cjk = count_words(path.read_text(encoding="utf-8"))
        totals[0] += words
        totals[1] += cjk
    keys = bibliography_keys(root)
    known = set(scan.labels)
    if keys:
        known.update(keys)
    for raw, where in scan.citation_occurrences:
        key = normalize_reference(raw, known)
        prefix = key.split(":", 1)[0]
        if ":" in key and prefix in CROSSREF:
            scan.references.append((key, where))
        else:
            scan.citations.append((key, where))
    for label, where in scan.references:
        if label not in scan.labels:
            scan.problems.append(f"{where}: @{label} refers to no figure, table, equation, or section")
    cited = sorted({key for key, _ in scan.citations})
    if cited and keys is None:
        problems.append("references/bibliography.bib does not exist, but the manuscript cites " + ", ".join(cited[:10]))
    elif cited:
        for key, where in scan.citations:
            if key not in keys:
                scan.problems.append(f"{where}: the citation key @{key} is not in references/bibliography.bib")
    listed = {Path(name).as_posix() for name in manifest["sections"]}
    drafts = sorted(p.relative_to(root / "manuscript").as_posix() for p in (root / "manuscript").glob("**/*.md")
                    if p.name not in NOT_SECTIONS and "assets" not in p.relative_to(root / "manuscript").parts
                    and p.relative_to(root / "manuscript").as_posix() not in listed)
    return {"paths": paths, "problems": problems + scan.problems, "warnings": scan.warnings, "open_items": scan.open_items,
            "drafts": drafts, "words": totals[0], "cjk": totals[1], "labels": len(scan.labels), "cited": cited,
            "keys_resolve": bool(cited) and keys is not None, "diagrams": scan.mermaid}


def command_check(args, root: Path) -> int:
    result = analyse(root)
    size = f"{result['words']} words" + (f" and {result['cjk']} CJK characters" if result["cjk"] else "")
    print(f"Manuscript: {len(result['paths'])} section file(s), {size}, {result['labels']} label(s), {len(result['cited'])} cited key(s), "
          f"{result['diagrams']} diagram(s).")
    for title, items in (("Problems", result["problems"]), ("Warnings", result["warnings"]), ("Open items", result["open_items"])):
        if items:
            print(f"{title} ({len(items)}):")
            for item in items:
                print(f"  - {item}")
    if result["drafts"]:
        print("Not assembled (not in the manifest): " + ", ".join(result["drafts"]))
    if result["keys_resolve"]:
        print("Citation keys resolve; whether each source supports its claim is a separate check (literature-and-evidence).")
    return 1 if result["problems"] else 0


def command_assemble(args, root: Path) -> int:
    manifest = read_manifest(root)
    paths, problems = section_paths(root, manifest)
    if problems:
        raise Refused("; ".join(problems))
    if not paths:
        raise Refused("the manifest lists no section files yet")
    parts = []
    metadata = metadata_name(root, manifest)
    if metadata and (root / "manuscript" / metadata).is_file():
        parts.append("---\n" + (root / "manuscript" / metadata).read_text(encoding="utf-8").strip() + "\n---")
    for name, path in paths:
        parts.append(path.read_text(encoding="utf-8").strip())
        words, cjk = count_words(path.read_text(encoding="utf-8"))
        print(f"  {name}: {words} words" + (f", {cjk} CJK characters" if cjk else ""))
    target = Path(args.to) if args.to else root / "outputs" / "preview" / "manuscript.md"
    target = target if target.is_absolute() else root / target
    write_text_atomic(target, "\n\n".join(parts) + "\n")
    print(f"Assembled {len(paths)} section file(s) into {target.relative_to(root).as_posix() if root in target.parents else target}.")
    return 0


# Adopting an existing manuscript

MARK = re.compile(r"\{\.(?:insertion|deletion|comment-start|comment-end|paragraph-insertion|paragraph-deletion)\b")
FOOTNOTE_DEFINITION = re.compile(r"^\[\^([^\]]+)\]:")


def split_front_matter(text: str) -> tuple:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end > 0:
            return text[4:end], text[end + 5:]
    return "", text


def split_references(meta: str) -> tuple:
    """(metadata without the references list, the references list as YAML), from Pandoc's YAML block."""
    kept, references, inside = [], [], False
    for line in meta.splitlines():
        if re.match(r"^references\s*:", line):
            inside = True
        elif inside and line and not line.startswith((" ", "-")):
            inside = False
        (references if inside else kept).append(line)
    return "\n".join(kept).strip(), "\n".join(references).strip()


def footnote_definitions(body: str) -> tuple:
    """(body without footnote definitions, {id: definition text})."""
    lines, kept, definitions, current = body.splitlines(), [], {}, None
    for line in lines:
        match = FOOTNOTE_DEFINITION.match(line)
        if match:
            current = match.group(1)
            definitions[current] = [line]
        elif current and (line.startswith(("    ", "\t")) or (not line.strip() and definitions[current][-1].strip())):
            definitions[current].append(line)
        else:
            current = None
            kept.append(line)
    return "\n".join(kept), {key: "\n".join(value).rstrip() for key, value in definitions.items()}


def split_sections(body: str) -> list:
    """[(title, text)] split at the highest heading level used; text before the first heading is a front section."""
    blocks = blocks_of(body)
    headings = [(start, len(HEADING.match(lines[0]).group(1)), HEADING.match(lines[0]).group(2))
                for kind, _, lines, start in blocks if kind == "heading"]
    if not headings:
        return [("manuscript", body.strip())]
    top = min(level for _, level, _ in headings)
    cuts = [(start, title) for start, level, title in headings if level == top]
    lines, sections = body.splitlines(), []
    front = "\n".join(lines[:cuts[0][0] - 1]).strip()
    if front:
        sections.append(("front matter", front))
    for number, (start, title) in enumerate(cuts):
        end = cuts[number + 1][0] - 1 if number + 1 < len(cuts) else len(lines)
        sections.append((ATTRIBUTES.sub("", title).strip(), "\n".join(lines[start - 1:end]).strip()))
    return sections


def inventory(name: str, text: str) -> dict:
    found = {"file": name, "words": count_words(text)[0], "cjk": count_words(text)[1], "display": 0, "inline": 0, "images": 0,
             "tables": 0, "footnotes": len(set(re.findall(r"\[\^([^\]]+)\](?!:)", text))), "citations": set(), "labels": set(),
             "numbered_in_formula": 0, "raw_latex": 0, "equation_images": 0}
    for kind, _, lines, _ in blocks_of(text):
        if kind == "math":
            found["display"] += 1
            if re.search(r"\(\s*\d+\s*\)\s*$", "\n".join(lines[1:-1]).strip()):
                found["numbered_in_formula"] += 1
        elif kind == "para":
            joined = "\n".join(lines)
            found["inline"] += len(INLINE_MATH.findall(INLINE_CODE.sub(" ", joined)))
            found["tables"] += int(lines[0].lstrip().startswith("|") and len(lines) > 1 and set(lines[1].replace(" ", "")) <= set("|-:"))
            found["raw_latex"] += len(re.findall(r"^\s*\\(?:begin|end|[a-zA-Z]+\{)", joined, re.M))
            for image in IMAGE.finditer(joined):
                found["images"] += 1
                found["equation_images"] += int(image.group(2).lower().endswith((".wmf", ".emf")))
            for key in citation_keys(prose(joined)):
                (found["labels"] if key.split(":", 1)[0] in CROSSREF and ":" in key else found["citations"]).add(key)
    return found


def command_adopt(args, root: Path) -> int:
    folder = root / "inbox" / "imports" / args.import_id
    markdown_dir = folder / "extracted" / "markdown"
    documents = sorted(p for p in markdown_dir.glob("*.md") if p.name != "README.md" and not p.name.endswith(".annotations.md")) \
        if markdown_dir.is_dir() else []
    if not documents:
        raise Refused(f"import {args.import_id} holds no converted manuscript; convert it with python scripts/ingest.py run --to manuscript")
    if args.document:
        documents = [d for d in documents if d.stem == args.document]
    if len(documents) != 1:
        raise Refused("name the document to adopt with --document: " + ", ".join(d.stem for d in sorted(markdown_dir.glob("*.md"))
                                                                              if d.name != "README.md" and not d.name.endswith(".annotations.md")))
    document = documents[0]
    text = document.read_text(encoding="utf-8")
    marks = MARK.findall(text)
    if marks:
        raise Refused(f"the converted text still carries {len(marks)} tracked-change or comment mark(s); the researcher decides "
                      "whether to accept or reject the changes (convert again with --track-changes accept or reject) or to handle "
                      f"them one by one; the comments are listed in {document.with_name(document.stem + '.annotations.md').name}")
    meta, body = split_front_matter(text)
    meta, references = split_references(meta)
    body, notes = footnote_definitions(body)
    sections = split_sections(body)
    if args.into == "manuscript":
        if read_manifest(root)["sections"]:
            raise Refused("the manuscript already lists section files; stage the import as a revision candidate to compare "
                          "(--into candidate --revision-id ID after revision-start), never over the current manuscript")
        target = root / "manuscript"
    else:
        if not args.revision_id:
            raise Refused("--into candidate needs --revision-id")
        revision = revision_folder(root, args.revision_id)
        load_baseline(revision)
        target = revision / "candidate"
        target.mkdir(parents=True, exist_ok=True)
    assets_used, missing = [], []

    def relink(match: re.Match) -> str:
        link = match.group(2)
        if link.startswith("../assets/"):
            name = link[len("../assets/"):]
            source = folder / "extracted" / "assets" / name
            if source.is_file():
                (target / "assets").mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target / "assets" / name)
                assets_used.append(name)
                return match.group(0).replace(link, f"assets/{name}")
            missing.append(name)
        return match.group(0)

    names, rows = [], []
    for number, (title, content) in enumerate(sections):
        content = IMAGE.sub(relink, content)
        used = sorted(set(re.findall(r"\[\^([^\]]+)\](?!:)", content)))
        content = content.rstrip() + ("\n\n" + "\n\n".join(notes[key] for key in used if key in notes) if any(k in notes for k in used) else "")
        # The front matter, when there is one, is 00; the sections are numbered from 01.
        position = number if sections[0][0] == "front matter" else number + 1
        base = "front-matter" if title == "front matter" else slug(title, limit=40, fallback="section")
        name, suffix = f"{position:02d}-{base}.md", 2
        while (target / name).exists():
            name, suffix = re.sub(r"(-\d+)?\.md$", f"-{suffix}.md", name), suffix + 1
        write_text_atomic(target / name, content + "\n")
        names.append(name)
        rows.append(inventory(name, content))
    metadata_note = ""
    if meta:
        meta_target = target / "metadata.yaml"
        if meta_target.exists():
            meta_target = folder / "metadata.yaml"
            metadata_note = f"kept in inbox/imports/{args.import_id}/metadata.yaml because the manuscript already has one"
        write_text_atomic(meta_target, meta + "\n")
    if references:
        write_text_atomic(folder / "references.yaml", references + "\n")
        try:
            from export import tools
            pandoc = tools.find(root)["pandoc"]
        except ImportError:
            pandoc = None
        if pandoc:
            completed = subprocess.run([pandoc, "-f", "markdown", "-t", "bibtex", "-o", str(folder / "references.bib")],
                                       input=f"---\n{references}\n---\n", capture_output=True, text=True)
            if completed.returncode != 0:
                (folder / "references.bib").unlink(missing_ok=True)
    manifest_lines = ["# Manuscript assembly manifest, maintained by the agent.",
                      "# Lists the section files (paths relative to this directory) in reading order.",
                      "# Only listed files are assembled; README.md, outline.md, notes, and drafts never are.", "version: 1"]
    if meta and not metadata_note:
        manifest_lines.append("metadata: metadata.yaml")
    manifest_lines += ["sections:"] + [f"  - {name}" for name in names]
    write_text_atomic(target / "manifest.yaml", "\n".join(manifest_lines) + "\n")
    keys = bibliography_keys(root) or set()
    cited = sorted(set().union(*(row["citations"] for row in rows)))
    unresolved = [key for key in cited if key not in keys]
    report = [f"# Adoption of {document.stem}", "",
              f"Converted from `{document.relative_to(folder).as_posix()}` into `{target.relative_to(root).as_posix()}/` on "
              f"{datetime.now():%Y-%m-%d}. The originals stay in [`originals/`](originals/README.md).", "",
              "| Section file | Words | CJK | Display formulas | Inline formulas | Images | Tables | Footnotes | Citations |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for row in rows:
        report.append(f"| `{row['file']}` | {row['words']} | {row['cjk']} | {row['display']} | {row['inline']} | {row['images']} | "
                      f"{row['tables']} | {row['footnotes']} | {len(row['citations'])} |")
    checks = []
    if unresolved:
        checks.append(f"Citation keys not in `references/bibliography.bib` ({len(unresolved)}): " + ", ".join(unresolved[:30]) +
                      (". The citation metadata found in the document is in `references.bib` here." if (folder / "references.bib").is_file()
                       else "."))
    for key, words in (("numbered_in_formula", "display formula(s) end with a typed number such as (1); the export numbers formulas itself"),
                       ("raw_latex", "line(s) of LaTeX that were not converted"),
                       ("equation_images", "image(s) in Windows metafile format, often equations from an old equation editor; they need transcription")):
        total = sum(row[key] for row in rows)
        if total:
            checks.append(f"{total} {words}.")
    if missing:
        checks.append("Images that the extraction does not hold: " + ", ".join(missing))
    annotations = document.with_name(document.stem + ".annotations.md")
    if annotations.is_file():
        checks.append(f"The original had comments or tracked changes; they are listed in `extracted/markdown/{annotations.name}`.")
    if metadata_note:
        checks.append(f"The document's metadata was {metadata_note}.")
    report += ["", "## Needs a check", ""] + ([f"- {item}" for item in checks] or ["- Nothing was flagged; compare the result with the original anyway."])
    write_text_atomic(folder / "mapping.md", "\n".join(report) + "\n")
    print(f"Adopted {document.stem} as {len(names)} section file(s) in {target.relative_to(root).as_posix()}/: " + ", ".join(names))
    print(f"{len(assets_used)} image(s) copied; the mapping and the items to check are in inbox/imports/{args.import_id}/mapping.md.")
    for item in checks:
        print(f"  - {item}")
    return 0


# Input-versioned check records

def checks_file(root: Path) -> Path:
    return root / "outputs" / "checks" / "checks.json"


def load_checks(root: Path) -> dict:
    path = checks_file(root)
    if path.is_file():
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("schema") == "paper-template.checks/1":
            return data
    return {"schema": "paper-template.checks/1", "checks": []}


CHECKS_README = (
    "Records of checks made on the manuscript and its outputs: audits, evidence checks, format checks, and readiness "
    "assessments. Each record in `checks.json` names the files it examined with their checksums, so that "
    "`python scripts/manuscript.py checks` can tell whether a result still applies. A result whose inputs changed is "
    "stale and is never carried forward as proof. The findings of a check are kept in a Markdown report next to it, "
    "in the interaction language.")


def command_record_check(args, root: Path) -> int:
    inputs = []
    for value in args.input:
        path = root / value
        if not path.exists():
            raise Refused(f"{value} does not exist")
        inputs.append({"path": Path(value).as_posix(), "sha256": checksum(path)})
    if args.report and not (root / args.report).is_file():
        raise Refused(f"the report {args.report} does not exist")
    update_readme(root / "outputs" / "checks" / "README.md", "Check Records", CHECKS_README, OWNER)
    data = load_checks(root)
    base = f"{datetime.now():%Y-%m-%d}-{slug(args.name, limit=40, fallback='check')}"
    check_id, number = base, 2
    while any(entry["id"] == check_id for entry in data["checks"]):
        check_id, number = f"{base}-{number}", number + 1
    data["checks"].append({"id": check_id, "name": args.name, "kind": args.kind, "scope": args.scope or "",
                           "result": args.result, "summary": args.summary, "report": args.report or "",
                           "date": datetime.now().isoformat(timespec="seconds"), "inputs": inputs})
    write_json_atomic(checks_file(root), data)
    print(f"Recorded check {check_id} ({args.result}) over {len(inputs)} input(s).")
    return 0


def changed_inputs(root: Path, entry: dict) -> list:
    """The inputs of a recorded check that no longer exist or no longer match their checksum."""
    return [item["path"] for item in entry["inputs"]
            if not (root / item["path"]).exists() or checksum(root / item["path"]) != item["sha256"]]


def command_checks(args, root: Path) -> int:
    data = load_checks(root)
    if not data["checks"]:
        print("No checks recorded.")
        return 0
    stale = 0
    for entry in data["checks"]:
        changed = changed_inputs(root, entry)
        state = "stale: " + ", ".join(changed) + " changed" if changed else "current"
        stale += bool(changed)
        print(f"{entry['id']}: {entry['kind']}, {entry['result']} — {entry['summary'][:100]} ({state})")
    return 2 if stale else 0


# Major revisions

SNAPSHOT_ROOTS = ("manuscript", "requirements", "references/bibliography.bib", "research/plan.md")


def revision_folder(root: Path, revision_id: str) -> Path:
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", revision_id):
        raise Refused("a revision ID uses lowercase ASCII letters, digits, and single hyphens, for example 2026-11-argument")
    return root / "revisions" / revision_id


def snapshot_files(root: Path, extra: list) -> list:
    files = []
    for value in list(SNAPSHOT_ROOTS) + list(extra):
        path = root / value
        if path.is_file():
            files.append(Path(value).as_posix())
        elif path.is_dir():
            files += [p.relative_to(root).as_posix() for p in sorted(path.rglob("*")) if p.is_file() and p.name != "README.md"
                      and not any(part.startswith(".") for part in p.relative_to(root).parts)]
    return sorted(set(files))


def git_state(root: Path) -> dict:
    if not shutil.which("git"):
        return {"available": False}
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True)
    if head.returncode != 0:
        return {"available": True, "version": None}
    dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--", "manuscript", "requirements"], capture_output=True, text=True)
    return {"available": True, "version": head.stdout.strip(), "unsaved_changes": bool(dirty.stdout.strip())}


def load_baseline(folder: Path) -> dict:
    path = folder / "baseline.json"
    if not path.is_file():
        raise Refused(f"{folder.name} has no baseline; start the revision with revision-start")
    return json.loads(path.read_text(encoding="utf-8"))


def load_closure(folder: Path) -> dict | None:
    """The closing record of a revision (completed or abandoned), or None while the revision is open."""
    path = folder / "closed.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def write_closure(folder: Path, outcome: str, note: str = "", **extra) -> dict:
    log = folder / "apply.json"
    record = {"schema": "paper-template.revision-closed/1", "revision": folder.name, "outcome": outcome,
              "closed": datetime.now().isoformat(timespec="seconds"), "mode": "candidate" if log.is_file() else "in place",
              "note": note, **extra}
    write_json_atomic(folder / "closed.json", record)
    return record


def command_revision_start(args, root: Path) -> int:
    folder = revision_folder(root, args.id)
    if (folder / "baseline.json").exists():
        raise Refused(f"revision {args.id} already has a baseline; it is never replaced")
    files = snapshot_files(root, args.include or [])
    for value in args.include or []:
        if not (root / value).exists():
            raise Refused(f"{value} does not exist")
    baseline = folder / "baseline"
    inventory = {}
    for name in files:
        target = baseline / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(root / name, target)
        inventory[name] = sha256_file(target)
    record = {"schema": "paper-template.revision-baseline/1", "revision": args.id,
              "created": datetime.now().isoformat(timespec="seconds"), "git": git_state(root),
              "included": list(SNAPSHOT_ROOTS) + list(args.include or []), "files": inventory}
    write_json_atomic(folder / "baseline.json", record)
    update_readme(folder / "README.md", f"Revision {args.id}", (
        f"Major revision `{args.id}`. [`baseline/`](baseline/README.md) holds the starting version, copied on "
        f"{record['created'][:10]} with checksums in `baseline.json`, so it can be recovered with or without Git. `plan.md` "
        "states the goal, scope, affected material, ordered work, and next action; `changes.md` maps old to new sections, "
        "claims, figures, and citations; `checks.md` records which inputs were checked with what result. A staged manuscript, "
        "when one is used, is in `candidate/` and is never assembled until it is applied. `closed.json` appears when the "
        "revision is completed or abandoned; until then the project status reports the revision as open."), OWNER)
    update_readme(baseline / "README.md", f"Baseline of {args.id}", (
        f"The starting version of revision `{args.id}`: the manuscript, the requirements, the bibliography, the research plan, "
        "and any other included files, exactly as they were when the revision began. Nothing here is edited; "
        "`python scripts/manuscript.py revision-restore` copies it back if the revision is abandoned."), OWNER)
    git = record["git"]
    where = f" Git version {git['version'][:7]}" + (" plus unsaved changes" if git.get("unsaved_changes") else "") if git.get("version") else ""
    print(f"Revision {args.id}: baseline of {len(files)} file(s) kept in revisions/{args.id}/baseline/.{where}")
    return 0


def changed_since(root: Path, baseline: dict) -> tuple:
    current = snapshot_files(root, [value for value in baseline["included"] if value not in SNAPSHOT_ROOTS])
    changed = [p for p in baseline["files"] if (root / p).is_file() and sha256_file(root / p) != baseline["files"][p]]
    removed = [p for p in baseline["files"] if not (root / p).is_file()]
    added = [p for p in current if p not in baseline["files"]]
    return changed, added, removed


def candidate_files(folder: Path) -> list:
    candidate = folder / "candidate"
    if not candidate.is_dir():
        return []
    return sorted(p.relative_to(candidate).as_posix() for p in candidate.rglob("*") if p.is_file() and p.name != "README.md")


def command_revision_status(args, root: Path) -> int:
    folder = revision_folder(root, args.id)
    baseline = load_baseline(folder)
    changed, added, removed = changed_since(root, baseline)
    print(f"Revision {args.id}, baseline of {baseline['created'][:10]}:")
    closed = load_closure(folder)
    if closed:
        print(f"  Closed: {closed['outcome']} on {closed['closed'][:10]} ({closed['mode']})" + (f"; {closed['note']}" if closed.get("note") else "") + ".")
    for label, items in (("Changed since the baseline", changed), ("New since the baseline", added), ("Removed since the baseline", removed)):
        if items:
            print(f"  {label}: " + ", ".join(items))
    if not (changed or added or removed):
        print("  The workspace still matches the baseline.")
    staged = candidate_files(folder)
    log = folder / "apply.json"
    data = json.loads(log.read_text(encoding="utf-8")) if log.is_file() else None
    applied = {op["path"]: op["new_sha256"] for op in (data or {}).get("operations", []) if op.get("done")}
    if staged:
        conflicts = []
        for name in staged:
            path = f"manuscript/{name}"
            current = root / path
            if path in applied:
                if not current.is_file() or sha256_file(current) != applied[path]:
                    conflicts.append(path)
            elif path in changed or path in added:
                conflicts.append(path)
        print(f"  Candidate: {len(staged)} file(s)." + (" Edited in manuscript/ since the baseline, to reconcile before applying: "
                                                        + ", ".join(conflicts) if conflicts else ""))
    if data:
        done = sum(op["done"] for op in data["operations"])
        state = data["status"] if data["status"] != "in progress" else f"interrupted after {done} of {len(data['operations'])} file(s); continue with revision-apply --resume"
        print(f"  Application: {state}.")
    return 0


def describe_replaced(folder: Path) -> None:
    update_readme(folder / "replaced" / "README.md", "Replaced manuscript versions", (
        "Copies of manuscript or other workspace files kept before a revision candidate was applied or a baseline "
        "was restored. The dated folders preserve the previous contents so changes can be inspected and recovered; "
        "the application log identifies the saved files when a candidate was applied."), OWNER)


def command_revision_apply(args, root: Path) -> int:
    folder = revision_folder(root, args.id)
    baseline = load_baseline(folder)
    log_path = folder / "apply.json"
    log = json.loads(log_path.read_text(encoding="utf-8")) if log_path.is_file() else None
    if log and log["status"] == "applied":
        raise Refused(f"the candidate of {args.id} was already applied on {log['finished'][:10]}")
    if log and not args.resume:
        raise Refused("an earlier application was interrupted; continue it with --resume")
    if not log:
        if args.resume:
            raise Refused("there is no interrupted application to resume")
        staged = candidate_files(folder)
        if not staged:
            raise Refused(f"revisions/{args.id}/candidate/ holds no files to apply")
        reconciled = {Path(value).as_posix() for value in args.reconciled or []}
        conflicts = []
        for name in staged:
            target = f"manuscript/{name}"
            current = root / target
            if current.is_file() and target not in reconciled and baseline["files"].get(target) != sha256_file(current):
                conflicts.append(target)
        if conflicts:
            raise Refused("these files were edited after the baseline and are not reconciled with the candidate: " + ", ".join(conflicts) +
                          ". Merge those edits into the candidate, then apply with --reconciled for each file")
        stamp = f"{datetime.now():%Y%m%d-%H%M%S}"
        operations = []
        for name in staged:
            target = root / "manuscript" / name
            keep = None
            if target.is_file():
                keep = f"replaced/{stamp}/manuscript/{name}"
                (folder / keep).parent.mkdir(parents=True, exist_ok=True)
                describe_replaced(folder)
                shutil.copy2(target, folder / keep)
            operations.append({"path": f"manuscript/{name}", "from": f"candidate/{name}", "kept_previous": keep,
                               "new_sha256": sha256_file(folder / "candidate" / name), "done": False})
        log = {"schema": "paper-template.revision-apply/1", "revision": args.id, "status": "in progress",
               "started": datetime.now().isoformat(timespec="seconds"), "reconciled": sorted(reconciled), "operations": operations}
        write_json_atomic(log_path, log)
    for operation in log["operations"]:
        source, target = folder / operation["from"], root / operation["path"]
        if operation["done"]:
            if not target.is_file() or sha256_file(target) != operation["new_sha256"]:
                print(f"The applied file {operation['path']} changed during the interruption; the application stopped without overwriting it.")
                return 1
            continue
        if sha256_file(source) != operation["new_sha256"]:
            print(f"The candidate file {operation['from']} changed during the application; the application stopped.")
            return 1
        # A file may have been replaced just before a crash, before its completed flag was saved.
        if target.is_file() and sha256_file(target) == operation["new_sha256"]:
            operation["done"] = True
            write_json_atomic(log_path, log)
            continue
        previous = folder / operation["kept_previous"] if operation.get("kept_previous") else None
        unchanged = (previous is not None and previous.is_file() and target.is_file()
                     and sha256_file(previous) == sha256_file(target)) or (previous is None and not target.exists())
        if not unchanged:
            print(f"The file {operation['path']} changed during the application; the application stopped without overwriting it.")
            return 1
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(f".applying-{target.name}")
        shutil.copy2(source, temporary)
        temporary.replace(target)
        operation["done"] = True
        write_json_atomic(log_path, log)
    log["status"], log["finished"] = "applied", datetime.now().isoformat(timespec="seconds")
    write_json_atomic(log_path, log)
    staged = {op["path"] for op in log["operations"]}
    left = sorted(p for p in baseline["files"] if p.startswith("manuscript/") and p not in staged and (root / p).is_file())
    print(f"Applied {len(log['operations'])} file(s) from revisions/{args.id}/candidate/ to manuscript/. "
          f"The replaced versions are kept in revisions/{args.id}/replaced/.")
    if left:
        print("Files that the candidate does not contain were left as they are: " + ", ".join(left))
    print("Run python scripts/manuscript.py check and recheck the affected parts; older check records are now stale where their inputs changed.")
    return 0


def command_revision_complete(args, root: Path) -> int:
    """Record that a revision is finished, so that the project status stops reporting it as open."""
    folder = revision_folder(root, args.id)
    load_baseline(folder)
    closed = load_closure(folder)
    if closed:
        raise Refused(f"revision {args.id} was already {closed['outcome']} on {closed['closed'][:10]}")
    log_path = folder / "apply.json"
    log = json.loads(log_path.read_text(encoding="utf-8")) if log_path.is_file() else None
    if log and log["status"] != "applied":
        raise Refused("the application of the candidate was interrupted; continue it with revision-apply --resume first")
    staged = candidate_files(folder)
    if staged and not log:
        raise Refused(f"revisions/{args.id}/candidate/ holds {len(staged)} file(s) that were not applied. Apply them with "
                      "revision-apply, or ask the researcher what to do with the candidate before completing the revision in place")
    analysis = analyse(root)
    stale = sum(bool(changed_inputs(root, entry)) for entry in load_checks(root)["checks"])
    remaining = {"problems": len(analysis["problems"]), "open_markers": len(analysis["open_items"]), "stale_checks": stale}
    record = write_closure(folder, "completed", args.note or "", remaining=remaining)
    print(f"Revision {args.id} is recorded as completed ({record['mode']}). The manuscript check reports {remaining['problems']} "
          f"problem(s) and {remaining['open_markers']} open marker(s), and {stale} recorded check(s) are stale.")
    if any(remaining.values()):
        print("The record does not hide this: recheck these (python scripts/manuscript.py check and checks) before calling the revision checked.")
    return 0


def command_revision_restore(args, root: Path) -> int:
    folder = revision_folder(root, args.id)
    baseline = load_baseline(folder)
    changed, added, removed = changed_since(root, baseline)
    stamp = f"{datetime.now():%Y%m%d-%H%M%S}"
    for name in changed:
        keep = folder / "replaced" / stamp / name
        keep.parent.mkdir(parents=True, exist_ok=True)
        describe_replaced(folder)
        shutil.copy2(root / name, keep)
    for name in changed + removed:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(folder / "baseline" / name, target)
    print(f"Restored {len(changed) + len(removed)} file(s) to the baseline of {args.id}." +
          (f" The current versions were kept in revisions/{args.id}/replaced/{stamp}/." if changed else ""))
    if added:
        print("Files created after the baseline were left in place: " + ", ".join(added))
    write_closure(folder, "abandoned", "the baseline was restored")
    print(f"Revision {args.id} is recorded as abandoned; start a new revision for another attempt.")
    return 0


def main(argv: list | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Check, assemble, and revise the manuscript.")
    parser.add_argument("--root", type=Path, default=ROOT, help="workspace root (default: the parent of the scripts folder)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="check the manuscript against the workspace conventions")
    sections = commands.add_parser("set-sections", help="set the ordered list of section files in the manifest")
    sections.add_argument("files", nargs="*")
    assemble = commands.add_parser("assemble", help="join the listed section files into one preview file")
    assemble.add_argument("--to")
    record = commands.add_parser("record-check", help="record a check with the checksums of the inputs it examined")
    record.add_argument("--name", required=True)
    record.add_argument("--kind", required=True, choices=("audit", "evidence", "format", "readiness", "other"))
    record.add_argument("--input", action="append", required=True)
    record.add_argument("--result", required=True, choices=("passed", "findings", "failed"))
    record.add_argument("--summary", required=True)
    record.add_argument("--scope")
    record.add_argument("--report")
    commands.add_parser("checks", help="list recorded checks and whether their inputs changed")
    adopt_parser = commands.add_parser("adopt", help="adopt a converted manuscript from an import into manuscript/ or a revision candidate")
    adopt_parser.add_argument("--import-id", required=True)
    adopt_parser.add_argument("--document")
    adopt_parser.add_argument("--into", choices=("manuscript", "candidate"), default="manuscript")
    adopt_parser.add_argument("--revision-id")
    for name, help_text in (("revision-start", "keep a baseline snapshot for a major revision"),
                            ("revision-status", "compare the workspace and the candidate with the baseline"),
                            ("revision-apply", "apply the staged candidate to manuscript/, resumably"),
                            ("revision-complete", "record a revision, in place or applied, as completed"),
                            ("revision-restore", "copy the baseline back, keeping the current versions, and record the revision as abandoned")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("--id", required=True)
        if name == "revision-start":
            command.add_argument("--include", action="append")
        if name == "revision-complete":
            command.add_argument("--note", help="a short remark kept in the closing record")
        if name == "revision-apply":
            command.add_argument("--reconciled", action="append")
            command.add_argument("--resume", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    handlers = {"check": command_check, "set-sections": command_set_sections, "assemble": command_assemble, "adopt": command_adopt,
                "record-check": command_record_check, "checks": command_checks, "revision-start": command_revision_start,
                "revision-status": command_revision_status, "revision-apply": command_revision_apply,
                "revision-complete": command_revision_complete, "revision-restore": command_revision_restore}
    try:
        return handlers[args.command](args, root)
    except Refused as error:
        print(f"Refused: {error}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
