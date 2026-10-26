# Acceptance Checklists

Scenario checklists for verifying each MVP in fresh agent sessions, as the [MVP implementation guideline](../mvp-implementation-guideline.md) requires. Each checklist names its test copies, the exact requests to make, the expected behavior, what to inspect, and a results table.

- [MVP 1](mvp-1.md): instruction loading, onboarding, environment and credentials, privacy configuration, confirmed rules, and decision confirmation.

Never copy this folder into a test workspace: an agent under test could read the expected results. After a run, the agent in the template repository records the results in the [implementation status](../implementation-status.md). Only the template maintainer uses these checklists; researchers never need them.
