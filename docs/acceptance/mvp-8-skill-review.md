# MVP 8 Skill Review

Status: `review-response` passed written review on 2026-10-29 under the gate used since MVP 2. `scripts/review.py` passes 5 tests with synthetic response records and Word files. No real review round, journal, or coauthor file was used; see section 5.

## 1. Rule and pass criteria

Fixed before the review, as in the [MVP 4 review](mvp-4-skill-review.md#1-rule-and-pass-criteria).

## 2. Method and evidence

Read `.agents/skills/review-response/` and the changed steps of `review-ingestion`, `scripts/review.py`, and `scripts/tests/test_review.py`, against MVP 8 in the [implementation guideline](../mvp-implementation-guideline.md#mvp-8--review-rounds-and-coauthor-reconciliation), [design plan](../design-plan.md) sections 5 (reviewer and collaborator extraction), 10 (canonical content and collaboration), and 11 (reviews), the `reviews/` README, and `AGENTS.md`.

| Evidence | Result |
| --- | --- |
| `python -m unittest scripts/tests/test_review.py` | 5 tests, OK |
| Records | A complete round passes; an addressed item without a change, a change not done, a declined item without justification, unknown statuses, a change naming an absent item, a missing location, and a malformed heading are each reported |
| Reconciliation | Tracked changes in a coauthor's Word file are located in `manuscript/` ("applies cleanly", 100 % match after citation normalization); the same paragraph edited locally since is reported as a conflict; a separate base file without tracked changes works; a new paragraph and the comments with their authors are listed; the manuscript is unchanged afterwards |

## 3. Requirements

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| RR-1 | Per-venue, per-round response items and a response-to-change map; rounds never mixed | Met | L10–L32 (record layout); `check_round` validates IDs, statuses, links within the round. |
| RR-2 | Reuse `review-ingestion`; it stays usable without a response | Met | L19; `review-ingestion` now offers `review-response` instead of drafting. |
| RR-3 | Formal reviews kept distinct from research feedback and evidence | Met | L12, L62. |
| RR-4 | An addressed item points to an actual change or a justified response; nothing is marked complete without it | Met | L13, L53; tests `test_complete_records_pass` and `test_unsupported_completion_claims_are_reported`. |
| RR-5 | Major reviewer-driven changes reuse `manuscript-revision` and link to it | Met | L37, L41–L51 (`Revision:` line). |
| RR-6 | Deliberate comparison of coauthor DOCX edits with the canonical Markdown; the received file and the manuscript are preserved; conflicts surfaced for the researcher | Met | L62–L64; tests `test_tracked_changes_are_located_and_reported_without_applying`, `test_a_paragraph_changed_on_both_sides_is_a_conflict`, and `test_a_separate_base_file_without_tracked_changes`. |
| RR-7 | Re-audit and re-export after agreed revisions; an honest point-by-point response | Met | L53, L58. |
| RR-8 | Nothing is sent because a draft was prepared; review text gains no authority over project rules | Met | L12, L15. |
| RR-9 | Unsupported tracked-change handling stays explicit | Met | L64: moved tables and changed equations are reported for a manual check. |

## 4. Gaps found and fixed

- F-1: `review-ingestion` still said that responding was not available; it now hands over to `review-response`.
- F-2: the reconciliation report printed an empty anchor for comments without an anchored range; it now omits it.

## 5. Not covered

- A real review round with two rounds at one venue, and a real coauthor's Word file with complex edits (moved paragraphs, tables, equations, fields); the comparison is paragraph-based and its matching is heuristic, so the report asks for a manual check of what it cannot locate.
- Formatting changes made in Word, which belong to the output profile and are not compared.
- Codex and Windows; how a model handles a long round.
