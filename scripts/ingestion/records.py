"""Import records in inbox/imports/<import-id>/: what was received, where each item went, and what is open.

The record is the resumable state of a batch. It is saved after every change, so an interrupted
run continues from it. Paths outside the workspace are stored with the home folder as "~".
"""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path

from .common import now, read_json, slug, today, update_readme, write_json_atomic

SCHEMA = "paper-template.import/1"
# Items in these states are worked on again when the import continues.
OPEN = ("pending", "converting", "submitted", "failed")
DONE = ("converted", "needs-review", "partial", "already-imported")
LABELS = {
    "converted": "converted", "needs-review": "converted, needs review", "partial": "partly converted",
    "already-imported": "already imported", "duplicate": "duplicate in this batch", "unsupported": "not supported",
    "failed": "failed", "pending": "waiting", "converting": "interrupted", "submitted": "processing at mineru.net",
    "not-routed": "kept for later",
}


def display_path(path: Path, root: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError:
        pass
    home = Path.home().resolve()
    try:
        return "~/" + resolved.relative_to(home).as_posix()
    except ValueError:
        return str(resolved)


def resolve_display(value: str, root: Path) -> Path:
    if value.startswith("~/"):
        return Path(os.path.expanduser(value))
    path = Path(value)
    return path if path.is_absolute() else root / path


class ImportRecord:
    def __init__(self, root: Path, data: dict):
        self.root, self.data = root, data

    @property
    def id(self) -> str:
        return self.data["import_id"]

    @property
    def folder(self) -> Path:
        return self.root / "inbox" / "imports" / self.id

    @property
    def items(self) -> list:
        return self.data["items"]

    @classmethod
    def create(cls, root: Path, destination: str, route: str | None, inputs: list, recursive: bool) -> "ImportRecord":
        base = f"{today()}-{slug(Path(inputs[0]).stem if inputs else 'import', limit=30, fallback='import')}"
        imports = root / "inbox" / "imports"
        import_id, number = base, 2
        while (imports / import_id).exists():
            import_id, number = f"{base}-{number}", number + 1
        data = {"schema": SCHEMA, "import_id": import_id, "created_at": now(), "updated_at": now(),
                "destination": destination, "route": route, "inputs": inputs, "recursive": recursive,
                "items": [], "stopped": None}
        record = cls(root, data)
        record.save()
        return record

    @classmethod
    def load(cls, root: Path, import_id: str) -> "ImportRecord":
        data = read_json(root / "inbox" / "imports" / import_id / "import.json")
        if not isinstance(data, dict) or data.get("schema") != SCHEMA:
            raise FileNotFoundError(f"no import record named {import_id!r}")
        return cls(root, data)

    @classmethod
    def all(cls, root: Path) -> list:
        records = []
        for path in sorted((root / "inbox" / "imports").glob("*/import.json")):
            data = read_json(path)
            if isinstance(data, dict) and data.get("schema") == SCHEMA:
                records.append(cls(root, data))
        return sorted(records, key=lambda record: record.data.get("created_at", ""))

    def find(self, sha: str) -> dict | None:
        return next((item for item in self.items if item.get("sha256") == sha), None)

    def counts(self) -> Counter:
        return Counter(item["status"] for item in self.items)

    def save(self) -> None:
        self.data["updated_at"] = now()
        write_json_atomic(self.folder / "import.json", self.data)
        update_readme(self.folder / "README.md", f"Import {self.id}", self.readme())

    def readme(self) -> str:
        destination = self.data["destination"]
        where = "the reference library (`references/`)" if destination == "references" else f"the review round `{destination}/`"
        route = {"local": "MinerU on this computer", "cloud": "the mineru.net service"}.get(self.data.get("route") or "", "direct reading only")
        counts = ", ".join(f"{count} {LABELS.get(status, status)}" for status, count in sorted(self.counts().items())) or "no items yet"
        lines = [
            f"Import `{self.id}`, started {self.data['created_at']} and last updated {self.data['updated_at']}. "
            f"Material from {', '.join(f'`{value}`' for value in self.data['inputs'])} went to {where}, converted with {route}. "
            f"State: {counts}.",
            "",
            "| Input | Status | Result | Notes |",
            "| --- | --- | --- | --- |",
        ]
        for item in self.items:
            result = item.get("result")
            link = f"[{item.get('target', 'result')}](../../../{result})" if result else ""
            notes = "; ".join(item.get("notes") or [])
            if item.get("error"):
                notes = "; ".join(filter(None, [item["error"], notes]))
            cells = [item["input"], LABELS.get(item["status"], item["status"]), link, notes]
            lines.append("| " + " | ".join(cell.replace("|", "\\|").replace("\n", " ") for cell in cells) + " |")
        stopped = self.data.get("stopped")
        if stopped:
            lines += ["", f"The run stopped before finishing: {stopped['message']} ({stopped['at']}). Continuing this import picks up the open items."]
        lines += ["", "The machine-readable record is [`import.json`](import.json). Input files were not changed; originals are archived "
                  "with their destination, and an adopted manuscript would be kept here."]
        return "\n".join(lines)
