# Directory Details for Follow-up Questions

Read only when the researcher requests more detail about a folder or workflow. Use the relevant rows or section to answer that question; do not repeat the complete tour. The compact first reply is defined in [the directory guide](directory-guide.md).

## All top-level project folders

| Folder | What it holds and when it is used | What the researcher does | What the assistant does |
| --- | --- | --- | --- |
| [inbox/](../../../inbox/README.md) | Optional drop-off for unsorted drafts, papers, letters, templates, or notes. | Put material here if convenient, or give its existing location. | Identify its role and organize an authorized import without changing the supplied file. |
| [requirements/](../../../requirements/README.md) | Confirmed goals, languages, writing rules, privacy choices, and output requirements. | State or change a requirement in conversation and confirm its scope. | Record the confirmed choice and apply the relevant rules; never turn a guess into a rule. |
| [manuscript/](../../../manuscript/README.md) | Working outline, manuscript text, and figures during drafting and revision. | Read and edit the working text, or ask for a specific change. | Draft or edit within scope, keep the assembly list, and check affected text. |
| [references/](../../../references/README.md) | Source documents, readable extractions, reading notes, bibliography, and searches. | Supply sources or ask for literature and evidence checks. | Preserve originals, organize sources, record metadata, and check claim support. |
| [ideas/](../../../ideas/README.md) | Exploratory directions and ideas the researcher chooses to keep. | Discuss possibilities and choose which ideas to retain. | Save selected ideas and their open questions without presenting them as results. |
| [research/](../../../research/README.md) | Research plans, decisions, advice, results, and venue assessments. | Make scholarly choices, provide material, and review findings. | Record provenance, distinctions between planned and observed work, and unresolved issues. |
| [reviews/](../../../reviews/README.md) | Editor and reviewer correspondence and responses by venue and round. | Supply review letters and decide the response strategy. | Preserve numbering and originals, draft responses, and link them to actual changes. |
| [revisions/](../../../revisions/README.md) | Recoverable baselines and plans for substantial changes to an existing manuscript. | Specify the revision goal and decide consequential changes. | Keep a recoverable starting point, stage the revision, and reconcile later author edits. |
| [outputs/](../../../outputs/README.md) | Generated previews, checks, and preserved release packages after formatting. | Inspect the output and ask for corrections or a final package. | Build from the working manuscript, inspect the result, and preserve releases. |
| [state/](../../../state/README.md) | A short note of actual work in progress and its next step. | Ask to continue later without reconstructing the previous session. | Maintain the handoff and inspect current work before resuming; do not log a tour. |
| [docs/](../../../docs/README.md) | Optional guides to supported operations, limits, and conventions. | Ask for an explanation when needed; reading them is not an entry requirement. | Consult only the operational guide needed for the task. |
| [scripts/](../../../scripts/README.md) | Tools for importing, checking, formatting, and version history. | Ask for the outcome in ordinary language. | Run and maintain the tools; do not hand the researcher commands to memorize. |
| [.agents/](../../../.agents/README.md) | Canonical task instructions used by Codex and shared with the other adapter. | Describe a task; no manual skill selection is required. | Select relevant instructions and maintain their single editable source. |
| [.claude/](../../../.claude/README.md) | Generated task copies and the Claude Code adapter. | Use the same conversational requests in Claude Code. | Keep generated copies synchronized; the researcher does not maintain two versions. |

## Common child folders

Explain only the child folders relevant to the follow-up. Do not ask the researcher to memorize the paths or manually distribute files into them.

| Locations | What to understand and how to use them |
| --- | --- |
| [references/originals/](../../../references/originals/README.md) and [references/extracted/](../../../references/extracted/README.md) | Originals are unchanged source files; extractions are derived readable text and images that can contain errors. Ask the assistant to check a questionable passage against its original. |
| [references/notes/](../../../references/notes/README.md) and [references/searches/](../../../references/searches/README.md) | Notes hold interpretation and evidence links; search records hold how sources were found and coverage gaps. Ask to find support for a claim rather than treating a saved summary as proof. |
| [research/decisions/](../../../research/decisions/README.md) and [research/feedback/](../../../research/feedback/README.md) | Decisions record what the researcher chose; feedback preserves what someone advised. Receiving a collaborator's suggestion does not adopt it automatically. |
| [research/results/](../../../research/results/README.md) and [research/venues/](../../../research/venues/README.md) | Results retain inputs, methods, outputs, and checks; venue records retain official journal information and its date. Ask for an analysis or venue comparison and review its limits. |
| [manuscript/assets/](../../../manuscript/assets/README.md) | Figures and other assets used in the working text. Supply existing figures wherever they are; the assistant places authorized working copies and maintains references. |
| [requirements/profiles/](../../../requirements/profiles/README.md) | Journal or thesis instructions, templates, and the settings used to format output. Supply the target guidelines; the assistant builds the matching profile. |
| [outputs/preview/](../../../outputs/preview/README.md) and [outputs/releases/](../../../outputs/releases/README.md) | Previews can be regenerated; release packages are preserved versions. Ask to change the working manuscript and rebuild, rather than treating the preview as the master draft. |
| [inbox/imports/](../../../inbox/imports/README.md) | Import records, not the place users need to sort incoming files. The assistant uses these records to resume interrupted imports and report gaps. |

If asked about the main files, briefly explain: `README.md` is the human introduction; `AGENTS.md` supplies shared collaboration rules; `CLAUDE.md` connects Claude Code to those rules; `CONTEXT.md` explains terms. None must be edited to start a conversation.

## Optional and hidden support locations

Explain the purpose without opening private files, creating these locations, or teaching their internals. They may not exist yet and are often hidden in a file manager.

- `code/` appears only when the study needs computation. It holds research analysis and its runs, separate from the workspace tools in `scripts/`. The researcher supplies the research question and data; the assistant sets up and records the authorized analysis. An existing analysis repository can live there as its own Git repository: the researcher develops it in a separate session opened in its folder, and the paper session only reads it and records runs.
- `.git/` holds local saved versions. Ask the assistant to save, compare, or recover work. Local history is not an external backup.
- `.venv/` holds an environment for tools that need extra packages; `.tools/` keeps separate tool installations. The assistant prepares these only when needed and authorized.
- `.cache/` holds rebuildable caches; `.tmp/` holds temporary work; `.local/` holds machine-specific reports and logs. These are assistant-maintained support locations, not places to keep the only copy of research material.
- `.env.local` is a local credential **file**, not a research folder. Keys go through the private entry page when a chosen service needs one. Do not read, link to its contents, request a key, or start credential setup during the tour.

## Connect the map to three real uses

Expand the requested example only; these flows describe what happens after an actual task is requested, not work performed during a tour.

1. **An existing draft:** the researcher gives its current location or optionally puts it in `inbox/` and asks to bring it into the workspace. The assistant preserves the received draft in the import record, checks conversion, and adopts working sections and assets into `manuscript/`. An existing working manuscript is preserved and competing drafts are compared before replacement.
2. **Reference papers:** the researcher supplies papers and requests import. Unchanged files go to `references/originals/`; derived text and images go to `references/extracted/`. When reading and evidence work is requested, interpretations go to `references/notes/`, and source metadata goes to the bibliography. Import does not mean the papers have been critically read.
3. **A submission format:** the researcher supplies journal instructions and requests formatting. The assistant records the output requirements in `requirements/profiles/`, builds from `manuscript/` into `outputs/preview/`, and checks the result. Only a requested final package is frozen in `outputs/releases/`. Formatting and freezing do not submit the paper.

Make the distinction explicit: originals are retained evidence/input; manuscript files are the working text; previews are derived views; releases preserve a particular output. Changes made in an exported Word file are not automatically synchronized back; the assistant can reconcile them when asked.

