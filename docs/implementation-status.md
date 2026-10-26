# Implementation Status

Agent-maintained record of what has actually been implemented and verified, one entry per MVP from the [MVP implementation guideline](mvp-implementation-guideline.md). A capability counts as working only after its acceptance evidence has been observed. The presence of a directory, a README, or a SKILL.md is not evidence.

Updated: 2026-10-26.

## Summary

| MVP | Researcher-visible outcome | Status |
| --- | --- | --- |
| 1 | Usable project and confirmed memory | In progress: workspace scaffold only |
| 2 | Flexible intake and MinerU batch ingestion | Planned |
| 3 | Searchable literature and traceable evidence | Planned |
| 4 | Ideas, impact, and feasible research plans | Planned |
| 5 | Evidence-based writing, audit, and major revision | Planned |
| 6 | Journal choice, template-driven layout, and readiness | Planned |
| 7 | Practical Git control and explicit backup | Planned |
| 8 | Review rounds and coauthor reconciliation | Planned |
| 9 | Connected paper hands-on and release candidate | Planned |

No skill is implemented. No end-to-end test has been run.

## MVP 1, partial increment: workspace scaffold

Status: in progress. This increment is narrower than MVP 1 and does not meet its acceptance evidence.

Request: the template maintainer asked to initialize the Git repository, implement the basic project structure described by the design documents, write project documents in English, and delete the Chinese translations (2026-10-26).

Implemented:

- A local Git repository on branch `main`, with no remote.
- `.gitignore` by role, following [design plan Section 13](design-plan.md#13-version-control-and-ignore-policy): credentials (`.env*` except `.env.example`), `.local/`, environments, caches, `.tmp/`, rebuildable previews, Claude Code personal settings, and editor, office, and operating-system artifacts. Documents, templates, and images are not ignored by type. `.gitattributes` normalizes text line endings.
- Every static directory of the [design plan Section 4](design-plan.md#4-proposed-directory-structure) tree, each with a directory-specific English README. Instance directories (`<source-id>/`, `<profile-id>/`, `<venue-id>/`, and so on) are left for the skills that create them.
- Empty-state records that agents can read in a fresh session: `requirements/project.md`, `requirements/writing.md`, `requirements/privacy.md`, `state/current.md`, `references/index.md`, `ideas/index.md`, `research/decisions/index.md`, `manuscript/outline.md`, and `manuscript/manifest.yaml` (no sections).
- A draft `AGENTS.md` following design plan Section 8, marked as not adopted, and a `CLAUDE.md` that imports it.
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

Remaining for MVP 1: agree on the `AGENTS.md` text; implement `project-onboarding`, `environment-management`, `privacy-configuration`, and `constraint-maintenance` with Codex and Claude Code adapters; guided local credential entry; and the acceptance scenarios in both agent applications.
