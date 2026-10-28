# Review Ingestion

Files editor and reviewer documents by venue and submission round, and turns them into readable Markdown. Give the agent the decision letter, the reviewer reports, annotated PDFs, or Word files with comments and tracked changes; it keeps the originals unchanged in `reviews/<venue>/<round>/` and makes a Markdown copy of each.

Ask, for example: "Convert these reviewer comments to Markdown and file them under this journal's first round."

## What to expect

- Reviewer labels, item numbers, and page or line references stay as they are in the documents.
- Word comments, tracked changes, and PDF annotations are listed separately, because a normal conversion does not show them. The agent tells you what it found and what it could not capture.
- Rounds never mix, and importing the same files again creates no duplicates.
- Review documents are confidential: they are uploaded to an online service only if you confirmed that service for this kind of material.
- Nothing is sent to the journal, and no response is drafted.

The agent instructions are in [SKILL.md](SKILL.md). The skill uses `scripts/ingest.py`. Related skills: `source-ingestion` and `privacy-configuration`.
