"""Conversion routes: local MinerU (mineru-kit), the mineru.net precision API, and direct reading.

Each route turns one archived original into a folder of raw parser output (Markdown, images, and
parser JSON). No route falls back to another: a failure is reported, never retried elsewhere.
"""

from __future__ import annotations

import http.client
import json
import os
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

from .common import Redactor

TESTED_MINERU = "4.0.12"
OFFICIAL_API = "https://mineru.net"
TIERS = ("flash", "basic", "standard", "advanced")
OCR_MODES = ("auto", "txt", "ocr")
MAX_OUTPUT = 4 << 30
MAX_UPLOAD = 200 << 20
# mineru.net accepts 50 submitted files a minute; 20 files every 30 seconds stays below that.
CLOUD_BATCH = 20
CLOUD_PACE = 30.0

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
# Local MinerU reads these as whole documents with its flash tier.
LOCAL_WHOLE_DOCUMENT = frozenset({"word", "slides", "spreadsheet", "opendocument", "rtf", "epub", "html", "table"})
CLOUD_KINDS = frozenset({"pdf", "image", "word", "slides", "spreadsheet", "legacy-office"})
DIRECT_KINDS = frozenset({"markdown", "text"})
# The researcher's own editable manuscript is read locally by Pandoc;
# references and review documents keep the confirmed MinerU routes.
PANDOC_KINDS = {"word": "docx+citations", "opendocument": "odt", "latex": "latex"}
PANDOC_OUTPUT = "markdown-simple_tables-multiline_tables-grid_tables"
ADOPT_FILTER = Path(__file__).resolve().parent / "adopt-conventions.lua"
# Previously observed (route, kind, tier or cloud model) combinations; see
# docs/capabilities.md. Other documented combinations remain flagged for review.
VERIFIED = frozenset({
    ("local", "pdf", "flash"), ("local", "pdf", "basic"), ("local", "word", "flash"),
    ("cloud", "pdf", "vlm"),
    ("direct", "markdown", ""), ("direct", "text", ""),
    ("pandoc", "word", ""), ("pandoc", "latex", ""), ("pandoc", "opendocument", ""),
})
MODELS_MISSING = re.compile(r"Model repo \S+ is not ready|quality_tier_unavailable", re.I)


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
    if route == "local" and (kind in ("pdf", "image") or kind in LOCAL_WHOLE_DOCUMENT):
        return "local"
    if route == "cloud" and kind in CLOUD_KINDS:
        return "cloud"
    return None


def unsupported_reason(kind: str, route: str) -> str:
    if route == "pandoc" and kind in ("pdf", "image"):
        return "a PDF or scanned manuscript is converted with MinerU (the local or cloud route), not with Pandoc"
    if route == "pandoc" and kind == "legacy-office":
        return "Pandoc does not read old Word files (.doc); a copy saved as .docx can be imported"
    if kind == "legacy-office" and route == "local":
        return "the local parser does not read old Office formats (.doc, .ppt, .xls); a copy saved as .docx, .pptx, or .xlsx can be imported"
    if kind == "unknown":
        return "this file type is not supported"
    return f"this file type is not supported by the {route} route"


def safe_extract(archive: Path, target: Path) -> None:
    """Unpack a parser archive, refusing absolute paths, parent references, and oversized content."""
    total = 0
    try:
        with zipfile.ZipFile(archive) as package:
            for info in package.infolist():
                name = info.filename.replace("\\", "/")
                parts = [part for part in name.split("/") if part not in ("", ".")]
                if name.startswith("/") or ".." in parts or (parts and re.match(r"^[A-Za-z]:$", parts[0])):
                    raise ConversionError(f"the parser output contains an unsafe path: {info.filename}")
                if not parts:
                    continue
                total += info.file_size
                if total > MAX_OUTPUT:
                    raise ConversionError("the parser output is larger than expected")
                destination = target.joinpath(*parts)
                if info.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                    continue
                destination.parent.mkdir(parents=True, exist_ok=True)
                with package.open(info) as source, open(destination, "wb") as out:
                    shutil.copyfileobj(source, out)
    except zipfile.BadZipFile as error:
        raise ConversionError(f"the parser output is not a valid archive: {error}") from error


def tail(text: str, lines: int = 3) -> str:
    kept = [line.strip() for line in text.splitlines() if line.strip() and "it/s]" not in line and "s/it]" not in line]
    return " ".join(kept[-lines:])[-600:]


class LocalRoute:
    """MinerU installed on this computer, in .tools/mineru/ or on the PATH."""

    name = "local"

    def __init__(self, root: Path, tier: str, ocr_mode: str = "auto", command: list[str] | None = None,
                 timeout: int = 7200, redact: Redactor | None = None):
        if tier not in TIERS:
            raise ValueError(f"unknown tier {tier!r}")
        if ocr_mode not in OCR_MODES:
            raise ValueError(f"unknown OCR mode {ocr_mode!r}")
        self.root, self.tier, self.ocr_mode, self.timeout = root, tier, ocr_mode, timeout
        self.command = command or self.locate(root)
        self.redact = redact or Redactor()
        self._version: str | None = None

    @staticmethod
    def locate(root: Path) -> list[str] | None:
        tool = root / ".tools" / "mineru"
        for candidate in (tool / "Scripts" / "mineru-kit.exe", tool / "bin" / "mineru-kit"):
            if candidate.is_file():
                return [str(candidate)]
        found = shutil.which("mineru-kit")
        return [found] if found else None

    def env(self) -> dict:
        cache = self.root / ".cache"
        return dict(
            os.environ,
            MINERU_HOME=str(cache / "mineru"),
            HF_HOME=str(cache / "huggingface"),
            MODELSCOPE_CACHE=str(cache / "modelscope"),
            # Missing models must fail, not start a large download that nobody agreed to.
            MINERU_MODEL_SOURCE="local",
            NO_COLOR="1",
            COLUMNS="400",  # keeps the parser's messages, and the file paths in them, on one line
            PYTHONIOENCODING="utf-8",
            PYTHONUTF8="1",
        )

    def ensure_config(self) -> None:
        """Keep MinerU's configuration and models inside the workspace's ignored .cache/ folder."""
        home = self.root / ".cache" / "mineru"
        config = home / "config.yaml"
        base = (home / "models").as_posix()
        home.mkdir(parents=True, exist_ok=True)
        text = config.read_text(encoding="utf-8") if config.is_file() else ""
        line = f"  base_dir: {base}"
        if re.search(r"(?m)^  base_dir: .*$", text):
            updated = re.sub(r"(?m)^  base_dir: .*$", lambda _: line, text)
        elif re.search(r"(?m)^model:\s*$", text):
            updated = re.sub(r"(?m)^model:\s*$", lambda _: "model:\n" + line, text, count=1)
        else:
            updated = text.rstrip("\n") + ("\n" if text else "") + "model:\n" + line + "\n"
        if updated != text:
            config.write_text(updated, encoding="utf-8")

    def run(self, arguments: list[str], timeout: int) -> subprocess.CompletedProcess:
        if not self.command:
            raise BatchStop("MinerU is not installed on this computer", "parser-missing")
        try:
            return subprocess.run(self.command + arguments, capture_output=True, text=True, encoding="utf-8",
                                  errors="replace", env=self.env(), timeout=timeout)
        except FileNotFoundError as error:
            raise BatchStop(f"MinerU could not be started: {error}", "parser-missing") from error

    def version(self) -> str:
        if self._version is None:
            result = self.run(["version", "--json"], timeout=300)
            try:
                self._version = str(json.loads(result.stdout)["mineru_version"])
            except (ValueError, KeyError, TypeError) as error:
                raise BatchStop(f"the MinerU version could not be read: {tail(result.stderr or result.stdout)}", "parser-missing") from error
            if not self._version.startswith("4."):
                raise BatchStop(f"MinerU {self._version} is installed; this workspace needs MinerU 4", "parser-version")
        return self._version

    def settings(self, kind: str) -> dict:
        settings = {"route": "local", "converter": "mineru", "entry_point": "mineru-kit parse", "version": self.version(),
                    "tier": "flash" if kind in LOCAL_WHOLE_DOCUMENT else self.tier}
        if kind in ("pdf", "image"):
            settings["ocr_mode"] = self.ocr_mode
        if kind == "pdf":
            settings["pages"] = "all"
        return settings

    def convert(self, original: Path, work: Path, kind: str) -> Path:
        self.ensure_config()
        settings = self.settings(kind)
        output = work / "parser-output"
        output.mkdir(parents=True, exist_ok=True)
        arguments = ["parse", str(original), "-o", str(output), "--format", "zip", "--tier", settings["tier"]]
        if "ocr_mode" in settings:
            arguments += ["--ocr-mode", settings["ocr_mode"]]
        if kind == "pdf":
            arguments += ["--pages", "all"]
        try:
            result = self.run(arguments, timeout=self.timeout)
        except subprocess.TimeoutExpired as error:
            raise ConversionError(f"the parser did not finish within {self.timeout} seconds", "timeout") from error
        messages = self.redact(result.stdout + "\n" + result.stderr).replace(str(original), original.name)
        if result.returncode != 0:
            if MODELS_MISSING.search(messages):
                raise BatchStop(f"the models for the {settings['tier']} tier are not installed", "models-missing")
            raise ConversionError(f"the parser stopped with exit status {result.returncode}: {tail(messages)}")
        archives = sorted(output.rglob("*.zip"))
        if len(archives) != 1:
            raise ConversionError(f"the parser wrote {len(archives)} result archives instead of one")
        raw = work / "raw"
        safe_extract(archives[0], raw)
        return raw


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


class _SameOriginRedirects(urllib.request.HTTPRedirectHandler):
    """Never forward the token to another origin through a redirect."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if origin(newurl) != origin(req.full_url):
            raise urllib.error.HTTPError(newurl, code, "redirect to another origin refused", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def origin(url: str) -> tuple:
    parts = urllib.parse.urlsplit(url)
    return parts.scheme, parts.hostname, parts.port or (443 if parts.scheme == "https" else 80)


def check_transfer_url(url: str) -> None:
    """Service uploads and downloads must use HTTPS."""
    scheme = urllib.parse.urlsplit(url).scheme
    if scheme != "https":
        raise ConversionError("the service returned an address that is not HTTPS", "unsafe-url")


class CloudRoute:
    """The mineru.net precision API (v4): signed upload, batch parsing, and a result archive per file."""

    name = "cloud"

    def __init__(self, token: str, model_version: str = "vlm", language: str = "ch", is_ocr: bool = False,
                 enable_formula: bool = True, enable_table: bool = True,
                 poll_interval: float = 10.0, poll_timeout: float = 3600.0, sleep=time.sleep,
                 redact: Redactor | None = None):
        if model_version not in ("pipeline", "vlm"):
            raise ValueError(f"unknown model version {model_version!r}")
        self.token = token
        self.base = OFFICIAL_API
        self.model_version, self.language, self.is_ocr = model_version, language, is_ocr
        self.enable_formula, self.enable_table = enable_formula, enable_table
        self.poll_interval, self.poll_timeout, self.sleep = poll_interval, poll_timeout, sleep
        self.redact = redact or Redactor([token])
        self.opener = urllib.request.build_opener(_SameOriginRedirects)

    def settings(self, kind: str) -> dict:
        return {"route": "cloud", "service": "mineru.net", "api": "precision v4", "model_version": self.model_version,
                "language": self.language, "is_ocr": self.is_ocr, "enable_formula": self.enable_formula,
                "enable_table": self.enable_table}

    def _api(self, method: str, path: str, body: dict | None = None) -> dict:
        data = json.dumps(body).encode("utf-8") if body is not None else None
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}
        if data is not None:
            headers["Content-Type"] = "application/json"
        delays = [5, 30, 120]
        for attempt in range(len(delays) + 1):
            request = urllib.request.Request(self.base + path, data=data, method=method, headers=headers)
            try:
                with self.opener.open(request, timeout=60) as response:
                    payload = json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as error:
                error.close()
                if error.code in (401, 403):
                    raise BatchStop("mineru.net refused the token", "token-rejected") from None
                if (error.code == 429 or error.code >= 500) and attempt < len(delays):
                    self.sleep(delays[attempt])
                    continue
                raise BatchStop(f"mineru.net answered with HTTP status {error.code}", "service-error") from None
            except (urllib.error.URLError, OSError, ValueError) as error:
                if attempt < len(delays):
                    self.sleep(delays[attempt])
                    continue
                raise BatchStop(f"mineru.net could not be reached: {self.redact(str(error))}", "network") from None
            code = str(payload.get("code"))
            message = self.redact(str(payload.get("msg", "")))
            if code == "0":
                return payload.get("data") or {}
            if code == "A0211":
                raise BatchStop("the mineru.net token has expired", "token-expired")
            if code == "A0202":
                raise BatchStop("mineru.net did not accept the token", "token-rejected")
            if code in ("-60018", "-60019"):
                raise BatchStop("the daily mineru.net parsing limit is reached; continue tomorrow", "quota")
            if code in ("-60009", "-10001", "-60007", "-60001") and attempt < len(delays):
                self.sleep(delays[attempt])
                continue
            raise BatchStop(f"mineru.net refused the request ({code}: {message})", "service-error")
        raise BatchStop("mineru.net stayed busy; try again later", "service-busy")

    def request_uploads(self, files: list[dict]) -> tuple[str, list[str]]:
        body = {"files": files, "model_version": self.model_version, "language": self.language,
                "enable_formula": self.enable_formula, "enable_table": self.enable_table}
        data = self._api("POST", "/api/v4/file-urls/batch", body)
        urls = data.get("file_urls") or []
        if not data.get("batch_id") or len(urls) != len(files):
            raise BatchStop("mineru.net returned an incomplete upload batch", "service-error")
        return str(data["batch_id"]), [str(url) for url in urls]

    def upload(self, url: str, path: Path) -> None:
        """PUT the file to the signed address with no token and no content type, as the service requires."""
        check_transfer_url(url)
        parts = urllib.parse.urlsplit(url)
        connection_class = http.client.HTTPSConnection if parts.scheme == "https" else http.client.HTTPConnection
        proxy = urllib.request.getproxies().get(parts.scheme)
        if proxy and parts.scheme == "https" and not urllib.request.proxy_bypass(parts.hostname or ""):
            # Through an institutional proxy: open a tunnel to the storage host, as urllib would.
            proxy_parts = urllib.parse.urlsplit(proxy if "://" in proxy else f"http://{proxy}")
            connection = connection_class(proxy_parts.hostname, proxy_parts.port or 8080, timeout=600)
            connection.set_tunnel(parts.hostname, parts.port or 443)
        else:
            connection = connection_class(parts.hostname, parts.port, timeout=600)
        target = parts.path + (f"?{parts.query}" if parts.query else "")
        try:
            connection.putrequest("PUT", target, skip_accept_encoding=True)
            connection.putheader("Content-Length", str(path.stat().st_size))
            connection.endheaders()
            with open(path, "rb") as stream:
                for chunk in iter(lambda: stream.read(1 << 20), b""):
                    connection.send(chunk)
            response = connection.getresponse()
            response.read()
        except OSError as error:
            raise ConversionError(f"the upload failed: {self.redact(str(error))}", "upload") from error
        finally:
            connection.close()
        if response.status not in (200, 201, 204):
            raise ConversionError(f"the upload was refused with HTTP status {response.status}", "upload")

    def results(self, batch_id: str) -> list[dict]:
        data = self._api("GET", f"/api/v4/extract-results/batch/{urllib.parse.quote(batch_id, safe='')}")
        return list(data.get("extract_result") or [])

    def download(self, url: str, work: Path) -> Path:
        """Fetch the result archive (without the token) and unpack it."""
        check_transfer_url(url)
        archive = work / "result.zip"
        work.mkdir(parents=True, exist_ok=True)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "*/*"}), timeout=600) as response, \
                    open(archive, "wb") as out:
                copied = 0
                for chunk in iter(lambda: response.read(1 << 20), b""):
                    copied += len(chunk)
                    if copied > MAX_OUTPUT:
                        raise ConversionError("the result archive is larger than expected")
                    out.write(chunk)
        except (urllib.error.URLError, OSError) as error:
            raise ConversionError(f"the result could not be downloaded: {self.redact(str(error))}", "download") from error
        raw = work / "raw"
        safe_extract(archive, raw)
        return raw


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
