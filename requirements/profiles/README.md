# Output Profiles

One subdirectory per intended output, such as a journal submission or a thesis format: `<profile-id>/`. A profile holds the requirements for that output and the resources needed to produce it. Changing the target journal selects a different profile; it does not require rewriting the scientific content.

## Each profile contains

```text
<profile-id>/
├── README.md          # Which output this is, its sources, and its current check status
├── requirements.md    # Adopted requirements, each mapped to its source, implementation, and check result
├── profile.yaml       # Export settings maintained by the agent
├── originals/         # Supplied author guidelines and format examples, kept unchanged
└── templates/         # Word templates, LaTeX classes, citation styles, and other format files
```

The agent creates each of these folders with its own README. A project without a target venue can use a neutral profile.

## Who edits what

- **You** supply the journal's instructions and any Word, LaTeX, or PDF template, and decide conflicts between sources.
- **The agent** extracts the explicit rules, clarifies ambiguity with you, maintains `profile.yaml` and the templates, and checks the actual rendered output against the requirements. You never need to edit a style file or YAML.

Example request: "Format my manuscript using these journal instructions and this template, then check the result against the requirements."

Related skills: `journal-selection`, `submission-assembly`, `submission-readiness`.
