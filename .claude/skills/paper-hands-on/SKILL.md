---
name: paper-hands-on
description: Use when the researcher asks, in any language and without naming a task, to continue or resume previous work, asks what to do next, or wants guidance through research and manuscript development. Recognizes the current stage, helps the researcher examine evidence and choices, and connects authorized tasks toward the agreed goal using existing project records. A request for one named task goes to that task's skill instead.
---

# Paper hands-on

Outcome: progress toward the researcher's agreed goal, with inspectable evidence, research choices brought back for discussion, and authorized routine work connected through the existing records. The researcher directs the inquiry and final expression; the agent prepares comparisons, challenges assumptions, and carries the production and coordination. An interrupted session can continue from `state/current.md` and the linked records.

## How to guide

- This skill selects and connects tasks; it never repeats their procedures. Each step is carried out exactly as the matching skill says, with its own checks.
- Work toward the requested outcome, not a fixed sequence of lessons. Explain each useful action briefly, carry it out, and continue through routine handoffs already covered by the request and confirmed choices. A progress update is not a request for permission. Ask only for missing judgments, material or access, and major choices.
- Help the researcher understand what the evidence permits: distinguish observations, interpretations, and hypotheses; surface competing explanations and evidence that could change the conclusion. Do not select a scientific conclusion just to keep the work moving.
- Never hand the researcher a technical chore: no copying between tools, no editing of records, no running commands, no keeping track of progress.
- A direct request for one task goes straight to its skill; the guided path is optional and never forces earlier stages.

## Step 1: Recognize where the project stands

1. Read `state/current.md`, then run `python scripts/status.py` (read-only). It summarizes the library, ideas, plan, results, venues, outline, manuscript, checks, builds, releases, review rounds, revisions, feedback, and unsaved work, and lists the gaps that suggest a next task.
2. Establish the current goal, authorized scope, and what would count as a useful delivery from the request and confirmed records. Ask only when those leave a material ambiguity. Their account takes precedence over the signals; do not turn a request for a paragraph into a whole-paper workflow.

## Step 2: Choose the entry and the next step

3. Common entries, each continuing along the same standalone skills:

   | The researcher has | First steps |
   | --- | --- |
   | Only an interest | `project-onboarding`, then `literature-discovery` and `source-ingestion`, then `literature-and-evidence` and `research-ideation` |
   | Readings or a library | `literature-and-evidence`, `research-ideation` or `idea-deepening` |
   | An idea | `idea-deepening`, `impact-assessment`, `research-planning` |
   | Data or a planned analysis | `research-planning`, then `research-code-setup` for the runs and result records |
   | An existing draft | `manuscript-import`, then `manuscript-audit`, then `manuscript-writing` or `manuscript-revision` |
   | A target venue to meet | `journal-selection`, then `submission-assembly` and `submission-readiness` |
   | Reviewer comments | `review-ingestion`, then `review-response` |
   | Advice from colleagues | `research-feedback` |

4. Choose the action that advances the agreed goal: missing results block related findings; an unsettled argument needs discussion; stale checks need renewal. Name the needed inputs, the expected artifact, the check that will establish completion, and any research choice it depends on. Reuse existing confirmations instead of asking again.
5. Research that cannot be done with the available material, tools, or access (fieldwork, laboratory work, institutional data) becomes an external dependency with a prepared next step. Never fill it with invented findings, and say plainly that the paper cannot claim what the research has not shown.

## Step 3: Carry out the step and connect it

6. Run the step with its skill. Its results land in the shared records: sources in `references/`, ideas in `ideas/`, the plan, results, decisions, venues, and feedback in `research/`, the outline and sections in `manuscript/`, profiles in `requirements/profiles/`, outputs in `outputs/`, reviews in `reviews/`. The next step reads them from there.
7. After the step, update `state/current.md` in the interaction language: the goal, the stage reached, what was done in this step, what is open (including any question waiting for the researcher), and the next step. Replace outdated lines; keep it short.

- Before handing off, inspect the artifact and its checks; a file's existence or a successful command alone does not establish completion. Link the actual inputs, outputs, checks, and unresolved questions in the owning source note, plan, result, outline, audit, or revision record. Do not create a parallel task database.
- Bring a result back as a supported observation, its plausible interpretations and limits, and the next useful check or choice. If it challenges the agreed explanation, inspect technical errors and contrary evidence first; propose the scientific alternatives for the researcher to decide.
- Continue within scope until the goal is delivered or a necessary judgment or external dependency prevents progress. A pending choice blocks dependent work only; complete independent authorized work where useful. Do not replace missing evidence with a stronger claim or stop solely because a skill returned.
- For routine technical failures, preserve logs and try a bounded repair within the existing method and permissions: at most two repair attempts per failing action, stopping earlier if the same failure repeats without progress. Record the attempts and remaining blocker in the owning work record; keep only a short link in state. A negative scientific result is evidence, not an error to retry away. Escalate a changed method, resource, service, or cost through the existing confirmation rules.

## Step 4: Milestones

8. Offer to save a version (`git-save`) at natural milestones: after setup, after the first complete draft, before a major revision, and before a release. Offer `git-hands-on` when the researcher wants to learn version control. Nothing leaves the computer without an explicit instruction for that destination (`git-backup`).
9. Before the paper is presented as ready, run `submission-readiness` with current checks. A formatted file, a checked draft, and a paper ready to submit are different milestones; submission is the researcher's own action.

## Step 5: Pause and resume

10. When the session ends or the researcher switches tasks, make sure `state/current.md` names the next step. A later session starts again at Step 1 and continues from the records, without repeating completed imports, analyses, or checks whose inputs have not changed.

On resumption, read the linked work and actual current files, then check run records (`research.py runs`), result freshness (`research.py check`), and relevant manuscript checks. Reconcile intervening author edits before applying a candidate. Use a still-valid artifact rather than repeating expensive work. Keep the goal and scope, links to completed work and checks, the precise unanswered question or blocker, and the next independent or dependent action in the short state note; never store an inferred preference there.

## Completion check

- Each completed step was done by its standalone skill, and its result is in the shared records.
- The agreed goal was delivered or its specific remaining dependency is stated; routine authorized handoffs did not require the researcher to dispatch each skill.
- The researcher can see what was observed, what remains interpretation, and which scientific choice is theirs; favorable model assessments do not establish correctness.
- Scientific choices, uploads, account changes, and submission were left to the researcher, and every major decision was confirmed.
- No result, source, or finding was invented to move the paper forward; missing research is named as such.
- `state/current.md` names the stage and the next step, and nothing technical was handed to the researcher.
