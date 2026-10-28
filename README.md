# Agent-Assisted Paper Template

An organized workspace for developing research ideas, reading literature, writing a manuscript, and preparing submission files with an AI agent.

**Project status: early implementation.** The workspace folders, their descriptions, and the agent operating contract (`AGENTS.md`) exist. The setup skills (project onboarding, environment checks, privacy checks, and confirmed rules) and document import with MinerU (references and review documents) are implemented and passed a documented review. They are not yet tested on Windows or in Codex, and document import is not yet tested with the live mineru.net service. The other workflows below describe the intended experience. Follow the [design plan](docs/design-plan.md) to review the current proposal, and see the [implementation status](docs/implementation-status.md) for what actually works.

For framework development, the [MVP implementation guideline](docs/mvp-implementation-guideline.md) organizes the work into nine planned increments with concrete deliverables and acceptance criteria.

The [workflow review and public knowledge transfer](docs/research-workflow-review.md) examines what is still needed to carry the researcher's ideas through actual results to a complete submission package. A bounded complete-path case is confirmed as a framework test only. It does not limit supported research or establish real publication readiness; detailed implementation proposals remain open.

## Why this workspace exists

Research work spans ideas, source documents, evidence notes, writing requirements, drafts, and reviewer comments. This template gives each of them a clear home so researchers do not have to design their own project structure or repeat confirmed requirements in every conversation.

The agent selects appropriate skills and handles routine technical work. It can help explore ideas, examine assumptions, retrieve and compare sources, draft with evidence, and assemble outputs. The researcher directs scholarly decisions and chooses what to retain.

Your main contribution is the research idea, domain knowledge, scholarly judgment, and final author review. Within the scope you confirm, the agent should carry the routine production work and connect the stages itself. You should not need to shuttle text between tools, maintain progress records, or issue a separate instruction for every file and skill. These are design requirements; the workflow is not implemented yet.

The intended researcher has ordinary computer skills and no coding or software-engineering background. Git operations, BibTeX records, YAML/JSON settings, and scripts are maintained through the agent. Describe the change you want and review the outcome; you do not need to edit those technical files. You can still write manuscript prose and ideas directly.

The framework does not prescribe a discipline, article structure, or writing language. It targets ordinary Windows laptops, with macOS and Linux support to be verified progressively. Heavy local inference is optional.

Markdown formulas use GitHub-renderable LaTeX, and agent-created explanation diagrams use Mermaid. Word exports must contain correct, native editable equations. The agent maintains the syntax and checks both previews and final outputs; scientific result plots retain suitable plotting formats. These are confirmed design requirements awaiting implementation.

## Getting started: intended workflow

1. Obtain a copy of this repository for your paper and open its folder with Codex or Claude Code. Each paper uses its own copy.
2. Ask the agent: “Help me initialize this research writing project. I do not have a programming background.”
3. The agent guides the few choices needed to begin, including writing language, research goals, privacy settings, and local or cloud document parsing. Unknown details can wait.
4. If the selected service requires an API key, the agent explains where to obtain it and guides private entry on your computer. You do not paste it into the conversation or write setup code.
5. Start with a document, an idea, or an existing draft. You do not need to memorize skill names or command-line options.

## Everyday requests

| What you want to do | What to ask the agent |
| --- | --- |
| Work through a paper from scratch | “Guide me from collecting literature and developing an idea to examining its impact, choosing a journal, and writing a manuscript in its required format.” |
| Learn practical version control | “I do not know Git. Help me save this version, compare changes, and practice retrieving earlier content.” |
| Import literature | “Import all PDFs from this folder into the reference library, including their images.” |
| Adopt an existing paper | “Organize this Word manuscript into the workspace conventions, preserving its text, figures, and references, and show anything that could not be migrated.” |
| Download and import references | “Download the available full text from this reference list, convert it to Markdown, and add it to the library. Tell me which items still need access.” |
| Extract review documents | “Convert these Word reviewer comments to Markdown and archive them with this submission round, including comments and images where supported.” |
| Work through research feedback | “Organize these comments from my co-researchers and collaborators, discuss their implications with me, and apply the changes I choose.” |
| Continue an interrupted import | “Continue the import and retry only the failed documents.” |
| Explore a direction | “Based on these readings and my interests, help me develop several distinct research ideas.” |
| Deepen an idea | “Examine this idea with me, one question at a time. Check the closest prior work and help me identify a feasible contribution.” |
| Investigate a question | “Compare what these sources actually support and explain where they disagree.” |
| Work on the manuscript | “Revise this section using my confirmed writing requirements and identify claims that need evidence.” |
| Make a major revision | “Restructure this paper around the revised question. Preserve the current version, show what must change, and check the evidence and whole manuscript after rewriting.” |
| Prepare a formatted output | “Format my manuscript using these journal instructions and this Word, LaTeX, or PDF reference template, then check the result against the requirements.” |
| Handle peer review | “Organize this round of reviewer comments and help me respond point by point.” |

The agent should report what completed, link the results, and explain anything needing attention. For batch conversion, it manages archiving, Markdown, images, indexing, duplicates, and retries in the background. It uses MinerU in the processing mode you selected.

Put mixed material in the intake area, `inbox/`, or simply point the agent to its existing location. You do not need to sort it first. Downloading, conversion, manuscript adoption, and comment extraction can be requested separately or together. Unavailable full text and conversion gaps remain visible; received advice becomes a lasting requirement only when you adopt it.

Major revision is also a proposed independent task, before submission or after feedback. The agent would preserve the starting version, explain affected work, coordinate revision, and recheck changed claims and related passages. You do not need to operate Git, and a small edit does not require a revision project. A changed manuscript needs current checks; an earlier successful export is not proof that the revision is ready.

## Two guided hands-on paths

The planned **paper hands-on** coordinates literature collection, idea exploration, impact assessment, journal fit and readiness, necessary research, drafting, and format checks. Start from your current situation and resume across sessions. The planned **Git hands-on** uses practical examples to help you preserve versions, compare changes, and retrieve earlier material while the agent handles the commands.

Each task is also independently available: ask only to assess an idea's impact, compare journals, check submission readiness, or compare two versions. The agent chooses the matching skill and reuses your current material; you do not need to complete a course or memorize skill names.

See the [hands-on guide](docs/hands-on.md). These are design previews, not implemented skills. Journal prospects are discussed through evidence-based strengths and risks, with no promise of acceptance.

## Where your work belongs

| Area | Folder | Purpose |
| --- | --- | --- |
| Intake | [`inbox/`](inbox/README.md) | An optional landing area for existing manuscripts, reference lists, comments, and other files awaiting organization. |
| References | [`references/`](references/README.md) | Original documents, readable extractions, and evidence notes. |
| Requirements | [`requirements/`](requirements/README.md) | Your confirmed project, writing, privacy, and submission requirements. |
| Manuscript | [`manuscript/`](manuscript/README.md) | The working text and its figures and other assets. |
| Ideas | [`ideas/`](ideas/README.md) | Research directions and thoughts you choose to keep, including unfinished ones. |
| Research records | [`research/`](research/README.md) | Important confirmed choices and their rationale, plus attributed feedback from co-researchers, collaborators, coauthors, supervisors, or other contributors and its follow-up. |
| Reviews | [`reviews/`](reviews/README.md) | Editorial and reviewer correspondence, responses, and changes by submission round. |
| Major revisions, proposed | [`revisions/`](revisions/README.md) | Recoverable starting versions or references, revision plans, changes, and current checks for substantial rewrites. |
| Outputs | [`outputs/`](outputs/README.md) | Previews and preserved submission packages. |
| Project state | [`state/`](state/README.md) | A short note of work in progress and the next step, kept by the agent between sessions. |
| Scripts and optional research code | [`scripts/`](scripts/README.md), `code/` | Reusable automation and research implementation, managed with the agent. `code/` is created only when the research needs it. |

The framework's design documents are in [`docs/`](docs/README.md), and agent instructions are in `AGENTS.md`, `.agents/`, and `.claude/`. You do not need to open them for ordinary work.

Every designed project directory has its own short English `README.md`, and folders created later, such as each source, review round, revision, or skill, receive one when they are created. It explains the directory's purpose, contents, related records, and what the agent maintains. The agent writes and updates these descriptions; human-facing translations can be added when useful. Runtime caches and installed dependencies are outside this project-directory requirement.

## Your choices stay explicit

Only verified, researcher-confirmed writing rules become lasting instructions. An idea may remain exploratory; a converted document may still need checking. Neither becomes an established rule or verified evidence merely because it was saved.

Before a major decision, the agent must show a concrete recommendation and obtain your explicit confirmation. This includes consequential changes to the research, manuscript structure, target venue, privacy, or external sharing. Clear instructions you already gave apply within their scope. Questions, including idea-deepening interviews, address one substantive choice at a time. English questions follow ASD-STE100; other languages use corresponding clarity principles without changing your chosen language or imposing a manuscript style.

Choose whether your documents may be parsed locally or by a cloud service. Credentials stay in local, untracked storage. A privacy setup skill will help with supported training opt-outs and explain what was actually verified. Your choices about the AI application and the parsing service are checked separately.

If something is missing or fails, ask the agent to help configure it or continue the task. The intended workflow does not require you to diagnose software tracebacks.
