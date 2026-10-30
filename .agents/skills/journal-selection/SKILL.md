---
name: journal-selection
description: Compare target venues using current official scope, policies, format limits, costs, and relevant publications.
---

# Journal selection

Outcome: an examination of a named venue, or a comparison of several, in `research/venues/`: fit with the paper's question, article type, evidence, and audience; requirements that affect the writing (article type, length, structure, AI use, data, code, and reporting policies); costs and access; and conditions or risks. Every fact has a dated official source. The researcher's chosen target is recorded only after confirmation.

## Step 1: Prepare

1. Read `requirements/project.md` (question, contribution, article type, language, audience, any target), `research/venues/index.md` and the existing venue notes, `research/impact.md` if it exists, and `state/current.md`.
2. Collect the candidates and say where each came from: named by the researcher, the venue of inspected related work (`references/index.md`, search records), or a search for venues in the field. When the researcher named no candidates, propose a small set and explain the basis.
3. Reading public venue pages sends only addresses and search terms to the web. Use venue names and general field terms in searches; never put unpublished manuscript text or unpublished results into a query.

## Step 2: Read the current official sources

4. For each venue, read the official pages through the agent application's web access: aims and scope, article types, author guidelines (length, structure, abstract, references, figures, supplementary material), the policy on AI use, data, code, and reporting policies, open-access options and fees, the review model, and language requirements. Record each address and the date you read it.
5. If a page cannot be read, say so, and record the fact as unchecked. Knowledge from memory or training data is not a source: never fill a requirement from it without labeling it unchecked.
6. When accessible, inspect a few recent publications in the venue that are close to the topic: their article types, length, approach, and evidence. They show what the venue publishes; they are not evidence for the paper's claims.
7. Record the AI-use policy carefully: what the venue permits, restricts, or requires to be disclosed. If it restricts drafting by an AI agent, say so clearly; it governs how `manuscript-writing` may help with this paper.

## Step 3: Assess fit separately

8. For each venue, assess fit with reasons tied to the sources: scope, article type, kind of evidence, audience, and the requirements that would need work. Keep fit apart from impact (`impact-assessment`) and from the readiness of a manuscript (`submission-readiness`). Do not rank by prestige or a metric alone; when the researcher cares about a metric, report the official figure with its source and date.
9. Never state or imply an acceptance probability for this paper. A published acceptance rate is the venue's statistic, not this paper's chance; report it only as such, with its source.
10. For a comparison, use the same criteria for every venue in `research/venues/index.md`. Recommend a target or a shortlist with the reasons and the conditions, then ask one question about the choice.

## Step 4: Record

11. Write or update `research/venues/<venue-id>.md` with the layout in `research/venues/README.md`, and update `research/venues/index.md`. Use the interaction language; quotations keep their original language.
12. Choosing or changing the target venue is a major decision. After a clear yes, record it with `constraint-maintenance`: the target in `requirements/project.md` and a decision record. The venue's formatting rules become an output profile through `submission-assembly`; follow the availability table in `AGENTS.md`.
13. Run `python scripts/research.py check` and fix every problem in the files you wrote.

## Completion check

- Every requirement and policy has an official source with its address and reading date, or is labeled unchecked.
- Fit, impact, and readiness are kept apart, and no acceptance probability appears.
- The AI-use policy of each examined venue is recorded, with its consequence for drafting.
- The target is recorded only after the researcher's clear confirmation.
- The check reports no problem in the venue notes.
