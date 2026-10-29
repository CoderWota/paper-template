# General Review Form

The form that `mock-review` uses when no venue is set, or when the venue publishes no reviewer form. The report must say that it used this form. When the venue has its own form, use that form instead, with its own fields, scales, and anchor wording.

## Written fields

1. **Summary.** What the paper claims to contribute, in the reviewer's own words, without judgment.
2. **Strengths.** The reasons to publish, each with its evidence.
3. **Weaknesses.** Numbered, most serious first. Each names its location, what is missing or overstated, whether it is a matter of presentation or of substance, and whether a revision can fix it.
4. **Questions.** What the authors could answer to change a score, and which score it would change.
5. **Limitations and ethics.** Whether the paper states its limits and possible harms adequately, and what is missing.

## Criterion scores (1 to 4)

| Score | Soundness | Clarity | Significance | Originality |
| --- | --- | --- | --- | --- |
| 4 | Every main claim rests on adequate evidence and correct methods. | An expert can follow every step and could repeat the work from the paper. | Others in the field are likely to use or build on the result. | A clear advance over the closest prior work, which the paper identifies. |
| 3 | The main claims are supported; minor points lack detail. | Readable; some details must be inferred. | Useful to part of the field. | A real difference from prior work, though the difference is incremental. |
| 2 | At least one main claim is not adequately supported, or the method has a problem. | Important parts are hard to follow or missing. | The gain is small or narrow. | The difference from prior work is unclear or small. |
| 1 | The central claims are unsupported, or the method is flawed. | The paper cannot be followed. | No clear use for others. | Known results, or no comparison with the prior work. |

**Reproducibility (1 to 4).** 4: the paper and its materials allow a full repeat. 3: a repeat is possible with some effort or variation. 2: important settings or data are missing. 1: a repeat is not possible.

## Overall recommendation (1 to 6)

| Score | Meaning |
| --- | --- |
| 6 | Strong accept: sound throughout, with an important contribution. |
| 5 | Accept: sound, with a clear contribution to its area. |
| 4 | Leaning to accept: the reasons to accept outweigh the weaknesses. |
| 3 | Leaning to reject: the weaknesses, such as a limited evaluation, outweigh the reasons to accept. |
| 2 | Reject: substantive problems that need new work. |
| 1 | Strong reject: fundamental flaws, known results, or outside the scope. |

Use 4 and 3 only when the evidence is genuinely balanced.

## Confidence (1 to 5)

| Score | Meaning |
| --- | --- |
| 5 | Every relevant detail was checked, and the related work is well known to the reviewer. |
| 4 | The main points were checked; a missed detail is unlikely. |
| 3 | The area is familiar, but details such as proofs or the experimental design were not checked. |
| 2 | Central parts or related work may have been missed. |
| 1 | The assessment is a guess. |

## Recording a venue's form

When a venue publishes its own form, add it to the `Review form` field of the venue note in `research/venues/` before scoring, with the reviewer guidelines listed under `Sources`: the date it was read, each written field, and each scale with every anchor in the venue's wording. A later mock review reuses the recorded form until the venue publishes a new one.
