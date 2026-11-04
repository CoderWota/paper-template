# Current State

Project: not initialized; no research goal or manuscript language is confirmed.

Completed template maintenance: [standard MCP installation](../mcp/README.md) is part of both clients' onboarding. [Setup script](../scripts/setup_mcp.py) installs pinned official packages, generates local client configurations, and checks MCP discovery without research queries or uploads. Earlier service tests passed on 2026-10-31: one generic Sciverse query and one researcher-authorized, single-file MinerU upload test. Both were one-time tests, not standing query or upload authorizations. Their local records are in the ignored `.local/` folder.

Completed on 2026-10-31: Sciverse and MinerU calls in workspace scripts use the installed official MCP servers through [the MCP bridge](../scripts/mcp_bridge.py). MinerU is remote-only and limited to reference materials. The import script enforces the recorded reference-only scope and `references` destination; client configurations expose Sciverse only, and the MinerU server is started internally by the importer. The MinerU local installer, parser class, CLI route, and environment probe have been removed. [The agent-call audit](../docs/agent-call-audit.md) covers all 37 skill entrypoints in both client trees, service call paths, and the conditional reviewer-session instructions. [MCP operations](../mcp/operations.md) documents their call and scope rules.

Template maintenance on 2026-10-31 added `pdftotext` (Poppler) to the initialization scope and environment check. No paper was initialized, and this change made no Sciverse queries or MinerU uploads. Earlier service tests remain one-time tests and do not authorize other queries or uploads. Claude Code may ask for first-use server approval when reopened.

Template maintenance on 2026-11-04 added a confirmed requirement for an internal Mermaid logic map in both the from-scratch outline and manuscript-import workflows. The map is kept out of publication output, tracked in project status, and checked as part of argument writing and audit. The paper remains uninitialized. Next step: reopen the project in either client; the authoring workflows now include logic-map creation.
