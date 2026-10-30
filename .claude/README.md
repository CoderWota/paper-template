# Claude Code Adapter

Claude Code reads task packages from [skills/](skills/README.md). They are generated from the canonical packages in [`.agents/`](../.agents/README.md), so both applications receive the same task instructions without requiring symlinks.

The root [CLAUDE.md](../CLAUDE.md) imports the shared [contract](../AGENTS.md). Edit skills at their canonical source and regenerate the copies; never maintain independent versions here. Personal `settings.local.json` stays ignored on this computer. Researchers do not need to open or maintain these files.
