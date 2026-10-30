# Ingestion Modules

The internals of [`../ingest.py`](../ingest.py), which imports documents with MinerU. The command-line script is the only entry point; agents never call these modules directly, and researchers never need them. Everything here uses only the Python standard library and runs on Python 3.9 or later.

| Module | Responsibility |
| --- | --- |
| [`common.py`](common.py) | Checksums, identifiers, atomic writes, READMEs with a maintained block, the workspace lock, redaction, and the technical log in `.local/logs/`. |
| [`routes.py`](routes.py) | The conversion routes: local MinerU (`mineru-kit` in `.tools/mineru/`), the mineru.net precision API (v4), and direct reading of Markdown and text. No route falls back to another. |
| [`extraction.py`](extraction.py) | Turns raw parser output into `document.md`, `assets/`, and `native/`, and checks page coverage, pages without text, text left out of the Markdown, image links, and math delimiters. |
| [`library.py`](library.py) | The reference library: source IDs from checksums, archived originals, atomic publication, extraction READMEs, `references/index.md`, and `references/bibliography.bib`. |
| [`reviews.py`](reviews.py) | Review rounds in `reviews/<venue>/<round>/`, Word comments and tracked changes, and PDF annotations. |
| [`pdf.py`](pdf.py) | A best-effort PDF page count and annotation scan, without a PDF library. |
| [`records.py`](records.py) | The resumable import record in `inbox/imports/<import-id>/`. |
| [`pipeline.py`](pipeline.py) | Runs an import item by item and saves the record after every change. |

See [document processing](../../docs/mineru-integration.md) for route selection, extraction checks, and operational limits. Use the command's plan and verification modes to inspect actual imports; extraction success does not establish faithful content.
