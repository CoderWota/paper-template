---
name: manuscript-writing
description: Draft, translate, shorten, or revise manuscript passages, captions, and diagram briefs within the requested scope.
---

# Manuscript writing

Outcome: the requested working draft in its requested language, or publication text in the chosen paper language, consistent with confirmed requirements and actual evidence; claims have checked support or visible gaps, and changes are reported.

## Step 1: Settle the scope

1. A request that names a passage or sentence is a one-time edit: change only that passage. A section draft or a revision of a section is bounded by that section. A change of the central argument, the structure across sections, or the evidence base is a major revision: use `manuscript-revision`.
2. A lasting instruction ("from now on, use ...") is a rule: record it with `constraint-maintenance` first. A one-time request never becomes a rule, and you never save an inferred preference.

When `manuscript-revision` hands off a staged candidate, the text, assets, metadata, manifest, and candidate logic map are in `revisions/<revision-id>/candidate/`. Read the workspace requirements and evidence, and the candidate's outline and map; maintain its graph, reasoning register, and synchronization record as part of the writing task. Apply every text edit and original-copy comparison to candidate files. Use `set-sections --revision-id <revision-id> FILE ...` and `check --revision-id <revision-id>` below; do not change active `manuscript/` files or assemble the candidate. Without that handoff, use `manuscript/`.

## Step 2: Read before writing

3. Read `requirements/project.md` (manuscript language and its exceptions), the rules in `requirements/writing.md` whose scope covers this text, the current section text, and the evidence notes and result records the text will rely on. Read the relevant outline and logic-map entries from the selected target when the edit depends on the section's role, claim, or reasoning; a sentence-level wording edit does not require loading either whole file. Always edit the current file as it is now: the researcher may have changed it since you last read it.
At entry, inspect `python scripts/manuscript.py logic-status [--revision-id ID] --json`. A stale status identifies saved-file changes to inspect, including direct author edits; preserve and reconcile those edits before refreshing the map. Use the [logic map guide](../../../docs/logic-map-guide.md) for the synchronization loop.

4. When a target venue is set, read its AI policy in `research/venues/`. If the venue restricts drafting by an AI, say so before drafting and follow the researcher's decision about how you may help.

When a result relies on code in an imported repository (`code/<name>/`), read [repositories](../research-code-setup/repositories.md) first. Check the method you describe against the code at the recorded commit, and report a mismatch instead of smoothing it over.

Use the researcher's confirmed argument and evidence. When contribution, claim strength, limitations, or venue impact is in scope, read [argument and impact guidance](argument-and-impact.md). Make the argument persuasive by stating the contribution and why it matters; keep empirical, causal, novelty, generalization, and validation claims supported. A request to strengthen the presentation can improve the explanation of value without inflating findings. Explain specific evidence gaps and useful ways to address them. A changed main claim or structure remains the researcher's decision.

## Step 3: Write

5. For a requested edit to existing notes or a working draft, retain that material's language unless the researcher asks to translate it. A new working draft may use the language the researcher requests. For text prepared for publication, use the chosen paper language in the body, headings, abstract, figure and table captions and descriptions, and publication metadata. The working and publication languages can differ. Keep quotations, proper names, and bibliography titles in their original language, and follow confirmed exceptions.
6. Support empirical findings with a citation key from `references/bibliography.bib` whose source ID resolves to an archived original for that exact version and whose support for this claim was checked with `literature-and-evidence`, or a checked result record in `research/results/`. Any uncited paper used to inform manuscript claims, background, interpretation, or structure, including a paper underlying a linked result record, must also have its exact original archived. Abstracts, snippets, service-only text, search records, source notes, and bibliographic metadata alone are not manuscript sources. If a needed original is unavailable, do not use that paper; mark dependent content as an evidence gap (using `[TODO: ...]` where appropriate) and report it. The researcher's confirmed account can establish their own choices or procedures; confirmation alone does not validate an empirical finding. Write an observed but unchecked result as preliminary. Never invent a source, a citation key, a quotation, a number, or a result.
   For original deductions, analyses, interpretations, or judgments, make the premises, analytical operation or warrant, scope conditions, and evaluative criteria explicit and examine whether the conclusion follows at the claimed strength. This argument can support its derived claim without a separate citation for every step. Check external or empirical premises through their sources or results; identify assumptions and value criteria as such. Record substantive derivations in an appropriate result record when needed. Do not report a reasoned judgment as an observed empirical finding.
   If a needed paper is not yet archived, use [reference-download](../reference-download/SKILL.md) for an authorized public original or [source-ingestion](../source-ingestion/SKILL.md) for a researcher-provided document before treating it as unavailable. Follow those skills' access, version-identity, and processing requirements. If acquisition is blocked, report the exact access or authorization gap and continue independent writing without using that paper as a source.
7. When the change involves math, citations, figures, tables, diagrams, or Word output, read the relevant part of [document conventions](../../../docs/markdown-and-export-conventions.md). Never number cross references by hand. Place new figures and their sources in `assets/` beside the selected manuscript manifest.
8. Read the matching part of the [editing guide](editing-guide.md) for translation, shortening, expansion, results passages, captions, diagrams, or a rewrite that needs a literal rendering. A single sentence polish needs only the requested text and applicable rules. Apply a [style preset](style-presets.md) only when chosen for this scope. For a natural prose check or a request to remove formulaic writing, use `natural-prose` and its language patterns; do not load those guides for every edit.
9. Keep the researcher's own text unless the request is to change it. When a requested change would remove or rewrite their wording beyond the request, ask first.

## Step 4: Apply and check

10. When the edit rewrites existing text (a translation, a polish, a shortening, or an expansion), copy the section file to `.tmp/edits/` before you change it.
11. Write the section file. A new section gets its own file (one file per major section at most, or a single file for a short paper); set the manifest's complete ordered section list with `python scripts/manuscript.py set-sections FILE ...`, including the existing sections that remain. The command replaces the list. Never list the outline, logic map, notes, or drafts. The title, authors, and keywords go in `metadata.yaml` beside that manifest, not in a section file (`title:`, `author:` as a list of plain names, `keywords:` as a list). The check, the preview, and every build use that file whenever it exists, and a Word build fails when a declared title, author, or keyword does not reach the Word file. Take them from the researcher; never invent them.
12. Run `python scripts/manuscript.py check`. Resolve actual integrity or output-loss problems in the text you changed: unresolved labels, unknown citation keys, missing images, broken math, or LaTeX commands that the Word route drops. Review warnings as writing guidance; do not change the author's style merely to silence them. When a citation key is missing from the bibliography, add the entry only from a real source: the archived document through `python scripts/ingest.py metadata`, or the metadata of a recorded search result. Never type in bibliographic details from memory.
13. After an edit of existing text, run `python scripts/check_edit.py <copy> <section file>`, adding `--translation` for a translation. Account for every difference it reports: restore what was lost, or tell the researcher why the difference is intended.

Every manuscript write includes the [logic map guide's synchronization loop](../../../docs/logic-map-guide.md), without a separate request. Compare the actual edit with the selected target's graph and reasoning register; update affected premises, analyses, inferences, judgments, criteria, conditions, locations, and dependencies, then inspect their effect on the whole argument. For a wording-only edit, retain the graph after checking meaning. After this semantic comparison, run `logic-record [--revision-id ID] --input <each new dependency>`; retain recorded dependencies or deliberately replace the reviewed list with `--replace-inputs` as the guide specifies, and confirm `logic-status` is current; do not merely renew fingerprints to silence staleness. Update outline links and result `Used by` fields within the authorized scope. If upstream support changed, recheck affected passages and record which scientific choices remain open.

## Step 5: Report

14. Report in the interaction language: what changed and where, which rules were applied, the claims marked `[TODO: ...]` with the evidence they need, the citations used and whether their support was checked, the literal rendering for checking that the editing guide asks for after a translation or rewrite, and anything the researcher should decide. Offer `manuscript-audit` after a substantial draft.

When a correction and recheck were already requested, continue to that recheck rather than offering it again. Match each earlier finding to the actual revision and inspected support, or state why it remains unresolved. A new scientific choice still requires confirmation; retain the original finding so the repair can be assessed.

## Completion check

- The change stays inside the requested scope, and the researcher's own text is kept.
- Empirical findings have checked evidence/results or an explicit preliminary or missing status. Derived claims and judgments have inspectable premises and reasoning, with conditions and criteria stated. Author approval is not empirical or logical validation; nothing was invented.
- Every cited paper and every uncited paper used to inform manuscript content has an archived original for its exact version; `python scripts/literature.py audit-bibliography` passes for the bibliography.
- The text follows the rules for its scope and language: working drafts retain their chosen language; publication text uses the target paper language, including figure and table captions. Review and report relevant facts and warnings from `python scripts/manuscript.py check`; the command does not judge meaning, evidence, or prose quality.
- After every manuscript write, the target's graph and reasoning register were compared with the actual change, updated where needed, and recorded with current `logic-status`; unresolved reasoning remains visible. Internal files stay outside the manifest.
- After an edit of existing text, every difference that `check_edit.py` reported is restored or explained.
- No rule was created from a one-time request or an inference.
