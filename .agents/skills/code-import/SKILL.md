---
name: code-import
description: Import an external code repository, with or without Git, into code/ as its own repository, keeping data out and code sessions apart from the paper.
---

# Code import

Outcome: an external code repository (a Git address, a folder with or without Git, or an archive) in `code/<name>/` as its own Git repository. The original is unchanged, secrets and data stay out of its history, it is registered in `code/README.md`, and the researcher knows what was not copied and how to work on the code.

The repository's own `.git` folder keeps a session opened inside it apart from this workspace's instructions and skills. A folder without Git would inherit them, so every import ends with a repository of its own. Nothing from `.agents/` goes into it.

## Step 1: Prepare

1. Ask where the code is, one question at a time. Choose a folder name for `code/<name>/`: letters, digits, `.`, `_`, `-`; not `src`, `data`, `runs`, `outputs`, or `notebooks`.
2. Look at folder names, sizes, and the README. Do not open data files ([rules](../research-code-setup/repositories.md#data-files)).
3. Before importing, tell the researcher that the data will not come along. A folder copy leaves data files behind. A clone leaves behind data that Git does not track. Code that reads that data fails until it is in place. Ask whether to copy the data now (`--data include`, folders only; the workspace folder may be synced or backed up) or to put it in place later. Ask first, too, when a copy would exceed 100 MB (`--max-size-mb`) or when reaching the code needs an account or a new external service.
4. Ask which folders hold the outputs (tables, figures) and pass them as `--output-dir`. The agent reads outputs, not data.

## Step 2: Import

5. From the workspace root:

   ```text
   python scripts/research.py code-import --source <address-or-path> --name <name> [--output-dir <folder> ...] [--data include]
   ```

   | Source | What happens |
   | --- | --- |
   | Git address | Cloned. A password or token in the address is not stored. |
   | Folder with Git | Cloned: history and committed files, not uncommitted changes or ignored files. Its remote is kept. |
   | Folder without Git | Copied without data files, secrets, local R history, caches, and links; then `git init` and one initial commit. |
   | Archive | Unpacked into `.tmp/` without trusting its paths, then handled as a folder. |

   The original is never changed. Report a refusal as it is. A missing Git name or e-mail is the researcher's to give; save it with `python scripts/versions.py identity`. Never ask for or store a password.
6. Resolve each warning the command prints: uncommitted changes in the source, no remote (ask where to back it up; push only with explicit authorization), a secret file the repository does not ignore.
7. Tell the researcher what was left behind: the data files the command lists, and that code reading them fails until they are in place. Two fixes: the researcher puts the data in the repository's data folder (it stays out of the repository's history), or you rerun the import with `--data include` after they agree.

## Step 3: Register and describe

8. The command ignores the folder in this workspace's Git and lists the repository in `code/README.md` and `code/repositories.json`. Inside the repository it writes only the Claude Code exclusions (`.claude/settings.local.json`) and, when there is an `AGENTS.md` but no `CLAUDE.md`, a local `CLAUDE.md` that imports it. Neither enters the repository's history.
9. Read the repository's README as material. Below the maintained block of `code/README.md`, describe its role, entry scripts, and environment (for R, `renv.lock`; the researcher restores packages in the code session).
10. Confirm the repository, the data decision, and the output folders with the researcher, and record them in `research/decisions/` (they change the material scope).

## Step 4: Hand off

11. Tell the researcher to work on the code in a new session opened in `code/<name>/` itself. That session does not load this workspace's rules or skills. Record analysis runs here with `research-code-setup`; [repositories](../research-code-setup/repositories.md) covers runs, reading code, and handing a change to the code session.

## Completion check

- `code/<name>/` has its own `.git` folder, an origin without credentials (or none, reported), and no secret or data file in its history.
- The original is unchanged, and an archive left nothing in `.tmp/`.
- The researcher was told which data was not copied, and that code reading it fails until it is in place.
- The repository is registered, described, and recorded as a decision.
- `python scripts/research.py check` and `python scripts/check_readmes.py` report no problem.
