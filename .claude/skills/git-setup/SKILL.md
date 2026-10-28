---
name: git-setup
description: Use when the researcher wants version history for the workspace, when Git is missing, or when an existing history needs arranging or repair, for example an inherited template history, an origin that points to the template, another paper's history, a tracked secret, files that should not be tracked, or an unfinished merge. Inspects first, explains the choices in plain language, creates or repairs the local history only with the researcher's choice, keeps secrets out, and never rewrites shared history or pushes anything.
---

# Git setup

Outcome: a usable local version history whose tracked scope the researcher understands, with secrets excluded, an author identity set for this workspace, and any inherited or broken state arranged as the researcher chose. Nothing leaves this computer.

## Step 1: Inspect first

1. Run `python scripts/versions.py inspect` and, when the history exists, `python scripts/versions.py scope`. Follow `git-inspection` to understand the state. Reuse an existing history when it serves the paper; never reset it to make setup simpler.

## Step 2: Install Git when it is missing

2. If Git is not installed, use `environment-management`: it explains the installation for this computer (Git for Windows, or the command-line tools on macOS) and installs only with consent. Writing and reading work without Git; say so.

## Step 3: Create a new history

3. Explain in two sentences what a local history does: saved versions on this computer, which can be compared and retrieved; it is not a backup. Ask whether to create it.
4. Agree on what it tracks. By default it tracks the whole workspace except the ignored paths (credentials, environments, caches, previews, temporary files). Ask one question when it matters: large or copyright-restricted originals, research data, or sensitive material may be better kept out, especially if an external copy is planned. Add an ignore rule only for what the researcher chose; never ignore documents, templates, or images by type.
5. Run `python scripts/versions.py init`. It refuses inside another repository and adds the secret exclusions if they are missing.
6. Ask which author name and e-mail to record with saved versions; a placeholder address is fine. Run `python scripts/versions.py identity --name "..." --email "..."`; it applies to this workspace only.
7. Offer to save the first version with `git-save`.

## Step 4: Arrange an inherited history

8. **Template history and an `origin` that is the template.** Explain that the template's development versions came with the copy, and that sending the paper to `origin` would publish it in the template's repository. Recommend keeping the history and renaming that remote, so that no backup can reach it by accident: `git remote rename origin template`. Removing it (`git remote remove origin`) is the alternative. Do it only after the researcher chooses.
9. **Another paper's history or material.** Never delete or rewrite it. Ask whether this workspace continues that paper (keep everything) or whether the new paper should start from a fresh copy of the template, as `project-onboarding` describes. Starting a fresh history inside this folder is a risky recovery: it needs the researcher's explicit choice, and the old `.git` folder is kept, renamed into `.local/`, never deleted.

## Step 5: Repair

10. **A tracked secret.** Stop tracking it with `python scripts/versions.py untrack --path PATH` (the file stays on this computer), then save a version. Explain that earlier versions still contain the secret: if any copy of the history ever left this computer, the researcher should replace the secret at its service. Rewriting history to remove it is a separate major decision with risks; do not do it as part of setup.
11. **Tracked files that the ignore rules exclude** (for example a preview tracked by mistake): `untrack` them after the researcher agrees, then save.
12. **An unfinished merge, rebase, or cherry-pick, or a detached version.** Explain what happened in plain words and what each way out keeps or discards. Prefer the way that preserves both sides, such as finishing or aborting a merge without losing files. Never use a command that discards uncommitted work (`reset --hard`, `checkout -f`, `clean`) and never force-push.

## Step 6: Verify and report

13. Run `python scripts/versions.py inspect` again and report the result: the history exists or was arranged, what it tracks, the identity, and what is still only local.

## Completion check

- The history was created or changed only after the researcher's choice, and inspection preceded every change.
- `.env.local` and other credentials are excluded and untracked; no ignore rule excludes documents by type.
- No history was rewritten, nothing was deleted, and nothing was pushed.
