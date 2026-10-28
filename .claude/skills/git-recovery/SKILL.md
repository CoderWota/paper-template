---
name: git-recovery
description: Use when the researcher wants earlier content back, such as a deleted paragraph, an older section, a figure, or a whole earlier version of a file or folder, or wants to undo changes. Finds the right version, retrieves earlier content without touching current files, restores in place only with the researcher's explicit choice of scope after keeping a copy of the current content, and explains what changed and how to return, without rewriting history.
---

# Git recovery

Outcome: the requested earlier material, either as a separate copy next to the current work or restored in place within the scope the researcher chose, with the current content kept and a clear way back.

## Step 1: Find the material

1. Run `python scripts/versions.py history --path PATH` and, if needed, `git-compare` to find the version that holds the wanted material. Confirm the version with the researcher by its date and message when the request is not precise.

## Step 2: Retrieve without changing anything

2. Retrieval is the default:

   ```text
   python scripts/versions.py retrieve --rev VERSION --path PATH
   ```

   It writes the earlier file or folder under `.tmp/recovered/<version>/` and leaves the current files alone. Show the researcher the recovered passage itself, not only the file location.
3. Putting a recovered paragraph back into the manuscript is a manuscript edit: make it as `manuscript-writing` allows, at the place the researcher names.

## Step 3: Restore in place only on an explicit choice

4. Restoring replaces current files and is a risky recovery. Before you ask, show the scope (which files), what would be replaced, and the unsaved changes that it affects (`git-compare`). Recommend the smallest scope that meets the request. Ask one question and wait for a clear yes.
5. Run `python scripts/versions.py restore --rev VERSION --path PATH`. It copies the current content to `.tmp/recovered/before-restore-<time>/` first, writes the earlier version, leaves files that did not exist then in place, and saves nothing.
6. Offer to save the result as a new version with `git-save`. History is never rewritten: no `reset --hard`, no `checkout -f`, no `clean`, and no force-push. An earlier version stays reachable after a restore.

## Step 4: Report

7. Report what was recovered or restored, from which version, where the previous content was kept, and how to return to it.

## Completion check

- Retrieval left current files unchanged; a restore happened only after the researcher's explicit choice of scope.
- The current content was kept before anything was replaced, and the way back is stated.
- No history was rewritten and nothing was deleted.
