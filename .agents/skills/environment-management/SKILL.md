---
name: environment-management
description: Check computer readiness or set up missing tools and private credentials when a research task needs them. Use for setup requests and for setup handoffs from task-specific skills.
---

# Environment management

Outcome: a working setup for the task at hand, or one exact, plain next step. Secrets never appear in the conversation, in command arguments, or in logs.

## Rules for this skill

- Follow `AGENTS.md`. Installing, upgrading, or removing software and changing a system setting are decisions: explain the effect, recommend one option, and wait for explicit consent unless a confirmed project requirement already authorizes that exact scoped setup.
- A request to initialize this workspace authorizes the pinned Sciverse and MinerU MCP installation in `.tools/mcp/`, configuration, and protocol checks, plus checking for `pdftotext` and installing Poppler if it is missing. Follow `project-onboarding` without another installation question for these items. This does not authorize base-runtime installation, replacing a working tool, unrelated upgrades, credentials, queries, or uploads.
- Inspect before you change anything. Reuse a compatible installed tool. Never upgrade or replace a working global installation to suit this workspace.
- Prefer per-user installations that need no administrator rights. Basic work never needs Docker, WSL, a GPU, or a local model.
- A missing tool must not block unrelated work. Reading and writing Markdown never needs a tool.
- Never read `.env.local` yourself or print a value from it.
- Keep what you observed separate from what you assume. Do not say that a setup works until you have run it.
- Before you say whether this computer is ready for a task, run the inspection in step 1. Say what still works without the missing tool; reading and writing Markdown never needs one. Ask at most one question in that report.

## Step 1: Inspect the computer

If Python works, run `python scripts/inspect_environment.py` from the workspace root. When `python` is not found, try `python3 scripts/inspect_environment.py` (macOS and Linux) or `py -3 scripts\inspect_environment.py` (Windows). The report changes nothing.

If no Python works, use the shell's own commands to find the operating system, the processor architecture, and which Python commands exist. On Windows, a `python` command inside `WindowsApps` is usually only a Microsoft Store alias.

## Step 2: Compare the setup with the task

State only what the current task needs:

- Reading and writing Markdown: nothing.
- Workspace scripts: Python 3.9 or later (the tested versions are 3.9 and 3.12).
- Standard MCP tools: `python scripts/setup_mcp.py check` reports pinned packages, protocol discovery, client configurations, and credential presence. Setup needs Python 3.11+ and Node.js 18+ with npm; it does not need local MinerU models.
- PDF text extraction: `pdftotext` from Poppler. Project initialization checks for it and installs Poppler if missing; verify with `pdftotext -v`. This does not authorize converting or uploading a document.
- Document parsing, export, or research code: the requirements of that integration, from its current official documentation. MinerU runs remotely through the official MCP and is limited to reference materials; no local MinerU models or parser are installed. `source-ingestion` describes the approved route. Check the processor architecture for other parsers: an x64 package can fail, or run slowly under emulation, on ARM64 Windows.

Use the path notes from the report: spaces or non-ASCII characters, a long Windows path, or a cloud-synced folder such as OneDrive, where `.venv/` and caches cause sync conflicts. Mention a risk only when it affects the task.

## Step 3: Install or repair, with consent

1. Explain in plain words what is missing and what it prevents. For `pdftotext` during project initialization, the confirmed project requirement already authorizes installing Poppler if missing.
2. Recommend one option. Prefer a per-user installation from the official source, for example Python from python.org. Read the current official installation instructions for this operating system and architecture before you guide the researcher; do not rely on remembered steps.
3. Wait for explicit consent unless the exact installation is already authorized by a confirmed project requirement. Then do the steps that you can do, and guide the researcher through the steps that only they can do, one at a time, in their language.
4. Run the inspection again and confirm the result.

## Step 4: Project environments

- Create `.venv/` only when a workspace script needs packages: `python -m venv .venv`. Call `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` directly. Do not rely on an activated shell.
- Install packages from the dependency file that the script declares, and record the installed versions. If `uv` is installed, you can use it; never require it.
- Put a heavy tool, such as a local document parser, in its own environment under `.tools/<tool>/`, so that it cannot break the workspace scripts or the research code.
- If the workspace folder moved and `.venv/` no longer runs, delete it and create it again from the dependency file. Ask before you delete a tool environment that took a long time to install.

## Step 5: Credentials, only when needed

When a task-specific skill identifies a supported service that the researcher chose and its data/query scope is confirmed, follow [private credential entry](credential-entry.md) as part of that task. Do not wait for the researcher to request environment setup separately. A subscription does not imply a separate API key is needed. Do not read local secret values or request them in conversation. Credential entry does not authorize sending queries or documents to the service.

## Step 6: Verify and report

- Prove the setup with the smallest real use: a version command (for `pdftotext`, `pdftotext -v`), the script itself, or a documented check that sends no research content. If a credential can only be checked by real processing, say that it stays unverified until the first authorized job.
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
