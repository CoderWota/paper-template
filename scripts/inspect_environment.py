#!/usr/bin/env python3
"""Report this computer's setup for the workspace without changing anything.

Used by the environment-management skill: operating system, processor
architecture (including emulation), memory, free storage, Python interpreters,
optional command-line tools, workspace path risks, and project-local setup.

Usage: python scripts/inspect_environment.py [--json]
Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.util
import json
import os
import platform
import shutil
import struct
import subprocess
import sys
from pathlib import Path

from export.tools import find_in_tools

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ("git", "uv", "pandoc", "quarto", "node", "winget", "pdftotext")
CLOUD_SYNC_MARKERS = ("onedrive", "dropbox", "google drive", "icloud drive", "mobile documents", "box sync")
WINDOWS_MACHINES = {0x014C: "x86", 0x8664: "x64", 0x01C4: "ARM", 0xAA64: "ARM64"}
LONG_WINDOWS_PATH = 150  # Leaves room for nested project paths under the 260-character limit.


def first_line(command: list[str]) -> str | None:
    """Run a version command and return its first output line, or None when it fails."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, errors="replace", timeout=15)
    except (OSError, subprocess.SubprocessError):
        return None
    output = (result.stdout or result.stderr).strip()
    return output.splitlines()[0] if output else None


def windows_native_machine() -> str | None:
    try:
        kernel32 = ctypes.WinDLL("kernel32")
        kernel32.GetCurrentProcess.restype = ctypes.c_void_p
        kernel32.IsWow64Process2.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ushort), ctypes.POINTER(ctypes.c_ushort)]
        process_machine, native_machine = ctypes.c_ushort(), ctypes.c_ushort()
        if kernel32.IsWow64Process2(kernel32.GetCurrentProcess(), ctypes.byref(process_machine), ctypes.byref(native_machine)):
            return WINDOWS_MACHINES.get(native_machine.value)
    except (AttributeError, OSError):
        pass
    return os.environ.get("PROCESSOR_ARCHITEW6432") or os.environ.get("PROCESSOR_ARCHITECTURE")


def macos_sysctl(name: str) -> int | None:
    try:
        libc = ctypes.CDLL(ctypes.util.find_library("c"))
        libc.sysctlbyname.argtypes = [ctypes.c_char_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t), ctypes.c_void_p, ctypes.c_size_t]
        value, size = ctypes.c_int64(0), ctypes.c_size_t(8)
        if libc.sysctlbyname(name.encode(), ctypes.byref(value), ctypes.byref(size), None, 0) == 0:
            return value.value
    except (AttributeError, OSError, TypeError):
        pass
    return None


def windows_memory() -> int | None:
    class MemoryStatus(ctypes.Structure):
        _fields_ = [("length", ctypes.c_ulong), ("load", ctypes.c_ulong)] + [
            (field, ctypes.c_ulonglong)
            for field in ("total", "available", "page_total", "page_available", "virtual_total", "virtual_available", "extended")
        ]

    try:
        status = MemoryStatus()
        status.length = ctypes.sizeof(status)
        if ctypes.WinDLL("kernel32").GlobalMemoryStatusEx(ctypes.byref(status)):
            return status.total
    except (AttributeError, OSError):
        pass
    return None


def operating_system() -> dict:
    system = platform.system()
    info = {"system": system, "release": platform.release(), "version": platform.version()}
    if system == "Windows":
        release, build, _, _ = platform.win32_ver()
        edition = platform.win32_edition() if hasattr(platform, "win32_edition") else ""
        info["name"] = f"Windows {release} {edition}".strip() + f" (build {build})"
    elif system == "Darwin":
        info["name"] = f"macOS {platform.mac_ver()[0]}"
    else:
        name = "Linux"
        try:
            for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
                if line.startswith("PRETTY_NAME="):
                    name = line.split("=", 1)[1].strip().strip('"')
        except OSError:
            pass
        info["name"] = name
    return info


def processor() -> dict:
    system = platform.system()
    process = platform.machine()
    if system == "Windows":
        native = windows_native_machine()
        process = {"AMD64": "x64", "ARM64": "ARM64", "x86": "x86"}.get(process, process)
        native = {"AMD64": "x64"}.get(native or "", native)
        emulated = bool(native and native != process)
    elif system == "Darwin":
        native = "arm64" if macos_sysctl("hw.optional.arm64") == 1 else "x86_64"
        emulated = macos_sysctl("sysctl.proc_translated") == 1
    else:
        native, emulated = process, False
    return {"native": native, "python_process": process, "python_bits": struct.calcsize("P") * 8, "emulated": emulated, "cpu_count": os.cpu_count()}


def memory_bytes() -> int | None:
    system = platform.system()
    if system == "Windows":
        return windows_memory()
    if system == "Darwin":
        return macos_sysctl("hw.memsize")
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    except (AttributeError, OSError, ValueError):
        return None


def pythons() -> list[dict]:
    found = []
    for name in ("python3", "python", "py"):
        path = shutil.which(name)
        if not path:
            continue
        entry = {"command": name, "path": path, "version": first_line([path, "--version"])}
        if "windowsapps" in path.lower():
            entry["note"] = "Microsoft Store alias; it may only offer to install Python"
        if name == "py":
            entry["installed"] = first_line([path, "-0p"])
        found.append(entry)
    return found


def workspace_tool(name: str) -> str | None:
    """A tool installed in the workspace's own .tools/ folder, where the export and import scripts look first."""
    if name == "pandoc":
        found = find_in_tools(ROOT, "pandoc", "pandoc")
        return str(found) if found else None
    else:
        candidates = []
    found = [p for p in candidates if p.is_file() and os.access(p, os.X_OK)]
    return str(found[-1]) if found else None


def tools() -> dict:
    report = {}
    for name in TOOLS:
        path, location = workspace_tool(name), "workspace .tools"
        if not path:
            path, location = shutil.which(name), "PATH"
        version_args = ["-v"] if name == "pdftotext" else ["--version"]
        version = first_line([path, *version_args]) if path else None
        report[name] = {"path": path, "location": location if path else None, "version": version}
    return report


def workspace() -> dict:
    text = str(ROOT)
    lowered = text.lower()
    venv_python = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return {
        "path": text,
        "has_spaces": " " in text,
        "has_non_ascii": not text.isascii(),
        "length": len(text),
        "long_for_windows": platform.system() == "Windows" and len(text) > LONG_WINDOWS_PATH,
        "cloud_synced": next((marker for marker in CLOUD_SYNC_MARKERS if marker in lowered), None),
        "free_bytes": shutil.disk_usage(ROOT).free,
        "venv_python": first_line([str(venv_python), "--version"]) if venv_python.exists() else None,
        "venv_exists": (ROOT / ".venv").exists(),
        "tool_environments": sorted(p.name for p in (ROOT / ".tools").iterdir() if p.is_dir()) if (ROOT / ".tools").is_dir() else [],
        "env_local_exists": (ROOT / ".env.local").is_file(),
        "git_repository": (ROOT / ".git").exists(),
    }


def tool_summary(name: str, info: dict) -> str:
    if not info["path"]:
        return f"{name} not found"
    version = info["version"] or "(found)"
    text = version if version.lower().startswith(name) else f"{name} {version}"
    return text + (" in the workspace .tools folder" if info.get("location") == "workspace .tools" else "")


def gigabytes(value: int | None) -> str:
    return f"{value / 1024 ** 3:.1f} GB" if value else "unknown"


def render(report: dict) -> str:
    cpu, ws = report["processor"], report["workspace"]
    emulation = "; Python runs under emulation" if cpu["emulated"] else ""
    risks = [label for flag, label in (
        (ws["has_spaces"], "contains spaces"),
        (ws["has_non_ascii"], "contains non-ASCII characters"),
        (ws["long_for_windows"], f"is long ({ws['length']} characters)"),
        (ws["cloud_synced"], f"is inside a cloud-synced folder ({ws['cloud_synced']})"),
    ) if flag]
    lines = [
        "Workspace environment (read-only check)",
        f"Operating system: {report['os']['name']}",
        f"Processor: {cpu['native']} native, {cpu['cpu_count']} logical cores; Python process {cpu['python_process']} ({cpu['python_bits']}-bit){emulation}",
        f"Memory: {gigabytes(report['memory_bytes'])}",
        f"Free storage on the workspace drive: {gigabytes(ws['free_bytes'])}",
        f"Workspace path: {ws['path']}",
        f"  Path notes: {', '.join(risks) if risks else 'none'}",
        f"Python running this check: {report['python']['version']} at {report['python']['executable']}",
    ]
    for entry in report["pythons_on_path"]:
        note = f"; {entry['note']}" if "note" in entry else ""
        lines.append(f"  On PATH: {entry['command']} -> {entry['version'] or 'no version output'} ({entry['path']}){note}")
        if entry.get("installed"):
            lines.append(f"    Python launcher reports: {entry['installed']}")
    lines.append("Tools: " + "; ".join(tool_summary(name, info) for name, info in report["tools"].items()))
    lines.append(
        "Project setup: "
        f".venv {'works: ' + ws['venv_python'] if ws['venv_python'] else ('exists but does not run' if ws['venv_exists'] else 'not created')}; "
        f".tools {', '.join(ws['tool_environments']) or 'none'}; "
        f".env.local {'present' if ws['env_local_exists'] else 'absent'}; "
        f"Git repository {'yes' if ws['git_repository'] else 'no'}"
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Report this computer's setup for the workspace without changing anything.")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)
    report = {
        "os": operating_system(),
        "processor": processor(),
        "memory_bytes": memory_bytes(),
        "python": {"version": platform.python_version(), "executable": sys.executable},
        "pythons_on_path": pythons(),
        "tools": tools(),
        "workspace": workspace(),
    }
    print(json.dumps(report, indent=2) if args.json else render(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
