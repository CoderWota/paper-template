#!/usr/bin/env python3
"""Install and check MinerU for the local processing route, inside this workspace.

MinerU goes into its own environment in .tools/mineru/, and its configuration and models into
.cache/mineru/. Git ignores both, so the parser cannot affect the workspace scripts, research
code, or other projects. Run "install" and "models" only after the researcher has agreed to the
download and the disk space: MinerU needs about 1.4 GB, the basic-tier models about 0.9 GB, and
the standard tier adds a VLM of several GB.

Usage:
  python scripts/setup_mineru.py check [--json]
  python scripts/setup_mineru.py install [--python PATH]
  python scripts/setup_mineru.py models --tier basic|standard [--source huggingface|modelscope]
Exit status: 0 on success, 1 on a problem. Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ingestion.routes import TESTED_MINERU, LocalRoute  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SUPPORTED = ((3, 10), (3, 14))


def tool_python(root: Path) -> Path:
    tool = root / ".tools" / "mineru"
    return tool / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")


def python_version(command: list) -> tuple | None:
    try:
        result = subprocess.run(command + ["-c", "import sys; print(sys.version_info[0], sys.version_info[1])"],
                                capture_output=True, text=True, timeout=60)
        major, minor = (int(part) for part in result.stdout.split())
        return major, minor
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None


def find_python() -> list | None:
    """A Python that MinerU 4 supports (3.10 to 3.14). The workspace scripts themselves need only 3.9."""
    candidates = [[sys.executable]]
    if sys.platform == "win32":
        candidates += [["py", f"-3.{minor}"] for minor in (12, 13, 11, 10, 14)]
    candidates += [[name] for name in ("python3.12", "python3.13", "python3.11", "python3.10", "python3.14", "python3", "python")]
    for command in candidates:
        if command[0] not in ("py",) and not shutil.which(command[0]) and command[0] != sys.executable:
            continue
        version = python_version(command)
        if version and SUPPORTED[0] <= version <= SUPPORTED[1]:
            return command
    return None


def models_ready(route: LocalRoute, tier: str) -> bool:
    result = route.run(["models", "verify", "--tier", tier], timeout=600)
    return result.returncode == 0


def size(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file()) if path.exists() else 0


def command_check(args, root: Path) -> int:
    route = LocalRoute(root, "flash")
    report = {"mineru": None, "tested_version": TESTED_MINERU, "location": None, "models": {}, "disk_free_gb": None}
    if route.command:
        report["location"] = route.command[0]
        try:
            report["mineru"] = route.version()
            route.ensure_config()
            for tier in ("basic", "standard"):
                report["models"][tier] = "ready" if models_ready(route, tier) else "not installed"
        except Exception as error:  # noqa: BLE001 - a check reports every failure plainly
            report["problem"] = str(error)
    report["disk_free_gb"] = round(shutil.disk_usage(root).free / 2**30, 1)
    report["installed_size_gb"] = round(size(root / ".tools" / "mineru") / 2**30, 2)
    report["models_size_gb"] = round(size(root / ".cache" / "mineru" / "models") / 2**30, 2)
    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if report["mineru"] else 1
    if not report["mineru"]:
        print("MinerU is not installed for this workspace." + (f" Problem: {report['problem']}" if report.get("problem") else ""))
        print(f"Free disk space: {report['disk_free_gb']} GB.")
        return 1
    print(f"MinerU {report['mineru']} at {report['location']} (tested version: {TESTED_MINERU}).")
    print("Flash tier: ready; it reads the text layer of PDFs and Word files without models. Other office formats are converted too,"
          " but their results are flagged until they are verified in this workspace.")
    for tier, state in report["models"].items():
        print(f"{tier.capitalize()} tier models: {state}.")
    print(f"Disk use: {report['installed_size_gb']} GB for MinerU, {report['models_size_gb']} GB for models; {report['disk_free_gb']} GB free.")
    return 0


def command_install(args, root: Path) -> int:
    python = [args.python] if args.python else find_python()
    if not python:
        print("No Python 3.10 to 3.14 was found. MinerU 4 needs one; install Python 3.12 from python.org first.")
        return 1
    version = python_version(python)
    if not version or not SUPPORTED[0] <= version <= SUPPORTED[1]:
        print(f"{' '.join(python)} is Python {version}; MinerU 4 needs 3.10 to 3.14.")
        return 1
    tool = root / ".tools" / "mineru"
    if not tool_python(root).is_file():
        print(f"Creating the tool environment in {tool} with Python {version[0]}.{version[1]} ...", flush=True)
        if subprocess.run(python + ["-m", "venv", str(tool)]).returncode != 0:
            print("The environment could not be created.")
            return 1
    print(f"Installing MinerU {TESTED_MINERU} (about 1.4 GB) ...", flush=True)
    result = subprocess.run([str(tool_python(root)), "-m", "pip", "install", "--disable-pip-version-check", f"mineru=={TESTED_MINERU}"])
    if result.returncode != 0:
        print("The installation failed; the messages above say why. Nothing outside .tools/mineru/ was changed.")
        return 1
    route = LocalRoute(root, "flash")
    route.ensure_config()
    print(f"Installed MinerU {route.version()}. Models for the basic and standard tiers are not downloaded yet.")
    return 0


def command_models(args, root: Path) -> int:
    route = LocalRoute(root, args.tier)
    if not route.command:
        print("MinerU is not installed for this workspace; run the install command first.")
        return 1
    route.ensure_config()
    env = route.env()
    env.pop("MINERU_MODEL_SOURCE", None)
    print(f"Downloading the {args.tier}-tier models into .cache/mineru/models ...", flush=True)
    download = subprocess.run(route.command + ["models", "download", "--tier", args.tier, "--source", args.source], env=env)
    if download.returncode != 0 or not models_ready(route, args.tier):
        print("The models are not complete. Run the same command again to continue the download.")
        return 1
    print(f"The {args.tier}-tier models are ready ({round(size(root / '.cache' / 'mineru' / 'models') / 2**30, 2)} GB in .cache/mineru/models).")
    return 0


def main(argv: list | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Install and check MinerU for the local processing route.")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("check", help="report the installation, the models, and the disk space")
    check.add_argument("--json", action="store_true")
    install = commands.add_parser("install", help=f"install MinerU {TESTED_MINERU} into .tools/mineru/")
    install.add_argument("--python", help="the Python 3.10 to 3.14 interpreter to use")
    models = commands.add_parser("models", help="download the models of a tier into .cache/mineru/models")
    models.add_argument("--tier", choices=("basic", "standard"), required=True)
    models.add_argument("--source", choices=("huggingface", "modelscope"), default="huggingface")
    args = parser.parse_args(argv)
    handlers = {"check": command_check, "install": command_install, "models": command_models}
    return handlers[args.command](args, args.root.resolve())


if __name__ == "__main__":
    sys.exit(main())
