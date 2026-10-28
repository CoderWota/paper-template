"""Formal review documents: venue and round folders, Word comments and tracked changes, and PDF annotations.

MinerU converts the main text of a review document. It does not convert Word comments, and it shows
tracked changes as if they had been accepted, so those structures are read here from the original
file's XML. PDF annotations are found with a simple scan of the file.
"""

from __future__ import annotations

import os
import re
import shutil
import uuid
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from . import pdf
from .common import read_json, safe_filename, sha256_file, slug, update_readme, write_json_atomic

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
W14 = "{http://schemas.microsoft.com/office/word/2010/wordml}"
W15 = "{http://schemas.microsoft.com/office/word/2012/wordml}"
DESTINATION = re.compile(r"^reviews/([a-z0-9][a-z0-9-]{0,59})/([a-z0-9][a-z0-9-]{0,59})$")
SCHEMA = "paper-template.review-extraction/1"


def parse_destination(value: str) -> tuple:
    match = DESTINATION.match(value.strip().strip("/"))
    if not match:
        raise ValueError("a review destination looks like reviews/<venue-id>/<round-id>, in lowercase letters, digits, and hyphens")
    return match.group(1), match.group(2)


class Round:
    def __init__(self, root: Path, venue: str, round_id: str):
        self.root, self.venue, self.round = root, venue, round_id
        self.folder = root / "reviews" / venue / round_id
        self.originals = self.folder / "originals"
        self.markdown = self.folder / "extracted" / "markdown"
        self.assets = self.folder / "extracted" / "assets"
        self.record_path = self.folder / "extracted" / "provenance.json"

    def ensure(self) -> None:
        for folder in (self.originals, self.markdown, self.assets):
            folder.mkdir(parents=True, exist_ok=True)
        name = f"`{self.venue}`, round `{self.round}`"
        update_readme(self.root / "reviews" / self.venue / "README.md", f"Venue: {self.venue}", (
            f"Editorial and review correspondence from the venue `{self.venue}`, one folder per submission or revision round. "
            "Each round keeps its received originals, the readable extraction, and later the response and the change map, "
            "so that numbering and manuscript versions of different rounds never mix."
        ))
        self.update_round_readme()
        update_readme(self.originals / "README.md", f"Originals: {self.venue} {self.round}", (
            f"Decision letters and reviewer files of {name}, exactly as received. They are never edited or replaced; "
            "readable copies are in [`../extracted/markdown/`](../extracted/markdown/README.md)."
        ))
        update_readme(self.folder / "extracted" / "README.md", f"Extraction: {self.venue} {self.round}", (
            f"Readable versions of the review documents of {name}: Markdown in [`markdown/`](markdown/README.md), images in "
            "[`assets/`](assets/README.md), and the checksum, converter, settings, coverage, and gaps of each document in "
            "[`provenance.json`](provenance.json). Extraction can contain errors; the originals are authoritative."
        ))
        update_readme(self.markdown / "README.md", f"Review Markdown: {self.venue} {self.round}", (
            f"One Markdown file per review document of {name}. Reviewer labels, item numbers, and page or line references are "
            "kept as the parser found them. Word comments, tracked changes, and PDF annotations are listed in a separate section "
            "at the end of each file, because the main conversion does not capture them."
        ))
        update_readme(self.assets / "README.md", f"Review images: {self.venue} {self.round}", (
            f"Images and table pictures extracted from the review documents of {name}. Each file name starts with the "
            "identifier of its document and two hyphens, and the Markdown files link to them."
        ))

    def record(self) -> dict:
        data = read_json(self.record_path)
        if not isinstance(data, dict) or data.get("schema") != SCHEMA:
            data = {"schema": SCHEMA, "venue": self.venue, "round": self.round, "documents": {}}
        return data

    def update_round_readme(self) -> None:
        documents = self.record().get("documents", {}) if self.record_path.is_file() else {}
        lines = [f"Submission or revision round `{self.round}` at the venue `{self.venue}`. Received documents are in "
                 "[`originals/`](originals/README.md) and their readable versions in [`extracted/`](extracted/README.md). "
                 "A point-by-point response and the change map are added here only when the researcher asks for them."]
        if documents:
            lines += ["", "| Document | Extraction | Comments, changes, annotations |", "| --- | --- | --- |"]
            names = {"comments": "comment(s)", "insertions": "insertion(s)", "deletions": "deletion(s)", "pdf_annotations": "PDF annotation(s)"}
            for document_id, entry in sorted(documents.items()):
                structures = entry.get("structures") or {}
                found = ", ".join(f"{value} {names.get(name, name)}" for name, value in structures.items() if isinstance(value, int)) or "none found"
                status = {"needs-review": "needs review"}.get(entry.get("status"), entry.get("status"))
                lines.append(f"| [{entry.get('original_name', document_id)}](extracted/markdown/{document_id}.md) | {status} | {found} |")
        update_readme(self.folder / "README.md", f"Round: {self.venue} {self.round}", "\n".join(lines))

    def archive(self, path: Path, sha: str) -> tuple:
        """Copy the file into originals/ unless the same content is already there. Returns (document id, file, new)."""
        record = self.record()
        for document_id, entry in record["documents"].items():
            if entry.get("sha256") == sha and (self.originals / entry.get("original_name", "")).is_file():
                return document_id, self.originals / entry["original_name"], False
        for existing in self.originals.iterdir():
            if existing.is_file() and existing.name != "README.md" and sha256_file(existing) == sha:
                return self.document_id(existing.name, record), existing, False
        name = safe_filename(path.name)
        stem, suffix, number = Path(name).stem, Path(name).suffix, 2
        while (self.originals / name).exists():
            name, number = f"{stem} ({number}){suffix}", number + 1
        temporary = self.originals / f".copying-{uuid.uuid4().hex}"
        shutil.copy2(path, temporary)
        if sha256_file(temporary) != sha:
            temporary.unlink()
            raise OSError(f"the copy of {path.name} does not match the original")
        os.replace(temporary, self.originals / name)
        return self.document_id(name, record), self.originals / name, True

    @staticmethod
    def document_id(name: str, record: dict) -> str:
        for document_id, entry in record["documents"].items():
            if entry.get("original_name") == name:
                return document_id
        base = slug(Path(name).stem, limit=50, fallback="document")
        document_id, number = base, 2
        while document_id in record["documents"]:
            document_id, number = f"{base}-{number}", number + 1
        return document_id


def text_of(element) -> str:
    return "".join(node.text or "" for node in element.iter(W + "t"))


def docx_structures(path: Path) -> dict:
    """Comments with their anchored text and replies, insertions, and deletions, in document order."""
    try:
        package = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        return {"error": "the file is not a readable Word package"}
    with package:
        names = set(package.namelist())
        comments, parents = {}, {}
        if "word/comments.xml" in names:
            for comment in ET.fromstring(package.read("word/comments.xml")).iter(W + "comment"):
                paragraphs = [text_of(p) for p in comment.iter(W + "p")]
                ids = [p.get(W14 + "paraId") for p in comment.iter(W + "p") if p.get(W14 + "paraId")]
                comments[comment.get(W + "id")] = {"author": comment.get(W + "author") or "", "date": (comment.get(W + "date") or "")[:10],
                                                   "text": "\n".join(p for p in paragraphs if p), "para_id": ids[-1] if ids else None}
        if "word/commentsExtended.xml" in names:
            for entry in ET.fromstring(package.read("word/commentsExtended.xml")).iter(W15 + "commentEx"):
                if entry.get(W15 + "paraIdParent"):
                    parents[entry.get(W15 + "paraId")] = entry.get(W15 + "paraIdParent")
        if "word/document.xml" not in names:
            return {"error": "the Word package has no main document"}
        state = {"paragraph": 0, "open": {}, "anchors": {}, "order": [], "insertions": [], "deletions": []}
        walk(ET.fromstring(package.read("word/document.xml")), state)
    by_para = {entry["para_id"]: comment_id for comment_id, entry in comments.items() if entry["para_id"]}
    ordered = [cid for cid in state["order"] if cid in comments] + [cid for cid in comments if cid not in state["order"]]
    numbers = {cid: number for number, cid in enumerate(ordered, start=1)}
    listed = []
    for cid in ordered:
        entry = comments[cid]
        parent = by_para.get(parents.get(entry["para_id"])) if entry["para_id"] else None
        listed.append({"number": numbers[cid], "author": entry["author"], "date": entry["date"], "text": entry["text"],
                       "anchor": state["anchors"].get(cid, ""), "reply_to": numbers.get(parent)})
    return {"comments": listed, "insertions": state["insertions"], "deletions": state["deletions"]}


def walk(element, state: dict) -> None:
    tag = element.tag
    if tag == W + "p":
        state["paragraph"] += 1
    elif tag == W + "commentRangeStart":
        cid = element.get(W + "id")
        state["open"][cid] = []
        if cid not in state["order"]:
            state["order"].append(cid)
    elif tag == W + "commentRangeEnd":
        cid = element.get(W + "id")
        state["anchors"][cid] = "".join(state["open"].pop(cid, []))
    elif tag == W + "commentReference":
        cid = element.get(W + "id")
        if cid not in state["order"]:
            state["order"].append(cid)
    elif tag == W + "t":
        for buffer in state["open"].values():
            buffer.append(element.text or "")
    elif tag in (W + "ins", W + "del"):
        text = "".join(node.text or "" for node in element.iter(W + ("t" if tag == W + "ins" else "delText")))
        if text:
            key = "insertions" if tag == W + "ins" else "deletions"
            state[key].append({"author": element.get(W + "author") or "", "date": (element.get(W + "date") or "")[:10],
                               "paragraph": state["paragraph"], "text": text})
    for child in element:
        walk(child, state)


def structures_markdown(kind: str, structures: dict, annotations: list | None) -> str:
    """A section listing what the main conversion does not show. Quoted text keeps its original language."""
    lines = []
    if kind == "word":
        comments, inserted, deleted = structures.get("comments", []), structures.get("insertions", []), structures.get("deletions", [])
        lines += ["", "---", "", "## Comments and tracked changes in the Word file", "",
                  f"Read by the workspace from the original file: {len(comments)} comment(s), {len(inserted)} insertion(s), and "
                  f"{len(deleted)} deletion(s). The text above shows the document as if every tracked change had been accepted: "
                  "inserted text appears without a mark and deleted text is missing."]
        if structures.get("error"):
            lines += ["", f"The comments could not be read: {structures['error']}. Check the original file."]
        for comment in comments:
            who = ", ".join(filter(None, [comment["author"], comment["date"]]))
            title = f"Comment {comment['number']}" + (f" ({who})" if who else "") + (f", a reply to comment {comment['reply_to']}" if comment.get("reply_to") else "")
            lines += ["", f"### {title}", ""]
            if comment["anchor"]:
                lines += [f"On the text: “{comment['anchor']}”", ""]
            lines += ["> " + line for line in (comment["text"] or "(empty comment)").split("\n")]
        if inserted or deleted:
            lines += ["", "### Tracked changes", ""]
            changes = [("Inserted", change) for change in inserted] + [("Deleted", change) for change in deleted]
            for number, (action, change) in enumerate(sorted(changes, key=lambda c: c[1]["paragraph"]), start=1):
                who = ", ".join(filter(None, [change["author"], change["date"]]))
                lines.append(f"{number}. {action}" + (f" by {who}" if who else "") + f", paragraph {change['paragraph']}: “{change['text']}”")
    if annotations is not None:
        lines += ["", "---", "", "## Annotations in the PDF file", "",
                  f"A simple scan of the original file found {len(annotations)} comment annotation(s). The scan can miss annotations "
                  "and does not determine their pages, so check the original file before relying on this list.", ""]
        for number, note in enumerate(annotations, start=1):
            author = f" by {note['author']}" if note.get("author") else ""
            text = note.get("text")
            lines.append(f"{number}. {note['type']} annotation{author}: " + (f"“{text}”" if text else "(no readable text)"))
    return "\n".join(lines) + ("\n" if lines else "")


def inspect(original: Path, kind: str) -> tuple:
    """(structures summary, Markdown section, warnings) for the structures the parser does not convert."""
    if kind == "word":
        found = docx_structures(original)
        summary = {"comments": len(found.get("comments", [])), "insertions": len(found.get("insertions", [])),
                   "deletions": len(found.get("deletions", []))}
        warnings = []
        if found.get("error"):
            warnings.append({"code": "structures-unreadable", "level": "review", "message": f"Word comments could not be read: {found['error']}"})
        elif summary["insertions"] or summary["deletions"]:
            warnings.append({"code": "tracked-changes", "level": "review",
                             "message": "the document has tracked changes; the main text shows them as accepted, and they are listed separately"})
        return summary, structures_markdown(kind, found, None), warnings
    if kind == "pdf":
        notes = pdf.annotations(original)
        warnings = [{"code": "pdf-annotations", "level": "review",
                     "message": f"{len(notes)} PDF annotation(s) found by a simple scan; check the original for their pages and for any the scan missed"}] if notes else []
        return {"pdf_annotations": len(notes)}, structures_markdown(kind, {}, notes) if notes else "", warnings
    return {}, "", []


def store(round_: Round, document_id: str, entry: dict) -> None:
    record = round_.record()
    record["documents"][document_id] = entry
    write_json_atomic(round_.record_path, record)
    round_.update_round_readme()


def edited(round_: Round, document_id: str) -> bool:
    entry = round_.record()["documents"].get(document_id) or {}
    path = round_.markdown / f"{document_id}.md"
    expected = entry.get("markdown_sha256")
    return bool(expected and path.is_file() and sha256_file(path) != expected)


def publish(round_: Round, document_id: str, stage: Path) -> None:
    """Move the staged Markdown and images into the round, replacing this document's earlier files.

    Image names start with "<document id>--"; identifiers never contain two hyphens in a row, so one
    document's images are never mistaken for another's.
    """
    for old in round_.assets.glob(f"{document_id}--*"):
        old.unlink()
    for image in sorted((stage / "assets").glob("*")) if (stage / "assets").is_dir() else []:
        os.replace(image, round_.assets / image.name)
    os.replace(stage / "markdown" / f"{document_id}.md", round_.markdown / f"{document_id}.md")
