# Editing Guide

How to carry out particular kinds of edits within `manuscript-writing`. Each part says what may change, what must stay, and what to report. Confirmed rules in `requirements/writing.md`, the venue's output profile, and any [style preset](style-presets.md) the researcher has chosen take precedence over these defaults. Every part keeps the rules of the skill: no invented support, the researcher's own text kept, and the workspace conventions followed.

For a staged revision, paths under `manuscript/` below mean the selected `revisions/<revision-id>/candidate/` folder, as `manuscript-writing` specifies. Use its candidate check instead of assembling a preview; shared requirements and research results remain workspace records.

## Writing from notes or fragments

- Find the main line before writing: the one point each paragraph makes, and the order the points need. Use general to specific, cause to effect, or time order, whichever the content needs. Do not apply a fixed template.
- Give each paragraph one core point. Join sentences through their meaning, not through stock connectives.
- Turn a list into prose when its items depend on each other. Keep a list only for items that are separate and parallel.
- Replace colloquial wording with the manuscript's register. "The results got much better" becomes the measured change from the result record, or a `[TODO: ...]` marker when no record exists.
- Keep technical names as the field uses them, including English terms inside a Chinese or Japanese manuscript where the field does so. The terminology table in `requirements/writing.md` decides first.
- Report the main line you chose, the order, and what you merged or moved, in a few sentences, so that the researcher can check the logic.

## Translating into the manuscript language

- Translate the meaning, and write natural prose in the manuscript language. Avoid the patterns that `natural-prose` lists for that language.
- Keep the workspace syntax unchanged: citation keys, cross-references, labels, math, and image and link targets. The manuscript is Markdown, so add no LaTeX escapes such as `\%` or `\_`. If an identifier with an underscore reads as emphasis, put it in code formatting.
- Keep every hedge, negation, condition, scope limit, attribution, and completion status that the source has. Do not improve the argument: add no claim, and resolve no unclear passage by guessing. Ask about it, or mark it with `[TODO: ...]`, and keep the marker in the translation.
- Use the terminology table first. Keep established abbreviations, and define them at first use where the venue or the manuscript does so.
- Read the draft once as a strict reviewer would. Look for untranslated fragments, formatting that the manuscript does not use (bold, italics, quotation marks), logic jumps, and claims without support. Fix each one you find.
- Run `python scripts/check_edit.py <source> <translation> --translation`.
- When the manuscript language differs from the interaction language, give a literal rendering of the new text in the interaction language, sentence by sentence. Give it for up to about two paragraphs, and offer it for longer text. The rendering keeps the sentence order and does not smooth over errors. It is for checking only and never enters the manuscript.
- Style choices such as the tense of method sentences, dashes, possessives, or lists apply only when the researcher chooses them as a preset in [style-presets.md](style-presets.md).

## Translating for reading

When the researcher asks what a passage says in their language, give a literal translation in the reply. Keep the sentence order, so that each sentence maps back to the original. Drop citation keys, cross-reference syntax, and labels unless the researcher asks for them. Render math in words or plain symbols, not LaTeX. Ignore formatting commands, but keep the words they mark. Do not correct or improve the text; mark a grammar problem in brackets instead. Write nothing to a file.

## Shortening

- Use the target the researcher gives, such as "about ten percent shorter" or "under 150 words". Without a target, remove only redundancy and wordy syntax, and say how many words you removed.
- Compress the syntax: a clause into a phrase, a passive into an active form when that is shorter, filler phrases out ("in order to" becomes "to"), and repeated points merged.
- Keep every parameter, number, condition, qualifier, hedge, citation, and result.
- Do not reduce a paragraph to a sentence on your own. If the target cannot be met without losing content, name what would have to go, and let the researcher choose.
- Keep a modification log: one line per change, stating what was cut or merged, and why nothing essential was lost.
- Confirm with `check_edit.py`, and check manuscript-wide length with `python scripts/manuscript.py assemble`, or `check --revision-id <revision-id>` for a candidate. Count the requested passage separately when its own length is the target.

## Expanding

- Make explicit only what the text or its checked sources already state or directly entail: an unstated premise, a missing step of reasoning, a consequence, or the relation between two sentences.
- Add a connective only where it names a relation the text already has: cause, contrast, or sequence.
- Never add data, sources, examples, or claims, and never pad with adjectives or repetition. A point that needs new evidence becomes a `[TODO: ...]` marker.
- Use the target length the researcher gives. Without one, make a small expansion.
- Keep a modification log that gives the basis for each addition: the sentence or the source that it makes explicit.

## Polishing

- Set the depth from the request. A light polish fixes errors and clarity. A thorough polish also restructures sentences for flow. Without a qualifier, polish lightly, and repair any sentence that reads badly.
- Change a sentence only for one of these reasons: a grammar, spelling, article, agreement, or punctuation error; an unclear reference; wording that is colloquial for the manuscript; a break in the logic; or a sentence so long that a reader cannot follow it. Leave every other sentence as it is, even when you would write it differently.
- Do not swap synonyms for variety, and add no emphasis formatting. Keep labels, citations, established abbreviations, and the researcher's terms. Keep the tense that the manuscript follows, and ask before changing it across sections.
- Apply the language checklists in [style-presets.md](style-presets.md) only when the researcher has chosen them.
- When nothing needs to change, return the text unchanged, and say so.
- Report the kinds of changes with a few examples, and run `check_edit.py`.

## Results passages

- Write only from result records in `research/results/`. A checked result may be stated as a finding. An observed but unchecked result must be called preliminary. Cite the record as step 6 of the skill requires.
- Structure each paragraph: one sentence that states the finding; then the numbers that show it, with units and conditions; then the comparison and what it means; then the limits that the record states. Use no headings or bold labels inside the paragraph, and separate findings with a blank line.
- Discuss only the analysis dimensions that the record supports: comparison with the strongest baseline under the same settings; sensitivity to a key parameter or seed; the trade-off between performance and cost; the contribution of each component in an ablation; and the spread across runs.
- When a difference is small, absent, or inconsistent across runs, say so. Never select favorable numbers.
- When "significant" asserts statistical significance, use only the test that the record reports, and name it. Qualitative importance and descriptions of the measured magnitude do not automatically assert a statistical test.
- Copy every number exactly, with its unit and the precision of the record.
- Report which result records the passage uses and their status, and which claims wait for a result that does not exist yet.

## Captions and table titles

- Start with what is shown: "Accuracy of three models across training-set sizes". Do not begin with "This figure shows" or "The table presents".
- Make a caption readable on its own: what is plotted or compared, under which conditions, what error bars or shading represent, and the number of runs when it matters. Define the abbreviations that appear in the figure.
- A table title names the comparison or the study, for example "Comparison of the methods on the test set", "Ablation study on the attention module", or "Results on the held-out split". Prefer plain verbs such as show or compare.
- Do not number a caption in the text ("Figure 1:" or "Table 2:"). The label and the numbering come from the conventions.
- Capitalization and final punctuation follow the venue's output profile first. Without one, use the caption style in [style-presets.md](style-presets.md) only if the researcher chooses it; otherwise keep one style across all captions.
- Report the caption style you applied, and any caption that waits for a value the record lacks.

## Method and overview diagrams

- Draw the diagram as a Mermaid block under the conventions by default. Give it one main direction of flow, group modules by role, use the same shape or color for the same kind of module, and use one accent color for the new module. Labels are short names in the manuscript language, not sentences. Arrows show the flow of data or control.
- When Mermaid cannot express the picture, or the researcher wants to draw it elsewhere, write a figure brief. It states the claim the figure supports; names the components; gives the flow, the grouping, and the labels in the manuscript language; assigns color roles (two or three pale tones and one accent); and specifies a plain white background with no shadows, 3D effects, photographs, or sketch lines. Add icons only where the venue allows them. Keep the brief beside the figure's source in `manuscript/assets/`.
- An image from an external generator is outside this skill. Before one is used, the researcher must confirm the tool and what it does with the data, and you must check the venue's policy on generated images. Record the source.
- Report the diagram's source file and where any figure brief is saved.
- Charts of results follow the [figure guide](../research-code-setup/figure-guide.md).
