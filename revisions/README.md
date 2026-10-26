# Major Revisions

Records for substantial manuscript revisions: a changed central argument, a restructured paper, genuinely new evidence, or adaptation to a new venue. They can be used before submission or in response to feedback. Ordinary edits do not create a revision record.

## Each revision directory

One subdirectory per major revision, created only when the scale warrants it: `<revision-id>/`.

```text
<revision-id>/
├── README.md    # Goal, current state, and where the active manuscript stands
├── plan.md      # Baseline reference, your goal and scope, affected material, ordered work, next action
├── changes.md   # Old-to-new mapping of sections, claims, figures, and citations, and the actual changes
├── checks.md    # Which input versions were checked, with what result, and the remaining gaps
└── candidate/   # Optional staged manuscript, never assembled until it is applied
```

The agent creates each of these folders with its own README.

## Rules

- The starting version is preserved and recoverable before any change, with or without Git.
- A changed claim, figure, analysis, section, or output profile makes the affected earlier checks stale. An old passed check is never carried forward as proof.
- There is always one clearly identified active manuscript in [`manuscript/`](../manuscript/README.md). Candidate drafts are kept apart and applied deliberately, and intervening author edits are reconciled, not overwritten.
- Earlier submitted packages in [`outputs/releases/`](../outputs/releases/README.md) remain unchanged.

## Who edits what

Describe the change you want, for example: "Restructure this paper around the revised question. Preserve the current version, show what must change, and check the evidence and whole manuscript after rewriting." The agent preserves the baseline, maps the impact, asks you to confirm the plan, and coordinates the work.

Related skill: `manuscript-revision`.
