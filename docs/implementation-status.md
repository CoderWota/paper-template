# Implementation Status

Agent-maintained record of what has actually been implemented and verified, one entry per MVP from the [MVP implementation guideline](mvp-implementation-guideline.md). A capability counts as working only after its acceptance evidence has been observed. The presence of a directory, a README, or a SKILL.md is not evidence.

Updated: 2026-10-26.

## Summary

| MVP | Researcher-visible outcome | Status |
| --- | --- | --- |
| 1 | Usable project and confirmed memory | In progress: scaffold and adopted AGENTS.md |
| 2 | Flexible intake and MinerU batch ingestion | Planned |
| 3 | Searchable literature and traceable evidence | Planned |
| 4 | Ideas, impact, and feasible research plans | Planned |
| 5 | Evidence-based writing, audit, and major revision | Planned |
| 6 | Journal choice, template-driven layout, and readiness | Planned |
| 7 | Practical Git control and explicit backup | Planned |
| 8 | Review rounds and coauthor reconciliation | Planned |
| 9 | Connected paper hands-on and release candidate | Planned |

Execution order (revised 2026-10-26): 1 → 7 → 2 → 3 → 4 → 5 → 6 → 8 → 9, with the export trial running alongside MVP 7; see the [MVP implementation guideline](mvp-implementation-guideline.md#3-mvp-overview-and-dependencies). The export trial is planned.

No skill is implemented. No end-to-end test has been run.

## MVP 1, partial increment: workspace scaffold

Status: in progress. This increment is narrower than MVP 1 and does not meet its acceptance evidence.

Request: the template maintainer asked to initialize the Git repository, implement the basic project structure described by the design documents, write project documents in English, and delete the Chinese translations (2026-10-26).

Implemented:

- A local Git repository on branch `main`, with no remote.
- `.gitignore` by role, following [design plan Section 13](design-plan.md#13-version-control-and-ignore-policy): credentials (`.env*` except `.env.example`), `.local/`, environments, caches, `.tmp/`, rebuildable previews, Claude Code personal settings, and editor, office, and operating-system artifacts. Documents, templates, and images are not ignored by type. `.gitattributes` normalizes text line endings.
- Every static directory of the [design plan Section 4](design-plan.md#4-proposed-directory-structure) tree, each with a directory-specific English README. Instance directories (`<source-id>/`, `<profile-id>/`, `<venue-id>/`, and so on) are left for the skills that create them.
- Empty-state records that agents can read in a fresh session: `requirements/project.md`, `requirements/writing.md`, `requirements/privacy.md`, `state/current.md`, `references/index.md`, `ideas/index.md`, `research/decisions/index.md`, `manuscript/outline.md`, and `manuscript/manifest.yaml` (no sections).
- A draft `AGENTS.md` following design plan Section 8, and a `CLAUDE.md` that imports it. The draft was adopted later the same day; see the next section.
- `scripts/check_readmes.py`, a standard-library check of the README contract.
- The Chinese translations of the README, design plan, hands-on design, MVP guideline, and workflow review were removed; the maintainer confirmed that they matched the English documents one to one. Links to them were removed or updated.

Deliberately not created yet:

- `code/`: created by `research-code-setup` only when the research needs code (MVP 4).
- `references/bibliography.bib`: the canonical citation-metadata representation is decided in MVP 2; BibTeX is the current proposal.
- Skill packages and their Claude Code mirrors, and the mirror generation and validation step: these arrive with the first implemented skills.
- `.env.example`: credential variable names depend on the verified MinerU route (MVP 2).

Verification observed (macOS, Apple Silicon, Python 3.12.9 and 3.9.6):

- `check_readmes.py` passes on the scaffold (27 project directories).
- On a disposable copy, it ignores intake material in `inbox/`, preview output, `.venv/`, and folders inside an archived original; accepts a README with a byte order mark and non-ASCII text; and reports a missing README, a lowercase `readme.md`, a too-short README, a placeholder marker, and two identical READMEs.
- All relative Markdown links and heading anchors in the repository resolve.

Not verified:

- Loading of `AGENTS.md` and `CLAUDE.md` in fresh Codex and Claude Code sessions.
- Any behavior on Windows, including the README check.

## MVP 1, partial increment: AGENTS.md adoption

Status: the contract text is adopted; its loading in fresh agent sessions has not been observed yet.

The template maintainer reviewed the draft one decision at a time and adopted `AGENTS.md` on 2026-10-26. Decisions:

- Workspace scope: one main manuscript per workspace, including its submission rounds and revisions. Each additional paper uses its own copy of the workspace.
- Research records: `research/feedback/` holds advice and `research/decisions/` holds confirmed choices with their reasons, from the first session. Record formats are refined in MVP 4.
- Record language: records the researcher reads and confirms use the interaction language; agent-facing files and technical metadata stay in English. Agent guidance moved from the requirement files into `requirements/README.md`, so the records themselves can be written entirely in the researcher's language.
- Skill adapters: skills are written once in `.agents/skills/`; `.claude/skills/` holds generated, committed copies with a consistency check. Both arrive with the first skill.
- Adopted with the text: the one-line `CLAUDE.md` import, the rule that no skill can waive the confirmation rules, role identification by the subject of the request, and the ignored local paths `.tools/`, `.cache/`, `.tmp/`, and `.local/`.

Documentation checked on 2026-10-26 (sources linked in [design plan Section 8](design-plan.md#8-agentsmd-and-tool-compatibility)):

- Claude Code reads project skills only from `.claude/skills/`. Version 2.1.277 or later reads `AGENTS.md` directly only when no `CLAUDE.md` exists, and an `@AGENTS.md` import never loads it twice.
- Codex reads repository skills only from `.agents/skills/` and requires `name` and `description`. It reads `AGENTS.md` from the repository root down to the working directory, up to 32 KiB by default, and ignores `CLAUDE.md`.
- Both follow symlinked skill folders, but symlinks fail in Windows clones without symlink support.

Open question for `project-onboarding`: how to treat a workspace copied from one that already holds another paper, including what to keep (such as references) and what to reset or re-check (such as requirements, state, `.venv/`, and local credentials).

## Execution order review (2026-10-26)

The maintainer reviewed the MVP dependencies and confirmed four changes to the [MVP implementation guideline](mvp-implementation-guideline.md):

- MVP 7 (Git) moves to immediately after MVP 1, before MVP 2.
- An export trial, which is not an MVP, runs alongside MVP 7. It decides the publishing engine and the citation and cross-reference syntax before MVP 2 fixes the metadata representation and before MVP 5 fixes the writing conventions.
- `journal-selection` moves from MVP 6 to MVP 4.
- MVP 1 verifies the credential mechanism with a test consumer; MVP 2 verifies the live MinerU credential and the selected service's data-use policy. Read-only MinerU service research starts during MVP 1.

## Remaining for MVP 1

Implement `project-onboarding`, `environment-management`, `privacy-configuration`, and `constraint-maintenance`, with the skill-copy generation and consistency check; guided local credential entry, verified with a test consumer; start the read-only MinerU service research; observe `AGENTS.md` loading in fresh Codex and Claude Code sessions; and run the acceptance scenarios in both agent applications.

## Open items affecting the order

- Result production for the complete-path test: no MVP yet owns producing actual research results. Decide before MVP 9, preferably before MVP 4.
- Verification resources: a Windows test machine matching the baseline (x64 or ARM64), access to Codex, and rights-cleared test fixtures. Without them, MVP 1 and MVP 2 can be implemented but not marked verified.
