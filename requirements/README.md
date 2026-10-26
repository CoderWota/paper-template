# Requirements

The researcher's confirmed requirements: what currently governs work on this project. Agents read the relevant files here before working, and nothing becomes a requirement unless you have confirmed it.

## Contents

| File or folder | Holds |
| --- | --- |
| [`project.md`](project.md) | Purpose, intended contribution, audience, article type, and languages. |
| [`writing.md`](writing.md) | Active writing rules and terminology, each with its scope. |
| [`privacy.md`](privacy.md) | Confirmed document-processing choices and data-use requirements. |
| [`profiles/`](profiles/README.md) | Output profiles: journal or thesis requirements and their format resources. |

## The confirmation rule

- Only verified rules that you have confirmed are recorded here. A clear instruction from you counts as confirmation; you will not be asked to approve it again.
- Preferences the agent infers from your edits are discussed with you first. They are never saved here, or anywhere else, as candidates.
- Each rule has a scope: the whole project, one section, or one output profile. One-time edit requests are not saved as lasting rules.
- When a new rule conflicts with an existing one, the agent asks you to resolve the conflict. Only active rules stay here: a replaced rule is removed, and an important change also gets a decision record in [`research/decisions/`](../research/decisions/README.md).
- Anything undecided, such as the research direction or the target venue, stays open rather than guessed.

The requirement files are written in your interaction language; this README stays in English.

## Processing and credentials

Until a processing choice is confirmed in `privacy.md`, no document is uploaded to a parsing service, and a failed local conversion is never retried in the cloud or with another parser. A cloud-based AI agent also receives the files it reads; that route is governed by the AI application's own settings, which are checked separately.

Credentials never go in these files or anywhere else in version history. They are stored only in ignored local files on this computer, and privacy verification reports stay local too.

Why a requirement was chosen is recorded in [`research/decisions/`](../research/decisions/README.md) when that is useful. Advice you have not adopted stays in [`research/feedback/`](../research/feedback/README.md).

## Who edits what

You can state or change a requirement in ordinary language at any time, for example: "From now on, use British spelling in the manuscript." The agent records it in the right file with the right scope. You do not need to edit these files, although you may.

Related skills: `project-onboarding`, `constraint-maintenance`, `privacy-configuration`.
