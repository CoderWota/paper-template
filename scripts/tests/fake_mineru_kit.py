#!/usr/bin/env python3
"""A stand-in for mineru-kit, used by the ingestion tests. It needs no models and writes MinerU 4 shaped archives.

FAKE_MINERU_BEHAVIOUR holds JSON that maps an input file name to its behaviour: "fail", "models_missing",
"processed" (pages converted), "blank" (pages without text), "lost_header", and "unlinked_image".
FAKE_MINERU_LOG names a file that receives one JSON line per call.
"""

from __future__ import annotations

import json
import os
import re
import sys
import zipfile
from pathlib import Path


def text_block(index: int, kind: str, text: str) -> dict:
    return {"type": kind, "index": index, "content": [{"type": "text", "content": text}]}


def main(argv: list) -> int:
    if os.environ.get("FAKE_MINERU_LOG"):
        with open(os.environ["FAKE_MINERU_LOG"], "a", encoding="utf-8") as log:
            log.write(json.dumps({"argv": argv, "model_source": os.environ.get("MINERU_MODEL_SOURCE"),
                                  "home": os.environ.get("MINERU_HOME")}) + "\n")
    if argv[:1] == ["version"]:
        print(json.dumps({"mineru_version": "4.0.12", "python_version": "3.12.9"}))
        return 0
    if argv[:1] != ["parse"]:
        return 2
    source, out = Path(argv[1]), Path(argv[argv.index("-o") + 1])
    behaviour = json.loads(os.environ.get("FAKE_MINERU_BEHAVIOUR", "{}")).get(source.name, {})
    if behaviour.get("fail"):
        print(f"错误: 解析 {source} 失败: Failed to load document (PDFium: Data format error).", file=sys.stderr)
        return 1
    if behaviour.get("models_missing"):
        print(f"错误: 解析 {source} 失败: Model repo MinerU-4_models_torch is not ready under /models; missing: x", file=sys.stderr)
        return 1
    tier = argv[argv.index("--tier") + 1]
    images, markdown, pages = {}, [], []
    if source.suffix.lower() == ".docx":
        with zipfile.ZipFile(source) as package:
            document = package.read("word/document.xml").decode("utf-8")
        paragraphs = [" ".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p)) for p in re.findall(r"<w:p>(.*?)</w:p>", document)]
        markdown = [p for p in paragraphs if p.strip()]
        pages = [{"page_idx": 0, "blocks": [text_block(i, "text", p) for i, p in enumerate(markdown)]}]
        total, document_meta = 1, {"title": "untitled", "authors": ["anonymous"]}
    else:
        total = len(re.findall(rb"/Type\s*/Page(?![A-Za-z])", source.read_bytes())) or 1
        document_meta = {"title": "untitled", "authors": ["anonymous"], "page_count": total, "page_count_kind": "physical"}
        for index in range(behaviour.get("processed", total)):
            blocks = [text_block(0, "header", "Synthetic Journal of Workspace Tests"), text_block(1, "page_number", f"Page {index + 1}")]
            if index + 1 not in behaviour.get("blank", []):
                text = f"Text of page {index + 1} of {source.stem}, written only for a test of the import."
                blocks.append(text_block(2, "text", text))
                markdown.append(text)
            if index == 0:
                images["images/page_0_image_3.jpg"] = b"\xff\xd8\xff synthetic image"
                blocks.append({"type": "image", "index": 3, "content": [{"type": "image_body", "image_path": "images/page_0_image_3.jpg", "content": ""}]})
                markdown.append("![](images/page_0_image_3.jpg)")
                if behaviour.get("lost_header"):
                    blocks.append(text_block(4, "header", "A unique sentence that the parser classified as a page header by mistake."))
                if behaviour.get("unlinked_image"):
                    images["images/page_0_image_5.jpg"] = b"\xff\xd8\xff another image"
                    blocks.append({"type": "image", "index": 5, "content": [{"type": "image_body", "image_path": "images/page_0_image_5.jpg", "content": ""}]})
                if behaviour.get("math"):
                    markdown.append("Inline \\(a+b\\) and a display formula:\n\n$$x^2 + y^2$$")
            pages.append({"page_idx": index, "blocks": blocks})
    middle = {"metadata": {"file_suffix": source.suffix.lstrip("."), "producer": {"name": "mineru", "version": "4.0.12"}, "document": document_meta},
              "extensions": {"mineru": {"tier": tier}}, "pages": pages, "is_full_document": len(pages) == total,
              "schema": "docvortex.middle", "schema_version": "2.0"}
    out.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out / f"{source.stem}.zip", "w") as archive:
        archive.writestr("markdown.md", "\n\n".join(markdown) + "\n")
        archive.writestr("middle_json.json", json.dumps(middle))
        archive.writestr("structured_content.json", "{}")
        for name, data in images.items():
            archive.writestr(name, data)
    print("已解析 1 个输入。")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
