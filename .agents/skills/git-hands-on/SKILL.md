---
name: git-hands-on
description: Guide practical version-control learning on a separate practice copy, with the agent operating Git.
---

# Git hands-on

Outcome: the researcher understands, through their own tasks, how versions are inspected, saved, compared, retrieved, and backed up, while the agent operates Git. Real work is never put at risk for a lesson.

## How to guide

- One step at a time: say what the step does and why it is useful, carry it out, show the visible result, and ask what to do next. No command memorization, quizzes, or branch and rebase lessons unless the researcher asks.
- Each step uses the procedure of its skill; do not repeat those procedures here. A direct request ("save this version") goes to its skill without a lesson.
- Resume from `state/current.md`, where an unfinished lesson notes its next step.

## Step 1: Start from the real state

1. Use `git-inspection` and explain what the workspace has: history or not, unsaved work, external copies. If there is no history, use `git-setup` with the researcher's choice.

## Step 2: Practice safely

2. Create the practice copy: `python scripts/versions.py practice`. It is a separate folder (`.tmp/git-practice/`) with its own short history of a practice note, so nothing that happens there touches the paper.
3. Practice there with the same commands and `--root .tmp/git-practice`: list the versions (`history`), compare two of them (`compare --words`), retrieve the first paragraph from the oldest version (`retrieve`), and restore the note to an earlier version (`restore`), showing where the current content was kept. Then save the practice result (`save`). `--reset` starts the practice copy again.

## Step 3: Apply to the paper

4. Move to the researcher's real tasks: save the current state with a meaningful message (`git-save`), compare it with an earlier version (`git-compare`), and retrieve an earlier passage when one is wanted (`git-recovery`). Retrieval is the default; a restore in place needs the researcher's explicit choice.
5. Explain local history versus an external copy. Offer `git-backup` only when the researcher wants an external copy; a lesson never creates a remote or pushes.

## Step 4: Close or pause

6. Summarize what the researcher can now ask for in ordinary words, for example "save this version", "show what changed since yesterday", or "bring back the paragraph I deleted". When the lesson stops early, record the next step in `state/current.md`.

## Completion check

- Practice happened on the practice copy; the paper and its history changed only through the researcher's real requests.
- Every step was carried out by the agent through the matching skill, and its result was shown.
- No remote was created, nothing was pushed, and no history was rewritten during the lesson.
