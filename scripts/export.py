#!/usr/bin/env python3
"""Build formatted outputs of the manuscript with an output profile, check them, render them, and freeze releases.

An output profile lives in requirements/profiles/<profile-id>/: profile.yaml holds the export settings and the
checkable expectations, templates/ holds the Word reference document and an optional CSL style, originals/ holds the
supplied guidelines, and requirements.md maps each adopted rule to its source, implementation, and check. A build
assembles the files that manuscript/manifest.yaml lists with Pandoc, pandoc-crossref, citeproc, and the workspace's
Lua filters, renders Mermaid diagrams as figures, and checks the DOCX: one native Word equation per source formula
with matching structure, figures, references, citations, the title, authors, and keywords that manuscript/metadata.yaml
declares, layout expectations, word limits, and anonymization.
Previews go to outputs/preview/<profile-id>/; a release copies a passing, current build into outputs/releases/<id>/
and is never overwritten.

Usage:
  python scripts/export.py tools
  python scripts/export.py install --component pandoc|crossref|mermaid [...]
  python scripts/export.py profile-init --id ID --name NAME
  python scripts/export.py reference-doc --profile ID [--page A4|letter] [--margins-cm N] [--font NAME] [--east-asian-font NAME]
      [--size-pt N] [--line-spacing single|1.5|double] [--space-after-pt N] [--table-line-spacing single|1.5|double]
      [--heading-font NAME] [--heading-color black|theme] [--line-numbers yes|no]
  python scripts/export.py build --profile ID [--render]
Profile keys: output, reference_doc, csl, number_sections, figure_prefix[_plural], table_prefix[_plural],
  equation_prefix[_plural], section_prefix[_plural], figure_title, table_title, table_equations, anonymize,
  mermaid_scale, doc_* (reference-document settings), and expect_page, expect_margins_cm, expect_font, expect_size_pt,
  expect_line_spacing, expect_line_numbers, expect_max_words, expect_anonymized.
  python scripts/export.py verify --profile ID
  python scripts/export.py render --docx PATH
  python scripts/export.py release --profile ID --id RELEASE_ID [--allow-open-items]
All commands take --root WORKSPACE. Exit status: 0 done and checks passed; 1 a check failed; 3 refused.
Uses only the Python standard library; Pandoc, pandoc-crossref, and mermaid-cli are external tools.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import manuscript  # noqa: E402
from text_rules import AI_AUTHOR, open_marker, signature_problems  # noqa: E402
from export import docx, tools  # noqa: E402
from ingestion.common import sha256_file, update_readme, write_json_atomic, write_text_atomic  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OWNER = "scripts/export.py"
FILTERS = Path(__file__).resolve().parent / "export"
DOC_SETTINGS = ("page", "margins_cm", "font", "east_asian_font", "size_pt", "line_spacing", "space_after_pt",
                "table_line_spacing", "heading_font", "heading_color", "line_numbers")
DEFAULT_PROFILE = """# Output profile, maintained by the agent. requirements.md maps each adopted rule to its source, implementation, and check.
version: 1
name: {name}
output: docx
reference_doc: templates/reference.docx
number_sections: false
figure_prefix: Figure
table_prefix: Table
equation_prefix: Equation
section_prefix: Section
figure_title: Figure
table_title: Table
mermaid_scale: 3
"""


class Refused(Exception):
    pass


# Profiles

def profile_folder(root: Path, profile_id: str) -> Path:
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", profile_id):
        raise Refused("a profile ID uses lowercase ASCII letters, digits, and single hyphens, for example journal-of-tests")
    return root / "requirements" / "profiles" / profile_id


def read_profile(root: Path, profile_id: str) -> dict:
    path = profile_folder(root, profile_id) / "profile.yaml"
    if not path.is_file():
        raise Refused(f"requirements/profiles/{profile_id}/profile.yaml does not exist; create the profile first")
    values = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = re.sub(r"\s+#.*$", "", raw).strip() if not raw.lstrip().startswith("#") else ""
        if not line:
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise Refused(f"profile.yaml cannot read the line {raw!r}")
        value = manuscript.unquote(value.strip())
        values[key.strip()] = {"true": True, "false": False, "yes": True, "no": False}.get(value.lower(), value)
    return values


def write_profile_values(root: Path, profile_id: str, updates: dict) -> None:
    path = profile_folder(root, profile_id) / "profile.yaml"
    lines = path.read_text(encoding="utf-8").splitlines()
    for key, value in updates.items():
        text = f"{key}: {'true' if value is True else 'false' if value is False else value}"
        for index, line in enumerate(lines):
            if re.match(rf"^{re.escape(key)}\s*:", line):
                lines[index] = text
                break
        else:
            lines.append(text)
    write_text_atomic(path, "\n".join(lines) + "\n")


def pandoc_path(root: Path) -> str:
    info = tools.find(root)
    if not info["pandoc"]:
        raise Refused("Pandoc is not installed; install it with the researcher's consent: python scripts/export.py install --component pandoc")
    return info["pandoc"]


def command_profile_init(args, root: Path) -> int:
    folder = profile_folder(root, args.id)
    if (folder / "profile.yaml").exists():
        raise Refused(f"the profile {args.id} already exists")
    pandoc = pandoc_path(root)
    (folder / "templates").mkdir(parents=True, exist_ok=True)
    write_text_atomic(folder / "profile.yaml", DEFAULT_PROFILE.format(name=args.name))
    completed = subprocess.run([pandoc, "-o", str(folder / "templates" / "reference.docx"), "--print-default-data-file", "reference.docx"],
                               capture_output=True, text=True)
    if completed.returncode != 0:
        raise Refused(f"Pandoc could not write its default reference document: {completed.stderr.strip()[:300]}")
    update_readme(folder / "README.md", f"Output profile: {args.name}", (
        f"The output profile `{args.id}` ({args.name}): the requirements for this output and the resources that produce it. "
        "`requirements.md` lists each adopted rule with its source, implementation, and check result; `profile.yaml` holds the "
        "export settings and the checkable expectations; [`originals/`](originals/README.md) keeps the supplied guidelines and "
        "examples unchanged; [`templates/`](templates/README.md) holds the Word reference document and any citation style. "
        "Builds go to `outputs/preview/` and releases to `outputs/releases/`."), OWNER)
    update_readme(folder / "originals" / "README.md", f"Originals: {args.id}", (
        f"Author guidelines, journal instructions, templates, and example articles supplied for the profile `{args.id}`, "
        "exactly as received. They are the sources of the rules in `../requirements.md`; nothing here is edited."), OWNER)
    update_readme(folder / "templates" / "README.md", f"Templates: {args.id}", (
        f"Format resources used by the build of `{args.id}`: `reference.docx` provides Word styles and page setup "
        "(rebuilt by `python scripts/export.py reference-doc` from the settings in `../profile.yaml`), and a `.csl` file, when "
        "present, sets the citation style. A supplied journal template is kept in `../originals/`; what is adapted from it "
        "is recorded in `../requirements.md`."), OWNER)
    print(f"Created the profile {args.id} with Pandoc's default Word styles. Record the adopted rules in requirements.md.")
    return 0


def command_reference_doc(args, root: Path) -> int:
    folder = profile_folder(root, args.profile)
    profile = read_profile(root, folder.name)
    updates = {}
    for key in DOC_SETTINGS:
        value = getattr(args, key, None)
        if value is not None:
            updates[f"doc_{key}"] = {"yes": True, "no": False}.get(value, value) if isinstance(value, str) else value
    if updates:
        write_profile_values(root, folder.name, updates)
        profile = read_profile(root, folder.name)
    settings = {key: profile[f"doc_{key}"] for key in DOC_SETTINGS if f"doc_{key}" in profile}
    if settings.get("heading_color") == "theme":
        settings.pop("heading_color")
    pandoc = pandoc_path(root)
    with tempfile.TemporaryDirectory() as temporary:
        default = Path(temporary) / "default.docx"
        subprocess.run([pandoc, "-o", str(default), "--print-default-data-file", "reference.docx"], check=True, capture_output=True)
        applied = docx.build_reference_doc(default, folder / "templates" / "reference.docx", settings)
    print(f"Rebuilt the Word reference document of {folder.name}: " + (", ".join(applied) if applied else "Pandoc's defaults") + ".")
    return 0


# Building

def mermaid_blocks(paths: list) -> list:
    blocks = []
    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        index = 0
        while index < len(lines):
            fence = manuscript.FENCE.match(lines[index])
            if fence:
                marker, start = fence.group(2), index
                index += 1
                while index < len(lines) and not lines[index].strip().startswith(marker[0] * len(marker)):
                    index += 1
                if fence.group(3).lower() == "mermaid":
                    blocks.append("\n".join(lines[start + 1:index]))
            index += 1
    return blocks


def render_diagrams(root: Path, info: dict, blocks: list, folder: Path, scale: str) -> list:
    """Render each Mermaid block to <sha1>.png in folder; return the problems."""
    problems = []
    if not blocks:
        return problems
    if not (info["mmdc"] and info["browser"]):
        return [f"{len(blocks)} diagram(s) cannot be rendered: mermaid-cli or a Chrome-family browser is missing"]
    folder.mkdir(parents=True, exist_ok=True)
    config = tools.puppeteer_config(root, info["browser"])
    for text in blocks:
        name = hashlib.sha1(text.encode("utf-8")).hexdigest()
        target = folder / f"{name}.png"
        if target.is_file():
            continue
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "diagram.mmd"
            source.write_text(text, encoding="utf-8")
            completed = subprocess.run([info["mmdc"], "-p", str(config), "-i", str(source), "-o", str(target), "-s", str(scale),
                                        "-b", "white", "-q"], capture_output=True, text=True, timeout=180)
        if completed.returncode != 0 or not target.is_file():
            first = text.splitlines()[0] if text.splitlines() else ""
            problems.append(f"a diagram could not be rendered ({first[:40]}...): " + (completed.stderr.strip().splitlines() or ["no image"])[-1][:200])
    return problems


def pandoc_command(root: Path, info: dict, profile: dict, folder: Path, sections: list, figures: Path) -> list:
    command = [info["pandoc"], "--from", "markdown", "--resource-path", "manuscript"]
    metadata = manuscript.metadata_name(root, manuscript.read_manifest(root))
    if metadata and (root / "manuscript" / metadata).is_file():
        command += ["--metadata-file", f"manuscript/{metadata}"]
    command += [f"manuscript/{name}" for name in sections]
    # Cross-reference settings go in a metadata file, because prefixes with a plural form are lists.
    settings = {"autoSectionLabels": True, "mermaid-figures": figures.as_posix()}
    for key, name in (("figure_prefix", "figPrefix"), ("table_prefix", "tblPrefix"), ("equation_prefix", "eqnPrefix"),
                      ("section_prefix", "secPrefix")):
        if profile.get(key):
            plural = profile.get(f"{key}_plural")
            settings[name] = [str(profile[key]), str(plural)] if plural else str(profile[key])
    for key, name in (("figure_title", "figureTitle"), ("table_title", "tableTitle")):
        if profile.get(key):
            settings[name] = str(profile[key])
    if profile.get("number_sections") is True:
        settings["numberSections"] = True
        command += ["--number-sections"]
    if profile.get("table_equations") is True:
        settings["tableEqns"] = True
    crossref = figures.parent / "crossref.yaml"
    crossref.parent.mkdir(parents=True, exist_ok=True)
    write_text_atomic(crossref, "".join(f"{key}: {json.dumps(value, ensure_ascii=False)}\n" for key, value in settings.items()))
    command += ["--metadata-file", str(crossref), "--lua-filter", str(FILTERS / "equation-labels.lua"),
                "--lua-filter", str(FILTERS / "mermaid-figures.lua"), "--filter", info["crossref"]]
    if (root / "references" / "bibliography.bib").is_file():
        command += ["--citeproc", "--bibliography", "references/bibliography.bib"]
        if profile.get("csl"):
            command += ["--csl", str(folder / profile["csl"])]
    if profile.get("anonymize") is True:
        command += ["-M", "author=", "-M", "institute="]
    command += ["--reference-doc", str(folder / profile.get("reference_doc", "templates/reference.docx"))]
    return command


def build_inputs(root: Path, folder: Path, profile: dict, sections: list) -> list:
    paths = [f"manuscript/{name}" for name in sections] + ["manuscript/manifest.yaml"]
    metadata = manuscript.metadata_name(root, manuscript.read_manifest(root))
    if metadata:
        paths.append(f"manuscript/{metadata}")
    for value in ("references/bibliography.bib",):
        if (root / value).is_file():
            paths.append(value)
    relative = folder.relative_to(root).as_posix()
    paths += [f"{relative}/profile.yaml", f"{relative}/{profile.get('reference_doc', 'templates/reference.docx')}"]
    if profile.get("csl"):
        paths.append(f"{relative}/{profile['csl']}")
    for name in sections:
        for image in manuscript.IMAGE.finditer((root / "manuscript" / name).read_text(encoding="utf-8")):
            if (root / "manuscript" / image.group(2)).is_file():
                paths.append(f"manuscript/{image.group(2)}")
    return [{"path": p, "sha256": sha256_file(root / p)} for p in dict.fromkeys(paths) if (root / p).is_file()]


def verify(root: Path, profile: dict, output: Path, facts: dict, warnings: list, sections: list) -> list:
    """Checks of a built DOCX: (name, passed, detail)."""
    checks = []
    signatures = [problem for part, paragraph in docx.paragraph_texts(output)
                  for problem in signature_problems(paragraph, part)]
    signatures.extend(f"file properties: AI author in {key}" for key, value in docx.core_properties(output).items()
                      if key in ("creator", "lastModifiedBy") and AI_AUTHOR.search(value))
    checks.append(("AI signatures", not signatures, "; ".join(signatures) or "no recognized AI signature or AI author"))
    objects = docx.omml_objects(output)
    formula_problems = docx.compare_formulas(facts, objects)
    total = len(facts["body"]) + len(facts["notes"])
    checks.append(("native equations", not formula_problems,
                   "; ".join(formula_problems) or f"{total} formula(s), each a native Word equation with matching structure"))
    images = facts.get("images", 0)
    drawn = docx.drawings(output)
    checks.append(("figures", drawn >= images and facts["mermaid_code"] == 0,
                   f"{images} image(s) in the source, {drawn} in the Word file" +
                   (f"; {facts['mermaid_code']} diagram(s) left as code" if facts["mermaid_code"] else "")))
    text = docx.text_of(output)
    unresolved = sorted(set(re.findall(r"¿([^?]+)\?", text))) + [w for w in warnings if "Undefined cross-reference" in w]
    checks.append(("cross-references", not unresolved, "all resolved" if not unresolved else "unresolved: " + ", ".join(unresolved[:8])))
    missing = [w for w in warnings if "Citeproc" in w and "not found" in w]
    checks.append(("citations", not missing, "all keys found" if not missing else "; ".join(missing[:8])))
    declared = facts.get("front_matter") or {}
    lost, found = docx.compare_front_matter(declared, output)
    checks.append(("front matter", not lost, "; ".join(lost) if lost else
                   ("in the Word file, from the manuscript metadata: " + ", ".join(found)) if found else
                   "the manuscript metadata declares no title, authors, or keywords, so the Word file has none"))
    fetched = [w for w in warnings if "Could not fetch" in w or "could not be found" in w.lower()]
    if fetched:
        checks.append(("resources", False, "; ".join(fetched[:5])))
    found = docx.layout(output)
    expectations = {"expect_page": "page", "expect_font": "font", "expect_size_pt": "size_pt", "expect_line_spacing": "line_spacing",
                    "expect_line_numbers": "line_numbers"}
    for key, fact in expectations.items():
        if key in profile:
            expected, actual = profile[key], found.get(fact)
            same = str(expected).lower() == str(actual).lower() or (fact == "size_pt" and actual is not None and float(expected) == float(actual))
            checks.append((key.replace("expect_", "") .replace("_", " "), same, f"expected {expected}, found {actual}"))
    if "expect_margins_cm" in profile:
        margins = found.get("margins_cm") or []
        same = margins == [round(float(profile["expect_margins_cm"]), 2)]
        checks.append(("margins", same, f"expected {profile['expect_margins_cm']} cm, found {margins}"))
    if "expect_max_words" in profile:
        words = sum(manuscript.count_words((root / "manuscript" / name).read_text(encoding="utf-8"))[0] for name in sections)
        limit = int(profile["expect_max_words"])
        checks.append(("length", words <= limit, f"{words} words in the listed sections (limit {limit}; check which parts the venue counts)"))
    if profile.get("expect_anonymized") is True:
        core = docx.core_properties(output)
        names = [v for k, v in core.items() if k in ("creator", "lastModifiedBy") and v.strip()]
        checks.append(("anonymization", not names, "no author in the file properties" if not names else "file properties name " + ", ".join(names)))
    output_open_items = sum(open_marker(paragraph) for _, paragraph in docx.paragraph_texts(output))
    open_items = facts["todo"] + output_open_items
    checks.append(("open items", open_items == 0, f"{open_items} open marker(s) in the text"))
    return checks


def command_build(args, root: Path) -> int:
    folder = profile_folder(root, args.profile)
    profile = read_profile(root, args.profile)
    analysis = manuscript.analyse(root)
    paths = analysis["paths"]
    if analysis["problems"] or not paths:
        raise Refused(f"the manuscript check reports {len(analysis['problems'])} problem(s); fix them first "
                      "(python scripts/manuscript.py check)" if analysis["problems"] else "the manifest lists no section files yet")
    info = tools.find(root)
    sections = [name for name, _ in paths]
    blocks = mermaid_blocks([path for _, path in paths])
    missing = tools.problems(info, bool(blocks))
    if any("Pandoc" in m or "pandoc-crossref" in m for m in missing):
        raise Refused("; ".join(missing))
    out = root / "outputs" / "preview" / args.profile
    figures = out / "figures"
    diagram_problems = render_diagrams(root, info, blocks, figures, profile.get("mermaid_scale", "3"))
    command = pandoc_command(root, info, profile, folder, sections, figures.resolve())
    output = out / "manuscript.docx"
    out.mkdir(parents=True, exist_ok=True)
    built = subprocess.run(command + ["-o", str(output)], cwd=root, capture_output=True, text=True, encoding="utf-8")
    if built.returncode != 0:
        print(f"Pandoc failed: {built.stderr.strip()[:600]}")
        return 1
    tree = subprocess.run(command + ["-t", "json"], cwd=root, capture_output=True, text=True, encoding="utf-8")
    ast = json.loads(tree.stdout)
    facts = docx.ast_facts(ast)
    facts["front_matter"] = docx.front_matter(ast)
    facts["images"] = len(re.findall(r'"t":\s*"Image"', tree.stdout))
    warnings = [line.strip() for line in built.stderr.splitlines() if line.strip()]
    checks = verify(root, profile, output, facts, warnings, sections)
    for problem in diagram_problems:
        checks.append(("diagrams", False, problem))
    passed = all(ok for name, ok, _ in checks if name != "open items")
    record = {"schema": "paper-template.build/1", "profile": args.profile, "built": datetime.now().isoformat(timespec="seconds"),
              "status": "passed" if passed else "failed", "inputs": build_inputs(root, folder, profile, sections),
              "tools": {"pandoc": info["pandoc_version"], "pandoc-crossref": info["crossref_version"],
                        "mermaid-cli": tools.MERMAID_CLI_VERSION if info["mmdc"] and blocks else None, "python": tools.python_info()},
              "command": [Path(c).name if os.path.isabs(c) else c for c in command] + ["-o", "manuscript.docx"],
              "warnings": warnings, "checks": [{"name": n, "passed": ok, "detail": d} for n, ok, d in checks],
              "output": {"file": "manuscript.docx", "sha256": sha256_file(output)}}
    write_json_atomic(out / "build.json", record)
    print(f"Built outputs/preview/{args.profile}/manuscript.docx with the profile {args.profile}: {record['status']}.")
    for name, ok, detail in checks:
        print(f"  [{'pass' if ok else 'FAIL' if name != 'open items' else 'open'}] {name}: {detail}")
    if args.render and passed:
        render(root, output)
    return 0 if passed else 1


def stale_inputs(root: Path, record: dict) -> list:
    return [item["path"] for item in record["inputs"] if not (root / item["path"]).is_file() or sha256_file(root / item["path"]) != item["sha256"]]


def command_verify(args, root: Path) -> int:
    path = root / "outputs" / "preview" / args.profile / "build.json"
    if not path.is_file():
        raise Refused(f"there is no build of {args.profile}; run build first")
    record = json.loads(path.read_text(encoding="utf-8"))
    changed = stale_inputs(root, record)
    output = path.parent / record["output"]["file"]
    if not output.is_file() or sha256_file(output) != record["output"]["sha256"]:
        changed.append(f"outputs/preview/{args.profile}/{record['output']['file']}")
    print(f"Build of {record['built'][:16]} with {args.profile}: {record['status']}" +
          (f"; out of date because these changed: {', '.join(changed)}" if changed else "; still current."))
    for check in record["checks"]:
        print(f"  [{'pass' if check['passed'] else 'FAIL'}] {check['name']}: {check['detail']}")
    return 0 if record["status"] == "passed" and not changed else 1


# Rendering

def render(root: Path, output: Path) -> Path | None:
    pdf = output.with_suffix(".pdf")
    if tools.system() == "darwin" and tools.word_available():
        container = Path.home() / "Library" / "Containers" / "com.microsoft.Word" / "Data" / "Documents" / "paper-template-export"
        container.mkdir(parents=True, exist_ok=True)
        staged, staged_pdf = container / output.name, container / pdf.name
        shutil.copy2(output, staged)
        script = ['with timeout of 180 seconds', 'tell application "Microsoft Word"', f'open file name "{staged}"',
                  f'save as active document file name "{staged_pdf}" file format format PDF', "close active document saving no",
                  "end tell", "end timeout"]
        completed = subprocess.run(["osascript"] + sum((["-e", line] for line in script), []), capture_output=True, text=True, timeout=240)
        if completed.returncode == 0 and staged_pdf.is_file():
            shutil.move(str(staged_pdf), pdf)
            staged.unlink(missing_ok=True)
            print(f"Rendered {pdf.relative_to(root).as_posix()} with Microsoft Word.")
            return pdf
        print("Microsoft Word did not render the file; it may be showing a dialog that needs the researcher. " + completed.stderr.strip()[:200])
        return None
    if tools.system() == "windows" and tools.word_available():
        script = (f"$w = New-Object -ComObject Word.Application; $w.Visible = $false; "
                  f"$d = $w.Documents.Open('{output}', $false, $true); $d.SaveAs([ref]'{pdf}', [ref]17); $d.Close($false); $w.Quit()")
        completed = subprocess.run(["powershell", "-NoProfile", "-Command", script], capture_output=True, text=True, timeout=240)
        if completed.returncode == 0 and pdf.is_file():
            print(f"Rendered {pdf.relative_to(root).as_posix()} with Microsoft Word.")
            return pdf
    info = tools.find(root)
    if info["libreoffice"]:
        subprocess.run([info["libreoffice"], "--headless", "--convert-to", "pdf", "--outdir", str(output.parent), str(output)],
                       capture_output=True, timeout=240)
        if pdf.is_file():
            print(f"Rendered {pdf.relative_to(root).as_posix()} with LibreOffice (its layout can differ from Word's).")
            return pdf
    print("No application that renders Word files is available, so the layout could not be inspected.")
    return None


def command_render(args, root: Path) -> int:
    output = Path(args.docx)
    output = output if output.is_absolute() else root / output
    if not output.is_file():
        raise Refused(f"{args.docx} does not exist")
    return 0 if render(root, output) else 1


# Releases

def command_release(args, root: Path) -> int:
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", args.id):
        raise Refused("a release ID uses lowercase ASCII letters, digits, and single hyphens, for example 2026-11-journal-a-round-1")
    target = root / "outputs" / "releases" / args.id
    if target.exists():
        raise Refused(f"the release {args.id} already exists and is never overwritten; choose a new release ID")
    preview = root / "outputs" / "preview" / args.profile
    path = preview / "build.json"
    if not path.is_file():
        raise Refused(f"there is no build of {args.profile}; build and inspect it first")
    record = json.loads(path.read_text(encoding="utf-8"))
    if record["status"] != "passed":
        raise Refused("the latest build did not pass its checks")
    changed = stale_inputs(root, record)
    output = preview / record["output"]["file"]
    if changed or sha256_file(output) != record["output"]["sha256"]:
        raise Refused("the build is out of date (" + ", ".join(changed or [record["output"]["file"]]) + " changed); build it again")
    open_items = next((c for c in record["checks"] if c["name"] == "open items" and not c["passed"]), None)
    if open_items and not args.allow_open_items:
        raise Refused(f"{open_items['detail']}; resolve them or confirm a release with open items")
    staging = root / "outputs" / "releases" / f".{args.id}.part"
    shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True)
    files = [output] + [p for p in (output.with_suffix(".pdf"),) if p.is_file() and p.stat().st_mtime >= output.stat().st_mtime]
    for file in files:
        shutil.copy2(file, staging / file.name)
    if (preview / "figures").is_dir():
        shutil.copytree(preview / "figures", staging / "figures")
    release = {"schema": "paper-template.release/1", "release": args.id, "profile": args.profile,
               "created": datetime.now().isoformat(timespec="seconds"), "build": record,
               "files": [{"file": p.relative_to(staging).as_posix(), "sha256": sha256_file(p)} for p in sorted(staging.rglob("*")) if p.is_file()]}
    write_json_atomic(staging / "release.json", release)
    update_readme(staging / "README.md", f"Release {args.id}", (
        f"A frozen package made on {release['created'][:10]} from the build of {record['built'][:16]} with the output profile "
        f"`{args.profile}`. `release.json` records the checksums of every file, of the manuscript and profile inputs, the tool "
        "versions, the build command, and the check results. This folder is never edited or rebuilt; a later version is a new "
        "release. A release is not a submission: submitting it is the researcher's separate decision." +
        (f" It was released with open items: {open_items['detail']}." if open_items else "")), OWNER)
    if (staging / "figures").is_dir():
        update_readme(staging / "figures" / "README.md", f"Figures of {args.id}", (
            "The diagram figures rendered for this release, named by the checksum of their Mermaid source. They are embedded in "
            "the Word file as well; venues that ask for separate figure files can take them from here."), OWNER)
    staging.rename(target)
    for file in target.rglob("*"):
        if file.is_file():
            os.chmod(file, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
    print(f"Released outputs/releases/{args.id}/ ({len(files)} file(s) and the build record). It will not be overwritten.")
    return 0


def command_tools(args, root: Path) -> int:
    info = tools.find(root)
    print(f"Pandoc: {info['pandoc_version'] or 'not installed'}" + (f" ({info['pandoc']})" if info["pandoc"] else ""))
    print(f"pandoc-crossref: {info['crossref_version'] or 'not installed'}" + (f", built for Pandoc {info['crossref_built_with']}" if info["crossref_built_with"] else ""))
    print(f"mermaid-cli: {'installed' if info['mmdc'] else 'not installed'}; browser: {info['browser'] or 'none found'}")
    print(f"Microsoft Word: {'available' if info['word'] else 'not found'}; LibreOffice: {info['libreoffice'] or 'not found'}")
    for problem in tools.problems(info, True):
        print(f"Needs attention: {problem}")
    return 0


def command_install(args, root: Path) -> int:
    try:
        done = tools.install(root, args.component)
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f"Installation failed: {error}")
        return 1
    print("Installed into .tools/: " + ", ".join(done) + ".")
    return 0


def main(argv: list | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")
    parser = argparse.ArgumentParser(description="Build, check, render, and release formatted outputs of the manuscript.")
    parser.add_argument("--root", type=Path, default=ROOT, help="workspace root (default: the parent of the scripts folder)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("tools", help="report the export tools on this computer")
    install = commands.add_parser("install", help="install export tools into .tools/ (needs the researcher's consent)")
    install.add_argument("--component", action="append", required=True, choices=("pandoc", "crossref", "mermaid"))
    init = commands.add_parser("profile-init", help="create an output profile with Pandoc's default Word styles")
    init.add_argument("--id", required=True)
    init.add_argument("--name", required=True)
    reference = commands.add_parser("reference-doc", help="rebuild a profile's Word reference document from its settings")
    reference.add_argument("--profile", required=True)
    reference.add_argument("--page", choices=sorted(docx.PAGES))
    reference.add_argument("--margins-cm", dest="margins_cm")
    reference.add_argument("--font")
    reference.add_argument("--east-asian-font", dest="east_asian_font")
    reference.add_argument("--size-pt", dest="size_pt")
    reference.add_argument("--line-spacing", dest="line_spacing", choices=sorted(docx.LINE))
    reference.add_argument("--space-after-pt", dest="space_after_pt")
    reference.add_argument("--table-line-spacing", dest="table_line_spacing", choices=sorted(docx.LINE))
    reference.add_argument("--heading-font", dest="heading_font")
    reference.add_argument("--heading-color", dest="heading_color", choices=("black", "theme"))
    reference.add_argument("--line-numbers", dest="line_numbers", choices=("yes", "no"))
    build = commands.add_parser("build", help="build and check the DOCX preview with a profile")
    build.add_argument("--profile", required=True)
    build.add_argument("--render", action="store_true", help="also render a PDF with Word or LibreOffice for inspection")
    verify_command = commands.add_parser("verify", help="show the checks of the latest build and whether it is still current")
    verify_command.add_argument("--profile", required=True)
    render_command = commands.add_parser("render", help="render a DOCX to PDF with Word or LibreOffice")
    render_command.add_argument("--docx", required=True)
    release = commands.add_parser("release", help="freeze the latest passing, current build into outputs/releases/")
    release.add_argument("--profile", required=True)
    release.add_argument("--id", required=True)
    release.add_argument("--allow-open-items", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    handlers = {"tools": command_tools, "install": command_install, "profile-init": command_profile_init,
                "reference-doc": command_reference_doc, "build": command_build, "verify": command_verify,
                "render": command_render, "release": command_release}
    try:
        return handlers[args.command](args, root)
    except (Refused, manuscript.Refused) as error:
        print(f"Refused: {error}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
