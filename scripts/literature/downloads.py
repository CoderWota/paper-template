"""Resumable retrieval of publicly accessible PDF files from DOI and URL references."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import shutil
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from ingestion.common import read_json, safe_http_url, slug, write_json_atomic, write_text_atomic
from ingestion import library

MAX_DOWNLOAD_BYTES = 500 * 1024 * 1024
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s<>\"{}|\\^`]+)", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s<>\"{}]+", re.IGNORECASE)


class DownloadError(RuntimeError):
    """A safe-to-report reference-download error."""


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^doi:\s*", "", value, flags=re.IGNORECASE)
    value = re.split(r"[?#]", value, maxsplit=1)[0]
    return value.rstrip(".,;:)]}").strip() or None


def _from_text(line: str) -> dict | None:
    line = line.strip()
    if not line or line.startswith(("#", "%", "//")):
        return None
    doi_match = DOI_RE.search(line)
    url_match = URL_RE.search(line)
    doi = normalize_doi(doi_match.group(1)) if doi_match else None
    url = url_match.group(0).rstrip(".,;:)]}") if url_match else None
    if url and "doi.org/" in url.casefold():
        doi = normalize_doi(url)
    if not doi and not url:
        return {"reference": line, "title": None, "doi": None, "url": None, "status": "metadata-only",
                "notes": ["No DOI or direct URL was found; no full-text request was made."]}
    safe_reference = doi or safe_http_url(url) or line
    item = {"reference": safe_reference, "title": None, "doi": doi, "url": safe_http_url(url), "status": "pending", "notes": []}
    is_doi_resolver = url and (urllib.parse.urlsplit(url).hostname or "").casefold() in ("doi.org", "dx.doi.org")
    if url and urllib.parse.urlsplit(url).query and not (doi and is_doi_resolver):
        item.update(status="login/manual-access-needed", notes=["The URL contains query parameters that may be signed or secret. It was not stored or requested; provide a public URL without query parameters."])
    return item


def read_references(inputs: list[str], root: Path) -> list[dict]:
    """Read DOI/URL arguments, plain text lines, Markdown lists, or BibTeX entries."""
    found = []
    for value in inputs:
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = root / path
        if path.is_file() and path.suffix.casefold() == ".bib":
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            for entry_type, key, body in ((kind, key, body) for _, _, kind, key, body in library.entries(text)):
                fields = library.fields_of(body)
                raw_url = fields.get("url")
                reference = {"reference": f"{key} ({entry_type})", "title": fields.get("title"),
                             "doi": normalize_doi(fields.get("doi")), "url": safe_http_url(raw_url), "status": "pending", "notes": []}
                is_doi_resolver = raw_url and (urllib.parse.urlsplit(raw_url).hostname or "").casefold() in ("doi.org", "dx.doi.org")
                if raw_url and not reference["doi"] and not is_doi_resolver and urllib.parse.urlsplit(raw_url).query:
                    reference.update(status="login/manual-access-needed", notes=["The BibTeX URL has query parameters that may be signed or secret. It was not stored or requested; provide a public URL without query parameters."])
                if reference["doi"] or reference["url"]:
                    found.append(reference)
                else:
                    reference.update(status="metadata-only", notes=["The BibTeX entry has no DOI or URL."])
                    found.append(reference)
        elif path.is_file() and path.suffix.casefold() in (".txt", ".md"):
            for line in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
                item = _from_text(line)
                if item:
                    found.append(item)
        elif path.exists():
            raise DownloadError(f"Unsupported reference-list file: {value}. Use BibTeX, a DOI/URL text list, or Markdown.")
        else:
            item = _from_text(value)
            if item:
                found.append(item)
    return found


def new_batch(root: Path, inputs: list[str]) -> tuple[str, Path, dict]:
    references = read_references(inputs, root)
    if not references:
        raise DownloadError("No DOI, URL, or reference item was found.")
    base = dt.datetime.now().astimezone().strftime("%Y%m%d") + "-" + slug(Path(inputs[0]).stem if inputs else "references", 30, "references")
    parent = root / "references" / "downloads"
    batch_id, number = base, 2
    while (parent / batch_id).exists():
        batch_id, number = f"{base}-{number}", number + 1
    safe_inputs = [safe_http_url(value) or value for value in inputs]
    data = {"schema": "paper-template.reference-download/1", "batch_id": batch_id,
            "created_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "updated_at": None,
            "inputs": safe_inputs, "items": references}
    folder = parent / batch_id
    _save(root, folder, data)
    return batch_id, folder, data


def load_batch(root: Path, batch_id: str) -> tuple[Path, dict]:
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,100}", batch_id):
        raise DownloadError("Invalid download batch ID.")
    folder = root / "references" / "downloads" / batch_id
    data = read_json(folder / "batch.json")
    if not isinstance(data, dict) or data.get("schema") != "paper-template.reference-download/1":
        raise DownloadError(f"No download batch named {batch_id!r}.")
    return folder, data


def _save(root: Path, folder: Path, data: dict) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    data["updated_at"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    write_json_atomic(folder / "batch.json", data)
    counts = {}
    for item in data.get("items", []):
        counts[item.get("status", "unknown")] = counts.get(item.get("status", "unknown"), 0) + 1
    lines = [f"Download batch `{data['batch_id']}` started {data['created_at']} and updated {data['updated_at']}.", "",
             "| Item | Status | Source | Identity check | Notes |", "| --- | --- | --- | --- | --- |"]
    for number, item in enumerate(data.get("items", []), 1):
        source = item.get("source_id") or item.get("archive_path") or "—"
        cells = [str(number), item.get("status", "unknown"), source, item.get("identity_status", "not applicable"),
                 "; ".join(item.get("notes") or [])]
        lines.append("| " + " | ".join(value.replace("|", "\\|").replace("\n", " ") for value in cells) + " |")
    lines += ["", "Counts: " + (", ".join(f"{n} {k}" for k, n in sorted(counts.items())) or "no items"),
              "", "Only public PDF responses are archived. HTML login/error pages are not stored as successful downloads. "
              "A PDF download does not by itself verify that the file is the requested edition; see the identity status in `batch.json`.",
              "Retrieved files are archived unchanged under [`../../originals/`](../../originals/README.md). Conversion uses the separate `source-ingestion` workflow.",
              "The machine-readable retrieval provenance is in [`batch.json`](batch.json)."]
    write_text_atomic(folder / "README.md", f"# Reference Download: {data['batch_id']}\n\n" + "\n".join(lines) + "\n")


def known_doi_sources(root: Path) -> dict[str, str]:
    """Find DOI-to-source links already recorded in download batches or the canonical bibliography."""
    known = {}
    batches = root / "references" / "downloads"
    if batches.is_dir():
        for path in batches.glob("*/batch.json"):
            data = read_json(path)
            if not isinstance(data, dict):
                continue
            for item in data.get("items", []):
                doi, source_id = normalize_doi(item.get("doi")), item.get("source_id")
                if doi and source_id and re.fullmatch(r"src-[0-9a-f]{12,64}", source_id) and library.archived_file(library.originals(root, source_id)):
                    known[doi.casefold()] = source_id
    bibliography = root / "references" / "bibliography.bib"
    if bibliography.is_file():
        text = bibliography.read_text(encoding="utf-8", errors="replace")
        for _, _, _, _, body in library.entries(text):
            fields = library.fields_of(body)
            doi, source_id = normalize_doi(fields.get("doi")), fields.get("sourceid")
            if doi and source_id and re.fullmatch(r"src-[0-9a-f]{12,64}", source_id) and library.archived_file(library.originals(root, source_id)):
                known[doi.casefold()] = source_id
    return known


def _target_url(item: dict) -> str | None:
    doi = normalize_doi(item.get("doi"))
    if doi:
        return "https://doi.org/" + urllib.parse.quote(doi, safe="/()")
    value = item.get("url")
    if not value:
        return None
    parts = urllib.parse.urlsplit(value)
    if parts.query:
        raise DownloadError("The URL contains query parameters that may be signed or secret. It was not stored or requested; provide a public URL without query parameters.")
    if parts.scheme not in ("http", "https") or not parts.hostname:
        return None
    return value


def _login_page(body: bytes) -> bool:
    sample = body[:32768].decode("utf-8", "ignore").casefold()
    return any(word in sample for word in ("sign in", "log in", "login", "institutional access", "access denied", "subscribe", "purchase access"))


def _fetch(url: str, temporary: Path) -> tuple[str, str, int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "paper-template-reference-fetch/1.0", "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.2"})
    try:
        response = urllib.request.urlopen(request, timeout=45)
    except urllib.error.HTTPError as error:
        status = "login/manual-access-needed" if error.code in (401, 402, 403) else "unavailable" if error.code in (404, 410) else "rate-limited" if error.code == 429 else "failed"
        return status, safe_http_url(error.geturl()) or safe_http_url(url) or "", 0, f"HTTP {error.code}"
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return "failed", safe_http_url(url) or "", 0, type(error).__name__
    with response:
        final_url = safe_http_url(response.geturl()) or safe_http_url(url) or ""
        status_code = getattr(response, "status", 200)
        if status_code in (401, 402, 403):
            return "login/manual-access-needed", final_url, 0, f"HTTP {status_code}"
        if status_code == 429:
            return "rate-limited", final_url, 0, "HTTP 429; wait for the service limit to reset before retrying"
        content_type = response.headers.get_content_type().casefold()
        length = response.headers.get("Content-Length")
        if length and length.isdigit() and int(length) > MAX_DOWNLOAD_BYTES:
            return "failed", final_url, 0, f"response exceeds the {MAX_DOWNLOAD_BYTES // (1024 * 1024)} MiB download limit"
        first = response.read(16)
        if not first.startswith(b"%PDF-") or content_type not in ("application/pdf", "application/octet-stream", "binary/octet-stream"):
            remainder = response.read(32768)
            body = first + remainder
            if _login_page(body):
                return "login/manual-access-needed", final_url, 0, "the server returned an access or sign-in page, not a PDF"
            return "metadata-only", final_url, 0, "the address returned a web page or another non-PDF response, not a full-text PDF"
        temporary.parent.mkdir(parents=True, exist_ok=True)
        size = 0
        digest = hashlib.sha256()
        with temporary.open("wb") as stream:
            stream.write(first)
            size += len(first)
            digest.update(first)
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > MAX_DOWNLOAD_BYTES:
                    stream.close()
                    temporary.unlink(missing_ok=True)
                    return "failed", final_url, 0, f"response exceeds the {MAX_DOWNLOAD_BYTES // (1024 * 1024)} MiB download limit"
                digest.update(chunk)
                stream.write(chunk)
        if size < 16:
            temporary.unlink(missing_ok=True)
            return "failed", final_url, 0, "the PDF response is incomplete"
        with temporary.open("rb") as stream:
            stream.seek(max(0, size - 2048))
            tail = stream.read(2048)
        if b"%%EOF" not in tail:
            temporary.unlink(missing_ok=True)
            return "failed", final_url, 0, "the response has a PDF header but no end-of-file marker"
        return "downloaded", final_url, size, digest.hexdigest()


def run_batch(root: Path, folder: Path, data: dict, *, retry_rate_limited: bool = False, emit=print) -> dict:
    seen_doi = {}
    rate_limited_hosts = set()
    known_dois = known_doi_sources(root)
    last_host = None
    last_request_at = 0.0
    for index, item in enumerate(data.get("items", []), 1):
        doi = normalize_doi(item.get("doi"))
        if doi and doi.casefold() in seen_doi:
            prior = data.get("items", [])[seen_doi[doi.casefold()] - 1]
            item.update(status="duplicate", duplicate_of=seen_doi[doi.casefold()], source_id=prior.get("source_id"),
                        notes=["The same DOI is already listed in this batch."])
            _save(root, folder, data)
            continue
        if doi:
            seen_doi[doi.casefold()] = index
        if item.get("status") not in ("pending", "failed", "downloading") and not (retry_rate_limited and item.get("status") == "rate-limited"):
            continue
        if doi and doi.casefold() in known_dois:
            source_id = known_dois[doi.casefold()]
            archived = library.archived_file(library.originals(root, source_id))
            item.update(status="existing", source_id=source_id, archive_path=archived.relative_to(root).as_posix(),
                        identity_status="unverified", notes=["This DOI is already linked to an archived source in the reference library."])
            library.index_upsert(root, source_id, files=item["archive_path"])
            _save(root, folder, data)
            continue
        try:
            url = _target_url(item)
        except DownloadError as error:
            item.update(status="login/manual-access-needed", notes=[str(error)])
            _save(root, folder, data)
            continue
        if not url:
            item.update(status="metadata-only", notes=["No safe DOI resolver or HTTP(S) URL is available."])
            _save(root, folder, data)
            continue
        host = (urllib.parse.urlsplit(url).hostname or "").casefold()
        if host in rate_limited_hosts:
            item.update(status="rate-limited", notes=["A previous item on this host returned HTTP 429; this batch stopped requesting the host."])
            _save(root, folder, data)
            continue
        if host == last_host:
            time.sleep(max(0.0, 1.0 - (time.monotonic() - last_request_at)))
        last_host, last_request_at = host, time.monotonic()
        item["attempts"] = item.get("attempts", 0) + 1
        item["retrieval_started_at"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
        item["retrieval_url"] = safe_http_url(url)
        item["status"] = "downloading"
        _save(root, folder, data)
        staging = root / ".tmp" / "literature-download" / data["batch_id"] / f"{index:04d}.pdf"
        staging.parent.mkdir(parents=True, exist_ok=True)
        outcome, final_url, size, detail = _fetch(url, staging)
        item["final_url"] = final_url
        if outcome != "downloaded":
            item.update(status=outcome, notes=[detail])
            if outcome == "rate-limited":
                rate_limited_hosts.add(host)
                final_host = (urllib.parse.urlsplit(final_url).hostname or "").casefold()
                if final_host:
                    rate_limited_hosts.add(final_host)
            _save(root, folder, data)
            continue
        sha = detail
        try:
            source_id, archived, created = library.archive(root, staging, sha, safe_http_url(item.get("url")) or item.get("doi") or "reference list",
                                                           dt.date.today().isoformat())
            item.update(status="downloaded" if created else "existing", source_id=source_id,
                        archive_path=archived.relative_to(root).as_posix(), sha256=sha, bytes=size,
                        retrieved_at=dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                        identity_status="unverified", notes=["PDF content was validated; requested title/version still needs checking against the document."])
            try:
                library.index_upsert(root, source_id, default_title=f"(downloaded) {archived.name}", files=item["archive_path"])
            except OSError:
                item.setdefault("notes", []).append("The original was archived, but the reference index could not be updated.")
        except (OSError, ValueError) as error:
            item.update(status="failed", notes=[f"The PDF was retrieved but could not be archived: {type(error).__name__}"])
            recovered = folder / "unarchived"
            recovered.mkdir(parents=True, exist_ok=True)
            retained = recovered / staging.name
            if staging.is_file():
                shutil.move(str(staging), str(retained))
                write_text_atomic(recovered / "README.md", "# Unarchived PDF\n\nA PDF was retrieved but could not be copied into `references/originals/`. It is retained here for recovery. The batch record links the item and checksum.\n")
                item["recovered_path"] = retained.relative_to(root).as_posix()
        finally:
            try:
                staging.unlink()
            except OSError:
                pass
        _save(root, folder, data)
        emit(f"{index}. {item.get('reference', item.get('doi') or item.get('url'))}: {item['status']}")
    shutil.rmtree(root / ".tmp" / "literature-download" / data["batch_id"], ignore_errors=True)
    _save(root, folder, data)
    return data


def verify_identity(root: Path, batch_id: str, item_number: int, result: str, evidence: str) -> dict:
    if result not in ("match", "version-different", "uncertain", "mismatch"):
        raise DownloadError("Identity result must be match, version-different, uncertain, or mismatch.")
    folder, data = load_batch(root, batch_id)
    items = data.get("items", [])
    if not 1 <= item_number <= len(items):
        raise DownloadError("Download item number is outside the batch.")
    item = items[item_number - 1]
    if item.get("status") not in ("downloaded", "existing"):
        raise DownloadError("Only an archived PDF can receive an identity check.")
    if not evidence.strip():
        raise DownloadError("Record what document details were checked.")
    item["identity_status"] = result
    item["identity_checked_at"] = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    item["identity_evidence"] = evidence.strip()
    _save(root, folder, data)
    return item


def summary(batch_id: str, data: dict) -> str:
    lines = [f"Download batch {batch_id}:"]
    for number, item in enumerate(data.get("items", []), 1):
        reference = item.get("title") or item.get("doi") or item.get("url") or item.get("reference") or "reference"
        source = f" — {item['source_id']}" if item.get("source_id") else ""
        identity = f", identity {item['identity_status']}" if item.get("identity_status") else ""
        note = "; ".join(item.get("notes") or [])
        lines.append(f"  {number}. {reference}: {item.get('status', 'unknown')}{identity}{source}" + (f" ({note})" if note else ""))
    lines.append(f"Record: references/downloads/{batch_id}/README.md")
    return "\n".join(lines)
