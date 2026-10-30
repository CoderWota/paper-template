# Document Processing with MinerU

Use this guide for import setup or a conversion problem. Reference and review documents use MinerU locally or the official mineru.net precision API v4, as confirmed in `requirements/privacy.md`. The researcher's own editable Word, OpenDocument, or LaTeX manuscript uses local Pandoc instead. Markdown and plain text are read directly.

## Choose and prepare a route

Inspect the computer and run `python scripts/setup_mineru.py check` before recommending local setup. Previously observed local version: MinerU 4.0.12; supported installation range: 4.x, Python 3.10–3.14. Recheck current official requirements before installing. The scripts themselves need only Python 3.9 or later. [Quick start](https://opendatalab.github.io/MinerU/quick_start/).

| Local tier | Intended material | Additional setup |
| --- | --- | --- |
| flash, `--ocr-mode txt` | Text-layer PDFs and editable office documents | No model download; scanned pages yield no text. |
| flash with OCR, or basic | Scans; basic adds layout, table, and formula handling | Basic model bundle was about 0.9 GB; request consent before downloading. |
| standard or advanced | Layouts that need a vision model | Several GB more; at least 16 GB memory recommended. These tiers remain unverified here. |

The parser environment was about 1.4 GB on Apple Silicon. Use `setup_mineru.py install` and `models --tier basic` only after consent. The adapter uses `mineru-kit parse` for the whole document and local model configuration; missing models stop a run rather than silently downloading more. Other documented formats can be attempted through the supported route but stay flagged until checked against originals.

Cloud processing sends documents to mineru.net. Confirm the material scope before using `MINERU_API_TOKEN`, entered through the private credential page. The adapter refuses cloud processing unless the active privacy record names mineru.net; also inspect every batch against the human-readable scope. A scope for published papers does not cover an unpublished draft or reviewer letter.

Service information last inspected on 2026-10-28: the precision API documents 200 MB and 200 pages per file, priority and daily limits, and token expiry. Read current [API documentation](https://mineru.net/apiManage/docs) and [limits](https://mineru.net/apiManage/limit) before relying on access or cost. Its legal pages did not establish training use or retention, and included a broad uploaded-material license. These remain unknown until current terms establish otherwise; see the [privacy source pointers](../.agents/skills/privacy-configuration/sources.md).

No failed route switches to another parser or destination. A changed processing route needs a new scoped decision.

## Import and resume

Use `scripts/ingest.py plan` before an import, `run` for the authorized route, `status` for progress, and `run --import-id ID` to continue interrupted or failed items. Reuse completed items. Changing conversion settings requires `--reconvert`; a hand-edited extraction is protected unless `--overwrite-edited` is explicitly used after preserving the correction in a source note.

The importer archives the original unchanged under a checksum-based source ID, verifies the copy, and stages derived output in `.tmp/` before publication. The extraction contains `document.md`, linked assets, provenance, and local parser-native data. Import records under `inbox/imports/` retain each item's outcome so the assistant can resume without starting over. Parser-native data is local and ignored; originals, notes, and metadata remain separate.

Cloud batches use source IDs rather than research file names, keep signed transfer addresses out of logs, and send the token only to the API origin. The adapter paces submissions and stops on account-wide failures, retaining open work for resumption. Do not upload research material solely to probe connectivity.

## Check and report

Check page coverage, pages without text, omitted prose, image links, formulas, and format/route limitations. A complete extraction is not a guarantee of faithful content. Compare consequential passages, tables, and formulas with the original or retained formula images. Keep corrections in source notes rather than editing generated text that a later conversion replaces.

Review letters retain Word comments, replies, insertions, and deletions separately. PDF annotation extraction is best effort; annotation page locators, Word footnotes/endnotes, and moved text can need manual comparison. Resolve comments and tracked changes before adopting an editable manuscript.

Use `ingest.py metadata` to record only title, author, year, DOI, and other metadata actually inspected in the source; leave unknown fields empty. `references/bibliography.bib` is the canonical bibliography. Matching a registry is not provided by this import route. Keep distinct source versions and relate them only after their identity is checked.

Run `ingest.py verify` and explain every partial, failed, unsupported, or needs-review outcome. Local PDF/Word and cloud PDF with the `vlm` model have prior macOS observations; other combinations and platforms remain subject to the [capability limits](capabilities.md).
