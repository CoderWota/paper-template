# Research Writing Workspace

Develop one paper with an AI assistant in Codex or Claude Code. You direct the research question, scholarly judgments, final wording, and submission choices. The assistant helps examine evidence, write and revise the manuscript, and handle files and tools. You do not need programming knowledge.

## Start with your situation

Open this folder in your AI application and start a conversation. If you do not know what to do, simply say:

> I do not know how to use this project. Show me what each folder is for and how to begin.

The assistant explains all top-level folders and the common subfolders, with links and examples. You do not need to read a manual, move files, or know a setup command first. A tour does not initialize the paper or process your material.

When you want to set up a new paper, you can ask:

> Help me set up this research writing project. I do not have a programming background.

You can bring an existing draft, a research question, collected papers, or reviewer comments. Unknown choices can wait. Each additional paper uses a separate fresh copy of this workspace.

You can also request one task directly:

| Your need | What to ask |
| --- | --- |
| Bring in a draft | “Import my existing manuscript and show any conversion losses before we continue.” |
| Organize reading | “Import these papers, keep their originals, and flag missing pages or uncertain formulas.” |
| Find literature | “Find sources on this question and show the search scope and full-text gaps.” |
| Examine an idea | “Challenge this explanation and compare the closest work.” |
| Develop an argument | “Help me structure the paper around this question and the results we actually have.” |
| Edit prose | “Shorten this paragraph without losing its conditions, citations, or meaning.” |
| Check support | “Check which claims in this section are supported and which need more evidence.” |
| Prepare output | “Format the manuscript using these journal instructions and check the Word output.” |
| Handle reviews | “Organize this review round and help me respond point by point.” |
| Preserve work | “Save this version locally so I can compare or recover it later.” |

The assistant selects the needed instructions and tools. You do not need to know skill names or run commands. For setup details or uncertain support, see [capabilities and limits](docs/capabilities.md).

## Bring your material

You can put files in [`inbox/`](inbox/README.md), or point the assistant to their existing location; this folder is optional. It identifies reference sources, manuscripts, feedback, reviewer letters, and format templates before organizing them. Original files stay unchanged.

Before parsing documents, choose local processing or the named MinerU service and the material that choice covers. Cloud processing sends documents to that service; the assistant explains relevant limits before asking. Credentials are entered on a private local page, never in chat. Checking the AI application's data-use settings is a separate, optional task.

## Where your work lives

| Folder | Contents |
| --- | --- |
| [`requirements/`](requirements/README.md) | Your confirmed project, language, writing, privacy, and output requirements. |
| [`manuscript/`](manuscript/README.md) | The outline, section files, figures, and assembly manifest. |
| [`references/`](references/README.md) | Unchanged sources, readable extractions, bibliography, search records, and evidence notes. |
| [`ideas/`](ideas/README.md) | Ideas you choose to keep, including exploratory ones. |
| [`research/`](research/README.md) | Plans, decisions, collaborator feedback, venue assessments, and results with their provenance. |
| [`reviews/`](reviews/README.md) | Editorial correspondence and responses by venue and submission round. |
| [`revisions/`](revisions/README.md) | Recoverable baselines and change records for major revisions. |
| [`outputs/`](outputs/README.md) | Rebuildable previews and preserved release packages. |
| [`state/`](state/README.md) | A short handoff for the next session, maintained by the assistant. |

Ask “Explain the project folders” for a guided tour of these and the supporting folders.

The assistant maintains the supporting [`scripts/`](scripts/README.md) and agent configuration. Research code is created separately in `code/` only when a study needs computation.

## Continue, review, and decide

To resume, ask “Continue from the project records.” The assistant checks the current material and open work without making you reconstruct past sessions. You can also ask to compare versions, recover a passage, or inspect what remains before submission.

Clear instructions authorize routine work within their scope. Changes to the research question, main claim, method, structure, venue, lasting rules, or external sharing need your decision. Suggestions and inferred preferences do not become requirements. A change to a rule does not silently rewrite your manuscript.

Converted text can contain errors. Search hits are leads rather than verified evidence, simulated review scores are not acceptance probabilities, and an exported file still needs inspection. The assistant reports what it actually checked and what remains unresolved. Local version history is separate from an external backup; nothing is pushed without your instruction for a destination.

Operational details are available in [the guides](docs/README.md), including [document conventions](docs/markdown-and-export-conventions.md) and [agent loading](docs/context-loading.md). They are reference material, not prerequisites for ordinary writing.
