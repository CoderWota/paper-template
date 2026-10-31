# Import Route and Operations

Read the route-selection and preparation sections only when setting up or changing an import. Read run, review, and metadata sections when performing that part of the import. Shared constraints remain in the workspace contract.

## Step 2: Settle the processing route

Read `requirements/privacy.md`. Markdown and plain text need no route: they are read directly.

Read `requirements/privacy.md`. MinerU is remote-only through the official MCP, and the confirmed scope permits reference materials only. Do not ask the researcher to choose the route or confirm this same scope again. Before using the cloud route, identify every input as a reference source from its name and contents. If a file is a draft, review correspondence, feedback, or another non-reference item, do not upload it; route it to its specialist skill or leave it unprocessed. If its role is unclear, ask before sending it. The route applies only to reference materials, including unpublished sources only when they are genuinely being used as references. A request to extend the scope needs a new confirmed choice recorded in `requirements/privacy.md`.

## Step 3: Prepare the route

**mineru.net through the MCP:**

1. `python scripts/setup_mcp.py check` reports the pinned Sciverse and MinerU MCP packages, whether each server answers, and which credentials are present. If the package is missing during project initialization, follow `project-onboarding`'s authorized install step. During a standalone import, explain the missing setup and ask before installing it; continue any work that needs no conversion.
2. `python scripts/credentials.py status MINERU_API_TOKEN` shows whether a token is set. Without a token, flash limits apply. Offer precision mode only if the researcher wants it. Then start `environment-management`'s private credential-entry flow for `MINERU_API_TOKEN` in the researcher's language. The researcher signs in at mineru.net and creates the token on the API management page, <https://mineru.net/apiManage/token>. Tokens can expire. Token entry does not authorize an upload; the document scope must already be confirmed.

## Step 4: Run the import

```text
python scripts/ingest.py run --to references --route cloud [--language CODE] [--ocr] [--recursive] PATH...
```

- Run a large batch in the background, and check it with `python scripts/ingest.py status`.
- Use this command only for files already identified as reference materials. The script enforces the `references` destination; it cannot determine a file's scholarly role by itself. It archives each original, sends it through the MCP, saves the returned Markdown, checks what it can, publishes it in one step, and saves the import record in `inbox/imports/<import-id>/` after every change. A file that was imported before with the same settings is reused, not sent again.
- The script keeps a receipt for each upload in `.local/mcp/imports/<key>/receipt.json`, written before the upload and again after its outcome. When an MCP call breaks, the run stops and the upload stays without a recorded outcome. Later runs report that item without sending the file again. Check the receipt with the researcher before deleting it. After a reported failure, the next run sends the file again.
- Exit status 2 means that the run stopped for a reason that affects every document, such as a missing MCP installation or a network failure. Explain the reason in plain words, fix it with the researcher's consent, and continue the same import: `python scripts/ingest.py run --import-id ID`. Never start a second import of the same material instead.
- "Retry the failed ones" or "continue" also means `run --import-id ID`: it works on open, interrupted, and failed items only, and keeps every finished result.
- To convert files again with other settings, for example scanned papers with OCR, name those files and add `--reconvert`. If a `document.md` was edited by hand, the script refuses. Keep the researcher's edit: copy it into the source note, `references/notes/<source-id>.md`, as their correction and nothing more, then add `--overwrite-edited`.

## Step 5: Check what needs review

Every conversion through the MinerU MCP needs review. The MCP returns Markdown only, so the page-coverage check cannot run. For each item that is partial or needs review, read the problem list in the README of its extraction folder and explain it in plain words, with one recommended action:

| Problem | Meaning | Recommended action |
| --- | --- | --- |
| Page coverage not checked | The MCP returns Markdown only, without page records | Check pages against the original; do not present the text as complete |
| Pages were not converted | The extraction is partial | Convert again; never present it as complete |
| No text on some pages | Scanned pages that the flash mode cannot read | If the item is still an authorized reference source, rerun it with OCR (`--ocr`) when the researcher requests that conversion |
| Passages left out of the Markdown | The parser took text for a page header or footer | Read those pages in the original before relying on the extraction |
| Figures not kept | The MCP does not return images | Compare each figure and table with the original |
| Formulas transcribed by the parser | Formula text can be wrong | Compare a formula with the original before relying on it |
| Format not verified in this workspace | The conversion route for this file type has not been tested here | Compare the result with the original |

Never repair the extracted text yourself. A correction that the researcher gives is kept in the source note, so that it survives a new conversion; the note then holds that correction only, because reading and evaluating sources is a separate task.

## Step 6: Record citation metadata

For each newly converted source:

1. Read the beginning of its `document.md` and the `hints` in its `provenance.json`: the title and authors embedded in the file, and DOI candidates. Embedded metadata is often wrong; the first page decides.
2. Write only what the document itself shows. Leave out every field it does not show, and never guess a year, a venue, or a DOI. Use a DOI only when the document gives it as its own.

   ```text
   python scripts/ingest.py metadata SOURCE_ID --type article --title "..." --author "Family, Given" --author "..." --year YYYY [--journal "..."] [--doi ...]
   ```

3. The entry is marked as read from the document. Checking it against a registry such as Crossref is not available yet; say so if the researcher asks how reliable the metadata is.
4. If two sources look like versions of the same work, such as a preprint and the published article, tell the researcher. Keep both, because their files differ. When the researcher confirms that they are versions of one work, record the link in both entries with `--field relatedsource=<the other source ID>`.
