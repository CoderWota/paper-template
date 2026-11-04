# Manuscript Logic Map

Internal authoring reference. This Mermaid map is not manuscript body text and must never be listed in `manifest.yaml` or included in a publication output.

No manuscript logic map yet. Replace this scaffold after the paper's argument and structure are confirmed, or after an imported draft is adopted. The nodes below are placeholders, not claims about this paper.

```mermaid
flowchart TD
    Q["Research question"]
    E1["Evidence or result 1 • status: checked / observed / missing"]
    C1["Supporting claim 1"]
    C2["Supporting claim 2"]
    M["Main claim"]
    A1["Alternative or contrary evidence"]
    G1["Open evidence or inference gap"]
    L1["Limitation"]
    I["Conclusion or implication"]
    Q -->|answered by| M
    E1 -->|supports, qualifies, or challenges| C1
    C1 -->|state the inferential step| C2
    C2 -->|contributes to| M
    A1 -->|qualifies or challenges| M
    G1 -.->|needed to assess| C1
    M -->|within the evidence scope| I
    L1 -->|narrows| I
```

Replace each multi-option edge label with the actual relationship and explain each inferential step in a short edge label. Group claims by the paper's real sections when that improves the view. If a single graph becomes hard to read, keep this paper-level flowchart and add a focused local flowchart below for the section that needs it. Do not force a fixed article structure.

Arrows show support, inference, qualification, challenge, or another stated logical relation, not manuscript reading order. Use dashed arrows only for an explicit gap and label what evidence or reasoning is needed; do not make a gap look like support.

For imported text, map what the draft states and mark source support as unchecked until it has been checked against an archived original or a checked result. The map exposes reasoning and evidence gaps; it does not prove that a claim is true.
