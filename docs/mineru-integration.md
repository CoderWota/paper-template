# Document Processing with MinerU

Use this guide for import setup or a conversion problem. Reference and review documents are converted through the official MinerU MCP server, `mineru-open-mcp` 1.0.22, which `scripts/setup_mcp.py` installs in `.tools/mcp/`. The server sends each document to mineru.net, as confirmed in `requirements/privacy.md`. The researcher's own editable Word, OpenDocument, or LaTeX manuscript uses local Pandoc instead. Markdown and plain text are read directly.

## Choose and prepare a route

The installed MCP server is cloud-only, so local MinerU conversion is not available. `scripts/ingest.py --route local` refuses, and the legacy local installer `scripts/setup_mineru.py` is not used by any route. A local route needs a local MCP server or another reviewed design first.

Cloud processing sends each document to mineru.net. Confirm the material scope before any upload, and inspect every batch against the human-readable scope: a scope for published papers does not cover an unpublished draft or reviewer letter. The script refuses cloud processing unless `requirements/privacy.md` names mineru.net.

| Mode | Credential | Limits | Output |
| --- | --- | --- | --- |
| Precision | `MINERU_API_TOKEN`, entered through the private credential page | Up to 200 pages a file; the script also refuses files above 200 MB | Markdown from the MCP |
| Flash | None | Up to 20 pages and 10 MB a file | Markdown only |

The script refuses a file above the selected mode's limit before anything is sent; it never truncates silently. The page count is checked for PDFs only. For other formats the service enforces its own limit and reports an error. Each mode uploads the whole file, because the script never requests a page range. Tokens can expire.

Service information was last inspected on 2026-10-28 (API documentation) and 2026-10-30 (MCP documentation). Read current [API documentation](https://mineru.net/apiManage/docs), [limits](https://mineru.net/apiManage/limit), and the [MCP documentation](https://github.com/opendatalab/MinerU-Ecosystem/blob/main/mcp/README.md) before relying on access or cost. The legal pages did not establish training use or retention, and they include a broad license to uploaded material. These remain unknown until current terms establish otherwise; see the [privacy source pointers](../.agents/skills/privacy-configuration/sources.md).

No failed route switches to another parser or destination. A changed processing route needs a new scoped decision.

## Import and resume

Use `scripts/ingest.py plan` before an import, `run --route cloud` for the authorized route, `status` for progress, and `run --import-id ID` to continue open, interrupted, or failed items. Reuse completed items. Changing conversion settings requires `--reconvert`. A hand-edited extraction is protected unless `--overwrite-edited` is used after the correction is preserved in a source note.

The importer archives the original unchanged under a checksum-based source ID, verifies the copy, and stages derived output in `.tmp/` before publication. The extraction contains `document.md`, provenance, and a README. Import records under `inbox/imports/` retain each item's outcome so that the assistant can resume without starting over.

The service receives a neutral file name, not the researcher's file name. The script copies the original to `document.<extension>` in the job folder and removes that copy after the call. The Markdown returned by the service is saved under `.local/mcp/imports/<key>/`, which Git ignores, together with a receipt. The receipt is written before the upload and again after its outcome. A complete receipt is reused, so the same file and settings are not sent twice. An upload without a recorded outcome, for example after a broken MCP call, stops the run and is not sent again automatically. A reported failure is retried on the next run. The token reaches the MCP server through its environment. It never appears in command arguments, receipts, or logs.

Do not upload research material solely to probe connectivity.

## Check and report

Every MCP conversion is marked as needing review. The server returns Markdown only, without page records, images, or parser JSON, so the page-coverage check cannot run. Compare consequential passages, tables, figures, and formulas with the original. Keep corrections in source notes rather than editing generated text that a later conversion replaces.

Review letters retain Word comments, replies, insertions, and deletions separately. PDF annotation extraction is best effort; annotation page locators, Word footnotes and endnotes, and moved text can need manual comparison. Resolve comments and tracked changes before adopting an editable manuscript.

Use `ingest.py metadata` to record only the title, authors, year, DOI, and other metadata actually inspected in the source; leave unknown fields empty. `references/bibliography.bib` is the canonical bibliography. This import route does not match a registry. Keep distinct source versions, and relate them only after their identity is checked.

Run `ingest.py verify` and explain every partial, failed, unsupported, or needs-review outcome. The MCP route has been checked once on macOS, in flash mode, on a single document. Spot checks matched the source text, although some ligatures were misread and images were placeholders. Other documents, formats, modes, and platforms remain subject to the [capability limits](capabilities.md).
