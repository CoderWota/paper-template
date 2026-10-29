# MVP 6 Skill Review

Status: `submission-assembly` and `submission-readiness` passed written review on 2026-10-29 under the gate used since MVP 2. `scripts/export.py` and its filters pass 10 tests (unit tests, and real builds where Pandoc and pandoc-crossref are installed), and a live build of a synthetic manuscript with a neutral and a synthetic journal profile was rendered by Microsoft Word and inspected. The first route is Word (DOCX), as the maintainer decided; see section 6 for what is not covered.

## 1. Rule and pass criteria

Fixed before the review, as in the [MVP 4 review](mvp-4-skill-review.md#1-rule-and-pass-criteria). For MVP 6 the guideline also requires rendered-output evidence: a claim about the delivered layout counts only when an actual rendered document was inspected; an openable file does not pass.

## 2. Method and evidence

Read both `SKILL.md` files and READMEs, `scripts/export.py`, `scripts/export/` (`tools.py`, `docx.py`, `equation-labels.lua`, `mermaid-figures.lua`), `scripts/tests/test_export.py`, and the profile README, against MVP 6 in the [implementation guideline](../mvp-implementation-guideline.md#mvp-6--template-driven-layout-and-readiness), [design plan](../design-plan.md) section 10, the [Markdown and export conventions](../markdown-and-export-conventions.md), the [export trial](../export-trial.md), and `AGENTS.md`.

| Evidence | Result |
| --- | --- |
| `python -m unittest scripts/tests/test_export.py` | 10 tests, OK, including two real builds and a Mermaid figure (Pandoc 3.12.1, pandoc-crossref 0.3.26, mermaid-cli 12.0.0 with Chrome 156) |
| Live build, neutral profile (synthetic manuscript in `.tmp/mvp6-live/`, three sections, metadata, two citations, nine formulas including one in a footnote, a figure, a Mermaid diagram, a table) | Passed: 9 of 9 formulas native with matching structure; 2 of 2 images placed; all references and citations resolved |
| Live build, synthetic journal profile (A4, 2.5 cm margins, Times New Roman and SimSun, 12 pt, double spacing, single-spaced tables, numbered black headings, line numbers, "Fig."/"Eq." with plurals, 6000-word limit) | Passed every expectation; Word 16.114.2 rendered the PDF |
| Visual inspection of the Word-rendered PDF | A4 pages with continuous line numbers; Times New Roman body text, double spaced; numbered black headings; inline and display equations laid out correctly with numbers on the right; footnote math; the gradient figure and the rendered diagram (Chinese label intact) with "Figure 1:" and "Figure 2:" captions; a single-spaced table with its caption above; author-date references with hanging indents; "Eqs. 1, 2" after the plural fix |
| Release rules, live | A passing, current build was frozen read-only; the same release ID was refused; after a body edit `verify` reported the build out of date and `release` refused |

## 3. Requirements

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| SA-1 | Archive supplied guidelines and templates unchanged in the profile; a PDF example is a visual specification, not a template | Met | `submission-assembly` L18–L19; `profile-init` writes `originals/` and `templates/` with READMEs. |
| SA-2 | A per-rule mapping of source, scope, implementation, and check, with confirmed interpretations only | Met | L23–L25; `requirements/profiles/README.md` layout. |
| SA-3 | Profile templates and reusable settings; no manual repair of each export | Met | L29–L30; `reference-doc` rebuilds the Word styles from `profile.yaml`; test `test_settings_are_applied_and_section_children_keep_schema_order`. |
| SA-4 | Faithful source-math-to-OMML: each formula a correctly structured native equation, inline or display, no silent fallback | Met | `docx.compare_formulas` matches formulas one by one (count, placement, structures such as `m:f`, `m:rad`, `m:nary`, `m:m`, `m:eqArr`, `m:acc`, and unconverted LaTeX); tests `test_matching_formulas_pass` and `test_missing_structure_unparsed_latex_placement_and_count_are_reported`; live builds 9 of 9. |
| SA-5 | Mermaid rendered as figures with source, identity, caption, and quality; unrendered diagrams reported | Met | `mermaid-figures.lua`; `render_diagrams`; test `test_a_diagram_becomes_a_numbered_figure`; live PDF inspection. |
| SA-6 | Render, inspect, and repair; report the actual application; missing fonts or renderers reported | Met | L34–L36; `render` names Word or LibreOffice; the inspection found the missing plural prefix, which was repaired in the build (F-1). |
| SA-7 | Rebuild after a body edit and switch between a neutral and a journal profile without rewriting content | Met | Live builds with both profiles; `verify` detects the stale build; L36 forbids rewriting scientific content for layout. |
| SA-8 | Immutable releases with input, profile, and tool records; previews rebuildable | Met | L41; `release`; tests `test_a_current_passing_build_is_frozen_once` and `test_failed_stale_or_unfinished_builds_are_not_released`. |
| SA-9 | Tools set up on demand with consent; writing never depends on them | Met | L13; `install` checks the published SHA-256 digests. |
| SR-1 | Readiness separate from impact and fit; reuses only current checks | Met | `submission-readiness` L12–L14. |
| SR-2 | Real remaining tasks and reviewer concerns with grounded improvements; no acceptance percentage; no submission | Met | L18–L32. |
| SR-3 | Author-only facts (declarations, contributions, funding) are asked for, never invented | Met | L22. |

## 4. Gaps found and fixed

- F-1: the inspection showed "Eq. 1, 2" for several equations; cross-reference settings now go in a metadata file, so profiles can set plural prefixes (`equation_prefix_plural`), and the live rebuild shows "Eqs. 1, 2".
- F-2: in Pandoc 3 a figure is a `Figure` block; the Mermaid filter first produced an image in a paragraph, which pandoc-crossref did not number. It now produces a `Figure`.
- F-3: the export trial's hand-edited reference document broke the schema order of the section properties; the builder now writes them in schema order (tested).

## 5. Verdict

Both skills are accepted by review on 2026-10-29.

## 6. Not covered

- A real journal's own Word or LaTeX template and current guidelines: the first profile is synthetic by the maintainer's choice.
- Editing a native equation in Word; Word fields for figure and table numbers (pandoc-crossref writes static numbers); Word on Windows; LibreOffice rendering.
- PDF routes other than Word's rendering of the checked DOCX, and LaTeX output.
- Fonts that are not installed on the rendering computer, and very large manuscripts.
- Codex and Windows; how a model follows the inspect-and-repair loop.
