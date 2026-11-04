# Manuscript Import

Brings an existing manuscript into the workspace: a Word, LaTeX, OpenDocument, Markdown, or PDF draft becomes section files in `manuscript/`, with its images, title and abstract, formulas, footnotes, and citations, in the workspace conventions.

Ask, for example: "Organize this Word manuscript into the workspace, keep its text, figures, and references, and show me anything that could not be migrated."

## What to expect

- Your original file is kept unchanged. Word, LaTeX, and OpenDocument files are converted with Pandoc on this computer; nothing is uploaded. A PDF draft cannot be sent to MinerU under the confirmed reference-only scope. Keep it unchanged and ask for a readable editable copy or another authorized route.
- Tracked changes and comments are never accepted silently: the agent shows them and asks what to do. Comments from colleagues can be kept as research feedback.
- An existing manuscript is never replaced; the imported version is staged beside it for comparison.
- The adopted or staged draft gets an internal Mermaid logic map of its existing argument. It stays out of manuscript assembly and does not verify the cited sources.
- A list of everything that needs a check (unresolved citations, formulas that were images, numbers typed by hand) comes with the result. Your wording and claims are not changed.

The agent instructions are in [SKILL.md](SKILL.md). The skill uses `scripts/ingest.py` and `scripts/manuscript.py`. Related skills: `manuscript-audit`, `manuscript-revision`, `research-feedback`, `source-ingestion`.
