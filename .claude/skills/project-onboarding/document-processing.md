# Document processing choice

Read this only when an import needs a processing choice now or the researcher asks to settle it.

## Step 5: Explain the confirmed document-processing scope

Ask this when the researcher has documents that need conversion now (PDFs, office files, or images) or wants to settle it now. Markdown and plain-text files are read directly and need no processing choice, and data files are not documents to convert. Otherwise, list the processing choice as open ("decide at the first import") and continue.

1. Read `requirements/privacy.md`. The confirmed MinerU route is remote through the official MCP and covers reference materials only. It does not cover manuscripts or drafts, review correspondence, feedback, or other material.
2. Initialization sends no queries or documents. Do not ask the researcher to confirm the existing reference-only scope again. If a later request needs MinerU for another kind of material, stop before sending it and ask whether they want to change the recorded scope.
3. Run `python scripts/setup_mcp.py check` to see whether the official MinerU MCP is installed and answers. Use `environment-management` for anything it reports as missing.
4. Markdown and plain text can be read directly. Editable manuscript formats can use local Pandoc where supported. Other non-reference documents that need MinerU conversion remain unprocessed under the confirmed scope.

If the choice needs a credential or an installation, use `environment-management`. If that setup cannot be done yet, record the choice and mark the setup as deferred.

