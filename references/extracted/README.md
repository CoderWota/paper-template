# Extracted Content

Readable, searchable versions of the original documents, produced with MinerU, or read directly when the original is already Markdown or plain text. One subdirectory per source: `<source-id>/`. Extracted content is derived and can contain errors or omissions, so consequential claims are checked against the original.

## Each source directory contains

```text
<source-id>/
├── README.md         # What this extraction is, its coverage, and known problems
├── document.md       # Readable Markdown with working image links
├── assets/           # Images and other files referenced by document.md
├── provenance.json   # Source ID, checksum, converter and version, settings, mode, time, page coverage, warnings
└── native/           # Parser outputs, kept unchanged for provenance and structured retrieval
```

The agent creates each of these folders with its own README.

## Rules

- A partial extraction stays visibly partial. Unknown page coverage is recorded as unknown, never assumed complete.
- Re-running an unchanged import reuses the matching result. Re-conversion never overwrites notes or reviewed corrections, which are kept separately.
- Mathematics follows the [Markdown conventions](../../docs/markdown-and-export-conventions.md): derived formulas are normalized only when their meaning is preserved, and uncertain formulas are flagged.

## Who edits what

The agent creates and maintains everything here. Read `document.md` freely, but report problems to the agent instead of editing the extraction, so the correction is kept separately and survives re-conversion.

Related skill: `source-ingestion`.
