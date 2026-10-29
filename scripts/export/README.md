# Export Filters and Helpers

Pandoc filters and helpers that turn the workspace's Markdown into formatted outputs with `scripts/export.py`. They implement the [Markdown and export conventions](../../docs/markdown-and-export-conventions.md) that Pandoc and pandoc-crossref do not cover on their own:

- `equation-labels.lua` attaches an equation label written as its own paragraph (`{#eq:id}` after a blank line) to the formula before it. The workspace writes labels this way because GitHub stops rendering a formula whose closing `$$` line carries a label.
- `mermaid-figures.lua` replaces each Mermaid block with the figure rendered for it and takes the caption and label from the `: Caption {#fig:id}` paragraph after the block. A diagram that was not rendered stays as code and is reported.

Both run before pandoc-crossref. The agent maintains these files; researchers never need to edit them.
