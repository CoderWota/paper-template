---
name: manuscript-import
description: Import an existing manuscript while preserving its original and mapping its stated argument. Use when the researcher asks to adopt a draft; report conversion losses and unresolved references.
---

# Manuscript import

Outcome: the researcher's existing draft adopted into `manuscript/` (or staged beside the current one for comparison), with an internal Mermaid logic map of the imported argument, in the workspace conventions, with the original kept unchanged and conversion losses named. Import preserves the draft's language even when the target paper language differs; it does not translate, rewrite the science, or accept tracked changes on the researcher's behalf.

## Step 1: Identify the material and the target

1. Find the main manuscript file and what belongs to it: a figures folder, a `.bib` file for LaTeX, supplementary files. Prefer an editable source (Word, LaTeX, OpenDocument, Markdown) over a PDF of the same text.
2. Run `python scripts/manuscript.py check` and read `manuscript/manifest.yaml`. When the manuscript already lists section files, the import is staged as a revision candidate for comparison (Step 4); it never goes over the current manuscript. Read the current `manuscript/logic-map.md` if present when comparing an existing working manuscript. If it is missing, note that gap and leave it unchanged while staging the import. Ask the researcher which version is the working one when that is unclear.

Ready to convert when the input and target are clear and an existing manuscript is protected from replacement.

## Step 2: Convert, keeping the original

3. Choose the route by format:

   | Format | Command |
   | --- | --- |
   | Word `.docx`, OpenDocument `.odt`, LaTeX `.tex` | `python scripts/ingest.py run --to manuscript --route pandoc FILE` (Pandoc on this computer; nothing is uploaded) |
   | Markdown or text | `python scripts/ingest.py run --to manuscript FILE` (read directly) |
   | PDF or a scan | Do not upload it to MinerU: the confirmed scope allows reference materials only. No local MinerU conversion is available. Preserve the original and report that a readable editable copy or another authorized route is needed. |
   | Old Word `.doc` | Ask the researcher to save a copy as `.docx`. |

   When Pandoc is missing, explain it and install it only with consent: `python scripts/export.py install --component pandoc`.
4. The import keeps the original unchanged in `inbox/imports/<import-id>/originals/` and the converted text in `extracted/markdown/`, with its images in `extracted/assets/`. Word citation fields from Zotero, Mendeley, and EndNote become citations; LaTeX labels, references, and citations become the workspace syntax; formulas become `$...$` and `$$` with label paragraphs. Write or update the import folder's English README from `import.json` and the observed conversion results.

Done when the original, converted text, assets, and conversion provenance are preserved, or the exact conversion blocker is recorded.

## Step 3: Tracked changes and comments

5. When the Word file has tracked changes or comments, they are listed in `extracted/markdown/<document>.annotations.md` and marked in the converted text, and adoption refuses to continue. Show the researcher the changes with their authors and ask one question: accept them all, reject them all, or go through them. Then convert again with `--track-changes accept` or `--track-changes reject` and `--reconvert`; for a mixed decision, convert with the choice that covers most items and apply the remaining decisions as manuscript edits, as agreed.
6. Comments from coauthors or supervisors are advice: offer to file them with `research-feedback`. Never apply a comment's suggestion as part of the conversion.

Proceed only after tracked changes have a researcher-approved disposition. Preserve comments as advice; do not apply them during conversion.

## Step 4: Adopt

7. Adopt into an empty manuscript:

   ```text
   python scripts/manuscript.py adopt --import-id <import-id> [--document <name>]
   ```

   With a current manuscript, keep it and stage the import: `python scripts/manuscript.py revision-start --id <revision-id>`, then `adopt ... --into candidate --revision-id <revision-id>`, and compare the two (`revision-status`, `git-compare`). Replacing the working manuscript with the imported one is the researcher's decision, applied through `manuscript-revision`.
8. The adoption splits the text into one file per top-level section (the front matter, if any, is `00-front-matter.md`), keeps each footnote with the section that uses it, copies the images that the text uses into `assets/`, writes the document's title, authors, and abstract to `metadata.yaml`, writes the manifest, and writes `mapping.md` in the import record.

Done when the manuscript is adopted into the empty target or staged beside the protected current version, with `mapping.md` in the import record.

## Step 5: Resolve what the mapping names

9. **Citations.** Map the citation keys to `references/bibliography.bib`. LaTeX keys usually match the supplied `.bib` file: add its entries, linking each to its library source ID when the source is in the library. Keys from Word citation fields are the reference manager's identifiers: the import keeps the document's own citation metadata in `references.bib` in the import record; add those entries, or match them to existing entries and change the keys in the text. Never invent a match, and never claim that a cited work's full text is in the library because its entry exists; keys that stay unresolved remain visible in the check.
10. **Conversion details.** A typed number inside a formula, such as `(1)`, is removed and replaced by a label paragraph when the formula is referred to; a hand-written "Figure 1" becomes an `@fig:` reference with a label on the figure; an image in Windows metafile format is often an equation from an old equation editor and needs transcription by the researcher or a checked conversion, never a guess; unconverted LaTeX lines and missing images are reported. These are format repairs: report each one, and change no wording or claim.
11. Run `python scripts/manuscript.py check` and compare the important parts with the original file or its rendered pages: formulas, tables, figures, and the section order. The imported claims are the researcher's text, not verified findings. If the draft language differs from the target paper language, identify translation as remaining work; do not translate during import.

Done when every conversion loss and unresolved citation is recorded; do not invent citation matches or treat the imported claims as verified.

## Step 6: Create the internal logic map

12. After adoption and citation mapping, replace the scaffold or create `logic-map.md` in the adoption target: `manuscript/logic-map.md` for an empty manuscript, or `revisions/<revision-id>/candidate/logic-map.md` for a staged import. Remove the "No manuscript logic map yet" marker and unused placeholder nodes. Follow the [internal logic map guide](../../../docs/logic-map-guide.md). Represent what the imported text states; mark unclear inferences and unchecked or missing support. A citation in the draft is not verified support. Do not infer or change the author's main claim, edit the imported text, or put the map in the manifest. Keep the current manuscript and its map unchanged when staging a candidate.

Done when the map matches the imported text, traces its main claim through the argument sections or marks unclear links, identifies unchecked/missing support, and is not in the target manifest.

## Step 7: Report

13. Report in the interaction language: where the manuscript was adopted or staged, where its logic map was written, the sections, the open decisions (tracked changes, comments, unresolved citations), every loss or uncertain conversion, and the next useful step, such as `manuscript-audit`.

## Completion check

- The original is unchanged in the import record, and the converter and settings are recorded.
- No tracked change was accepted or rejected without the researcher's decision, and comments were not applied.
- An existing manuscript was not replaced; a second version was staged for comparison.
- The internal logic map represents the imported draft's argument without changing it, labels unchecked support and gaps, and is not in the manifest.
- The logic map passes the traceability check in the shared guide.
- Every loss, unresolved citation, and uncertain formula or image is named in `mapping.md` and in the report; nothing was invented to fill a gap.
- Review `python scripts/manuscript.py check`: resolve actual loss or meaning risks, and report other findings as open items when relevant. The command reports findings; a nonzero exit is not a writing judgment.
