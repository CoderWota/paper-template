# Import Records

One subdirectory per intake batch, named `<import-id>/` (for example `2026-10-26-thesis-draft`). Each records what was received, where each item went, and what still needs attention, so an interrupted or partial import can be resumed and audited.

## Each import directory contains

- `README.md`: what this batch was, when it was received, and its current state, with one row per input.
- `import.json`: the machine-readable import record that links each input to its checksum, identified role, destination, conversion status, and unresolved items. It is saved after every step, so an interrupted import continues from it. Inputs outside the workspace are recorded with the home folder written as `~`.
- The received originals of an adopted manuscript, once adopting a manuscript is available. Reference documents and formal reviews keep their originals in their own archives instead, so nothing is stored twice.
- `mapping.md`: for an adopted manuscript, the section files made from the document, their counts of words, formulas, images, tables, footnotes, and citations, and what needs a check.
- `references.yaml` and `references.bib`: the citation data that an adopted document carried; use them when a citation key is missing from `references/bibliography.bib`. `metadata.yaml` is kept here only when the manuscript already has its own metadata file.

## Who edits what

The agent creates and maintains these records. You can read them to see what happened to your material; you do not need to edit them. Ask, for example: "What from last week's import still needs my attention?"

Original files kept here are preserved unchanged.
