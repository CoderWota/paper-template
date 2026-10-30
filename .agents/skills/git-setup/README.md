# Git Setup

Prepares or repairs the local version history of the workspace when you want one: installs Git with your consent if it is missing, creates the history, agrees with you on what it tracks, and keeps passwords and keys out of it. During paper-project initialization, the assistant disconnects a clear link to the original template repository without discarding your local versions. Ambiguous connections need your decision.

Ask, for example: "Set up version history for this paper."

## What to expect

- Local version setup follows your request; a clear template connection is disconnected as part of confirmed paper-project initialization. Nothing is sent anywhere.
- Existing local files, branches, and commits are kept; the template's remote-tracking references are removed with its connection.
- You never need to edit Git settings yourself.

The agent instructions are in [SKILL.md](SKILL.md). Related skills: `git-inspection`, `git-save`, `environment-management`.
