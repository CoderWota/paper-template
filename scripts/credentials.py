#!/usr/bin/env python3
"""Store, check, and pass on local credentials without showing them.

Credentials live in .env.local at the workspace root. Git ignores that file, but
it is not encrypted. A value is entered privately on a one-time page that only
this computer can open (or at a hidden terminal prompt), never in the
conversation or in a command argument, and this script never prints a value.
Saving or removing one name keeps every other line of the file. Writers take
turns, so two saves that overlap cannot lose each other's value.

Usage:
  python scripts/credentials.py set NAME [--label TEXT] [--note TEXT] [--help-url URL]
      [--title TEXT] [--button TEXT] [--done-message TEXT] [--timeout SECONDS]
      [--no-browser | --terminal]
  python scripts/credentials.py status [NAME ...]
  python scripts/credentials.py remove NAME
  python scripts/credentials.py run [--only NAME ...] -- COMMAND [ARGUMENT ...]
Researcher-facing texts can be given in the researcher's language. Workspace
scripts can call load_env_local() to read the values for their own process.
Exit status: 0 on success, 1 on a refusal or problem, 2 when no value was entered.
Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import contextlib
import errno
import fnmatch
import html
import os
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ".env.local"
HEADER = "# Local credentials for this workspace. Git ignores this file, but it is not encrypted. Never share or commit it."
NAME = re.compile(r"[A-Z][A-Z0-9_]*")
LINE = re.compile(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")
MAX_VALUE = 4096
MAX_BODY = 16384
LOCK_FILE = ".tmp/credentials.lock"
LOCK_WAIT = 30  # seconds to wait for another writer; a change takes milliseconds
# Errors that mean "another process holds the lock" (POSIX flock, Windows msvcrt.locking).
HELD = {errno.EACCES, errno.EAGAIN, errno.EWOULDBLOCK, getattr(errno, "EDEADLOCK", errno.EAGAIN)}


class Busy(Exception):
    """Another process kept .env.local locked for too long."""


def unquote(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        return re.sub(r"\\(.)", r"\1", raw[1:-1])
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1]
    return raw.split(" #", 1)[0].strip()


def quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8-sig").splitlines() if path.is_file() else []


def load_env_local(root: Path = ROOT) -> dict[str, str]:
    """Return the variables stored in root/.env.local; empty when the file is absent."""
    values = {}
    for line in read_lines(root / ENV_FILE):
        match = LINE.match(line)
        if match and not line.lstrip().startswith("#"):
            values[match.group(1)] = unquote(match.group(2))
    return values


def lock_file(handle) -> None:
    """Take the lock on the first byte of an open file without waiting; raise OSError when another process holds it."""
    if os.name == "nt":
        import msvcrt

        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
    else:
        import fcntl

        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)


def unlock_file(handle) -> None:
    try:
        if os.name == "nt":
            import msvcrt

            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except OSError:
        pass  # closing the file frees the lock as well


@contextlib.contextmanager
def exclusive(root: Path):
    """Hold an exclusive lock while .env.local is read, changed, and replaced.

    Two writers that overlap would each start from the same old lines, and the later one would drop the value of the
    earlier one. The operating system frees the lock when a process ends, so a crash leaves no stale lock. A file
    system that cannot lock at all is used without a lock, as it was before."""
    lock = root / LOCK_FILE
    lock.parent.mkdir(parents=True, exist_ok=True)
    with open(lock, "a+b") as handle:
        if handle.seek(0, os.SEEK_END) == 0:
            handle.write(b"\0")
            handle.flush()
        deadline, locked = time.monotonic() + LOCK_WAIT, False
        while not locked:
            try:
                handle.seek(0)
                lock_file(handle)
                locked = True
            except OSError as error:
                if error.errno not in HELD:
                    break
                if time.monotonic() >= deadline:
                    raise Busy(f"another change to {ENV_FILE} did not finish within {LOCK_WAIT} seconds") from None
                time.sleep(0.05)
        try:
            yield
        finally:
            if locked:
                unlock_file(handle)


def write_value(root: Path, name: str, value: str | None) -> bool:
    """Set name to value, or remove it when value is None, keeping every other line.

    Returns whether name was set before. The file is read, changed, and replaced under a lock, in a temporary file
    of its own, so that another writer cannot lose this value and this one cannot lose another writer's."""
    path = root / ENV_FILE
    with exclusive(root):
        lines, existed = [], False
        for line in read_lines(path):
            match = LINE.match(line)
            if match and match.group(1) == name and not line.lstrip().startswith("#"):
                existed = True
            else:
                lines.append(line)
        if not lines:
            lines = [HEADER]
        if value is not None:
            lines.append(f"{name}={quote(value)}")
        descriptor, temporary = tempfile.mkstemp(dir=root, prefix=ENV_FILE + ".", suffix=".tmp")
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
                handle.write("\n".join(lines) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        except BaseException:
            Path(temporary).unlink(missing_ok=True)
            raise
        if os.name == "posix":
            os.chmod(path, 0o600)
    return existed


def quiet(command: list[str]) -> int:
    try:
        return subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15).returncode
    except (OSError, subprocess.SubprocessError):
        return 1


def exclusion_problem(root: Path) -> str | None:
    """Return why .env.local could enter version history, or None when it cannot."""
    git = shutil.which("git")
    if git and quiet([git, "-C", str(root), "rev-parse", "--is-inside-work-tree"]) == 0:
        if quiet([git, "-C", str(root), "ls-files", "--error-unmatch", "--", ENV_FILE]) == 0:
            return f"Git already tracks {ENV_FILE}, so ignoring it cannot protect a secret. Remove it from version history first."
        if quiet([git, "-C", str(root), "check-ignore", "-q", "--", ENV_FILE]) != 0:
            return f"Git does not ignore {ENV_FILE}. Add it to .gitignore first."
        return None
    ignored = False
    for line in read_lines(root / ".gitignore"):
        pattern = line.strip()
        if not pattern or pattern.startswith("#") or pattern.endswith("/"):
            continue
        negated = pattern.startswith("!")
        if fnmatch.fnmatchcase(ENV_FILE, pattern.lstrip("!").lstrip("/")):
            ignored = not negated
    return None if ignored else f".gitignore does not exclude {ENV_FILE}. Add it before storing a secret."


def acceptable(value: str) -> bool:
    return bool(value) and len(value) <= MAX_VALUE and "\n" not in value and "\r" not in value


class OneTimeServer(HTTPServer):
    """Serves one form on 127.0.0.1 at a secret path until a value arrives."""

    def __init__(self, texts: dict[str, str]):
        super().__init__(("127.0.0.1", 0), FormHandler)
        self.texts = texts
        self.secret_path = "/" + secrets.token_urlsafe(24)
        self.value: str | None = None
        self.timeout = 1

    def page(self, error: str = "") -> str:
        t = {key: html.escape(text) for key, text in self.texts.items()}
        note = f"<p>{t['note']}</p>" if t["note"] else ""
        link = f'<p><a href="{t["help_url"]}" target="_blank" rel="noreferrer noopener">{t["help_url"]}</a></p>' if t["help_url"] else ""
        problem = f'<p class="error">{html.escape(error)}</p>' if error else ""
        return (
            '<!doctype html><html><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            f"<title>{t['title']}</title><style>"
            "body{font-family:system-ui,sans-serif;max-width:34rem;margin:3rem auto;padding:0 1rem;line-height:1.5}"
            "input{width:100%;padding:.5rem;font-size:1rem;box-sizing:border-box}"
            "button{margin-top:1rem;padding:.5rem 1.25rem;font-size:1rem}.error{color:#b00020}"
            f"</style></head><body><h1>{t['title']}</h1>{note}{link}{problem}"
            f'<form method="post" autocomplete="off"><label for="value">{t["label"]}</label>'
            '<input id="value" name="value" type="password" autocomplete="off" autofocus required>'
            f'<button type="submit">{t["button"]}</button></form></body></html>'
        )


class FormHandler(BaseHTTPRequestHandler):
    server: OneTimeServer
    server_version = "workspace-credentials"
    sys_version = ""

    def log_message(self, format: str, *args) -> None:  # noqa: A002 - keep request lines out of the output
        pass

    def send_page(self, status: int, body: str) -> None:
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        # "same-origin", not "no-referrer": with "no-referrer", browsers send "Origin: null"
        # on the form submission, and the origin check below would reject it.
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'")
        self.end_headers()
        self.wfile.write(data)

    def allowed(self) -> bool:
        port = self.server.server_address[1]
        hosts = (f"127.0.0.1:{port}", f"localhost:{port}")
        origin = self.headers.get("Origin")
        return (
            self.path == self.server.secret_path
            and self.headers.get("Host") in hosts
            and (origin is None or origin in tuple(f"http://{host}" for host in hosts))
        )

    def do_GET(self) -> None:  # noqa: N802
        if self.allowed() and self.server.value is None:
            self.send_page(200, self.server.page())
        else:
            self.send_page(404, "<h1>Not found</h1>")

    def do_POST(self) -> None:  # noqa: N802
        if not self.allowed() or self.server.value is not None:
            self.send_page(404, "<h1>Not found</h1>")
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = -1
        if not 0 <= length <= MAX_BODY:
            self.send_page(413, "<h1>Too large</h1>")
            return
        fields = urllib.parse.parse_qs(self.rfile.read(length).decode("utf-8", "replace"), keep_blank_values=True)
        value = fields.get("value", [""])[0].strip()
        if not acceptable(value):
            self.send_page(400, self.server.page(self.server.texts["invalid"]))
            return
        self.server.value = value
        self.send_page(200, f"<!doctype html><meta charset=\"utf-8\"><h1>{html.escape(self.server.texts['done'])}</h1>")


def collect_in_browser(name: str, texts: dict[str, str], timeout: int, open_browser: bool) -> str | None:
    server = OneTimeServer(texts)
    url = f"http://127.0.0.1:{server.server_address[1]}{server.secret_path}"
    print(f"Open this page on this computer to enter {name}: {url}", flush=True)
    print(f"Waiting up to {max(1, timeout // 60)} minute(s). Nothing is saved until the form is submitted.", flush=True)
    if open_browser:
        try:
            webbrowser.open(url)
        except webbrowser.Error:
            pass
    deadline = time.monotonic() + timeout
    try:
        while server.value is None and time.monotonic() < deadline:
            server.handle_request()
    finally:
        server.server_close()
    return server.value


def command_set(args: argparse.Namespace) -> int:
    if not NAME.fullmatch(args.name):
        print(f"Not saved: {args.name!r} is not a valid name. Use capital letters, digits, and underscores.")
        return 1
    problem = exclusion_problem(ROOT)
    if problem:
        print(f"Not saved: {problem}")
        return 1
    help_url = args.help_url if args.help_url and args.help_url.startswith(("https://", "http://")) else ""
    texts = {
        "title": args.title,
        "label": args.label or f"Value for {args.name}",
        "note": args.note or "",
        "help_url": help_url,
        "button": args.button,
        "done": args.done_message,
        "invalid": args.invalid_message,
    }
    if args.terminal:
        import getpass

        value = getpass.getpass(f"{texts['label']}: ").strip()
    else:
        value = collect_in_browser(args.name, texts, args.timeout, not args.no_browser) or ""
    if not value:
        print("No value was entered. Nothing was saved.")
        return 2
    if not acceptable(value):
        print("Not saved: the value is empty, too long, or contains a line break.")
        return 1
    try:
        replaced = write_value(ROOT, args.name, value)
    except Busy as error:
        print(f"Not saved: {error}. Try again.")
        return 1
    action = "Replaced" if replaced else "Saved"
    print(f"{action} {args.name} ({len(value)} characters) in {ENV_FILE}. Git ignores this file; it is not encrypted.")
    return 0


def command_status(args: argparse.Namespace) -> int:
    values = load_env_local(ROOT)
    names = args.names or sorted(values)
    if not names:
        print(f"No credentials are stored in {ENV_FILE}.")
    for name in names:
        print(f"{name}: set ({len(values[name])} characters)" if name in values else f"{name}: not set")
    problem = exclusion_problem(ROOT)
    print(f"Protection: {problem}" if problem else f"Protection: Git ignores {ENV_FILE}. The file is not encrypted.")
    return 1 if problem else 0


def command_remove(args: argparse.Namespace) -> int:
    if args.name not in load_env_local(ROOT):
        print(f"{args.name} was not set.")
        return 0
    try:
        write_value(ROOT, args.name, None)
    except Busy as error:
        print(f"Not removed: {error}. Try again.")
        return 1
    print(f"Removed {args.name} from {ENV_FILE}.")
    return 0


def command_run(args: argparse.Namespace) -> int:
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        print("Give the command to run after --.")
        return 1
    values = load_env_local(ROOT)
    missing = [name for name in args.only if name not in values]
    if missing:
        print(f"Not set: {', '.join(missing)}. Nothing was run.")
        return 1
    environment = dict(os.environ)
    environment.update({name: values[name] for name in args.only} if args.only else values)
    try:
        return subprocess.run(command, env=environment).returncode
    except OSError as error:
        print(f"Could not run {command[0]!r}: {error.strerror}")
        return 1


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Store, check, and pass on local credentials without showing them.")
    commands = parser.add_subparsers(dest="action", required=True)

    store = commands.add_parser("set", help="enter a value privately and save it in .env.local")
    store.add_argument("name", help="variable name, for example MINERU_API_KEY")
    store.add_argument("--label", help="field label shown to the researcher")
    store.add_argument("--note", help="short explanation shown above the field")
    store.add_argument("--help-url", help="official page where the researcher can get the value")
    store.add_argument("--title", default="Enter a credential")
    store.add_argument("--button", default="Save")
    store.add_argument("--done-message", default="Saved. You can close this page and return to the conversation.")
    store.add_argument("--invalid-message", default="Enter a value on one line.")
    store.add_argument("--timeout", type=int, default=600, help="seconds to wait for the form (default 600)")
    entry = store.add_mutually_exclusive_group()
    entry.add_argument("--no-browser", action="store_true", help="print the page address without opening a browser")
    entry.add_argument("--terminal", action="store_true", help="ask at a hidden prompt in this terminal instead")
    store.set_defaults(handler=command_set)

    status = commands.add_parser("status", help="show which names are set, without values")
    status.add_argument("names", nargs="*")
    status.set_defaults(handler=command_status)

    remove = commands.add_parser("remove", help="delete one stored value")
    remove.add_argument("name")
    remove.set_defaults(handler=command_remove)

    run = commands.add_parser("run", help="run a command with stored values in its environment")
    run.add_argument("--only", nargs="+", default=[], metavar="NAME", help="pass only these names")
    run.add_argument("command", nargs=argparse.REMAINDER)
    run.set_defaults(handler=command_run)

    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    sys.exit(main())
