# Claude Code Adapters

Claude Code reads project skills from this directory. Its skill contents are generated from the canonical, application-independent packages in [`.agents/`](../.agents/README.md), so Claude Code and Codex follow the same instructions.

## Contents

- [`skills/`](skills/README.md): generated skill mirrors. Do not edit them by hand.

Claude Code also loads [`CLAUDE.md`](../CLAUDE.md) at the workspace root, which imports the shared contract in [`AGENTS.md`](../AGENTS.md).

Personal Claude Code settings (`settings.local.json`) can appear here. They stay on this computer and are excluded from version history.

## Who edits what

The agent maintains this directory. Researchers do not need to open or edit it.
