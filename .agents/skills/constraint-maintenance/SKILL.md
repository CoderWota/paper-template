---
name: constraint-maintenance
description: Record or replace confirmed project and writing rules; resolve conflicts and distinguish lasting requirements from one-time edits.
---

# Constraint maintenance

Outcome: `requirements/` states exactly the rules that the researcher confirmed, each with its scope, so that any agent in any later session applies the same rules.

## Rules for this skill

- Follow the research-choice and record rules in `AGENTS.md`.
- An explicit, clear instruction is confirmation. Record it without asking for approval again.
- Never save an inferred preference. This applies to `requirements/`, notes, `state/`, skills, feedback records, idea notes, and the agent application's own memory feature. If you notice a pattern, you can ask about it once in the conversation; without a clear yes, keep nothing.
- Keep only active rules in `requirements/`. Remove a rule when it is replaced or withdrawn.
- A consequential research choice also gets a decision record, whether or not it replaces a rule. Follow the research-choice and record rules in `AGENTS.md`. Write the record and its index entry in English with the layout in `research/decisions/README.md`, name the old and the new choice, and state the reason as the researcher gave it, or say that none was given. When the new decision replaces an earlier one, link both records to each other and mark the earlier one as replaced; never delete a record. Run `python scripts/research.py check` afterwards.
- Write rules in English. Capture the researcher's confirmed intent faithfully. Quote an English rendering of their instruction; do not add a translation label or claim that a translation is verbatim. Add an example or an exception only when the researcher gave it or confirms it; never add one that you inferred. Avoid broad bans on words, which damage meaning and natural expression.
- A rule governs writing and behavior. It is not evidence for a scientific claim, and an idea or a hypothesis is not a rule.

## Step 1: Decide whether the statement is a lasting rule

| The researcher says | Treat it as | Action |
| --- | --- | --- |
| "From now on, ...", "Always ...", "Never ...", "In this paper, ..." | A lasting rule | Record it (steps 2 to 4). |
| "Shorten this paragraph", "Change this word here" | A one-time edit | Make the edit. Record nothing. If it conflicts with an active rule, follow step 3. |
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

Language settings belong in `requirements/project.md`: the manuscript language, the interaction language, and explicit exceptions, such as quotations, proper names, bibliography titles, or a required abstract in a second language. Spelling variety (for example British or American English) and style are writing rules, so they belong in `requirements/writing.md`.

## Step 3: Check for duplicates and conflicts

Read the active rules in the target file before you write.

- The same rule is already recorded: do not add it again. Update its scope or examples if the researcher changed them.
- The new rule conflicts with an active rule: show both rules and ask one question. The choices are to replace the old rule, to limit one rule to a narrower scope, or to keep the old rule. Recommend one choice. If the researcher's words already say to replace or switch to the new rule (for example "改用…" or "switch to …"), that is the replacement: record it and name the rule that it replaces, without a question. Ask only when the words leave the relation open.
- A current request conflicts with an active rule. If it names one passage or sentence ("这一句", "this sentence"), it is a one-time edit: make the edit, say that no rule changed, and offer to change the rule if the researcher wants. Otherwise, say so before you act, and ask whether this is a one-time exception or a change of the rule. A one-time exception changes no file.

## Step 4: Write the rule

Use this suggested layout in `requirements/writing.md`. Write the values in English. The label examples help the agent find rules, but no script checks their wording or format:

```text
## <short name>

- Rule: <what to do, in the researcher's words where possible>
- Scope: <whole manuscript | section: <name> | output profile: <id>>
- Examples: <only if the researcher gave them>
- Exceptions: <only if the researcher gave or confirmed them>
- Confirmed: <date>; <an English rendering of the researcher's confirming words in quotation marks, or the adopted feedback or decision record>
```

Leave out the `Examples` and `Exceptions` lines unless the researcher gave or confirmed them. If an exception seems necessary, ask one question; do not write it first.

After you write a rule, read it back against the confirmed scope and wording. The workspace has no automatic form checker for requirements. `python scripts/research.py check` can report broken links in related decision records; review those facts and repair an actual broken link when appropriate.

When there are several terms, keep terminology in a table with the preferred term, the terms to avoid, and the scope. Keep any text that the researcher wrote in the file.

## Step 5: Replace or remove a rule

- Remove the old rule from the file. `requirements/` never keeps replaced rules.
- In the "Confirmed" line of the new rule, name the rule that it replaces.
- If the change also has a decision record, link it from the new rule. A writing rule or a language setting has none.

## Step 6: Check what the change affects

A confirmed change authorizes the change and its records. It does not authorize edits to manuscript text. Search `manuscript/` for passages that the change affects, such as an introduction that states the old research goal. List them in your report and ask one question about what to do with them. Edit those passages only when the researcher authorizes that scope; reuse an explicit instruction that already covers it. If support for an action is uncertain, consult [capabilities and limits](../../../docs/capabilities.md) before offering it.

## Step 7: Report

Tell the researcher, in their language, what you recorded, changed, or removed, with its scope and a link to the file, and list the manuscript passages that the change affects. When the researcher asks which rules apply, list the active rules by scope.

## Completion check

- Every rule in `requirements/` came from an explicit instruction or a confirmed answer, and has a scope and a date.
- No inferred preference appears in any file or in the agent application's memory.
- No two active rules contradict each other.
- A replaced rule is gone from `requirements/`, and a consequential change has a decision record in English. Consider any broken links reported by `python scripts/research.py check`; the command does not assess the record's form or meaning.
- Every example and exception in `requirements/` came from the researcher.
- No manuscript text was edited without the researcher's answer.
