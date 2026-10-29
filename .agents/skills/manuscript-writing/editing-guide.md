# Editing Guide

How to carry out particular kinds of edits within `manuscript-writing`. Each part says what may change, what must stay, and what to report. Confirmed rules in `requirements/writing.md` and the venue's output profile take precedence over everything here, and every part keeps the rules of the skill: no invented support, the researcher's own text kept, and the workspace conventions followed.

## Writing from notes or fragments

- Find the main line before writing: the point of each paragraph, and the order the points need (general to specific, cause to effect, or chronological, as the content requires; no fixed template).
- Give each paragraph one point, and join its sentences through their meaning rather than stock connectives.
- Turn a list into prose when its items depend on each other; keep a list of genuinely separate items.
- Raise colloquial wording to the register of the manuscript without adding claims: "the results got much better" becomes the measured change from the result record, or a `[TODO: ...]` marker when there is none.
- Keep technical terms in the form the field uses, including English terms inside a Chinese or Japanese manuscript where the field does so. The terminology table in `requirements/writing.md` decides first.
- Report how the material was arranged (the main line chosen, what was merged or moved), so that the researcher can check the logic.

## Translating into the manuscript language

- Translate the meaning and write natural prose in the manuscript language; avoid the patterns that `natural-prose` lists for that language.
- Never change citation keys, cross-references, labels, math, or image links. Translate the text of a `[TODO: ...]` marker, but keep the marker.
- Use the terminology table first. Keep established abbreviations, and define each at first use when the venue or the manuscript does so.
- Do not improve the argument while translating: add no claim, drop no hedge, and add no emphasis. A passage that is unclear in the source is asked about or marked, never resolved by a guess.
- Run `python scripts/check_edit.py <source> <translation> --translation`.
- When the manuscript language differs from the interaction language, give a literal rendering of the new text in the interaction language, sentence by sentence, after a translation or rewrite of up to about two paragraphs; offer it for longer text. The rendering keeps the sentence order and does not smooth over errors. It is for checking only and never enters the manuscript.

## Translating for reading

When the researcher asks what a manuscript passage says in their language, translate it literally in the reply: keep the sentence order, leave out citation and cross-reference syntax unless asked, render math in words or plain symbols, and neither correct nor improve the text. Point out errors separately. Nothing is written to a file.

## Shortening

- Compress the syntax: a clause into a phrase, a passive into an active form when that is shorter, filler phrases out ("in order to", "it should be noted that"), repetitions merged.
- Keep every parameter, number, condition, qualifier, citation, and result. When a target length cannot be met without losing content, say what would have to go and let the researcher choose.
- Shorten moderately unless asked for more; do not reduce a paragraph to one sentence on your own.
- Report what was cut, and confirm with `check_edit.py` that no protected item was lost.

## Expanding

- Make explicit only what the text or its checked sources already state or directly entail: a premise, a step of reasoning, a consequence, or the relation between two sentences.
- Never add data, sources, examples, or claims, and never pad with adjectives or repetition. A point that would need new evidence becomes a `[TODO: ...]` marker.
- Report each addition with its basis: the sentence or the source it makes explicit.

## Polishing

- Set the depth from the request. A light polish fixes errors (grammar, spelling, articles, agreement, punctuation), unclear references, colloquial wording, and breaks in the logic. A thorough polish may also restructure sentences for flow. A request without a qualifier gets the light polish, plus flow repairs where a sentence reads poorly.
- In both, leave sound sentences unchanged, do not swap synonyms for variety, add no emphasis formatting, and keep the tense convention that the manuscript follows (ask before changing it across sections). Keep established abbreviations and the researcher's terms. Avoid both colloquial and old-fashioned bureaucratic register; in English article prose, avoid contractions unless the venue's style uses them.
- When nothing needs to change, return the text unchanged and say so.
- Report the kinds of changes with a few examples, and run `check_edit.py`.

## Results passages

- Write only from result records in `research/results/`: checked results as findings, observed but unchecked ones as preliminary, each cited as step 6 of the skill requires.
- Lead with the finding, then the numbers that show it, the comparison, and the conditions (data, setting, number of runs).
- Explain comparisons, trends, and trade-offs (against the baseline, across parameters, between the components of an ablation) instead of listing values.
- Say plainly when a difference is small, absent, or inconsistent across runs, and never select favorable numbers.
- Use "significant" only for a statistical test that the record reports, and name the test; otherwise let the numbers speak.
- Copy every number exactly, with its unit and the precision of the record.

## Captions

- Describe directly what the figure or table shows, starting with its content ("Accuracy of the three models across training-set sizes"), not with "This figure shows".
- Make the caption readable on its own: what is plotted or tabulated, under which conditions, what error bars or shading mean, and the number of runs when it matters. Define the abbreviations that appear in the figure.
- The venue's output profile decides capitalization and final punctuation; without one, keep one style across all captions.
- Use the caption syntax of the conventions, and never number a caption by hand.

## Method and overview diagrams

- Draw explanation diagrams as Mermaid blocks under the conventions: one main direction of flow, modules grouped by role, the same shape or color for the same kind of module, short labels (names, not sentences), and arrows for the flow of data or control.
- For an illustration that Mermaid cannot express, write a figure brief for the researcher to draw or to give to an illustrator: its purpose, components, flow, grouping, labels, and color roles, with a muted palette of sufficient contrast, a plain background, and no decorative 3D effects. Generating an image with an external service is not part of this skill; if the researcher considers one, check the venue's policy on generated images first.
- Charts of results follow the [figure guide](../research-code-setup/figure-guide.md).
