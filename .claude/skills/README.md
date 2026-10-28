# Claude Code Skill Mirrors

Generated copies of the canonical skill packages in [`.agents/skills/`](../../.agents/skills/README.md), placed where Claude Code discovers project skills. Each mirror is a regular copy, not a symbolic link, so the workspace works on Windows without special permissions.

## Rules

- Change a skill only in `.agents/skills/<skill-id>/`, then run `python scripts/sync_skills.py` to regenerate its mirror here. `python scripts/sync_skills.py --check` reports any difference between the copies.
- Do not edit a mirror directly; the next regeneration replaces it.
- Each mirror directory has its own generated README that identifies its canonical source.

## Current status

The mirrors of the four MVP 1 skills are generated here: `project-onboarding`, `environment-management`, `privacy-configuration`, and `constraint-maintenance`. All four were accepted by review on 2026-10-28; none is verified on Windows or in Codex. See the [implementation status](../../docs/implementation-status.md).
