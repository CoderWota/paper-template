# Repository MCP Tools

Workspace initialization installs the official Sciverse and MinerU cloud MCP servers for Codex and Claude Code. The assistant performs this work; researchers do not need to run setup commands.

## Operations

Use Python 3.11 or later and Node.js 18 or later with npm. No global package installation, GPU, local MinerU models, Docker, or API token is required for installation. Existing runtimes are reused. Installing a missing runtime is a separate choice.

```sh
python3 scripts/setup_mcp.py install
python3 scripts/setup_mcp.py configure
python3 scripts/setup_mcp.py check
```

`install` uses `package-lock.json` and the hash-checked `requirements.lock`. Dependencies go into ignored `.tools/mcp/`. Repeating a completed installation does not download packages. Interrupted installations can be retried. `configure` can be repeated independently and preserves unrelated client settings, with previous changed files backed up under `.local/mcp/backups/`.

`configure` generates ignored, machine-specific `.codex/config.toml` and `.mcp.json` from the templates here. Neither contains credentials. Reopen the project in a trusted client to load the new tools and accept any client workspace/server trust prompt. These scripts do not change global trust or client settings. After moving or copying the repository, rerun installation and configuration; Python environments are not portable.

`check` reports installation, JSON-RPC handshake, tool discovery, generated configurations, and credential presence separately. It saves the latest local report in `.local/mcp/status.json`. It uses dummy credentials for discovery and only sends MCP `initialize`, `notifications/initialized`, and `tools/list`, never service queries or file uploads. This checks the servers independently; it does not prove a particular client has loaded them, nor that a credential is valid.

Clients call `python scripts/setup_mcp.py start sciverse` or `start mineru` using the dedicated environment. Start never installs or upgrades a package. Diagnostics go to stderr; stdout belongs to MCP. Pin updates are deliberate maintenance of both manifests and lock files, followed by installation and protocol checks.

## Credentials and data flow

The launcher reads credentials through the existing private-store code. Sciverse uses `SCIVERSE_API_TOKEN` from the process environment, then `SCIVERSE_API_KEY` from the environment, then the project's private `SCIVERSE_API_KEY` or `SCIVERSE_API_TOKEN`. MinerU uses `MINERU_API_TOKEN` from the environment or private store. Values are never included in generated configuration or status reports. Only the selected service token is added to the server environment. Do not enter keys in chat.

Missing credentials do not block installation. Sciverse service calls need a token; MinerU can run its limited, token-free Flash cloud mode. Both MinerU modes send submitted files or URLs to mineru.net. Installing cloud MCP does not select cloud processing for a document or authorize any upload. Existing query-sharing and document-processing scope rules remain in force.

Research commands use these servers through the workspace scripts. `scripts/literature.py` and `scripts/ingest.py` call them through `scripts/mcp_bridge.py`, which starts only the configured servers and calls only the tool that the command names. Each script applies its own scope checks, archival, and records. The MinerU Markdown that the workspace imports is saved under `.local/mcp/imports/` with an upload receipt. The server's default output folder is `.local/mcp/output/`. These outputs are working files, not archived originals or verified extractions. Calling an official tool directly from a chat bypasses those checks, so do not do that for research material.

## Official references

- [Sciverse Agent Tools](https://github.com/opendatalab/Sciverse-Agent-Tools)
- [MinerU Open MCP](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/mcp)
- [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
- [Claude Code project MCP configuration](https://code.claude.com/docs/en/mcp)

Sciverse 1.0.0 and MinerU Open MCP 1.0.22 are the initial pinned versions. This cloud MCP package is distinct from the legacy local `mineru` document parser, which no route uses.
