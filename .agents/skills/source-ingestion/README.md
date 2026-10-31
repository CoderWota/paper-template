# Source Ingestion

Imports your documents into the reference library: one file, a folder, or whatever you put in `inbox/`. The agent keeps each original unchanged, converts it into readable Markdown through the official MinerU MCP, checks what it can, and adds the source to the index and the bibliography. You do not need to know MinerU, sort your files, or name any output.

Ask, for example: "Import all PDFs in this folder, including the images." or "Continue the import, but only the files that failed."

## What to expect

- Documents are converted only with the mineru.net service, and only for the documents you confirmed. Conversion on this computer is not available yet. A failure is reported; it never moves your documents to another service.
- Converted text comes back as Markdown without page records or figures, so every converted document is marked as needing a check against its original.
- Every file gets a status: converted, already imported, needs a check, failed, or not supported. The agent tells you why and what it recommends.
- A converted document can still contain errors, especially in formulas, tables, and scanned pages. The agent points out what to check, and the original stays the authority.
- An interrupted import continues where it stopped, and files that were already converted are not converted again.
- Citation details come from the document itself and are marked as not yet checked against a registry.

The agent instructions are in [SKILL.md](SKILL.md). The skill uses `scripts/ingest.py`, which calls the official MinerU MCP, and `scripts/setup_mcp.py` for its installation check. Related skills: `review-ingestion`, `environment-management`, and `privacy-configuration`.

Route setup, continuation, extraction review, and metadata commands are in [the import guide](import-guide.md), read only for the operation being performed.
