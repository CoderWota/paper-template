# Document processing choice

Read this only when an import needs a processing choice now or the researcher asks to settle it.

## Step 5: Ask how documents can be processed

Ask this when the researcher has documents that need conversion now (PDFs, office files, or images) or wants to settle it now. Markdown and plain-text files are read directly and need no processing choice, and data files are not documents to convert. Otherwise, list the processing choice as open ("decide at the first import") and continue.

1. Run `python scripts/setup_mcp.py check` to see whether the official MinerU MCP is installed and answers. Use `environment-management` for anything it reports as missing. Do not install anything in this step.
2. Explain the options in plain words:
   - Local: not available yet. The installed official MinerU MCP is cloud-only, so documents cannot be converted on this computer until a local integration is added.
   - Cloud: the official MinerU MCP sends each document to mineru.net, a named service, which processes it. The whole file is sent.
   - Decide later.
3. Recommend one option, with its reason. Base it on how sensitive the documents are. Unpublished or confidential documents cannot be converted yet, because the local option is not available.
4. For a cloud choice, also confirm which documents the choice covers.

If the choice needs a credential or an installation, use `environment-management`. If that setup cannot be done yet, record the choice and mark the setup as deferred.

