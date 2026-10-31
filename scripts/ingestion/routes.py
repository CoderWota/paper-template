"""Conversion routes: the official MinerU MCP, local Pandoc, and direct reading.

Each route turns one archived original into a folder of raw output. MinerU runs remotely through
the official MCP. No route falls back to another: a failure is reported, never retried elsewhere.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import re
import shutil
import subprocess
import urllib.parse
from pathlib import Path

from .common import Redactor, sha256_file, write_json_atomic
from mcp_bridge import MCPError, call_tool, tool_data

MAX_UPLOAD = 200 << 20

KINDS = {
    ".pdf": "pdf",
    **{ext: "image" for ext in (".png", ".jpg", ".jpeg", ".jp2", ".webp", ".gif", ".bmp")},
    ".docx": "word", ".pptx": "slides", ".xlsx": "spreadsheet",
    ".doc": "legacy-office", ".ppt": "legacy-office", ".xls": "legacy-office",
    ".odt": "opendocument", ".odp": "opendocument", ".ods": "opendocument",
    ".rtf": "rtf", ".epub": "epub",
    ".html": "html", ".htm": "html", ".mhtml": "html", ".mht": "html",
    ".csv": "table", ".tsv": "table",
    ".md": "markdown", ".markdown": "markdown", ".txt": "text", ".tex": "latex",
}
CLOUD_KINDS = frozenset({"pdf", "image", "word", "slides", "spreadsheet", "legacy-office"})
DIRECT_KINDS = frozenset({"markdown", "text"})
# The researcher's own editable manuscript is read locally by Pandoc.
PANDOC_KINDS = {"word": "docx+citations", "opendocument": "odt", "latex": "latex"}
PANDOC_OUTPUT = "markdown-simple_tables-multiline_tables-grid_tables"
ADOPT_FILTER = Path(__file__).resolve().parent / "adopt-conventions.lua"
VERIFIED = frozenset({
    ("direct", "markdown", ""), ("direct", "text", ""),
    ("pandoc", "word", ""), ("pandoc", "latex", ""), ("pandoc", "opendocument", ""),
})


class ConversionError(Exception):
    """A failure that affects one document."""

    def __init__(self, message: str, code: str = "failed"):
        super().__init__(message)
        self.code = code


class BatchStop(Exception):
    """A failure that affects every remaining document, such as a rejected token or an exhausted quota."""

    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code


def kind_of(path: Path) -> str:
    return KINDS.get(path.suffix.lower(), "unknown")


def handler_for(kind: str, route: str) -> str | None:
    """The route that converts this kind under the confirmed processing route, or None."""
    if kind in DIRECT_KINDS:
        return "direct"
    if route == "pandoc":
        return "pandoc" if kind in PANDOC_KINDS else None
    if route == "cloud" and kind in CLOUD_KINDS:
        return "cloud"
    return None


def unsupported_reason(kind: str, route: str) -> str:
    if route == "local":
        return "this import record uses the removed local MinerU route; start a new import through the official cloud MCP only for reference material and with --to references"
    if route == "pandoc" and kind in ("pdf", "image"):
        return "a PDF or image is not supported by Pandoc; MinerU cloud processing is limited to reference materials"
    if route == "pandoc" and kind == "legacy-office":
        return "Pandoc does not read old Word files (.doc); a copy saved as .docx can be imported"
    if kind == "unknown":
        return "this file type is not supported"
    return f"this file type is not supported by the {route} route"


def tail(text: str, lines: int = 3) -> str:
    kept = [line.strip() for line in text.splitlines() if line.strip() and "it/s]" not in line and "s/it]" not in line]
    return " ".join(kept[-lines:])[-600:]


class PandocRoute:
    """The researcher's own editable manuscript (Word, OpenDocument, or LaTeX), read by Pandoc on this computer.

    Comments and tracked changes are kept as Pandoc marks them by default (track_changes "all"), so that adoption
    stops on them; "accept" or "reject" applies the researcher's choice. Citation fields from Zotero, Mendeley, and
    EndNote become Pandoc citations with their metadata. adopt-conventions.lua applies the workspace conventions.
    """

    name = "pandoc"

    def __init__(self, executable: str, track_changes: str = "all"):
        self.executable, self.track_changes = executable, track_changes

    def version(self) -> str:
        completed = subprocess.run([self.executable, "--version"], capture_output=True, text=True)
        return (completed.stdout.splitlines() or [""])[0].replace("pandoc", "").strip()

    def settings(self, kind: str) -> dict:
        return {"route": "pandoc", "converter": "pandoc", "version": self.version(), "reader": PANDOC_KINDS.get(kind),
                "writer": PANDOC_OUTPUT, "track_changes": self.track_changes if kind == "word" else None,
                "filter": "scripts/ingestion/adopt-conventions.lua"}

    def convert(self, original: Path, work: Path, kind: str, source_folder: Path | None = None) -> tuple[Path, list[str]]:
        raw = work / "raw"
        raw.mkdir(parents=True, exist_ok=True)
        command = [self.executable, str(original), "-f", PANDOC_KINDS[kind], "-t", PANDOC_OUTPUT, "-s", "--wrap=none",
                   "--extract-media=images", "--lua-filter", str(ADOPT_FILTER), "-M", f"adopt-source={kind}", "-o", "markdown.md"]
        if kind == "word":
            command.append(f"--track-changes={self.track_changes}")
        completed = subprocess.run(command, cwd=raw, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
        if completed.returncode != 0:
            raise ConversionError(f"Pandoc could not read the file: {tail(completed.stderr)}")
        notes = [line.strip() for line in completed.stderr.splitlines() if line.strip()][:5]
        text = (raw / "markdown.md").read_text(encoding="utf-8")
        if kind == "latex" and source_folder is not None:
            text = DirectRoute.copy_images(text, source_folder, raw / "images")
            (raw / "markdown.md").write_text(text, encoding="utf-8")
        return raw, notes


class CloudRoute:
    """The official MinerU MCP (mineru.net). A receipt per file and setting prevents a second upload of the same file."""

    name = "cloud"

    def __init__(self, token: str, language: str = "ch", is_ocr: bool = False, timeout: float = 3600.0, *, root: Path):
        self.root, self.language, self.is_ocr, self.timeout = root, language, is_ocr, timeout
        self.mode = "precision" if token else "flash"
        self.redact = Redactor([token] if token else [])

    def settings(self, kind: str) -> dict:
        return {"route": "cloud", "service": "mineru.net", "transport": "mcp", "mcp_server": "mineru", "mode": self.mode,
                "language": self.language, "is_ocr": self.is_ocr, "output_contract": "official-mcp-markdown"}

    def convert(self, original: Path, work: Path, kind: str) -> tuple[Path, list[str]]:
        from .pdf import page_count
        page_limit, size_limit = (200, MAX_UPLOAD) if self.mode == "precision" else (20, 10 << 20)
        pages = page_count(original) if kind == "pdf" else None
        if original.stat().st_size > size_limit or (pages or 0) > page_limit:
            raise ConversionError(f"the file is above the {self.mode} mode limit of {page_limit} pages or {size_limit >> 20} MB, so it was not sent", "mcp-limit")
        digest = sha256_file(original)
        key = hashlib.sha256((digest + json.dumps(self.settings(kind), sort_keys=True)).encode()).hexdigest()
        cache = self.root / ".local" / "mcp" / "imports" / key
        receipt, cached = cache / "receipt.json", cache / "markdown.md"
        state = json.loads(receipt.read_text(encoding="utf-8")) if receipt.is_file() else {}
        if state.get("status") == "submitted":
            raise ConversionError("an earlier upload has no recorded outcome; check its receipt in .local/mcp/imports before the file is sent again", "mcp-unresolved")
        if state.get("status") == "complete" and not cached.is_file():
            raise ConversionError("the Markdown saved for an earlier upload is missing; restore it or remove its receipt before converting again", "mcp-unresolved")
        if state.get("status") != "complete":
            cache.mkdir(parents=True, exist_ok=True)
            attempts = state.get("attempts", 0) + 1
            write_json_atomic(receipt, {"status": "submitted", "attempts": attempts, "sha256": digest, "settings": self.settings(kind)})
            try:
                text = self.parse(original, cache)
            except ConversionError:
                write_json_atomic(receipt, {"status": "failed", "attempts": attempts, "sha256": digest, "settings": self.settings(kind)})
                raise
            cached.write_text(text, encoding="utf-8")
            write_json_atomic(receipt, {"status": "complete", "attempts": attempts, "sha256": digest, "settings": self.settings(kind)})
        raw = work / "raw"
        raw.mkdir(parents=True, exist_ok=True)
        shutil.copy2(cached, raw / "markdown.md")
        notes = ["The official MinerU MCP returns Markdown only. Page records and images are not kept, so check coverage and figures against the original."]
        if self.mode == "flash":
            notes.append("No MINERU_API_TOKEN is set, so MinerU flash mode was used: Markdown only, at most 20 pages and 10 MB per file.")
        return raw, notes

    def call_mcp(self, arguments: dict):
        try:
            return tool_data(call_tool(self.root, "mineru", "parse_documents", arguments, timeout=self.timeout))
        except MCPError as error:
            raise BatchStop(self.redact(str(error)), "mcp-unresolved") from None

    def parse(self, original: Path, cache: Path) -> str:
        # The service sees a neutral file name, not the researcher's file name; the copy is removed after the call.
        staged = cache / f"document{original.suffix.lower()}"
        try:
            shutil.copy2(original, staged)
            arguments = {"file_sources": [str(staged.resolve())], "language": self.language, "output_dir": str(cache.resolve())}
            if self.is_ocr:
                arguments["enable_ocr"] = True
            response = self.call_mcp(arguments)
        except OSError as error:
            raise ConversionError(f"the file could not be copied for upload: {error}", "write") from None
        finally:
            with contextlib.suppress(OSError):
                staged.unlink()
        results = response.get("results") if isinstance(response, dict) else None
        entry = results[0] if isinstance(results, list) and len(results) == 1 and isinstance(results[0], dict) else {}
        if entry.get("status") != "success":
            raise ConversionError(f"MinerU could not convert the file: {self.redact(str(entry.get('error') or 'no result was returned'))}", "mcp-service")
        if "content" in entry and not entry.get("truncated"):
            text = entry["content"]
        else:
            # Long replies are cut short. The complete Markdown is the copy that the server saved in the job folder.
            saved = Path(entry.get("extract_path") or "").resolve()
            if cache.resolve() not in saved.parents or not saved.is_file():
                raise ConversionError("MinerU returned only part of the Markdown and no complete copy; the document was not converted", "mcp-incomplete")
            text = saved.read_text(encoding="utf-8")
        if not isinstance(text, str) or not text.strip():
            raise ConversionError("MinerU returned no Markdown", "no-markdown")
        return text


class DirectRoute:
    """Markdown and plain text are read directly; no parser is involved."""

    name = "direct"

    def settings(self, kind: str) -> dict:
        return {"route": "direct", "converter": "none", "reader": "scripts/ingest.py"}

    def convert(self, original: Path, work: Path, kind: str, source_folder: Path | None = None) -> tuple[Path, list[str]]:
        raw = work / "raw"
        raw.mkdir(parents=True, exist_ok=True)
        notes = []
        data = original.read_bytes()
        try:
            text = data.decode("utf-8-sig")
        except UnicodeDecodeError:
            text = data.decode("utf-8", errors="replace")
            notes.append("the file is not valid UTF-8; unreadable characters were replaced")
        if kind == "markdown" and source_folder is not None:
            text = self.copy_images(text, source_folder, raw / "images")
        with open(raw / "markdown.md", "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        return raw, notes

    @staticmethod
    def copy_images(text: str, folder: Path, images: Path) -> str:
        """Copy images that the Markdown links from its own folder, and point the links at the copies."""
        used: dict[str, str] = {}

        def replace(match: re.Match) -> str:
            target = urllib.parse.unquote(match.group(2))
            if re.match(r"^[a-z][a-z0-9+.-]*:|^#|^/", target, re.I):
                return match.group(0)
            source = (folder / target).resolve()
            try:
                source.relative_to(folder.resolve())
            except ValueError:
                return match.group(0)
            if not source.is_file():
                return match.group(0)
            if target not in used:
                name = f"{len(used) + 1:03d}-{source.name}"
                images.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, images / name)
                used[target] = f"images/{name}"
            return f"{match.group(1)}{used[target]}{match.group(3)}"

        return re.sub(r"(!\[[^\]]*\]\()<?([^)\s>]+)>?((?:\s+\"[^\"]*\")?\))", replace, text)
