# MVP 4 Skill Review

Status: all seven MVP 4 skills, and the extension of `research-investigation` to project results, passed written review on 2026-10-28 under the gate used for MVP 2 and MVP 3. The deterministic scripts pass their tests: 15 tests for `scripts/research.py` and 2 new tests for feedback import, in a full suite of 96. This does not verify any behavior on Windows or in Codex, or how a given model follows the text; see section 7.

## 1. Rule and pass criteria

The criteria were fixed before the review started and follow [section 6 of the MVP implementation guideline](../mvp-implementation-guideline.md#6-completion-record-for-each-mvp) and the MVP 3 gate (“我们验收标准和mvp2差不多的标准就行”):

- A skill passes when every readable requirement listed below is met by its text, after any fix made during the review, with the file and lines that meet it.
- A requirement carried by a script counts as met only with an automated test or a recorded synthetic observation.
- A requirement that only a real platform, host, or service can show stays not covered and unverified; the review never turns it into a pass.
- Observed misses of a model are residual risks, not review failures, unless the text lacks or blurs the required behavior.

## 2. Method and evidence

Read the seven new `SKILL.md` files and their READMEs, the changed sections of `research-investigation`, `constraint-maintenance`, `project-onboarding`, `review-ingestion`, and `source-ingestion`, `scripts/research.py`, the changed ingestion modules (`reviews.py`, `pipeline.py`, `common.py`) and `ingest.py`, the new and changed tests, and the READMEs of `research/`, `research/decisions/`, `research/feedback/`, `research/results/`, `research/venues/`, and `ideas/`.

Requirements reviewed: MVP 4 in the [implementation guideline](../mvp-implementation-guideline.md#mvp-4--ideas-impact-and-feasible-research-plans); [design plan](../design-plan.md) sections 4 (directory README contract), 7 (research decision and feedback records), 9 (skill catalog, common boundaries, research ideation and idea deepening, expected research interaction), and 11 (ideas and research code); [`AGENTS.md`](../../AGENTS.md); the [interaction specification](../agent-interaction.md); the [skill-package rules](../../.agents/skills/README.md); the [research workflow review](../research-workflow-review.md) sections 3 and 6 for result production; and the maintainer's decision of 2026-10-28 that `research-code-setup` and `research-investigation` produce results, recorded in `research/results/`, without a new skill.

Mechanical and script checks, run on 2026-10-28 after the review fixes (macOS 26.6.2, Apple Silicon, Python 3.12.9):

| Check | Result |
| --- | --- |
| `python -m unittest discover -s scripts/tests` | 96 tests, OK; 15 in `test_research.py`, and 2 new feedback-import tests in `test_ingest.py` |
| `python scripts/sync_skills.py --check` | 17 packages; copies match |
| `python scripts/check_capabilities.py` | The availability table matches the skills folder |
| `python scripts/check_readmes.py` | Every project directory has a README, including `research/results/` and `research/venues/` |
| `python scripts/research.py check` | The template's empty research records have the required form |
| `python -m compileall -q scripts` | Pass |

Claude Code listed the seven new skills in this session after their copies were generated, which shows discovery of the generated copies by Claude Code 2.x on macOS. No skill was run in a fresh session.

## 3. Requirements shared by the seven skills

| ID | Requirement | Source | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| CC-1 | One canonical package per skill with the required frontmatter, English instructions, a people-facing README, and a generated Claude Code copy | `AGENTS.md` (Skills); skills README | Met | Seven packages with `README.md` and `SKILL.md`; names equal directories; descriptions are one line (450 to 600 characters); `sync_skills.py --check` passes. |
| CC-2 | Each skill states triggers, inputs and records to read, outputs, completion checks, and handoffs | Design plan §9 (L505) | Met | Each description names its triggers; each body starts with its records to read and ends with a completion check; handoff lines name the neighbouring skills. |
| CC-3 | Shared rules stay in `AGENTS.md`: confirmation, question form, language, decisions; skills refer to them | Skills README; design plan §9 (L507); rule placement, principle 2 | Met | Skills say "a major decision: ask the confirmation question" and "the shared question form" without restating the rules; decision records go through `constraint-maintenance` and the folder README. |
| CC-4 | Records the researcher reads are in the interaction language, with fixed, checkable labels | `AGENTS.md` (Language and formats); rule placement, principle 4 | Met | Layouts in the READMEs of `research/decisions/`, `research/feedback/`, `research/results/`, `research/venues/`, and `ideas/`; `research.py check` reads English labels and the listed Chinese labels; tests use Chinese and English records. |
| CC-5 | No invented sources, gaps, data, results, numbers, or acceptance probabilities | `AGENTS.md` (Evidence and integrity); design plan §9 (L513, L525) | Met | `research-ideation` L26; `idea-deepening` L20; `impact-assessment` L21; `journal-selection` L19, L26; `research-planning` L26; `research-code-setup` L46. |
| CC-6 | Offer only what the availability table lists | `AGENTS.md` (Capabilities) | Met | Handoffs to MVP 5 and MVP 6 skills say "as the availability table in `AGENTS.md` allows" (`research-planning` L36, `journal-selection` L32, `research-feedback` L49). |
| CC-7 | Every created directory has a meaningful README | Design plan §4 (L239–L255) | Met | `code-init`, `run`, and the feedback import write READMEs; tests `test_code_init_creates_only_requested_parts_and_keeps_added_text` and `test_a_feedback_event_keeps_each_contributors_comments_apart_from_review_rounds` run `check_readmes.py` on the result. |

## 4. Requirements by skill

### 4.1 `research-ideation`

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| RID-1 | Organize starting thoughts from interests, materials, observations, and constraints; help an undeveloped thought before examining it | Met | L12–L14. |
| RID-2 | Propose a small set of meaningfully different directions, fitted to the discipline, without requiring experiments | Met | L18 (three to five, differing in kind; no forced experiment). |
| RID-3 | Each direction states question, contribution, basis, assumption, feasibility, and first check | Met | L19–L25. |
| RID-4 | Keep novelty, significance, feasibility, and support apart; qualify originality; never invent a gap | Met | L26. |
| RID-5 | Save only on the researcher's request, in `ideas/` with an index; a retained idea or hypothesis is not a rule or evidence | Met | L31–L33; `ideas/README.md` layout; test `IdeaTests`. |

### 4.2 `idea-deepening`

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| IDP-1 | Investigate what workspace material or authorized searches can answer before asking | Met | L14. |
| IDP-2 | One substantive question at a time with the reason and a recommendation; wait for the answer; dependency-aware order | Met | L13, L18. |
| IDP-3 | Challenge a weak premise without pressure or a long questionnaire | Met | L19. |
| IDP-4 | Compare the nearest inspected prior work; label originality preliminary when coverage is limited | Met | L20. |
| IDP-5 | Separate novelty, significance, feasibility, and support; offer alternatives | Met | L21–L22. |
| IDP-6 | Summarize at checkpoints and stop when a next action is clear | Met | L26–L27. |
| IDP-7 | Update a retained idea note; a consequential choice becomes a decision only after confirmation | Met | L31–L32. |

### 4.3 `impact-assessment`

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| IMP-1 | Why the contribution matters, to whom, what supports and limits its value | Met | L17–L20. |
| IMP-2 | Ground claims in inspected sources or project results; label assumptions | Met | L17, L19. |
| IMP-3 | Keep impact apart from novelty, venue fit, and readiness; no metric-based value, no acceptance prediction | Met | L21. |
| IMP-4 | Concrete ways to strengthen the contribution, with what each needs | Met | L25–L26. |
| IMP-5 | Keep the assessment only on request; it is not evidence | Met | L30–L31. |

### 4.4 `journal-selection`

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| JS-1 | Read current official sources: scope, article types, length and structure, AI-use policy, and relevant publications | Met | L18, L20. |
| JS-2 | Record source addresses and reading dates; label unchecked facts; no facts from memory | Met | L18–L19; `research/venues/README.md`; test `test_venue_notes_need_a_date_and_official_addresses`. |
| JS-3 | Fit is assessed separately from impact and readiness; no acceptance probability | Met | L25–L26. |
| JS-4 | Compare at least two venues on the same criteria, and examine a specified venue | Met | L13, L27. |
| JS-5 | The result informs drafting (AI policy) and the output profile; the target is recorded only after confirmation | Met | L21, L32. |
| JS-6 | Web queries carry no unpublished material | Met | L14. |

### 4.5 `research-planning`

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| RP-1 | Connect methods, required evidence, current resources, limitations, and next actions | Met after fix F-1 | L17–L21, L30. |
| RP-2 | Discipline-appropriate methods, including argument and interpretation; no forced experiment or structure | Met | L18. |
| RP-3 | Separate evidence already available from work still required; never write an expected finding as a result | Met | L17, L26. |
| RP-4 | External dependencies and work that needs the researcher are explicit, with a prepared next step | Met | L19–L20. |
| RP-5 | Consequential choices only after confirmation, with decision records; unconfirmed parts marked proposed | Met | L25. |

### 4.6 `research-feedback`

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| RF-1 | Accept advice from any contributor regardless of title; formal reviews go elsewhere | Met | Description; L12–L14. |
| RF-2 | Shared extraction mechanics; originals kept unchanged; privacy scope respected | Met | L20–L27; `ingest.py --to research/feedback/<feedback-id>`; test `test_a_feedback_event_keeps_each_contributors_comments_apart_from_review_rounds`. |
| RF-3 | Preserve each suggestion's attribution in multi-person documents and meetings; label exact statements, recollections, and summaries | Met | L32–L37; Word comment authors are kept by the import (test above); `actions.md` check requires `From`, `Source`, and `Kind` (`FeedbackTests`). |
| RF-4 | No ranking by title; conflicts resolved by the researcher; no suggestion becomes a rule before adoption | Met | L12–L13, L42–L43, L48. |
| RF-5 | A collaborator-supplied outline stays advice until adopted | Met | L38. |
| RF-6 | Distinguish accepted from implemented; link the actual change; declined advice never becomes active | Met | L47–L50; check requires a `Decision` quote or link for decided items and an existing `Change` target for implemented ones (`test_adoption_without_the_researchers_words_and_unlinked_changes_are_reported`, `test_a_change_link_must_exist_and_statuses_are_known`). |

### 4.7 `research-code-setup`

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| RCS-1 | Elicit actual needs before creating `code/`; nothing for non-code research | Met | L12–L14. |
| RCS-2 | Proportionate structure with READMEs; existing descriptions kept | Met | L19–L25; test `test_code_init_creates_only_requested_parts_and_keeps_added_text`. |
| RCS-3 | Research environment separate from ingestion tools; versions recorded | Met | L26; test `test_the_research_environment_is_separate_and_recorded_with_the_run` (the run uses `code/.venv`, and its package list is recorded). |
| RCS-4 | A reproducible smoke task on labeled test data | Met | L31; tests run a smoke task and record command, code checksum, interpreter, inputs, outputs, and logs (`test_a_run_records_command_code_inputs_outputs_and_logs`). |
| RCS-5 | Result production (maintainer decision): authorized analyses with provenance, checks, and result records that keep statuses distinct; failed results kept; nothing invented | Met | L32–L47; `research/results/README.md`; tests `test_failures_and_missing_outputs_are_recorded_and_missing_inputs_refused` and `test_result_records_detect_stale_inputs_and_unsupported_checked_status`. |
| RCS-6 | A changed input makes a result stale until it is run again | Met | L47; stale detection test above (exit status 2). |

### 4.8 `research-investigation` (extended)

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| RI-4 | Documentary, qualitative, and theoretical results get result records with inputs, method, checks, and a status that matches the checks made; quick questions get none | Met | L33–L43. |

### 4.9 Record formats (design plan §7: formats refined in MVP 4)

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| RC-1 | Decision records: date, confirmed choice and scope, context, reasons and alternatives, evidence links, consequences, supersession links in both directions, earlier rationale kept | Met | `research/decisions/README.md`; `check_decisions` requires the fields and a quotation, checks both directions of replacement and the index line (`DecisionTests`). |
| RC-2 | Feedback records: attribution, kind, status values received to implemented, decision and change links | Met | `research/feedback/README.md`; `check_feedback` (`FeedbackTests`). |
| RC-3 | Avoid a full decision record for every edit | Met | `research/decisions/README.md` first paragraph; `constraint-maintenance` L16. |

## 5. Gaps found and fixed during the review

- F-1: the research plan named risks and alternatives but not the limitations that the plan accepts, which the guideline requires ("limitations"). Fixed in `research-planning` step 7, the record sections, and the completion check.
- F-2: earlier skills still called research feedback and idea development "not available yet". Fixed in `constraint-maintenance` (table row, README, and the decision-record layout and check), `review-ingestion` (step 1), `source-ingestion` (routing table), and `project-onboarding` (step 3). The routing row for manuscripts and templates stays "not available yet" until MVP 5 and MVP 6.

No script requirement lacked test evidence after these fixes.

## 6. Verdict

| Skill | Verdict |
| --- | --- |
| `research-ideation` | Accepted by review, 2026-10-28 |
| `idea-deepening` | Accepted by review, 2026-10-28 |
| `impact-assessment` | Accepted by review, 2026-10-28 |
| `journal-selection` | Accepted by review, 2026-10-28 |
| `research-planning` | Accepted by review, 2026-10-28 |
| `research-feedback` | Accepted by review, 2026-10-28 |
| `research-code-setup` | Accepted by review, 2026-10-28 |
| `research-investigation` (result records) | Extension accepted by review, 2026-10-28 |

## 7. Not covered

- Reading venue pages with the agent application's web access: no venue was examined live, so the reachability of official pages and the handling of an unreadable page are unverified.
- How a model follows the one-question-at-a-time interview, the challenge of weak premises, and the separation of novelty, significance, feasibility, and support. The MVP 1 runs make occasional misses likely; no live run was made.
- Research runs with languages other than Python, large data, long runs, and runs on Windows (path forms such as `code\.venv\Scripts\python.exe` are documented but not exercised).
- Codex discovery of the seven skills; Windows; the ASD-STE100 review of English questions.
- The complete-path test, which needs MVPs 5 and 6.
