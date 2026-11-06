# Project Requirements

Status: not initialized. This workspace contains no imported manuscript yet. During manuscript import, populate the research goal and paper language from the draft as described below. Confirm the interaction language separately when initializing a project.

## Project information from manuscript import

- Rule: When importing an existing or partially written manuscript, extract its stated research goal and paper language and record both in this file before completing adoption. Read the abstract, introduction, and other relevant sections as needed. Record a concise, faithful statement of the goal and identify the language used for the paper. If the draft clearly identifies a different intended paper language from its current prose, record the intended language and note the source. If the goal or intended language is absent, conflicting, or unclear, record what the draft does establish and ask the researcher about the unresolved item; do not leave a blanket unconfirmed status without reporting the extraction.
- Scope: Import of an existing or partially written manuscript, in both clients.
- Confirmed: 2026-11-05; "The import skill should import the research goal and paper language from the half-written manuscript into the project records."

## Complete and unchanged manuscript content during export

- Rule: Preserve the complete content of the selected manuscript version during formatting and export. Do not make unauthorized additions, omissions, rewrites, or changes to wording, values, formulas, objects, notes, citations, or references. Compare the delivered content with the pre-export baseline and distinguish checked representation changes from content changes. Unexplained differences or unchecked content prevent a claim that the export is complete and unchanged.
- Scope: Manuscript formatting and export in this template's submission-assembly workflow, in both clients.
- Confirmed: 2026-11-06; "We also need to ensure that the content is complete and has not been modified."

## Font and table-style restoration during export

- Rule: When exporting a manuscript in the format of a supplied original or template, restore its fonts and table styles as well as its content and structure. Check the restored typography and table appearance against that format source. Report unmet restoration requirements instead of treating a structurally valid file as a faithful result.
- Scope: Source-format restoration in this template's submission-assembly workflow, in both clients.
- Confirmed: 2026-11-05; "We also need to restore fonts and table styles."

## Standard MCP installation during initialization

- Rule: Workspace initialization includes installing the pinned official Sciverse and MinerU cloud MCP packages inside the repository, configuring Codex and Claude Code, and checking MCP protocol and tool discovery. Provide installation, checking, and launch scripts. Missing credentials do not block installation; installation does not authorize research queries or document uploads.
- Scope: This template's initialization workflow, in both clients.
- Confirmed: 2026-10-30; "The repository initialization should include MCP installation." The researcher explicitly requested implementation of the plan for both official MCP servers and both clients.

## PDF text extraction during initialization

- Rule: During project initialization, check for `pdftotext`; install Poppler if it is missing and verify the command. Reuse an existing working installation. This setup does not authorize processing or uploading documents.
- Scope: This template's initialization workflow, in both clients.
- Confirmed: 2026-10-31; "Include `pdftotext` in the scope of project initialization."

## Internal manuscript logic map

- Rule: Maintain an internal Mermaid argument framework in `manuscript/logic-map.md` for each manuscript, whether written from scratch or imported. Include the author's material deductions, inferences, analyses, interpretations, and judgments, with their premises, assumptions, criteria, inferential steps, conditions, and conclusions, as well as evidence, alternatives, objections, and limits. Original reasoning can support a derived claim; distinguish the basis of its premises from the adequacy of its inference. Automatically synchronize the framework as part of each writing or revision task, inspect direct author edits at the next check or session, and track the input version so a stale map is visible. Keep the map and its synchronization record outside manuscript assembly and publication output.
- Scope: This template's manuscript workflow, for every manuscript project.
- Confirmed: 2026-11-04; "We need to ensure the paper's reasoning is coherent. Use a Mermaid flowchart to lay out the paper's logical framework. Keep it out of the paper body as an internal reference, so authors can keep their reasoning coherent and check the logic of the whole paper and its parts when their thinking jumps. Both writing a paper from scratch and importing a paper require this outline."
- Refined: 2026-11-05; "Should the author's deductions, inferences, analyses, judgments, and other reasoning also be included in the framework when the logic is reasonable? The logic map should update automatically as writing proceeds. Please rethink and redesign it."

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
