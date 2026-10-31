# Project Requirements

Status: not initialized. The research goal, manuscript language, and interaction language are unconfirmed.

## Standard MCP installation during initialization

- Rule: Workspace initialization includes installing the pinned official Sciverse and MinerU cloud MCP packages inside the repository, configuring Codex and Claude Code, and checking MCP protocol and tool discovery. Provide installation, checking, and launch scripts. Missing credentials do not block installation; installation does not authorize research queries or document uploads.
- Scope: This template's initialization workflow, in both clients.
- Confirmed: 2026-10-30; "The repository initialization should include MCP installation." The researcher explicitly requested implementation of the plan for both official MCP servers and both clients.

## PDF text extraction during initialization

- Rule: During project initialization, check for `pdftotext`; install Poppler if it is missing and verify the command. Reuse an existing working installation. This setup does not authorize processing or uploading documents.
- Scope: This template's initialization workflow, in both clients.
- Confirmed: 2026-10-31; "Include `pdftotext` in the scope of project initialization."

## Sciverse and MinerU calls through MCP

- Rule: Skills and scripts in this workspace make Sciverse and MinerU service calls only through the installed official MCP servers. No direct API fallback is used. MinerU runs remotely only and may process reference materials only; see `requirements/privacy.md` for the confirmed document scope. Credential and search-query scopes remain in force.
- Scope: This template's skills, scripts, and documents, in both clients.
- Confirmed: 2026-10-31; "Make sure every skill in the repository that involves Sciverse or MinerU calls the MCP." "Check all Agent calls in the repository." "We will not run MinerU locally; send processing remotely." "Only reference materials may be uploaded."

## Clear communication in all languages

- Rule: Questions and explanations to the researcher use short sentences, common words, one question at a time, and the conclusion first. Details are in `AGENTS.md` (Language). English also follows ASD-STE100.
- Scope: This project, long term, in both clients. Manuscript prose is excluded; see [writing.md](writing.md).
- Confirmed: 2026-10-30; "I want the AI to follow ASD-STE100 when it asks users questions or gives explanations, instead of producing a series of confusing questions." "Across all languages."

## English project documents

- Rule: Write project documents, records, and quoted researcher instructions in English, without translation labels.
- Scope: Requirements, state, and other project documents and records, in both clients. Conversation and manuscript languages are separate settings. Manuscript text intended for publication is excluded.
- Confirmed: 2026-10-30; "Do not write documents in Chinese." "Write the quoted words in English too." "You do not need to label them as translations."

## Working drafts and publication language

- Rule: Preserve researcher-authored notes and working drafts in their own language, which may differ from the target paper language. Write text prepared for publication, including body, headings, abstract, figure and table captions and descriptions, and publication metadata, in the language the researcher specifies for the paper. Do not translate working material without a request.
- Scope: Researcher-authored raw material and manuscript work; target publication content in both clients. Agent-written project records remain in English.
- Confirmed: 2026-10-30; "Use the language the user specifies for the paper text. Use English for project records. The manuscript can be in any language." "The paper text and working manuscript may be in different languages. For example, a student may have to publish in English but still record ideas in Chinese." "Figure and table descriptions follow the paper text language."

## Task-specific assessment guidance

Read [research assessment requirements](research-assessment.md) for idea development, originality checks, impact assessment, or mock review. Other tasks do not need this guidance.
