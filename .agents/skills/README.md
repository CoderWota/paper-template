# Canonical Skill Packages

Each subdirectory is one skill: a complete task that a researcher can request in ordinary language, such as importing a folder of PDFs or comparing two versions. This is the single authoritative copy of every skill. Claude Code mirrors are generated from it in [`.claude/skills/`](../../.claude/skills/README.md); never maintain two independent versions.

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

The four MVP 1 skills, `project-onboarding`, `environment-management`, `privacy-configuration`, and `constraint-maintenance`, and the two MVP 2 skills, `source-ingestion` and `review-ingestion`, are implemented. The MVP 2 skills were accepted by review on 2026-10-28 (see the [acceptance records](../../docs/acceptance/README.md)); no package is verified on Windows or in Codex. See the [implementation status](../../docs/implementation-status.md). The planned catalog, with each skill's responsibility and boundaries, is in [design plan Section 9](../../docs/design-plan.md#9-skill-architecture-and-standalone-task-catalog). The implementation order is in the [MVP implementation guideline](../../docs/mvp-implementation-guideline.md#4-complete-skill-to-mvp-assignment). A package counts as implemented only after its acceptance checks pass, not when its SKILL.md exists.
