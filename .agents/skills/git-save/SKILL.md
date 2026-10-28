---
name: git-save
description: Use when the researcher asks to save, keep, or mark the current version, a milestone, or the state before a big change. Reviews the intended changes by area, agrees on what the version includes, refuses secrets and oversized files, saves a local checkpoint with a meaningful message, and reports what was saved and what remains, without sending anything to an external copy.
---

# Git save

Outcome: a recognizable local version with a meaningful message, containing exactly the agreed scope, and a short summary of what it saved and what stayed unsaved. No implicit backup or publication.

## Step 1: Review what would be saved

1. Run `python scripts/versions.py inspect`. If there is no history, use `git-setup` first. If an operation is unfinished, use `git-setup` to resolve it first.
2. List the unsaved changes by area. Use `python scripts/versions.py compare` when the researcher wants to see them first.

## Step 2: Agree on the scope

3. The request sets the scope. "Save this version" or "save everything" means all current changes; "save the revised introduction" means that file or section. When unrelated changes are present, such as files from an unfinished task, name them and ask whether to include them. A routine save inside a clear request needs no further approval.
4. Write the message in the interaction language: what changed in research terms, for example "Introduction rewritten around the narrowed question", not "update files".

## Step 3: Save

5. Run one of:

   ```text
   python scripts/versions.py save --message "..." --path manuscript/01-introduction.md [--path ...]
   python scripts/versions.py save --message "..." --all
   ```

6. The script refuses files that look like secrets, files larger than 100 MB, and a scoped save while other changes are already prepared. When it refuses, explain the reason in plain words and agree on the next step: a credential belongs in `.env.local`; a very large file may stay outside the history (`git-setup`); prepared changes can join this version or be saved separately. Use `--allow-large` only after the researcher agrees and knows that online hosts may reject the file.

## Step 4: Report

7. Report the version's short identifier and message, what it saved by area, and what remains unsaved. Say that the version exists only on this computer, and offer `git-backup` when the researcher wants an external copy.

## Completion check

- The saved version contains exactly the agreed scope, with a message in research terms.
- No secret or unexpected large file was saved, and no other prepared change was taken along.
- Nothing was pushed or sent anywhere.
