# Acceptance Records

Acceptance records for each MVP. Since 2026-10-28, a skill passes acceptance when a written review against its requirements passes (maintainer ruling); live scenario runs are not required. The review lists every requirement with its source, a verdict, and the evidence, and it names what it does not cover. On 2026-10-29, the maintainer confirmed this MVP 2-style gate for MVPs 1–9. The complete-path live exercise is optional follow-up, not a gate; the checklists, test evidence and findings remain as history and optional aids.

- [MVP 1 skill review](mvp-1-skill-review.md): the review of `project-onboarding`, `environment-management`, `privacy-configuration`, and `constraint-maintenance`.
- [MVP 1 checklist](mvp-1.md): the scenarios and the results of the 13 live runs (instruction loading, onboarding, environment and credentials, privacy configuration, confirmed rules, and decision confirmation).
- [MVP 2 skill review](mvp-2-skill-review.md): the review of `source-ingestion` and `review-ingestion`, which both pass (2026-10-28).
- [MVP 2 checklist](mvp-2.md): the scenarios for local and cloud import, interruption and retry, the processing choice, Word and unsupported formats, mixed intake, review rounds, and citation metadata, written before the review ruling and not run. [`fixtures/`](fixtures/README.md) generates its synthetic test material.
- [MVP 3 skill review](mvp-3-skill-review.md): MVP 3 was accepted by the maintainer on 2026-10-28 under the MVP 2-style gate; the record covers all four skills, automated and live-service evidence, and remaining platform limits.
- [MVP 3 checklist](mvp-3.md): optional scenarios for search authorization and provider order, evidence locators, literature download/resumption, and source-ingestion handoff. It is not an acceptance gate under the current rule.
- [MVP 4 skill review](mvp-4-skill-review.md): the review of the seven idea, impact, venue, planning, feedback, and research-code skills, and of the result records added to `research-investigation` (2026-10-28).
- [MVP 5 skill review](mvp-5-skill-review.md): the review of the five manuscript skills, with the comparison of open-source converters behind the decision to adopt editable manuscripts with Pandoc (2026-10-29).
- [MVP 6 skill review](mvp-6-skill-review.md): the review of `submission-assembly` and `submission-readiness`, with the live builds and the inspection of Word's rendering (2026-10-29).
- [MVP 7 skill review](mvp-7-skill-review.md): the review of the seven Git skills, with the tests in disposable repositories (2026-10-28).
- [MVP 8 skill review](mvp-8-skill-review.md): the review of `review-response` and the reconciliation of coauthor Word edits (2026-10-29).
- [MVP 9 skill review](mvp-9-skill-review.md): the review of `paper-hands-on`, and the status of the complete-path test (2026-10-29).
- [MVP 9 complete-path live test](mvp-9-complete-path.md): interrupted partial run, observations, and remaining checks.
- [Natural prose skill review](natural-prose-skill-review.md): the review of `natural-prose`, added after the MVPs on 2026-10-29, with a second look at `manuscript-writing`, `manuscript-audit`, `submission-readiness`, `research-code-setup`, and `manuscript-outline`, which it extends.
- [Writing prompts review](writing-prompts-review.md): the conversion of writing prompts into the procedures of `manuscript-writing`, `manuscript-audit`, and `research-code-setup`, with the ledger of each prompt and the second look at the skills it extends (2026-10-29).
- [Literature quality evaluation](sciverse-quality-evaluation.md): candidate multilingual cases and scoring procedure, plus the bounded four-query retrieval smoke run and its remaining source-check gaps.

Never copy this folder into a test workspace: an agent under test could read the expected results. After a review, the agent in the template repository records the result in the [implementation status](../implementation-status.md). Only the template maintainer uses these records; researchers never need them.
