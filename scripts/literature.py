#!/usr/bin/env python3
"""Search literature, retrieve local passages, and acquire public PDF references.

Uses only the Python standard library. Sciverse queries require a recorded researcher
confirmation and the SCIVERSE_API_KEY credential. Document conversion remains in ingest.py.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from credentials import load_env_local  # noqa: E402
from ingestion import library  # noqa: E402
from literature import downloads, search  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TOKEN_NAME = search.API_KEY_NAME


def token_for(root: Path) -> str:
    token = os.environ.get(TOKEN_NAME) or load_env_local(root).get(TOKEN_NAME)
    if not token:
        raise search.LiteratureError(f"The {TOKEN_NAME} credential is not set. Enter it privately with scripts/credentials.py set {TOKEN_NAME} after the researcher confirms Sciverse use.")
    return token


def command_authorize(args, root: Path) -> int:
    search.authorize_sciverse(root, args.record.expanduser().resolve(), replace=args.replace)
    print("The confirmed Sciverse query-sharing scope is recorded in requirements/privacy.md.")
    return 0


def command_revoke(args, root: Path) -> int:
    if search.revoke_sciverse(root):
        print("The active Sciverse query-sharing scope was removed from requirements/privacy.md.")
    else:
        print("No active Sciverse query-sharing scope was recorded.")
    return 0


def command_sciverse(args, root: Path) -> int:
    search.validate_scope_basis(root, args.scope_basis)
    search_id, folder, data = search.sciverse_search(root, token_for(root), args.query, scope_basis=args.scope_basis,
                                                      top_k=args.top_k, sub_queries=args.sub_queries)
    route = data["routes"][0]
    if route["status"] != "complete":
        print(f"Sciverse is unavailable for this search. Record: references/searches/{search_id}/README.md")
        print("Use a transparent fallback only if it is within the researcher's confirmed privacy scope.")
        return 1
    print(f"Sciverse returned {len(route['results'])} search snippets. Search record: references/searches/{search_id}/README.md")
    return 0


def command_metadata_search(args, root: Path) -> int:
    search.validate_scope_basis(root, args.scope_basis)
    search_id, folder, data = search.metadata_search(root, token_for(root), args.query, scope_basis=args.scope_basis,
                                                       page=args.page, page_size=args.page_size,
                                                       filters=json.loads(args.filters), sort=json.loads(args.sort), cursor=args.cursor)
    route = data["routes"][0]
    if route["status"] != "complete":
        print(f"Sciverse metadata search is unavailable. Record: references/searches/{search_id}/README.md")
        return 1
    print(f"Sciverse returned {len(route['results'])} metadata record(s). Search record: references/searches/{search_id}/README.md")
    for item in route["results"]:
        print(f"  {item.get('title') or '(title not returned)'} — DOI: {item.get('doi') or 'not returned'}; full-text ID: {item.get('doc_id') or 'not returned'}")
    print("Metadata records are discovery results, not inspected full text or evidence passages.")
    return 0


def command_relations(args, root: Path) -> int:
    folder, entry = search.add_relations(root, token_for(root), args.search_id, args.unique_id, args.relation, args.page, args.page_size)
    print(f"Relationship page status: {entry['status']}. Record: references/searches/{folder.name}/search.json")
    print("Relationships are discovery leads, not evidence of support or contradiction.")
    return 0 if entry["status"] == "complete" else 1


def command_resume_metadata(args, root: Path) -> int:
    search.metadata_resume_request(root, args.search_id)
    search_id, _, data = search.resume_metadata_search(root, token_for(root), args.search_id)
    route = data["routes"][-1]
    print(f"Metadata page status: {route['status']}; {len(route.get('results', []))} records. Search: references/searches/{search_id}/README.md")
    if route["status"] == "complete":
        print("More pages are available." if route.get("pagination", {}).get("next_cursor") else "No next cursor was returned.")
    return 0 if route["status"] == "complete" else 1


def command_schema_discovery(args, root: Path) -> int:
    folder, result = search.schema_discovery(root, token_for(root), args.search_id, args.unique_id)
    print(f"Experimental Paper Schema discovery: {result['status']}; record: references/searches/{folder.name}/search.json")
    return 0 if result["status"] == "complete" else 1


def command_schema_materials(args, root: Path) -> int:
    folder, result = search.schema_materials(root, token_for(root), args.search_id, args.schema_id, args.goal)
    print(f"Experimental Paper Schema materials: {result['status']}; record: references/searches/{folder.name}/search.json")
    print("Structured materials can be truncated and require verification against the source.")
    return 0 if result["status"] == "complete" else 1


def command_resource(args, root: Path) -> int:
    search.context_request(root, args.search_id, args.doc_id, 0, 1)
    folder, result = search.fetch_resource(root, token_for(root), args.search_id, args.doc_id, args.file_name)
    print(f"Derived resource: {result['status']}; record: references/searches/{folder.name}/search.json")
    if result.get("file"):
        print(f"Stored as references/searches/{folder.name}/{result['file']}.")
    return 0 if result["status"] == "complete" else 1


def command_host_search(args, root: Path) -> int:
    search_id, folder = search.add_host_search(root, args.search_id, args.input.expanduser().resolve())
    print(f"Recorded the model-host search as references/searches/{search_id}/README.md.")
    return 0


def command_local_search(args, root: Path) -> int:
    search_id, folder, results = search.local_search(root, args.query, args.source_id, args.limit)
    print(f"Local search found {len(results)} matching passage(s). Search record: references/searches/{search_id}/README.md")
    for item in results:
        heading = f" [{item['heading']}]" if item.get("heading") else ""
        print(f"{item['source_id']} {item['file']}:{item['line']}{heading} (extraction revision {item.get('extraction_revision') or 'unknown'}):")
        print(f"  {item['excerpt']}")
    if results:
        print("Markdown line locators are not PDF page locators; verify consequential evidence against the source.")
    return 0


def command_context(args, root: Path) -> int:
    search.context_request(root, args.search_id, args.doc_id, args.offset, args.limit)
    folder, context = search.add_context(root, token_for(root), args.search_id, args.doc_id, args.offset, args.limit)
    if context.get("text"):
        print(context["text"])
    else:
        print("Sciverse returned no readable text for this document range.")
    print(f"Context and its provider locator are recorded in references/searches/{folder.name}/search.json.")
    return 0 if context.get("text") else 1


def command_download(args, root: Path) -> int:
    if args.batch_id:
        if args.inputs:
            raise downloads.DownloadError("Use either a new reference list or --batch-id to resume an existing batch.")
        folder, data = downloads.load_batch(root, args.batch_id)
    else:
        if not args.inputs:
            raise downloads.DownloadError("Name DOI/URL values or a BibTeX, Markdown, or text reference list.")
        batch_id, folder, data = downloads.new_batch(root, args.inputs)
        args.batch_id = batch_id
    data = downloads.run_batch(root, folder, data, retry_rate_limited=args.retry_rate_limited)
    print(downloads.summary(args.batch_id, data))
    return 0


def command_download_status(args, root: Path) -> int:
    _, data = downloads.load_batch(root, args.batch_id)
    print(downloads.summary(args.batch_id, data))
    return 0


def command_download_verify(args, root: Path) -> int:
    item = downloads.verify_identity(root, args.batch_id, args.item, args.identity, args.evidence)
    print(f"Item {args.item}: identity status recorded as {item['identity_status']}.")
    return 0


def command_audit(args, root: Path) -> int:
    path = root / "references" / "bibliography.bib"
    if not path.is_file():
        print("No BibTeX bibliography exists yet. No citation-key resolution was checked.")
        return 0
    entries = library.entries(path.read_text(encoding="utf-8", errors="replace"))
    problems = []
    seen = set()
    for _, _, kind, key, body in entries:
        fields = library.fields_of(body)
        source_id = fields.get("sourceid")
        if key in seen:
            problems.append(f"duplicate citation key: {key}")
        seen.add(key)
        if not source_id:
            problems.append(f"{key}: no sourceid links this entry to the library")
        elif not re.fullmatch(r"src-[0-9a-f]{12,64}", source_id):
            problems.append(f"{key}: sourceid has an invalid format")
        elif not library.originals(root, source_id).is_dir():
            problems.append(f"{key}: source {source_id} has no archived original")
        elif not library.archived_file(library.originals(root, source_id)):
            problems.append(f"{key}: source {source_id} has no single archived original file")
        else:
            print(f"{key} -> {source_id}: source link resolves")
    for problem in problems:
        print(problem)
    print(f"Checked {len(entries)} BibTeX entries. This checks source links and citation-key uniqueness, not whether a source supports a claim.")
    return 1 if problems else 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Search literature and keep source-traceable retrieval records.")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    commands = parser.add_subparsers(dest="command", required=True)

    authorize = commands.add_parser("authorize-sciverse", help="record a confirmed query-sharing scope")
    authorize.add_argument("--record", type=Path, required=True, help="English Markdown record with the confirmed scope and researcher confirmation")
    authorize.add_argument("--replace", action="store_true", help="replace the active scope after the researcher confirms the change")
    commands.add_parser("revoke-sciverse", help="remove the active query-sharing scope after it has been changed")

    sciverse = commands.add_parser("search-sciverse", help="search Sciverse after privacy confirmation")
    sciverse.add_argument("--query", required=True)
    sciverse.add_argument("--scope-basis", required=True, help="exact excerpt from the active Sciverse scope that covers this query")
    sciverse.add_argument("--top-k", type=int, default=10)
    sciverse.add_argument("--sub-queries", type=int, default=0)

    metadata = commands.add_parser("search-sciverse-metadata", help="search structured Sciverse metadata, for example by title or DOI")
    metadata.add_argument("--query", default="")
    metadata.add_argument("--scope-basis", required=True, help="exact excerpt from the active Sciverse scope that covers this query")
    metadata.add_argument("--page", type=int, default=1)
    metadata.add_argument("--page-size", type=int, default=25)
    metadata.add_argument("--cursor", help="opaque next_cursor from a previous result")
    metadata.add_argument("--filters", default="[]", help="JSON array of catalog-supported filters")
    metadata.add_argument("--sort", default="[]", help="JSON array of catalog-supported sort fields")

    resume = commands.add_parser("resume-sciverse-metadata", help="continue a recorded metadata search with the same query and filters")
    resume.add_argument("--search-id", required=True)

    relations = commands.add_parser("sciverse-relations", help="record a page of a metadata result's paper relationships")
    relations.add_argument("--search-id", required=True)
    relations.add_argument("--unique-id", required=True)
    relations.add_argument("--relation", choices=("CITATIONS", "REFERENCES", "RELATED_WORKS"), required=True)
    relations.add_argument("--page", type=int, default=1)
    relations.add_argument("--page-size", type=int, default=25)

    schema_discovery = commands.add_parser("experimental-sciverse-schema-search", help="opt in to Paper Schema lookup for a recorded metadata result")
    schema_discovery.add_argument("--search-id", required=True)
    schema_discovery.add_argument("--unique-id", required=True)
    schema_discovery.add_argument("--enable-experimental", action="store_true", required=True)

    schema_materials = commands.add_parser("experimental-sciverse-schema-materials", help="opt in to a bounded Paper Schema material pack")
    schema_materials.add_argument("--search-id", required=True)
    schema_materials.add_argument("--schema-id", required=True)
    schema_materials.add_argument("--goal", choices=("overview", "survey", "benchmark", "method", "reproduction"), default="survey")
    schema_materials.add_argument("--enable-experimental", action="store_true", required=True)

    resource = commands.add_parser("read-sciverse-resource", help="retrieve a bounded resource named in recorded Sciverse context")
    resource.add_argument("--search-id", required=True)
    resource.add_argument("--doc-id", required=True)
    resource.add_argument("--file-name", required=True)

    host = commands.add_parser("record-host-search", help="add built-in search results to an existing provider record")
    host.add_argument("--search-id", help="append to a Sciverse record; omit for a standalone fallback search")
    host.add_argument("--input", type=Path, required=True, help="JSON with query, provider, results, and optional coverage_note")

    local = commands.add_parser("search-local", help="find passages in extracted local sources")
    local.add_argument("--query", required=True)
    local.add_argument("--source-id", action="append")
    local.add_argument("--limit", type=int, default=15)

    context = commands.add_parser("read-sciverse-context", help="retrieve a text range from a Sciverse result")
    context.add_argument("--search-id", required=True)
    context.add_argument("--doc-id", required=True)
    context.add_argument("--offset", type=int, default=0)
    context.add_argument("--limit", type=int, default=2000)

    download = commands.add_parser("download", help="download public PDF full text from DOI or URL references")
    download.add_argument("inputs", nargs="*", help="DOI/URL values or a BibTeX, Markdown, or text reference list")
    download.add_argument("--batch-id", help="resume an existing retrieval batch")
    download.add_argument("--retry-rate-limited", action="store_true", help="retry HTTP 429 items only after the service limit resets")

    status = commands.add_parser("download-status", help="show a retrieval batch")
    status.add_argument("batch_id")

    identity = commands.add_parser("verify-download", help="record an agent's checked source identity/version")
    identity.add_argument("batch_id")
    identity.add_argument("item", type=int, help="1-based item number in the batch")
    identity.add_argument("--identity", choices=("match", "version-different", "uncertain", "mismatch"), required=True)
    identity.add_argument("--evidence", required=True, help="document fields checked; do not guess")

    commands.add_parser("audit-bibliography", help="check BibTeX citation keys against archived source IDs")

    args = parser.parse_args(argv)
    root = args.root.resolve()
    handlers = {"authorize-sciverse": command_authorize, "revoke-sciverse": command_revoke, "search-sciverse": command_sciverse,
                "search-sciverse-metadata": command_metadata_search,
                "sciverse-relations": command_relations,
                "resume-sciverse-metadata": command_resume_metadata,
                "experimental-sciverse-schema-search": command_schema_discovery,
                "experimental-sciverse-schema-materials": command_schema_materials,
                "read-sciverse-resource": command_resource,
                "record-host-search": command_host_search, "search-local": command_local_search,
                "read-sciverse-context": command_context, "download": command_download,
                "download-status": command_download_status, "verify-download": command_download_verify,
                "audit-bibliography": command_audit}
    try:
        return handlers[args.command](args, root)
    except (search.LiteratureError, downloads.DownloadError, OSError, ValueError) as error:
        print(f"Could not complete: {error}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
