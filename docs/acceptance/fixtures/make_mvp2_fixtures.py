#!/usr/bin/env python3
"""Build the synthetic, rights-cleared fixture folder for the MVP 2 acceptance checks.

Every document is generated here and says that it is a synthetic test document. The folder
covers the cases that the MVP 2 acceptance evidence names: duplicate names and content,
non-ASCII and spaced paths, images, a scanned page, two columns, a table, equations, a
document longer than ten pages, a Word review with comments and tracked changes, a PDF with
reviewer annotations, a Markdown file, a corrupt PDF, and an unsupported format.

Usage: python make_mvp2_fixtures.py OUTPUT_FOLDER
Needs reportlab and Pillow, for example the interpreter of the local MinerU tool environment
(.tools/mineru/bin/python). The Word file is written with the standard library only.
"""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

LABEL = "Synthetic test document for workspace checks. It contains no research results."


def font(size: int):
    for name in ("Arial.ttf", "Helvetica.ttc", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def diagram(path: Path) -> Path:
    image = Image.new("RGB", (480, 260), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle([30, 30, 450, 230], outline="black", width=3)
    draw.line([30, 230, 450, 30], fill="navy", width=5)
    draw.ellipse([200, 100, 280, 180], outline="darkred", width=4)
    draw.text((40, 40), "Synthetic figure", fill="black", font=font(22))
    image.save(path)
    return path


def text_image(path: Path, lines: list[str], size=(1240, 1754)) -> Path:
    """An image of printed text, used as a scanned page without a text layer."""
    image = Image.new("L", size, 255)
    draw = ImageDraw.Draw(image)
    y = 140
    for line in lines:
        draw.text((120, y), line, fill=0, font=font(34))
        y += 58
    image.save(path)
    return path


def header_footer(c: canvas.Canvas, page: int, total: int) -> None:
    width, height = A4
    c.setFont("Helvetica", 8)
    c.drawString(72, height - 40, "Synthetic Journal of Workspace Tests - running header")
    c.drawRightString(width - 72, 30, f"Page {page} of {total}")


def paragraph(c: canvas.Canvas, x: float, y: float, words: str, width_chars: int = 88, leading: float = 14) -> float:
    line = ""
    for word in words.split():
        if len(line) + len(word) + 1 > width_chars:
            c.drawString(x, y, line)
            y -= leading
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y - 6


def long_report(path: Path, work: Path) -> None:
    total = 12
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle("Synthetic Long Report for Import Tests")
    c.setAuthor("Workspace Test Generator")
    width, height = A4
    figure = diagram(work / "figure.png")
    formula = text_image(work / "formula.png", ["x = ( -b + sqrt(b^2 - 4ac) ) / 2a"], size=(1100, 120))
    for page in range(1, total + 1):
        header_footer(c, page, total)
        c.setFont("Helvetica", 10)
        y = height - 80
        if page == 1:
            c.setFont("Helvetica-Bold", 18)
            c.drawString(72, y, "Synthetic Long Report for Import Tests")
            c.setFont("Helvetica", 11)
            c.drawString(72, y - 22, "A. Tester and B. Example")
            c.drawString(72, y - 38, "doi:10.5555/synthetic.0001")
            c.setFont("Helvetica", 10)
            y = paragraph(c, 72, y - 64, LABEL)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(72, y - 4, f"{page}. Section {page}")
        c.setFont("Helvetica", 10)
        y = paragraph(c, 72, y - 24, f"This is page {page}. " + "The sentences on this page exist only to test document conversion and page coverage. " * 5)
        if page == 2:
            c.drawImage(ImageReader(str(figure)), 72, y - 200, width=300, height=162)
            c.drawString(72, y - 214, "Figure 1. A synthetic diagram with a line and a circle.")
        if page == 3:
            c.drawString(72, y - 6, "Table 1. Synthetic measurements.")
            rows = [["Sample", "Value", "Unit"], ["A", "1.25", "mm"], ["B", "2.50", "mm"], ["C", "3.75", "mm"]]
            ty = y - 30
            for row in rows:
                x = 72
                for cell in row:
                    c.rect(x, ty - 5, 110, 18)
                    c.drawString(x + 5, ty, cell)
                    x += 110
                ty -= 18
        if page == 4:
            c.drawString(72, y - 6, "Equation (1) is printed as text, and equation (2) as an image:")
            c.setFont("Times-Italic", 12)
            c.drawString(110, y - 30, "E = m c^2        (1)")
            c.setFont("Helvetica", 10)
            c.drawImage(ImageReader(str(formula)), 100, y - 90, width=330, height=36)
            c.drawString(450, y - 78, "(2)")
        if page == 5:
            left = "Left column text. " * 40
            right = "Right column text. " * 40
            paragraph(c, 72, y - 10, left, width_chars=40)
            paragraph(c, 320, y - 10, right, width_chars=40)
        c.showPage()
    c.save()


def scanned(path: Path, work: Path) -> None:
    lines = ["Scanned page of a synthetic test document.", "This page is an image without a text layer.", "Optical character recognition should read it."]
    scan = text_image(work / "scan.png", lines)
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    c.drawImage(ImageReader(str(scan)), 0, 0, width=width, height=height)
    c.showPage()
    c.setFont("Helvetica", 11)
    c.drawString(72, height - 90, "Page 2 has a normal text layer. " + LABEL[:40])
    c.showPage()
    c.save()


def annotated_review(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, height - 80, "Synthetic reviewer report (annotated PDF)")
    c.setFont("Helvetica", 11)
    c.drawString(72, height - 110, "Reviewer 2")
    c.drawString(72, height - 130, "Comment 1. The synthetic method section needs one more sentence.")
    c.drawString(72, height - 150, "Comment 2. Figure 1 of the synthetic manuscript lacks a scale.")
    c.textAnnotation("Annotation: please clarify the sampling interval.", Rect=(72, height - 135, 300, height - 120), relative=0)
    c.textAnnotation("Annotation: the scale bar is missing.", Rect=(72, height - 155, 300, height - 140), relative=0)
    c.showPage()
    c.save()


W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'


def run(text: str) -> str:
    return f'<w:r><w:t xml:space="preserve">{text}</w:t></w:r>'


def word_review(path: Path) -> None:
    """A Word reviewer letter with two comments and one insertion and one deletion."""
    body = (
        f"<w:p><w:r><w:t>Synthetic decision letter and reviewer comments</w:t></w:r></w:p>"
        f"<w:p>{run(LABEL)}</w:p>"
        f"<w:p>{run('Reviewer 1')}</w:p>"
        f'<w:p>{run("1. The introduction ")}<w:commentRangeStart w:id="0"/>{run("overstates the synthetic contribution")}'
        f'<w:commentRangeEnd w:id="0"/><w:r><w:commentReference w:id="0"/></w:r>{run(".")}</w:p>'
        f'<w:p>{run("2. Please report the sample size ")}<w:ins w:id="10" w:author="Reviewer 1" w:date="2026-09-01T10:00:00Z">{run("for each group")}</w:ins>'
        f'<w:del w:id="11" w:author="Reviewer 1" w:date="2026-09-01T10:01:00Z"><w:r><w:delText xml:space="preserve"> in total</w:delText></w:r></w:del>{run(".")}</w:p>'
        f"<w:p>{run('Reviewer 2')}</w:p>"
        f'<w:p>{run("1. ")}<w:commentRangeStart w:id="1"/>{run("Table 2 is missing units")}<w:commentRangeEnd w:id="1"/>'
        f'<w:r><w:commentReference w:id="1"/></w:r>{run(".")}</w:p>'
    )
    document = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {W}><w:body>{body}<w:sectPr/></w:body></w:document>'
    comments = (
        f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:comments {W}>'
        f'<w:comment w:id="0" w:author="Reviewer 1" w:date="2026-09-01T09:00:00Z" w:initials="R1"><w:p>{run("Please qualify this claim.")}</w:p></w:comment>'
        f'<w:comment w:id="1" w:author="Reviewer 2" w:date="2026-09-02T09:00:00Z" w:initials="R2"><w:p>{run("Add the units in the column headers.")}</w:p></w:comment>'
        "</w:comments>"
    )
    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>'
        "</Types>"
    )
    package_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
        "</Relationships>"
    )
    document_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/>'
        "</Relationships>"
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as package:
        package.writestr("[Content_Types].xml", content_types)
        package.writestr("_rels/.rels", package_rels)
        package.writestr("word/document.xml", document)
        package.writestr("word/comments.xml", comments)
        package.writestr("word/_rels/document.xml.rels", document_rels)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    out = Path(argv[1])
    work = out / ".work"
    for folder in (out, work, out / "子文件夹 two", out / "reviews in"):
        folder.mkdir(parents=True, exist_ok=True)
    long_report(out / "long report.pdf", work)
    (out / "重复 副本.pdf").write_bytes((out / "long report.pdf").read_bytes())
    scanned(out / "scanned page.pdf", work)
    second = canvas.Canvas(str(out / "子文件夹 two" / "long report.pdf"), pagesize=A4)
    second.drawString(72, 760, "A different synthetic file that has the same name as another fixture. " + LABEL[:30])
    second.showPage()
    second.save()
    (out / "notes.md").write_text("# Synthetic notes\n\n" + LABEL + "\n\nInline math $a^2 + b^2 = c^2$ and a display block:\n\n$$\n\\int_0^1 x\\,dx = \\frac{1}{2}\n$$\n", encoding="utf-8")
    (out / "corrupt.pdf").write_bytes(b"%PDF-1.7\n1 0 obj\n<< /Type /Catalog")
    (out / "data.xyz").write_text("An unsupported synthetic format.\n", encoding="utf-8")
    word_review(out / "reviews in" / "decision letter.docx")
    annotated_review(out / "reviews in" / "reviewer 2 annotated.pdf")
    for leftover in work.iterdir():
        leftover.unlink()
    work.rmdir()
    print(f"Fixtures written to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
