---
name: reference-download
description: Obtain public full-text PDFs from DOI or URL lists, BibTeX, or a bibliography; record identity checks and unavailable items.
---

# Reference download

Outcome: every requested reference has a status and any retrieved full text stays archived, even if later conversion fails. A metadata result or publisher page is not a downloaded document. Do not bypass access controls or promise that every item is obtainable.

## Scope and supported route

The script supports public PDF responses from a DOI resolver or a direct HTTP(S) URL. It reads BibTeX, Markdown, and text lists containing DOI or URL identifiers. For manuscript bibliographies, inspect the actual bibliography and extract only identifiable DOI/URL items; do not guess from a title. Other formats and authenticated access are not claimed as supported by this integration.

Read `references/README.md`, `references/index.md`, `requirements/privacy.md`, and the source-ingestion skill before work that will continue to conversion. A download request authorizes retrieval of the named public URLs. It does not authorize uploading a downloaded file to MinerU or another parser. The existing document-processing scope still governs conversion.

## Run a batch

For a BibTeX or list file, or a short set of identifiers:

```text
python scripts/literature.py download path/to/references.bib
python scripts/literature.py download 10.1234/example https://repository.example/paper.pdf
```

The command archives valid PDFs under `references/originals/<source-id>/`, identifies exact duplicates, and creates `references/downloads/<batch-id>/batch.json` and a human-readable README. It stores retrieval dates and URLs with query parameters removed. The fixed integration currently limits one download to 500 MiB, retrieves one item at a time, follows normal web redirects, and does not use institutional cookies or credentials.

Every item remains distinct: downloaded, existing/duplicate, metadata-only, login/manual-access-needed, unavailable, rate-limited, or failed. HTML login/error pages are not saved as PDFs. A status of `downloaded` means the bytes passed the PDF-signature check; it does not verify the requested edition. Read available document metadata using an already confirmed local or cloud route, compare title/author/DOI/version with the requested record, then record the result:

```text
python scripts/literature.py verify-download BATCH_ID 1 --identity match --evidence "The title and DOI on page 1 match the requested record."
```

Use only a result supported by the file: `match`, `version-different`, `uncertain`, or `mismatch`. If a downloaded PDF cannot be inspected under the current processing scope, keep identity uncertain and explain the gap. A version difference creates a related source; it does not replace or merge the other version.

Continue an interrupted batch without repeating finished items:

```text
python scripts/literature.py download --batch-id BATCH_ID
```

HTTP 429 items remain rate-limited; retry them only after the provider limit resets:

```text
python scripts/literature.py download --batch-id BATCH_ID --retry-rate-limited
```

## Import only when requested

If the researcher asks to import the acquired papers, use the existing `source-ingestion` skill on the archived originals. Do not implement conversion here. Confirmed parser scope, route failures, and cloud-upload boundaries still apply. If conversion fails, leave the archived PDF and successful download record intact; resume only the failed conversion in the ingestion record.

## Report

Report item counts by status, source IDs for archived items, unresolved identity/version checks, login/manual access gaps, service limits, and links to the batch record. Distinguish download success from conversion success and full-text reading. The script does not prove access through a publisher or institution; do not claim that an untested integration works.
