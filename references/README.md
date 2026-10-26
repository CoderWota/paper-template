# References

The reference library: every source collected for possible use in the manuscript, whether or not it is eventually cited. Original documents, their readable extractions, and interpretation of them are kept apart, so an extraction error never silently replaces the original and a summary is never mistaken for the source.

## Contents

| Path | Role |
| --- | --- |
| [`index.md`](index.md) | Compact discovery list of all sources and their reading status. |
| [`originals/`](originals/README.md) | Archived source files exactly as received. |
| [`extracted/`](extracted/README.md) | Derived Markdown, images, and provenance for reading and search. |
| [`notes/`](notes/README.md) | Interpretation and evidence notes, one per source. |
| `bibliography.bib` | Citation metadata, created with the first imported source. |

Each source has a stable source ID that does not depend on its filename, title, or citation key. The same ID names its folders in `originals/` and `extracted/` and its note in `notes/`.

## Who edits what

- **You** provide documents, reading lists, or identifiers, and can write or correct notes directly.
- **The agent** archives, converts, deduplicates, and indexes sources and maintains citation metadata. You never need to edit BibTeX or the index.

Example requests: "Import all PDFs from this folder into the library, including their images." "Download the available full text from this reference list." "Show me the passages that support this claim."

Related skills: `literature-discovery`, `reference-download`, `source-ingestion`, `literature-and-evidence`.
