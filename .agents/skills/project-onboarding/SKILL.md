---
name: project-onboarding
description: Initialize a paper project by recording confirmed languages, goal, and processing choices; resume incomplete setup.
---

# Project onboarding

Outcome: confirmed settings sufficient to begin, an accurate `state/current.md`, and one next action. The question, venue, method, and processing choice may remain open when the first task does not need them.

## When to use

Initialize only after a request to begin a paper. A tour uses `paper-hands-on` and changes no files; a bounded first task can proceed without initialization. After a tour, reuse answers already given. Ask one decision question at a time; record only clear answers, in English, while speaking in the interaction language. Preserve all existing material. Never make the researcher repeat settled information.

## Inspect and route

Read `state/current.md` and `requirements/project.md`. Inspect `manuscript/manifest.yaml` and directory names in `inbox/`, `references/originals/`, `ideas/`, `research/`, and `reviews/`. Template READMEs, empty indexes, and standing communication or English-document rules are not research material. Read a specific index or record only to resolve the current task.

- **New workspace:** status not initialized and no research material. Proceed below, even if standing template rules are already recorded. Files in `inbox/` are intake material, not another paper.
- **Interrupted setup:** paper-specific answers are recorded but status is incomplete. Continue at the first open item.
- **Existing paper:** status initialized or actual sources, manuscript sections, retained ideas, research records, or review rounds exist. Read [existing workspace](existing-workspace.md) to continue that paper or start a fresh copy.

For a setup request, say briefly what will be recorded and that unknown choices can wait. After a tour, go straight to the next missing choice.

## Disconnect the template remote

Once the researcher has asked to initialize this paper, tell them in one sentence that setup disconnects any link to the original template repository, while local versions and personal remotes remain. Run `python scripts/versions.py detach-template` before marking setup complete. For an unambiguous ordinary copy, run it with `--apply` and check again. A folder with no Git or no remote needs no change. If the result has mixed or uncertain addresses or shared worktrees, explain the issue and leave setup incomplete until the researcher decides. If `.git/config` access needs narrow local approval, request it when available; if not granted, leave setup incomplete. Do not disconnect during a tour, a bounded task, or template maintenance. Run `versions.py inspect` only for a history question or a real history ambiguity.

## Confirm only needed settings

1. **Conversation language.** Reuse a clear instruction or ask whether to use the researcher's current language. Explain that conversation uses that language and project records use English.
2. **Goal.** Ask for an interest, topic, question, or existing draft. “Not sure yet” is valid. Record a faithful English rendering of the researcher's answer, quoted without a translation label; do not turn an interest into a scientific question. Use material already present to avoid another question.
3. **Target paper language.** Ask only when the next task prepares publication text or the researcher wants to settle it. Raw notes and working drafts may use another language. Recommend from a confirmed venue when possible; do not infer the target from a draft's language. “Decide later” is valid.
4. **Document processing.** Ask only when documents need conversion now or the researcher wants to settle it. Read [document processing choice](document-processing.md) for the computer check, local/cloud options, scope, and deferred setup. Plain text and Markdown need no processing choice.
5. **Application privacy.** Offer `privacy-configuration` only when requested or relevant to the selected task. Do not make an account check a prerequisite to unrelated work. A declined or postponed offer belongs only in `state/current.md`.

Write each confirmed answer as soon as it arrives. Put status, goal, languages, and any confirmed audience, article type, or venue in `requirements/project.md`. Put confirmed document-processing and data-use choices, with their document scope, in `requirements/privacy.md`. Keep unknown choices open. Route any writing rule to `constraint-maintenance`. An offered or deferred choice is not a requirement.

## Finish

After the agreed setup and template-remote check, mark the project initialized with the date. If interrupted, retain incomplete status and recorded answers. Write `state/current.md` in English with what is set, open, and next. Report the settings with links and continue an already requested first task once its prerequisites are met. The optional `inbox/` is an intake place; the researcher can give an accessible existing file path instead.

Check that every recorded item came from a clear instruction, nothing was inferred or overwritten, the state names the next action, and no template remote remains on an initialized paper. A mixed or shared remote remains open for the researcher's decision.
