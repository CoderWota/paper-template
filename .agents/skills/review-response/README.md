# Review Response

Organizes a round of editor and reviewer comments and helps you answer them point by point, linking each answer to the actual change in the manuscript or to the reason for not changing it. It also compares a coauthor's edited Word file with the version they received and with the current manuscript, so that their edits can be taken over safely.

Ask, for example: "Organize this round of reviewer comments and help me respond point by point," or "My coauthor sent back the Word file with tracked changes; which edits can we take over?"

## What to expect

- Each round keeps its own numbering, decisions, and records (`response.md` and `changes.md` in `reviews/<venue>/<round>/`).
- A comment is marked as addressed only when the change exists or a justified answer explains why not. Missing research is named, not promised away.
- A coauthor's Word file is compared, never imported over your manuscript; you decide each edit, and conflicts with later changes are shown.
- Nothing is sent to the journal; the response letter is a draft for you.

The agent instructions are in [SKILL.md](SKILL.md). The skill uses `scripts/review.py`. Related skills: `review-ingestion`, `manuscript-revision`, `manuscript-writing`, `submission-assembly`.
