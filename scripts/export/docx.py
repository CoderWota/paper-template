"""Word reference documents and checks of built DOCX files.

`build_reference_doc` edits Pandoc's default reference document as text, so that every namespace and attribute
that Word expects survives, and writes the section properties in the order that the Office Open XML schema requires.
The check functions read a built DOCX: native equations (OMML) in the body and the footnotes, drawings, text, core
properties, and the layout that its section properties and styles produce.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
M = "{http://schemas.openxmlformats.org/officeDocument/2006/math}"
TWIPS_PER_CM = 566.929
PAGES = {"A4": (11906, 16838), "letter": (12240, 15840)}
LINE = {"single": 240, "1.5": 360, "double": 480}
# Children of w:sectPr in schema order (ECMA-376, CT_SectPr).
SECTPR_ORDER = ("headerReference", "footerReference", "footnotePr", "endnotePr", "type", "pgSz", "pgMar", "paperSrc",
                "pgBorders", "lnNumType", "pgNumType", "cols", "formProt", "vAlign", "noEndnote", "titlePg", "textDirection",
                "bidi", "rtlGutter", "docGrid", "printerSettings", "sectPrChange")
HEADING_STYLES = ("Title", "Subtitle", "Author", "Date") + tuple(f"Heading{n}" for n in range(1, 10))
STRUCTURES = ((r"\\[dt]?frac|\\over\b|\\binom", "m:f"), (r"\\sqrt", "m:rad"),
              (r"\\(sum|prod|coprod|int|iint|iiint|oint|bigcup|bigcap|bigoplus|bigotimes)\b", "m:nary"),
              (r"\\begin\{[pbvBV]?matrix\}|\\begin\{array\}", "m:m"),
              (r"\\begin\{(aligned|align\*?|gathered|split|eqnarray\*?|cases)\}", "m:eqArr"),
              (r"\\(hat|vec|tilde|dot|ddot|check|breve|acute|grave|widehat|widetilde)\b", "m:acc"))


# Reference documents

def _style_block(styles: str, style_id: str) -> re.Match | None:
    return re.search(r'<w:style\b[^>]*w:styleId="%s"[^>]*>.*?</w:style>' % re.escape(style_id), styles, re.S)


def _set_in_style(styles: str, style_id: str, edit) -> str:
    block = _style_block(styles, style_id)
    if not block:
        return styles
    return styles[:block.start()] + edit(block.group(0)) + styles[block.end():]


def _fonts(font: str, east_asian: str | None) -> str:
    east = east_asian or font
    return f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:eastAsia="{east}" w:cs="{font}" />'


def _with_spacing(block: str, attributes: dict) -> str:
    """Set attributes on the first w:spacing of a paragraph-properties block, creating it if needed."""
    spacing = re.search(r"<w:spacing\b([^>]*?)/>", block)
    if spacing:
        current = dict(re.findall(r'w:(\w+)="([^"]*)"', spacing.group(1)))
        current.update(attributes)
        text = "<w:spacing " + " ".join(f'w:{k}="{v}"' for k, v in current.items()) + " />"
        return block[:spacing.start()] + text + block[spacing.end():]
    text = "<w:spacing " + " ".join(f'w:{k}="{v}"' for k, v in attributes.items()) + " />"
    if "<w:pPr>" in block:
        return block.replace("<w:pPr>", "<w:pPr>" + text, 1)
    if "<w:pPr />" in block:
        return block.replace("<w:pPr />", "<w:pPr>" + text + "</w:pPr>", 1)
    return re.sub(r"(<w:rPr>|<w:rPr />|</w:style>)", "<w:pPr>" + text + r"</w:pPr>\1", block, count=1)


def edit_styles(styles: str, settings: dict) -> tuple:
    applied = []
    font, east, size = settings.get("font"), settings.get("east_asian_font"), settings.get("size_pt")
    defaults = re.search(r"<w:rPrDefault>.*?</w:rPrDefault>", styles, re.S)
    if defaults and (font or size):
        block = defaults.group(0)
        if font:
            block = re.sub(r"<w:rFonts\b[^>]*/>", _fonts(font, east), block, count=1)
            applied.append(f"body font {font}" + (f", East Asian font {east}" if east else ""))
        if size:
            half = int(round(float(size) * 2))
            block = re.sub(r'<w:sz w:val="\d+"\s*/>', f'<w:sz w:val="{half}" />', block)
            block = re.sub(r'<w:szCs w:val="\d+"\s*/>', f'<w:szCs w:val="{half}" />', block)
            applied.append(f"body size {size} pt")
        styles = styles[:defaults.start()] + block + styles[defaults.end():]
    spacing = settings.get("line_spacing")
    if spacing:
        paragraph = re.search(r"<w:pPrDefault>.*?</w:pPrDefault>", styles, re.S)
        block = _with_spacing(paragraph.group(0), {"line": str(LINE[spacing]), "lineRule": "auto"})
        styles = styles[:paragraph.start()] + block + styles[paragraph.end():]
        applied.append(f"{spacing} line spacing")
    after = settings.get("space_after_pt")
    if after is not None:
        twips = str(int(round(float(after) * 20)))
        for style in ("BodyText", "FirstParagraph"):
            styles = _set_in_style(styles, style, lambda b: _with_spacing(b, {"before": "0", "after": twips}))
        applied.append(f"{after} pt after body paragraphs")
    table = settings.get("table_line_spacing")
    if table:
        styles = _set_in_style(styles, "Compact", lambda b: _with_spacing(b, {"line": str(LINE[table]), "lineRule": "auto"}))
        applied.append(f"{table} spacing in tables")
    heading_font = settings.get("heading_font")
    if heading_font:
        for style in HEADING_STYLES:
            styles = _set_in_style(styles, style, lambda b: re.sub(r"<w:rFonts\b[^>]*/>", _fonts(heading_font, east), b, count=1))
        applied.append(f"heading font {heading_font}")
    if settings.get("heading_color") == "black":
        for style in HEADING_STYLES:
            styles = _set_in_style(styles, style, lambda b: re.sub(r"<w:color\b[^>]*/>", '<w:color w:val="000000" />', b))
        applied.append("black headings")
    return styles, applied


def edit_section(document: str, settings: dict) -> tuple:
    applied = []
    sections = list(re.finditer(r"<w:sectPr\b[^>]*>.*?</w:sectPr>|<w:sectPr\b[^>]*/>", document, re.S))
    if not sections:
        raise ValueError("the reference document has no section properties")
    section = sections[-1]
    opening = re.match(r"<w:sectPr\b[^>]*", section.group(0)).group(0).rstrip("/") + ">"
    inner = re.sub(r"^<w:sectPr\b[^>]*>|</w:sectPr>$", "", section.group(0)) if not section.group(0).endswith("/>") else ""
    children = {}
    for child in re.finditer(r"<w:(\w+)\b[^>]*?(?:/>|>.*?</w:\1>)", inner, re.S):
        children.setdefault(child.group(1), []).append(child.group(0))
    page = settings.get("page")
    if page:
        width, height = PAGES[page]
        children["pgSz"] = [f'<w:pgSz w:w="{width}" w:h="{height}" />']
        applied.append(f"{page} pages")
    margins = settings.get("margins_cm")
    if margins is not None:
        twips = int(round(float(margins) * TWIPS_PER_CM))
        children["pgMar"] = [f'<w:pgMar w:top="{twips}" w:right="{twips}" w:bottom="{twips}" w:left="{twips}" '
                             f'w:header="709" w:footer="709" w:gutter="0" />']
        applied.append(f"{margins} cm margins")
    if settings.get("line_numbers") is True:
        children["lnNumType"] = ['<w:lnNumType w:countBy="1" w:restart="continuous" />']
        applied.append("line numbers")
    elif settings.get("line_numbers") is False:
        children.pop("lnNumType", None)
    unknown = [name for name in children if name not in SECTPR_ORDER]
    ordered = "".join("".join(children[name]) for name in SECTPR_ORDER + tuple(unknown) if name in children)
    rebuilt = f"{opening}{ordered}</w:sectPr>"
    return document[:section.start()] + rebuilt + document[section.end():], applied


def build_reference_doc(source: Path, target: Path, settings: dict) -> list:
    """Write a copy of the reference document `source` with the requested styles and page setup."""
    applied = []
    with zipfile.ZipFile(source) as package:
        items = [(info, package.read(info.filename)) for info in package.infolist()]
    output = []
    for info, data in items:
        if info.filename == "word/styles.xml":
            text, done = edit_styles(data.decode("utf-8"), settings)
            ET.fromstring(text.encode("utf-8"))
            data, applied = text.encode("utf-8"), applied + done
        elif info.filename == "word/document.xml":
            text, done = edit_section(data.decode("utf-8"), settings)
            ET.fromstring(text.encode("utf-8"))
            data, applied = text.encode("utf-8"), applied + done
        output.append((info, data))
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".part")
    with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as package:
        for info, data in output:
            package.writestr(info, data)
    temporary.replace(target)
    return applied


# Reading a built DOCX

def _xml(docx: Path, part: str):
    with zipfile.ZipFile(docx) as package:
        if part not in package.namelist():
            return None
        return ET.fromstring(package.read(part))


def omml_objects(docx: Path) -> list:
    """Every top-level native equation, in document order, from the body and then the footnotes."""
    found = []
    for part in ("word/document.xml", "word/footnotes.xml", "word/endnotes.xml"):
        root = _xml(docx, part)
        if root is None:
            continue
        parents = {child: parent for parent in root.iter() for child in parent}
        for element in root.iter(M + "oMath"):
            parent = parents.get(element)
            if parent is not None and parent.tag == M + "oMath":
                continue
            tags = {node.tag.replace(M, "m:") for node in element.iter() if node.tag.startswith(M)}
            text = "".join(node.text or "" for node in element.iter(M + "t"))
            found.append({"part": part, "display": parent is not None and parent.tag == M + "oMathPara", "tags": tags,
                          "text": text, "unparsed": bool(re.search(r"\\[A-Za-z]{2,}", text))})
    return found


def expected_structures(tex: str) -> set:
    return {tag for pattern, tag in STRUCTURES if re.search(pattern, tex)}


def ast_facts(ast: dict) -> dict:
    """Formulas (body, then notes), figures, Mermaid blocks left as code, and open markers in a Pandoc JSON AST."""
    facts = {"body": [], "notes": [], "figures": 0, "mermaid_code": 0, "todo": 0}

    def walk(node, target):
        if isinstance(node, dict):
            kind = node.get("t")
            if kind == "Note":
                walk(node.get("c"), facts["notes"])
                return
            if kind == "Math":
                target.append({"display": node["c"][0]["t"] == "DisplayMath", "tex": node["c"][1]})
            elif kind == "Figure":
                facts["figures"] += 1
            elif kind == "CodeBlock" and "mermaid" in node["c"][0][1]:
                facts["mermaid_code"] += 1
            elif kind == "Str" and "TODO" in node.get("c", ""):
                facts["todo"] += 1
            for value in node.values():
                walk(value, target)
        elif isinstance(node, list):
            for value in node:
                walk(value, target)

    walk(ast.get("blocks", []), facts["body"])
    return facts


def compare_formulas(facts: dict, objects: list) -> list:
    """Problems found when the source formulas are matched, in order, with the native equations."""
    problems = []
    for part, formulas in (("the body", facts["body"]), ("the notes", facts["notes"])):
        natives = [o for o in objects if (o["part"] == "word/document.xml") == (part == "the body")]
        if len(formulas) != len(natives):
            problems.append(f"{len(formulas)} formula(s) in {part} of the source, but {len(natives)} native equation(s) in the Word file")
        for number, (formula, native) in enumerate(zip(formulas, natives), start=1):
            label = f"formula {number} in {part} ({formula['tex'][:40].strip()})"
            if formula["display"] != native["display"]:
                problems.append(f"{label}: display and inline placement differ")
            missing = expected_structures(formula["tex"]) - native["tags"] - ({"m:acc"} if "m:bar" in native["tags"] else set())
            if missing:
                problems.append(f"{label}: the Word equation lacks {', '.join(sorted(missing))}")
            if native["unparsed"]:
                problems.append(f"{label}: the Word equation contains unconverted LaTeX: {native['text'][:40]}")
    return problems


def drawings(docx: Path) -> int:
    root = _xml(docx, "word/document.xml")
    return sum(1 for _ in root.iter(W + "drawing")) if root is not None else 0


def text_of(docx: Path) -> str:
    root = _xml(docx, "word/document.xml")
    return "".join(node.text or "" for node in root.iter(W + "t")) if root is not None else ""


def core_properties(docx: Path) -> dict:
    root = _xml(docx, "docProps/core.xml")
    if root is None:
        return {}
    return {node.tag.split("}")[-1]: (node.text or "") for node in root}


def _style_chain(styles, style_id: str) -> list:
    by_id = {s.get(W + "styleId"): s for s in styles.iter(W + "style")}
    chain, current = [], by_id.get(style_id)
    while current is not None and current not in chain:
        chain.append(current)
        based = current.find(W + "basedOn")
        current = by_id.get(based.get(W + "val")) if based is not None else None
    return chain


def layout(docx: Path) -> dict:
    """Page size and margins, line numbering, and the body text's font, size, and line spacing."""
    facts: dict = {}
    document = _xml(docx, "word/document.xml")
    sections = list(document.iter(W + "sectPr")) if document is not None else []
    if sections:
        section = sections[-1]
        size, margins = section.find(W + "pgSz"), section.find(W + "pgMar")
        if size is not None:
            width, height = int(size.get(W + "w")), int(size.get(W + "h"))
            facts["page"] = next((name for name, (w, h) in PAGES.items() if abs(w - width) <= 20 and abs(h - height) <= 20),
                                 f"{width}x{height} twips")
        if margins is not None:
            facts["margins_cm"] = sorted({round(int(margins.get(W + side)) / TWIPS_PER_CM, 2) for side in ("top", "right", "bottom", "left")})
        facts["line_numbers"] = section.find(W + "lnNumType") is not None
    styles = _xml(docx, "word/styles.xml")
    if styles is not None:
        defaults = styles.find(f"{W}docDefaults")
        chain = _style_chain(styles, "BodyText")
        sources = [s.find(W + "rPr") for s in chain] + [defaults.find(f"{W}rPrDefault/{W}rPr") if defaults is not None else None]
        paragraph_sources = [s.find(W + "pPr") for s in chain] + [defaults.find(f"{W}pPrDefault/{W}pPr") if defaults is not None else None]
        for properties in sources:
            fonts = properties.find(W + "rFonts") if properties is not None else None
            if fonts is not None and "font" not in facts:
                facts["font"] = fonts.get(W + "ascii") or "theme font"
            size = properties.find(W + "sz") if properties is not None else None
            if size is not None and "size_pt" not in facts:
                facts["size_pt"] = int(size.get(W + "val")) / 2
        for properties in paragraph_sources:
            spacing = properties.find(W + "spacing") if properties is not None else None
            if spacing is not None and spacing.get(W + "line") and "line_spacing" not in facts:
                value = int(spacing.get(W + "line"))
                facts["line_spacing"] = next((name for name, v in LINE.items() if v == value), f"{value}/240")
        facts.setdefault("line_spacing", "single")
    return facts
