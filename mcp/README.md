# Repository MCP Tools

Workspace initialization installs the official Sciverse and MinerU cloud MCP servers. Codex and Claude Code receive the Sciverse MCP directly. MinerU stays installed for `scripts/ingest.py`, which starts the official server internally after checking the reference-only scope; clients do not receive its raw upload tool.

## Operations

Use Python 3.11 or later and Node.js 18 or later with npm. No global package installation, GPU, local MinerU models, Docker, or API token is required for installation. Existing runtimes are reused. Installing a missing runtime is a separate choice.

```sh
python3 scripts/setup_mcp.py install
python3 scripts/setup_mcp.py configure
python3 scripts/setup_mcp.py check
```

`install` uses `package-lock.json` and the hash-checked `requirements.lock`. Dependencies go into ignored `.tools/mcp/`. Repeating a completed installation does not download packages. Interrupted installations can be retried. `configure` can be repeated independently and preserves unrelated client settings. It removes the direct `mineru` client entry so uploads cannot bypass the workspace importer; previous changed files are backed up under `.local/mcp/backups/`.

`configure` generates ignored, machine-specific `.codex/config.toml` and `.mcp.json` from the templates here. They expose Sciverse as a client-native tool and do not expose MinerU's upload tool. Neither contains credentials. Reopen the project in a trusted client to load the new tools and accept any client workspace/server trust prompt. These scripts do not change global trust or client settings. After moving or copying the repository, rerun installation and configuration; Python environments are not portable.

`check` reports installation, JSON-RPC handshake, tool discovery, generated configurations, and credential presence separately. It saves the latest local report in `.local/mcp/status.json`. It uses dummy credentials for discovery and only sends MCP `initialize`, `notifications/initialized`, and `tools/list`, never service queries or file uploads. This checks the servers independently; it does not prove a particular client has loaded them, nor that a credential is valid.

`scripts/setup_mcp.py start` launches a pinned server for a client or the internal bridge. Generated client configurations expose only Sciverse; the import bridge starts MinerU. Start never installs or upgrades a package. Diagnostics go to stderr; stdout belongs to MCP. Pin updates are deliberate maintenance of both manifests and lock files, followed by installation and protocol checks.

## Credentials and data flow

The launcher reads credentials through the existing private-store code. Sciverse uses `SCIVERSE_API_TOKEN` from the process environment, then `SCIVERSE_API_KEY` from the environment, then the project's private `SCIVERSE_API_KEY` or `SCIVERSE_API_TOKEN`. MinerU uses `MINERU_API_TOKEN` from the environment or private store. Values are never included in generated configuration or status reports. Only the selected service token is added to the server environment. Do not enter keys in chat.

Missing credentials do not block installation. Sciverse service calls need a token; MinerU can run its limited, token-free Flash cloud mode. Both MinerU modes send submitted files or URLs to mineru.net. This workspace permits MinerU uploads only for reference materials, as recorded in `requirements/privacy.md`; drafts, review correspondence, feedback, and other materials are excluded. Installing cloud MCP does not authorize an upload. Existing search-query scope rules remain in force.

Research commands use these servers through the workspace scripts. `scripts/literature.py` and `scripts/ingest.py` call them through `scripts/mcp_bridge.py`, which starts only the configured servers and calls only the tool that the command names. Each script applies its own scope checks, archival, and records. The MinerU Markdown that the workspace imports is saved under `.local/mcp/imports/` with an upload receipt. The server's default output folder is `.local/mcp/output/`. These outputs are working files, not archived originals or verified extractions. A read-only mock review may use native Sciverse MCP tools without creating workspace search records, as described in [MCP call operations](operations.md); check the active query scope and report the search in the response. All MinerU reference imports use the workspace script so that scope checks, archival, and upload receipts are preserved.

## Official references

- [Sciverse Agent Tools](https://github.com/opendatalab/Sciverse-Agent-Tools)
- [MinerU Open MCP](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/mcp)
- [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
- [Claude Code project MCP configuration](https://code.claude.com/docs/en/mcp)

Sciverse 1.0.0 and MinerU Open MCP 1.0.22 are the initial pinned versions. The MinerU MCP runs remotely; the workspace does not install or run local MinerU inference.
