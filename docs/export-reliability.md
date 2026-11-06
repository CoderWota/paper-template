# Export Reliability

Use this guide with `submission-assembly` for imported drafts, example Word files, complex tables, or a failed conversion. It applies to both clients. It does not authorize rewriting science, replacing the current manuscript, installing tools, or uploading material.

## Content and format are separate inputs

Read the current manifest, sections, metadata, and import mapping. Use the original only as format evidence unless the researcher explicitly requests a copy. Check whether the current manuscript has changed since import. Matching the archive to `manuscript/source/` does not compare it with the maintained Markdown.

When the researcher says “use the paper format in the inbox,” inspect the available file and state the selected source. If there is one clear example, proceed with its observable layout. Ask only if multiple plausible files or conflicting instructions affect the result. Record example-derived layout separately from adopted venue requirements.

Pandoc's reference document supplies styles and document properties. It does not copy the example's body, direct formatting, all section layouts, table geometry, or exact pagination. A style named Normal may inherit its font; visible headings may be directly formatted paragraphs. Inspect actual properties and source pages before promising fidelity.

## Preserve complete content without rewriting

Formatting and export must preserve the current manuscript's complete content without unauthorized changes. Establish the comparison baseline before conversion: the manifest and its section order, selected section text, publication metadata, bibliography and citation locators, figures and other included assets, notes, and explicitly included appendices or supplements. Preserve a recoverable snapshot and hashes in ignored working storage; do not overwrite received originals or releases. Do not silently include an unlisted file or omit a listed one. A style example supplies appearance, not prose or data for the manuscript.

Compare with the current selected content, not an archived draft that predates authorized edits. If the researcher explicitly requests the original's content, use that version as the stated baseline and resolve any conflict with the maintained version before substituting it. Do not edit manuscript wording, punctuation, numbers, units, hedges, citations, mathematical meaning, or language while repairing output. Report a suspected source error for a separate decision.

Use an independent source-to-output comparison. Establish expected content from the pre-conversion sources and a checked source parse, not solely from the converter's final AST, which may already have lost material. Reconcile the final DOCX in both directions: every expected item appears in its proper context and every output item has a source or an explicitly documented generated role. Check sequence and identity as well as presence to detect duplication, relocation, and replacement. Cover the following:

- Title, authors, affiliations, abstract, keywords, headings, all paragraphs and lists, quotations, acknowledgments, and declarations, in reading order.
- Every table's cell contents and positions, numbers and decimal precision, signs, uncertainty values, units, statistical marks, notes, merged-cell relationships, and captions. A matching table count or bag of cell text cannot prove correct row/column association.
- Each inline and displayed formula, symbols, operators, scripts, fractions, matrices, limits, conditions, and equation references. Compare mathematical structure and meaning with the source; formula counts and the presence of OMML tags alone do not establish equality.
- Each figure's identity and visible content, labels, panels, captions, notes, and in-text references. Check cropping and clipping. Where media bytes differ because of a documented conversion, inspect visual equivalence rather than treating a count as proof or a changed hash alone as proof of altered scientific content.
- Footnotes and endnotes linked to the right text, citation identities and locators, every reference entry, hyperlinks where part of the manuscript, and included appendices or supplements. Inspect relevant DOCX parts, not only the main body. Include source text boxes or content-bearing headers/footers where applicable; handle comments and tracked changes through their authorized workflow.

Text extraction or a DOCX-to-text round trip can locate differences, but is not complete evidence for formulas, tables, fields, images, or reading order. Use structure-aware comparisons for those objects and inspect all rendered pages for invisible, clipped, overlapped, or missing content. Content present in XML but absent from the visible pages does not pass. A full textual comparison and targeted object checks complement page inspection; neither a few inspected pages nor a word-count match covers the whole manuscript.

Distinguish exact content from its output representation. Line wrapping and layout whitespace, generated page numbers, cross-reference expansion, and bibliography rendering can legitimately differ under the adopted profile. Record those transformations explicitly and verify their mappings, including citation keys and locators and referenced objects. Do not normalize away negation, punctuation with meaning, signs, decimal precision, superscripts, symbols, capitalization, or row order to obtain equality. Do not ignore all headers, numbers, or bracketed text because some are generated. An unexplained difference remains a failure, not an assumed formatting effect.

Write a content-comparison report in the profile's check record or a linked file under `outputs/checks/`. Identify baseline files and hashes, the final DOCX/PDF hashes and renderer, comparison method and coverage, expected transformations, each located difference and disposition, and the separate completeness and unchanged-content results. Use passed, failed, or not checked. Confirm source hashes remain unchanged after export. If the source changes while work is in progress, take a new baseline and repeat affected checks. If the final output changes during repair or post-processing, invalidate the prior comparison and inspect the new result.

Do not deliver an unexplained content difference as an unchanged completed export or freeze it as a completed final package. A failed or incomplete preview can be supplied with its actual status. Restore the affected output from the baseline or fix the converter; do not alter the baseline to make a difference disappear. The current exporter checks selected losses, object structures, and file freshness, but does not yet implement exhaustive content comparison. Its passing status or a release receipt alone cannot satisfy this requirement. When a comparison cannot cover a construct, name that scope and leave content preservation unverified for it.

## Restore fonts and table appearance

A request to restore a supplied format includes its fonts and table styles. Reproducing text, table structure, and numbering alone is insufficient. Create separate sourced requirements for typography and table appearance. Use the source's own settings, not an assumed journal convention or a preferred three-line table style.

For each text role used in the output, record the effective font family, size, bold and italic state, color, paragraph spacing, and alignment: title, abstract, heading levels, body, captions, table headers and cells, table notes, and references. Preserve meaningful differences within paragraphs, such as italic statistical symbols and superscripts. Resolve document defaults, theme fonts, style inheritance, paragraph and character styles, table conditional styles, and direct run formatting. Inspect Latin, East Asian, and complex-script font assignments where used. A font name in `styles.xml` alone is not evidence that the source text uses it.

Check that the required fonts are available to the selected renderer. If a font is missing or substituted, identify the affected role and leave its fidelity check unmet. Apply the environment-management consent rules before installing a font. Do not silently choose a similar font or bundle a font without authorization. A researcher-approved substitute is recorded as a substitute, not exact restoration.

For each table or genuinely shared table design, record the following properties where present:

- Table width, alignment, indentation, fixed or automatic layout, column widths, and row heights, including exact versus minimum height.
- Outer and inner borders, their position, line type, width, and color; borderless cells; shading and alternating row or column treatment.
- Cell margins and spacing, horizontal and vertical alignment, text direction, and paragraph indents and spacing.
- Header, body, and note typography; merged cells; repeated header rows; row splitting and page breaks; caption and note spacing.

Read effective table formatting from `w:tblPr`, table styles and conditional `w:tblStylePr` rules, `w:tblLook`, and row/cell/paragraph/run properties as needed. Restore the effective appearance, not merely the source style ID. Equal IDs can render differently, and different IDs can describe the same appearance. The current `expect_font` check and `table_line_spacing` setting do not verify this full set of properties.

Implement reusable properties in the derived reference document. Preserve source-derived style dependencies and keep received originals unchanged. Apply necessary table-specific or run-specific properties through a maintained export transform when the reference document does not control them. Ensure the build invokes that transform before checking and hashing the final DOCX; a manual edit after a passing build invalidates that build. Record the implementation location per requirement and verify that a rebuild reproduces it. Do not reset a tuned reference document to Pandoc's defaults during a later repair.

Compare the original and rebuilt DOCX properties, then inspect both with the same named renderer and page size. Check every distinct text role and table design, all affected tables, and their page continuations. Where available, inspect the rendered PDF's font inventory for actual font use and fallback; combine it with DOCX properties and page inspection, since an inventory alone does not map fonts to every text role. Check borders, shading, spacing, emphasis, symbols, line wrapping, and clipping at the intended printed size. Mark typography and table appearance separately as passed, failed, or not checked. Record renderer differences or unsupported properties and their effect; do not count structural success as visual fidelity.

## Inspect a fragile construct before rebuilding the paper

Run the manuscript check, then inspect the selected sources for raw HTML tables, merged cells, nested tables, equations, embedded objects, and manual captions. Source checks can recognize a label without the converter recognizing its object. An imported HTML table can become many `RawBlock` tags mixed with cell paragraphs in the Markdown reader; the DOCX writer can drop those tags and retain only disconnected text.

For a fragile construct, keep a small isolated fixture under ignored `.local/` or a temporary directory. Reuse installed tools. Include its caption, an in-text reference, and representative cell structure. Use the same reader and filter order as the build. Inspect Pandoc JSON for native `Table`, `Math`, and `Figure` objects, identifiers, captions, row and column spans, and remaining `RawBlock` or `RawInline` nodes. A regular expression match is only a way to locate material.

For tables, compare the expected cells, values, signs, notes, spans, and column widths with native Word `w:tbl`, `w:tr`, `w:tc`, `w:gridSpan`, and `w:vMerge` structures as applicable. Then render and inspect the table at the intended page size. A table count, visible text, or resolved reference alone cannot establish a faithful conversion.

When repairing a converter, establish the installed API in the minimal fixture before running the whole manuscript. Keep a regression fixture for the demonstrated failure. Preserve captions as inlines, including formatting, citations, and math. Run object conversion before cross-reference numbering. Do not flatten merged cells, discard columns, replace tables with screenshots, or alter values to obtain a passing build. If a conversion cannot be checked, report that construct as unsupported.

The exporter blocks remaining raw content for another format, apart from HTML comments. This is an output-loss guard, not an HTML-table converter or a proof of table fidelity. Converting HTML to a native Table remains a separate operation that needs the structural and visual checks above.

## Render with a named application

Use `build --render --renderer word` or `--renderer libreoffice` to select an installed application. `auto` chooses Word when available, otherwise LibreOffice. A failed Word attempt does not silently switch applications. Avoid another identical attempt after a timeout; use its diagnostic to decide whether a dialog needs the researcher or an installed renderer can produce a review preview.

`render --docx PATH --renderer libreoffice` uses a separate local application profile. No document is uploaded. State the renderer change before continuing. If Word verification is required, a LibreOffice preview leaves it open. Do not close the researcher's documents or terminate a shared application process to clear a render lock.

Rendering uses a distinct temporary output and requires a successful application result and a new, nonempty PDF. `<name>.render.json` records the source DOCX hash, renderer, result, and successful PDF hash. An old PDF is not a successful render of a changed DOCX. A requested render failure makes the build command fail even if DOCX generation passed; `build.json` continues to describe the mechanical build. Inspect the PDF pages separately and record the actual inspection scope.

## Keep evidence and deliver the requested version

Keep `build.json`, the relevant diagnostic, and enough failed output or page evidence to locate an unresolved failure. Remove only redundant temporary material after the useful evidence is retained. A filter or exporter change invalidates earlier checks; rebuild and inspect the affected output.

In the profile's rule record, separate source observations, implementation, mechanical results, and visual results. Name the assessed file and renderer. Check references in context: zero keyed citations does not validate manually typed author-year references. Missing supplements or unchecked evidence may affect readiness without preventing a clearly labeled layout preview.

Deliver a current rebuild with its real status. If conversion fails, report it as incomplete and identify the affected content. An archived original may be useful as an explicitly requested reference copy, but it is not a rebuild and may omit current edits. Do not name it a final rebuilt paper or claim it passed the failed build. Before freezing a release, follow the skill's review and language checks; the release command accepts only a passing current build and includes a PDF only with a matching successful render receipt.
