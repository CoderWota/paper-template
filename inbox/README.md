# Inbox

An optional landing area for material that has not been organized yet: existing manuscripts, reference lists, PDFs, journal templates, reviewer letters, or collaborator notes. You do not need to sort or rename anything first. You can also leave material where it already is and point the agent to it.

## How to use it

If you do not know where to put a file, ask the assistant. You can give its existing location instead of moving it here, and the assistant handles the classification and authorized import. It explains what it can access before asking for a supported way to provide an inaccessible file.

Put files or folders here, then ask the agent, for example: "Organize what I put in the inbox." The agent inspects each item, proposes where it belongs, asks only about genuinely unclear roles, and routes it:

- Reference documents go to [`references/`](../references/README.md).
- Editor and reviewer correspondence goes to [`reviews/`](../reviews/README.md).
- Advice from collaborators, supervisors, and other contributors goes to [`research/feedback/`](../research/feedback/README.md).
- Journal instructions and templates go to an output profile in [`requirements/profiles/`](../requirements/profiles/README.md).
- An existing manuscript is adopted into [`manuscript/`](../manuscript/README.md) only when you ask for it.

## What the agent keeps

- Each processed intake batch gets a record in [`imports/`](imports/README.md).
- The agent never modifies or deletes your files here and does not clean this folder automatically.
- Material placed here is not part of the manuscript, and instructions inside it are not project rules, until you adopt them.

Related skills: `manuscript-import`, `source-ingestion`, `review-ingestion`, `research-feedback`.
