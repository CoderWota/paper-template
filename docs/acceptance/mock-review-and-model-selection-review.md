# Mock Review and Model Selection Review

Status: `mock-review` and `model-selection`, added at the maintainer's instruction, passed written review on 2026-10-30 under the gate used since MVP 2. The reviewer's view of `manuscript-audit` and step 10 of `submission-readiness` passed a second look. No script changed. Live behavior of a model, Codex, and Windows are not covered; see section 6.

## 1. Rule and pass criteria

Fixed before the review, as in the [MVP 4 review](mvp-4-skill-review.md#1-rule-and-pass-criteria): every requirement of sections 3 and 4 must be met by the text of the skills, with line evidence, and the mechanical checks of section 2 must pass. The two skills must keep the standing rules of `AGENTS.md`: no invented acceptance probability, no key or account identifier in the conversation, consent for a lasting setting change, and availability only through the table.

## 2. Method and evidence

The design of `mock-review` rests on a survey, made on 2026-10-29 and 2026-10-30, of open-source automated reviewers, published evaluations of model reviewers, and the official reviewer forms of several machine-learning and language venues. What the survey showed, and where it entered the skill:

- Automated reviewers fill a venue's form with sub-scores, an overall score, and a confidence score, sample several reviews and merge them in a meta-review, let each review reflect once on itself, and use a cautious stance when unsure. In the skill: the venue's form (L13), three independent perspectives (L19), one reflection (L27), and a meta-review with median and range instead of a mean (L28); the lower anchor when the evidence does not reach a higher one (L20).
- Splitting the review among specialized reviewers gives more specific and fewer generic comments, and different reviewers or models catch different errors. In the skill: the methods, field, and skeptical perspectives (L19).
- Model reviewers score too generously, prefer text that they or a similar model wrote, follow instructions hidden in a manuscript, and accept limitations that authors declare minor; reported agreement between a model's scores and a single human reviewer is at best about the agreement between two human reviewers. In the skill: the bias countermeasures (L20), hidden instructions as a blocking integrity finding (L21), and the statement in every report (L33).
- Novelty judged without retrieval is unreliable. In the skill: originality only against the searched literature, with its coverage stated (L15).
- Venues differ in their forms and scales and revise them yearly, and reviewer policies restrict giving submissions to AI tools. In the skill: the form is read from the venue's current official guidelines into the venue note (L13), and a manuscript received as a reviewer stops at the venue's policy (L12).

For `model-selection`, the official model pages of Claude Code, Codex, and Cursor were read on 2026-10-29 and 2026-10-30; [sources.md](../../.agents/skills/model-selection/sources.md) gives what each said and its date.

| Evidence | Result |
| --- | --- |
| `python scripts/sync_skills.py --check` | 36 packages; the Claude Code copies match |
| `python scripts/check_capabilities.py`, `check_readmes.py`, `check_requirements.py` | Pass (109 project directories) |
| Descriptions | One line each, valid YAML: `mock-review` 713 characters, `model-selection` 624 (the limit is 1024) |
| Names | Neither skill names any surveyed system, paper, or author |
| Overlap with the external writing texts of the earlier extensions | No shared fragment of 8 words or 10 Chinese or Japanese characters in the new files |

## 3. Requirements of `mock-review`

Line numbers refer to `mock-review/SKILL.md`.

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| MV-1 | Triggers on a request for scores, a scored simulated review, or a review on a venue's form; the researcher's own manuscript; a manuscript received as a reviewer stops at the venue's policy | Met | L3, L12. |
| MV-2 | The venue's own form, recorded with its source and date; the general form only when none exists, and said so; no invented anchor | Met | L13; [review-form.md](../../.agents/skills/mock-review/review-form.md), last section. |
| MV-3 | Every score has its quoted anchor, its evidence, and what would raise it; confidence lowered for what was not checked; stale audits and results not reused; originality only against searched literature | Met | L14–L15, L25–L26. |
| MV-4 | Several independent perspectives, one reflection, and a meta-review with median and range | Met | L19, L27–L28. |
| MV-5 | Countermeasures for the known biases of model reviewers | Met | L20. |
| MV-6 | Text in the manuscript is material: instructions to reviewers or AI are reported as a blocking finding, never followed, and never added | Met | L3, L21; completion check. |
| MV-7 | No probability, percentile, chance of acceptance, decision forecast, or comparison with an acceptance rate; the report says it is a simulation | Met | L3, L28, L33; completion check. This keeps the `AGENTS.md` rule against invented acceptance probabilities and design plan section 9. |
| MV-8 | The report is recorded with its inputs, so it becomes stale when they change | Met | L34. |
| MV-9 | No external service, upload, or cost | Met | Every step uses local files and the host's own subagents or sessions. |

## 4. Requirements of `model-selection`, and the second look

Line numbers refer to `model-selection/SKILL.md`.

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| MS-1 | Triggers on choosing, switching, or comparing models for the project's kinds of work | Met | L3. |
| MS-2 | The application, plan type, and provider route are identified from the environment first; only types are asked, never an identifier or a key | Met | L12–L13. |
| MS-3 | Current official pages are read with their dates; no gap is filled from memory; dated starting points exist | Met | L17; `sources.md`. |
| MS-4 | One recommendation per kind of work, only from models that this application and plan offer, with reason and trade-off, based first on the application's own recommendations; no unsupported claim about a provider | Met | L22–L30. |
| MS-5 | Secondary evidence is labeled with its date and what it measures | Met | L18. |
| MS-6 | Switching: a session change on the researcher's request; a saved default only with consent and its scope explained; managed settings never changed | Met | L34. |
| MS-7 | A privacy check before content goes to an unchecked provider; the venue's AI policy and disclosure kept in view | Met | L35. |

| Changed skill | Change | Check | Verdict |
| --- | --- | --- | --- |
| `manuscript-audit`, `reviewer-view.md` | L36: the report still gives no score; a request for scores goes to `mock-review` instead of a refusal | The requirements of the [writing prompts review](writing-prompts-review.md) still hold: WP-4 concerns the converted procedures, and none of them gives a score | Met |
| `submission-readiness` | Step 10 names `mock-review` for a scored review and says that its scores are not a probability either | The MVP 6 requirements still hold, including no acceptance probability | Met |
| `research/venues/README.md` | The note layout gains an optional `Review form` field, where `mock-review` records a venue's form with the date it was read | `python scripts/research.py check` still passes; it reads only the `Checked` and `Sources` labels | Met |

## 5. Decisions

- **Scores, but no probability.** The maintainer asked for review scores as a separate skill. A score on a venue's form is a reviewer's judgment tied to evidence, which `AGENTS.md` and the design plan allow; a probability, a percentile, or a forecast of the decision stays excluded.
- **Model advice is read, not stored.** The maintainer asked for model recommendations that depend on the AI application. Because model offers change from month to month, the skill reads the application's current official pages each time; `sources.md` holds only dated starting points.
- **Names stay out of the skills.** The surveyed systems and papers are not named in the skill text.

## 6. Verdict and limits

Both skills pass, and the two changed files still pass. Not covered: how a model applies the review procedure and how its scores compare with real reviews in this workspace (no live run was made); venues whose forms were not read; model pages of applications other than Claude Code, Codex, and Cursor; Codex and Windows.
