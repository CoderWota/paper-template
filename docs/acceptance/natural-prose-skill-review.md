# Natural Prose Skill Review

Status: `natural-prose`, added after MVPs 1–9, passed written review on 2026-10-29 under the gate used since MVP 2. The skills that it extends (`manuscript-writing`, `manuscript-audit`, `submission-readiness`, `research-code-setup`, and `manuscript-outline`) passed a second look on the same day. `scripts/check_edit.py` passes 11 tests, and the whole script suite passes 192 tests. Live behavior of a model, Codex, and Windows are not covered; see section 6.

## 1. Rule and pass criteria

Fixed before the review, in the plan that the maintainer approved, as in the [MVP 4 review](mvp-4-skill-review.md#1-rule-and-pass-criteria): every requirement of sections 3 and 4 must be met by the text of the skills, with line evidence, and the mechanical checks of section 2 must pass. A second look passes only when the extended skill still meets the requirements of its earlier review.

## 2. Method and evidence

Read `.agents/skills/natural-prose/` (SKILL.md, README.md, `patterns.md`, and the English, Chinese, and Japanese lists), the changed SKILL.md and README.md files of the five extended skills, the new `manuscript-writing/editing-guide.md` and `research-code-setup/figure-guide.md`, `scripts/check_edit.py`, `scripts/check_edit.json`, and `scripts/tests/test_check_edit.py`, against [design plan](../design-plan.md) section 9, the [Markdown and export conventions](../markdown-and-export-conventions.md), [rule placement](../rule-placement.md), `AGENTS.md`, and the earlier reviews of the extended skills ([MVP 4](mvp-4-skill-review.md), [MVP 5](mvp-5-skill-review.md), [MVP 6](mvp-6-skill-review.md)).

| Evidence | Result |
| --- | --- |
| `python -m unittest scripts/tests/test_check_edit.py` | 11 tests, OK: a lost citation and lost hedges in English; a changed number and a lost negation in Chinese; a lost hedge in Japanese as a warning only; words that merely contain a negation or a limiting character; protected front matter, code, labels, and open markers, including full-width ones; formatting differences and a list turned into prose that are not losses; a faithful and an unfaithful translation; the note for a translation checked without the flag; no Chinese or Japanese vocabulary in the Python code |
| `python -m unittest discover -s scripts/tests` | 192 tests, OK |
| `python scripts/sync_skills.py --check` | 34 packages; the Claude Code copies match |
| `python scripts/check_capabilities.py`, `check_readmes.py`, `check_requirements.py` | Pass (105 project directories) |
| Descriptions | One line each, valid YAML: `natural-prose` 650 characters, `manuscript-writing` 628, `manuscript-audit` 677, `research-code-setup` 626 (the limit is 1024) |
| Walk-through: the 18 Before and After examples of the three language lists, each run through `check_edit.py` | Every protected item is kept, except the `[TODO: ...]` markers that six examples add on purpose for missing evidence. The word warnings name only intended changes: the negation of a staged contrast and stacked hedges reduced to one. The walk-through exposed one false warning (a limiting character inside the Chinese "not only" construction), fixed in `check_edit.json` and covered by a test |
| Own wording | The external material that informed this extension was kept outside the repository and compared with every new and changed file: no shared fragment of 8 words or 10 Chinese or Japanese characters. Shorter shared fragments are only the stock phrases that the lists quote as patterns and Python boilerplate. A search of the whole workspace finds none of that material's names, authors, or addresses |

## 3. Requirements of `natural-prose`

Line numbers refer to `natural-prose/SKILL.md` unless another file is named.

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| NP-1 | Triggers on text that reads as AI-generated, formulaic, inflated, or translated, in any language, for manuscript text, response letters, and other text; a check-only mode that never edits | Met | L3; L12; L25. |
| NP-2 | Meaning kept: no added fact, number, source, example, opinion, or experience; every claim, number, citation, cross-reference, hedge, negation, condition, and attribution kept; a missing source becomes a `[TODO: ...]` marker; the edit is compared with the original | Met | L15, L28–L29, L35, L37; completion check L48; `check_edit.py` and its tests. |
| NP-3 | Confirmed rules, venue requirements, and the researcher's own voice outrank every pattern; a pattern becomes a rule only through `constraint-maintenance` with confirmation | Met | L13–L15, L43; `patterns.md` L11 and "When not to act" (L84). |
| NP-4 | No judgment of authorship, no detector score or promise; disclosure duties unchanged | Met | L21, L42, L50; `patterns.md` L12. |
| NP-5 | Lists for English, Chinese, and Japanese; other languages through the families, with the limit stated | Met | L19; the three language lists; `patterns.md`. |
| NP-6 | Application through the existing routes: manuscript edits as `manuscript-writing` applies them, with its check; response letters with `review.py check`; text from the conversation in the reply; a saved version offered before a pass over several sections | Met | L31, L36. |
| NP-7 | Own wording: no text, names, addresses, or credits of the external material | Met | Section 2, last row. |
| NP-8 | No external service, cost, upload, or message | Met | Every step works on local files and local scripts. |
| NP-9 | Shared rules are linked, not copied (rule placement) | Met | Scope rules and the apply step point to `constraint-maintenance` and `manuscript-writing` (L13, L36) instead of repeating them. |

## 4. Second look at the extended skills

The [MVP 5 review](mvp-5-skill-review.md) cites lines of the versions reviewed on 2026-10-29 before this change. In `manuscript-writing`, items from L25 onward moved down by one to four lines; in `manuscript-audit`, items from L14 onward moved down by one to three lines. The requirements themselves did not change.

| Skill | Change | Check | Verdict |
| --- | --- | --- | --- |
| `manuscript-writing` | Description names translation, results passages, and captions, and checking against the original; L25 links the new editing guide and the pattern families; L30 keeps a copy before an edit of existing text; L33 runs `check_edit.py`; L37 adds the literal rendering for checking; a completion line; the conventions link now resolves from both copies (`../../../docs/...`) | MW-1 and CC-1 to CC-6 of the MVP 5 review still hold: scope and rules L12–L13 and L17, conventions L24, the researcher's text L26, support L23. The editing guide adds no route around them: expanding adds no data, results come only from result records, and translation keeps every protected item | Met |
| `manuscript-audit` | Description names formulaic wording, a final check, and a reviewer's view without a score; L14 final check; L23 style patterns; L29 reviewer's view; completion line L44 | MA-1 still holds: separate checks, findings tied to passages, no edit unless asked. The style check is one of the separate checks that the MVP 5 guideline lists. No score or chance of acceptance, as design plan section 9 requires | Met |
| `submission-readiness` | L28 labels each likely concern by presentation or substance and by fixability | The MVP 6 requirements still hold, including no acceptance probability | Met |
| `research-code-setup` | Description adds the chart question; L39 makes a chart an output of a recorded run; new `figure-guide.md` | The MVP 4 requirements still hold: nothing is created for research without code, and runs keep their provenance | Met |
| `manuscript-outline` | L23 links the figure guide for the form of planned figures | MO-1 of the MVP 5 review still holds | Met |

## 5. Adaptations

The external material behind this extension included parts that conflict with `AGENTS.md` or do not fit the workspace. They were not adopted:

- A numerical score for a simulated review: no score, rating, or chance of acceptance is given.
- Recommendations of particular AI models: the workspace does not depend on a model provider.
- Prompts for generating figures with an external image service: the editing guide offers Mermaid diagrams and a written figure brief, and asks for the venue's policy on generated images first.
- Advice to make text sound personal with opinions, experiences, or humor: scholarly text takes its voice only from the researcher's own writing, and Japanese articles keep the である style.
- Formatting rules for LaTeX escaping and for pasting plain text into Word: the workspace conventions govern instead.
- Fixed bans (on dashes, possessives with method names, lists, or a tense for methods): they are signals to examine, and a lasting rule needs the researcher's confirmation.

## 6. Verdict and limits

`natural-prose` passes, and the five extended skills still pass. Not covered: how a model applies the pattern lists, the strength levels, and the polish thresholds (acceptance is by review since 2026-10-28, and no live run was made); real manuscripts; languages other than English, Chinese, and Japanese; Codex; and Windows. The word lists in `check_edit.json` are bounded, and a changed count is only a prompt to read the sentence, not proof that its meaning changed or stayed the same.
