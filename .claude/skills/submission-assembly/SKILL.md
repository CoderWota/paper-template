---
name: submission-assembly
description: Format and inspect Word output against a journal or thesis profile; preserve editable equations and freeze releases on request.
---

# Submission assembly

Outcome: a formatted Word file built from the manuscript with the selected output profile, checked against each adopted rule both mechanically and by inspecting the rendered pages, with a short summary of what passed and what needs attention. On request, a frozen release in `outputs/releases/`. A file that opens is not a compliant file.

## Step 1: Select the profile

1. First read `manuscript/manifest.yaml`. If it lists no section, report that no Word manuscript can yet be assembled and ask for the draft or content; stop before reading export internals, installing tools, or loading profiles. Otherwise use the target venue in `requirements/project.md` or the one the researcher names. Its profile is `requirements/profiles/<venue-id>/`. Without a target, use a neutral profile.
2. Run `python scripts/export.py tools`. If Pandoc, pandoc-crossref, or mermaid-cli (for diagrams) is missing, explain what each is for and its size, and install only with consent: `python scripts/export.py install --component pandoc --component crossref [--component mermaid]`. Use `environment-management` when Node.js or a browser is missing. Writing never depends on these tools.
3. Create a missing profile: `python scripts/export.py profile-init --id <venue-id> --name "<venue name>"`. It creates the profile's `templates/` folder, `profile.yaml`, and Pandoc's default Word styles. Write an English `README.md` in the profile folder describing its role and linking to `templates/`, `requirements.md`, `profile.yaml`, and the reference document. When `originals/` is created, add a README that says supplied files remain unchanged; add a README to `templates/` that describes its actual contents.

## Step 2: Gather and keep the sources

4. Copy each supplied guideline, Word or LaTeX template, and example article into the profile's `originals/` unchanged. Read the current official guidelines named in the venue note in `research/venues/` as well, and note the version or date of each source.
5. A PDF example shows a layout; it is not an executable template and not automatically the current specification. Text extracted from a document helps reading, but the original stays the source.

## Step 3: Adopt the rules

6. Extract the explicit rules that the output must meet: page and margins, fonts by language, sizes, spacing, headings and their numbering, title page and author information or anonymization, abstract and keywords, section order and required sections, citation and reference style, figure and table placement, captions and numbering, equation numbering, line numbers, length limits, and file requirements.
7. Write them in the profile's `requirements.md`, in English, one section per rule with the layout in `requirements/profiles/README.md`: the rule, its source and location, the implementation, the check, the latest result, and how it was confirmed. Adopting a supplied template or guideline authorizes its explicit rules; an inference from an example, a conflict between sources, or an ambiguous rule is asked as one question with your recommendation, and only the confirmed interpretation is recorded.
8. Content that a rule requires but the manuscript lacks (a structured abstract, a data availability statement) is reported as missing. Never invent it, and never delete material to fit a limit; those are the researcher's decisions.

## Step 4: Implement the rules

9. Put Word styles and page setup in the reference document: `python scripts/export.py reference-doc --profile <id> [--page A4] [--margins-cm 2.5] [--font "..."] [--east-asian-font "..."] [--size-pt 12] [--line-spacing double] [--space-after-pt 0] [--table-line-spacing single] [--heading-font "..."] [--heading-color black] [--line-numbers yes]`. The settings are kept in `profile.yaml`, so the document can be rebuilt. When the venue supplies its own Word template, try it as `reference_doc` in `profile.yaml` and compare the result; record what it does and does not control.
10. Put the other settings in `profile.yaml`: section numbering, cross-reference words in the manuscript language (`figure_prefix`, `figure_prefix_plural`, `table_prefix`, `equation_prefix`, `section_prefix`, `figure_title`, `table_title`), `table_equations`, `anonymize`, and a CSL style in `templates/` when the venue sets one (`csl:`; obtain an official style only with the researcher's consent for the download). Add the checkable expectations: `expect_page`, `expect_margins_cm`, `expect_font`, `expect_size_pt`, `expect_line_spacing`, `expect_line_numbers`, `expect_max_words`, `expect_anonymized`.

## Step 5: Build, inspect, and repair

11. Build: `python scripts/export.py build --profile <id> --render`. The build blocks on manuscript integrity or output-loss issues (`python scripts/manuscript.py check`), such as a missing image, unresolved citation, dropped LaTeX, lost equation structure, missing required front matter, or an AI signature. It also reports layout expectations, length, and open `[TODO: ...]` markers; these findings do not by themselves block a preview. The record in `build.json` distinguishes blocking checks from notes. A manuscript without metadata builds with no title block; say so when the profile or venue requires one, and ask the researcher for the title, authors, and keywords instead of inventing them.
12. Inspect the rendered PDF page by page against every rule in `requirements.md`: layout, fonts for each language, spacing, headings, title block, abstract, captions and numbering, equations (inline, display, numbering), citations and the reference list, figures at the printed size (labels, Chinese text, clipping, resolution), tables, line numbers, page breaks. Compare body, headings, abstract, figure and table captions and descriptions, and publication metadata with the confirmed target paper language; a draft or preview may still contain another working language. Report mismatches without translating them during formatting. Microsoft Word renders on macOS and Windows; when Word shows a dialog and does not answer, ask the researcher to handle it, then render again with `python scripts/export.py render --docx ...`. LibreOffice's layout can differ from Word's; say which application rendered the pages.
13. Repair the profile, templates, or filters, never the scientific content, and build again until each rule passes or a specific limitation remains: a missing font, a construct that does not convert, a rule that the reference document cannot express. Record each rule's result in `requirements.md`.

## Step 6: Deliver

14. Report in the interaction language: the profile, the checks that passed, what still needs attention with its cause, and the file locations. A preview in `outputs/preview/` is rebuildable and is not a submission.
15. When the researcher asks for the final package, first confirm that publication components use the target paper language or report the specific unresolved mismatch for a research decision. Write a concise English release description at `outputs/preview/<profile>/release-README.md` from the actual build record, stating the manuscript file, profile, build date, and any nonblocking layout or length notes and open items allowed by the researcher. Then freeze it: `python scripts/export.py release --profile <id> --id <release-id> --readme outputs/preview/<profile>/release-README.md`. It accepts only a current build whose blocking checks passed, copies that README into the package, refuses open `[TODO: ...]` markers unless the researcher confirms a release with open items, and never overwrites a release. A release is not a submission; submitting is the researcher's separate action.

## Completion check

- Every adopted rule has a source, an implementation, a check, and a recorded result; inferred or conflicting rules were confirmed first.
- The build passed its checks, and the rendered pages were inspected against each rule; the application that rendered them is named.
- No scientific content was rewritten or removed for layout, and missing content is reported, not invented.
- A release, if made, is a current passing build, frozen and never overwritten.
