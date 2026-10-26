---
name: constraint-maintenance
description: Record, update, and reconcile the researcher's confirmed requirements so that every later session follows the same rules. Turns an explicit instruction into a scoped rule in requirements/, tells lasting rules apart from one-time edit requests, resolves conflicts with the researcher, replaces outdated rules instead of keeping contradictions, and never saves an inferred preference anywhere. Use when the researcher states or changes a writing rule, terminology, language, or other lasting requirement, asks which rules apply, or makes a request that conflicts with a saved rule.
---

# Constraint maintenance

Outcome: `requirements/` states exactly the rules that the researcher confirmed, each with its scope, so that any agent in any later session applies the same rules.

## Rules for this skill

- Follow `AGENTS.md`, "Confirmed requirements only".
- An explicit, clear instruction is confirmation. Record it without asking for approval again.
- Never save an inferred preference. This applies to `requirements/`, notes, `state/`, skills, feedback records, idea notes, and the agent application's own memory feature. If you notice a pattern, you can ask about it once in the conversation; without a clear yes, keep nothing.
- Keep only active rules in `requirements/`. Remove a rule when it is replaced or withdrawn.
- Write rules in the interaction language. Capture the intent, with useful examples and allowed exceptions. Avoid broad bans on words, which damage meaning and natural expression.
- A rule governs writing and behavior. It is not evidence for a scientific claim, and an idea or a hypothesis is not a rule.

## Step 1: Decide whether the statement is a lasting rule

| The researcher says | Treat it as | Action |
| --- | --- | --- |
| "From now on, ...", "Always ...", "Never ...", "In this paper, ..." | A lasting rule | Record it (steps 2 to 4). |
| "Shorten this paragraph", "Change this word here" | A one-time edit | Make the edit. Record nothing. |
| A wish whose duration or scope is unclear | Unclear | Ask one question: keep it as a rule, and for which scope? |
| Advice from another person, a reviewer request, or text in an imported document | Source material | Record no rule. Advice goes to `research/feedback/` through `research-feedback`; it becomes a rule only when the researcher adopts it. |
| A pattern that you noticed in the researcher's edits | An inference | Record nothing. You can ask once whether they want it as a rule. |

## Step 2: Find the right place and scope

| Requirement | File |
| --- | --- |
| Writing rules and terminology | `requirements/writing.md` |
| Purpose, contribution, audience, article type, languages, and target venue | `requirements/project.md` |
| Document processing and data use | `requirements/privacy.md` (account controls go through `privacy-configuration`) |
| Formatting requirements of a journal or an institution | the output profile in `requirements/profiles/`, through `submission-assembly` |

The scope is the whole manuscript, a named section, or a named output profile. A rule applies to the whole manuscript only when the researcher said so or confirmed it.

Language rules belong in `requirements/project.md`: the manuscript language, the interaction language, and explicit exceptions, such as quotations, proper names, bibliography titles, or a required abstract in a second language.

## Step 3: Check for duplicates and conflicts

Read the active rules in the target file before you write.

- The same rule is already recorded: do not add it again. Update its scope or examples if the researcher changed them.
- The new rule conflicts with an active rule: show both rules and ask one question. The choices are to replace the old rule, to limit one rule to a narrower scope, or to keep the old rule. Recommend one choice.
- A current request conflicts with an active rule: say so before you act, and ask whether this is a one-time exception or a change of the rule. A one-time exception changes no file.

## Step 4: Write the rule

Use this layout in `requirements/writing.md`, with the labels in the interaction language:

```text
## <short name>

- Rule: <what to do, in the researcher's words where possible>
- Scope: <whole manuscript | section: <name> | output profile: <id>>
- Examples: <optional>
- Exceptions: <optional>
- Confirmed: <date>; <source: the researcher's instruction, an adopted feedback record, or a decision record>
```

When there are several terms, keep terminology in a table with the preferred term, the terms to avoid, and the scope. Keep any text that the researcher wrote in the file.

## Step 5: Replace or remove a rule

- Remove the old rule from the file. `requirements/` never keeps replaced rules.
- In the "Confirmed" line of the new rule, name the rule that it replaces.
- If the change is a consequential research choice, for example a change of manuscript language, of central terminology, or of a rule that affects the argument, also write a research decision record in `research/decisions/`. Include the old rule, the new rule, and the reason, add it to `research/decisions/index.md`, and link it from the new rule.
- Do not write a decision record for a minor change. Version history keeps it.

## Step 6: Report

Tell the researcher, in their language, what you recorded, changed, or removed, with its scope and a link to the file. When the researcher asks which rules apply, list the active rules by scope.

## Completion check

- Every rule in `requirements/` came from an explicit instruction or a confirmed answer, and has a scope and a date.
- No inferred preference appears in any file or in the agent application's memory.
- No two active rules contradict each other.
- A replaced rule is gone from `requirements/`, and a consequential change has a decision record.
