# Canonical Skill Packages

Each accepted subdirectory is one skill: a complete task that a researcher can request in ordinary language, such as importing a folder of PDFs or comparing two versions. In-progress drafts may also be present, but the availability table in `AGENTS.md` is authoritative. This is the single source for every skill. Claude Code mirrors are generated from it in [`.claude/skills/`](../../.claude/skills/README.md); never maintain two independent versions.

## Package layout

```text
<skill-id>/
├── README.md   # Short introduction for people: the task, its outcome, and a link to SKILL.md
└── SKILL.md    # Agent instructions: triggers, inputs, records to read, outputs, checks, handoff
```

A package can add reference files or scripts that its SKILL.md uses. Deterministic scripts shared by several skills belong in [`scripts/`](../../scripts/README.md).

## Writing a skill

- Name the directory with the skill id from the catalog, in lowercase words joined by hyphens (for example `source-ingestion`).
- Keep the SKILL.md frontmatter to the fields both agent applications support: `name` (equal to the directory name) and `description`. Keep each field on one line, and quote a value that contains `: `.
- Write in English. Follow [`AGENTS.md`](../../AGENTS.md); do not copy shared rules, such as decision confirmation, the question format, or the README contract, into each skill.
- A skill that creates a project directory also writes that directory's README.
- After every change, run `python scripts/sync_skills.py` to regenerate the Claude Code copy, then `python scripts/sync_skills.py --check`.

## Current status

All 33 skills of the catalog are implemented. The MVP 1 to MVP 4 and MVP 7 skills were accepted by written review on 2026-10-28, and the MVP 5, 6, 8, and 9 skills on 2026-10-29 (see the [MVP 1](../../docs/acceptance/mvp-1-skill-review.md), [MVP 2](../../docs/acceptance/mvp-2-skill-review.md), [MVP 3](../../docs/acceptance/mvp-3-skill-review.md), [MVP 4](../../docs/acceptance/mvp-4-skill-review.md), [MVP 5](../../docs/acceptance/mvp-5-skill-review.md), [MVP 6](../../docs/acceptance/mvp-6-skill-review.md), [MVP 7](../../docs/acceptance/mvp-7-skill-review.md), [MVP 8](../../docs/acceptance/mvp-8-skill-review.md), and [MVP 9](../../docs/acceptance/mvp-9-skill-review.md) skill reviews). The availability table in `AGENTS.md` lists each capability with its verified limits. Windows and Codex operation remain unverified. See the [implementation status](../../docs/implementation-status.md). The full catalog and implementation order are in [design plan Section 9](../../docs/design-plan.md#9-skill-architecture-and-standalone-task-catalog) and the [MVP implementation guideline](../../docs/mvp-implementation-guideline.md#4-complete-skill-to-mvp-assignment). A package counts as accepted only after a written review against its requirements passes, not when its SKILL.md exists.
