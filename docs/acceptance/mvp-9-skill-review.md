# MVP 9 Skill Review

Status: `paper-hands-on` passed written review on 2026-10-29 under the gate used since MVP 2, and passed a second look the same day after the change to its description (section 6). `scripts/status.py` passes 2 tests. On 2026-10-29 the maintainer confirmed the MVP 2-style gate for MVPs 1–9; the complete-path exercise is optional follow-up verification, with its observations and limits in section 5.

## 1. Rule and pass criteria

Fixed before the review, as in the [MVP 4 review](mvp-4-skill-review.md#1-rule-and-pass-criteria). The coordinator passes only if it adds no second implementation of another skill's procedure.

## 2. Method and evidence

Read `.agents/skills/paper-hands-on/`, `scripts/status.py`, and `scripts/tests/test_status.py`, against MVP 9 in the [implementation guideline](../mvp-implementation-guideline.md#mvp-9--connected-paper-hands-on-and-release-candidate), the [hands-on design](../hands-on.md), the [research workflow review](../research-workflow-review.md) sections 4 and 7, design plan sections 3 (researcher-facing experience) and 9, and `AGENTS.md`.

| Evidence | Result |
| --- | --- |
| `python -m unittest scripts/tests/test_status.py` | 2 tests, OK: a new workspace points to setup and literature; a drafted paper with open review items and feedback points to those items, an audit, and a build, and not to setup |
| `python scripts/status.py` on the template and on the live MVP 6 copy | Correct summaries, no changes made |

## 3. Requirements

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| PH-1 | Stage recognition, one useful next action, focused questions, and concise resumable state | Met | L19–L20, L37, L43, L52; `status.py` lists the records and the gaps. |
| PH-2 | Entry from an interest, a library, an idea, a draft, data, a venue, reviewer comments, or advice, without forcing a course | Met | L15, L24–L35. |
| PH-3 | Coordinates existing skills and duplicates none of their procedures | Met | L12; the table names skills only. |
| PH-4 | Links to the Git guide at milestones and the review extension after actual comments | Met | L47 (milestones, `git-hands-on`), L34 (reviewer comments). |
| PH-5 | Scientific judgment, uploads, account changes, and submission stay explicit decisions of the researcher | Met | L48; completion check. |
| PH-6 | No manual technical-file maintenance, copying between stages, or status reconstruction by the researcher | Met | L14, L42–L43. |
| PH-7 | No invented findings; missing research is reported as an external dependency | Met | L38. |
| PH-8 | Reuse of outputs and checks; no repeat of completed work after a pause | Met | L52; stale detection in `research.py`, `manuscript.py checks`, and `export.py verify`. |

## 4. Gaps found and fixed

- F-1: the first version of the review-round signal in `status.py` compared text fragments; rounds are now counted as data (items and answered items), and the test covers a partly answered round.

## 5. Not covered: the complete-path test

The original complete-path scenario was a stricter live framework exercise, now optional under the maintainer’s 2026-10-29 decision. A deterministic scripted pass and a partial mixed-agent exercise are recorded in [implementation status](../implementation-status.md) and the [test record](mvp-9-complete-path.md). The full live path has not passed; acceptance by review does not establish the untested platforms, services, or real submission readiness.

## 6. Second look after the resume-trigger change (2026-10-29)

[Complete-path run 2](mvp-9-complete-path.md) showed that two fresh sessions, each started with the generic request “我们继续上次的工作。”, did not call `paper-hands-on`. Its description already named continuing as a trigger, but at the end of a long sentence. The maintainer chose to move that case to the front (“按推荐处理”). Only the description (L3) changed, and the README of the skill gained one example request. The body of the skill (L6 to L59) and `status.py` did not change, so no line number moved. The criteria in section 1 did not change.

| Check | Result |
| --- | --- |
| The whole skill re-read against PH-1 to PH-8 and the sources of section 2 | All Met. The new first clause of the description (continue or resume without naming a task, in any language) leads to the behavior of L19–L20 and L52, and its last sentence (a request for one named task goes to that task's skill) matches L15. So PH-2 (no forced course) and PH-3 (no second copy of another skill's procedure) are not weakened, and the description repeats no procedure |
| Line citations of section 3 | Three were one line off and are corrected in the table: PH-2 cites L15, PH-4 cites L34 for reviewer comments, and PH-6 cites L14 |
| Description rules | 776 characters (the limit is 1024), on one line, readable as YAML. `sync_skills.py --check` passes, and the Claude Code copy matches |
| Narrowness of the trigger | The resume case is limited to a request that names no task, so “continue writing the discussion” still goes to `manuscript-writing`. A review cannot show how a model routes it |

Still not covered: whether a model now calls the skill after a bare request to continue. The precedent is the readiness question: a description that led with its triggers raised the use of `environment-management` from 1 of 3 to 8 of 10 samples with Haiku ([implementation status](../implementation-status.md), run 10). That is a precedent, not a result for this skill, and live runs ended with the 2026-10-28 ruling. The other misses of run 2 stay recorded as residual risks (see the [follow-up in the run 2 record](mvp-9-complete-path.md)).

Verdict: `paper-hands-on` still passes.
