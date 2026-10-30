# Claude Code Skill Mirrors

Generated copies of the canonical skill packages in [`.agents/skills/`](../../.agents/skills/README.md), placed where Claude Code discovers project skills. Each mirror is a regular copy, not a symbolic link, so the workspace works on Windows without special permissions.

## Rules

- Change a skill only in `.agents/skills/<skill-id>/`, then run `python scripts/sync_skills.py` to regenerate its mirror here. `python scripts/sync_skills.py --check` reports any difference between the copies.
- Do not edit a mirror directly; the next regeneration replaces it.
- Each mirror directory has its own generated README that identifies its canonical source.

## Current status

The package mirrors are generated from the [canonical skill directory](../../.agents/skills/README.md). `python scripts/sync_skills.py --check` reports the package count and any differences. The availability table in [AGENTS.md](../../AGENTS.md) defines which capabilities are available and their verified limits; [implementation status](../../docs/implementation-status.md) records the evidence. This overview keeps no separate capability list.
