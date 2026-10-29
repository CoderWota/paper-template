# MVP 5 Skill Review

Status: `manuscript-import`, `manuscript-outline`, `manuscript-writing`, `manuscript-audit`, and `manuscript-revision` passed written review on 2026-10-29 under the gate used since MVP 2. `scripts/manuscript.py`, the Pandoc route of `scripts/ingest.py`, and `scripts/ingestion/adopt-conventions.lua` pass 15 tests, 4 of them real conversions with Pandoc. Live behavior of a model, Codex, and Windows are not covered; see section 6.

## 1. Rule and pass criteria

Fixed before the review, as in the [MVP 4 review](mvp-4-skill-review.md#1-rule-and-pass-criteria).

## 2. Method and evidence

Read the five `SKILL.md` files and READMEs, `scripts/manuscript.py`, the changed ingestion modules (`routes.py` with `PandocRoute`, `pipeline.py`, `reviews.py` with `ManuscriptStage`, `records.py`) and `ingest.py`, `scripts/ingestion/adopt-conventions.lua`, and `scripts/tests/test_manuscript.py`, against MVP 5 in the [implementation guideline](../mvp-implementation-guideline.md#mvp-5--evidence-based-writing-audit-and-major-revision), [design plan](../design-plan.md) sections 5 (flexible intake and manuscript adoption), 9, and 10 (canonical content; major revision), the [Markdown and export conventions](../markdown-and-export-conventions.md), and `AGENTS.md`. The converter for editable manuscripts follows the maintainer's decision of 2026-10-29 (“可编辑稿件用 Pandoc（推荐）”) and the comparison of open-source converters made for it (section 5).

| Evidence | Result |
| --- | --- |
| `python -m unittest scripts/tests/test_manuscript.py` | 15 tests, OK |
| Convention checks | A conforming manuscript in Chinese and English passes; a closing-line equation label, `\label` in a formula, a blank line in a formula, unresolved references and citation keys, a missing image, a duplicate label, an unclosed formula, and manifest errors are problems; hand-numbered references, a word repeated before an `@`-reference, currency, single-line display math, and `[TODO: ...]` markers are warnings or open items |
| Revisions | A baseline is kept with checksums; an author edit after the baseline blocks applying the candidate until it is reconciled; an interrupted application is detected and resumed; the baseline can be restored |
| Adoption, live Pandoc | A Word manuscript (Chinese title and heading, footnote with math, display formula, image, table) became section files with the image, `metadata.yaml`, the manifest, and `mapping.md`, and passed the check; tracked changes blocked adoption until it was converted again with the researcher's choice; a LaTeX file arrived as `@sec:`, `@eq:`, and `{#eq:...}`; the Pandoc route refused a reference document and a PDF |
| Live adoption of the export-trial Word file (`.tmp/adopt-live/`) | 4 section files, 1 image, metadata; the mapping flagged the 3 typed equation numbers; the check flagged the static "Figure 1" and "Table 1"; a second adoption over the manuscript was refused |

## 3. Requirements shared by the five skills

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| CC-1 | Packages, frontmatter, READMEs, generated copies | Met | `sync_skills.py --check`: 33 packages. |
| CC-2 | The conventions of the export trial: citations, labels, GitHub math, Mermaid, no hand numbering | Met | `manuscript-writing` L24; `manuscript.py check`; conventions document. |
| CC-3 | One file per major section at most; an explicit manifest; outline, notes, drafts, and READMEs never assembled | Met | `manuscript-writing` L29; `set-sections` refuses non-sections; `assemble` joins only listed files (test `test_assemble_joins_only_listed_sections_with_metadata`). |
| CC-4 | No invented sources, results, quotations, or repairs; unsupported claims stay visible | Met | `manuscript-writing` L23 (`[TODO: ...]`); `manuscript-audit` L26; `manuscript-revision` L34. |
| CC-5 | Scoped rules applied; no rule from a one-time request or an inference | Met | `manuscript-writing` L12–L13, L17. |
| CC-6 | The researcher's direct edits preserved | Met | `manuscript-writing` L17, L25; `manuscript-revision` L40–L41 and the reconciliation test. |

## 4. Requirements by skill

| ID | Skill | Requirement | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| MI-1 | `manuscript-import` | Preserve originals; prefer editable sources; convert supported formats; never silently replace a working manuscript | Met | L12–L27, L36–L41; `ManuscriptStage` keeps originals in the import record; adoption refuses over a manuscript (tests). |
| MI-2 | `manuscript-import` | Inventory sections, figures, tables, equations, footnotes, citations, comments, and revisions; expose losses and unresolved references | Met | L43–L49; `mapping.md`; `annotations.md`. |
| MI-3 | `manuscript-import` | Do not accept every tracked change or merge drafts silently; conversion is not a rewrite | Met | L31–L32, L48; test `test_tracked_changes_stop_adoption_until_the_researcher_decides`. |
| MI-4 | `manuscript-import` | Resolve references against actual records without inventing matches or claiming full text | Met | L47. |
| MO-1 | `manuscript-outline` | Argument and section plan from actual evidence; gaps visible; structure confirmed; no forced structure | Met | L17–L29. |
| MW-1 | `manuscript-writing` | Focused drafting against confirmed constraints and actual evidence, in the manuscript language, with venue AI policy | Met | L12–L25. |
| MA-1 | `manuscript-audit` | Separate checks of argument, terminology, style rules, citation integrity, and support; findings tied to passages; no edits unless asked | Met | L17–L33; check records make a changed input stale (test `test_a_changed_input_makes_a_recorded_check_stale`). |
| MR-1 | `manuscript-revision` | Real baseline including unsaved edits, recoverable without Git; earlier releases untouched | Met | L17–L24; `revision-start` (test). |
| MR-2 | `manuscript-revision` | Researcher-directed scope and plan; old-to-new mapping; confirmation of the plan | Met | L28–L30. |
| MR-3 | `manuscript-revision` | Bounded, resumable work; candidate kept out of assembly; intervening edits reconciled; interruption detectable | Met | L34–L41; tests `test_baseline_candidate_conflict_reconciliation_and_restore` and `test_an_interrupted_application_is_detected_and_resumed`. |
| MR-4 | `manuscript-revision` | Input-versioned rechecks; changed claims rechecked; stale passes never carried forward; missing research stays a gap | Met | L45–L46; `checks` reports stale records. |
| MR-5 | `manuscript-revision` | One clearly identified active manuscript | Met | L50; the manifest defines it. |

## 5. The converter decision and its evidence

At the maintainer's request, a subagent compared open-source converters on the export-trial Word file, a Word-style review fixture (comments, tracked changes, Zotero, Mendeley, and EndNote fields), a LaTeX file, and an OpenDocument file, on 2026-10-29, checking every formula by hand and rendering it with MathJax 3.2.2. Results (GitHub stars read on 2026-10-28):

| Tool | Stars | Word formulas correct | Footnotes | Comments and tracked changes | LaTeX input |
| --- | --- | --- | --- | --- | --- |
| Pandoc 3.12.1 | 46.7k | 14 of 14 | kept | kept as marks | best of those tested |
| MarkItDown 0.1.9 | 192.7k | 5 of 14 | plain list | comments lost, changes accepted | none |
| Docling 2.144.0 (docling-slim) | 69.7k | 9 of 14 | dropped | changes accepted | weak |
| MinerU 4.0.12 Office engine (DocVortex 0.6.7) | 82.7k | 10 of 14 | dropped | changes accepted | none |
| mammoth 1.13.0 | 1.1k | 0 of 14 | kept | changes accepted | none |

The more widely starred tools are built for feeding documents to language models or for PDF layout; on these fixtures they corrupted or dropped formulas and accepted tracked changes silently. Pandoc was kept. The findings that shaped the implementation: keep `--track-changes=all` so that changes are never accepted by default; write Pandoc Markdown, not GFM, because GFM output drops LaTeX citations; citation keys from Word fields are reference-manager identifiers that need mapping; typed equation numbers stay inside formulas; Pandoc's OpenDocument reader can mark inline formulas as display math, which the conventions filter reverses for formulas inside running text. The fixtures were made by Pandoc, which may favour it; real Word and LibreOffice files and old equation-editor objects were not tested.

## 6. Verdict and limits

All five skills are accepted by review on 2026-10-29. Not covered: real manuscripts with complex Word fields, cross-references, or old equation-editor objects; PDF manuscripts through MinerU (the route is the MinerU route already observed in MVP 2, not exercised for a manuscript here); how a model follows the outline, writing, audit, and revision procedures; Codex; Windows.
