---
name: environment-management
description: Use when the researcher asks whether this computer is ready for a task, such as importing PDFs, says that something is missing or does not work, or when onboarding or another task needs a tool, a Python environment, or a credential. Checks and prepares this computer for the workspace without requiring programming knowledge. Inspects the operating system, processor, memory, storage, and installed tools; reuses compatible tools; creates project environments only when a task needs them; guides private local entry of API keys; and repairs broken setups.
---

# Environment management

Outcome: a working setup for the task at hand, or one exact, plain next step. Secrets never appear in the conversation, in command arguments, or in logs.

## Rules for this skill

- Follow `AGENTS.md`. Installing, upgrading, or removing software and changing a system setting are decisions: explain the effect, recommend one option, and wait for explicit consent.
- Inspect before you change anything. Reuse a compatible installed tool. Never upgrade or replace a working global installation to suit this workspace.
- Prefer per-user installations that need no administrator rights. Basic work never needs Docker, WSL, a GPU, or a local model.
- A missing tool must not block unrelated work. Reading and writing Markdown never needs a tool.
- Never read `.env.local` yourself or print a value from it.
- Keep what you observed separate from what you assume. Do not say that a setup works until you have run it.
- Before you say whether this computer is ready for a task, run the inspection in step 1. Say what still works without the missing tool; reading and writing Markdown never needs one. Ask at most one question in that report.

## Step 1: Inspect the computer

If Python works, run `python scripts/inspect_environment.py` from the workspace root. On Windows, try `py -3 scripts\inspect_environment.py` when `python` is not found. The report changes nothing.

If no Python works, use the shell's own commands to find the operating system, the processor architecture, and which Python commands exist. On Windows, a `python` command inside `WindowsApps` is usually only a Microsoft Store alias.

## Step 2: Compare the setup with the task

State only what the current task needs:

- Reading and writing Markdown: nothing.
- Workspace scripts: Python 3.9 or later (the tested versions are 3.9 and 3.12).
- Document parsing, export, or research code: the requirements of that integration, from its current official documentation. For MinerU on this computer, `python scripts/setup_mineru.py check` reports the installation, the models, and the free disk space; `source-ingestion` describes the routes and tiers. Check the processor architecture: an x64 package can fail, or run slowly under emulation, on ARM64 Windows.

Use the path notes from the report: spaces or non-ASCII characters, a long Windows path, or a cloud-synced folder such as OneDrive, where `.venv/` and caches cause sync conflicts. Mention a risk only when it affects the task.

## Step 3: Install or repair, with consent

1. Explain in plain words what is missing and what it prevents.
2. Recommend one option. Prefer a per-user installation from the official source, for example Python from python.org. Read the current official installation instructions for this operating system and architecture before you guide the researcher; do not rely on remembered steps.
3. Wait for explicit consent. Then do the steps that you can do, and guide the researcher through the steps that only they can do, one at a time, in their language.
4. Run the inspection again and confirm the result.

## Step 4: Project environments

- Create `.venv/` only when a workspace script needs packages: `python -m venv .venv`. Call `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` directly. Do not rely on an activated shell.
- Install packages from the dependency file that the script declares, and record the installed versions. If `uv` is installed, you can use it; never require it.
- Put a heavy tool, such as a local document parser, in its own environment under `.tools/<tool>/`, so that it cannot break the workspace scripts or the research code.
- If the workspace folder moved and `.venv/` no longer runs, delete it and create it again from the dependency file. Ask before you delete a tool environment that took a long time to install.

## Step 5: Credentials

Do this only for a service that the researcher chose and that needs a credential. An AI application subscription does not mean that a separate API key is necessary.

Before you look for a key page or start the entry, check that a skill in `.agents/skills/` or a script in `scripts/` uses the credential. If none does yet, the credential is not needed now. Say so plainly in the researcher's own terms, for example "importing documents is not available yet, so you do not need a key now". Note the credential as deferred in `state/current.md`. Do not look up the key page or the variable name, and do not collect a value. The exception is a test value that the researcher asks for in order to try the private entry page: it needs no integration.

1. Find the exact variable name and the official page where the researcher gets the value, from the integration's documentation.
2. Explain what the credential allows and where it is stored: `.env.local`, which Git ignores but which is not encrypted.
3. Start the private entry page in the background, so that it can wait for the researcher (up to 10 minutes by default). Write the page texts in the researcher's language:

   ```text
   python scripts/credentials.py set NAME --title "..." --label "..." --note "..." --help-url "https://..." --button "..." --done-message "..." --invalid-message "..."
   ```

   The page opens in the researcher's browser and works only on the computer that runs the command. If the browser does not open, give the researcher the printed address.
4. Tell the researcher to enter the value on that page, not in the conversation. Wait until the command reports `Saved` or `Replaced`.
5. Confirm with `python scripts/credentials.py status NAME`. It shows only whether the value is set and its length.

A program receives the value through `python scripts/credentials.py run --only NAME -- <command>`, or a workspace script reads it with `load_env_local()` from `scripts/credentials.py`. Never put a value in a command argument.

If the researcher pastes a credential into the conversation, do not repeat it and do not store it from the conversation. Recommend that they revoke it at the provider, create a new one, and enter the new one on the private page.

If the command refuses because Git does not ignore `.env.local`, or already tracks it, fix that first. Never weaken this check.

## Step 6: Verify and report

- Prove the setup with the smallest real use: a version command, the script itself, or a documented check that sends no research content. If a credential can only be checked by real processing, say that it stays unverified until the first authorized job.
- Report one status in the researcher's language: ready, incomplete, or needs attention. Say what works, what is missing, and one plain next step.
- Machine-specific facts stay on this computer; do not write them into shared requirements. Update `state/current.md` only when work remains.

## Common problems

| Problem | Response |
| --- | --- |
| Python is not found, or only the Microsoft Store alias exists | Go to step 3 and recommend a per-user installation. |
| `.venv/` stopped working after the folder moved | Create it again (step 4). |
| An installation needs administrator rights | Look for a per-user alternative. If there is none, explain the exact requirement and let the researcher decide. |
| A credential is rejected or expired | Ask the researcher to get a new value from the official page, then enter it again (step 5). |
| The workspace is in a cloud-synced folder | Explain the sync conflicts and suggest a local folder. Moving the workspace is the researcher's choice. |
| The researcher wants a service for which no skill or script exists yet | Say that it is not available yet, note the credential as deferred in `state/current.md`, and collect no value (step 5). |
| A tool has the wrong architecture or version | Explain the supported options. Do not replace a working global tool without consent. |
