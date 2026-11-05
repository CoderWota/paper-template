# Manuscript Logic Map

Internal authoring reference. This Mermaid map is not manuscript body text and must never be listed in `manifest.yaml` or included in a publication output.

Follow the [internal logic map guide](../docs/logic-map-guide.md) when building or reviewing this file.

No manuscript logic map yet. Replace this scaffold after the paper's argument and structure are confirmed, or after an imported draft is adopted. The nodes below are placeholders, not claims about this paper.

```mermaid
flowchart TD
    Q["Research question"]
    E1["Evidence or result 1 • status: checked / observed / unchecked / missing"]
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
