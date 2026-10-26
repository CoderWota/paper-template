# Manuscript

The working text of the paper and its figures, tables, and other assets. Write in the language chosen for the manuscript. Nothing here assumes a discipline, an article structure, or a citation style.

## Contents

| Path | Role |
| --- | --- |
| [`outline.md`](outline.md) | The argument and section plan. Not a second copy of the body text. |
| [`manifest.yaml`](manifest.yaml) | The explicit list and order of section files that make up the manuscript. |
| Section files, for example `01-introduction.md` | Body text: at most one Markdown file per chapter or major section. A single-file manuscript is also fine. |
| [`assets/`](assets/README.md) | Figures, tables, captions, and their sources. |

Only files listed in `manifest.yaml` are assembled into outputs. This README, the outline, notes, and unselected drafts are never included.

## Writing conventions

- Mathematics uses GitHub-renderable LaTeX: `$...$` inline, and `$$` on separate lines for display.
- Explanation diagrams use fenced `mermaid` blocks. Scientific plots stay in their plotting formats.
- Citations and cross-references are maintained by the agent, never numbered by hand.

Details: [Markdown and export conventions](../docs/markdown-and-export-conventions.md).

## Who edits what

You can write and revise prose directly at any time. The agent drafts and revises on request using your confirmed requirements and the actual evidence, maintains the manifest, outline, and references, and preserves your direct edits.

Example requests: "Revise this section using my confirmed writing requirements and identify claims that need evidence." "Organize this Word manuscript into the workspace conventions."

Related skills: `manuscript-outline`, `manuscript-writing`, `manuscript-audit`, `manuscript-import`, `manuscript-revision`.
