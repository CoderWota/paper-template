---
name: source-ingestion
description: Import reference documents or organize the inbox with the confirmed MinerU route; route drafts and review letters separately.
---

# Source ingestion

Outcome: every requested document has a status. A converted source has its original in `references/originals/<source-id>/`, readable Markdown with working images in `references/extracted/<source-id>/`, a row in `references/index.md`, and citation metadata read from the document. The researcher gets a short report with counts and links. A finished conversion is not a claim that the text, tables, or formulas are correct.

## Rules for this skill

- Follow `AGENTS.md`. The processing route comes from `requirements/privacy.md` (step 2). When a route fails, report the failure: another route or another parser needs a new choice by the researcher.
- `scripts/ingest.py` does the archiving, conversion, checks, records, index, and bibliography. Never copy files into `references/` by hand, and never edit `index.md`, `bibliography.bib`, a `document.md`, or a `provenance.json` yourself.
- Never change, move, rename, or delete the researcher's input files, in `inbox/` or anywhere else, and add no files to their folders.
- Do not upload research material merely to check connectivity. Use a non-uploading check, or leave access unverified until the authorized import.
- Keep the technical output of the script in the background. Report results in the researcher's terms, with links.

## Step 1: Identify the material

1. Find what the researcher means: named files, a folder, or `inbox/`. When a folder has subfolders and the request does not say whether they count, include them only after you say so in one sentence; use `--recursive` to include them.
2. Run the plan, which changes nothing:

   ```text
   python scripts/ingest.py plan [--route local|cloud] [--recursive] PATH...
   ```

   It lists each file as to convert, already imported, duplicate, not supported, or needing a processing route.
3. Mixed material, for example in `inbox/`: look at each file that is not obviously a reference source (its name and its first page) and decide its role. Ask only about a role that you cannot tell.

   | Role | Where it goes |
   | --- | --- |
   | Reference source (an article, book, report, or dataset description) | This skill |
   | Editor or reviewer correspondence | `review-ingestion` |
   | Advice from co-researchers, collaborators, coauthors, or supervisors | `research-feedback` |
   | The researcher's own manuscript draft | `manuscript-import` |
   | A journal template or its author guidelines | `submission-assembly`, which keeps them in the output profile |
   | Anything else that is not a reference source | Keep the file where it is and record it with `python scripts/ingest.py note --import-id ID --role other --reason "..." PATH`, so that it stays visible. Never add a draft to `manuscript/manifest.yaml`. |

4. Tell the researcher in one short message how many files will be imported and with which processing route. Routine steps inside a confirmed scope need no further approval.

## Step 2: Confirm and prepare the route

Read the applicable choice in `requirements/privacy.md`. Markdown and text are read directly. For other documents, read the route-selection section of [the import guide](import-guide.md) before choosing or preparing a parser. Reuse a choice that covers this batch; confirm only a missing or changed scope. Do not load environment or privacy skills unless this import needs their setup or decision.

## Step 3: Import, review, and record metadata

Follow the run section of [the import guide](import-guide.md): use `run --import-id ID` for continuation and retain completed items. Read its review section for partial or needs-review output, and its metadata section when recording bibliographic fields. Preserve author corrections in notes before any explicitly authorized overwrite. Conversion alone does not verify a formula or source claim. After the batch, write or update `inbox/imports/<import-id>/README.md` in English from `import.json` and the observed results; preserve prior notes and do not invent details.

## Step 4: Report

- Report how many documents were converted, were already imported, need a check, failed, or are not supported, with links to the agent-written import README and to the extraction README of each item that needs attention. Say plainly that a converted document can still contain errors, and name the one useful next step.
- If work remains, such as failed items, a deferred token, or files kept for a capability that is not available yet, update `state/current.md`.

## Completion check

- Every requested file has a status in the import record. Nothing was skipped without a recorded reason.
- The originals are unchanged, and the input folders hold exactly what they held before.
- No route or parser was switched. Cloud uploads stayed inside the confirmed scope, and nothing was uploaded as a test.
- Citation metadata comes from the document and is marked as such.
- Review facts from `python scripts/ingest.py verify`. Inspect created directory descriptions for missing or broken material links and disclose other findings.
