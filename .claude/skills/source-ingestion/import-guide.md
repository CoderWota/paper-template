# Import Route and Operations

Read the route-selection and preparation sections only when setting up or changing an import. Read run, review, and metadata sections when performing that part of the import. Shared constraints remain in the workspace contract.

## Step 2: Settle the processing route

Read `requirements/privacy.md`. Markdown and plain text need no route: they are read directly.

If no processing choice covers these documents, guide the route choice as part of the requested import; do not wait for the researcher to ask for setup separately. First run `python scripts/setup_mcp.py check` to see whether the official MinerU MCP is installed and answers. Then explain the options in plain words, recommend one based on document sensitivity, and ask one choice question:

- **This computer.** Not available yet. The installed official MinerU MCP is cloud-only, and no route runs MinerU on this computer. Unpublished or confidential documents therefore cannot be converted until a local MCP integration is added. Say so plainly. Do not install the legacy local MinerU to work around it.
- **mineru.net, through the official MinerU MCP.** The whole file is uploaded to mineru.net, a service in mainland China. With a token in `MINERU_API_TOKEN`, precision mode applies: up to 200 pages a file. Without a token, the free flash mode applies: Markdown only, up to 20 pages and 10 MB a file. The public terms do not say whether uploaded documents are used to train models or how long they are kept, and they give the operator a broad license to uploaded material. [privacy-configuration/sources.md](../privacy-configuration/sources.md) has the details.
- **Decide later.** Record the processing choice as open and continue with the parts that need no conversion.

Record the confirmed choice in `requirements/privacy.md` with the documents that it covers, so that later imports reuse it without asking again. Record it through `privacy-configuration`, only after the researcher confirms which documents may be uploaded. The record must name the service as mineru.net: the script refuses the cloud route until `requirements/privacy.md` names it. Before each cloud import, check that every document in the batch is inside the confirmed scope; the researcher's own draft and reviewer letters are outside a scope of "published papers". Ask when a document is outside or unclear. Choosing a cloud route or entering its token does not by itself authorize uploading documents.

## Step 3: Prepare the route

**mineru.net through the MCP:**

1. `python scripts/setup_mcp.py check` reports the pinned Sciverse and MinerU MCP packages, whether each server answers, and which credentials are present. If a package is missing, explain the reason and ask for consent, then run `python scripts/setup_mcp.py install`.
2. `python scripts/credentials.py status MINERU_API_TOKEN` shows whether a token is set. Without a token, flash limits apply. Offer precision mode only if the researcher wants it. Then start `environment-management`'s private credential-entry flow for `MINERU_API_TOKEN` in the researcher's language. The researcher signs in at mineru.net and creates the token on the API management page, <https://mineru.net/apiManage/token>. Tokens can expire. Token entry does not authorize an upload; the document scope must already be confirmed.

## Step 4: Run the import

```text
python scripts/ingest.py run --route cloud [--language CODE] [--ocr] [--recursive] PATH...
```

- Run a large batch in the background, and check it with `python scripts/ingest.py status`.
- The script archives each original, sends it through the MCP, saves the returned Markdown, checks what it can, publishes it in one step, and saves the import record in `inbox/imports/<import-id>/` after every change. A file that was imported before with the same settings is reused, not sent again.
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
| No text on some pages | Scanned pages that the flash mode cannot read | Convert those files again with OCR (`--ocr`), after the researcher confirms the cloud scope |
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
