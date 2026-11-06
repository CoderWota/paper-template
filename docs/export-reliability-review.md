# Export Workflow Review

Reviewed on 2026-11-05 at the researcher's request to explain export friction and improve the skills. The evidence is the [inbox-format export chat](codex://threads/01a1ab3d-a6cb-7b80-a673-ad4306ba2983), the current exporter, and read-only inspection of the affected table source. This maintenance changed the template, not that paper project or its delivered files.

## Findings and corrections

| Finding in the chat | Cause or evidence | Change |
| --- | --- | --- |
| The agent initially looked for a separate format template although the inbox contained the imported Word manuscript. | The skill selected a venue or neutral profile before identifying the user-named format source. | Identify the format source first. A manuscript can be an example. Keep observable example formatting separate from venue requirements. |
| Four table references failed although the source labels existed. | The Markdown reader exposed HTML table tags as raw blocks; they were not native numbered tables. A source-label check did not establish converter support. | Add a raw-content output-loss blocker. Require a small parsed and rendered fixture for fragile constructs. The blocker also catches an unreferenced raw HTML table. |
| A temporary filter eventually resolved references, but the table layout still failed. | Numbering did not establish column widths, merged headers, or a faithful cell layout. The filter also went through repeated full builds while its Caption API use was still failing. | Test converter API and structure on an isolated fixture first. Check spans, cell values, widths, and rendered pages separately from reference resolution. |
| Using the original as a reference document did not restore the original appearance. | Reference styles do not reproduce all direct formatting, table geometry, or pagination. | Inspect actual properties and example pages. Record rules and results separately instead of one broad formatting pass. |
| Rendering stopped, then moved to a separate LibreOffice route. | The recorded interruption occurred while copying into Word's staging area. The chat does not establish why the copy stalled or whether a Word dialog caused it. The exporter offered no explicit application selector and could accept an old PDF in the LibreOffice path. | Add explicit renderer selection, distinct staging, bounded application calls, a private LibreOffice profile, and render receipts tied to DOCX/PDF hashes. A requested render failure returns failure. |
| The final file was byte-identical to the archived original. | A copy replaced the failed rebuild. Hash equality between original copies did not compare them with the maintained Markdown. Failed build and page artifacts were subsequently removed. | Require the current manifest content for a rebuild. Label a requested source copy separately; retain a failed rebuild's status and useful evidence. A source copy cannot establish export completion. |
| A passing citation check could suggest more coverage than it had. | The manuscript had zero keyed citations. Typed author-year references were outside that check. | Report zero keyed citations explicitly, and distinguish key resolution from source identity or claim support. |

## Files changed

- Both client copies of `submission-assembly` now identify content and format separately, test fragile constructs early, name the renderer, retain failure evidence, and check the identity of the delivered version.
- Both client copies of `manuscript-import` now record raw-table representation and export risks in the import mapping. Import does not require an unsolicited full export.
- [Export reliability](export-reliability.md) supplies the conditional procedure shared by both clients.
- [The exporter](../scripts/export.py) and [DOCX inspection](../scripts/export/docx.py) enforce raw-content checks, render freshness, explicit renderer choice, and changed-exporter invalidation for new builds. Releases include a PDF only with a current successful render receipt.
- [Regression checks](../scripts/test_export.py) exercise the demonstrated integrity and recovery boundaries.

## Validation

On 2026-11-06, the researcher further required complete, unchanged content. The assembly skills and shared guide now require a pre-export baseline, full source-to-output reconciliation, explicit handling of representation differences, unchanged source hashes, and separate content results tied to the delivered files. Unexplained changes and unchecked content block completion. This is an instruction and requirement update; the existing exporter still does not provide exhaustive automated content comparison, and no real manuscript was rechecked in this follow-up.

The researcher further confirmed that fonts and table styles must be restored. Both assembly skill entrypoints, the shared guide, the profile instructions, and the project requirements now require effective font and table-appearance extraction, reproducible restoration, and separate source-to-output checks. Missing fonts and unsupported styles remain unmet requirements. This follow-up adds instructions and a confirmed rule; it does not implement or validate a general font or table-style restoration transform.

All 13 isolated regression checks passed. They cover raw HTML without a reference, source-copy-independent build failure, release refusal for that failure, native table captions and references, unchanged and changed inputs, exporter changes, comments, requested render failure, unavailable application selection, timeout, source changes during rendering, changed PDF content, and exclusion of an old PDF without a valid receipt. Application failure cases use mocks; table conversion and build checks use installed Pandoc 3.12.1 and pandoc-crossref 0.3.26.

A separate synthetic one-page document was built and rendered with LibreOfficeDev 26.8.0.0.alpha0. Its three-column table, signed values, caption, cross-references, inline formula, and displayed fraction were visually inspected. Two source formulas matched native Word math structures in the mechanical check. This does not establish editing behavior in Word. The local artifacts remain under ignored `.local/export-maintenance-qa/`; no research material or external service was used.

All four changed skill entrypoints passed `quick_validate.py`. The two client copies match, their updated local links resolve, and the change has no whitespace errors.

## Remaining work

The affected paper's complex HTML tables still need a verified converter repair and a new current-manuscript build. This maintenance adds detection and a better repair workflow; it does not implement general HTML-table conversion. No new live Word rendering or Windows application test was performed. The failed-copy cause in the earlier Word attempt remains undetermined.
