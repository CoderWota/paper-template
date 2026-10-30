# Paper Hands-On

Introduces the workspace when you do not know how to use it, and guides research and manuscript work from wherever you are: an interest, readings, an idea, data, an existing draft, or reviewer comments. The agent connects routine work toward your agreed goal, prepares evidence and alternatives for discussion, and brings scientific choices back to you.

For your first conversation, say "I do not know how to use this project" or "Where should I put my files?" The assistant gives one compact map of all top-level folders with common subfolders, followed by three short examples. You can ask for details about any folder. You need not sort files or initialize a paper to take the tour.

For research work, ask, for example: "I have an area of interest but no paper yet. Guide me from collecting literature to a manuscript in the format of a suitable journal," or simply "What should I do next on this paper?" or "Let's continue where we stopped."

## What to expect

- A tour explains what each folder holds, when it is used, what you can do, and what the assistant maintains. It changes no files or project settings. You can stop there or choose a first task.

- The agent reads the project's records to see where things stand, so a new session continues where the last one stopped.
- Within the agreed scope it continues across routine stages without asking you to dispatch each one. It pauses for a necessary judgment or a specific blocker, while useful independent work can continue.
- You make the scientific choices, provide what only you can, and review the results; the agent does the production work and keeps track of progress in `state/current.md`.
- Nothing is invented to move the paper forward: research that has not been done is named as missing. Submitting or sending anything stays your decision.
- You can always ask for a single task directly instead of following the guide.

The agent instructions are in [SKILL.md](SKILL.md). It uses all the standalone skills, and `scripts/status.py` to recognize the stage of the project. Related guide: `git-hands-on`.

The [beginner directory guide](directory-guide.md) is loaded only for orientation; existing users and direct task requests do not need it.

The initial tour avoids repeating the map in separate subfolder lists or summaries. [Directory details](directory-details.md) are available only for follow-up questions.
