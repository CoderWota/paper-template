"""Shared helpers for document ingestion: paths, identifiers, checksums, atomic writes, READMEs, a lock, and redaction.

Uses only the Python standard library and works on Windows, macOS, and Linux, including paths
with spaces and non-ASCII characters.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
from pathlib import Path

MANAGED_BEGIN = "<!-- maintained by scripts/ingest.py: begin -->"
MANAGED_END = "<!-- maintained by scripts/ingest.py: end -->"
# Files that are never documents, wherever they appear.
IGNORED_NAMES = frozenset({".DS_Store", "Thumbs.db", "desktop.ini"})
WINDOWS_RESERVED = frozenset({"CON", "PRN", "AUX", "NUL", *(f"COM{n}" for n in range(1, 10)), *(f"LPT{n}" for n in range(1, 10))})


def now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def today() -> str:
    return _dt.date.today().isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def settings_key(settings: dict) -> str:
    """A short, stable digest of conversion settings, used to recognize a matching earlier result."""
    return hashlib.sha256(json.dumps(settings, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def slug(text: str, limit: int = 40, fallback: str = "item") -> str:
    """An ASCII identifier fragment: lowercase letters and digits joined by hyphens."""
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-")[:limit].strip("-")
    return value or fallback


def safe_filename(name: str) -> str:
    """Keep a received file name, replacing only what Windows cannot store."""
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).rstrip(" .")
    if not cleaned or cleaned.split(".")[0].upper() in WINDOWS_RESERVED:
        cleaned = "_" + cleaned
    return cleaned


def is_ignored(path: Path) -> bool:
    name = path.name
    return name in IGNORED_NAMES or name.startswith(".") or name.startswith("~$") or name.startswith(".~lock.")


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=".writing-", dir=str(path.parent))
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        os.replace(temporary, path)
    except BaseException:
        if os.path.exists(temporary):
            os.unlink(temporary)
        raise


def write_json_atomic(path: Path, data) -> None:
    write_text_atomic(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def relative(path: Path, root: Path) -> str:
    """The workspace-relative POSIX path, or the absolute path for a file outside the workspace."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def update_readme(path: Path, title: str, body: str) -> bool:
    """Create or update a README whose maintained block holds body. Text outside the block is kept.

    Returns True when the file changed.
    """
    block = f"{MANAGED_BEGIN}\n{body.strip()}\n{MANAGED_END}"
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        if MANAGED_BEGIN in text and MANAGED_END in text:
            start = text.index(MANAGED_BEGIN)
            end = text.index(MANAGED_END) + len(MANAGED_END)
            new = text[:start] + block + text[end:]
        else:
            new = text.rstrip("\n") + "\n\n" + block + "\n"
    else:
        text = ""
        new = f"# {title}\n\n{block}\n"
    if new == text:
        return False
    write_text_atomic(path, new)
    return True


class Redactor:
    """Removes secrets, bearer tokens, and signed query strings from text before it is logged or stored."""

    def __init__(self, secrets: list[str] | None = None):
        self.secrets = sorted({s for s in (secrets or []) if s and len(s) >= 4}, key=len, reverse=True)

    def __call__(self, text: str) -> str:
        for secret in self.secrets:
            text = text.replace(secret, "[redacted]")
        text = re.sub(r"(?i)(bearer\s+)[^\s\"']+", r"\1[redacted]", text)
        return re.sub(r"(https?://[^\s?\"']+)\?[^\s\"']+", r"\1?[query removed]", text)


class Log:
    """Technical log for one import, kept on this computer in .local/logs/ and never shown by default."""

    def __init__(self, root: Path, name: str, redact: Redactor):
        self.path = root / ".local" / "logs" / f"ingest-{name}.log"
        self.redact = redact

    def write(self, message: str) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "a", encoding="utf-8") as stream:
            stream.write(f"{now()} {self.redact(message)}\n")


class LockedError(RuntimeError):
    pass


def pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if sys.platform == "win32":
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not handle:
            return False
        code = ctypes.c_ulong()
        try:
            kernel32.GetExitCodeProcess(handle, ctypes.byref(code))
            return code.value == 259  # STILL_ACTIVE
        finally:
            kernel32.CloseHandle(handle)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


class WorkspaceLock:
    """Keeps two ingestion runs from changing the same workspace at once."""

    def __init__(self, root: Path):
        self.path = root / ".tmp" / "ingest.lock"

    def __enter__(self) -> "WorkspaceLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        for _ in range(2):
            try:
                handle = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                try:
                    pid = int(self.path.read_text(encoding="utf-8").split()[0])
                except (OSError, ValueError, IndexError):
                    pid = -1
                if pid_alive(pid):
                    raise LockedError(f"another import (process {pid}) is running in this workspace")
                self.path.unlink()
                continue
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                stream.write(f"{os.getpid()} {now()}\n")
            return self
        raise LockedError("could not take the import lock")

    def __exit__(self, *exc) -> None:
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass
