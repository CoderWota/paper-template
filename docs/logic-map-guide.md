# Internal Logic Map

Use `manuscript/logic-map.md` to inspect how the paper's evidence and reasoning connect. It is an authoring aid, not manuscript text and not evidence that a claim is true.

## Build the map

- Start from the confirmed question and main claim. Add each material supporting claim and the local claim or inference made in every argumentative section. Do not invent a claim to fill an empty node.
- Connect evidence or result nodes to the claims they support, qualify, or challenge. Label each node with its status: **checked** when the source passage or result was checked for that claim, **observed** when a result exists but its support or interpretation is not yet checked, **unchecked** when a cited source has not been checked for that claim, or **missing** when required evidence is unavailable. A resolving citation key alone is not checked support.
- Do not draw an evidence-support edge from an unarchived source. Mark the citation unchecked and show a source-access gap if its original is unavailable.
- Keep evidence details in `outline.md`, source notes, or result records; use short node labels and record IDs when helpful. Do not turn the graph into a copy of the prose.
- Label every edge with the actual relation or inference. Arrows show logical relations, not manuscript reading order. Do not imply causality or stronger support than the evidence allows. Use dashed arrows only for an explicit evidence or reasoning gap, and label what is needed.
- Group nodes by the manuscript's real sections when that helps show how local reasoning feeds the paper-level claim. Use one paper-level flowchart by default. If a section's reasoning makes that graph hard to read, keep the paper-level graph and add a focused local flowchart in the same file. Do not impose a fixed article structure.
- Include alternatives, contrary evidence, and limitations when they change how a claim or conclusion should be read. Connect them to the affected claim; do not add decorative or immaterial branches.

## Follow the manuscript path

- **New paper:** build from the confirmed argument, the actual results, and checked sources in the outline. Keep unknown support as a visible gap. A new main claim or a changed interpretation remains a researcher decision.
- **Imported paper:** represent what the imported text actually says. Do not rewrite its argument during import. Mark an unclear inference as unclear and cited source support as unchecked unless it was checked against the archived original or a checked result.
- **Writing or revision:** update only the map nodes and edges affected by an authorized argument change. Keep the map aligned with the active manuscript or, for a staged revision, its candidate.

## Check traceability

Before completing or auditing the map, confirm that:

1. The main claim and conclusion are connected through visible supporting claims and inferential steps.
2. Every material supporting claim links to evidence with an explicit status or to a visible evidence/inference gap; no unresolved or unchecked citation is treated as checked support. Each argumentative section's central step connects to the paper-level argument or is marked as local context.
3. Every edge names its relation, and alternatives, contrary evidence, and limitations connect to the claims they qualify or challenge.
4. The map matches the confirmed outline and the current manuscript. A mismatch is reported or shown as unclear; the map never silently changes the researcher's argument.
5. The file is not listed in `manuscript/manifest.yaml` and is absent from publication output.

Use simple Mermaid flowchart syntax and quoted labels. Follow [Markdown and output conventions](markdown-and-export-conventions.md) for diagram syntax and rendering limits.
