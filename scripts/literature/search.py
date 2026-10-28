"""Sciverse queries and local passage retrieval, with provider-specific search records."""

from __future__ import annotations

import datetime as dt
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from ingestion.common import now, read_json, safe_http_url, slug, write_json_atomic, write_text_atomic
from ingestion.library import extracted, provenance

API_ROOT = "https://api.sciverse.space"
API_KEY_NAME = "SCIVERSE_API_KEY"
SCIVERSE_BEGIN = "<!-- sciverse-query-sharing:begin -->"
SCIVERSE_MARKER = "<!-- sciverse-query-sharing-confirmed -->"
SCIVERSE_END = "<!-- sciverse-query-sharing:end -->"
MAX_QUERY_CHARS = 4096


class LiteratureError(RuntimeError):
    """A safe-to-report literature-tool refusal or service problem."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Do not forward an API authorization header to a redirect target."""

    def redirect_request(self, request, response, code, message, headers, new_url):
        return None


def _scrub(value):
    if isinstance(value, dict):
        clean = {}
        for key, item in value.items():
            if (key.lower() in {"url", "link", "source_url", "pdf_url", "download_url", "landing_page"} or key.lower().endswith("_url")) and isinstance(item, str):
                clean[key] = safe_http_url(item)
            else:
                clean[key] = _scrub(item)
        return clean
    if isinstance(value, list):
        return [_scrub(item) for item in value]
    return value


def _service_error(error: urllib.error.HTTPError) -> dict:
    body = b""
    try:
        body = error.read(65536)
    except OSError:
        pass
    try:
        parsed = json.loads(body.decode("utf-8", "replace"))
    except ValueError:
        parsed = {}
    code = parsed.get("code") if isinstance(parsed, dict) else None
    if not code and isinstance(parsed, dict):
        code = (parsed.get("error") or {}).get("code") if isinstance(parsed.get("error"), dict) else None
    return {"http_status": error.code, "code": str(code)[:120] if code else None}


def _request(url: str, token: str, body: dict | None = None, *, timeout: int = 45) -> dict:
    if not url.startswith(API_ROOT + "/"):
        raise LiteratureError("Refused an API address outside api.sciverse.space.")
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json", "User-Agent": "paper-template-literature/1.0"}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if data is not None else "GET")
    opener = urllib.request.build_opener(NoRedirect)
    last_error = None
    for attempt in range(3):
        try:
            with opener.open(request, timeout=timeout) as response:
                if response.geturl().split("/", 3)[:3] != API_ROOT.split("/", 3)[:3]:
                    raise LiteratureError("Sciverse redirected outside its documented API address.")
                payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, dict):
                raise LiteratureError("Sciverse returned an unexpected response format.")
            return _scrub(payload)
        except urllib.error.HTTPError as error:
            last_error = _service_error(error)
            status = error.code
            if status not in (500, 502, 503, 504) or attempt == 2:
                break
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
            last_error = {"problem": type(error).__name__}
            if attempt == 2:
                break
        time.sleep(1 + attempt)
    raise LiteratureError("Sciverse request failed: " + json.dumps(last_error, ensure_ascii=False))


def _privacy_confirmed(root: Path) -> bool:
    return bool(_confirmed_scope(root))


def _confirmed_scope(root: Path) -> str | None:
    path = root / "requirements" / "privacy.md"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    if (text.count(SCIVERSE_BEGIN), text.count(SCIVERSE_MARKER), text.count(SCIVERSE_END)) != (1, 1, 1):
        return None
    start = text.find(SCIVERSE_BEGIN) + len(SCIVERSE_BEGIN)
    marker = text.find(SCIVERSE_MARKER)
    end = text.find(SCIVERSE_END)
    if not start < marker < end:
        return None
    return text[start:marker].strip() or None


def _require_scope_basis(root: Path, scope_basis: str | None) -> str:
    scope = _confirmed_scope(root)
    if not scope:
        raise LiteratureError("No confirmed Sciverse query-sharing scope is recorded. Explain the data sent and ask the researcher first.")
    basis = " ".join((scope_basis or "").split())
    normalized_scope = " ".join(scope.split())
    if not basis or basis not in normalized_scope:
        raise LiteratureError("Provide an exact excerpt from the active Sciverse scope that covers this query; check the query against that scope before sending it.")
    return basis


def validate_scope_basis(root: Path, scope_basis: str | None) -> str:
    """Check that the cited query scope is present in the active confirmation."""
    return _require_scope_basis(root, scope_basis)


def privacy_confirmed(root: Path) -> bool:
    """Whether a researcher-confirmed Sciverse query scope is recorded."""
    return _privacy_confirmed(root)


def _remove_sciverse_block(text: str) -> tuple[str, bool]:
    if (text.count(SCIVERSE_BEGIN), text.count(SCIVERSE_MARKER), text.count(SCIVERSE_END)) != (1, 1, 1):
        if SCIVERSE_BEGIN not in text and SCIVERSE_MARKER not in text and SCIVERSE_END not in text:
            return text, False
        raise LiteratureError("The Sciverse scope record has incomplete or repeated machine markers; repair it before changing the choice.")
    start = text.find(SCIVERSE_BEGIN)
    marker = text.find(SCIVERSE_MARKER)
    end = text.find(SCIVERSE_END, start + len(SCIVERSE_BEGIN))
    if not start < marker < end:
        raise LiteratureError("The Sciverse scope markers are out of order; repair the record before changing the choice.")
    return text[:start].rstrip() + "\n\n" + text[end + len(SCIVERSE_END):].lstrip("\n"), True


def authorize_sciverse(root: Path, record_path: Path, *, replace: bool = False) -> None:
    """Append the researcher's confirmed, interaction-language record after a skill has obtained it."""
    privacy = root / "requirements" / "privacy.md"
    if not record_path.is_file():
        raise LiteratureError(f"Sciverse confirmation record not found: {record_path}")
    record = record_path.read_text(encoding="utf-8").strip()
    if not record or "sciverse" not in record.casefold() or SCIVERSE_MARKER in record:
        raise LiteratureError("The confirmation record must name Sciverse and contain the scope and the researcher's confirmation.")
    current = privacy.read_text(encoding="utf-8") if privacy.is_file() else "# Privacy and Processing Requirements\n"
    has_markers = any(marker in current for marker in (SCIVERSE_BEGIN, SCIVERSE_MARKER, SCIVERSE_END))
    if has_markers and not replace:
        raise LiteratureError("A Sciverse query-sharing scope is already recorded. Resolve any scope change with the researcher first.")
    current = current.replace("No document-processing or external query-sharing choices have been confirmed yet.",
                              "No document-processing choice has been confirmed yet.")
    if replace:
        current, removed = _remove_sciverse_block(current)
        if not removed:
            raise LiteratureError("There is no complete Sciverse scope record to replace.")
    suffix = f"\n\n{SCIVERSE_BEGIN}\n{record}\n{SCIVERSE_MARKER}\n{SCIVERSE_END}\n"
    write_text_atomic(privacy, current.rstrip() + suffix)


def revoke_sciverse(root: Path) -> bool:
    """Remove only the active machine-bounded Sciverse scope block after the choice is changed."""
    privacy = root / "requirements" / "privacy.md"
    if not privacy.is_file():
        return False
    text, removed = _remove_sciverse_block(privacy.read_text(encoding="utf-8"))
    if removed:
        write_text_atomic(privacy, text)
    return removed


def _search_dir(root: Path) -> Path:
    return root / "references" / "searches"


def _new_search_id(root: Path, query: str) -> str:
    base = dt.datetime.now().astimezone().strftime("%Y%m%d") + "-" + slug(query, 36, "search")
    target = _search_dir(root)
    candidate, number = base, 2
    while (target / candidate).exists():
        candidate, number = f"{base}-{number}", number + 1
    return candidate


def _save_search(root: Path, search_id: str, data: dict) -> Path:
    folder = _search_dir(root) / search_id
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,100}", search_id):
        raise LiteratureError("Invalid search record ID.")
    if folder.exists() and not (folder / "search.json").is_file():
        raise LiteratureError(f"Search folder exists without a record: {search_id}")
    folder.mkdir(parents=True, exist_ok=True)
    write_json_atomic(folder / "search.json", data)
    providers = ", ".join(sorted({route.get("provider", "unknown") for route in data.get("routes", [])}))
    results = sum(len(route.get("results", [])) for route in data.get("routes", []))
    notes = [f"Search `{search_id}` was recorded on {data.get('created_at', '')}.",
             f"- Initial query: {data.get('query', '')}", f"- Providers: {providers or 'none'}", f"- Result records: {results}"]
    for route in data.get("routes", []):
        notes.append(f"- {route.get('provider', 'unknown')} ({route.get('created_at', 'date unknown')}): query `{route.get('query', data.get('query', ''))}`; status {route.get('status', 'unknown')}; coverage: {route.get('coverage_note') or 'not specified'}")
    notes += [
             "Provider snippets are discovery leads. They do not show that the full text was inspected.",
             "The machine-readable provider results and source locators are in [`search.json`](search.json)."]
    write_text_atomic(folder / "README.md", f"# Literature Search: {search_id}\n\n" + "\n".join(notes) + "\n")
    return folder


def _new_record(root: Path, query: str, route: dict) -> tuple[str, dict]:
    search_id = _new_search_id(root, query)
    created_at = now()
    route.setdefault("query", query)
    route.setdefault("created_at", created_at)
    data = {"schema": "paper-template.literature-search/1", "search_id": search_id,
            "created_at": created_at, "query": query,
            "routes": [route]}
    return search_id, data


def sciverse_search(root: Path, token: str, query: str, *, scope_basis: str, top_k: int = 10, sub_queries: int = 0) -> tuple[str, Path, dict]:
    scope_basis = _require_scope_basis(root, scope_basis)
    query = query.strip()
    if not query or len(query) > MAX_QUERY_CHARS:
        raise LiteratureError(f"The query must contain 1 to {MAX_QUERY_CHARS} characters.")
    if not 1 <= top_k <= 100 or not 0 <= sub_queries <= 4:
        raise LiteratureError("Sciverse top_k must be 1–100 and sub_queries 0–4.")
    route = {"provider": "OpenDataLab Sciverse", "endpoint": "agentic-search", "status": "failed", "results": [],
             "scope_basis": scope_basis,
             "limitations": ["Sciverse returned only fields available to this account.",
                             "Returned chunks are search snippets until full text is separately inspected."]}
    search_id, data = _new_record(root, query, route)
    try:
        payload = _request(API_ROOT + "/agentic-search", token,
                           {"query": query, "top_k": top_k, "sub_queries": sub_queries})
        hits = payload.get("hits", [])
        if not isinstance(hits, list) or any(not isinstance(hit, dict) for hit in hits):
            raise LiteratureError("Sciverse returned an unexpected hit list.")
        route.update(status="complete", results=[{
            "provider_id": hit.get("doc_id"), "title": hit.get("title"),
            "snippet": hit.get("chunk"), "abstract": hit.get("abstract"),
            "score": hit.get("score"), "inspection": "search-snippet",
            "locator": {name: hit.get(name) for name in ("doc_id", "chunk_id", "offset", "page_no", "source_type") if hit.get(name) is not None},
            "metadata": {name: hit.get(name) for name in ("author", "publication_venue_name_unified", "publication_venue_type",
                         "publication_published_date", "publication_published_year", "doi", "lang", "metadata_type") if hit.get(name) is not None},
            "raw": hit,
        } for hit in hits])
        route["response_limits"] = {"top_k_requested": top_k, "sub_queries": sub_queries,
                                    "service_max_query_chars": MAX_QUERY_CHARS}
    except LiteratureError as error:
        try:
            route["error"] = json.loads(str(error).split(": ", 1)[1])
        except (ValueError, IndexError):
            route["error"] = {"message": str(error)}
        route["status"] = "unavailable"
    folder = _save_search(root, search_id, data)
    return search_id, folder, data


def metadata_search(root: Path, token: str, query: str, *, scope_basis: str, page: int = 1, page_size: int = 25) -> tuple[str, Path, dict]:
    """Search Sciverse bibliographic metadata, for example to resolve an exact DOI or title."""
    scope_basis = _require_scope_basis(root, scope_basis)
    query = query.strip()
    if not query:
        raise LiteratureError("Metadata search needs a title, DOI, or other query text.")
    if page < 1 or not 1 <= page_size <= 200 or page * page_size > 10000:
        raise LiteratureError("Metadata search supports page ≥ 1, page_size 1–200, and page × page_size ≤ 10000.")
    route = {"provider": "OpenDataLab Sciverse", "endpoint": "meta-search", "status": "failed", "results": [],
             "scope_basis": scope_basis,
             "limitations": ["Metadata results are not evidence passages and do not establish full-text access.",
                             "Fields may be omitted by account permissions."]}
    search_id, data = _new_record(root, query, route)
    try:
        payload = _request(API_ROOT + "/meta-search", token, {"query": query, "page": page, "page_size": page_size})
        results = payload.get("results", [])
        if not isinstance(results, list) or any(not isinstance(result, dict) for result in results):
            raise LiteratureError("Sciverse returned an unexpected metadata result list.")
        route.update(status="complete", results=[{"provider_id": result.get("unique_id"),
                                                   "doc_id": result.get("doc_id"), "title": result.get("title"),
                                                   "doi": result.get("doi"), "abstract": result.get("abstract"),
                                                   "metadata": result, "inspection": "metadata-only"} for result in results],
                     pagination={key: payload.get(key) for key in ("total_count", "page", "page_size", "total_pages", "next_cursor") if payload.get(key) is not None})
    except LiteratureError as error:
        try:
            route["error"] = json.loads(str(error).split(": ", 1)[1])
        except (ValueError, IndexError):
            route["error"] = {"message": str(error)}
        route["status"] = "unavailable"
    folder = _save_search(root, search_id, data)
    return search_id, folder, data


def add_host_search(root: Path, search_id: str | None, input_path: Path) -> tuple[str, Path]:
    if search_id and not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,100}", search_id):
        raise LiteratureError("Invalid search record ID.")
    payload = read_json(input_path)
    if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
        raise LiteratureError("The host-search input must be JSON with query, coverage_note, and a results list.")
    query = payload.get("query")
    coverage_note = payload.get("coverage_note")
    if not isinstance(query, str) or not query.strip():
        raise LiteratureError("Record the exact query used for the host search.")
    if not isinstance(coverage_note, str) or not coverage_note.strip():
        raise LiteratureError("Record which gap or cross-check the host search addressed.")
    if search_id:
        folder = _search_dir(root) / search_id
        data = read_json(folder / "search.json")
        if not isinstance(data, dict) or data.get("schema") != "paper-template.literature-search/1":
            raise LiteratureError(f"No search record named {search_id!r}.")
    else:
        route = {"provider": str(payload.get("provider") or "model-host built-in search"),
                 "endpoint": None, "status": "complete", "query": query.strip(),
                 "coverage_note": coverage_note.strip(), "created_at": now(), "results": _scrub(payload["results"]),
                 "limitations": ["A search result is a discovery lead until the source text is inspected."]}
        search_id, data = _new_record(root, query.strip(), route)
        folder = _save_search(root, search_id, data)
        return search_id, folder
    route = {"provider": str(payload.get("provider") or "model-host built-in search"),
             "endpoint": None, "status": "complete", "query": query.strip(),
             "coverage_note": coverage_note.strip(), "created_at": now(),
             "results": _scrub(payload["results"]),
             "limitations": ["A search result is a discovery lead until the source text is inspected."]}
    data.setdefault("routes", []).append(route)
    _save_search(root, search_id, data)
    return search_id, folder


def _tokens(text: str) -> list[str]:
    return [part.casefold() for part in re.findall(r"[^\W_]+", text, flags=re.UNICODE) if len(part) > 1]


def local_search(root: Path, query: str, source_ids: list[str] | None = None, limit: int = 15) -> tuple[str, Path, list[dict]]:
    terms = sorted(set(_tokens(query)))
    if not terms:
        raise LiteratureError("The local search needs at least one searchable word.")
    if not 1 <= limit <= 100:
        raise LiteratureError("The result limit must be 1–100.")
    base = root / "references" / "extracted"
    if source_ids and any(not re.fullmatch(r"src-[0-9a-f]{12,64}", item) for item in source_ids):
        raise LiteratureError("A source ID has an invalid format.")
    folders = [base / item for item in source_ids] if source_ids else sorted(base.glob("src-*"))
    results = []
    for folder in folders:
        document = folder / "document.md"
        if not document.is_file():
            continue
        record = provenance(root, folder.name) or {}
        revision = record.get("revision")
        heading = ""
        matches = []
        with document.open("r", encoding="utf-8", errors="replace") as stream:
            for line_number, line in enumerate(stream, 1):
                if line.lstrip().startswith("#"):
                    heading = line.strip(" #\r\n")
                folded = line.casefold()
                count = sum(folded.count(term) for term in terms)
                if count:
                    matches.append({"score": count, "source_id": folder.name, "file": f"references/extracted/{folder.name}/document.md",
                                    "line": line_number, "heading": heading or None,
                                    "extraction_revision": revision, "locator_status": "markdown-line-only",
                                    "excerpt": line.strip()[:1200]})
        matches.sort(key=lambda item: (-item["score"], item["line"]))
        results.extend(matches[:5])
    results.sort(key=lambda item: (-item["score"], item["source_id"], item["line"]))
    results = results[:limit]
    route = {"provider": "local extracted library", "endpoint": "streaming lexical search", "status": "complete",
             "created_at": now(), "query": query,
             "results": results, "limitations": ["Markdown line numbers are extraction locators, not PDF page locators."]}
    search_id, data = _new_record(root, query, route)
    folder = _save_search(root, search_id, data)
    return search_id, folder, results


def add_context(root: Path, token: str, search_id: str, doc_id: str, offset: int, limit: int) -> tuple[Path, dict]:
    folder, data, _ = context_request(root, search_id, doc_id, offset, limit)
    query = urllib.parse.urlencode({"doc_id": doc_id, "offset": offset, "limit": limit})
    try:
        payload = _request(API_ROOT + "/content?" + query, token)
        context = {"provider": "OpenDataLab Sciverse", "doc_id": doc_id, "offset": offset, "created_at": now(),
                   "limit_requested": limit, "text": payload.get("content", payload.get("text", "")),
                   "next_offset": payload.get("next_offset"), "more": payload.get("more"),
                   "inspection": "service-fulltext-context", "limitations": ["Service text was retrieved by character offset; verify consequential claims against the original where available."]}
    except LiteratureError as error:
        context = {"provider": "OpenDataLab Sciverse", "doc_id": doc_id, "offset": offset, "created_at": now(),
                   "limit_requested": limit, "inspection": "failed", "error": str(error)}
    data.setdefault("contexts", []).append(context)
    _save_search(root, search_id, data)
    return folder, context


def context_request(root: Path, search_id: str, doc_id: str, offset: int, limit: int) -> tuple[Path, dict, dict]:
    """Validate an authorized context locator without making a service request."""
    if offset < 0 or not 1 <= limit <= 8000:
        raise LiteratureError("Context offset must be non-negative and limit must be 1–8000 characters.")
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,100}", search_id):
        raise LiteratureError("Invalid search record ID.")
    folder = _search_dir(root) / search_id
    path = folder / "search.json"
    data = read_json(path)
    if not isinstance(data, dict) or data.get("schema") != "paper-template.literature-search/1":
        raise LiteratureError(f"No search record named {search_id!r}.")
    sciverse_routes = [route for route in data.get("routes", []) if route.get("provider") == "OpenDataLab Sciverse"]
    matched_route = next((route for route in sciverse_routes if any(
        str(result.get("doc_id") or result.get("provider_id") or "") == doc_id
        for result in route.get("results", [])
    )), None)
    if not matched_route:
        raise LiteratureError("The document ID is not present in this search record's Sciverse results.")
    _require_scope_basis(root, matched_route.get("scope_basis"))
    return folder, data, matched_route
