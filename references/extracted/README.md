# Extracted Content

Readable, searchable versions of the original documents, produced with MinerU, or read directly when the original is already Markdown or plain text. One subdirectory per source: `<source-id>/`. Extracted content is derived and can contain errors or omissions, so consequential claims are checked against the original.

## Each source directory contains

```text
<source-id>/
├── README.md         # What this extraction is, its coverage, and the problems the checks found
├── document.md       # Readable Markdown with working image links
├── assets/           # Images referenced by document.md, and pictures of transcribed tables and formulas
├── provenance.json   # Source ID, checksum, converter and version, settings, route, time, page coverage, checks, warnings
└── native/           # The parser's own output files; on this computer only, not in version history
```

The agent creates each of these folders with its own README, using `scripts/ingest.py`. A new conversion replaces the folder in one step and records the revision; text added to a README outside its maintained block is kept.

## Rules

- A partial extraction stays visibly partial. Unknown page coverage is recorded as unknown, never assumed complete.
- Re-running an unchanged import reuses the matching result. Re-conversion never overwrites notes or reviewed corrections, which are kept separately.
- The parser's own output in `native/` stays on this computer. It is not saved in version history or in Git backups (see `.gitignore`): the paper does not need it and nothing in the workspace reads it. The README of that folder lists the files, and `provenance.json` records the parser and settings that made the text. Importing the document again creates the files anew.
- Mathematics follows the [Markdown conventions](../../docs/markdown-and-export-conventions.md): derived formulas are normalized only when their meaning is preserved, and uncertain formulas are flagged.

## Who edits what

The agent creates and maintains everything here. Read `document.md` freely, but report problems to the agent instead of editing the extraction: the correction is kept in the source note, `../notes/<source-id>.md`, and survives re-conversion. A hand-edited `document.md` is never overwritten without being noticed.

Related skill: `source-ingestion`.
