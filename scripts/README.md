# Scripts

Reusable automation for operating this workspace, such as checks, conversion adapters, and build steps. The agent writes and runs these scripts; researchers never need to run or edit them.

Research analysis code is kept separately in `code/`, which is created only when a project needs it (`research-code-setup`), so that workspace tools cannot destabilize an analysis environment.

## Current scripts

| Script | Purpose |
| --- | --- |
| [`check_readmes.py`](check_readmes.py) | Checks that every project directory has a meaningful, directory-specific README, following the contract in [design plan Section 4](../docs/design-plan.md#directory-readme-contract). Run `python scripts/check_readmes.py`; it exits with status 1 and lists the problems when a check fails. |
| [`sync_skills.py`](sync_skills.py) | Validates each canonical skill package in `.agents/skills/` and regenerates its Claude Code copy in `.claude/skills/`. Run `python scripts/sync_skills.py` after a skill changes; add `--check` to report differences without writing. It removes only copies that it generated itself. |

## Conventions

- Prefer the Python standard library. When a script needs packages, use the project-local `.venv` and call its interpreter directly instead of relying on an activated shell.
- Scripts must work on Windows, macOS, and Linux, including paths with spaces and non-ASCII characters.
- Never print credentials or pass them as command arguments; redact them from logs.
- Reading and writing Markdown must never depend on a script.
