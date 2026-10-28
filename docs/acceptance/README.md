# Acceptance Checklists

Scenario checklists for verifying each MVP in fresh agent sessions, as the [MVP implementation guideline](../mvp-implementation-guideline.md) requires. Each checklist names its test copies, the exact requests to make, the expected behavior, what to inspect, and a results table.

- [MVP 1](mvp-1.md): instruction loading, onboarding, environment and credentials, privacy configuration, confirmed rules, and decision confirmation.
- [MVP 2 skill review](mvp-2-skill-review.md): the review of `source-ingestion` and `review-ingestion`, which both pass (2026-10-28).
- [MVP 2 checklist](mvp-2.md): the scenarios for local and cloud import, interruption and retry, the processing choice, Word and unsupported formats, mixed intake, review rounds, and citation metadata, written before the review ruling and not run. [`fixtures/`](fixtures/README.md) generates its synthetic test material.

Never copy this folder into a test workspace: an agent under test could read the expected results. After a run, the agent in the template repository records the results in the [implementation status](../implementation-status.md). Only the template maintainer uses these checklists; researchers never need them.
