# Major Revisions

Records for substantial manuscript revisions: a changed central argument, a restructured paper, genuinely new evidence, or adaptation to a new venue. They can be used before submission or in response to feedback. Ordinary edits do not create a revision record.

## Each revision directory

One subdirectory per major revision, created only when the scale warrants it: `<revision-id>/`.

```text
<revision-id>/
├── README.md      # Goal, current state, and where the active manuscript stands
├── baseline/      # The starting version: manuscript, requirements, bibliography, plan, and included files
├── baseline.json  # Checksums of the baseline and the Git version, if any
├── plan.md        # Baseline reference, your goal and scope, affected material, ordered work, next action
├── changes.md     # Old-to-new mapping of sections, claims, figures, and citations, and the actual changes
├── checks.md      # Which input versions were checked, with what result, and the remaining gaps
├── candidate/     # Optional staged manuscript, never assembled until it is applied
├── apply.json     # The log of applying the candidate, so an interruption can be resumed
├── closed.json    # Written when the revision is completed or abandoned: the outcome, the date, in place or candidate, and what was still open
└── replaced/      # Versions that an application or a restore replaced
```

`python scripts/manuscript.py` keeps the baseline (`revision-start`), compares the workspace and the candidate with it (`revision-status`), applies the candidate (`revision-apply`, with `--resume` after an interruption), records a finished revision, made in place or with a candidate (`revision-complete`), and copies the baseline back and records the revision as abandoned (`revision-restore`). A revision without `closed.json` is reported as open by the project status.

The agent creates each of these folders with its own README.

For a staged candidate, `python scripts/manuscript.py set-sections --revision-id <id> FILE ...` replaces only the candidate's ordered section list; include the complete list of sections to keep. `python scripts/manuscript.py check --revision-id <id>` checks its own manifest, metadata, text, labels, and assets against the workspace bibliography. Neither command changes the active manuscript. They require an existing candidate and baseline and refuse a closed revision or one whose application has begun. Check the active manuscript again after `revision-apply`; candidate checks do not establish that intervening edits were reconciled or that the science is supported.

## Rules

- The starting version is preserved and recoverable before any change, with or without Git.
- A changed claim, figure, analysis, section, or output profile makes the affected earlier checks stale. An old passed check is never carried forward as proof.
- There is always one clearly identified active manuscript in [`manuscript/`](../manuscript/README.md). Candidate drafts are kept apart and applied deliberately, and intervening author edits are reconciled, not overwritten.
- Earlier submitted packages in [`outputs/releases/`](../outputs/releases/README.md) remain unchanged.

## Who edits what

Describe the change you want, for example: "Restructure this paper around the revised question. Preserve the current version, show what must change, and check the evidence and whole manuscript after rewriting." The agent preserves the baseline, maps the impact, asks you to confirm the plan, and coordinates the work.

Related skill: `manuscript-revision`.
