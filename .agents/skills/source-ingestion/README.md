# Source Ingestion

Imports reference materials into the library: one source, a folder, or reference files from `inbox/`. The agent keeps each original unchanged, converts supported files into readable Markdown through the official remote MinerU MCP, checks what it can, and adds each source to the index and bibliography. Drafts, review correspondence, feedback, and other materials are never uploaded through this skill. You do not need to know MinerU, sort your files, or name any output.

Ask, for example: "Import all PDFs in this folder, including the images." or "Continue the import, but only the files that failed."

## What to expect

- MinerU is remote-only and processes reference materials only. The script enforces the `references` destination; the agent checks the material's role before upload. A failure is reported; it never moves the file to another service.
- Converted text comes back as Markdown without page records or figures, so every converted document is marked as needing a check against its original.
- Every file gets a status: converted, already imported, needs a check, failed, or not supported. The agent tells you why and what it recommends.
- A converted document can still contain errors, especially in formulas, tables, and scanned pages. The agent points out what to check, and the original stays the authority.
- An interrupted import continues where it stopped, and files that were already converted are not converted again.
- Citation details come from the document itself and are marked as not yet checked against a registry.

The agent instructions are in [SKILL.md](SKILL.md). The skill uses `scripts/ingest.py`, which calls the official MinerU MCP, and `scripts/setup_mcp.py` for its installation check. Related skills: `review-ingestion`, `environment-management`, and `privacy-configuration`.

Route setup, continuation, extraction review, and metadata commands are in [the import guide](import-guide.md), read only for the operation being performed.
