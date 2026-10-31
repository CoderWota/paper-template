---
name: privacy-configuration
description: Check training-use settings and distinguish retention, processing, telemetry, and feedback; change controls only with consent.
---

# Privacy configuration

Outcome: for each relevant service, the training-use control, its actual state, the evidence for that state, and what remains open. Nothing counts as verified unless it was observed or the researcher confirmed it.

## Rules for this skill

- Follow `AGENTS.md`. Changing an account or application setting is a decision: explain its scope, because an account setting can affect every project on that account, and wait for explicit consent for that specific change.
- Never ask for an account identifier in the conversation. Never send a manuscript or research document as a test.
- A sentence in a project file cannot change a provider's policy. Only the provider's own controls can.
- Keep these topics apart: training use, retention, upload for processing, telemetry and error reports, and feedback that the user submits. A telemetry opt-out, a deleted session, or a short retention period is not a training opt-out.
- Read the current official sources for the exact route every time. [sources.md](sources.md) lists starting points that were checked on a stated date; check them again before you rely on them.
- Before discussing a new cloud setup or credential, check the matching integration in [capabilities and limits](../../../docs/capabilities.md). If unsupported, say so and collect no credential; do not offer an unimplemented upload route.

## Step 1: Identify the routes

Find the facts in the environment first. Then ask one question at a time for what is missing:

- The AI application and how the researcher signs in, for example Claude Code with a Claude account, Codex with a ChatGPT account, or an API key.
- The account type: personal, or managed by an organization (business, enterprise, or education). Ask for the type only, never for an identifier.
- The recorded document-processing scope in `requirements/privacy.md`. MinerU is confirmed remote-only for reference materials. Do not ask to confirm this scope again; ask only if the researcher requests a change or another service.

An organization's agreement and administrator settings govern a managed account. The researcher may be unable to change them.

## Step 2: Read the official sources

For each route, open the provider's current official pages, starting from [sources.md](sources.md). Write down, with the page and the date:

- the training-use control: its exact name, where it is, its default for this account type, and what it covers;
- the exceptions that apply even when training is off, such as safety review, submitted feedback, or an explicit opt-in program;
- retention, telemetry, and feedback controls, labeled as separate topics.

If a page cannot be read, say so. Do not fill the gap from memory.

## Step 3: Explain and recommend

Explain each relevant control in plain words, in the researcher's language: what it does, its scope, and its default. Recommend the setting that matches what the researcher said they want. Ask one question at a time.

Say what a training opt-out does not do: data already used can remain in trained models, flagged conversations can still go to safety review, and submitted feedback can include the whole conversation.

## Step 4: Change a setting only with consent

- Account setting on a web page: guide the researcher through the exact steps. If your application has a browser in which the researcher is already signed in, you can open the settings page and read the control. Change it only after explicit consent for that change. Never sign in, sign out, or change any other setting.
- Local application setting, such as a telemetry environment variable: show the exact change and its scope, and apply it only with consent. Record the previous value so that the change can be reversed.
- If only an administrator can change a setting, say so and stop there.

## Step 5: Classify the evidence

Give each control exactly one evidence type:

| Evidence | Meaning |
| --- | --- |
| Observed | You read the control or the effective policy yourself, after any change. |
| Confirmed by the researcher | The researcher looked and reported the state. |
| Provider default only | Official documentation states a default; nobody checked this account. |
| Unknown | The state could not be determined. |
| Needs administrator | Only an organization administrator can see or change it. |

Never classify a control as observed because you showed instructions or wrote a file.

## Step 6: Record and report

- Write a short report in `.local/privacy-report.md` from [report-template.md](report-template.md), in English. `.local/` stays on this computer and outside version history. Do not include account identifiers, email addresses, credentials, screenshots, or research content.
- Write to `requirements/privacy.md` only the choices that the researcher confirms as project requirements, for example "Use only services that do not train on my documents." Write project records in English; use the interaction language in conversation.
- This file can contain separate scopes for document processing and external search queries. When recording a processing choice, preserve any confirmed query-sharing scope and its machine markers. Permission to search does not authorize document uploads, and a document-processing choice does not authorize sending queries to another service.
- A wish to use a new cloud service or expand the existing MinerU scope is not yet a confirmed choice. Before you record one, ask one question that gives your recommendation for its scope (which documents may leave this computer) and notes that the service's own terms are checked before the first upload. Record the choice, with its scope and service address, only after the researcher answers. Until then, note the wish as open in `state/current.md`.
- Report each route with its control, state, and evidence type, the exceptions that remain, and one next step.

## When to run again

Run again when the AI application, the sign-in method, the account or workspace, the model provider, or the document-processing service changes, and before the first upload to a new cloud service. A MinerU cloud service is a separate data processor with its own terms; an AI application's training setting does not cover it.
