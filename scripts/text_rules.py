"""Language-aware text checks used by manuscript and DOCX validation.

These helpers intentionally detect conventions without selecting a manuscript
language. English, Chinese, Japanese, and mixed text remain valid inputs; the
rules only report explicit formatting or attribution markers.
"""

from __future__ import annotations

import json
import re
import string
import unicodedata
from pathlib import Path


CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]")
WORD = re.compile(r"[A-Za-z0-9\u00c0-\u024f]+(?:['\u2019\-][A-Za-z0-9\u00c0-\u024f]+)*")
_CJK_OR_JAPANESE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\u3040-\u30ff\uac00-\ud7af]")

# Technical citation syntax stays ASCII at the start, but text around it may
# be Unicode. A CJK or Japanese character before @ is therefore valid.
_CITATION_START = re.compile(r"(?<![A-Za-z0-9_@./\\])-?@")
_CITATION_TAIL = re.compile(r"[^\s@\[\](){}<>\"'“”‘’]+")

_RULES = json.loads((Path(__file__).with_name("text_rules.json")).read_text(encoding="utf-8"))
_NUMBERED_LABELS = tuple(_RULES.get("numbered_labels", []))
_OPEN_MARKERS = tuple(_RULES.get("open_markers", []))
_AI_NAMES = tuple(_RULES.get("ai_names", []))
_AI_ROLES = tuple(_RULES.get("ai_signature_roles", []))
_AI_PREFIXES = tuple(_RULES.get("ai_signature_prefixes", []))
_AI_SUFFIXES = tuple(_RULES.get("ai_signature_suffixes", []))

_EN_HAND_NUMBERED = re.compile(
    r"(?<![A-Za-z0-9_@])(?:figure|fig\.|table|equation|eq\.|section|sect\.)\s*[\(（]?\s*[0-9０-９]+\s*[\)）]?",
    re.I,
)
_NUMBERED_LABEL_PATTERN = "|".join(map(re.escape, _NUMBERED_LABELS)) or r"(?!)"
_NON_LATIN_HAND_NUMBERED = re.compile(r"(?<!@)(?P<label>" + _NUMBERED_LABEL_PATTERN + r")\s*[0-9０-９]+")
_EN_DOUBLED = re.compile(
    r"(?i)\b(?:sections?|sect\.|figures?|figs?\.|tables?|tabs?\.|equations?|eqs?\.|eqns?)\s+\[?-?@(?:sec|fig|tbl|eq):"
)
_NON_LATIN_DOUBLED = re.compile(r"(?P<label>" + _NUMBERED_LABEL_PATTERN + r")\s+\[?-?@(?:sec|fig|tbl|eq):")

_EN_OPEN = re.compile(r"\b(?:TODO|TBD|FIXME|XXX)\b|(?i:citation needed)")
_MARKER_PATTERN = "|".join(map(re.escape, _OPEN_MARKERS))
_BRACKETED_OPEN = re.compile(r"[\[\(\uFF08\u3010\u300C].*?(?:" + (_MARKER_PATTERN or r"(?!)") + r").*?[\]\)\uFF09\u3011\u300D]")

AI_NAME = r"(?:ChatGPT|OpenAI|Codex|Claude|Anthropic|Gemini|Copilot|AI assistant" + ("|" + "|".join(map(re.escape, _AI_NAMES)) if _AI_NAMES else "") + r")"
AI_AUTHOR = re.compile(rf"(?<![A-Za-z0-9_]){AI_NAME}(?![A-Za-z0-9_])", re.I)
_AI_SUFFIX_PATTERN = "|".join(map(re.escape, _AI_SUFFIXES))
_AI_SUFFIX_PATTERN = _AI_SUFFIX_PATTERN or r"(?!)"
_AI_ROLE_PATTERN = "|".join(map(re.escape, _AI_ROLES)) or r"(?!)"
_AI_PREFIX_PATTERN = "|".join(map(re.escape, _AI_PREFIXES)) or r"(?!)"
AI_SIGNATURE = re.compile(
    rf"^\s*(?:[-—–*#>]+\s*)?(?:(?:written|generated|authored|signed|prepared)\s+by\s+{AI_NAME}\b"
    rf"|(?:{_AI_ROLE_PATTERN})\s*[:\uFF1A]\s*{AI_NAME}"
    rf"|(?:{_AI_PREFIX_PATTERN})\s*{AI_NAME}(?:{_AI_SUFFIX_PATTERN})"
    rf"|{AI_NAME}(?:{_AI_SUFFIX_PATTERN})"
    rf"|{AI_NAME}\s*[.\u3002\uFF01]?\s*$)",
    re.I,
)


def detection_text(text: str) -> str:
    """Normalize width variants for checks while preserving source text."""
    return unicodedata.normalize("NFKC", text)


def citation_keys(text: str) -> list[str]:
    """Extract citation/reference keys while allowing adjacent CJK/Japanese text."""
    found = []
    for start in _CITATION_START.finditer(text):
        tail = _CITATION_TAIL.match(text, start.end())
        if not tail:
            continue
        value = _strip_reference_punctuation(tail.group(0).lstrip("-"))
        if value:
            found.append(value)
    return found


def _strip_reference_punctuation(value: str) -> str:
    while value and (value[-1] in string.punctuation or unicodedata.category(value[-1]).startswith("P")):
        value = value[:-1]
    return value


def _unicode_suffix(value: str) -> bool:
    return bool(value) and all(ch.isspace() or _CJK_OR_JAPANESE.fullmatch(ch) or unicodedata.category(ch).startswith("P") for ch in value)


def normalize_reference(value: str, known: set[str]) -> str:
    """Trim punctuation and a trailing CJK/Japanese phrase from a known key.

    Latin suffixes are never discarded, so an unknown misspelling remains an
    unknown key and is reported by the manuscript check.
    """
    value = _strip_reference_punctuation(value.lstrip("-"))
    if value in known:
        return value
    for candidate in sorted(known, key=len, reverse=True):
        if value.startswith(candidate) and _unicode_suffix(value[len(candidate):]):
            return candidate
    return value


def hand_numbered(text: str) -> list[str]:
    normalized = detection_text(text)
    return [match.group(0) for match in list(_EN_HAND_NUMBERED.finditer(normalized)) + list(_NON_LATIN_HAND_NUMBERED.finditer(normalized))]


def doubled_reference(text: str) -> list[str]:
    normalized = detection_text(text)
    return [match.group(0) for match in list(_EN_DOUBLED.finditer(normalized)) + list(_NON_LATIN_DOUBLED.finditer(normalized))]


def open_marker(text: str) -> bool:
    """Find an explicit open marker without treating ordinary CJK prose as a TODO."""
    if _EN_OPEN.search(text):
        return True
    normalized = detection_text(text)
    stripped = normalized.strip()
    if _BRACKETED_OPEN.search(normalized):
        return True
    terms = _OPEN_MARKERS
    return bool(re.match(r"^(?:" + "|".join(map(re.escape, terms)) + r")(?:\s*[:\uFF1A].*)?$", stripped))


def signature_problems(text: str, display: str, *, metadata: bool = False) -> list[str]:
    """Flag explicit AI sign-offs and AI author entries with source locations."""
    problems, in_authors = [], False
    for number, line in enumerate(text.splitlines(), 1):
        author_field = re.match(r"^authors?\s*:\s*(.*)$", line, re.I) if metadata else None
        if author_field:
            in_authors = True
        elif metadata and line and not line[0].isspace() and not line.startswith("-"):
            in_authors = False
        if AI_SIGNATURE.search(line) or (in_authors and AI_AUTHOR.search(line)):
            problems.append(f"{display}:{number}: possible AI signature or AI author; inspect and remove unintended attribution")
    return problems


# LaTeX commands in Markdown prose. Pandoc reads them as raw LaTeX and drops them from a Word file,
# so a citation, a reference, or emphasized words would disappear without an error. Escapes such as
# \% or \_ are not commands and stay valid Markdown; an escaped backslash (\\) starts no command.
_LATEX_COMMAND = re.compile(r"(?<!\\)\\([A-Za-z]+)\*?(?:\[[^\]\n]*\])*(?:\{[^{}\n]*\})*")
_LATEX_ADVICE = (
    (("cite", "citep", "citet", "citealp", "citealt", "citeauthor", "citeyear", "parencite", "textcite", "autocite",
      "footcite", "nocite"), "write [@key], or @key inside the sentence"),
    (("ref", "eqref", "autoref", "cref", "Cref", "pageref", "nameref"), "write @fig:id, @tbl:id, @eq:id, or @sec:id"),
    (("label",), "write {#fig:id}, {#tbl:id}, {#eq:id}, or {#sec:id} where the conventions place a label"),
    (("textbf", "textit", "emph", "underline", "texttt", "textsc", "textsf", "textrm", "textup"),
     "write the words plainly, or with Markdown emphasis"),
    (("part", "chapter", "section", "subsection", "subsubsection", "paragraph"), "write a Markdown heading"),
    (("begin", "end", "item"), "write a Markdown list, table, or block"),
    (("footnote",), "write a Markdown footnote, [^id], with its note"),
    (("url", "href"), "write <address> or [text](address)"),
    (("includegraphics",), "write ![Caption](assets/file){#fig:id}"),
    (("newpage", "clearpage", "pagebreak", "vspace", "hspace", "noindent"), "leave page layout to the output profile"),
)

# Half-width punctuation after Chinese or Japanese text. Korean, which uses half-width marks, is excluded.
_FULLWIDTH_MARKS = _RULES.get("fullwidth_punctuation", {})
_HAN_OR_KANA = "\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
_KANA = re.compile(r"[\u3040-\u30ff]")
_HALFWIDTH_MARK = re.compile(r"(?<=[" + _HAN_OR_KANA + r"])[,.;:!?](?=\s*[" + _HAN_OR_KANA + r"]|\s*$)")


def raw_latex(text: str) -> list[tuple[str, str]]:
    """Find LaTeX commands in prose whose math and code are removed, each with the Markdown form to use instead."""
    found = []
    for match in _LATEX_COMMAND.finditer(text):
        advice = next((advice for names, advice in _LATEX_ADVICE if match.group(1) in names),
                      "write it in the workspace's Markdown form, or put a path or code in backticks")
        found.append((match.group(0).strip(), advice))
    return found


def halfwidth_punctuation(text: str) -> list[tuple[str, str]]:
    """Find half-width punctuation after Chinese or Japanese text, with the usual full-width form for that language.

    Citation keys and cross-references are masked first: an identifier such as @sec:<Chinese heading> is not
    Chinese text, so the period of an English sentence after it is not reported.
    """
    for key in sorted(set(citation_keys(text)), key=len, reverse=True):
        text = text.replace("@" + key, "@key")
    marks = _FULLWIDTH_MARKS.get("ja" if _KANA.search(text) else "zh", {})
    return [(match.group(0), marks.get(match.group(0), "")) for match in _HALFWIDTH_MARK.finditer(text)]
