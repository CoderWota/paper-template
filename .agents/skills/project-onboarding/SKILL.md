---
name: project-onboarding
description: Initialize a paper project by recording confirmed languages, goal, and processing choices; resume incomplete setup.
---

# Project onboarding

Outcome: the few confirmed settings needed to begin, an accurate `state/current.md`, and one clear next action. Unknown research directions, venues, and methods can stay open.

## Rules for this skill

- Follow the shared contract in `AGENTS.md`, especially researcher choices, continuity, and confirmed requirements.
- Ask one question at a time, in the form that `AGENTS.md` sets, and keep the reason to one sentence. Wait for the answer.
- Record an answer only when the researcher states or confirms it. Do not record a guess.
- Never delete, move, or overwrite existing material. Keep any text the researcher wrote in the files you update.
- After the interaction language is confirmed, write records in that language.
- Skip a question when the request or the workspace already answers it. An explicit statement is an answer.
- This skill records requested project setup, not a directory tour. When the researcher only wants to understand the workspace, use the beginner branch of `paper-hands-on` and change no records. Do not start setup merely because the project is uninitialized.
- After a tour, reuse the researcher's actual answers and requested first task. Do not repeat the directory explanation or require a full setup checklist before a bounded task. Confirm only missing information needed now; leave unrelated choices open.

## Step 1: Inspect the workspace before you ask

Start with `state/current.md` and `requirements/project.md`, then inspect `manuscript/manifest.yaml` and directory names in `inbox/`, `references/originals/`, `ideas/`, `research/`, and `reviews/` to distinguish a fresh workspace from existing research. Template READMEs and empty indexes are not research material. Read relevant requirement entries to reuse confirmed answers; open an index or record only when needed to resolve the current paper or task. Do not read the full library or every requirements file by default.

For a confirmed request to initialize this paper, run `python scripts/versions.py detach-template` before marking setup complete. Tell the researcher in one sentence that project setup will disconnect a link to the original template repository if one exists; their local versions and any personal remote remain. Run `python scripts/versions.py detach-template --apply` for an unambiguous ordinary copy, then check again. If the client restricts writing `.git/config`, request its narrow local filesystem approval when available and retry; if approval is unavailable or denied, report setup incomplete without asking the researcher to run a command. If the tool reports a mixed or uncertain address or shared Git worktrees, explain the specific issue and leave setup incomplete until the researcher chooses how to handle it. A folder without Git configuration or without remotes needs no action. Do not do this for a directory tour, a bounded first task, or template maintenance.

Inspect other version-history details with `python scripts/versions.py inspect` only when setup includes a history question or the current material leaves a history or recovery ambiguity. If it reveals relevant inherited history, an external copy, or a missing research version, explain that issue and offer the matching version task without changing history. Do not make a history discussion a prerequisite for a beginner's first task.

Research material means sources in the library, manuscript sections in the manifest, retained ideas, research records, or review rounds. Files in `inbox/` are intake material, not another paper.

| Case | Signs | Action |
| --- | --- | --- |
| New workspace | `requirements/project.md` says the project is not initialized, and there is no research material | Go to step 2. Use any `inbox/` files as context. |
| Interrupted onboarding | Some answers are recorded in `requirements/project.md` or `state/current.md` | Continue with the first open item. Do not ask confirmed items again. |
| Workspace already holds work | `requirements/project.md` says the project is initialized, or confirmed project requirements or research material exist | Go to "A workspace that already holds work". A project whose onboarding is finished counts, even when it has no research material yet. |

For a direct setup request, start with two short sentences explaining what will be recorded and that unknown choices can wait. After a tour, simply explain the next necessary choice; do not restart the introduction or ask for an answer already given.

## Step 2: Confirm the interaction language

Recommend the language the researcher writes in. Say that you will use it in the conversation and in their project records. Example: "I will talk with you and keep your project records in Chinese. Is that correct?"

## Step 3: Understand the research goal

Ask what the researcher wants to achieve: a topic, an interest, a question, or an existing draft. "Not sure yet" is a valid answer. If you found material in `inbox/` or a draft, say what you found and use it to suggest an answer.

Record the goal with the researcher's exact words in quotation marks, and never call a paraphrase their words. Do not turn an unclear interest into a research question by yourself; developing ideas is a separate task (`research-ideation`), which you can offer as the next action.

## Step 4: Ask for the manuscript language

Ask when the first task produces manuscript text or when the researcher wants to settle the manuscript language now. Recommend a language from the known field, venue, or draft; do not record the recommendation without confirmation. "Decide later" is valid. For an exploratory first task that needs no manuscript language yet, keep it open rather than blocking the task.

## Step 5: Ask how documents can be processed

Ask this when the researcher has documents that need conversion now (PDFs, office files, or images) or wants to settle it now. Markdown and plain-text files are read directly and need no processing choice, and data files are not documents to convert. Otherwise, list the processing choice as open ("decide at the first import") and continue.

1. Use `environment-management` to inspect the computer first: operating system, processor, memory, storage, and installed tools. Do not install anything in this step.
2. Explain the options in plain words:
   - Local: the documents stay on this computer. Processing can be slow, and some documents need a larger installation.
   - Cloud: a named MinerU service processes the documents. The documents are sent to that service.
   - Decide later.
3. Recommend one option, with its reason. Base it on the computer and on how sensitive the documents are.
4. For a cloud choice, also confirm which documents the choice covers.

If the choice needs a credential or an installation, use `environment-management`. If that setup cannot be done yet, record the choice and mark the setup as deferred.

## Step 6: Record each confirmed answer

Write each answer as soon as it is confirmed, so an interruption loses nothing. Write in the interaction language.

- `requirements/project.md`: the setup status and date (incomplete until the agreed setup is finished), the research goal in the researcher's words, confirmed languages, and any confirmed audience, article type, or target venue. Keep unconfirmed or unneeded items open instead of filling them from a recommendation.
- `requirements/privacy.md`: the confirmed processing choice (local or a named cloud service), the documents it covers, and any data-use requirement that the researcher confirmed. A declined or postponed offer or choice is not a requirement; do not write it here. If the researcher decides later, list the choice as open in `requirements/project.md` and `state/current.md`. A cloud service is recorded only after its scope is confirmed (see `privacy-configuration`).

If the researcher states a writing rule, record it in `requirements/writing.md` through `constraint-maintenance`.

## Step 7: Offer the AI application privacy check

Offer the optional check when the researcher asks about privacy or the selected task makes the account's data-use settings relevant. Explain its scope and recommend it; do not make an account questionnaire or check a prerequisite for a directory tour or unrelated first task. If they agree, use `privacy-configuration`. Do not change a setting without consent for that change. If they explicitly decline or postpone, record that only in `state/current.md`, in their words. An offer not yet made is not a declined choice or requirement.

## Step 8: Finish

1. Once the agreed setup and the template-remote check are complete, mark the project initialized with the date and keep unneeded choices explicitly open. If setup stops before that point, retain its incomplete status and the confirmed answers. Rewrite `state/current.md` in the interaction language: what is set up, what is open, and the next action. No record is written merely to log a tour.
2. Report the recorded settings with links, open items relevant to the task, and one feasible next action. Continue a first task already requested once its prerequisites are settled; do not stop solely to ask for the same authorization again. For documents, give the actual clickable location of optional `inbox/` or use their current location; the researcher need not sort or move files. `inbox/imports/` holds import records, not incoming files.

## A workspace that already holds work

Do not delete, move, or overwrite anything in this case. This folder can be the only copy of the earlier paper.

1. Unless the request already makes it clear, ask: "This workspace already contains work on <topic>. Do you want to continue that paper, or start a new paper?"
2. Continue: keep everything. Ask only the onboarding questions whose answers are not recorded yet, then summarize the recorded settings and ask what the researcher wants to do next. Changes to recorded requirements go through `constraint-maintenance`.
3. New paper: explain that each paper uses its own fresh copy of the template, and change no file here, `state/current.md` included. The state of the new paper belongs to its own copy.
   - If you can identify where the template came from, for example a Git URL, and the researcher confirms it, offer to create the fresh copy in a new folder that the researcher names. Copy no research material into it.
   - Otherwise, tell the researcher how to get a fresh copy the same way they got this one.
   - Tell the researcher to open the new folder with their AI application and ask to initialize it there.
   - Say that the reference library can be imported into the new workspace later.

## Completion check

- The researcher stated or confirmed every recorded item.
- No inferred preference appears in any file.
- `state/current.md` names the next action, in the interaction language.
- A declined or postponed offer appears only in `state/current.md`, not in `requirements/`.
- No existing material was deleted, moved, or overwritten.
- No original-template remote remains on an initialized project; ambiguous or shared Git configuration remains for a researcher decision.
