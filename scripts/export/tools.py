"""The export tools: Pandoc, pandoc-crossref, mermaid-cli with a browser, and an application that renders DOCX.

Tools are found in the workspace's ignored .tools/ folder first, then on PATH. `install` downloads the pinned
releases from their official GitHub pages, checks each archive against its published SHA-256 digest, and unpacks it
into .tools/; mermaid-cli is installed with npm, without its bundled browser. Installing needs the researcher's
consent; the skills ask first.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

PANDOC_VERSION, CROSSREF_VERSION, MERMAID_CLI_VERSION = "3.12.1", "0.3.26", "12.0.0"
PANDOC_RELEASE = f"https://github.com/jgm/pandoc/releases/download/{PANDOC_VERSION}/"
CROSSREF_RELEASE = f"https://github.com/lierdakil/pandoc-crossref/releases/download/v{CROSSREF_VERSION}/"
# (platform, machine) -> (archive name, SHA-256), as published on the release pages (read 2026-10-28).
PANDOC_ARCHIVES = {
    ("darwin", "arm64"): ("pandoc-3.12.1-arm64-macOS.zip", "c2146cf33a583f3ac93eccddf1bb662371d5cfcce1aad1c87ad860cca1435d46"),
    ("darwin", "x86_64"): ("pandoc-3.12.1-x86_64-macOS.zip", "81ed3e2cfecf096df15d407152f89a684fd65221082b919963f738e977fad3bc"),
    ("windows", "x86_64"): ("pandoc-3.12.1-windows-x86_64.zip", "6ef431cb20b2c24a0371fc19200dc49d452be54b1b5c9239f3462841ef53e587"),
    ("linux", "x86_64"): ("pandoc-3.12.1-linux-amd64.tar.gz", "d0c90410e90204c9ca83b8539fac5c7aed01fd537207e4585849f8abc5df20b8"),
    ("linux", "arm64"): ("pandoc-3.12.1-linux-arm64.tar.gz", "445d96fd08801fe636cab1158b4f017ee320ac3b7446328b4fe2f902117b19b9"),
}
CROSSREF_ARCHIVES = {
    ("darwin", "arm64"): ("pandoc-crossref-macOS-ARM64.tar.xz", "5bd7ab1472c37c22b775042b1e8b82449a541ca1a2181e402e98a8def5d0ce76"),
    ("darwin", "x86_64"): ("pandoc-crossref-macOS-X64.tar.xz", "d3601abd35881aacdf3bd22445971228db8332073041b13bcf86bf3dae92593e"),
    ("windows", "x86_64"): ("pandoc-crossref-Windows-X64.7z", "6b14345ef08bc663c89e1114d714987765ceb966596efad6afbcf3331d13a50e"),
    ("linux", "x86_64"): ("pandoc-crossref-Linux-X64.tar.xz", "83d09646629234dfcd3d267e28184f46b9d468e98508efb3542b014634bfe999"),
    ("linux", "arm64"): ("pandoc-crossref-Linux-ARM64.tar.xz", "458a6fa28667a0e2673421b632e168218ffb4cded0dd5eea463a1b630178c1f6"),
}
BROWSERS = {
    "darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
               "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
               "/Applications/Chromium.app/Contents/MacOS/Chromium"],
    "windows": [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Google\Chrome\Application\chrome.exe"],
    "linux": ["chromium", "chromium-browser", "google-chrome", "microsoft-edge"],
}


def system() -> str:
    name = platform.system().lower()
    return "windows" if name.startswith("win") else name


def machine() -> str:
    value = platform.machine().lower()
    return {"amd64": "x86_64", "x64": "x86_64", "aarch64": "arm64"}.get(value, value)


def executable(name: str) -> str:
    return f"{name}.exe" if system() == "windows" else name


def find_in_tools(root: Path, folder: str, name: str) -> Path | None:
    base = root / ".tools" / folder
    if not base.is_dir():
        return None
    found = sorted(p for p in base.rglob(executable(name)) if p.is_file() and os.access(p, os.X_OK))
    return found[-1] if found else None


def version_of(command: list) -> str | None:
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    text = (completed.stdout or completed.stderr).strip().splitlines()
    return text[0] if completed.returncode == 0 and text else None


def browser() -> str | None:
    for candidate in BROWSERS.get(system(), []):
        if os.path.isabs(candidate):
            if Path(candidate).exists():
                return candidate
        elif shutil.which(candidate):
            return shutil.which(candidate)
    return None


def word_available() -> bool:
    if system() == "darwin":
        return Path("/Applications/Microsoft Word.app").exists()
    if system() == "windows":
        return any(Path(p).exists() for p in (r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
                                               r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE"))
    return False


def find(root: Path) -> dict:
    """Paths and versions of the export tools that this computer has."""
    pandoc = find_in_tools(root, "pandoc", "pandoc") or (Path(shutil.which("pandoc")) if shutil.which("pandoc") else None)
    crossref = find_in_tools(root, "pandoc-crossref", "pandoc-crossref") or (
        Path(shutil.which("pandoc-crossref")) if shutil.which("pandoc-crossref") else None)
    mmdc = root / ".tools" / "mermaid-cli" / "node_modules" / ".bin" / ("mmdc.cmd" if system() == "windows" else "mmdc")
    info = {"pandoc": str(pandoc) if pandoc else None, "pandoc_version": None,
            "crossref": str(crossref) if crossref else None, "crossref_version": None, "crossref_built_with": None,
            "mmdc": str(mmdc) if mmdc.exists() else None, "browser": browser(), "word": word_available(),
            "libreoffice": shutil.which("soffice") or shutil.which("libreoffice")}
    if pandoc:
        line = version_of([str(pandoc), "--version"]) or ""
        info["pandoc_version"] = line.replace("pandoc", "").strip() or None
    if crossref:
        line = version_of([str(crossref), "--version"]) or ""
        found = re.search(r"pandoc-crossref v?([\d.]+).*?Pandoc v?([\d.]+)", line)
        if found:
            info["crossref_version"], info["crossref_built_with"] = found.group(1), found.group(2)
    return info


def problems(info: dict, need_mermaid: bool) -> list:
    found = []
    if not info["pandoc"]:
        found.append("Pandoc is not installed")
    if not info["crossref"]:
        found.append("pandoc-crossref is not installed")
    if info["pandoc_version"] and info["crossref_built_with"] and info["pandoc_version"] != info["crossref_built_with"]:
        found.append(f"pandoc-crossref was built for Pandoc {info['crossref_built_with']}, but Pandoc {info['pandoc_version']} is installed")
    if need_mermaid and not (info["mmdc"] and info["browser"]):
        found.append("diagrams cannot be rendered: mermaid-cli or a Chrome-family browser is missing")
    return found


def download(url: str, target: Path, sha256: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + ".part")
    with urllib.request.urlopen(url, timeout=120) as response, open(partial, "wb") as stream:
        shutil.copyfileobj(response, stream)
    digest = hashlib.sha256(partial.read_bytes()).hexdigest()
    if digest != sha256:
        partial.unlink()
        raise RuntimeError(f"{target.name} does not match its published checksum; nothing was installed")
    partial.replace(target)


def unpack(archive: Path, folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    if archive.name.endswith(".zip"):
        with zipfile.ZipFile(archive) as package:
            package.extractall(folder)
            for info in package.infolist():
                mode = info.external_attr >> 16
                if mode & 0o111:
                    os.chmod(folder / info.filename, mode & 0o777)
    elif archive.name.endswith((".tar.gz", ".tar.xz")):
        with tarfile.open(archive) as package:
            package.extractall(folder)
    else:  # .7z: the system tar (libarchive) reads it on Windows 10 and later and on macOS
        subprocess.run(["tar", "-xf", str(archive), "-C", str(folder)], check=True)


def install(root: Path, components: list) -> list:
    done = []
    key = (system(), machine())
    downloads = root / ".tools" / "downloads"
    if "pandoc" in components:
        if key not in PANDOC_ARCHIVES:
            raise RuntimeError(f"no Pandoc {PANDOC_VERSION} build is listed for {key[0]} on {key[1]}")
        name, digest = PANDOC_ARCHIVES[key]
        download(PANDOC_RELEASE + name, downloads / name, digest)
        unpack(downloads / name, root / ".tools" / "pandoc" / PANDOC_VERSION)
        done.append(f"Pandoc {PANDOC_VERSION}")
    if "crossref" in components:
        if key not in CROSSREF_ARCHIVES:
            raise RuntimeError(f"no pandoc-crossref {CROSSREF_VERSION} build is listed for {key[0]} on {key[1]}")
        name, digest = CROSSREF_ARCHIVES[key]
        download(CROSSREF_RELEASE + name, downloads / name, digest)
        unpack(downloads / name, root / ".tools" / "pandoc-crossref" / CROSSREF_VERSION)
        done.append(f"pandoc-crossref {CROSSREF_VERSION}")
    if "mermaid" in components:
        npm = shutil.which("npm")
        if not npm:
            raise RuntimeError("npm (Node.js 22.13 or later) is needed for mermaid-cli; install Node.js first")
        folder = root / ".tools" / "mermaid-cli"
        folder.mkdir(parents=True, exist_ok=True)
        environment = dict(os.environ, PUPPETEER_SKIP_DOWNLOAD="true")
        subprocess.run([npm, "install", "--prefix", str(folder), "--ignore-scripts", "--no-audit", "--no-fund", "--save-exact",
                        f"@mermaid-js/mermaid-cli@{MERMAID_CLI_VERSION}"], check=True, env=environment,
                       capture_output=True, text=True)
        done.append(f"mermaid-cli {MERMAID_CLI_VERSION}")
    return done


def puppeteer_config(root: Path, browser_path: str) -> Path:
    path = root / ".tools" / "mermaid-cli" / "puppeteer-config.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"executablePath": browser_path, "headless": "shell", "args": ["--no-sandbox"]}), encoding="utf-8")
    return path


def python_info() -> str:
    return f"{platform.python_implementation()} {platform.python_version()} ({sys.platform})"
