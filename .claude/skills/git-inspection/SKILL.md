---
name: git-inspection
description: Inspect saved versions, unsaved work, unfinished operations, and backup status without changing files.
---

# Git inspection

Outcome: a plain-language account of the version history: whether Git and a history exist, the saved versions, what is not yet saved (by area, such as manuscript or references), which external copies exist and what is only on this computer, inherited history, unfinished operations, and secret or tracking risks. Nothing is changed.

## Step 1: Read the facts

1. Run `python scripts/versions.py inspect` (use `python3` or `py -3` when `python` is not found). Add `--json` when you need the details. When the question is about what the history covers, also run `python scripts/versions.py scope`.
2. Both commands only read. They do not contact any external copy; what they say about a remote comes from the last time it was fetched.

## Step 2: Interpret

3. **No Git or no history.** Say so plainly. Version history is optional for writing; offer `git-setup` only when the researcher wants saved versions.
4. **Inherited history.** When the history includes the template's own development history, explain that the copy carries the template's versions; this is harmless locally. When an external copy (often `origin`) holds no research versions, it is probably the repository the template was copied from: never send research material there. When versions contain research material that does not belong to this paper, say so and ask before anything changes. In each case, offer `git-setup` to arrange the history; change nothing here.
5. **Unsaved work.** Group it by area and name the important files, for example "manuscript: 2 changed files; references: 1 new source". Point out large files and files that look like secrets.
6. **External copies.** Distinguish local history from an external copy. A remote listed in the configuration is not proof that the latest version is copied there; only `git-backup` checks that.
7. **Problems.** An unfinished merge or rebase, a detached version, a tracked secret, or a tracked file that the ignore rules now exclude: describe the effect in research terms and offer `git-setup` to repair it.

## Step 3: Report

8. Report in the interaction language, in a few lines, without Git jargon unless the researcher uses it. End with one useful next step, such as saving the current work (`git-save`), comparing versions (`git-compare`), or arranging an external copy (`git-backup`).

## Completion check

- Nothing in the workspace or its history changed, and nothing was contacted outside this computer.
- The report separates saved, unsaved, local, and external.
- Inherited history, secret risks, and unfinished operations are mentioned when present, with a next step.
