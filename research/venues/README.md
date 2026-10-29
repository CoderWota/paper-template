# Venue Assessments

Notes on journals or other venues that were examined for this paper: what their current official sources say about scope, article types, length and structure, AI use, data and reporting policies, costs, and review, and how well the paper fits. Fit is assessed separately from the paper's impact and from submission readiness.

## Contents

- [`index.md`](index.md): the comparison of the examined venues and the current recommendation.
- One note per examined venue, for example `journal-of-urban-studies.md` (lowercase ASCII letters, digits, and hyphens).

## Note layout

The values are in your interaction language; the `Checked` and `Sources` labels stay as shown, because `python scripts/research.py check` reads them.

```text
# <Venue name>

- Checked: <YYYY-MM-DD, the date the official sources were read>
- Sources:
  - <official address> (<what it covers, such as the author guidelines>)
- Scope: ...
- Article types: ...
- Requirements: <length, structure, abstract, references, figures, data and code>
- AI policy: <what the venue permits or requires, with its address>
- Costs and access: ...
- Review and timeline: <only what the venue states officially>
- Review form: <read on YYYY-MM-DD from the reviewer guidelines listed under Sources: each written field, and each scale with every anchor in the venue's wording; only when the venue publishes one>
- Publications inspected: <recent relevant articles, or none>
- Fit: <reasons tied to the paper and the sources>
- Conditions: <what would have to change, and open questions>
```

## Rules

- Every fact comes from a dated official source or an inspected publication. Knowledge that was not checked against a current source is labeled as unchecked.
- No acceptance probability is estimated. A published acceptance rate is the venue's statistic, not this paper's chance.
- Choosing the target venue is your decision. Once you confirm it, the target goes in [`requirements/project.md`](../../requirements/project.md) with a decision record, and the formatting requirements become an output profile in [`requirements/profiles/`](../../requirements/profiles/README.md).

## Who edits what

The agent reads the official sources, writes these notes, and keeps the comparison current. Example requests: "Compare these three journals for my paper." "Check whether this journal accepts AI-assisted writing."

Related skill: `journal-selection`.
