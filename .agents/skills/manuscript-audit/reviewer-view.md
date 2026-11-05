# Reviewer's View

A critical reading of the manuscript from a reviewer's position, for the researcher to act on before submission. It is not a prediction of any real review. It gives no score, rating, percentile, or chance of acceptance. The same evidence rules as the audit apply: every point names its location and its support.

## Inputs

- The manuscript files that `manuscript/manifest.yaml` lists, and the title and abstract in `manuscript/metadata.yaml`.
- The venue note in `research/venues/` when a target is set: scope, article types, length, required sections, and the AI policy.
- The outline, argument graph and reasoning register, and the source, result, or derivation records that the text relies on. Do not use a stale record as support.

## Checks

Make these checks separately from the audit's checks, and report the result of each one.

1. **Claims and reasoning.** Trace each contribution in the abstract and introduction to its support route. Empirical premises need checked sources/results; an analytical or evaluative contribution needs explicit premises, analysis or inference, conditions, and criteria. Report missing premises, weak inferences, and unsupported observations separately; do not demand a separate citation for an original derived step.
2. **Baselines, where applicable.** Each empirical comparison uses the same data, settings, and versions as far as the record shows. Name any baseline that differs.
3. **Analytical and design choices.** Examine definitions, assumptions, analytical operations, evaluative criteria, and relevant counterexamples or alternatives. For empirical methods, assess whether applicable ablations or sensitivity checks address key design choices; do not impose them on a purely deductive or interpretive argument.
4. **Consistency.** The numbers agree across the abstract, the results, and the conclusion. The conclusion reaches no further than the evidence and reasoning within their stated conditions.
5. **Reader check (optional).** Give only the section text to a reader who has no project context. Use a fresh session or a subagent when one is available. Ask the reader to state, in their own words, the main claim, the method in one paragraph, the main result with its conditions, what they would cite this paper for, and any points that are unclear (up to three; none is a valid answer). Compare the answers with the outline, and make each gap a finding. The reader's answers test clarity. They are not evidence.

## Report

Write the report in English, with these parts:

1. **Summary.** One sentence on what the paper claims and where it sits in its field, taken from the text.
2. **Strengths.** One to three. For each, say why it matters to the field and where its evidence is.
3. **Weaknesses.** In order of severity. For each one, give the passage or setting it concerns, what is missing, overstated, or understated, whether it is a matter of presentation or of substance (method, evidence, or scope), and whether a revision can fix it or it needs new work or a narrower claim. If no weakness is critical, say so plainly.
4. **Root causes.** Why each weakness arose: a gap in the design, or wording that hides a real limit.
5. **Action guide.** The analysis to add, with its dataset and setting named; the passage to rewrite; the limitation to state; and how the response letter should address each point without overclaiming. Use `review-response` when a real review round exists.

## Rules

- Go straight to the judgment. Skip courtesy and praise that carries no information.
- Criticize the claim, not the author. Every point names its location, inspected evidence, and consequence for the claim or likely use. Reject generic criticisms that fit almost any paper. Check whether repeated caveats obscure a supported contribution, and whether empirical, causal, novelty, or impact statements exceed their support. A task outside the promised scope is not a weakness merely because it was not attempted. Read [argument and impact guidance](../manuscript-writing/argument-and-impact.md).
- Separate a critical problem from a minor one. Do not list a style preference as a weakness unless it hurts understanding.
- Give no score, rating, or chance of acceptance in this report. When the researcher asks for scores, use `mock-review`, which scores on the venue's own form and gives no chance of acceptance either.
- Save the report to `outputs/checks/<date>-review-<scope>.md`, and record it with `python scripts/manuscript.py record-check --name "Reviewer's view of <scope>" --kind audit --input <each reviewed section> --input references/bibliography.bib --result findings --summary "..." --report outputs/checks/<file>.md`.
