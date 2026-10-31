# Environment Management

Keeps this computer ready for the work you ask for, with no programming on your part. The agent checks the operating system, processor, memory, storage, and installed tools; reuses what already works; sets up project environments only when a task needs them; and helps you enter API keys privately. It installs or changes nothing without your consent.

A request to initialize this workspace includes the standard local installation and checks for the official Sciverse and MinerU cloud MCP tools, plus checking for `pdftotext` and installing Poppler if it is missing. The assistant does not ask for the same installation consent again. Base-runtime changes and sending queries or documents remain separate choices.

Ask, for example: "Check whether this computer is ready to import PDFs." or "Something is missing. Please fix the setup."

## Private API keys

When a service that you chose needs a key, a one-time page opens in your browser on this computer. You type the key there, never in the conversation. The key is saved in `.env.local`, which Git ignores. The file is not encrypted, so do not share it.

The agent instructions are in [SKILL.md](SKILL.md). The skill uses `scripts/inspect_environment.py` and `scripts/credentials.py`. Related skills: `project-onboarding` and `privacy-configuration`.

The [private credential procedure](credential-entry.md) is loaded only when a supported, chosen service actually needs a key; it is not required for an ordinary readiness check.
