# MVP 3 Acceptance Checklist

Status: prepared on 2026-10-28. It has not been run. Do not copy this checklist into a researcher workspace; it contains expected outcomes.

The checklist covers the acceptance evidence in the [MVP implementation guideline](../mvp-implementation-guideline.md#mvp-3--searchable-literature-and-traceable-evidence). Use a disposable test copy and rights-cleared fixtures. Record the host, version, model, operating system, processor, date, Sciverse account state, and whether each step used a simulated or live service. A simulated download does not prove publisher or institutional access.

## A. Query scope and provider order

1. Fresh copy with no Sciverse query-sharing choice or key. Ask for literature discovery.
   - The agent explains that query text and identifiers go to OpenDataLab Sciverse and asks for a bounded scope before a request.
   - It requests neither an account nor a key before the scope is confirmed.
   - `requirements/privacy.md` remains unchanged until confirmation.
2. Confirm a scope. Verify that the exact confirmation and scope are recorded in the interaction language. Add a synthetic key through private entry; inspect no output or record for the value.
   - An in-scope query succeeds only when its exact scope excerpt is recorded; an excerpt absent from the active approval is rejected. A query outside the approved scope uses a permitted fallback or waits for a new confirmation.
   - The official Sciverse API runs first when available and within scope.
   - Its record keeps provider, endpoint, query, date, document IDs, chunk IDs, offsets/pages, returned metadata, and limits. A returned chunk is labeled a snippet.
   - An exact title/DOI request uses the Sciverse metadata endpoint and records metadata as metadata-only, not as an evidence passage.
3. Make the Sciverse route unavailable, unconfigured, outside scope, or return HTTP 429 in a controlled test.
   - The agent reports the exact limitation and uses built-in search only when that provider is inside the confirmed scope.
   - Built-in search is recorded as a distinct provider with the gap/cross-check it addressed.
   - Omitting the host-search query or coverage note is rejected; each provider pass records its own query and timestamp, including when the secondary query differs from Sciverse.
   - No Sciverse result is silently described as available or exhaustive.
4. Request full text for a known Sciverse result. Verify that the recorded context preserves `doc_id` and offset and remains distinct from the initial search snippet.

## B. Local passage retrieval and evidence

1. Use a small known corpus with one supporting passage, one contradictory passage, an abstract-only item, and an unsupported claim.
   - Local retrieval returns the correct source IDs, extraction revisions, and Markdown line locators without loading the whole library into the conversation.
   - It never labels a Markdown line as a PDF page.
2. Compare the passages with their originals.
   - Notes quote only text present in the source, separate PDF page index from printed page label, and preserve extraction revision/block or provider locators.
   - The answer distinguishes support, contradiction, qualification, no support found in the inspected scope, and not checked.
   - Abstract-only and snippet-only items are not used as full-text evidence.
3. Re-extract one source and check its prior block locator.
   - The agent rechecks it; an old locator is not silently reported as verified.
4. Run `audit-bibliography` against a BibTeX bibliography containing a valid source ID, a duplicate key, a missing source ID, and a missing original.
   - Key/source resolution errors are reported separately from whether any source supports a claim.

## C. Batch download and handoff

Use a rights-cleared local HTTP fixture server or a small set of explicitly public references. Include a valid PDF, an exact duplicate, a different version, an HTML login page, an unavailable URL, an interrupted transfer, and a file that later fails conversion.

- Valid PDF bytes are archived unchanged under a checksum-based source ID. HTML login/error pages are not archived as successful PDFs.
- The retrieval batch records the DOI/request URL, sanitized final URL, retrieval date, checksum, source ID, outcome, and identity status, without query secrets or credentials.
- Identity/version is compared with visible document details; uncertain or different versions stay explicit and are not merged.
- Exact duplicates are not downloaded twice. A preprint and publication remain separate sources.
- A stopped batch resumes pending or failed items while preserving finished items. HTTP 429 is not retried until the limit resets.
- Download-only keeps files in the reference library. Download-plus-import calls the existing `source-ingestion` flow, never a second converter.
- A conversion failure leaves the downloaded source and retrieval record intact. Download permission does not authorize a cloud parser upload.
- Status distinguishes downloaded, existing/duplicate, metadata-only, login/manual-access-needed, unavailable, rate-limited, and failed.

## D. Mechanical checks and limits

On the test copy, run:

```text
python scripts/literature.py audit-bibliography
python scripts/ingest.py verify
python scripts/check_readmes.py
python scripts/sync_skills.py --check
python scripts/check_capabilities.py
```

Inspect that query records, download batch folders, and any new source folders have useful English READMEs. Do not report that real publisher/institution integrations work based on a local fixture. Do not claim complete literature coverage or novelty.

## Results

No scenarios have been run. Sciverse API account availability, a live query, full-text access, public publisher/repository access, interruption/resumption, conversion handoff, Windows, and Codex remain unverified.
