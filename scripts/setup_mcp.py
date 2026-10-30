#!/usr/bin/env python3
"""Install, configure, inspect, and launch the repository's official MCP servers.

Installation needs Python >=3.11 and Node >=18. Only install downloads packages.
Check uses initialize/tools/list with dummy credentials, never tools/call.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time

if sys.version_info < (3, 11):
    raise SystemExit("MCP setup needs Python 3.11 or later. Other workspace scripts are unaffected.")

import tomllib

from credentials import load_env_local

ROOT = Path(__file__).resolve().parent.parent
NAMES = ("sciverse", "mineru")
VERSIONS = {"sciverse": "1.0.0", "mineru": "1.0.22"}
EXPECTED = {"sciverse": {"semantic_search", "read_content", "get_resource", "list_catalog"},
            "mineru": {"parse_documents", "get_ocr_languages"}}


class SetupError(Exception):
    pass


def python_path(root: Path) -> Path:
    return root / ".tools/mcp/python" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".writing-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def run_install(command: list[str], root: Path) -> None:
    # Do not display inherited environment values or dependency-manager diagnostics.
    result = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        raise SetupError(f"Package installation failed (exit {result.returncode}). Check network access and runtime compatibility, then rerun install.")


def fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for name in ("package.json", "package-lock.json", "requirements.lock"):
        digest.update((root / "mcp" / name).read_bytes())
    digest.update(str(root).encode())
    digest.update(sys.executable.encode())
    return digest.hexdigest()


def installed_version(root: Path, name: str) -> str | None:
    try:
        if name == "sciverse":
            return json.loads((root / ".tools/mcp/sciverse/node_modules/sciverse-mcp-server/package.json").read_text())["version"]
        result = subprocess.run([str(python_path(root)), "-c", "import importlib.metadata; print(importlib.metadata.version('mineru-open-mcp'))"],
                                capture_output=True, text=True, timeout=15)
        return result.stdout.strip() if result.returncode == 0 else None
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired):
        return None


def install(root: Path) -> None:
    node, npm = shutil.which("node"), shutil.which("npm")
    if not node or not npm:
        raise SetupError("Node.js >=18 and npm are required. Install a compatible runtime before retrying.")
    major = int(subprocess.check_output([node, "--version"], text=True).strip().lstrip("v").split(".")[0])
    if major < 18:
        raise SetupError("Node.js >=18 is required; the existing global runtime was not changed.")
    target = root / ".tools/mcp"
    target.mkdir(parents=True, exist_ok=True)
    stamp = target / "installed.json"
    try:
        previous = json.loads(stamp.read_text()) if stamp.exists() else {}
    except ValueError:
        previous = {}
    current = fingerprint(root)
    if previous.get("fingerprint") == current and all(installed_version(root, n) == VERSIONS[n] for n in NAMES):
        print("Both pinned MCP packages are already installed. No downloads.")
        return
    folder = target / "sciverse"
    folder.mkdir(exist_ok=True)
    for filename in ("package.json", "package-lock.json"):
        shutil.copy2(root / "mcp" / filename, folder / filename)
    completed = previous.get("completed", {})
    if completed.get("sciverse") != current or installed_version(root, "sciverse") != VERSIONS["sciverse"]:
        print("Installing pinned Sciverse MCP locally ...", flush=True)
        run_install([npm, "ci", "--prefix", str(folder), "--ignore-scripts", "--no-audit", "--no-fund"], root)
        completed["sciverse"] = current
        write_atomic(stamp, json.dumps({"completed": completed}, indent=2) + "\n")
    py = python_path(root)
    if not py.exists():
        run_install([sys.executable, "-m", "venv", str(target / "python")], root)
    if completed.get("mineru") != current or installed_version(root, "mineru") != VERSIONS["mineru"]:
        print("Installing pinned MinerU MCP locally ...", flush=True)
        run_install([str(py), "-m", "pip", "install", "--disable-pip-version-check", "--require-hashes", "-r", str(root / "mcp/requirements.lock")], root)
        completed["mineru"] = current
        write_atomic(stamp, json.dumps({"completed": completed}, indent=2) + "\n")
    for name in NAMES:
        if installed_version(root, name) != VERSIONS[name]:
            raise SetupError(f"{name}: installed version does not match the pinned version.")
    write_atomic(stamp, json.dumps({"fingerprint": current, "completed": completed, "versions": VERSIONS}, indent=2) + "\n")
    print("Both official MCP packages are installed in .tools/mcp/.")


def launch_command(root: Path, name: str) -> list[str]:
    if installed_version(root, name) != VERSIONS[name]:
        raise SetupError(f"{name}: missing or different version. Run setup_mcp.py install first.")
    if name == "sciverse":
        node = shutil.which("node")
        if not node:
            raise SetupError("Node.js is missing.")
        return [node, str(root / ".tools/mcp/sciverse/node_modules/sciverse-mcp-server/dist/cli.js")]
    return [str(python_path(root)), "-m", "mineru_open_mcp.cli", "--transport", "stdio",
            "--output-dir", str(root / ".local/mcp/output")]


def server_env(root: Path, name: str, probe: bool = False) -> dict[str, str]:
    env = dict(os.environ)
    values = {} if probe else load_env_local(root)
    # Pass only the selected service credential, never all of .env.local.
    for key in ("SCIVERSE_API_TOKEN", "SCIVERSE_API_KEY", "MINERU_API_TOKEN"):
        env.pop(key, None)
    if name == "sciverse":
        token = "mcp-local-probe-not-a-credential" if probe else (
            os.environ.get("SCIVERSE_API_TOKEN") or os.environ.get("SCIVERSE_API_KEY")
            or values.get("SCIVERSE_API_KEY") or values.get("SCIVERSE_API_TOKEN"))
        if not token:
            raise SetupError("Sciverse is installed; service calls need a privately entered SCIVERSE_API_KEY.")
        env["SCIVERSE_API_TOKEN"] = token
        env["SCIVERSE_BASE_URL"] = "https://api.sciverse.space"
    elif not probe:
        token = os.environ.get("MINERU_API_TOKEN") or values.get("MINERU_API_TOKEN")
        if token:
            env["MINERU_API_TOKEN"] = token
    env.update({"OUTPUT_DIR": str(root / ".local/mcp/output"), "ENABLE_LOG": "false",
                "MINERU_LOG_DIR": str(root / ".local/mcp/logs"), "PYTHONIOENCODING": "utf-8",
                "PYTHON_DOTENV_DISABLED": "1"})
    return env


def probe_server(root: Path, name: str, timeout: float = 45) -> list[str]:
    process = subprocess.Popen(launch_command(root, name), cwd=root / ".tools/mcp", env=server_env(root, name, probe=True),
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                               text=True, encoding="utf-8")
    messages: queue.Queue = queue.Queue()

    def read():
        try:
            for line in process.stdout:
                messages.put(line)
        finally:
            messages.put(None)

    threading.Thread(target=read, daemon=True).start()
    deadline = time.monotonic() + timeout

    def send(message):
        process.stdin.write(json.dumps({"jsonrpc": "2.0", **message}) + "\n")
        process.stdin.flush()

    def receive(identifier):
        while True:
            if time.monotonic() >= deadline:
                raise SetupError(f"{name}: MCP handshake timed out.")
            try:
                line = messages.get(timeout=max(0.01, deadline - time.monotonic()))
            except queue.Empty:
                raise SetupError(f"{name}: MCP handshake timed out.") from None
            if line is None:
                raise SetupError(f"{name}: server exited before completing MCP discovery.")
            try:
                message = json.loads(line)
                if message.get("jsonrpc") != "2.0":
                    raise ValueError()
            except (ValueError, AttributeError):
                raise SetupError(f"{name}: non-JSON-RPC output on stdout.") from None
            if message.get("id") == identifier:
                if "error" in message:
                    raise SetupError(f"{name}: MCP discovery returned a protocol error.")
                return message["result"]

    try:
        send({"id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {},
             "clientInfo": {"name": "paper-template-check", "version": "1.0"}}})
        receive(1)
        send({"method": "notifications/initialized"})
        names = []
        cursor = None
        for identifier in range(2, 22):
            send({"id": identifier, "method": "tools/list", "params": {"cursor": cursor} if cursor else {}})
            result = receive(identifier)
            names.extend(tool["name"] for tool in result["tools"])
            next_cursor = result.get("nextCursor")
            if not next_cursor:
                break
            if next_cursor == cursor:
                raise SetupError(f"{name}: repeated tool-list cursor.")
            cursor = next_cursor
        else:
            raise SetupError(f"{name}: tool pagination did not finish.")
        if not EXPECTED[name].issubset(names):
            raise SetupError(f"{name}: expected tools are missing.")
        return names
    finally:
        process.stdin.close()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        process.stdout.close()


def config_values(root: Path, name: str) -> dict:
    return {"name": name, "python": str(python_path(root)), "script": str(root / "scripts/setup_mcp.py"), "root": str(root)}


def save_config(root: Path, path: Path, content: str) -> None:
    if path.exists():
        if path.read_text(encoding="utf-8") == content:
            return
        backup = root / ".local/mcp/backups" / (path.name + "." + str(time.time_ns()))
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
    write_atomic(path, content)


def configure(root: Path) -> None:
    # tomlkit preserves unrelated TOML settings and comments.
    if sys.executable != str(python_path(root)):
        result = subprocess.run([str(python_path(root)), str(root / "scripts/setup_mcp.py"), "configure"], cwd=root)
        if result.returncode:
            raise SetupError("MCP configuration was not completed.")
        return
    import tomlkit
    codex = root / ".codex/config.toml"
    document = tomlkit.parse(codex.read_text(encoding="utf-8")) if codex.exists() else tomlkit.document()
    if "mcp_servers" not in document:
        document["mcp_servers"] = tomlkit.table()
    claude = root / ".mcp.json"
    data = json.loads(claude.read_text(encoding="utf-8")) if claude.exists() else {}
    servers = data.setdefault("mcpServers", {})
    for name in NAMES:
        values = config_values(root, name)
        template = (root / "mcp/codex.toml.template").read_text()
        rendered = template.format(**{key: value if key == "name" else json.dumps(value) for key, value in values.items()})
        document["mcp_servers"][name] = tomlkit.parse(rendered)["mcp_servers"][name]
        template = json.loads((root / "mcp/claude.json.template").read_text())
        servers[name] = {"type": template["type"], "command": values["python"],
                         "args": [part.format(**values) for part in template["args"]]}
    codex_text = tomlkit.dumps(document)
    tomllib.loads(codex_text)
    save_config(root, codex, codex_text)
    save_config(root, claude, json.dumps(data, indent=2) + "\n")
    print("Codex and Claude Code project configurations are ready. Reopen the project to load them.")


def check(root: Path) -> int:
    report = {"servers": {}, "configs": {}, "service_calls_tested": False}
    values = load_env_local(root)
    good = True
    for name in NAMES:
        entry = {"version": installed_version(root, name)}
        try:
            entry["tools"] = probe_server(root, name)
            entry["protocol"] = "ready"
        except (SetupError, OSError, ValueError, KeyError) as error:
            entry["protocol"] = "incomplete"
            entry["problem"] = str(error) if isinstance(error, SetupError) else "Could not inspect the server."
            good = False
        keys = ("SCIVERSE_API_KEY", "SCIVERSE_API_TOKEN") if name == "sciverse" else ("MINERU_API_TOKEN",)
        entry["credential"] = "present, validity untested" if any(os.environ.get(k) or values.get(k) for k in keys) else "not configured; service calls pending"
        report["servers"][name] = entry
    for name, path in (("codex", root / ".codex/config.toml"), ("claude", root / ".mcp.json")):
        try:
            data = tomllib.loads(path.read_text()) if name == "codex" else json.loads(path.read_text())
            servers = data["mcp_servers" if name == "codex" else "mcpServers"]
            valid = all(servers[n]["command"] == str(python_path(root)) and servers[n]["args"] == [str(root / "scripts/setup_mcp.py"), "start", n] for n in NAMES)
            report["configs"][name] = "ready" if valid else "needs configure"
            good &= valid
        except (OSError, ValueError, KeyError, TypeError):
            report["configs"][name] = "missing or invalid"
            good = False
    report["ready"] = good
    write_atomic(root / ".local/mcp/status.json", json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if good else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    for name in ("install", "configure", "check"):
        commands.add_parser(name)
    launch = commands.add_parser("start")
    launch.add_argument("server", choices=NAMES)
    args = parser.parse_args()
    try:
        if args.action == "install":
            install(ROOT)
        elif args.action == "configure":
            configure(ROOT)
        elif args.action == "check":
            return check(ROOT)
        else:
            command = launch_command(ROOT, args.server)
            env = server_env(ROOT, args.server)
            os.chdir(ROOT / ".tools/mcp")  # Avoid upstream dotenv auto-loading project secrets.
            os.execve(command[0], command, env)
        return 0
    except (SetupError, OSError, ValueError, subprocess.SubprocessError) as error:
        message = str(error) if isinstance(error, SetupError) else "MCP setup failed. Check files, runtimes, and permissions; no credentials were displayed."
        print(message, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
