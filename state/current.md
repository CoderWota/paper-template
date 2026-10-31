# Current State

Project: not initialized; no research goal or manuscript language is confirmed.

Completed template maintenance: [standard MCP installation](../mcp/README.md) is part of both clients' onboarding. [Setup script](../scripts/setup_mcp.py) installs pinned official packages, generates local client configurations, and checks MCP discovery without research queries or uploads. Earlier service tests passed on 2026-10-31: one generic Sciverse query and one researcher-authorized, single-file MinerU upload test. Both were one-time tests, not standing query or upload authorizations. Their local records are in the ignored `.local/` folder.

Completed on 2026-10-31: Sciverse and MinerU calls in the workspace scripts go through the installed official MCP servers, via [the MCP bridge](../scripts/mcp_bridge.py). The Sciverse operations map onto the six MCP tools. Paper Schema is not exposed, so its commands record `unavailable` and send nothing. MinerU conversion uses the cloud MCP only: flash mode without a token, precision mode with one. Each upload has a receipt, and an upload without a recorded outcome is not sent again automatically. The local MinerU route is refused. Skills in both client trees, the docs, and `requirements/project.md` describe this. Checks: stub tests for routing, receipts, and truncation; a real MCP handshake with refused calls that send no data; an in-process import with a stubbed reply.

Open decisions: whether to add a local MCP for document conversion, and whether to remove the legacy `scripts/setup_mineru.py` and the Paper Schema commands. Next action: reopen the project in both clients to load the MCP configuration, and approve Claude Code's first-use server prompt.
