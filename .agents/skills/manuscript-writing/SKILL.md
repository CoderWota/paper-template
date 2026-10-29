---
name: manuscript-writing
description: Use when the researcher asks to draft, write, rewrite, expand, shorten, polish, or revise manuscript text, a section, a paragraph, or a sentence, or to insert recovered or supplied text. Writes in the manuscript language against the confirmed outline, the writing rules in force for that scope, and the actual evidence and results, follows the workspace's math, figure, citation, and cross-reference conventions, keeps the researcher's own edits, marks claims that still need evidence instead of inventing support, and checks the result.
---

# Manuscript writing

Outcome: the requested text in the manuscript, written in the manuscript language, consistent with the confirmed requirements and the actual evidence; every claim either cited to checked support or marked as needing evidence; and a short report of what changed and what is open.

## Step 1: Settle the scope

1. A request that names a passage or sentence is a one-time edit: change only that passage. A section draft or a revision of a section is bounded by that section. A change of the central argument, the structure across sections, or the evidence base is a major revision: use `manuscript-revision`.
2. A lasting instruction ("from now on, use ...") is a rule: record it with `constraint-maintenance` first. A one-time request never becomes a rule, and you never save an inferred preference.

## Step 2: Read before writing

3. Read `requirements/project.md` (manuscript language and its exceptions), the rules in `requirements/writing.md` whose scope covers this text, `manuscript/outline.md`, the current text of the section file, and the evidence notes and result records the text will rely on. Always edit the current file as it is now: the researcher may have changed it since you last read it.
4. When a target venue is set, read its AI policy in `research/venues/`. If the venue restricts drafting by an AI, say so before drafting and follow the researcher's decision about how you may help.

## Step 3: Write

5. Write natural prose in the manuscript language. Keep quotations, proper names, and bibliography titles in their original language, and follow the confirmed exceptions; avoid unintended mixing of languages.
6. Support every substantive claim with one of: a citation key from `references/bibliography.bib` whose support for this claim was checked with `literature-and-evidence`; a result record in `research/results/` whose status is checked; or the researcher's confirmed statement. Write an observed but unchecked result as preliminary. When no support exists, keep the claim only as a visible marker in the manuscript language, `[TODO: ...]`, naming the evidence needed. Never invent a source, a citation key, a quotation, a number, or a result.
7. Follow the [conventions](../../docs/markdown-and-export-conventions.md): `$...$` and `$$` math; equation labels as a separate `{#eq:id}` paragraph after a blank line; figures `![Caption](assets/name.png){#fig:id}`; table captions `: Caption {#tbl:id}`; Mermaid diagrams in a `mermaid` block, with `: Caption {#fig:id}` after it when they are numbered figures; citations `[@key]` and `@key`; references `@fig:id`, `@tbl:id`, `@eq:id`, `@sec:id`. Never number figures, tables, equations, or citations by hand. Put new figures and their sources in `manuscript/assets/`.
8. Keep the researcher's own text unless the request is to change it. When a requested change would remove or rewrite their wording beyond the request, ask first.

## Step 4: Apply and check

9. Write the section file. A new section gets its own file (one file per major section at most, or a single file for a short paper); add it to the manifest in the outline's order with `python scripts/manuscript.py set-sections FILE ...`. Never list the outline, notes, or drafts.
10. Run `python scripts/manuscript.py check` and fix every problem in the text you wrote: unresolved labels, unknown citation keys, missing images, broken math. When a citation key is missing from the bibliography, add the entry only from a real source: the archived document through `python scripts/ingest.py metadata`, or the metadata of a recorded search result. Never type in bibliographic details from memory.

## Step 5: Report

11. Report in the interaction language: what changed and where, which rules were applied, the claims marked `[TODO: ...]` with the evidence they need, the citations used and whether their support was checked, and anything the researcher should decide. Offer `manuscript-audit` after a substantial draft.

## Completion check

- The change stays inside the requested scope, and the researcher's own text is kept.
- Every substantive claim is supported by checked evidence, a checked result, or the researcher's statement, or is visibly marked as needing evidence; nothing was invented.
- The text follows the rules in force for its scope, the manuscript language, and the workspace conventions; `python scripts/manuscript.py check` reports no problem in it.
- No rule was created from a one-time request or an inference.
