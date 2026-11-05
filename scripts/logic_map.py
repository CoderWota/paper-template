"""Track which saved inputs an agent compared with an internal argument map.

This module fingerprints files. It neither derives an argument nor certifies its validity.
Target-relative inputs let a revision candidate and its synchronization record move together.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

from ingestion.common import sha256_file, write_json_atomic

MAP = "logic-map.md"
RECORD = "logic-map.sync.json"
SCHEMA = "paper-template.logic-map-sync/1"
SCAFFOLD = "No manuscript logic map yet"
SHARED_INPUTS = ("requirements/project.md", "requirements/writing.md", "references/bibliography.bib", "docs/logic-map-guide.md")


def _path(root: Path, target: Path, base: str, name: str) -> Path:
    if base not in ("target", "workspace") or not isinstance(name, str):
        raise ValueError("invalid logic-map input scope")
    relative = Path(name)
    if (relative.is_absolute() or not relative.parts or "\\" in name
            or any(part == ".." or part.startswith(".") for part in relative.parts)):
        raise ValueError(f"logic-map input must be a non-private relative project file: {name}")
    parent = (target if base == "target" else root).resolve()
    path = (parent / relative).resolve()
    if parent not in path.parents:
        raise ValueError(f"logic-map input leaves its {base}: {name}")
    if path in ((target / MAP).resolve(), (target / RECORD).resolve()):
        raise ValueError("the map and its sync record cannot be dependency inputs")
    return path


def _specs(root: Path, target: Path, local_files: list[str], dependencies: list[dict]) -> list[dict]:
    entries = {("target", name) for name in local_files}
    entries.update(("workspace", name) for name in SHARED_INPUTS if (root / name).is_file())
    for item in dependencies:
        if not isinstance(item, dict) or set(item) != {"base", "path"}:
            raise ValueError("invalid logic-map dependency entry")
        entries.add((item["base"], item["path"]))
    for base, name in entries:
        _path(root, target, base, name)
    return [{"base": base, "path": name} for base, name in sorted(entries)]


def _inventory(root: Path, target: Path, specs: list[dict]) -> dict:
    result = {}
    for item in specs:
        path = _path(root, target, item["base"], item["path"])
        result[(item["base"], item["path"])] = sha256_file(path) if path.is_file() else None
    return result


def _map_state(target: Path) -> tuple[str | None, str]:
    path = target / MAP
    if target.resolve() not in path.resolve().parents:
        return "invalid", "the map leaves its manuscript target"
    if not path.is_file():
        return "missing", "the internal argument map is missing"
    text = path.read_text(encoding="utf-8")
    if SCAFFOLD in text:
        return "scaffold", "the map is still the template scaffold"
    if not re.search(r"(?m)^ {0,3}(?:`{3,}|~{3,})mermaid\s*$", text):
        return "invalid", "the map has no Mermaid block"
    return None, ""


def _load(root: Path, target: Path) -> dict:
    data = json.loads((target / RECORD).read_text(encoding="utf-8"))
    if (not isinstance(data, dict) or data.get("schema") != SCHEMA
            or not isinstance(data.get("inputs"), list)
            or not isinstance(data.get("dependencies"), list)
            or not isinstance(data.get("recorded_at"), str)
            or not isinstance(data.get("map_sha256"), str)
            or not re.fullmatch(r"[0-9a-f]{64}", data["map_sha256"])):
        raise ValueError("invalid logic-map synchronization record")
    seen = set()
    for item in data["inputs"]:
        if not isinstance(item, dict) or set(item) != {"base", "path", "sha256"}:
            raise ValueError("invalid logic-map input entry")
        _path(root, target, item["base"], item["path"])
        key = (item["base"], item["path"])
        if key in seen or not isinstance(item["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
            raise ValueError("invalid or duplicate logic-map input fingerprint")
        seen.add(key)
    _specs(root, target, [], data["dependencies"])
    return data


def status(root: Path, target: Path, local_files: list[str]) -> dict:
    """Report saved-file synchronization, including edits made directly by the author."""
    try:
        if root.resolve() not in target.resolve().parents:
            raise ValueError("the manuscript target leaves the workspace")
        if target.resolve() not in (target / RECORD).resolve().parents:
            raise ValueError("the synchronization record leaves its manuscript target")
        state, detail = _map_state(target)
    except (OSError, ValueError) as error:
        state, detail = "invalid", str(error)
    result = {"state": state, "detail": detail, "changed": [], "recorded_at": None, "dependencies": []}
    if state:
        return result
    if not (target / RECORD).is_file():
        return {**result, "state": "unrecorded", "detail": "no semantic synchronization has been recorded"}
    try:
        data = _load(root, target)
        current = _inventory(root, target, _specs(root, target, local_files, data["dependencies"]))
        previous = {(item["base"], item["path"]): item["sha256"] for item in data["inputs"]}
    except (OSError, ValueError, TypeError, KeyError) as error:
        return {**result, "state": "invalid", "detail": str(error)}
    changed = []
    for base, name in sorted(current.keys() | previous.keys()):
        key = (base, name)
        if key not in current:
            reason = "no longer selected"
        elif current[key] is None:
            reason = "missing"
        elif key not in previous:
            reason = "added"
        elif current[key] != previous[key]:
            reason = "changed"
        else:
            continue
        changed.append(f"{base}/{name} ({reason})")
    if sha256_file(target / MAP) != data["map_sha256"]:
        changed.append(f"target/{MAP} (map edited)")
    return {"state": "stale" if changed else "current",
            "detail": "saved inputs changed; inspect and synchronize the argument map" if changed else "recorded input fingerprints match",
            "changed": changed, "recorded_at": data["recorded_at"], "dependencies": data["dependencies"]}


def record(root: Path, target: Path, local_files: list[str], inputs: list[str], replace_inputs: bool = False) -> dict:
    """Record inputs only after the agent has compared and, where needed, updated the map."""
    if root.resolve() not in target.resolve().parents:
        raise ValueError("the manuscript target leaves the workspace")
    if target.resolve() not in (target / RECORD).resolve().parents:
        raise ValueError("the synchronization record leaves its manuscript target")
    state, detail = _map_state(target)
    if state:
        raise ValueError(detail)
    dependencies = []
    if not replace_inputs and (target / RECORD).is_file():
        try:
            dependencies = _load(root, target)["dependencies"]
        except (OSError, ValueError, TypeError, KeyError) as error:
            raise ValueError("inspect the invalid synchronization record before replacing its inputs with --replace-inputs") from error
    for name in inputs:
        path = _path(root, target, "workspace", name)
        if target.resolve() in path.parents:
            dependencies.append({"base": "target", "path": path.relative_to(target.resolve()).as_posix()})
        else:
            dependencies.append({"base": "workspace", "path": path.relative_to(root.resolve()).as_posix()})
    dependencies = [dict(base=base, path=name) for base, name in sorted({(d["base"], d["path"]) for d in dependencies})]
    inventory = _inventory(root, target, _specs(root, target, local_files, dependencies))
    missing = [f"{base}/{name}" for (base, name), digest in inventory.items() if digest is None]
    if missing:
        raise ValueError("logic-map input files are missing: " + ", ".join(missing))
    data = {"schema": SCHEMA, "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "map_sha256": sha256_file(target / MAP), "dependencies": dependencies,
            "inputs": [{"base": base, "path": name, "sha256": digest}
                       for (base, name), digest in sorted(inventory.items())]}
    write_json_atomic(target / RECORD, data)
    return status(root, target, local_files)
