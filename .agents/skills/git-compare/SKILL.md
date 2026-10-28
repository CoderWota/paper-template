---
name: git-compare
description: Use when the researcher asks what changed, wants to compare the current text with an earlier version or two saved versions, or wants to see the differences before saving, recovering, or choosing a draft. Identifies the versions from dates, messages, or descriptions, summarizes the differences by area, shows the changed words for prose, and explains the research-relevant differences such as claims, sections, citations, and figures, without changing anything.
---

# Git compare

Outcome: an understandable comparison: which versions were compared, what changed by area, where the important edits are, and what they mean for the paper. Nothing is changed.

## Step 1: Identify the versions

1. Run `python scripts/versions.py history [--path PATH]` to list the saved versions with their dates and messages. Match the researcher's description ("yesterday's version", "before the reviewer changes") to a version, and say which one you chose. Ask only when two versions fit equally well.
2. The default comparison is the last saved version against the current files.

## Step 2: Compare

3. Summarize by area:

   ```text
   python scripts/versions.py compare [--from VERSION] [--to VERSION] [--path PATH ...]
   ```

   It lists added, changed, renamed, deleted, and never-saved files with line counts, grouped by area.
4. For prose, show the changed words of the relevant files: `python scripts/versions.py compare --words --path manuscript/02-methods.md [--from ...] [--to ...]`. Read the output; do not paste long raw diffs to the researcher.

## Step 3: Explain

5. Explain the differences that matter for the research: claims added, removed, or weakened; sections moved, split, or merged; citations added or removed; figures, tables, and equations changed; requirements or plans changed. Give the location of each important edit (file and section).
6. Separate wording changes from changes of meaning. Do not judge which version is better unless asked; when asked, say what the judgment rests on.

## Step 4: Report

7. Report in the interaction language: the two versions compared, the important differences with locations, and the next useful step, such as saving (`git-save`) or retrieving earlier text (`git-recovery`).

## Completion check

- The compared versions are named, with how they were chosen.
- The differences are explained in research terms with locations, not as a raw diff.
- Nothing changed in the workspace or its history.
