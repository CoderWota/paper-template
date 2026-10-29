# MVP 9 Skill Review

Status: `paper-hands-on` passed written review on 2026-10-29 under the gate used since MVP 2, and `scripts/status.py` passes 2 tests. On 2026-10-29 the maintainer confirmed the MVP 2-style gate for MVPs 1–9; the complete-path exercise is optional follow-up verification, with its observations and limits in section 5.

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
| PH-2 | Entry from an interest, a library, an idea, a draft, data, a venue, reviewer comments, or advice, without forcing a course | Met | L14, L24–L35. |
| PH-3 | Coordinates existing skills and duplicates none of their procedures | Met | L12; the table names skills only. |
| PH-4 | Links to the Git guide at milestones and the review extension after actual comments | Met | L47 (milestones, `git-hands-on`), L35 (reviewer comments). |
| PH-5 | Scientific judgment, uploads, account changes, and submission stay explicit decisions of the researcher | Met | L48; completion check. |
| PH-6 | No manual technical-file maintenance, copying between stages, or status reconstruction by the researcher | Met | L13, L42–L43. |
| PH-7 | No invented findings; missing research is reported as an external dependency | Met | L38. |
| PH-8 | Reuse of outputs and checks; no repeat of completed work after a pause | Met | L52; stale detection in `research.py`, `manuscript.py checks`, and `export.py verify`. |

## 4. Gaps found and fixed

- F-1: the first version of the review-round signal in `status.py` compared text fragments; rounds are now counted as data (items and answered items), and the test covers a partly answered round.

## 5. Not covered: the complete-path test

The original complete-path scenario was a stricter live framework exercise, now optional under the maintainer’s 2026-10-29 decision. A deterministic scripted pass and a partial mixed-agent exercise are recorded in [implementation status](../implementation-status.md) and the [test record](mvp-9-complete-path.md). The full live path has not passed; acceptance by review does not establish the untested platforms, services, or real submission readiness.
