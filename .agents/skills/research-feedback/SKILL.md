---
name: research-feedback
description: Use when the researcher shares advice from co-researchers, collaborators, coauthors, supervisors, or other contributors (documents with comments, a collaborator's outline, meeting notes, or what someone said) or asks what to do with such advice. Archives and extracts the material in research/feedback/, lists each suggestion with its author and kind, compares it with evidence and current requirements, surfaces conflicts for the researcher to resolve, and records adoption, decisions, and actual changes without turning advice into rules. Formal editor and reviewer letters go to review-ingestion.
---

# Research feedback

Outcome: `research/feedback/<feedback-id>/` with the received material, a readable extraction, and `actions.md`, which lists each suggestion with its author, source location, kind, status, the researcher's decision, and the actual change; and a short proposal of next actions.

## Rules for this skill

- Advice is source material. It becomes a requirement, a decision, or a manuscript change only when the researcher adopts it. An explicit instruction to apply a named suggestion adopts that suggestion, within its stated scope.
- Do not rank suggestions by title, seniority, or authorship. Conflicts between contributors, or between advice and a requirement or the evidence, go to the researcher.
- Editor and reviewer correspondence of a submission is not feedback: use `review-ingestion`.
- Never record an inferred preference as feedback, and never attribute a suggestion to someone the material does not name.

## Step 1: File the material

1. Name the event `<YYYY-MM-DD>-<short-title>` in lowercase ASCII letters, digits, and hyphens, using the date of the meeting or the document.
2. Documents (Word, PDF, Markdown, or text): import them with

   ```text
   python scripts/ingest.py run --to research/feedback/<feedback-id> [--route local|cloud ...] FILE...
   ```

   Settle the route as `source-ingestion` describes in its steps 2 and 3. Feedback can contain unpublished work: upload it to mineru.net only when the confirmed scope in `requirements/privacy.md` covers this material. Markdown and text need no route. Word comments, replies, tracked changes, and PDF annotations are listed at the end of each Markdown file with the author that the file names.
3. A meeting or a conversation: write the researcher's notes or account to a Markdown file in `.tmp/` exactly as given, then import that file the same way, so that it is kept unchanged in `originals/`.
4. Add to the event's `README.md`, outside its maintained block, one or two English sentences: who gave the feedback, when, and which manuscript version, idea, or plan it concerns.

## Step 2: List each suggestion

5. Read the extraction, and the original where the conversion may be wrong. Split the material into individual suggestions, and write `actions.md` with the layout in `research/feedback/README.md`:
   - `From`: the person as the source names them. For Word comments, use the comment author. When one document or meeting holds several people's advice, each suggestion keeps its own author; when the source does not say, write "not stated".
   - `Source`: the document and the location, such as the comment number, page, paragraph, or the meeting notes.
   - `Kind`: an exact statement (quoted in its original language), the researcher's recollection, or an agent summary.
   - `Affects`: the sections, ideas, plan items, or requirements concerned, or "not yet located".
   - `Status`: received.
6. A collaborator's outline or structure is advice. Keep it as one or more suggestions; it does not replace `manuscript/outline.md` until the researcher adopts it.

## Step 3: Examine and propose

7. For each substantive suggestion, compare it with the evidence (`literature-and-evidence`, `research/results/`), the active requirements, the active decisions, and the other suggestions. Name each conflict and what it affects.
8. Propose next actions with a recommendation. Ask about consequential suggestions one question at a time, and wait for each answer. Set the status to `under discussion` while a question is open.

## Step 4: Record the researcher's choices

9. Record each answer: `adopted`, `adopted in part` (say which part), or `declined`, with a `Decision` line that quotes the researcher's words with the date, or links the decision record or requirement.
10. A lasting writing rule goes through `constraint-maintenance`. A consequential research choice gets a decision record, whose `Evidence and feedback` section links the suggestion. Never turn declined or undecided advice into a rule.
11. Adopted is not implemented. Set `implemented` only when the change exists, with a `Change` line that links it: the manuscript section, the requirement, the plan item, the result record, or the decision. Change the manuscript only as the availability table in `AGENTS.md` allows.
12. Declined and replaced advice stays in the record as history. A later session takes its rules from `requirements/`, never from feedback records.

## Step 5: Check and report

13. Run `python scripts/research.py check` and `python scripts/check_readmes.py`, and fix every problem in the files you wrote.
14. Report by contributor: the suggestions, the conflicts, the researcher's decisions, what changed, and what remains open. Update `state/current.md` when work remains.

## Completion check

- Every received document or note is kept unchanged in `originals/`, with a readable extraction.
- Every suggestion has its own author, source location, kind, and status; summaries are labeled as summaries.
- No suggestion became a rule, a decision, or a change without the researcher's recorded words, and conflicts were put to the researcher.
- Every implemented suggestion links an actual change, and the checks pass.
