# Import Route and Operations

Read the route-selection and preparation sections only when setting up or changing an import. Read run, review, and metadata sections when performing that part of the import. Shared constraints remain in the workspace contract.

## Step 2: Settle the processing route

Read `requirements/privacy.md`. Markdown and plain text need no route: they are read directly.

If no processing choice covers these documents, guide the route choice as part of the requested import; do not wait for the researcher to ask for setup separately. First inspect the computer with `environment-management`, and run `python scripts/setup_mineru.py check`. Then explain the two routes in plain words, recommend one based on document sensitivity and this computer, and ask one choice question:

- **This computer.** The documents stay here. MinerU needs about 1.4 GB in `.tools/mineru/` and Python 3.10 to 3.14. Its flash tier reads PDFs that contain a text layer, and Word files, without models; other office formats are converted too, but flagged until they are verified in this workspace. Scanned pages, formulas, and complex tables need the basic tier, whose models take about 0.9 GB. The standard tier adds a vision model of several gigabytes and needs at least 16 GB of memory.
- **mineru.net, the official MinerU service.** The documents are uploaded to a service in mainland China. It needs a free account and a token. Limits: 200 MB and 200 pages a file, about 1000 pages a day at full priority, 50 files a minute. Its public terms do not say whether uploaded documents are used to train models or how long they are kept, and they give the operator a broad license to uploaded material; [privacy-configuration/sources.md](../privacy-configuration/sources.md) has the details. Unpublished or confidential material therefore deserves the local route.

Record the confirmed choice in `requirements/privacy.md` with the documents that it covers, so that later imports reuse it without asking again. A local choice is recorded at once. A cloud choice is recorded through `privacy-configuration`, only after the researcher confirms which documents may be uploaded, and the record must name the service as mineru.net: the script refuses the cloud route until `requirements/privacy.md` names it. Before each cloud import, check that every document in the batch is inside the confirmed scope; the researcher's own draft and reviewer letters are outside a scope of "published papers". Ask when a document is outside or unclear. Choosing a cloud route or entering its token does not by itself authorize uploading documents.

## Step 3: Prepare the route

**This computer:**

1. `python scripts/setup_mineru.py check` reports the installation, the models, and the free disk space.
2. If MinerU is missing, explain the size and recommend the smallest setup that fits this batch. Ask for consent, then run `python scripts/setup_mineru.py install`. Do not wait for a separate setup request. If no Python 3.10 to 3.14 exists, use `environment-management` first.
3. Choose the tier for the material, and recommend the smallest one that fits:

   | Material | Tier | Command options | Needs |
   | --- | --- | --- | --- |
   | PDFs whose text can be selected; Word files (other office formats are flagged until verified) | flash | `--tier flash --ocr-mode txt` | nothing more |
   | Scanned pages, formulas that matter, complex tables | basic | `--tier basic` | basic models, about 0.9 GB, with consent |
   | Layouts that the basic tier gets wrong | standard | `--tier standard` | a vision model of several GB and 16 GB or more of memory, with consent |

   Download models only after consent: `python scripts/setup_mineru.py models --tier basic`.

**mineru.net:**

1. `python scripts/credentials.py status MINERU_API_TOKEN` shows whether the token is set.
2. If it is not, explain that the cloud route needs a mineru.net account and token, then start `environment-management`'s private credential-entry flow for `MINERU_API_TOKEN` in the researcher's language. Do not ask the researcher to invoke setup separately. The researcher signs in at mineru.net and creates the token on the API management page, <https://mineru.net/apiManage/token>. Tokens can expire. Token entry does not authorize an upload; the document scope must already be confirmed.

## Step 4: Run the import

```text
python scripts/ingest.py run --route local --tier flash --ocr-mode txt [--recursive] PATH...
python scripts/ingest.py run --route cloud [--recursive] PATH...
```

- Run a large batch in the background, and check it with `python scripts/ingest.py status`.
- The script archives each original, converts it, checks it, publishes it in one step, and saves the import record in `inbox/imports/<import-id>/` after every change. A file that was imported before with the same settings is reused, not converted again.
- Exit status 2 means that the run stopped for a reason that affects every document (missing models, an expired token, the daily limit, the network) or that mineru.net is still working. Explain the reason in plain words, fix it with the researcher's consent, and continue the same import: `python scripts/ingest.py run --import-id ID`. Never start a second import of the same material instead.
- "Retry the failed ones" or "continue" also means `run --import-id ID`: it works on open, interrupted, and failed items only, and keeps every finished result.
- To convert files again with other settings, for example scanned papers with the basic tier, name those files and add `--reconvert`. If a `document.md` was edited by hand, the script refuses. Keep the researcher's edit: copy it into the source note, `references/notes/<source-id>.md`, as their correction and nothing more, then add `--overwrite-edited`.

## Step 5: Check what needs review

For each item that is partial or needs review, read the problem list in the README of its extraction folder and explain it in plain words, with one recommended action:

| Problem | Meaning | Recommended action |
| --- | --- | --- |
| Pages were not converted | The extraction is partial | Convert again; never present it as complete |
| No text on some pages | Scanned pages that the flash tier cannot read | Convert those files again with the basic tier, or with OCR on mineru.net (`--ocr`) |
| Passages left out of the Markdown | The parser took text for a page header or footer | Read those pages in the original before relying on the extraction |
| Images not linked from the text | A figure, formula, or table may be missing from the text | Look at the images in `assets/` |
| Formulas transcribed by the parser | Formula text can be wrong | Compare a formula with its picture in `assets/`, or with the original, before relying on it |
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

