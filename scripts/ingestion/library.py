"""The reference library: archived originals, published extractions, the index, and the bibliography.

A source ID comes from the original's SHA-256, so the same file always gets the same ID and a
different file (another version, for example) gets another one, whatever the file names are.
"""

from __future__ import annotations

import os
import re
import shutil
import unicodedata
import uuid
from pathlib import Path

from .common import read_json, safe_filename, sha256_file, update_readme, write_text_atomic

INDEX_HEADER = "| Source | Title | Authors | Year | Reading status | Extraction | Files |"
INDEX_RULE = "| --- | --- | --- | --- | --- | --- | --- |"
INDEX_EMPTY = "No sources have been collected yet."
BIB_HEADER = (
    "% Citation metadata for this workspace, maintained by the agent with scripts/ingest.py.\n"
    "% sourceid links an entry to its folders in references/. metadatasource = {document} means that\n"
    "% the fields were read from the document itself and not checked against an authoritative record.\n"
)
FIELD_ORDER = ("author", "editor", "title", "journal", "booktitle", "publisher", "school", "institution", "year",
               "month", "volume", "number", "pages", "doi", "url", "isbn", "issn")
VERBATIM = {"doi", "url", "isbn", "issn", "sourceid", "metadatasource", "year", "month", "volume", "number", "pages", "urldate"}
STOPWORDS = {"the", "a", "an", "of", "on", "in", "for", "and", "to", "with", "from", "by", "at", "via", "toward", "towards"}
TEX = str.maketrans({"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "&": r"\&", "%": r"\%", "#": r"\#", "$": r"\$", "_": r"\_"})


class EditedError(RuntimeError):
    """The published Markdown was changed by hand after conversion."""


def originals(root: Path, source_id: str) -> Path:
    return root / "references" / "originals" / source_id


def extracted(root: Path, source_id: str) -> Path:
    return root / "references" / "extracted" / source_id


def archived_file(folder: Path) -> Path | None:
    files = [p for p in folder.iterdir() if p.is_file() and p.name != "README.md" and not p.name.startswith(".")] if folder.is_dir() else []
    return files[0] if len(files) == 1 else None


def lookup(root: Path, sha: str) -> str | None:
    for length in (12, 16, 24, 64):
        source_id = f"src-{sha[:length]}"
        found = archived_file(originals(root, source_id))
        if found is None:
            if not originals(root, source_id).exists():
                return None
            continue
        if sha256_file(found) == sha:
            return source_id
    return None


def allocate(root: Path, sha: str) -> str:
    for length in (12, 16, 24, 64):
        source_id = f"src-{sha[:length]}"
        if not originals(root, source_id).exists():
            return source_id
    raise RuntimeError("no free source ID")


def archive(root: Path, path: Path, sha: str, received: str, today: str) -> tuple:
    """Copy the original into references/originals/<source-id>/ unless it is already there."""
    source_id = lookup(root, sha)
    if source_id:
        return source_id, archived_file(originals(root, source_id)), False
    source_id = allocate(root, sha)
    folder = originals(root, source_id)
    folder.mkdir(parents=True)
    temporary = folder / f".copying-{uuid.uuid4().hex}"
    shutil.copy2(path, temporary)
    if sha256_file(temporary) != sha:
        temporary.unlink()
        raise OSError(f"the copy of {path.name} does not match the original")
    target = folder / safe_filename(path.name)
    os.replace(temporary, target)
    update_readme(folder / "README.md", f"Original: {source_id}", (
        f"The original file of source `{source_id}`, archived unchanged as `{target.name}`. "
        f"It was received from `{received}` on {today}. SHA-256: `{sha}`.\n\n"
        f"The readable extraction is in [`../../extracted/{source_id}/`](../../extracted/{source_id}/README.md), "
        f"and the source is listed in the [reference index](../../index.md). Never edit or replace this file; "
        f"corrections and interpretation belong in [`../../notes/{source_id}.md`](../../notes/README.md)."
    ))
    return source_id, target, True


def provenance(root: Path, source_id: str) -> dict | None:
    data = read_json(extracted(root, source_id) / "provenance.json")
    return data if isinstance(data, dict) else None


def edited(root: Path, source_id: str) -> bool:
    """True when document.md no longer matches what the last conversion wrote."""
    record = provenance(root, source_id)
    document = extracted(root, source_id) / "document.md"
    expected = ((record or {}).get("outputs") or {}).get("document_sha256")
    return bool(expected and document.is_file() and sha256_file(document) != expected)


def carry_readmes(root: Path, source_id: str, stage: Path) -> None:
    """Bring the published READMEs into the stage, so that text added outside the maintained block survives."""
    current = extracted(root, source_id)
    for relative in ("README.md", "assets/README.md", "native/README.md"):
        if (current / relative).is_file():
            (stage / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(current / relative, stage / relative)


def describe_conversion(conversion: dict) -> str:
    if conversion.get("route") == "local":
        return f"MinerU {conversion.get('version')} on this computer ({conversion.get('tier')} tier)"
    if conversion.get("route") == "cloud":
        return f"the mineru.net service ({conversion.get('model_version')} model)"
    return "direct reading, without a parser"


def write_readmes(stage: Path, record: dict) -> None:
    """READMEs of an extraction folder and its assets/ and native/ folders, kept with any text added outside the block."""
    source_id = record["source_id"]
    name = record["original"]["received_as"]
    coverage = record.get("coverage") or {}
    status = {"complete": "complete", "needs-review": "needs review", "partial": "partial"}.get(record["status"], record["status"])
    if coverage.get("unit") == "page" and coverage.get("expected"):
        extent = f"{coverage.get('processed')} of {coverage['expected']} pages (PDF page order, counted from 1)"
    elif coverage.get("unit") == "page":
        extent = "unknown: the total page count could not be read"
    else:
        extent = "the whole document" if coverage.get("status") == "complete" else "unknown"
    problems = [warning["message"] for warning in record.get("warnings") or [] if warning["level"] != "info"]
    notes = [warning["message"] for warning in record.get("warnings") or [] if warning["level"] == "info"]
    lines = [
        f"The readable extraction of source `{source_id}` (original file `{name}`), revision {record['revision']}, made on "
        f"{record['conversion']['finished_at'][:10]} with {describe_conversion(record['conversion'])}. Status: {status}.",
        "",
        f"- Coverage: {extent}.",
    ]
    if problems:
        lines += ["- Problems found by the automatic checks:"] + [f"  - {problem}" for problem in problems]
    else:
        lines.append("- The automatic checks found no problem. They do not prove that the text, tables, or formulas are correct.")
    lines += [f"- {note[0].upper()}{note[1:]}." for note in notes]
    native_role = ("stays empty because no parser was used" if record["conversion"].get("route") == "direct"
                   else "keeps the parser's own output")
    lines += [
        "",
        f"[`document.md`](document.md) is the readable text with working image links. [`assets/`](assets/README.md) holds its images, "
        f"[`native/`](native/README.md) {native_role}, and [`provenance.json`](provenance.json) records the checksum, "
        f"converter, settings, time, coverage, and warnings. The original is in [`../../originals/{source_id}/`](../../originals/{source_id}/README.md). "
        f"Report errors to the agent instead of editing `document.md`: corrections are kept in the source note, so they survive a new conversion.",
    ]
    update_readme(stage / "README.md", f"Extraction: {source_id}", "\n".join(lines))
    assets = record["outputs"]["assets"]
    (stage / "assets").mkdir(parents=True, exist_ok=True)
    update_readme(stage / "assets" / "README.md", f"Images: {source_id}", (
        f"Images extracted from `{name}` (source `{source_id}`): {len(assets)} file(s), linked from `../document.md`. "
        "They are derived copies; the original document stays authoritative, and a figure that matters for a claim is checked there."
    ))
    native = record["outputs"]["native"]
    (stage / "native").mkdir(parents=True, exist_ok=True)
    if record["conversion"].get("route") == "direct":
        text = (f"No parser output exists for source `{source_id}`: `{name}` was read directly. This folder stays empty "
                "so that every extraction has the same layout.")
    else:
        text = (f"The parser's own output for source `{source_id}` (`{name}`), kept unchanged for provenance and structured retrieval: "
                + ", ".join(f"`{path}`" for path in native) + ". Its Markdown links images under `images/`; those images are in "
                "`../assets/` with the same names. Page numbers inside these files count from 0.")
    update_readme(stage / "native" / "README.md", f"Parser output: {source_id}", text)


def publish(root: Path, source_id: str, stage: Path, overwrite_edited: bool = False) -> Path:
    """Replace references/extracted/<source-id>/ with the staged extraction in one rename."""
    target = extracted(root, source_id)
    if target.exists() and edited(root, source_id) and not overwrite_edited:
        raise EditedError(f"references/extracted/{source_id}/document.md was edited after conversion")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        old = target.with_name(f".{source_id}.replaced-{uuid.uuid4().hex[:8]}")
        os.replace(target, old)
        try:
            move(stage, target)
        except BaseException:
            os.replace(old, target)
            raise
        shutil.rmtree(old, ignore_errors=True)
    else:
        move(stage, target)
    return target


def move(source: Path, target: Path) -> None:
    try:
        os.replace(source, target)
    except OSError:
        # Another file system: copy next to the target, then rename.
        temporary = target.with_name(f".{target.name}.copying-{uuid.uuid4().hex[:8]}")
        shutil.copytree(source, temporary)
        os.replace(temporary, target)
        shutil.rmtree(source, ignore_errors=True)


def split_cells(line: str) -> list:
    cells, current, escaped = [], "", False
    for char in line.strip().strip("|"):
        if escaped:
            current += char
            escaped = False
        elif char == "\\":
            current += char
            escaped = True
        elif char == "|":
            cells.append(current.strip())
            current = ""
        else:
            current += char
    cells.append(current.strip())
    return cells


def cell(value: str) -> str:
    return (value or "—").replace("\n", " ").replace("|", "\\|")


def index_upsert(root: Path, source_id: str, *, title: str | None = None, authors: str | None = None, year: str | None = None,
                 extraction: str | None = None, files: str | None = None, default_title: str | None = None) -> None:
    """Add or update the source's row; the reading status set later by the agent or the researcher is kept.

    default_title fills the title only while the row has none, so a file name never replaces real metadata.
    """
    path = root / "references" / "index.md"
    text = path.read_text(encoding="utf-8") if path.is_file() else "# Reference Index\n"
    lines = text.rstrip("\n").split("\n")
    if INDEX_HEADER not in lines:
        if INDEX_EMPTY in lines:
            position = lines.index(INDEX_EMPTY)
            lines[position:position + 1] = [INDEX_HEADER, INDEX_RULE]
        else:
            lines += ["", INDEX_HEADER, INDEX_RULE]
    start = lines.index(INDEX_HEADER) + 2
    end = start
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    rows = [split_cells(line) for line in lines[start:end]]
    row = next((r for r in rows if r and r[0] == source_id), None)
    if row is None:
        row = [source_id, "—", "—", "—", "collected", "—", "—"]
        rows.append(row)
    row += ["—"] * (7 - len(row))
    if title is None and default_title and row[1] in ("", "—"):
        title = default_title
    for position, value in ((1, title), (2, authors), (3, year), (5, extraction), (6, files)):
        if value is not None:
            row[position] = cell(value)
    lines[start:end] = ["| " + " | ".join(r[:7]) + " |" for r in rows]
    write_text_atomic(path, "\n".join(lines) + "\n")


def entries(text: str) -> list:
    """(start, end, type, key, body) for each @entry, with brace matching."""
    found, position = [], 0
    pattern = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,")
    while True:
        match = pattern.search(text, position)
        if not match:
            return found
        depth, index = 0, text.index("{", match.start())
        while index < len(text):
            if text[index] == "{" and text[index - 1] != "\\":
                depth += 1
            elif text[index] == "}" and text[index - 1] != "\\":
                depth -= 1
                if depth == 0:
                    break
            index += 1
        found.append((match.start(), index + 1, match.group(1).lower(), match.group(2), text[match.end():index]))
        position = index + 1


def fields_of(body: str) -> dict:
    values, position = {}, 0
    pattern = re.compile(r"(\w[\w-]*)\s*=\s*\{")
    while True:
        match = pattern.search(body, position)
        if not match:
            return values
        depth, index = 1, match.end()
        while index < len(body) and depth:
            if body[index] == "{" and body[index - 1] != "\\":
                depth += 1
            elif body[index] == "}" and body[index - 1] != "\\":
                depth -= 1
            index += 1
        values[match.group(1).lower()] = body[match.end():index - 1]
        position = index


def ascii_letters(value: str) -> str:
    folded = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z]", "", folded.lower())


def make_key(authors: list, year: str, title: str, fallback: str, taken: set) -> str:
    family = ""
    if authors:
        first = authors[0]
        family = first.split(",")[0] if "," in first else first.split()[-1] if first.split() else ""
    family = ascii_letters(family)
    word = next((w for w in (ascii_letters(t) for t in re.split(r"\s+", title or "")) if len(w) >= 3 and w not in STOPWORDS), "")
    base = f"{family}{year}{word}" if family and year and re.fullmatch(r"\d{4}", year) else fallback
    key, suffix = base, 0
    while key in taken:
        suffix += 1
        key = base + chr(ord("a") + suffix - 1) if suffix <= 26 else f"{base}-{suffix}"
    return key


def cited(root: Path, key: str) -> bool:
    pattern = re.compile(r"@" + re.escape(key) + r"(?![\w:.#$%&+?<>~/-]*[\w])")
    for path in (root / "manuscript").rglob("*.md"):
        if pattern.search(path.read_text(encoding="utf-8", errors="replace")):
            return True
    return False


def format_entry(entry_type: str, key: str, fields: dict) -> str:
    ordered = [name for name in FIELD_ORDER if name in fields]
    ordered += sorted(name for name in fields if name not in FIELD_ORDER and name not in ("sourceid", "metadatasource"))
    ordered += [name for name in ("sourceid", "metadatasource") if name in fields]
    lines = [f"@{entry_type}{{{key},"] + [f"  {name} = {{{fields[name]}}}," for name in ordered] + ["}"]
    return "\n".join(lines)


def bib_upsert(root: Path, source_id: str, entry_type: str | None, values: dict, key: str | None = None) -> tuple:
    """Create or update the entry whose sourceid is source_id. Returns (key, note)."""
    path = root / "references" / "bibliography.bib"
    text = path.read_text(encoding="utf-8") if path.is_file() else BIB_HEADER
    existing = None
    taken = set()
    for start, end, kind, entry_key, body in entries(text):
        fields = fields_of(body)
        if fields.get("sourceid") == source_id:
            existing = (start, end, kind, entry_key, fields)
        else:
            taken.add(entry_key)
    fields = dict(existing[4]) if existing else {}
    for name, value in values.items():
        if value in (None, ""):
            continue
        fields[name] = value if name in VERBATIM else str(value).translate(TEX)
    fields["sourceid"] = source_id
    note = ""
    authors = [a.strip() for a in values.get("author", "").split(" and ")] if values.get("author") else []
    proposed = key or make_key(authors, str(values.get("year") or ""), str(values.get("title") or ""), source_id, taken)
    if existing:
        current = existing[3]
        if key is None and current != source_id:
            proposed = current
        elif proposed != current and cited(root, current):
            note = f"kept the key {current} because the manuscript cites it"
            proposed = current
    if proposed in taken:
        raise ValueError(f"the citation key {proposed!r} is already used by another source")
    entry = format_entry((entry_type or (existing[2] if existing else "misc")).lower(), proposed, fields)
    if existing:
        text = text[:existing[0]] + entry + text[existing[1]:]
    else:
        text = text.rstrip("\n") + "\n\n" + entry + "\n"
    write_text_atomic(path, text if text.endswith("\n") else text + "\n")
    return proposed, note
