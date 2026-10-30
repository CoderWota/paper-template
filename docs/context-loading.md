# Context Loading and Tool Access

Use this guide when configuring either application or diagnosing missing instructions, skills, or tools. Ordinary writing starts from the short project records and the selected task. Documentation checked on 2026-10-30; application behavior and settings can change.

## Shared instructions and task records

Codex discovers project `AGENTS.md` files along the path from repository root to its starting directory; it does not promise to discover every child file merely because a tool opens one. Claude Code has its own instruction loading rules. Keep essential shared constraints in the root contract and explicitly read task-specific records in both clients. [Codex instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Claude memory](https://code.claude.com/docs/en/memory).

The root `CLAUDE.md` imports `AGENTS.md` for compatibility. An `@path` import expands into startup context; a normal Markdown link does not automatically import its target. Do not import the whole library or all requirements. Do not duplicate the shared contract in a startup hook or another instruction file. Whether a newer Claude version also reads `AGENTS.md` directly depends on version and instruction settings; the adapter does not require that behavior.

At session start read `state/current.md` and `requirements/project.md`. For a request to edit a sentence, then read that sentence, applicable writing rules, and any support needed to preserve its meaning. For a request to resume a broader goal, use the resume skill and inspect relevant records and freshness checks. Read an index only to locate material needed for the request.

Confirmed project records govern the paper across sessions. Auto memory is not a source of confirmed requirements or authorization, and must not store inferred preferences. Do not change a user's global memory settings as a side effect of workspace setup.

## Loading is not system-message authority

Claude Code's official [memory troubleshooting](https://code.claude.com/docs/en/memory#claude-isnt-following-my-claudemd) states that `CLAUDE.md` content is delivered as a user message after the system prompt, not as part of the system prompt. An `@AGENTS.md` import expands into that project-instruction context; copying the same rules into `CLAUDE.md` does not promote them to system authority. The [session transcript documentation](https://platform.claude.com/docs/en/manage-claude/compliance-sessions) also describes project instructions as user-role content.

Use the import to ensure discovery and maintain one source. An ordinary later tool read is not a substitute for startup loading, but neither approach makes file contents a hard enforcement layer. Claude offers `--append-system-prompt` for an intentional launch-time system addition; this workspace neither requires it nor changes the user's launch command. Do not claim project-file rules override the host's higher-level instructions. Keep important research constraints concise, check outputs, and report actual loading separately from behavioral compliance.

## Skill discovery and adapters

Codex discovers repository skills under `.agents/skills/`; Claude Code discovers the generated packages under `.claude/skills/`. Names and descriptions participate in initial discovery. The selected skill's full instructions and its references are read when needed, so shorten descriptions at the source rather than increasing context budgets. [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Claude skills](https://code.claude.com/docs/en/skills).

Keep the 36 task names stable and automatic selection enabled. Do not load related skill bodies just because their names appear in a routing table. A skill handoff is needed only when that subtask is necessary for the authorized outcome. Conditional procedures should link to their reference beside the condition that needs it; a short skill needs no extra routing layer.

Edit only `.agents/skills/`, then run `python scripts/sync_skills.py` and `python scripts/sync_skills.py --check`. Committed generated copies work in a normal download without symlink setup. Researchers do not run synchronization. Preserve task scope, evidence safeguards, and candidate-versus-active manuscript handling when editing instructions.

## Harness, scripts, and MCP

The application's native harness handles conversations, context management, skill discovery, and tool execution. This workspace adds instructions and scripts, not another orchestration engine. Skills describe decisions and research procedures; scripts implement repeatable file operations; MCP connectors provide specific external data or actions.

When a task needs an external tool, discover only the relevant tool names in the current session and read the selected tools' schemas before calling them. Do not enumerate every server, resource, and schema at startup. When no connector covers a task, use the existing authorized script or host capability and state its limits. Tool presence does not prove connectivity, account access, or permission to transfer research material.

Codex project MCP configuration uses `.codex/config.toml` in a trusted project. Claude Code project MCP configuration uses `.mcp.json`; it is not the Codex TOML format. No servers or startup hooks are enabled by this workspace. Configure a named service only when requested, without changing global settings or adding embedded credentials. [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [Claude MCP](https://code.claude.com/docs/en/mcp).

Claude Code can discover deferred MCP tools through tool search where the client, model, and provider route support it. Codex can restrict a server's exposed tools with its supported allow/deny settings. Do not assume a common setting, automatic deferral, or the same behavior across providers. Keep any tool-specific setup in the relevant task instructions. Neither discovery nor connection authorizes uploads, costs, or sharing.

## Inspecting loading

In a fresh client session, inspect its instruction and skill listing (for example, Claude's `/context` or Codex's skill selector) and compare the actual sources with this guide. Check representative requests: a sentence edit, PDF import, evidence lookup, Word output, and project resumption. Confirm that only relevant references are read and that both clients find the same task instructions.

A matching generated copy and a smaller instruction file establish file consistency and size only. They do not establish faster execution, actual client loading, model adherence, or Windows behavior. Report any client or platform that was not observed.
