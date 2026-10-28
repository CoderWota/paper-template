"""Run an import: archive, convert, check, and publish each item, saving the record after every step.

Items are independent. A failed document does not stop the others; a failure that would repeat
for every document (a rejected token, an exhausted quota, missing models) stops the run, and the
open items continue when the import runs again. Nothing switches to another route.
"""

from __future__ import annotations

import shutil
import time
from pathlib import Path

from . import extraction, library, reviews
from .common import Log, Redactor, is_ignored, now, relative, sha256_file, settings_key, today, write_json_atomic
from .records import OPEN, ImportRecord, display_path, resolve_display
from .routes import (CLOUD_BATCH, CLOUD_PACE, MAX_UPLOAD, VERIFIED, BatchStop, ConversionError, DirectRoute, handler_for,
                     kind_of, unsupported_reason)

STATUS_WORDS = {"complete": "complete", "needs-review": "needs review", "partial": "partial"}


def list_files(root: Path, path: Path, recursive: bool) -> tuple:
    """(files, folders left out) under path. Workspace READMEs and import records are not material."""
    if path.is_file():
        return [path], []
    files, skipped = [], []
    imports = (root / "inbox" / "imports").resolve()
    for entry in sorted(path.iterdir(), key=lambda p: p.name):
        if is_ignored(entry):
            continue
        if entry.is_dir():
            if entry.resolve() == imports:
                continue
            if recursive:
                more, deeper = list_files(root, entry, True)
                files += more
                skipped += deeper
            else:
                skipped.append(entry)
        elif entry.is_file():
            if entry.name == "README.md" and relative(entry, root) != str(entry):
                continue
            files.append(entry)
    return files, skipped


def coverage_words(coverage: dict) -> str:
    if coverage.get("unit") == "page" and coverage.get("expected"):
        return f"{coverage.get('processed', 0)} of {coverage['expected']} pages"
    if coverage.get("unit") == "page":
        return "page count unknown"
    return "whole document" if coverage.get("status") == "complete" else "coverage unknown"


class Pipeline:
    def __init__(self, root: Path, record: ImportRecord, *, local=None, cloud=None, redact: Redactor | None = None,
                 reconvert: bool = False, overwrite_edited: bool = False, emit=print):
        self.root, self.record = root, record
        self.route = record.data.get("route")
        self.local, self.cloud, self.direct = local, cloud, DirectRoute()
        self.redact = redact or Redactor()
        self.log = Log(root, record.id, self.redact)
        self.reconvert, self.overwrite_edited, self.emit = reconvert, overwrite_edited, emit
        destination = record.data["destination"]
        self.round = None if destination == "references" else reviews.Round(root, *reviews.parse_destination(destination))
        self.work = root / ".tmp" / "ingest" / record.id

    # Collecting the items

    def add_inputs(self, inputs: list, recursive: bool) -> None:
        for value in inputs:
            path = resolve_display(value, self.root)
            files, skipped = list_files(self.root, path, recursive)
            for folder in skipped:
                left = self.record.data.setdefault("folders_left_out", [])
                shown = display_path(folder, self.root)
                if shown not in left:
                    left.append(shown)
            for file in files:
                self.add_file(file)
        given = set(inputs)
        left = [folder for folder in self.record.data.get("folders_left_out", []) if folder not in given]
        if left:
            self.record.data["folders_left_out"] = left
        else:
            self.record.data.pop("folders_left_out", None)
        self.record.save()

    def add_file(self, path: Path) -> None:
        shown = display_path(path, self.root)
        if any(item["input"] == shown for item in self.record.items):
            return
        sha = sha256_file(path)
        item = {"input": shown, "name": path.name, "sha256": sha, "bytes": path.stat().st_size, "kind": kind_of(path),
                "status": "pending", "notes": []}
        twin = self.record.find(sha)
        if twin:
            item.update(status="duplicate", notes=[f"same content as {twin['input']}"])
        self.record.items.append(item)

    # Running

    def save(self) -> None:
        self.record.save()

    def settings_for(self, item: dict) -> dict:
        handler = handler_for(item["kind"], self.route)
        if handler == "local":
            return self.local.settings(item["kind"])
        if handler == "cloud":
            return self.cloud.settings(item["kind"])
        return self.direct.settings(item["kind"])

    def run(self) -> int:
        self.record.data["stopped"] = None
        queue = []
        try:
            for item in self.record.items:
                if item["status"] not in OPEN:
                    continue
                if item["status"] == "submitted":
                    queue.append(item)
                    continue
                handler = handler_for(item["kind"], self.route)
                if handler is None:
                    item.update(status="unsupported", notes=[unsupported_reason(item["kind"], self.route or "direct")])
                    self.save()
                    continue
                if handler == "cloud":
                    self.prepare(item)
                    if item["status"] in OPEN:
                        queue.append(item)
                    continue
                self.convert_now(item, handler)
            if queue:
                self.cloud_items(queue)
        except BatchStop as stop:
            self.record.data["stopped"] = {"code": stop.code, "message": str(stop), "at": now()}
            self.log.write(f"run stopped: {stop.code}: {stop}")
            self.save()
            return 2
        finally:
            shutil.rmtree(self.work, ignore_errors=True)
        self.save()
        counts = self.record.counts()
        if counts.get("submitted"):
            return 2
        return 1 if counts.get("failed") else 0

    def prepare(self, item: dict) -> Path | None:
        """Archive the original (once) and recognize an earlier result. Returns the archived file."""
        if item.get("archived") and (self.root / item["archived"]).is_file():
            archived = self.root / item["archived"]
        else:
            source = resolve_display(item["input"], self.root)
            if not source.is_file():
                self.fail(item, ConversionError("the input file is no longer where it was"))
                return None
            if sha256_file(source) != item["sha256"]:
                self.fail(item, ConversionError("the input file changed after the import started; import it again as a new item"))
                return None
            if self.round:
                self.round.ensure()
                target, archived, _ = self.round.archive(source, item["sha256"])
            else:
                target, archived, _ = library.archive(self.root, source, item["sha256"], item["input"], today())
            item.update(target=target, archived=relative(archived, self.root))
        if not self.reconvert:
            earlier = self.earlier(item)
            if earlier:
                item.update(status="already-imported", result=self.result_path(item), notes=[earlier])
                if not self.round:
                    record = library.provenance(self.root, item["target"]) or {}
                    library.index_upsert(self.root, item["target"], default_title=f"(file) {item['name']}",
                                         extraction=self.extraction_cell(record), files=self.files_cell(item["target"]))
        self.save()
        return archived

    def earlier(self, item: dict) -> str | None:
        """A note when a usable earlier conversion of this file exists, otherwise None."""
        key = settings_key(self.settings_for(item))
        if self.round:
            entry = self.round.record()["documents"].get(item["target"])
            found = entry.get("settings_key") if entry else None
        else:
            record = library.provenance(self.root, item["target"])
            found = (record.get("conversion") or {}).get("settings_key") if record else None
        if not found:
            return None
        if found == key:
            return "converted earlier with the same settings"
        return "converted earlier with other settings; convert it again only if the researcher asks"

    def result_path(self, item: dict) -> str:
        if self.round:
            return relative(self.round.markdown / f"{item['target']}.md", self.root)
        return f"references/extracted/{item['target']}/document.md"

    def convert_now(self, item: dict, handler: str) -> None:
        archived = self.prepare(item)
        if archived is None or item["status"] not in OPEN:
            return
        item.update(status="converting", attempts=item.get("attempts", 0) + 1)
        item.pop("error", None)
        self.save()
        work = self.work / item["sha256"][:16]
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        started = now()
        try:
            if handler == "local":
                raw, notes = self.local.convert(archived, work, item["kind"]), []
            else:
                raw, notes = self.direct.convert(archived, work, item["kind"], resolve_display(item["input"], self.root).parent)
            self.finish(item, raw, work, archived, started, notes, self.settings_for(item))
        except ConversionError as error:
            self.fail(item, error)
        except library.EditedError as error:
            self.fail(item, ConversionError(f"{error}; keep the hand edits in the source note, then convert again with --overwrite-edited", "edited"))
        except BatchStop:
            item["status"] = "pending"
            self.save()
            raise
        except OSError as error:
            # For example a result file that another program holds open on Windows.
            self.fail(item, ConversionError(f"the result could not be written: {error}", "write"))
        finally:
            shutil.rmtree(work, ignore_errors=True)

    def finish(self, item: dict, raw: Path, work: Path, archived: Path, started: str, notes: list, settings: dict) -> None:
        stage, kind = work / "stage", item["kind"]
        if self.round:
            document_id = item["target"]
            if reviews.edited(self.round, document_id) and not self.overwrite_edited:
                raise library.EditedError(f"{relative(self.round.markdown / (document_id + '.md'), self.root)} was edited after conversion")
            result = extraction.build(raw, kind=kind, original=archived, document=stage / "document.md", asset_dir=stage / "assets",
                                      asset_link="../assets/", asset_prefix=f"{document_id}--")
            summary, section, extra = reviews.inspect(archived, kind)
            if section:
                with open(stage / "document.md", "a", encoding="utf-8", newline="\n") as stream:
                    stream.write(section)
            result.warnings += extra
        else:
            library.carry_readmes(self.root, item["target"], stage)
            result = extraction.build(raw, kind=kind, original=archived, document=stage / "document.md", asset_dir=stage / "assets",
                                      asset_link="assets/", native_dir=stage / "native")
            summary = None
        if settings["route"] == "direct":
            # Nothing was transcribed: the text is the original, so coverage is whole and formulas are as written.
            result.coverage = {"unit": "document", "status": "complete", "method": "read directly"}
            result.warnings = [w for w in result.warnings if w["code"] not in ("formulas-unverified", "coverage-unknown")]
        for note in notes:
            result.warn("not-utf8", note)
        if (settings["route"], kind, settings.get("tier", "")) not in VERIFIED:
            result.warn("unverified-format", f"converting {kind} files this way is documented by MinerU but not yet verified in this workspace; compare the result with the original")
        conversion = dict(settings, settings_key=settings_key(settings), started_at=started, finished_at=now(), import_id=self.record.id)
        document_sha = sha256_file(stage / "document.md")
        if self.round:
            reviews.publish(self.round, item["target"], stage)
            reviews.store(self.round, item["target"], {
                "original_name": archived.name, "sha256": item["sha256"], "kind": kind, "settings_key": conversion["settings_key"],
                "conversion": conversion, "markdown": f"markdown/{item['target']}.md", "markdown_sha256": document_sha,
                "assets": result.assets, "coverage": result.coverage, "checks": result.checks, "structures": summary,
                "warnings": result.warnings, "status": result.status})
        else:
            self.publish_source(item, stage, archived, conversion, result, document_sha)
        item.update(status="converted" if result.status == "complete" else result.status, result=self.result_path(item),
                    notes=[w["message"] for w in result.warnings if w["level"] != "info"][:3])
        self.log.write(f"{item['input']}: {item['status']} ({coverage_words(result.coverage)})")
        self.save()

    def publish_source(self, item: dict, stage: Path, archived: Path, conversion: dict, result, document_sha: str) -> None:
        source_id = item["target"]
        previous = library.provenance(self.root, source_id)
        history = []
        if previous:
            history = (previous.get("previous") or [])[-4:] + [{
                "revision": previous.get("revision"), "status": previous.get("status"),
                "finished_at": (previous.get("conversion") or {}).get("finished_at"),
                "settings_key": (previous.get("conversion") or {}).get("settings_key")}]
        record = {
            "schema": "paper-template.extraction/1", "source_id": source_id,
            "revision": ((previous or {}).get("revision") or 0) + 1,
            "original": {"file": relative(archived, self.root), "sha256": item["sha256"], "bytes": item["bytes"],
                         "received_as": item["name"], "received_from": item["input"]},
            "conversion": conversion, "coverage": result.coverage,
            "outputs": {"document": "document.md", "document_sha256": document_sha, "assets": result.assets, "native": result.native},
            "checks": result.checks, "warnings": result.warnings, "hints": result.hints, "status": result.status,
            "previous": history,
        }
        write_json_atomic(stage / "provenance.json", record)
        library.write_readmes(stage, record)
        library.publish(self.root, source_id, stage, self.overwrite_edited)
        library.index_upsert(self.root, source_id, default_title=f"(file) {item['name']}", extraction=self.extraction_cell(record),
                             files=self.files_cell(source_id))

    @staticmethod
    def extraction_cell(record: dict) -> str:
        status = STATUS_WORDS.get(record.get("status"), record.get("status") or "unknown")
        if (record.get("conversion") or {}).get("route") == "direct":
            return f"{status}, read directly"
        return f"{status}, {coverage_words(record.get('coverage') or {})}"

    @staticmethod
    def files_cell(source_id: str) -> str:
        return f"[original](originals/{source_id}/) · [text](extracted/{source_id}/document.md)"

    def fail(self, item: dict, error: Exception) -> None:
        item.update(status="failed", error=self.redact(str(error)), error_code=getattr(error, "code", "failed"))
        self.log.write(f"{item['input']}: failed: {error}")
        self.save()

    # The cloud route works in batches: upload, then collect the results.

    def cloud_items(self, items: list) -> None:
        fresh = []
        for item in items:
            if item["status"] == "submitted":
                continue
            if (self.root / item["archived"]).stat().st_size > MAX_UPLOAD:
                self.fail(item, ConversionError("the file is larger than the 200 MB limit of mineru.net", "too-large"))
                continue
            fresh.append(item)
        for start in range(0, len(fresh), CLOUD_BATCH):
            if start:
                self.cloud.sleep(CLOUD_PACE)
            chunk = fresh[start:start + CLOUD_BATCH]
            # The service sees the source ID as the file name, not the researcher's file name.
            files = [{"name": f"{item['target']}{Path(item['archived']).suffix.lower()}", "data_id": item["target"],
                      "is_ocr": self.cloud.is_ocr} for item in chunk]
            batch_id, urls = self.cloud.request_uploads(files)
            for item, url, spec in zip(chunk, urls, files):
                try:
                    self.cloud.upload(url, self.root / item["archived"])
                except ConversionError as error:
                    self.fail(item, error)
                    continue
                item.update(status="submitted", attempts=item.get("attempts", 0) + 1,
                            remote={"batch_id": batch_id, "data_id": spec["data_id"], "name": spec["name"], "submitted_at": now()})
                item.pop("error", None)
                self.save()
        self.collect_cloud()

    def collect_cloud(self) -> None:
        deadline = time.monotonic() + self.cloud.poll_timeout
        interval = self.cloud.poll_interval
        while True:
            waiting = [item for item in self.record.items if item["status"] == "submitted"]
            for batch_id in sorted({item["remote"]["batch_id"] for item in waiting}):
                for result in self.cloud.results(batch_id):
                    item = next((i for i in waiting if i["status"] == "submitted" and i["remote"]["batch_id"] == batch_id
                                 and (result.get("data_id") == i["remote"]["data_id"] or result.get("file_name") == i["remote"]["name"])), None)
                    if item is None:
                        continue
                    state = result.get("state")
                    if state == "done":
                        self.cloud_done(item, result)
                    elif state == "failed":
                        self.fail(item, ConversionError(f"mineru.net could not convert the file: {result.get('err_msg') or 'no reason given'}"))
                    elif item["remote"].get("state") != state:
                        item["remote"]["state"] = state
                        self.save()
            if not any(item["status"] == "submitted" for item in self.record.items):
                return
            if time.monotonic() + interval > deadline:
                self.emit("Some documents are still being processed at mineru.net. Continue this import later to collect them.")
                return
            self.cloud.sleep(interval)
            interval = min(interval * 1.5, 60)

    def cloud_done(self, item: dict, result: dict) -> None:
        work = self.work / item["sha256"][:16]
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        try:
            raw = self.cloud.download(str(result.get("full_zip_url") or ""), work)
            self.finish(item, raw, work, self.root / item["archived"], item["remote"]["submitted_at"], [], self.cloud.settings(item["kind"]))
        except ConversionError as error:
            self.fail(item, error)
        except library.EditedError as error:
            self.fail(item, ConversionError(f"{error}; keep the hand edits in the source note, then convert again with --overwrite-edited", "edited"))
        except OSError as error:
            self.fail(item, ConversionError(f"the result could not be written: {error}", "write"))
        finally:
            shutil.rmtree(work, ignore_errors=True)
