# References

The reference library: every source collected for possible use in the manuscript, whether or not it is eventually cited. Original documents, their readable extractions, and interpretation of them are kept apart, so an extraction error never silently replaces the original and a summary is never mistaken for the source.

Before a paper is cited or used to inform manuscript claims, background, interpretation, or structure, archive the original document for that exact version under [`originals/`](originals/README.md) with its source ID. Search records, abstracts, snippets, Sciverse content, source notes, and bibliography metadata alone do not count as archived sources. If the original cannot be obtained through an authorized route, record the access gap and do not use the paper as a manuscript source.

## Contents

| Path | Role |
| --- | --- |
| [`index.md`](index.md) | Compact discovery list of all sources and their reading status. |
| [`originals/`](originals/README.md) | Archived source files exactly as received. |
| [`extracted/`](extracted/README.md) | Derived Markdown, images, and provenance for reading and search. |
| [`notes/`](notes/README.md) | Interpretation and evidence notes, one per source. |
| [`searches/`](searches/README.md) | Provider-specific literature search records and source locators. |
| [`downloads/`](downloads/README.md) | Resumable reference-acquisition records and access outcomes. Retrieved files remain in `originals/`. |
| `bibliography.bib` | Citation metadata in BibTeX, created when the first source's details are recorded. Each entry names its source ID; details read from the document itself are marked as not yet checked against a registry. |

Each source has a stable source ID that does not depend on its filename, title, or citation key: `src-` followed by the start of the original file's SHA-256 checksum. The same file always gets the same ID, and another version of a work, such as a preprint and the published article, gets its own. The same ID names its folders in `originals/` and `extracted/` and its note in `notes/`.

## Who edits what

- **You** provide documents, reading lists, or identifiers, and can write or correct notes directly.
- **The agent** archives, converts, deduplicates, and indexes sources and maintains citation metadata. You never need to edit BibTeX or the index.

Example requests: "Import all PDFs from this folder into the library, including their images." "Download the available full text from this reference list." "Show me the passages that support this claim."

Related skills: `literature-discovery`, `reference-download`, `source-ingestion`, `literature-and-evidence`.
