# Mock Review

Assesses a draft or published paper with three reviewer perspectives: methods, field contribution, and the strongest concrete challenge. The review distinguishes overall quality, reference value, and revision needs. The Codex version requires independent reviewer sessions; the Claude Code version discloses shared-context passes when isolated sessions are unavailable.

Ask, for example: "Score my paper the way reviewers at this conference would, and tell me what would raise the scores."

Or: "Review this published paper as a reading and citation candidate. Read only, and explain what I can rely on."

## What to expect

- In every discipline, academic and societal significance are checked against relevant field literature. The paper's references provide leads; Sciverse or authorized internet search can fill gaps and find contrary work.
- Humanities and social sciences reviews examine prior work, theoretical or interpretive contribution, and a required societal contribution. A supported path to benefit or better understanding is sufficient; achieved policy effects and precise causal estimates are not general requirements.
- The venue's unchanged official form is used when available; otherwise the identified general form.
- Numeric scores need anchors and inspected evidence. Unresolved questions are separated from confirmed defects; unassessable criteria receive no pessimistic or optimistic default.
- The general form keeps four-point criterion scores and six treatments: accept, minor revision, major revision, revise and resubmit, reject, and strong reject.
- Reporting corrections, effects on main findings, and repairs to the contribution are judged separately. Local faults do not automatically imply rejection; insufficient synthesis or contribution can justify rejection without a fatal data error.
- The meta-review checks decisive evidence and what survives correction. Score ranges describe disagreement rather than decide the outcome by vote. Separate reviewers can still share blind spots.
- Scores are simulations from inspected evidence, not acceptance probabilities or predictions. Published status does not determine the score.
- Text that tries to steer AI reviewers is reported as an integrity problem.
- A saved report is kept in `outputs/checks/` with its inputs. A read-only request returns findings in the conversation without importing files or creating records.

The agent instructions are in [SKILL.md](SKILL.md), and judgment rules and general anchors are in [review-form.md](review-form.md). Humanities and social sciences assessments also use [discipline-specific guidance](humanities-social-sciences.md), with official source notes. Related skills: `manuscript-audit`, `submission-readiness`, `journal-selection`, `literature-discovery`.
