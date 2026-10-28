"""Turn raw parser output into the workspace layout and check what was actually extracted.

The checks compare the Markdown with the parser's own page and block records: missing pages,
pages without text, text that the parser kept but left out of the Markdown, image links, and
math delimiters. A successful parser run is never taken as proof of a complete extraction.
"""

from __future__ import annotations

import re
import shutil
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

from . import pdf
from .common import read_json
from .routes import ConversionError

# Blocks whose text is not plain prose; their Markdown form differs too much to match.
NOT_PROSE = ("table", "equation", "image", "chart", "figure", "code", "algorithm", "seal", "formula")
# Page furniture that MinerU leaves out of the Markdown on purpose.
RUNNING = ("header", "footer", "page_number", "discarded")
SHORT_RUNNING = 60
PLACEHOLDERS = {"", "untitled", "unknown", "anonymous", "unspecified", "none", "null"}
# Commands that need a LaTeX preamble or a package that GitHub's math renderer does not load.
UNSUPPORTED_MATH = ("\\usepackage", "\\documentclass", "\\begin{document}", "\\newcommand", "\\renewcommand",
                    "\\def\\", "\\DeclareMathOperator", "\\bm{", "\\mathbbm")
DOI = re.compile(r"\b10\.\d{4,9}/[^\s\"<>()\[\]{}]+")
LINK = re.compile(r"(!?\[[^\]]*\]\()<?([^)\s>]+)>?((?:\s+\"[^\"]*\")?\))")
IMG_SRC = re.compile(r"(<img\b[^>]*?\bsrc=[\"'])([^\"']+)([\"'])", re.I)
INLINE_MATH = re.compile(r"(?<![\\$])\$(?!\$)[^$\n]+?(?<![\\$])\$(?!\$)")
REVIEW = "review"
PARTIAL = "partial"
INFO = "info"


@dataclass
class Extraction:
    text: str
    assets: list = field(default_factory=list)
    native: list = field(default_factory=list)
    coverage: dict = field(default_factory=dict)
    checks: dict = field(default_factory=dict)
    warnings: list = field(default_factory=list)
    hints: dict = field(default_factory=dict)
    parser: dict = field(default_factory=dict)

    def warn(self, code: str, message: str, level: str = REVIEW, details=None) -> None:
        entry = {"code": code, "level": level, "message": message}
        if details:
            entry["details"] = details
        self.warnings.append(entry)

    @property
    def status(self) -> str:
        levels = {warning["level"] for warning in self.warnings}
        if PARTIAL in levels:
            return "partial"
        return "needs-review" if REVIEW in levels else "complete"


def descend(raw: Path) -> Path:
    """Some archives wrap everything in one folder; use that folder as the root."""
    entries = [entry for entry in raw.iterdir() if not entry.name.startswith(".")]
    if len(entries) == 1 and entries[0].is_dir() and entries[0].name != "images":
        return descend(entries[0])
    return raw


def find_markdown(raw: Path) -> Path:
    for name in ("markdown.md", "full.md"):
        if (raw / name).is_file():
            return raw / name
    candidates = [path for path in raw.iterdir() if path.is_file() and path.suffix.lower() == ".md"]
    if len(candidates) == 1:
        return candidates[0]
    raise ConversionError("the parser output contains no Markdown file", "no-markdown")


def matchable(text: str) -> str:
    """Lowercase letters, digits, and single spaces, for comparing parser blocks with the Markdown."""
    value = unicodedata.normalize("NFKC", text).lower()
    value = re.sub(r"\\(.)", r"\1", value)
    value = re.sub(r"[\W_]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def span_text(span) -> str:
    if isinstance(span, str):
        return span
    if isinstance(span, dict):
        content = span.get("content")
        if isinstance(content, (str, list, dict)):
            return span_text(content)
        return " ".join(span_text(child) for child in span.get("blocks") or [])
    if isinstance(span, list):
        return " ".join(span_text(item) for item in span)
    return ""


def legacy_text(block: dict) -> str:
    """Text of a block in the older pipeline layout (lines of spans, nested blocks)."""
    parts = []
    for line in block.get("lines") or []:
        for item in line.get("spans") or []:
            if isinstance(item.get("content"), str):
                parts.append(item["content"])
    for child in block.get("blocks") or []:
        parts.append(legacy_text(child))
    return " ".join(part for part in parts if part)


def load_layout(raw: Path) -> dict | None:
    for pattern in ("middle_json.json", "layout.json", "*middle*.json"):
        for candidate in sorted(raw.rglob(pattern)):
            data = read_json(candidate)
            if isinstance(data, dict) and (data.get("schema") == "docvortex.middle" or "pdf_info" in data):
                return data
    return None


def pages_of(layout: dict) -> list:
    """(page index, [(block type, text, discarded)]) for every page the parser processed."""
    pages = []
    if layout.get("schema") == "docvortex.middle":
        for page in layout.get("pages") or []:
            blocks = [(str(block.get("type", "")), span_text(block), False) for block in page.get("blocks") or []]
            pages.append((page.get("page_idx"), blocks))
    else:
        for page in layout.get("pdf_info") or []:
            blocks = [(str(block.get("type", "")), legacy_text(block), False) for block in page.get("para_blocks") or []]
            blocks += [(str(block.get("type", "discarded")), legacy_text(block), True) for block in page.get("discarded_blocks") or []]
            pages.append((page.get("page_idx"), blocks))
    return pages


def rewrite_links(text: str, mapping: dict) -> str:
    def target(value: str) -> str | None:
        key = unquote(value)
        key = key[2:] if key.startswith("./") else key
        return mapping.get(key)

    def markdown(match: re.Match) -> str:
        new = target(match.group(2))
        return f"{match.group(1)}{new}{match.group(3)}" if new else match.group(0)

    def html(match: re.Match) -> str:
        new = target(match.group(2))
        return f"{match.group(1)}{new}{match.group(3)}" if new else match.group(0)

    return IMG_SRC.sub(html, LINK.sub(markdown, text))


def local_targets(text: str) -> list:
    found = [match.group(2) for match in LINK.finditer(text)] + [match.group(2) for match in IMG_SRC.finditer(text)]
    return [value for value in found if not re.match(r"^([a-z][a-z0-9+.-]*:|#)", value, re.I)]


def split_code(text: str) -> list:
    """[(is_code, text)] chunks; joining their texts with newlines gives the input back."""
    chunks, buffer, in_code, fence = [], [], False, ""
    for line in text.split("\n"):
        marker = line.strip()[:3] if re.match(r"^(```|~~~)", line.strip()) else ""
        if not in_code and marker:
            if buffer:
                chunks.append((False, "\n".join(buffer)))
            buffer, in_code, fence = [line], True, marker
            continue
        buffer.append(line)
        if in_code and marker == fence and len(buffer) > 1:
            chunks.append((True, "\n".join(buffer)))
            buffer, in_code = [], False
    if buffer:
        chunks.append((in_code, "\n".join(buffer)))
    return chunks


def normalize_math(text: str) -> tuple:
    """Apply the workspace math conventions to derived Markdown without changing any formula.

    Display math becomes $$ on its own lines with no blank lines inside and blank lines around it;
    \\( \\) and \\[ \\] become $ and $$. Code is left alone. Returns the text and its statistics.
    """
    stats = {"inline": 0, "display": 0, "normalized": 0, "unbalanced_lines": [], "unsupported": []}
    chunks = []
    for is_code, chunk in split_code(text):
        if not is_code:
            chunk, count = re.subn(r"\\\[(.+?)\\\]", lambda m: f"\n$$\n{m.group(1).strip()}\n$$\n", chunk, flags=re.S)
            stats["normalized"] += count
            chunk, count = re.subn(r"\\\((.+?)\\\)", lambda m: f"${m.group(1).strip()}$", chunk)
            stats["normalized"] += count
            chunk = display_blocks(chunk, stats)
        chunks.append((is_code, chunk))
    result = "\n".join(chunk for _, chunk in chunks)
    number = 0
    for is_code, chunk in split_code(result):
        in_display = False
        for line in chunk.split("\n"):
            number += 1
            if is_code:
                continue
            if line.strip() == "$$":
                in_display = not in_display
                continue
            math = line if in_display else " ".join(INLINE_MATH.findall(line))
            if not in_display:
                stats["inline"] += len(INLINE_MATH.findall(line))
                if len(re.findall(r"(?<![\\$])\$(?!\$)", line)) % 2:
                    stats["unbalanced_lines"].append(number)
            for command in UNSUPPORTED_MATH:
                if command in math:
                    stats["unsupported"].append({"line": number, "command": command})
    return result, stats


def display_blocks(chunk: str, stats: dict) -> str:
    """Put $$ on its own lines, drop blank lines inside display math, and surround it with blank lines."""
    out, in_display = [], False

    def emit_open() -> None:
        if out and out[-1].strip():
            out.append("")
            stats["normalized"] += 1
        out.append("$$")
        stats["display"] += 1

    for line in chunk.split("\n"):
        stripped = line.strip()
        if in_display:
            if not stripped:
                stats["normalized"] += 1
                continue
            if stripped == "$$" or stripped.endswith("$$"):
                body = stripped[:-2].rstrip()
                if body:
                    out.append(body)
                    stats["normalized"] += 1
                out.append("$$")
                in_display = False
                continue
            out.append(line)
            continue
        single = re.match(r"^\$\$(.+?)\$\$$", stripped)
        if single:
            emit_open()
            out.extend([single.group(1).strip(), "$$"])
            stats["normalized"] += 1
            continue
        if stripped.startswith("$$"):
            emit_open()
            rest = stripped[2:].strip()
            if rest:
                out.append(rest)
                stats["normalized"] += 1
            in_display = True
            continue
        if out and out[-1] == "$$" and stripped:
            out.append("")
            stats["normalized"] += 1
        out.append(line)
    if in_display:
        # An unclosed block would swallow the rest of the document; close it and flag the line.
        out.append("$$")
        stats["unclosed_display"] = stats.get("unclosed_display", 0) + 1
    return "\n".join(out)


def build(raw: Path, *, kind: str, original: Path, document: Path, asset_dir: Path, asset_link: str,
          asset_prefix: str = "", native_dir: Path | None = None, details: str = "the README of this folder") -> Extraction:
    """Write document.md, the assets, and optionally the native outputs, then check them.

    details names the place that explains an incomplete extraction, for the note at the top of the text.
    """
    raw = descend(raw)
    source = find_markdown(raw)
    text = source.read_text(encoding="utf-8", errors="replace")
    mapping, assets = {}, []
    images = raw / "images"
    if images.is_dir():
        for path in sorted(p for p in images.rglob("*") if p.is_file()):
            relative = path.relative_to(images).as_posix()
            name = asset_prefix + relative.replace("/", "-")
            asset_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, asset_dir / name)
            mapping[f"images/{relative}"] = asset_link + name
            assets.append(name)
    text, math = normalize_math(rewrite_links(text, mapping))
    text = text.rstrip("\n") + "\n"
    native = []
    if native_dir is not None:
        for path in sorted(p for p in raw.rglob("*") if p.is_file()):
            relative = path.relative_to(raw)
            # The service returns a copy of the original (for example "<id>_origin.docx"); the archive already holds it.
            if relative.parts[0] == "images" or re.search(r"_origin\.[A-Za-z0-9]+$", path.name):
                continue
            destination = native_dir.joinpath(*relative.parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
            native.append(relative.as_posix())
    result = Extraction(text=text, assets=assets, native=native)
    layout = load_layout(raw)
    result.parser = parser_info(layout) if layout else {}
    check_layout(result, layout, kind, original)
    note = coverage_note(result.coverage, details)
    if note:
        result.text = note + result.text
        shift = note.count("\n")
        math["unbalanced_lines"] = [number + shift for number in math["unbalanced_lines"]]
        for entry in math["unsupported"]:
            entry["line"] += shift
    document.parent.mkdir(parents=True, exist_ok=True)
    with open(document, "w", encoding="utf-8", newline="\n") as stream:
        stream.write(result.text)
    check_links(result, document, image_roles(layout) if layout else {}, asset_prefix)
    check_math(result, math)
    return result


def parser_info(layout: dict) -> dict:
    """The parser version that wrote the output, as the output itself states it.

    A cloud service reports its own version only here, so provenance records it from the result.
    """
    if layout.get("schema") == "docvortex.middle":
        producer = (layout.get("metadata") or {}).get("producer") or {}
        mineru = (layout.get("extensions") or {}).get("mineru") or {}
        parser_details = {"name": producer.get("name"), "version": producer.get("version"), "tier": mineru.get("tier")}
    else:
        parser_details = {"name": "mineru", "version": layout.get("_version_name"), "backend": layout.get("_backend")}
    return {key: value for key, value in parser_details.items() if value}


def coverage_note(coverage: dict, details: str) -> str:
    """A note at the top of an incomplete extraction, so that the text itself shows that it is incomplete.

    The workspace adds it and says so; it holds no link, because the text is checked before the README exists.
    """
    if coverage.get("status") == "partial":
        missing, expected = coverage.get("missing_pages") or [], coverage.get("expected")
        what = (f"pages {span_list(missing)} of {expected} were not converted" if missing and expected
                else "the parser converted only part of the document")
    elif coverage.get("status") == "unknown" and coverage.get("unit") == "page":
        what = "the page coverage is unknown, so text may be missing"
    else:
        return ""
    return (f"> [!WARNING]\n> Incomplete extraction, noted by the workspace: {what}. "
            f"This note is not part of the document; {details} has the details.\n\n")


def image_roles(layout: dict) -> dict:
    """{image file name: (block type, transcribed)} from the parser's records.

    MinerU keeps a picture of every table and formula it transcribes; such a picture is not linked
    from the Markdown because the text holds its content. Any other unlinked picture may be lost content.
    """
    roles = {}

    def visit(node, parent: str) -> None:
        if isinstance(node, dict):
            kind = str(node.get("type") or parent)
            path = node.get("image_path")
            if isinstance(path, str) and path:
                content = span_text(node.get("content")) + str(node.get("html") or "") + str(node.get("latex") or "")
                roles[Path(path).name] = (kind if kind not in ("image", "") else parent or kind, bool(content.strip()))
            for value in node.values():
                visit(value, kind)
        elif isinstance(node, list):
            for value in node:
                visit(value, parent)

    visit(layout.get("pages") or layout.get("pdf_info") or [], "")
    return roles


def check_layout(result: Extraction, layout: dict | None, kind: str, original: Path) -> None:
    counted = pdf.page_count(original) if kind == "pdf" else None
    if layout is None:
        if kind in ("pdf", "image"):
            result.coverage = {"unit": "page", "expected": counted, "expected_from": "file structure" if counted else None,
                               "processed": None, "status": "unknown"}
            result.warn("coverage-unknown", "the parser output has no page records, so page coverage is unknown")
        else:
            result.coverage = {"unit": "document", "status": "unknown"}
        return
    pages = pages_of(layout)
    document = (layout.get("metadata") or {}).get("document") or {}
    if kind == "pdf":
        expected, expected_from = None, None
        if document.get("page_count_kind") == "physical" and isinstance(document.get("page_count"), int):
            expected, expected_from = document["page_count"], "parser"
        if expected is None and counted:
            expected, expected_from = counted, "file structure"
        elif expected and counted and counted != expected:
            result.warn("page-count-mismatch", f"the parser counted {expected} pages, the file structure {counted}")
        processed = sorted({index for index, _ in pages if isinstance(index, int)})
        missing = [number + 1 for number in range(expected or 0) if number not in processed]
        result.coverage = {"unit": "page", "numbering": "PDF page order, counted from 1; not printed page labels",
                           "expected": expected, "expected_from": expected_from, "processed": len(processed),
                           "missing_pages": missing, "status": "unknown" if expected is None else ("partial" if missing else "complete")}
        if missing:
            result.warn("missing-pages", f"{len(missing)} of {expected} pages were not converted: {span_list(missing)}", PARTIAL, missing)
        elif expected is None:
            result.warn("coverage-unknown", "the total page count is unknown, so completeness cannot be checked")
    else:
        full = layout.get("is_full_document")
        status = "complete" if full is True else "partial" if full is False else "unknown"
        result.coverage = {"unit": "document", "is_full_document": full, "status": status}
        if full is False:
            result.warn("missing-pages", "the parser reports that it converted only part of the document", PARTIAL)
        elif full is not True:
            result.warn("coverage-unknown", "the parser did not report whether it converted the full document, so coverage is unknown")
    empty = [index + 1 for index, blocks in pages if isinstance(index, int) and not any(
        (matchable(text) and not running(kind, discarded)) or any(word in kind.lower() for word in NOT_PROSE)
        for kind, text, discarded in blocks)]
    if empty and kind in ("pdf", "image"):
        result.coverage["pages_without_text"] = empty
        result.warn("pages-without-text", f"no text was extracted from page(s) {span_list(empty)}; scanned pages need a tier that reads images (OCR)", REVIEW, empty)
    check_omissions(result, pages)
    result.hints = hints(layout, pages, result.text)


def running(kind: str, discarded: bool) -> bool:
    return discarded or any(word in kind.lower() for word in RUNNING)


def check_omissions(result: Extraction, pages: list) -> None:
    """Find prose that the parser recorded but the Markdown lacks, apart from running heads.

    A running head repeats on several pages, or is a short header or footer. A long, unique passage
    that the parser classified as a header is reported, because that is how content gets lost.
    """
    markdown = matchable(result.text)
    missing = []
    for index, blocks in pages:
        for kind, text, discarded in blocks:
            value = matchable(text)
            if len(value) < 20 or any(word in kind.lower() for word in NOT_PROSE):
                continue
            if value[:60] in markdown:
                continue
            missing.append((index, kind, value, discarded))
    repeats = Counter(re.sub(r"\d+", "#", value) for _, _, value, _ in missing)
    unique = [item for item in missing if repeats[re.sub(r"\d+", "#", item[2])] < 2
              and not (running(item[1], item[3]) and len(item[2]) < SHORT_RUNNING)]
    result.checks["omitted_text"] = {"running_heads": len(missing) - len(unique), "unique_passages": len(unique),
                                     "unique_characters": sum(len(value) for _, _, value, _ in unique)}
    if unique:
        pages_hit = sorted({index + 1 for index, _, _, _ in unique if isinstance(index, int)})
        types = sorted({kind for _, kind, _, _ in unique})
        result.warn("omitted-text", f"{len(unique)} passage(s) on page(s) {span_list(pages_hit)} are in the parser output but not in the Markdown "
                    f"(parser block types: {', '.join(types)}); they may be lost content", REVIEW,
                    [{"page": index + 1 if isinstance(index, int) else None, "type": kind, "start": value[:80]} for index, kind, value, _ in unique[:20]])


def hints(layout: dict, pages: list, text: str) -> dict:
    """Metadata clues for the agent. They come from the file and are not verified."""
    document = (layout.get("metadata") or {}).get("document") or {}
    found: dict = {}
    title = str(document.get("title") or "").strip()
    if title.lower() not in PLACEHOLDERS:
        found["embedded_title"] = title
    authors = [str(a).strip() for a in document.get("authors") or [] if str(a).strip().lower() not in PLACEHOLDERS]
    if authors:
        found["embedded_authors"] = authors
    for _, blocks in pages[:1]:
        for kind, value, _ in blocks:
            if kind in ("doc_title", "title") and value.strip():
                found["first_page_title"] = value.strip()[:300]
                break
    early = " ".join(value for _, blocks in pages[:2] for _, value, _ in blocks) + " " + text[:5000]
    dois = []
    for match in DOI.finditer(early):
        value = match.group(0).rstrip(".,;:")
        if value.lower() not in [d.lower() for d in dois]:
            dois.append(value)
    if dois:
        found["doi_candidates"] = dois[:5]
    return found


def check_links(result: Extraction, document: Path, roles: dict, asset_prefix: str = "") -> None:
    broken = []
    for value in local_targets(result.text):
        if not (document.parent / unquote(value)).is_file():
            broken.append(value)
    linked = set(unquote(value) for value in local_targets(result.text))
    unlinked = [name for name in result.assets if not any(target.endswith(name) for target in linked)]
    pictures, unexplained = [], []
    for name in unlinked:
        role, transcribed = roles.get(name[len(asset_prefix):], ("", False))
        (pictures if transcribed and ("table" in role or "equation" in role) else unexplained).append(name)
    result.checks["links"] = {"local": len(linked), "broken": broken, "pictures_of_transcribed_content": pictures,
                              "unreferenced_assets": unexplained}
    if broken:
        result.warn("broken-links", f"{len(broken)} image or file link(s) in the Markdown do not resolve", REVIEW, broken[:20])
    if pictures:
        result.warn("transcription-pictures", f"the image folder keeps {len(pictures)} picture(s) of tables or formulas that the text transcribes; use them to check the transcription", INFO)
    if unexplained:
        result.warn("unreferenced-images", f"{len(unexplained)} extracted image(s) are not linked from the text; they may hold content that the text lacks",
                    REVIEW, unexplained[:20])


def check_math(result: Extraction, math: dict) -> None:
    result.checks["math"] = math
    formulas = math["inline"] + math["display"]
    if formulas:
        result.warn("formulas-unverified", f"{formulas} formula(s) were transcribed by the parser and are not checked against the original", INFO)
    if math["unbalanced_lines"]:
        result.warn("unbalanced-dollar", f"{len(math['unbalanced_lines'])} line(s) have an unpaired $ sign (a broken formula or a currency sign)",
                    REVIEW, math["unbalanced_lines"][:20])
    if math.get("unclosed_display"):
        result.warn("unclosed-formula", f"{math['unclosed_display']} display formula(s) had no closing $$; one was added at the end of the section")
    if math["unsupported"]:
        result.warn("unsupported-math", f"{len(math['unsupported'])} formula command(s) will not render on GitHub", REVIEW, math["unsupported"][:20])


def span_list(numbers: list) -> str:
    """1, 2, 3, 5 -> "1-3, 5"."""
    ranges, start, previous = [], None, None
    for number in sorted(numbers):
        if start is None:
            start = previous = number
        elif number == previous + 1:
            previous = number
        else:
            ranges.append(f"{start}-{previous}" if previous != start else str(start))
            start = previous = number
    if start is not None:
        ranges.append(f"{start}-{previous}" if previous != start else str(start))
    return ", ".join(ranges)
