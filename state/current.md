# Current State

Project: not initialized; no research goal or manuscript language is confirmed.

Completed template maintenance: [standard MCP installation](../mcp/README.md) is part of both clients' onboarding. [Setup script](../scripts/setup_mcp.py) installs pinned official packages, generates local client configurations, and checks MCP discovery without research queries or uploads. Nine behavior tests and all four changed skill validations passed; the temporary test script was then removed as requested. Runtime configuration templates and dependency manifests remain in use. No research work is in progress; template remotes were not changed.

Completed service tests: Sciverse returned a result for the generic test query. On 2026-10-31, the researcher-authorized MinerU upload test succeeded for pages 1-3 of the specified Batul PDF after an earlier unspecified failure. The original is unchanged. Result, single-file authorization, checks, and limitations are recorded in ignored `.local/mcp/upload-test-batul/README.md` and `status.json`; this was not a library import or a standing upload authorization. Temporary diagnostic traces were removed.

Next action: reopen the project to load its MCP configuration. Claude Code requires its first-use server approval; service credentials and future data-sharing scopes remain separate from installation. Machine-specific installation and credential status stays in ignored `.local/mcp/status.json`. Begin paper setup only when requested.
