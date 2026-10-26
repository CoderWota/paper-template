# Claude Code Skill Mirrors

Generated copies of the canonical skill packages in [`.agents/skills/`](../../.agents/skills/README.md), placed where Claude Code discovers project skills. Each mirror is a regular copy, not a symbolic link, so the workspace works on Windows without special permissions.

## Rules

- Change a skill only in `.agents/skills/<skill-id>/`, then regenerate its mirror here and check that the copies match.
- Do not edit a mirror directly; the next regeneration replaces it.
- Each mirror directory has its own README that identifies its canonical source.

## Current status

No skill is implemented yet, so there are no mirrors. The generation and validation step will be added with the first skills (MVP 1 in the [implementation guideline](../../docs/mvp-implementation-guideline.md)).
