# MinerU Integration

Status: integration decided by the template maintainer on 2026-10-28 and implemented in MVP 2. The local route was observed working on macOS; the mineru.net route is implemented against its documentation and tested only with a fake service. For what is verified, see [implementation status](implementation-status.md#mvp-2-flexible-intake-and-mineru-batch-ingestion).

This note records the read-only MinerU research that [design plan Section 5](design-plan.md#5-document-ingestion-mineru-decision-and-publishing-options) asked for, the integration decisions, and the behaviour observed in this workspace. Sources were read on 2026-10-28; versions and terms change, so check them again before relying on a detail.

## Decisions (2026-10-28)

The maintainer answered three questions:

1. **Routes.** The adapter supports both MinerU on this computer and the official cloud service, mineru.net (precision API v4). The token-free "Agent" API is not used: it accepts at most 10 MB and 20 pages and returns Markdown without images. Each researcher's confirmed processing choice selects one route; a failure is never retried on the other route.
2. **Local test installation.** MinerU 4.0.12 was installed into the worktree's ignored `.tools/mineru/` and tested with the flash and basic tiers on synthetic fixtures. The standard tier was not tested: it needs a vision model of several gigabytes, and the vendor recommends at least 16 GB of memory, which is what the test computer has.
3. **Citation metadata.** `references/bibliography.bib` (BibTeX) is the canonical citation metadata from now on, before the export trial. Pandoc and Quarto both read BibTeX, and the export trial was planned with BibTeX input. If the trial chooses another representation, the bibliography is migrated once.

The planned order put MVP 7 (Git) and the export trial before MVP 2. The maintainer asked for MVP 2 first on 2026-10-28.

## MinerU 4

| Fact | Value | Source |
| --- | --- | --- |
| Current version | 4.0.12 (`mineru>=4.0,<5`) | [PyPI](https://pypi.org/project/mineru/), [quick start](https://opendatalab.github.io/MinerU/quick_start/) |
| Python | 3.10 to 3.14; the workspace scripts themselves need only 3.9 | quick start |
| Package size observed | 1.06 GB in `.tools/mineru/` when installed with uv, and 1.37 GB with pip through `scripts/setup_mineru.py install`, on Apple Silicon, where it pulls in PyTorch | this workspace |
| License | Apache 2.0 with additional terms: a separate license above 100 million monthly users or USD 20 million monthly revenue, and attribution for online services built on MinerU. Model weights are not mentioned. The template does not redistribute MinerU or its models. | [LICENSE.md](https://github.com/opendatalab/MinerU/blob/master/LICENSE.md) |
| Entry point used | `mineru-kit parse`, which converts every PDF page by default. `mineru parse` stops after ten pages by default and is not used. | [quick start](https://opendatalab.github.io/MinerU/quick_start/) |

### Tiers on this computer

| Tier | What it does | Needs | Observed |
| --- | --- | --- | --- |
| flash, `--ocr-mode txt` | Reads the PDF text layer; converts Word, PowerPoint, Excel, OpenDocument, RTF, EPUB, HTML, and CSV as whole documents | No models | 12-page PDF in 15 s. A scanned page yields no text. Some lines at the top of a page were classified as headers and left out of the Markdown. Word tracked changes appear as accepted, and comments are lost. |
| flash, `--ocr-mode auto` | Also OCRs pages without text | The small-model bundle for scanned pages | With the models, the scanned page was read. Without them, the scanned PDF failed with "Model repo MinerU-4_models_torch is not ready". |
| basic | Layout, OCR, table, and formula models | Small-model bundle, 854 MB observed | 12-page PDF in 53 s including model loading. Headings and the table were structured; the scanned page was read; one printed formula was transcribed wrongly and a formula image was merged into it. |
| standard, advanced | Add a vision-language model | Several GB more, 16 GB or more of memory recommended | Not tested |

Models are downloaded only on request (`mineru-kit models download --tier basic`). `scripts/setup_mineru.py` keeps MinerU's configuration and models in the ignored `.cache/mineru/`, and the adapter sets `MINERU_MODEL_SOURCE=local` while parsing, so a missing model stops the run instead of starting a download that nobody agreed to.

### Output contract observed

`mineru-kit parse --format zip` writes one archive per input with `markdown.md`, `middle_json.json` (schema `docvortex.middle` 2.0), `structured_content.json`, `model_output.json`, and `images/page_<page>_<type>_<n>.jpg`. The Markdown links images as `images/...`. Page indexes in the JSON count from 0. The middle JSON records each page's blocks with their types (`header`, `page_number`, `text`, `table`, `equation`, `image`, and others), the physical page count, and `is_full_document`. MinerU keeps a picture of every table and formula that it transcribes; these pictures are not linked from the Markdown. See the [output reference](https://opendatalab.github.io/MinerU/reference/output_files/).

## mineru.net

| Topic | Finding (2026-10-28) |
| --- | --- |
| API | Precision API v4 with a token: `POST /api/v4/file-urls/batch` returns a batch ID and one signed upload address per file; each file is uploaded with `PUT` and no content type; `GET /api/v4/extract-results/batch/{batch_id}` reports `waiting-file`, `pending`, `running`, `converting`, `done`, or `failed`, and a `full_zip_url` when done. The archive holds `full.md`, `layout.json` (middle JSON), `*_model.json`, `*_content_list.json`, and the images. Options used: `model_version` (`vlm`, which MinerU recommends, or `pipeline`), `language`, `enable_formula`, `enable_table`, and `is_ocr`. See the [API documentation](https://mineru.net/apiManage/docs). |
| Limits | 200 MB and 200 pages a file; 1000 pages a day at full priority; 50 submitted files a minute and 5000 a day; no paid plan at present ([rate limits](https://mineru.net/apiManage/limit)). |
| Errors | `A0202` token error and `A0211` expired token; `-60018` daily limit; `-60009` queue full; `-60005` and `-60006` file too large or too long; others in the documentation's table. |
| Token | Created by the user on the [API management page](https://mineru.net/apiManage/token); tokens can expire. |
| Data use | The legal pages linked from mineru.net are OpenDataLab's general privacy policy and service agreement of 2022. They do not name MinerU and do not say whether uploaded documents are used for training or how long they are kept, and the agreement grants the operator a perpetual license to uploaded material. Training use and retention are therefore **unknown**. Details are in [privacy-configuration/sources.md](../.agents/skills/privacy-configuration/sources.md). |

How the adapter uses it:

- It runs only when `requirements/privacy.md` names mineru.net, which happens only after the researcher confirms the scope, and only with the `MINERU_API_TOKEN` credential from `.env.local` or the environment.
- The token goes only to the API address. Uploads and downloads use the signed addresses without it, and redirects to another origin are refused.
- The service receives the source ID as the file name and as `data_id`, not the researcher's file name.
- Batches hold 20 files and start at most every 30 seconds. A rejected or expired token, the daily limit, or an unreachable service stops the run once, with the open items kept; uploaded items that are still processing are collected by a later run without a second upload.
- Signed addresses and the token are removed from every record and log.

Not verified: the live service. The tests use a fake service that follows the documentation; the archive layout and the `layout.json` format of the live service are assumptions until a live run with a real token and synthetic files.

## Integration contract as implemented

- **Archive.** The original is copied unchanged into `references/originals/<source-id>/`, and the copy's checksum is verified. The source ID is `src-` plus the first 12 hexadecimal digits of the file's SHA-256, so the same file always gets the same ID and a different version gets another one.
- **Extraction.** `references/extracted/<source-id>/` holds `document.md` with image links into `assets/`, the parser output in `native/` (without its copy of the original PDF), `provenance.json`, and a README for each folder. The folder is built in `.tmp/` and published with one rename.
- **Checks.** Page coverage against the parser's physical page count, cross-checked with a page count read from the PDF; pages without text; prose that the parser recorded but the Markdown lacks, apart from repeated or short running heads; broken links and unlinked images, apart from pictures of transcribed tables and formulas; math delimiters normalized to `$...$` and `$$` blocks without changing a formula, with unpaired `$` signs and commands that GitHub cannot render flagged; and a flag for format and route combinations not yet verified here. The result is complete, needs review, or partial.
- **Records.** Each batch has `inbox/imports/<import-id>/import.json` and a README, saved after every change. Items are pending, converting, submitted, converted, needs review, partial, already imported, duplicate, unsupported, failed, or kept for later.
- **Repeat and retry.** A file converted before with the same settings is reused. Other settings are reported and converted again only with `--reconvert`; a hand-edited `document.md` is never overwritten without `--overwrite-edited`. Continuing an import works on open, interrupted, and failed items only.
- **Reviews.** `reviews/<venue>/<round>/` keeps originals, `extracted/markdown/<document>.md`, images named `<document>--<image>`, and `extracted/provenance.json`. Word comments, replies, insertions, and deletions are read from the file's XML with the standard library, and PDF comment annotations with a best-effort scan; both are listed in a separate section of the Markdown.
- **Metadata.** `scripts/ingest.py metadata` writes BibTeX entries with `sourceid` and `metadatasource` fields, which citation processors ignore, and fills the title, authors, and year of the index row.

## Open

- A live mineru.net run with a real token and synthetic files, including the training-use and retention terms at that time.
- Windows and Linux runs of both routes, and the standard tier.
- Local formats other than PDF and Word (PowerPoint, Excel, OpenDocument, EPUB, HTML, images). They are converted but flagged as unverified.
- Page numbers of PDF annotations, and Word footnotes, endnotes, and moved text.
- Checking citation metadata against a registry, which belongs to MVP 3.
