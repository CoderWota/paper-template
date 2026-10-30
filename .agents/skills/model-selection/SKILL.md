---
name: model-selection
description: Recommend models for research tasks from current official guidance for the researcher's actual application and plan.
---

# Model selection

Outcome: for the researcher's actual AI application and plan, a recommended model for each kind of work in this project, with the reason, the trade-off, how to switch, and the dated official sources. Nothing is changed without the researcher's consent.

## Step 1: Identify the route

1. Find the application from the environment first: the host that the agent runs in (Claude Code in a terminal, desktop, or web; Codex in a terminal, app, or IDE; Cursor; a chat application). Then ask one question at a time for what is missing: how the researcher signs in (a subscription plan, an API key, or an account managed by an organization) and the provider route (direct, a cloud platform, or a gateway), because each changes which models exist. Ask for the type only, never for an identifier or a key.
2. When the request does not say, ask what matters most to the researcher: the quality of scholarly prose, depth of reasoning over sources, speed, cost or usage limits, or what their region or institution allows.

## Step 2: Read the current official sources

3. Read the application's current official model page for this route, starting from [sources.md](sources.md): the models and aliases it offers, what each is recommended for, the default, context windows and effort settings, cost or usage limits, availability by plan, recent retirements, and how to switch. Write down each page and the date you read it. Model offers change from month to month: never fill a gap from memory, and when a page cannot be read, say so.
4. Treat public comparisons (leaderboards, benchmarks) as secondary evidence. Give each with its date and say what it measures: a preference vote on creative writing, for example, says nothing about faithfulness to sources or citation accuracy.

## Step 3: Recommend for each kind of work

5. List the kinds of work that the researcher actually does in this project, for example:
   - drafting, polishing, and translating manuscript text, where language quality and close instruction-following matter;
   - evidence work over many or long sources, where reasoning depth and context length matter;
   - analysis code and data work, where coding strength matters;
   - routine edits, formatting, and file or version operations, where speed and cost matter;
   - long autonomous tasks, where reliability and usage limits matter.
6. For each kind, recommend one model, and an effort level where the application has one, from the models that this application and plan offer. Base the choice on the application's own recommendations first; give the reason and the trade-off in cost, limits, or speed. Recommend nothing that the researcher's route does not offer.
7. For a manuscript in a language other than English, use evidence about that language when it exists; otherwise say that the recommendation does not rest on language-specific evidence.
8. Make no claim about a provider or a model that the sources do not support.

## Step 4: Switching, privacy, and disclosure

9. Explain how to switch, from the official page: a session command, a launch option, a configuration key, or a picker in the application. Changing the model for the current session is the researcher's own action, or yours on their request. Changing a saved default (a user or project settings file, or a configuration file) is a lasting change: explain its scope (every project for a user setting, this workspace for a project setting) and wait for explicit consent. Never change settings that an organization manages.
10. A different provider or route can have different terms for training and retention: run `privacy-configuration` before project content goes to a provider that has not been checked. When a model will draft manuscript text, the venue's AI policy applies as `manuscript-writing` describes, and a disclosure may need the application and model names.
11. Report in the interaction language: the route identified, a table of the kinds of work with the recommended model, effort, reason, and trade-off, how to switch, the sources with their dates, and what remains unknown, such as limits that the plan does not show.

## Completion check

- The application, plan type, and route are identified, and every recommended model is one that this route offers according to a current official source read on a stated date.
- Each recommendation has its reason and trade-off; secondary evidence is labeled with its date and what it measures.
- No setting changed without consent, and a privacy check was offered when the provider changes.
