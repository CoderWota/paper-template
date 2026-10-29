# Submission Assembly

Formats the manuscript as a Word file with the rules of a journal, an institution, or a neutral profile, and checks the result. Give the agent the author guidelines and any template; it keeps them unchanged, lists the rules they set, builds the file, and inspects the rendered pages against each rule.

Ask, for example: "Format my manuscript with these journal instructions and this Word template, then tell me what still fails."

## What to expect

- Every formula becomes a native, editable Word equation; diagrams become numbered figures; citations and cross-references are resolved, never numbered by hand.
- Each adopted rule is recorded with its source and its check result in the profile's `requirements.md`. Unclear or conflicting instructions are asked about, not guessed.
- The layout is fixed in the profile, not by editing your scientific text; content a rule requires but the paper lacks is reported, not invented.
- Previews are rebuildable. A final package is frozen in `outputs/releases/` only when you ask, and it is never overwritten. Submitting it remains your decision.

The agent instructions are in [SKILL.md](SKILL.md). The skill uses `scripts/export.py`. Related skills: `journal-selection`, `submission-readiness`, `manuscript-audit`.
