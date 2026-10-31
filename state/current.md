# Current State

Project: not initialized; no research goal or manuscript language is confirmed.

Completed template maintenance: [standard MCP installation](../mcp/README.md) is part of both clients' onboarding. [Setup script](../scripts/setup_mcp.py) installs pinned official packages, generates local client configurations, and checks MCP discovery without research queries or uploads. Earlier service tests passed on 2026-10-31: one generic Sciverse query and one researcher-authorized, single-file MinerU upload test. Both were one-time tests, not standing query or upload authorizations. Their local records are in the ignored `.local/` folder.

Completed on 2026-10-31: Sciverse and MinerU calls in workspace scripts use the installed official MCP servers through [the MCP bridge](../scripts/mcp_bridge.py). MinerU is remote-only and limited to reference materials. The import script enforces the recorded reference-only scope and `references` destination; client configurations expose Sciverse only, and the MinerU server is started internally by the importer. The MinerU local installer, parser class, CLI route, and environment probe have been removed. [The agent-call audit](../docs/agent-call-audit.md) covers all 37 skill entrypoints in both client trees, service call paths, and the conditional reviewer-session instructions. [MCP operations](../mcp/operations.md) documents their call and scope rules.

This template-maintenance task did not initialize a paper. No live service calls were made during this audit. Earlier service tests remain one-time tests and do not authorize other queries or uploads. Next step: reopen the project in each client to load its MCP configuration; Claude Code may ask for first-use server approval.
