---
name: manuscript-revision
description: Use when the researcher wants a substantial change to an existing manuscript, such as a changed central argument, a restructured paper, sections split, merged, moved, or removed, genuinely new evidence or analyses, adaptation to a new venue, or major changes requested by reviewers or collaborators. Preserves a recoverable baseline, makes the change concrete in a confirmed plan and an old-to-new map, coordinates the research, outline, writing, and audit skills in resumable steps, reconciles intervening author edits, applies a staged candidate safely, and rechecks everything the change affected. Ordinary edits go to manuscript-writing.
---

# Manuscript revision

Outcome: one clearly identified active manuscript that implements the confirmed revision, with a recoverable baseline, a plan and an old-to-new map in `revisions/<revision-id>/`, current checks of everything the change affected, and honest remaining gaps. A checked revision, a draft that needs more evidence, and a submission-ready package are different outcomes.

## Step 1: Confirm that this is a major revision

1. A changed argument, structure, evidence base, or target qualifies. A wording change, a section polish, or a single correction does not: use `manuscript-writing`, and create no revision record.
2. A venue change can need formatting only. Establish the actual scope before you plan a scientific rewrite.

## Step 2: Preserve the starting point

3. Choose a revision ID such as `2026-11-argument` and keep the baseline:

   ```text
   python scripts/manuscript.py revision-start --id <revision-id> [--include research/results --include code/outputs ...]
   ```

   It copies the manuscript (including unsaved edits), the requirements, the bibliography, and the research plan, with checksums, into `revisions/<revision-id>/baseline/`. Include result records, figures, or data outputs that the revision may change; reference large data by path instead of copying it. When the workspace has a version history, also save the current state as a version (`git-save`). Recovery never depends on Git.
4. Earlier packages in `outputs/releases/` stay untouched.

## Step 3: Make the change concrete

5. Read the question, the argument (`manuscript/outline.md`), the evidence and results, relevant feedback or review items, and the requested goal. Write `revisions/<revision-id>/plan.md` in the interaction language: the goal in the researcher's words; the scope (what may change and what stays); the baseline reference; the affected material (sections, claims, figures and tables, citations, title, abstract, conclusion, methods or materials, venue requirements); whether to work in a staged candidate or in place; the ordered work items with owner and status; and the next action.
6. Map the change in `revisions/<revision-id>/changes.md`: each section, claim, figure, table, and citation that is kept, moved, split, merged, rewritten, or removed, from where to where.
7. The plan changes the argument or the structure, so it is a major decision: present it with your recommendation, ask one question, and wait. After a clear yes, record the decision with `constraint-maintenance`, and update the outline with `manuscript-outline`. A clear instruction that already states the scope is that confirmation; do not ask again for each section.

## Step 4: Revise in recoverable steps

8. Work through the plan with the specialist skills: `research-investigation`, `research-code-setup`, or `literature-and-evidence` for new evidence (missing research stays a gap; never rewrite findings to fit the new narrative), and `manuscript-writing` for text. Mark each work item's status in `plan.md` as it finishes, record actual changes in `changes.md`, and keep `state/current.md` pointing to the next item, so that a fresh session can continue.
9. **Staged candidate**, when alternative structures or a large replacement warrant one: copy the manuscript files (with `manifest.yaml`) into `revisions/<revision-id>/candidate/`, give the folder a README, and edit there. The candidate is never assembled. **In place**, for a bounded revision: edit `manuscript/` directly against the preserved baseline.
10. Keep removed material recoverable: it stays in the baseline, and `changes.md` says where it went.

## Step 5: Apply a candidate safely

11. Run `python scripts/manuscript.py revision-status --id <revision-id>`. Files edited in `manuscript/` since the baseline are intervening edits by the researcher or a coauthor: merge each into the candidate, never overwrite it, and say how you merged it.
12. Apply: `python scripts/manuscript.py revision-apply --id <revision-id> [--reconciled manuscript/<file> ...]`. It keeps the replaced versions and logs every file, so an interruption is detectable; continue it with `--resume`. Files that the candidate does not contain are left in place and listed; remove an obsolete section from the manifest, not from the disk.

## Step 6: Recheck what changed

13. Run `python scripts/manuscript.py check`, `python scripts/manuscript.py checks` (earlier audits and evidence checks whose inputs changed are stale), and `python scripts/research.py check` (stale results). Recheck the support of every changed or moved claim, even when its citation key still resolves, and the whole-manuscript coherence: title, abstract, introduction claims, methods or materials, findings, conclusion, figures, tables, and cross-references. Use `manuscript-audit` and record the checks.
14. Write `revisions/<revision-id>/checks.md` in the interaction language: which inputs (with the check records) were checked, the results, and the remaining gaps. Rebuild and inspect outputs only as the availability table in `AGENTS.md` allows.

## Step 7: Establish the current version

15. Report the research-relevant differences against the baseline (`git-compare` or `revision-status`), the remaining gaps, and the state: checked revision, draft needing evidence, or ready for formatting. The active manuscript is what the manifest lists; the outline and the confirmed requirements match it.
16. When every work item in `plan.md` is done or dropped and the researcher accepts that state, close the revision, whether it was made in place or with a candidate: `python scripts/manuscript.py revision-complete --id <revision-id> [--note "..."]`. It refuses while a candidate is staged but not applied or an application is interrupted. It records the date, whether the work was in place or through a candidate, and how many manuscript problems, open markers, and stale check records remain. It hides none of them: a revision that is closed with stale checks is not a checked revision. Until the record exists, the project status reports the revision as open and suggests continuing it.
17. Abandoning the revision is a risky recovery: ask first, then `python scripts/manuscript.py revision-restore --id <revision-id>`, which copies the baseline back, keeps the current versions, and records the revision as abandoned. Another attempt starts a new revision.

## Completion check

- The baseline was kept before any change and can be restored without Git; earlier releases are untouched.
- The plan and the map were confirmed and kept current; the work can resume from `plan.md` and `state/current.md`.
- No intervening author edit was lost, and an interrupted application can be resumed.
- Changed claims were rechecked; stale checks were redone, not carried forward; research still missing is reported as missing.
- One active manuscript is defined by the manifest, and no candidate was assembled by accident.
- A finished revision is closed with `revision-complete`, and an abandoned one with `revision-restore`, so that the project status no longer reports it as open.
