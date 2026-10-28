---
name: literature-and-evidence
description: Use when the researcher asks what selected literature supports, where a claim is supported, how sources agree or conflict, or whether a passage needs evidence. Retrieves a small set of matching passages, checks locators against available originals, and records interpretations separately from source text.
---

# Literature and evidence

Outcome: a compact, source-linked comparison that distinguishes direct support, contradiction, qualification, no support found, and not checked. A citation key resolving in the bibliography does not establish support.

## Retrieve only relevant material

1. Read `state/current.md`, `references/index.md`, the specific matching source notes, and the relevant extraction READMEs. Open only the sources needed for the question.
2. If the sources are unclear, run `python scripts/literature.py search-local --query "..."` and narrow with `--source-id`. The search is lexical over extracted Markdown; line numbers identify the extraction revision, not the PDF page.
3. Inspect matching sections in `references/extracted/<source-id>/document.md`. Then verify important passages against the original PDF or another trustworthy source locator when available. MinerU output and Sciverse text are derived/service text; note when the original could not be checked.
4. For a Sciverse hit, preserve `doc_id`, `chunk_id`, `offset`, and `page_no` when present. A returned `chunk` is a search snippet. If the full text is available through Sciverse `content`, retrieve it only through the recorded search result while its confirmed query scope remains active; record the character offset and retrieved range. Do not call a snippet a full article.

## Record evidence without altering the source

Create or update `references/notes/<source-id>.md` in the interaction language. Preserve existing researcher-authored content. Keep quotations verbatim and attributed, and do not edit the archived original or generated `document.md`.

For each passage needed to answer the question, record:

- the claim or question it bears on;
- a short exact quotation or a clearly labeled paraphrase;
- source ID and the locator as printed in the original, if present;
- PDF page index (1-based, as counted in the file) separately from any printed page label;
- section, table, figure, or paragraph details where available;
- extraction revision or Sciverse provider/chunk/offset identifiers when those are the locator;
- whether the original was checked, only an extraction was checked, only an abstract/snippet was available, or the passage was not checked;
- scope, design, population/material, uncertainty, and limitations relevant to the claim;
- evidence direction: supports, contradicts, qualifies, or does not address.

Never convert an absent page number, printed label, DOI, quote, or result into a guessed value. Block/chunk IDs belong to their extraction or provider revision. After a re-extraction, recheck old block locators before calling them verified; do not carry them forward silently.

## Compare and answer

- Compare what each inspected source says, its scope, and its limitations. Name unresolved contradictions and differences in population, method, definitions, or version when the documents establish them.
- Separate exact source statements, your synthesis, and unverified interpretations. An abstract-only record cannot support a claim about uninspected full-text results.
- State the search/read scope and gaps. “No support found in the inspected sources” does not mean “no evidence exists.”
- Use `python scripts/literature.py audit-bibliography` when checking that BibTeX entries resolve to archived sources. Report this separately from whether the sources support a manuscript claim.
- Do not write to `manuscript/` unless the researcher asked for a manuscript edit. If they did, follow the manuscript-writing capability status in `AGENTS.md`.

## Completion check

- Every quoted passage is exact and each locator is checkable at the level stated.
- Support, contradiction, qualification, uncertainty, and source-access limits remain distinct.
- Full-text status and extraction revision are explicit.
- No reference, locator, result, conclusion, or support relationship was invented.
