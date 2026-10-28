# Scripts

Reusable automation for operating this workspace, such as checks, conversion adapters, and build steps. The agent writes and runs these scripts; researchers never need to run or edit them.

Research analysis code is kept separately in `code/`, which is created only when a project needs it (`research-code-setup`), so that workspace tools cannot destabilize an analysis environment.

## Current scripts

| Script | Purpose |
| --- | --- |
| [`check_readmes.py`](check_readmes.py) | Checks that every project directory has a meaningful, directory-specific README, following the contract in [design plan Section 4](../docs/design-plan.md#directory-readme-contract). Run `python scripts/check_readmes.py`; it exits with status 1 and lists the problems when a check fails. |
| [`check_capabilities.py`](check_capabilities.py) | Checks that the "Available now" table in `AGENTS.md` matches the skills folder: every skill is listed, every named skill or script exists, and no skill is named as "Not available yet". Run `python scripts/check_capabilities.py`. |
| [`check_requirements.py`](check_requirements.py) | Checks the form of the writing rules in `requirements/writing.md`: each rule has a rule, a scope, and a confirmation that quotes the researcher; examples and exceptions appear only with a quotation. |
| [`inspect_environment.py`](inspect_environment.py) | Reports the operating system, processor architecture (including emulation), memory, free storage, Python interpreters, optional tools, workspace path risks, and project-local setup, without changing anything. Add `--json` for a machine-readable report. |
| [`credentials.py`](credentials.py) | Stores credentials in the ignored `.env.local` without showing them: `set` opens a one-time page on this computer for private entry, `status` shows only whether a name is set, `remove` deletes one value, and `run` passes values to another program. It refuses to store anything when Git could track `.env.local`. |
| [`sync_skills.py`](sync_skills.py) | Validates each canonical skill package in `.agents/skills/` and regenerates its Claude Code copy in `.claude/skills/`. Run `python scripts/sync_skills.py` after a skill changes; add `--check` to report differences without writing. It removes only copies that it generated itself. |

Automated tests for these scripts are in [`tests/`](tests/README.md). Run them after changing a script.

## Conventions

- Prefer the Python standard library. When a script needs packages, use the project-local `.venv` and call its interpreter directly instead of relying on an activated shell.
- Scripts must work on Windows, macOS, and Linux, including paths with spaces and non-ASCII characters.
- Never print credentials or pass them as command arguments; redact them from logs.
- Reading and writing Markdown must never depend on a script.
