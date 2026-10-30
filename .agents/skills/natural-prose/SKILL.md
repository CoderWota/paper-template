---
name: natural-prose
description: Check or revise formulaic, inflated, or translated prose while preserving claims, evidence, uncertainty, and author voice.
---

# Natural prose

Outcome: the requested text revised so that it reads like careful human writing in its language and register, with the same claims, evidence, and limits as before; or, for a check, the patterns found with their locations. A short report says what was found, what changed, what was kept and why, and what the researcher must supply.

## Step 1: Settle the text and the task

1. Identify the text: a passage or section of the manuscript, a response in a review round, or text given in the conversation, such as a cover letter or an abstract for a form. Identify the task: check only, or revise. A check never edits.
2. A request about named text is a one-time edit. A lasting instruction ("never use dashes in the manuscript") is a rule: record it with `constraint-maintenance` first. A pattern found here becomes a rule only with that confirmation.
3. Read `requirements/project.md` (manuscript and interaction languages), the rules in `requirements/writing.md` whose scope covers the text, and, for the manuscript, the venue note when its language or AI policy matters. Confirmed rules and venue requirements take precedence over every pattern: a construction that a rule requires stays.
4. Base the voice on the researcher's own writing: passages they wrote or edited, or a sample they give. Follow its habits (how long its sentences run, which words it prefers, how it punctuates), including habits that a pattern list would flag. Without a sample, keep the register of the text type: formal and impersonal for an article, courteous and direct for a letter. Never add opinions, experiences, anecdotes, humor, or rhetorical questions to make scholarly text sound personal.

## Step 2: Mark the patterns

5. Read [the pattern families](patterns.md) and the list for the text's language: [English](patterns-en.md), [Chinese](patterns-zh.md), or [Japanese](patterns-ja.md). For another language, apply the families with that language's own norms, and tell the researcher that no tailored list exists.
6. Go through the entire text before changing anything. Mark each pattern with its family and strength, at the level where it occurs: a phrase, a sentence, a paragraph, or the same move repeated across sections. A strong pattern warrants attention on its own; revise only when the edit preserves meaning. A substantive claim problem is flagged for the researcher. Act on a weak pattern only when several cluster or repeat. Persuasive contribution language, emphatic evaluation, and ambitious outlook are allowed; intensity alone is no reason to cut or mark a claim as unsupported.
7. Patterns are editing signals. Never state or imply that a passage was or was not written by AI, never estimate a detector's score, and never promise that the result will pass a detector.

## Step 3: Revise

Skip this step for a check.

8. Change only what a marked pattern or a real clarity problem needs. Leave sound sentences as they are, and say so when the text needs no change.
9. Keep the content exactly: every claim and its strength, numbers and units, citation keys, cross-references, labels, math, `[TODO: ...]` markers, hedges, negations, conditions, scope, comparisons, tense and completion status ("is testing" is not "tested"), and attribution ("Smith argues" is not a fact). Never add a fact, a number, a source, an example, a reason, or a claim. When a vague phrase hides a relationship that the text does not state, keep it vague or ask; never guess it.
10. A pattern that hides a missing source, such as "studies show" without a citation, is a support gap. In the manuscript, keep the claim with a `[TODO: ...]` marker that names the evidence needed, as `manuscript-writing` does; never supply a citation from memory.
11. Reread the revision for patterns that tend to outlast a first pass (contrasts with a view nobody holds, closers that restate, lists of three, dashes, connectives that open every sentence) and for patterns that the revision itself introduced. When phrase-by-phrase fixes leave a paragraph stiff, rebuild the paragraph from its central claim.
12. Before revising several sections at once, offer to save a version first (`git-save`).

## Step 4: Check the edit

13. Before writing a revised file, copy the original to `.tmp/edits/`; for a long text from the conversation, save both versions there.
14. Apply manuscript text as `manuscript-writing` applies an edit: within the requested scope, keeping the researcher's own edits, then `python scripts/manuscript.py check`. After a response in a review round, run `python scripts/review.py check --round <round folder>`. Return text from the conversation in the reply.
15. Run `python scripts/check_edit.py <original> <revised>` and account for every difference it reports: restore what was lost, or tell the researcher why a difference is intended. Its warnings about hedges and negations need a reading, not an automatic fix.

## Step 5: Report

16. Report in the interaction language: the patterns found, grouped by family, with short quotations; what changed and where; what was kept and why (a confirmed rule, the researcher's voice, a deliberate choice); and any information the researcher must supply. When the text is in another language than the interaction language, add a literal rendering of the changed sentences in the interaction language so that the researcher can check the meaning.
17. Revising wording does not change what a venue requires authors to disclose about AI assistance; that follows the researcher's decision and the venue's policy.
18. When a pattern recurs and the researcher wants it avoided from now on, offer to record it as a rule with `constraint-maintenance`.

## Completion check

- The task (check or revise) and the scope of the text are stated, and confirmed rules took precedence over the pattern lists.
- Every claim, number, citation, cross-reference, hedge, condition, and attribution of the original is still present, and nothing was added; every difference that `check_edit.py` reported is accounted for.
- Sound text was left unchanged, and the researcher's voice was kept.
- No statement about who wrote the text and no promise about AI detectors was made.
- No rule was recorded without the researcher's confirmation.
