---
name: project-onboarding
description: Set up this research writing workspace for a researcher who may have no programming background. Confirms the interaction language, research goal, manuscript language, and document-processing choice one question at a time, records only confirmed answers, and ends with one clear next action. Use when the researcher asks in any language to initialize, start, or set up the paper project, or when requirements/project.md says the project is not initialized.
---

# Project onboarding

Outcome: the few confirmed settings needed to begin, an accurate `state/current.md`, and one clear next action. Unknown research directions, venues, and methods can stay open.

## Rules for this skill

- Follow `AGENTS.md`, especially "Decisions and questions" and "Confirmed requirements only".
- Ask one question at a time, in the form that `AGENTS.md` sets, and keep the reason to one sentence. Wait for the answer.
- Record an answer only when the researcher states or confirms it. Do not record a guess.
- Never delete, move, or overwrite existing material. Keep any text the researcher wrote in the files you update.
- After the interaction language is confirmed, write records in that language.
- Skip a question when the request or the workspace already answers it. An explicit statement is an answer.

## Step 1: Inspect the workspace before you ask

Read these without asking the researcher:

- `state/current.md` and the files in `requirements/`
- `manuscript/manifest.yaml`, `references/index.md`, and `ideas/index.md`
- the lists of files in `inbox/`, `references/originals/`, `research/`, and `reviews/`

Research material means sources in the library, manuscript sections in the manifest, retained ideas, research records, or review rounds. Files in `inbox/` are intake material, not another paper.

| Case | Signs | Action |
| --- | --- | --- |
| New workspace | `requirements/project.md` says the project is not initialized, and there is no research material | Go to step 2. Use any `inbox/` files as context. |
| Interrupted onboarding | Some answers are recorded in `requirements/project.md` or `state/current.md` | Continue with the first open item. Do not ask confirmed items again. |
| Workspace already holds work | `requirements/project.md` says the project is initialized, or confirmed project requirements or research material exist | Go to "A workspace that already holds work". A project whose onboarding is finished counts, even when it has no research material yet. |

Start the conversation with two sentences: what onboarding does, and that it asks a few questions whose answers can wait when unknown.

## Step 2: Confirm the interaction language

Recommend the language the researcher writes in. Say that you will use it in the conversation and in their project records. Example: "I will talk with you and keep your project records in Chinese. Is that correct?"

## Step 3: Understand the research goal

Ask what the researcher wants to achieve: a topic, an interest, a question, or an existing draft. "Not sure yet" is a valid answer. If you found material in `inbox/` or a draft, say what you found and use it to suggest an answer.

Record the goal with the researcher's exact words in quotation marks, and never call a paraphrase their words. Do not turn an unclear interest into a research question by yourself; developing ideas is a separate task that is not available yet.

## Step 4: Ask for the manuscript language

Recommend a language from what you know, such as the field, a target journal, or an existing draft. "Decide later" is a valid answer.

## Step 5: Ask how documents can be processed

Ask this when the researcher has documents to import now or wants to settle it now. Otherwise, list the processing choice as open ("decide at the first import") and continue.

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

- `requirements/project.md`: the status (initialized, with the date), the research goal in the researcher's words, the interaction language, the manuscript language, and any confirmed audience, article type, or target venue. List the items that are still open.
- `requirements/privacy.md`: the confirmed processing choice (local or a named cloud service), the documents it covers, and any data-use requirement that the researcher confirmed. A declined or postponed offer or choice is not a requirement; do not write it here. If the researcher decides later, list the choice as open in `requirements/project.md` and `state/current.md`. A cloud service is recorded only after its scope is confirmed (see `privacy-configuration`).

If the researcher states a writing rule, record it in `requirements/writing.md` through `constraint-maintenance`.

## Step 7: Offer the AI application privacy check

Ask whether the researcher wants you to check if their AI application can use project content for model training. Recommend the check. If they agree, use `privacy-configuration`. Do not change an account setting without their explicit consent. If they decline or postpone, note it as deferred, in their words, only in `state/current.md`. Do not write it to `requirements/privacy.md`, and do not add a rule that they did not state.

## Step 8: Finish

1. Set the status in `requirements/project.md` to initialized, with the date. Rewrite `state/current.md` as a whole in the interaction language, including its heading: what is set up, what is deferred, and the next action. The researcher reads this record.
2. Report in the interaction language: the recorded settings with links to the files, the deferred items, and exactly one recommended next action that you can carry out now with the available skills and your own tools. If that action involves documents, name `inbox/` as the place for them; `inbox/imports/` holds the agent's import records, not documents.

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
