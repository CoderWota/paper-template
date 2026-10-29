# Writing Prompts Review

Status: the writing prompts of an external collection were converted into the procedures of `manuscript-writing`, `manuscript-audit`, and `research-code-setup`, and the word lists of `natural-prose` were extended (2026-10-29). Of the 18 prompts, 16 are converted, one is merged into a translation procedure, and one is partly carried over. The verdict and its limits are in section 6.

## 1. Rule and pass criteria

The criteria are the requirements of the conversion. None was changed to fit a result.

- **WP-1.** Each prompt has a destination in the workspace, or a stated reason for leaving it out (section 2).
- **WP-2.** Each converted procedure says what may change, what must stay, and what to report.
- **WP-3.** No LaTeX, Word, or model-specific instruction is a step where the workspace uses Markdown, the export step, or model-neutral instructions.
- **WP-4.** No score, rating, or chance of acceptance appears in any procedure.
- **WP-5.** Translation and expansion add no claim, results passages draw only on result records, and no number is invented.
- **WP-6.** Every style rule is a preset. It is off by default and applies only after the researcher chooses it.
- **WP-7.** The workspace carries no name, address, or credit of the external collection, and no fragment of 8 words or 10 CJK characters is shared with its text.
- **WP-8.** The reviewer's view and the reader check do not claim to predict a review outcome.
- **WP-9.** The skill copies, the availability table, the READMEs, the writing-rule forms, the skill descriptions, and the relative links pass their checks, and the script tests pass.

## 2. Ledger of the prompts

"Before" is the state before this change, judged by reading the files: *Mostly* means the function and most constraints were carried over; *Partly* means the function was carried over without its constraints, output format, or checklist.

| # | Prompt, by function | Before | After | Where | Left out or changed, and why |
| --- | --- | --- | --- | --- | --- |
| 1 | Chinese draft into English manuscript text, with LaTeX output | Partly | Converted | editing-guide: translating into the manuscript language; style-presets: formal English | LaTeX escapes and commands replaced by the workspace Markdown syntax. The style rules (emphasis, quotation marks, dashes, lists, tense) are presets, off by default. |
| 2 | English passage into a Chinese reading aid | Mostly | Converted | editing-guide: translating for reading | Citation and label syntax dropped in the reading only; math rendered in words. |
| 3 | Chinese draft into English plain text for Word | Not included | Merged into 1 | editing-guide: translating into the manuscript language | The no-Markdown output does not apply. The export step builds the Word formatting from the Markdown manuscript. |
| 4 | Chinese notes into a formal paragraph, with a note on the logic | Mostly | Converted | editing-guide: writing from notes; style-presets: formal Chinese | The note on the logic becomes the arrangement report. |
| 5 | Shortening by a set number of words | Mostly | Converted | editing-guide: shortening | The fixed 5–15 word target becomes the researcher's target. Without one, only redundancy is removed. |
| 6 | Expanding by a set number of words, making implied conclusions explicit | Mostly | Converted, restricted | editing-guide: expanding | Only what the text or its checked sources already entail. Each addition is logged with its basis. |
| 7 | English polish to top-venue standard | Partly | Converted | editing-guide: polishing; style-presets: formal English | Change thresholds added. The word-choice, possessive, "of", and list rules are presets. |
| 8 | Chinese polish that keeps sound sentences | Partly | Converted | editing-guide: polishing; style-presets: formal Chinese | The change thresholds are explicit. The register, punctuation, and bilingual-bracket rules are presets. |
| 9 | Logic red-line check | Mostly | Converted | manuscript-audit: final check (step 3) | Blocking problems only, and a plain statement when there are none. |
| 10 | Removing AI style, English | Mostly | Converted | natural-prose: patterns-en, stock vocabulary | The word list is regrouped by type, with reasons. Each entry is a signal, not a ban. |
| 11 | Removing AI style, Chinese | Mostly | Converted | natural-prose: patterns-zh, stock vocabulary | An empty-emphasis group and a praise-to-fact example added. |
| 12 | Architecture diagram of a method | Mostly | Converted | editing-guide: method and overview diagrams | Mermaid first; a figure brief when Mermaid cannot express the picture; labels in the manuscript language. |
| 13 | Chart recommendation, with a chart catalogue and scale remedies | Partly | Converted | figure-guide: recommend a form, choose by the statement, fit the data, tables | Three-part answer format added. The catalogue gains the bubble chart, the Pareto front, and aligned panels for different units. Radar charts are limited to a few criteria, and the reason is stated. |
| 14 | Figure caption in English, with case rules and no number | Partly | Converted | editing-guide: captions and table titles; style-presets: caption case | The case rule is a preset. No numbering in the text stays a convention. |
| 15 | Table title in English | Partly | Converted | editing-guide: captions and table titles | Table phrases as examples. Plain verbs preferred. |
| 16 | Results analysis paragraphs | Mostly | Converted | editing-guide: results passages | Analysis dimensions added. The LaTeX paragraph command becomes a lead sentence. Numbers are copied, never invented. |
| 17 | Reviewer's report on the whole paper | Mostly | Converted | manuscript-audit: reviewer-view.md | The numeric rating is dropped. Root causes, consistency checks, a reader check, and an action guide are added. |
| 18 | Architecture image prompt for an external image tool | Not included | Partly | editing-guide: method and overview diagrams (figure brief) | The tool-specific prompt is not included. An external image tool needs the researcher's confirmation first. |
| — | Model recommendations (not a prompt) | Not included | Not included | — | Model-specific and time-sensitive. The workspace is model-neutral. |

Counts: 16 converted, 1 merged into a translation procedure, and 1 partly carried over, which makes 18 prompts. The model recommendations are not a prompt, and they are left out. Before this change, 10 were mostly carried over, 6 partly, and 2 not at all.

### External skills

| External skill, by function | Before | After | Where | Left out, and why |
| --- | --- | --- | --- | --- |
| English AI-style removal skill | Converted (earlier extension) | Converted | natural-prose | Nothing new. |
| Co-writing skill with a reader test | Not included | Converted (reader check) | manuscript-audit: reviewer-view.md | Its stage-by-stage method is already covered by outlining and writing. |
| Conference paper-writing package (LaTeX templates, checklists, citation checks) | Not included | Partly | literature-and-evidence (citation support); submission-readiness with venue notes; figure-guide (tables) | LaTeX templates, booktabs commands, and conference-specific checklists. Venue notes hold such requirements. |
| Word document skill | Not included | Not included | — | The export step and review-response (tracked changes) cover the parts the workspace needs. |
| Design-philosophy poster skill | Not included | Not included | — | Paper figures follow the figure guide. |
| Installation tutorial for a skills tool | Not included | Not included | — | Tool-specific. The workspace has its own skill mechanism. |

## 3. Method and evidence

| Evidence | Result |
| --- | --- |
| `python scripts/sync_skills.py --check` | 34 packages; the Claude Code copies match. |
| `check_capabilities.py`, `check_readmes.py`, `check_requirements.py` | Pass; 105 project directories. |
| Skill descriptions | One line each. `manuscript-writing` 646 characters, `manuscript-audit` 677, `research-code-setup` 626, `natural-prose` 650; the limit is 1024. |
| Overlap with the external texts, 8-word and 10-character runs, every changed file | 0 shared fragments. A 6-word and 8-character run also gives 0. A deliberate copy of 40 words from the same texts gives 33 hits, so the detector works. The texts stay outside the repository. |
| Search for names, addresses, and credits of the external material across the workspace | None in any changed file. |
| Relative links in every changed Markdown file | All resolve. The `assets/name.png` in the manuscript-writing skill is a placeholder in an example, not a link. |
| `python -m unittest discover -s scripts/tests` | 192 tests, OK. |

## 4. Verdicts

| ID | Verdict | Evidence |
| --- | --- | --- |
| WP-1 | Met | Section 2 gives a destination or a reason for each prompt. |
| WP-2 | Met | Each procedure in `editing-guide.md` names what to report (lines 12, 22, 27, 35, 44, 53, 63, 72, 79). The procedures that change text name what must stay (lines 17–18, 33, 40–42, 49–50). |
| WP-3 | Met | The only mentions of LaTeX in the new procedures are prohibitions or explanations (`editing-guide.md` lines 17 and 27). |
| WP-4 | Met | The words "score", "rating", and "acceptance" appear in `reviewer-view.md` only as prohibitions (lines 3 and 36). |
| WP-5 | Met | Lines 18 and 42 of `editing-guide.md` forbid added claims and data; line 57 limits results passages to result records; lines 60–62 forbid selecting favorable numbers and require exact copies. |
| WP-6 | Met | `style-presets.md`, "Rules for presets": a preset applies only when the researcher chooses it, is recorded with `constraint-maintenance`, and changes no manuscript text by itself. The guide points to presets at lines 23, 51, and 71. |
| WP-7 | Met | Name search and overlap check (section 3). |
| WP-8 | Met | `reviewer-view.md` line 19 limits the reader check to clarity, and line 3 says the report predicts no review. |
| WP-9 | Met | Section 3: every check and the 192 script tests pass. |

### Second look at the extended skills

- **`manuscript-writing`.** Step 8 now points to the editing guide and to the presets, and the description adds a method diagram. The requirements of the MVP 5 review still hold: drafting against the outline and the rules (MW-1), the scope rules (steps 1 and 2), the conventions (step 7), and the researcher's own text (step 9) are unchanged.
- **`manuscript-audit`.** Step 12 now points to `reviewer-view.md`. The final check (step 3) and the style check (step 9) are unchanged. The requirement that checks stay separate and that findings name their passages (MA-1) still holds, and the audit does not edit without a request.
- **`research-code-setup`.** `figure-guide.md` gained a recommendation format, a longer chart catalogue, and a section on tables. The requirements of the MVP 4 review still hold: no code without a need, and runs keep their provenance.
- **`natural-prose`.** The word lists were regrouped and extended, and each entry is still a signal. The requirements of the natural-prose review still hold: meaning kept (NP-2), confirmed rules first (NP-3), and no judgment of authorship (NP-4).

## 5. Decisions

- **Procedures, not a copy-paste library.** The prompts became procedures inside the skills, because the workspace routes work through skills. A copy-paste library would skip the confirmation and check rules. A library can still be added later if the maintainer wants one.
- **Style rules are presets, off by default.** A rule such as "no dashes" or "present tense" is the choice of one author, not a requirement of the workspace. It applies only after the researcher's clear yes, recorded with `constraint-maintenance`.
- **LaTeX and Word output rules are replaced.** The workspace manuscript is Markdown with its own citation and label syntax, and the export step builds the Word file. The LaTeX escapes and the plain-text Word output do not apply.
- **No rating.** The reviewer's view gives no score, rating, or chance of acceptance, as the design plan requires for every readiness assessment.
- **Model recommendations and the image-tool prompt are left out.** Model advice is model-specific and goes out of date. The workspace is model-neutral. The image prompt is written for one external tool; its content survives as the figure brief.
- **Later change (2026-10-30).** At the maintainer's instruction, scored reviews and model recommendations became two separate skills, `mock-review` and `model-selection`. The procedures reviewed here still give no score; the reviewer's view now hands a request for scores to `mock-review`, which never gives a chance of acceptance, and model advice is read from each application's current official pages instead of being written into the procedures. See the [mock review and model selection review](mock-review-and-model-selection-review.md).

## 6. Verdict and limits

Verdict: passes. Not covered: how a model applies the procedures and presets, because no live run was made; real manuscripts and real researchers; the Chinese and English procedures were checked by reading and by the edit comparison, not by a researcher's review; the Japanese lists were not changed in this review; Codex; Windows; and the parts of the external skills that are left out.
