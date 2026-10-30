---
name: research-investigation
description: Investigate a research question or contested claim from sources, examine alternatives, and record supported results and gaps.
---

# Research investigation

Outcome: a concise answer to the researcher's question, with the relevant search/read scope, evidence and locators, competing accounts, limitations, and unresolved work. The researcher owns the scientific question and consequential choices.

## Establish scope

- Read `state/current.md`, `requirements/project.md`, `requirements/privacy.md`, the relevant `requirements/` entries, and `references/index.md`.
- Restate the question internally as a checkable inquiry. Identify terms that could have multiple meanings. Ask one focused question only if ambiguity would materially change the search or interpretation.
- Do not convert the task into ideation, impact assessment, journal choice, a research plan, or manuscript drafting unless the researcher asks. Those are separate capabilities.

## Search and inspect

- Follow the `literature-discovery` order and privacy gates. Record every external search provider, exact query, date, coverage purpose, source identifiers, locators, and limits in `references/searches/`.
- Screen results for direct relevance. Keep abstracts, search snippets, full text, and original-checked passages distinct.
- Follow the `literature-and-evidence` procedure for quotations, source notes, page conventions, extraction revisions, and support status.
- Search enough to answer the scoped question and make the limits visible. Do not claim exhaustive coverage or originality from a finite search.
- Keep API use proportional to the question: start with a bounded result set and retrieve extra pages, relationship pages, and source context only for a stated gap or evidence check. Report known quota, costs, service limits, failures and inaccessible text; do not infer account pricing. Count requests during a planned evaluation, including retries and catalog calls.

## Reason across sources

- Separate established facts in inspected sources from your synthesis, inference, and open hypotheses.
- Compare methods, definitions, materials, populations, versions, and time periods when the source text supports those distinctions.
- For each substantive answer, associate the claim with the specific source version, a checkable locator, access level, and support direction. Do not merge preprints and publications merely because their titles are similar. Explain unchecked correction or retraction status when it could change the answer.
- Look for contrary findings and alternative explanations. Do not suppress a disagreement because one result is newer, cited more often, or more convenient.
- State when evidence is indirect, abstract-only, provider-snippet-only, based on an unchecked extraction, or unavailable.
- If a requested conclusion is unsupported, say what the inspected material establishes and what further source or analysis would be needed. Do not invent experiments, data, results, or a literature gap.
- If the evidence challenges the working explanation, first check extraction, definitions, source versions, and the actual passages. Show what supports retaining the explanation, what calls for narrowing or revising it, and what remains undecidable, only where the evidence warrants those alternatives. A changed main claim or material scope goes back to the researcher; do not change it to make the investigation look complete.

## Record a project result

When the researcher asked for the investigation as research work whose finding the paper will report, such as a documentary or archival comparison, a coded analysis of sources, a derivation, or a proof, write a result record with the layout in `research/results/README.md` and add it to `research/results/index.md`:

- `Kind`: documentary, qualitative, theoretical, or other.
- `Inputs`: source IDs with locators, search records, or files with checksums.
- `Method`: the procedure or the argument, with enough detail to repeat it.
- `Checks`: what was actually checked, such as passages verified against the originals, a search for counterevidence, a second reading, or a check of each step of a derivation, and what it found.
- `Status`: the one that matches what was done; a result whose checks are still open is observed, not checked.

A quick question that needs only an answer gets no result record. Computational work goes through `research-code-setup`. Run `python scripts/research.py check` after writing.

## Report

Use the interaction language. Organize the response around the question, not a generic article outline. Include citations or links to the workspace sources and precise locators wherever available. Separate the supported answer, sources that qualify or disagree, and remaining uncertainty. Keep a durable interpretation in the relevant per-source evidence notes; do not save the whole conversation or a new unconfirmed research decision.

For a project result, keep the observation, interpretation, and open hypothesis distinct in its narrative, with the checks and limitations beside them. Name the next discriminating check or necessary researcher judgment. Pass the result and evidence locators, contrary findings, and unresolved questions to already-authorized planning or writing work; do not expand an answer-only request. Use the existing result's `Used by` field for dependent passages and exhibits, and recheck them when the underlying evidence changes.

## Completion check

- Each consequential conclusion points to inspected evidence and an accurate locator.
- Search scope and what was actually read are clear.
- Contradictory evidence and limitations are visible.
- No source result is reported beyond what the source supports.
- Research decisions remain with the researcher.
- A project result, when the work produced one, has a result record whose status matches the checks actually made.
