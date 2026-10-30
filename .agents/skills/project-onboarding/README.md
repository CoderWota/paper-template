# Project Onboarding

Sets up a paper project when you ask to begin one. If you only want to understand the folders, ask for a tour first; no setup is needed. The agent asks a few questions, one at a time, and records only the answers you confirm: the language you want to work in, what you want to achieve, the manuscript language, and how your documents may be processed. Anything you do not know yet can wait.

Ask, for example: "Help me initialize this research writing project. I do not have a programming background."

## What it produces

- `requirements/project.md` and `requirements/privacy.md` with your confirmed answers, written in your language.
- An updated `state/current.md` with one clear next step.
- A check for a link back to the original template repository. A clear link is disconnected before setup finishes, while local saved versions remain.

## What it never does

- It never deletes, moves, or overwrites research material. A workspace that already holds another paper stays unchanged; a new paper starts from a fresh copy of the template instead.
- It never asks for a password or an API key in the conversation.

The agent instructions are in [SKILL.md](SKILL.md). Related skills: `environment-management`, `privacy-configuration`, and `constraint-maintenance`.

After a directory tour, the assistant reuses what you already told it and asks only for missing information needed for the first task. Processing choices, software setup, and the optional account privacy check are introduced when relevant, rather than required to understand the workspace.

Initialization also installs the official Sciverse and MinerU cloud MCP tools inside this workspace, configures Codex and Claude Code, and checks their tool lists. No research query or document is sent. Keys can wait until the first authorized service use. Installation failures remain recorded for retry.
