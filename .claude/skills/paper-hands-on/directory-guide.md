# Compact Beginner Directory Guide

Use for first-time workspace use, uncertainty about how to start, or questions about where files go. This branch explains use; it does not authorize setup, file processing, accounts, or teaching-progress records. A greeting alone does not initialize a project.

## Read and locate only what is needed

Read the short project state and project requirements. Use the confirmed interaction language, or the researcher's current language until one is confirmed. Do not interrupt the tour for a language-setting question. Do not inspect document contents, version history, the environment, accounts, or secrets for a tour.

Use this package's actual discovered path and resolve links relative to it; do not guess a user-level installation. Resolve output links against the current workspace. When checking folders, list existing directory entries or check existence first; optional paths can be absent without an error. Do not probe a list of guessed optional names with a command that fails when one is missing.

## First reply: one map, three examples, then stop

Keep the first reply compact while covering every top-level folder. Use this order:

1. Two short opening sentences: the researcher supplies ideas, material, and judgments; the assistant organizes files and operates tools. No commands or skill names need to be learned. Explain a folder as a place to keep related files only if needed.
2. One table with exactly the 14 project folders below, translated into the interaction language. Each row gives purpose/when used and how to use it. Include common child names inside their parent's row instead of printing a second directory list. Use one clickable absolute local folder or README link per top-level row; child names can remain short inline paths in that row. Do not repeat every path as another full link.
3. One short paragraph for optional and hidden support locations, then three one-sentence material flows. The flows show where work goes after it is requested; they are not imports performed during the tour.
4. For a tour-only request, end. Otherwise ask at most one substantive question about the first task, only if the user has not already supplied it. Having material is not itself a request to process it; no clear direction or material is a valid starting point.

Do not add a second map, a recap of the same paths, an FAQ, a technical-file lecture, a setup questionnaire, or another invitation to initialize. Keep each table row and each example short; preserve coverage rather than meeting a rigid word count. Expand only a folder or step the researcher asks about using [directory details](directory-details.md); do not read or reproduce that reference for a normal first tour. An explicitly requested detailed tour can be longer.

## The map to convey

| Folder | Purpose and common children | How to use it |
| --- | --- | --- |
| [inbox/](../../../inbox/README.md) | Optional unsorted incoming material; `imports/` contains import records. | Put files here if convenient, or give their existing location; the assistant classifies an authorized import. |
| [requirements/](../../../requirements/README.md) | Confirmed goals and rules; `profiles/` holds output requirements. | State your requirements in chat; the assistant records only confirmed choices. |
| [manuscript/](../../../manuscript/README.md) | Working outline and text; `assets/` holds figures. | Read or edit the working text, or ask the assistant to change it. |
| [references/](../../../references/README.md) | `originals/` source files, `extracted/` readable copies, `notes/` interpretation, `searches/` searches, and the bibliography. | Supply papers or ask for evidence checks; the assistant keeps originals separate from derived text and notes. |
| [ideas/](../../../ideas/README.md) | Exploratory directions chosen for retention. | Discuss possibilities and choose what to keep; the assistant does not present ideas as results. |
| [research/](../../../research/README.md) | Plans, `decisions/` choices, `feedback/` advice, `results/` findings, and `venues/` journal information. | You decide and review; the assistant records what was planned, confirmed, or actually found. |
| [reviews/](../../../reviews/README.md) | Editor/reviewer letters and responses by venue and round. | Supply letters and decide the strategy; the assistant tracks responses and changes. |
| [revisions/](../../../revisions/README.md) | Recoverable baselines and plans for substantial manuscript changes. | Set the revision goal; the assistant preserves the starting draft and reconciles changes. |
| [outputs/](../../../outputs/README.md) | `preview/` regenerable outputs; `releases/` preserved packages. | Inspect output; ask to correct the working text and rebuild, or preserve a final package. |
| [state/](../../../state/README.md) | Short handoff of actual work in progress. | Ask to continue later; the assistant keeps the handoff, not a log of this tour. |
| [docs/](../../../docs/README.md) | Optional operating guides. | Ask when needed; the assistant reads the relevant guide. |
| [scripts/](../../../scripts/README.md) | Workspace tools. | Describe the outcome; the assistant runs and maintains tools. |
| [.agents/](../../../.agents/README.md) | Canonical task instructions. | Describe a task; the assistant selects the instructions. |
| [.claude/](../../../.claude/README.md) | Generated Claude Code task adapters. | Use ordinary requests; the assistant keeps the adapters synchronized. |

## Optional support: one short paragraph

Mention `code/` for research analysis, including an imported analysis repository, when needed; `.git/` for local saved versions (not an external backup); `.venv/` and `.tools/` for tool environments; `.cache/` for rebuildable caches; `.tmp/` for temporary work; `.local/` for local logs; and `.env.local` as a private credential file. The assistant maintains these, some may not exist yet, and no setup or secret entry is needed for a tour. Do not open, create, or link to credential contents.

## Three flows: one sentence each

- **Existing draft:** give its location or optionally use `inbox/`; after an import request, the assistant retains the received original in `inbox/imports/` and adopts working text and figures into `manuscript/`, comparing any existing working draft first.
- **Reference papers:** on request, preserve files in `references/originals/` and derive readable copies in `references/extracted/`; requested reading produces `references/notes/` and source metadata in the bibliography, without equating import with critical reading.
- **Submission format:** supplied guidelines become `requirements/profiles/`; the assistant builds from `manuscript/` into `outputs/preview/` and freezes a checked package in `outputs/releases/` only when requested, without submitting it.

The map and flows must distinguish original inputs, working text, generated previews, and preserved releases. Do not repeat that distinction in a separate recap. If asked about editing an exported Word file, explain that edits do not synchronize back automatically and can be reconciled by the assistant.

## Follow-up and handoff

`inbox/` remains optional. For a file-location question, explain that the researcher can supply the current location without sorting internal folders. If that location cannot be accessed, state the observed limitation and describe an actually supported way to supply it. Do not assume attachments, file-manager control, outside-folder access, or cloud upload; do not claim a folder was opened without observing it.

Answer follow-up questions without repeating the full tour. Once an actual task is requested, use its specialist skill and reuse answers already given. Use onboarding only for requested project setup, confirm missing settings needed now, and leave unrelated choices open. A person with no material or clear direction can request help exploring interests. Existing users and direct tasks bypass the tour.

A tour is complete when every top-level folder, common children, optional support, and three practical flows are explained. Do not change manuscript, requirements, state, imports, accounts, or teaching records merely to mark completion.
