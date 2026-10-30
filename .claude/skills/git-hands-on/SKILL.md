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

2. Create the empty practice copy: `python scripts/versions.py practice`. In `.tmp/git-practice/`, write an English README explaining that this is a disposable lesson copy and a short neutral `practice-note.md` that is not research material. Save the first version with `python scripts/versions.py --root .tmp/git-practice save --path README.md --path practice-note.md --message "Start the practice note"`.
3. Make one small change to the practice note and save a second version with an agent-written message. Practice listing the versions (`history`), comparing them (`compare --words`), retrieving the first paragraph from the oldest version (`retrieve`), and restoring the note to an earlier version (`restore`), showing where the current content was kept. Then change the note once more and save the practice result. `--reset` starts the practice copy again.

## Step 3: Apply to the paper

4. Move to the researcher's real tasks: save the current state with a meaningful message (`git-save`), compare it with an earlier version (`git-compare`), and retrieve an earlier passage when one is wanted (`git-recovery`). Retrieval is the default; a restore in place needs the researcher's explicit choice.
5. Explain local history versus an external copy. Offer `git-backup` only when the researcher wants an external copy; a lesson never creates a remote or pushes.

## Step 4: Close or pause

6. Summarize what the researcher can now ask for in ordinary words, for example "save this version", "show what changed since yesterday", or "bring back the paragraph I deleted". When the lesson stops early, record the next step in `state/current.md`.

## Completion check

- Practice happened on the practice copy; the paper and its history changed only through the researcher's real requests.
- Every step was carried out by the agent through the matching skill, and its result was shown.
- No remote was created, nothing was pushed, and no history was rewritten during the lesson.
