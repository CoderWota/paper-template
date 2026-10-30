---
name: review-ingestion
description: Archive and convert editor or reviewer correspondence by venue and round, retaining comments and change markers.
---

# Review ingestion

Outcome: `reviews/<venue-id>/<round-id>/` holds the received documents in `originals/`, one readable Markdown file per document in `extracted/markdown/` with its images in `extracted/assets/`, and the checks in `extracted/provenance.json`. The researcher gets a short account of the reviewers, items, comments, and tracked changes that were found, and of anything that could not be captured.

## Rules for this skill

- Follow `AGENTS.md`. Review documents are confidential correspondence.
- A Markdown or plain-text letter needs no converter: the script reads it directly on this computer. Install nothing and ask nothing about a route, a tier, or an upload for it.
- For a letter in another format, use the route confirmed in `requirements/privacy.md`. Upload review documents to mineru.net only if the confirmed scope covers editorial and review correspondence; a scope of "published papers" does not. When in doubt, ask, and recommend this computer.
- Keep rounds apart. Importing the same files again must not create a second copy.
- Do not draft, send, or plan a response, and do not edit the manuscript. Responding is a separate task, `review-response`, which starts from this extraction.

## Step 1: Establish the venue and the round

1. Look for the venue, the manuscript identifier, and the round in the documents and in `reviews/`: the journal or conference named in the letter, "first revision", a decision date. Reuse an existing venue folder for the same venue.
2. Ask only when the venue or the round is missing or ambiguous.
3. Identifiers use lowercase letters, digits, and hyphens, for example `example-journal` and `round-1`.
4. Comments from co-researchers, collaborators, coauthors, or supervisors are research feedback, not a review round, even when they look like a review. Do not file them under `reviews/`; they go to `research-feedback`, which files them in `research/feedback/`.

## Step 2: Prepare the route

If every supplied file is Markdown or plain text, skip this step: nothing is converted, so no route, tier, or MinerU installation is needed.

Otherwise settle and prepare the processing route as `source-ingestion` describes in its steps 2 and 3, with the scope check above. A Word letter needs only the flash tier on this computer. A scanned letter needs the basic tier or OCR.

## Step 3: Run the import

```text
python scripts/ingest.py run --route local --tier flash --ocr-mode txt --to reviews/<venue-id>/<round-id> PATH...
```

When every file is Markdown or plain text, leave out `--route`, `--tier`, and `--ocr-mode`; the same command then needs no parser:

```text
python scripts/ingest.py run --to reviews/<venue-id>/<round-id> PATH...
```

The script archives the files, converts them, adds a section to each Markdown file for what the main conversion does not show, and keeps a resumable record in `inbox/imports/<import-id>/`. Continue a stopped import with `python scripts/ingest.py run --import-id ID`.
Write or update that import folder's English README from `import.json` and observed conversion results. The script creates the machine-readable record; the README is agent-authored.

## Step 4: Check what was captured

- **Word files.** The section at the end lists each comment with the text it refers to, its author, its date, and the comment it replies to, and then every insertion and deletion. The main text above it shows the document as if every tracked change had been accepted. Say so whenever the researcher reads the main text.
- **PDF annotations.** They are found by a simple scan of the file, which can miss some and does not find their pages. Say this plainly and point to the original.
- **Reviewer items.** Count the reviewers and the numbered items in each Markdown file, and compare them with the original. Report any difference; never renumber items.
- **Other problems.** Read the warnings for each document in `extracted/provenance.json`, and handle them as `source-ingestion` describes in its step 5.

## Step 5: Describe the round

Write or update the round's README in English from the documents and `extracted/provenance.json`: identify the venue, round, received documents, what the conversion found, and any capture limits. Include the manuscript identifier, version, and decision date only when the letters state them, and link to the document that states each fact. Preserve useful existing text; add nothing that the documents do not state.

## Step 6: Report

Report the venue and round, each document with its reviewers, items, comments, tracked changes, and annotations, what could not be captured, and links to the Markdown files. If the researcher asks for a response, offer `review-response`. If work remains, update `state/current.md`.

## Completion check

- Each supplied file is archived once in this round, and every item, comment, and change that the script found is in the Markdown.
- Anything that could not be captured is reported, not hidden.
- No response was drafted or sent, and the manuscript is unchanged.
- The round README accurately reflects the source documents and extraction record.
