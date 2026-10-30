# Code Import

Brings an existing code repository, for example an R analysis, into the workspace. It can come from a Git address, a folder with or without Git, or a zip or tar archive. The code ends up in `code/<name>/` as its own Git repository, so you can develop the analysis next to the paper.

Ask, for example: "Import my R analysis folder into this project."

## What to expect

- Your original is never changed. A folder without Git becomes a new repository with one starting commit.
- Data files are not copied by default, and a clone does not bring data that Git does not track. The agent tells you which files are missing. Code that reads them fails until you put the data in the repository's data folder, or agree to copy it with the import.
- You work on the code in a separate session opened in the code folder. That session does not load the paper's rules.
- Back in the paper session, the agent reads the code as evidence for the manuscript and records each analysis run with the code version. It does not edit the code, and it does not read your data files unless you ask.
- If the paper session finds a problem in the code, it tells you and asks you to open a code session for the change.

The agent instructions are in [SKILL.md](SKILL.md). The skill uses `scripts/research.py`. Related skills: `research-code-setup`, `environment-management`, `git-setup`.
