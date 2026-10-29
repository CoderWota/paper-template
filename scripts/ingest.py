#!/usr/bin/env python3
"""Import documents into the workspace with MinerU, or read Markdown and plain text directly.

Archives each original unchanged, converts it with the processing route that the researcher
confirmed, checks the result (page coverage, text left out of the Markdown, image links, and
formulas), publishes it in one step, and keeps a resumable record of the batch in
inbox/imports/<import-id>/. References go to references/; review documents go to
reviews/<venue-id>/<round-id>/; research feedback goes to research/feedback/<feedback-id>/. The researcher's own
manuscript goes to its import record (--to manuscript) for adoption with scripts/manuscript.py adopt; an editable
manuscript (Word, OpenDocument, LaTeX) is read with Pandoc on this computer (--route pandoc), a PDF with MinerU.
Nothing ever switches to another route or parser.

Usage:
  python scripts/ingest.py plan [--to DEST] [--route local|cloud] [--recursive] PATH...
  python scripts/ingest.py run --route local --tier flash|basic|standard|advanced [--ocr-mode auto|txt|ocr]
      [--to DEST] [--recursive] [--reconvert] [--overwrite-edited] PATH...
  python scripts/ingest.py run --route cloud [--model-version vlm|pipeline] [--language CODE] [--ocr] [--to DEST] PATH...
  python scripts/ingest.py run --to manuscript --route pandoc [--track-changes all|accept|reject] PATH...
  python scripts/ingest.py run --import-id ID          continue an import: open, interrupted, and failed items
  python scripts/ingest.py status [--import-id ID]
  python scripts/ingest.py verify [SOURCE_ID ...]
  python scripts/ingest.py metadata SOURCE_ID [--type TYPE] [--title TEXT] [--author "Family, Given" ...] [--year YEAR]
      [--doi DOI] [--journal TEXT] [--field NAME=VALUE ...] [--key KEY] [--source document|researcher|registry]
  python scripts/ingest.py note --import-id ID --role ROLE --reason TEXT PATH...
DEST is "references" (the default), manuscript, reviews/<venue-id>/<round-id>, or research/feedback/<feedback-id>.
Markdown and plain text need no route.
The cloud route needs a confirmed choice that names mineru.net in requirements/privacy.md and the
MINERU_API_TOKEN credential, entered with scripts/credentials.py.
Exit status: 0 done, 1 some items failed, 2 stopped or still processing (continue later), 3 refused.
Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from credentials import load_env_local  # noqa: E402
from ingestion import extraction, library, reviews  # noqa: E402
from ingestion.common import LockedError, Redactor, WorkspaceLock, sha256_file  # noqa: E402
from ingestion.pipeline import Pipeline, list_files  # noqa: E402
from ingestion.records import LABELS, ImportRecord, display_path  # noqa: E402
from ingestion.routes import (DIRECT_KINDS, OCR_MODES, TIERS, CloudRoute, LocalRoute, PandocRoute, handler_for, kind_of,  # noqa: E402
                              unsupported_reason)

ROOT = Path(__file__).resolve().parent.parent
TOKEN = "MINERU_API_TOKEN"
ROLES = ("reference", "review", "manuscript", "template", "feedback", "other")


class Refused(Exception):
    pass


def destination(value: str) -> str:
    value = value.strip().strip("/")
    if value != "references":
        reviews.open_destination(Path("."), value)
    return value


def cloud_route(root: Path, options: dict) -> CloudRoute:
    privacy = root / "requirements" / "privacy.md"
    if "mineru.net" not in (privacy.read_text(encoding="utf-8").lower() if privacy.is_file() else ""):
        raise Refused("requirements/privacy.md has no confirmed processing choice that names mineru.net. "
                      "Record the researcher's confirmed cloud choice and the documents it covers first.")
    token = os.environ.get(TOKEN) or load_env_local(root).get(TOKEN)
    if not token:
        raise Refused(f"the {TOKEN} credential is not set. The researcher enters it privately with "
                      f"python scripts/credentials.py set {TOKEN} (see the environment-management skill).")
    return CloudRoute(token, model_version=options.get("model_version", "vlm"), language=options.get("language", "ch"),
                      is_ocr=options.get("is_ocr", False), base_url=os.environ.get("INGEST_MINERU_API_URL") or None,
                      poll_interval=float(os.environ.get("INGEST_POLL_INTERVAL", "10")),
                      poll_timeout=float(os.environ.get("INGEST_POLL_TIMEOUT", "3600")), redact=Redactor([token]))


def pandoc_route(root: Path, options: dict) -> PandocRoute:
    from export import tools
    found = tools.find(root)["pandoc"]
    if not found:
        raise Refused("Pandoc is not installed for this workspace. Install it with the researcher's consent: "
                      "python scripts/export.py install --component pandoc (see the submission-assembly skill).")
    return PandocRoute(found, options.get("track_changes", "all"))


def local_route(root: Path, options: dict) -> LocalRoute:
    command = json.loads(os.environ["INGEST_MINERU_KIT"]) if os.environ.get("INGEST_MINERU_KIT") else None
    route = LocalRoute(root, options["tier"], options.get("ocr_mode", "auto"), command=command)
    if not route.command:
        raise Refused("MinerU is not installed for this workspace. Install it with the researcher's consent: "
                      "python scripts/setup_mineru.py install (see the source-ingestion skill).")
    return route


def summary(record: ImportRecord) -> str:
    counts = record.counts()
    order = ("converted", "needs-review", "partial", "already-imported", "duplicate", "unsupported", "failed", "submitted",
             "pending", "converting", "not-routed")
    parts = [f"{counts[status]} {LABELS[status]}" for status in order if counts.get(status)]
    lines = [f"Import {record.id}: " + (", ".join(parts) or "nothing to import") + ".",
             f"Record: inbox/imports/{record.id}/README.md"]
    attention = [item for item in record.items if item["status"] in ("needs-review", "partial", "failed", "unsupported", "submitted", "pending")]
    if attention:
        lines.append("Needs attention:")
        for item in attention:
            detail = item.get("error") or "; ".join(item.get("notes") or [])
            lines.append(f"  - {item['input']}: {LABELS[item['status']]}" + (f" ({detail})" if detail else ""))
    left = record.data.get("folders_left_out")
    if left:
        lines.append("Folders not included (subfolders need --recursive): " + ", ".join(left))
    stopped = record.data.get("stopped")
    if stopped:
        lines.append(f"Stopped: {stopped['message']}. Continue with: python scripts/ingest.py run --import-id {record.id}")
    return "\n".join(lines)


def command_plan(args, root: Path) -> int:
    rows, seen = [], {}
    for value in args.paths:
        path = Path(value).expanduser().resolve()
        if not path.exists():
            rows.append({"input": value, "status": "missing", "detail": "not found"})
            continue
        files, skipped = list_files(root, path, args.recursive)
        for folder in skipped:
            rows.append({"input": display_path(folder, root), "status": "folder left out", "detail": "use --recursive to include it"})
        for file in files:
            shown, sha, kind = display_path(file, root), sha256_file(file), kind_of(file)
            row = {"input": shown, "kind": kind, "bytes": file.stat().st_size, "sha256": sha}
            handler = handler_for(kind, args.route) if args.route or kind in DIRECT_KINDS else None
            if sha in seen:
                row.update(status="duplicate", detail=f"same content as {seen[sha]}")
            elif args.to == "references" and library.lookup(root, sha) and library.provenance(root, library.lookup(root, sha)):
                row.update(status="already imported", detail=library.lookup(root, sha))
            elif handler is None and not args.route and kind not in DIRECT_KINDS:
                row.update(status="needs a processing route", detail=f"a {kind} file is converted locally or with mineru.net")
            elif handler is None:
                row.update(status="not supported", detail=unsupported_reason(kind, args.route))
            else:
                row.update(status="to convert", detail=handler)
            seen.setdefault(sha, shown)
            rows.append(row)
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return 0
    counts = Counter(row["status"] for row in rows)
    print("Plan: " + ", ".join(f"{count} {status}" for status, count in counts.items()) + f" (destination: {args.to}).")
    for row in rows[:200]:
        print(f"  - {row['input']}: {row['status']}" + (f" ({row['detail']})" if row.get("detail") else ""))
    if len(rows) > 200:
        print(f"  ... and {len(rows) - 200} more; use --json for the full list")
    return 0


def command_run(args, root: Path) -> int:
    with WorkspaceLock(root):
        if args.import_id:
            record = ImportRecord.load(root, args.import_id)
            if args.route and args.route != record.data.get("route"):
                raise Refused(f"import {record.id} uses the {record.data.get('route') or 'direct'} route; start a new import for another route")
            options = record.data.get("options") or {}
        else:
            if not args.paths:
                raise Refused("name the files or folders to import, or --import-id to continue an import")
            missing = [value for value in args.paths if not Path(value).expanduser().exists()]
            if missing:
                raise Refused("not found: " + ", ".join(missing))
            if args.route == "local" and not args.tier:
                raise Refused("the local route needs --tier (flash, basic, standard, or advanced)")
            if args.route == "pandoc" and args.to != "manuscript":
                raise Refused("the pandoc route is only for the researcher's own manuscript (--to manuscript); "
                              "references and review documents are converted with MinerU")
            options = {"tier": args.tier, "ocr_mode": args.ocr_mode} if args.route == "local" else \
                {"model_version": args.model_version, "language": args.language, "is_ocr": args.ocr} if args.route == "cloud" else \
                {"track_changes": args.track_changes} if args.route == "pandoc" else {}
            if not args.route:
                kinds = {kind_of(file) for value in args.paths
                         for file in list_files(root, Path(value).expanduser().resolve(), args.recursive)[0]}
                needing = sorted(kind for kind in kinds if kind not in DIRECT_KINDS)
                if needing:
                    raise Refused(f"these files need a processing route that the researcher confirmed (--route local or cloud): {', '.join(needing)}")
        route = record.data.get("route") if args.import_id else args.route
        local = local_route(root, options) if route == "local" else None
        cloud = cloud_route(root, options) if route == "cloud" else None
        pandoc = pandoc_route(root, options) if route == "pandoc" else None
        if not args.import_id:
            inputs = [display_path(Path(value).expanduser().resolve(), root) for value in args.paths]
            record = ImportRecord.create(root, args.to, route, inputs, args.recursive)
            record.data["options"] = options
        pipeline = Pipeline(root, record, local=local, cloud=cloud, pandoc=pandoc, redact=cloud.redact if cloud else Redactor(),
                            reconvert=args.reconvert, overwrite_edited=args.overwrite_edited)
        if not args.import_id:
            pipeline.add_inputs(record.data["inputs"], args.recursive)
        try:
            code = pipeline.run()
        finally:
            print(summary(record))
    return code


def command_status(args, root: Path) -> int:
    records = [ImportRecord.load(root, args.import_id)] if args.import_id else ImportRecord.all(root)[-5:]
    if not records:
        print("No imports yet.")
    for record in records:
        print(summary(record))
    return 0


def command_verify(args, root: Path) -> int:
    folder = root / "references" / "extracted"
    sources = args.sources or sorted(p.name for p in folder.iterdir() if p.is_dir() and p.name.startswith("src-")) if folder.is_dir() else args.sources
    index = (root / "references" / "index.md").read_text(encoding="utf-8") if (root / "references" / "index.md").is_file() else ""
    problems = []
    for source_id in sources:
        record = library.provenance(root, source_id)
        here = library.extracted(root, source_id)
        if not record:
            problems.append(f"{source_id}: no provenance.json")
            continue
        original = root / record["original"]["file"]
        if not original.is_file():
            problems.append(f"{source_id}: the original {record['original']['file']} is missing")
        elif sha256_file(original) != record["original"]["sha256"]:
            problems.append(f"{source_id}: the original no longer matches its checksum")
        if library.edited(root, source_id):
            problems.append(f"{source_id}: document.md was edited after conversion")
        document = here / "document.md"
        if document.is_file():
            for target in extraction.local_targets(document.read_text(encoding="utf-8")):
                if not (here / target).is_file():
                    problems.append(f"{source_id}: broken link {target}")
        else:
            problems.append(f"{source_id}: document.md is missing")
        for readme in (here / "README.md", here / "assets" / "README.md", here / "native" / "README.md",
                       library.originals(root, source_id) / "README.md"):
            if not readme.is_file():
                problems.append(f"{source_id}: {readme.relative_to(root).as_posix()} is missing")
        if f"| {source_id} |" not in index:
            problems.append(f"{source_id}: not listed in references/index.md")
    for problem in problems:
        print(problem)
    print(f"Checked {len(sources)} source(s): " + ("no problems." if not problems else f"{len(problems)} problem(s)."))
    return 1 if problems else 0


def command_metadata(args, root: Path) -> int:
    if not library.originals(root, args.source_id).is_dir():
        raise Refused(f"{args.source_id} is not in the reference library")
    values = {"title": args.title, "author": " and ".join(args.author) if args.author else None, "year": args.year,
              "doi": args.doi, "journal": args.journal, "metadatasource": args.source}
    for pair in args.field or []:
        name, separator, value = pair.partition("=")
        if not separator or not name.strip():
            raise Refused(f"--field needs NAME=VALUE, not {pair!r}")
        values[name.strip().lower()] = value.strip()
    key, note = library.bib_upsert(root, args.source_id, args.type, values, args.key)
    library.index_upsert(root, args.source_id, title=args.title, authors="; ".join(args.author) if args.author else None, year=args.year)
    print(f"{args.source_id}: citation key {key}" + (f" ({note})" if note else "") + ".")
    return 0


def command_note(args, root: Path) -> int:
    record = ImportRecord.load(root, args.import_id)
    for value in args.paths:
        path = Path(value).expanduser().resolve()
        if not path.is_file():
            raise Refused(f"not a file: {value}")
        shown = display_path(path, root)
        item = next((i for i in record.items if i["input"] == shown), None)
        if item is None:
            item = {"input": shown, "name": path.name, "sha256": sha256_file(path), "bytes": path.stat().st_size, "kind": kind_of(path)}
            record.items.append(item)
        item.update(status="not-routed", role=args.role, notes=[args.reason])
    record.save()
    print(summary(record))
    return 0


def main(argv: list | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Import documents with MinerU and keep a resumable record.")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    commands = parser.add_subparsers(dest="command", required=True)

    plan = commands.add_parser("plan", help="list what an import would do, without changing anything")
    plan.add_argument("paths", nargs="+")
    plan.add_argument("--to", type=destination, default="references")
    plan.add_argument("--route", choices=("local", "cloud", "pandoc"))
    plan.add_argument("--recursive", action="store_true")
    plan.add_argument("--json", action="store_true")

    run = commands.add_parser("run", help="import files or folders, or continue an import")
    run.add_argument("paths", nargs="*")
    run.add_argument("--import-id")
    run.add_argument("--to", type=destination, default="references")
    run.add_argument("--route", choices=("local", "cloud", "pandoc"))
    run.add_argument("--track-changes", dest="track_changes", choices=("all", "accept", "reject"), default="all",
                     help="pandoc route: keep Word comments and tracked changes as marks (all), or apply the researcher's choice")
    run.add_argument("--tier", choices=TIERS)
    run.add_argument("--ocr-mode", choices=OCR_MODES, default="auto")
    run.add_argument("--model-version", choices=("vlm", "pipeline"), default="vlm")
    run.add_argument("--language", default="ch")
    run.add_argument("--ocr", action="store_true", help="cloud route: force OCR")
    run.add_argument("--recursive", action="store_true")
    run.add_argument("--reconvert", action="store_true", help="convert again even when an earlier conversion exists")
    run.add_argument("--overwrite-edited", action="store_true", help="replace Markdown that was edited by hand")

    status = commands.add_parser("status", help="show the state of recent imports")
    status.add_argument("--import-id")

    verify = commands.add_parser("verify", help="check library extractions against their records")
    verify.add_argument("sources", nargs="*")

    metadata = commands.add_parser("metadata", help="write citation metadata for a source")
    metadata.add_argument("source_id")
    metadata.add_argument("--type", default=None)
    metadata.add_argument("--title")
    metadata.add_argument("--author", action="append")
    metadata.add_argument("--year")
    metadata.add_argument("--doi")
    metadata.add_argument("--journal")
    metadata.add_argument("--field", action="append")
    metadata.add_argument("--key")
    metadata.add_argument("--source", choices=("document", "researcher", "registry"), default="document")

    note = commands.add_parser("note", help="record items of an import that are kept for later")
    note.add_argument("paths", nargs="+")
    note.add_argument("--import-id", required=True)
    note.add_argument("--role", choices=ROLES, required=True)
    note.add_argument("--reason", required=True)

    args = parser.parse_args(argv)
    root = args.root.resolve()
    handlers = {"plan": command_plan, "run": command_run, "status": command_status, "verify": command_verify,
                "metadata": command_metadata, "note": command_note}
    try:
        return handlers[args.command](args, root)
    except (Refused, LockedError, ValueError, FileNotFoundError) as error:
        print(f"Refused: {error}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
