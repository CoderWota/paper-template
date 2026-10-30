# Research Feedback

Attributed advice about the research or the manuscript from co-researchers, collaborators, coauthors, supervisors, or anyone else whose input you want to keep, regardless of title or authorship. One subdirectory per feedback event, such as a received document or a meeting: `<feedback-id>/`, named `<YYYY-MM-DD>-<short-title>` in lowercase ASCII letters, digits, and hyphens.

## Each feedback directory contains

```text
<feedback-id>/
├── README.md        # What the event is and its documents, with who gave the feedback and when
├── originals/       # Received documents or your meeting notes, kept unchanged
├── extracted/
│   ├── markdown/    # Readable Markdown of the received documents, with Word comments and their authors
│   ├── assets/      # Images and other files referenced by the Markdown
│   └── provenance.json
└── actions.md       # Each suggestion with its source, your decision, and actual progress
```

`python scripts/ingest.py run ... --to research/feedback/<feedback-id> FILES` creates the folders with their READMEs, using the document-processing choice confirmed in [`requirements/privacy.md`](../../requirements/privacy.md). Markdown and text files, such as meeting notes, are read directly.

## Layout of actions.md

One section per suggestion is a suggested layout. `python scripts/research.py check` follows recognized status and `Change` fields to check links for suggestions marked implemented. Other or unfamiliar labels and status words are not rejected. Chinese equivalents such as `原话`, `研究者回忆`, `智能体摘要`, `已收到`, `讨论中`, `已采纳`, `部分采纳`, `未采纳`, and `已实施` are also understood.

```text
## F1 <short title>

- From: <the person as named in the source, or "not stated">
- Source: <document and location, such as comment 3 or page 2, or the meeting notes>
- Kind: exact statement | researcher recollection | agent summary
- Suggestion: <quoted in its original language, or a labeled summary>
- Affects: <sections, ideas, plan items, or requirements>
- Status: received | under discussion | adopted | adopted in part | declined | implemented
- Decision: <date; your words in quotation marks, or a link to the decision record or requirement>
- Change: <a link to the actual change>
```

`Decision` is required once a suggestion is adopted, adopted in part, declined, or implemented. `Change` is required for implemented suggestions.

## Rules

- Each suggestion keeps its own attribution, even when one document or meeting contains several people's advice.
- Exact statements, your recollections, and agent summaries are labeled differently.
- A suggestion can be received, under discussion, adopted, adopted in part, declined, or implemented. Adopted is not implemented until the change exists.
- Advice becomes a requirement or a decision only when you confirm it. You resolve conflicting suggestions; they are not ranked by seniority or title.

## Who edits what

Give the agent the documents or tell it what was said. The agent archives, extracts, and organizes the advice and helps you decide what to do with it. Example request: "Organize these comments from my collaborators, discuss their implications with me, and apply the changes I choose."

Related skill: `research-feedback`.
