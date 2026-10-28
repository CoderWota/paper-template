# Export Trial

Status: run on 2026-10-28 with Pandoc only, as the maintainer decided (“只装 Pandoc”); Quarto was not installed or compared. The maintainer's decisions are in section 6. This is a design trial, not an MVP or a skill; MVP 6 proves the chosen route on a profile.

## 1. Environment

- macOS 26.6.2 on Apple Silicon (arm64), 16 GB memory. Microsoft Word 16.114.2, Google Chrome 156, and Node.js 25.9.0 were already installed. No LaTeX, Typst, or LibreOffice is installed.
- Pandoc 3.12.1 (`pandoc-3.12.1-arm64-macOS.zip`, SHA-256 `c2146cf33a583f3ac93eccddf1bb662371d5cfcce1aad1c87ad860cca1435d46`) and pandoc-crossref 0.3.26 (`pandoc-crossref-macOS-ARM64.tar.xz`, SHA-256 `5bd7ab1472c37c22b775042b1e8b82449a541ca1a2181e402e98a8def5d0ce76`), downloaded from their official GitHub releases, checked against the published digests, and unpacked into the ignored `.tools/pandoc/3.12.1/` and `.tools/pandoc-crossref/0.3.26/` (188 MB and 165 MB unpacked). Pandoc 3.12.1 was chosen over the newer 3.13 because pandoc-crossref 0.3.26 is built against Pandoc 3.12.1.
- `@mermaid-js/mermaid-cli` 12.0.0 (Mermaid 12.2.0, Puppeteer 25.16.0), installed with npm into the ignored `.tools/mermaid-cli/` (457 MB) with install scripts disabled and no browser download; it renders with the installed Chrome through a Puppeteer configuration file. Installed after the maintainer's answer “安装（推荐）”.
- Windows builds exist for x64 only (Pandoc 3.12.1 `.msi` and `.zip`; pandoc-crossref `Windows-X64.7z`). An ARM64 Windows machine would run them under emulation; nothing was run on Windows.

## 2. Fixture

A synthetic test manuscript written for the trial, kept in the ignored `.tmp/export-trial/`: a YAML title block; three numbered sections; two synthetic BibTeX entries cited as `@key`, `[@key, p. 12]`, and `[@key1; @key2]`; inline math (Greek letters, a fraction, sub- and superscripts, a sum, an integral with a vector accent, a bar accent, a square root); three labeled display equations (a fraction with a hat accent and a sum; a parenthesized matrix with a limit; an `aligned` derivation); math inside a footnote; a literal currency amount (`US\$5`); a Chinese paragraph with inline math; a PNG figure with a caption and a width; a captioned table; a fenced Mermaid block; and references to sections, the figure, the table, and the equations.

## 3. Commands

```text
pandoc manuscript.md --filter pandoc-crossref --citeproc --bibliography references.bib \
  [-M autoSectionLabels=true] [-M tableEqns=true] [--reference-doc reference-journal.docx] -o trial.docx
pandoc manuscript.md --filter pandoc-crossref --citeproc --bibliography references.bib -t markdown
```

Native equations were reconciled with a namespace-aware script that reads the Pandoc JSON AST and the OMML in `word/document.xml` and `word/footnotes.xml`, formula by formula.

## 4. Results

| Area | Observation |
| --- | --- |
| Citations | `[@key]`, `@key`, locators, and multiple citations resolve with citeproc; the default style is Chicago author-date, and the bibliography is placed at `::: {#refs}`. A missing key produces a citeproc warning, which a build can turn into a failure. |
| Cross-references | pandoc-crossref resolves `@sec:`, `@fig:`, `@tbl:`, and `@eq:` references, including `[@eq:a; @eq:b]` (“eqns. 1, 2”). With `autoSectionLabels`, every heading can be referenced by its automatic identifier (`@sec:data-and-methods`) without an attribute in the heading. A `\label{}` inside math is not recognized: pandoc-crossref warns “Undefined cross-reference” and prints `¿eq:energy?`, so a build check can detect it. The prefixes (“fig.”, “eq.”) are configurable per profile; writing “Section @sec:x” duplicates the word. |
| Native Word equations | All 11 source formulas (10 in the body, 1 in a footnote) became separate native OMML objects; the 3 display formulas sit in `m:oMathPara`. Structures matched the source: `m:f` for fractions, `m:sSub`, `m:sSup`, and `m:sSubSup` for scripts, `m:nary` for the sum and the integral, `m:m` inside `m:d` for the matrix, `m:limLow` for the limit, `m:acc` for accents, `m:rad` for the root, and `m:eqArr` for the aligned derivation, whose alignment points are `&` runs. No OMML text contained a LaTeX command, and the literal `US$5` stayed text. |
| Equation numbers | By default pandoc-crossref puts the number inside the equation (`\qquad(1)`, as text in the OMML). With `tableEqns` it places each equation and its number in a table. Neither uses Word fields. |
| Captions | “Figure 1:” and “Table 1:” are written as static text in the captions, not as Word `SEQ` fields: numbering is correct in the output but does not update when someone edits the Word file. |
| Template | A modified reference document carried its page size (A4), margins (2.5 cm), line numbering, default fonts (Times New Roman, SimSun for East Asian text), and double spacing into the output. Hand-editing the reference document must keep the schema order of `w:sectPr` children (`w:footnotePr` before `w:pgSz`); the trial edit did not, so a profile builder needs a validated writer. |
| Mermaid | Pandoc alone leaves a Mermaid block as a code block in the DOCX. `mmdc` with the installed Chrome rendered a flowchart with a Chinese label, punctuation (parentheses, a colon, an ampersand), and a long label that wrapped, as a 1656 × 435 PNG at scale 3; a diagram with a syntax error produced no image and an error. Placing rendered diagrams as captioned figures is MVP 6 work. |
| Rendered view | macOS Quick Look rendered the DOCX without any equation (blank gaps), so it cannot judge math. Word 16.114.2, driven through AppleScript, first timed out on a dialog; after the maintainer handled the dialog, it exported both DOCX files to PDF, and the pages were rendered to images with PDFKit. Word laid out every equation correctly: inline math in English and Chinese text, the fraction, scripts, sum, matrix in parentheses, limit, integral with a vector accent, bar accent, square root of a fraction, the footnote math, and the aligned derivation with its two `=` signs aligned (the `&` runs are invisible alignment points). Equation numbers stand to the right. The journal-styled file showed A4 pages, line numbers, Times New Roman, and double spacing, while headings kept the template's own font and colour, and table rows took the double spacing of body text. Editing an equation in Word was not exercised; Word's AppleScript dictionary has no object for counting equations. |
| GitHub | With the maintainer's permission (“允许（推荐）”), two synthetic samples were rendered by GitHub's Markdown API (`POST https://api.github.com/markdown`, `gfm` mode, no repository, no sign-in). A display block with `{#eq:...}` on its closing line, or on the next line of the same paragraph, is not recognized as math: it shows as plain text. The same block followed by a blank line and a `{#eq:...}` paragraph renders as display math, with the label shown as a separate line. Image attributes (`{#fig:...}`) and table caption lines show as literal text after the image or table. `@eq:force` and `[@eq:force]` become links to the GitHub user named `eq`, a cosmetic effect of GitHub's mention syntax; a citation key that matches no user stays text. Mermaid blocks come back marked for GitHub's diagram viewer. |
| PDF | Not attempted: the maintainer chose the Word route first, and no PDF engine is installed. |

## 5. Assessment

Pandoc with pandoc-crossref meets the source-to-native-OMML requirement for every construct in the fixture, Word renders those equations correctly, and citations and cross-references resolve, with detectable failures for missing keys and labels. Its reference document controls styles and page setup, but not body content, numbering fields, or a journal's full layout, which matches the design plan's caution (section 10). pandoc-crossref's own equation-label form breaks GitHub's math rendering, so the workspace writes the label as its own paragraph and a small project Lua filter attaches it before pandoc-crossref runs; this form was tested with Pandoc and with GitHub. Open points: editing an equation in Word, Word fields for numbering, and a PDF route.

## 6. Decisions

The maintainer answered on 2026-10-28:

- Publishing engine and syntax (“采用（推荐）”): Pandoc, with pandoc-crossref for cross-references and citeproc with CSL styles for citations. Citations are written `[@key]`, `@key`, or `[@key, p. 12]`, with the metadata in `references/bibliography.bib`. Figures are written `![Caption](path){#fig:id}`, tables have a caption line `: Caption {#tbl:id}`, sections are referenced by their automatic identifiers (`@sec:<identifier>`, with `autoSectionLabels`), and the text refers to `@fig:id`, `@tbl:id`, `@eq:id`, and `@sec:id`.
- Equation labels (“改用空行后标签（推荐）”), replacing the closing-line form after the GitHub check: a labeled display equation is followed by a blank line and a paragraph that holds only `{#eq:id}`; the project's Lua filter attaches it to the equation before pandoc-crossref runs.
- GitHub check: synthetic samples only, through GitHub's Markdown API (“允许（推荐）”).
- Mermaid renderer: `@mermaid-js/mermaid-cli` in `.tools/`, using the installed browser (“安装（推荐）”).
- Word inspection: retried with the maintainer handling Word's dialog (“我重试，你处理弹窗（推荐）”).

The first output route stays Word (DOCX) with a neutral and a synthetic representative journal profile, decided earlier the same day; the PDF route and its engine are decided in MVP 6.
