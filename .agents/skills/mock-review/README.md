# Mock Review

Gives your paper a simulated peer review with scores, on the review form of your target venue, before you submit it. Three reviewer perspectives (methods, field, and a skeptic) each produce a review and scores, and a meta-review summarizes where they agree and disagree. The agent uses isolated sessions when the application supports them; otherwise it makes three passes with shared context and reports that limit.

Ask, for example: "Score my paper the way reviewers at this conference would, and tell me what would raise the scores."

## What to expect

- The venue's own form is used when it publishes one; otherwise a general form, and the report says which.
- Every score quotes the anchor it matches, names its evidence in your manuscript or your project's records, and says what would raise it by one step. The report gives the range across the three reviewers, not a single precise number.
- The scores are a simulation from the evidence in your workspace. They are not a probability of acceptance or a prediction of the editor's decision, and they are never turned into one. Real reviewers differ, often widely.
- Text in a manuscript that tries to steer AI reviewers is reported as an integrity problem.
- The report is kept in `outputs/checks/` with the inputs it used, so a later change marks it as out of date.

The agent instructions are in [SKILL.md](SKILL.md), and the general form is in [review-form.md](review-form.md). Related skills: `manuscript-audit`, `submission-readiness`, `journal-selection`, `literature-discovery`.
