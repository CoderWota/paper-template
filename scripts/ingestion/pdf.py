"""Small, best-effort PDF inspection with the standard library: page count and comment annotations.

This is not a PDF parser. It reads the raw file and the decompressed object streams, so it can
miss structures that a full parser would find. Callers report its results as approximate.
"""

from __future__ import annotations

import re
import zlib
from pathlib import Path

MAX_STREAM = 8 << 20
# Annotation types that carry a reviewer's comment or mark. Links, widgets, and pop-ups are not comments.
COMMENT_SUBTYPES = (
    "Text", "FreeText", "Highlight", "Underline", "StrikeOut", "Squiggly", "Caret", "Ink",
    "Stamp", "Square", "Circle", "Line", "Polygon", "PolyLine", "FileAttachment", "Sound",
)
SUBTYPE = re.compile(rb"/Subtype\s*/(" + b"|".join(s.encode() for s in COMMENT_SUBTYPES) + rb")(?![A-Za-z])")
ESCAPES = {ord("n"): 10, ord("r"): 13, ord("t"): 9, ord("b"): 8, ord("f"): 12}


def bodies(data: bytes) -> list[bytes]:
    """The raw file plus every decompressed object stream, where page and annotation objects can hide."""
    result = [data]
    for match in re.finditer(rb"stream\r?\n", data):
        if b"/ObjStm" not in data[max(0, match.start() - 600):match.start()]:
            continue
        start = match.end()
        end = data.find(b"endstream", start)
        if end < 0 or end - start > MAX_STREAM:
            continue
        try:
            result.append(zlib.decompressobj().decompress(data[start:end]))
        except zlib.error:
            continue
    return result


def enclosing_dict(body: bytes, position: int) -> bytes:
    """The innermost << ... >> dictionary that contains position, or b"" when there is none."""
    depth, index, start = 0, position, -1
    while index > 0:
        pair = body[index - 1:index + 1]
        if pair == b">>":
            depth += 1
            index -= 2
        elif pair == b"<<":
            if depth == 0:
                start = index - 1
                break
            depth -= 1
            index -= 2
        else:
            index -= 1
    if start < 0:
        return b""
    depth, index = 0, start
    while index < len(body) - 1:
        pair = body[index:index + 2]
        if pair == b"<<":
            depth += 1
            index += 2
        elif pair == b">>":
            depth -= 1
            index += 2
            if depth == 0:
                return body[start:index]
        else:
            index += 1
    return b""


def page_count(path: Path) -> int | None:
    """The page count from the page tree, or None when it cannot be read."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if not data.lstrip().startswith(b"%PDF"):
        return None
    counts, leaves = [], 0
    for body in bodies(data):
        for match in re.finditer(rb"/Type\s*/Pages(?![A-Za-z])", body):
            found = re.search(rb"/Count\s+(\d+)", enclosing_dict(body, match.start()))
            if found:
                counts.append(int(found.group(1)))
        leaves += len(re.findall(rb"/Type\s*/Page(?![A-Za-z])", body))
    if counts:
        return max(counts)
    return leaves or None


def literal(body: bytes, start: int) -> bytes:
    """The bytes of the literal string that opens at body[start] == "(", decoded from PDF escapes."""
    value, depth, index = bytearray(), 0, start
    while index < len(body):
        byte = body[index]
        if byte == 0x5C and index + 1 < len(body):  # backslash
            following = body[index + 1]
            if following in ESCAPES:
                value.append(ESCAPES[following])
                index += 2
            elif 0x30 <= following <= 0x37:
                octal = re.match(rb"[0-7]{1,3}", body[index + 1:index + 4]).group(0)
                value.append(int(octal, 8) & 0xFF)
                index += 1 + len(octal)
            elif following in (0x0A, 0x0D):
                index += 2
            else:
                value.append(following)
                index += 2
            continue
        if byte == 0x28:  # (
            depth += 1
            if depth > 1:
                value.append(byte)
        elif byte == 0x29:  # )
            depth -= 1
            if depth == 0:
                return bytes(value)
            value.append(byte)
        else:
            value.append(byte)
        index += 1
    return bytes(value)


def text_of(raw: bytes) -> str:
    if raw.startswith(b"\xfe\xff"):
        return raw[2:].decode("utf-16-be", errors="replace")
    if raw.startswith(b"\xff\xfe"):
        return raw[2:].decode("utf-16-le", errors="replace")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1")


def string_value(dictionary: bytes, key: bytes) -> str | None:
    match = re.search(rb"/" + key + rb"(?![A-Za-z])\s*([(<])", dictionary)
    if not match:
        return None
    if match.group(1) == b"(":
        return text_of(literal(dictionary, match.start(1)))
    end = dictionary.find(b">", match.start(1))
    digits = re.sub(rb"[^0-9A-Fa-f]", b"", dictionary[match.start(1) + 1:end])
    if len(digits) % 2:
        digits += b"0"
    return text_of(bytes.fromhex(digits.decode("ascii")))


def annotations(path: Path) -> list[dict]:
    """Comment-type annotations found by a simple scan, with their text and author when readable."""
    try:
        data = path.read_bytes()
    except OSError:
        return []
    found, seen = [], set()
    for body in bodies(data):
        for match in SUBTYPE.finditer(body):
            dictionary = enclosing_dict(body, match.start())
            # Every annotation has a /Rect; other dictionaries with these subtypes do not.
            if not dictionary or dictionary in seen or b"/Rect" not in dictionary:
                continue
            seen.add(dictionary)
            found.append({
                "type": match.group(1).decode(),
                "text": string_value(dictionary, b"Contents"),
                "author": string_value(dictionary, b"T"),
            })
    return found
