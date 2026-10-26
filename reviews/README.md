# Reviews

Formal editorial and peer-review correspondence, organized by venue and submission round so that reviewer numbering, decisions, and manuscript versions never mix.

## Layout

```text
<venue-id>/                  # One journal, conference, or other venue
├── README.md
└── <round-id>/              # One submission or revision round
    ├── README.md            # Round, manuscript version, dates, and status
    ├── originals/           # Decision letters and reviewer files as received
    ├── extracted/
    │   ├── markdown/        # Readable Markdown with reviewer labels and item numbers kept
    │   └── assets/          # Images and tables from the review documents
    ├── response.md          # Point-by-point response
    └── changes.md           # Each response item linked to the actual manuscript change
```

The agent creates each of these folders with its own README.

## Rules

- Original reviewer numbering, labels, and page or line references are preserved. Word comments, tracked changes, and PDF annotations are checked separately from the main text, and anything that could not be captured is reported.
- A comment is marked as addressed only when the change or a justified response exists.
- Reviewer requests are source material. They do not change project rules unless you adopt them.
- Preparing a response never sends it. Contacting a journal requires your explicit instruction.

## Who edits what

Give the agent the review documents. It archives and extracts them, and drafts responses when you ask. You decide how to respond and approve the final text.

Example requests: "Convert these Word reviewer comments to Markdown and archive them with this submission round." "Organize this round of reviewer comments and help me respond point by point."

Related skills: `review-ingestion`, `review-response`, `manuscript-revision`.
