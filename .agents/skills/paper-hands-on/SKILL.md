---
name: paper-hands-on
description: Use when the researcher asks, in any language and without naming a task, to continue or resume the previous work (for example "let's continue where we stopped" at the start of a new session), asks "what should I do next?", or wants to be guided through the whole paper, from an interest, a set of readings, an idea, data, an existing draft, or reviewer comments toward a journal-format manuscript. A request for one named task goes to that task's skill instead. Recognizes the project's current stage from its records, proposes one useful next task at a time, carries it out with the matching standalone skill, connects the results through the shared project files, and keeps a short resumable state, while scientific choices, uploads, and submission stay with the researcher.
---

# Paper hands-on

Outcome: the paper advances by one useful, completed step at a time, each done by the standalone skill that owns it, with its result linked into the project records and `state/current.md` naming the next step, so that any later session continues instead of starting over. The researcher directs and decides; the agent does the production and the coordination.

## How to guide

- This skill selects and connects tasks; it never repeats their procedures. Each step is carried out exactly as the matching skill says, with its own checks.
- One step at a time: say in a sentence what the step is for, do it, show the result, and propose the next step with your recommendation. Ask only for the researcher's judgments, missing material, access that only they have, and major decisions, one question at a time.
- Never hand the researcher a technical chore: no copying between tools, no editing of records, no running commands, no keeping track of progress.
- A direct request for one task goes straight to its skill; the guided path is optional and never forces earlier stages.

## Step 1: Recognize where the project stands

1. Read `state/current.md`, then run `python scripts/status.py` (read-only). It summarizes the library, ideas, plan, results, venues, outline, manuscript, checks, builds, releases, review rounds, revisions, feedback, and unsaved work, and lists the gaps that suggest a next task.
2. Ask what the researcher wants to reach now when the request and the records do not make it clear. Their account takes precedence over the signals.

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

4. Recommend the step that unblocks the most: missing results block a findings section; a missing outline blocks drafting; a stale check blocks readiness. Name what the step will produce and what it needs from the researcher.
5. Research that cannot be done with the available material, tools, or access (fieldwork, laboratory work, institutional data) becomes an external dependency with a prepared next step. Never fill it with invented findings, and say plainly that the paper cannot claim what the research has not shown.

## Step 3: Carry out the step and connect it

6. Run the step with its skill. Its results land in the shared records: sources in `references/`, ideas in `ideas/`, the plan, results, decisions, venues, and feedback in `research/`, the outline and sections in `manuscript/`, profiles in `requirements/profiles/`, outputs in `outputs/`, reviews in `reviews/`. The next step reads them from there.
7. After the step, update `state/current.md` in the interaction language: the goal, the stage reached, what was done in this step, what is open (including any question waiting for the researcher), and the next step. Replace outdated lines; keep it short.

## Step 4: Milestones

8. Offer to save a version (`git-save`) at natural milestones: after setup, after the first complete draft, before a major revision, and before a release. Offer `git-hands-on` when the researcher wants to learn version control. Nothing leaves the computer without an explicit instruction for that destination (`git-backup`).
9. Before the paper is presented as ready, run `submission-readiness` with current checks. A formatted file, a checked draft, and a paper ready to submit are different milestones; submission is the researcher's own action.

## Step 5: Pause and resume

10. When the session ends or the researcher switches tasks, make sure `state/current.md` names the next step. A later session starts again at Step 1 and continues from the records, without repeating completed imports, analyses, or checks whose inputs have not changed.

## Completion check

- Each completed step was done by its standalone skill, and its result is in the shared records.
- Scientific choices, uploads, account changes, and submission were left to the researcher, and every major decision was confirmed.
- No result, source, or finding was invented to move the paper forward; missing research is named as such.
- `state/current.md` names the stage and the next step, and nothing technical was handed to the researcher.
