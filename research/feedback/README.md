# Research Feedback

Attributed advice about the research or the manuscript from co-researchers, collaborators, coauthors, supervisors, or anyone else whose input you want to keep, regardless of title or authorship. One subdirectory per feedback event, such as a received document or a meeting: `<feedback-id>/`.

## Each feedback directory contains

```text
<feedback-id>/
├── README.md        # Who gave the feedback, when, about which version, and its current state
├── originals/       # Received documents or your meeting notes, kept unchanged
├── extracted/
│   ├── markdown/    # Readable Markdown of the received documents
│   └── assets/      # Images and other files referenced by the Markdown
└── actions.md       # Each suggestion with its source, your decision, and actual progress
```

The agent creates each of these folders with its own README.

## Rules

- Each suggestion keeps its own attribution, even when one document or meeting contains several people's advice.
- Exact statements, your recollections, and agent summaries are labeled differently.
- A suggestion can be received, under discussion, adopted in part, declined, or implemented. Adopted is not implemented until the change exists.
- Advice becomes a requirement or a decision only when you confirm it. You resolve conflicting suggestions; they are not ranked by seniority or title.

## Who edits what

Give the agent the documents or tell it what was said. The agent archives, extracts, and organizes the advice and helps you decide what to do with it. Example request: "Organize these comments from my collaborators, discuss their implications with me, and apply the changes I choose."

Related skill: `research-feedback`.
