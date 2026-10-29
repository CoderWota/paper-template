# Model Selection

Recommends which AI model to use for each kind of work in your project (drafting and polishing, translation, literature work, analysis code, routine tasks), based on the AI application you actually use, such as Claude Code, Codex, or Cursor. Different applications offer different models, so the recommendation always comes from your application's current official documentation.

Ask, for example: "Which model should I use in my AI tool for polishing the English of my paper, and which one for routine edits?"

## What to expect

- The agent first finds out which application and plan you use, then reads the current official model pages and tells you the date it read them. Model offers change often, so nothing comes from memory.
- Each recommendation gives the reason and the trade-off in cost, usage limits, or speed, and only names models that your application and plan offer.
- You learn how to switch. A change to a saved default setting happens only with your consent, and the agent says whether it affects every project or only this one.
- When you move to another provider, the agent offers to check its training and data-use settings first.

The agent instructions are in [SKILL.md](SKILL.md), and dated starting points are in [sources.md](sources.md). Related skills: `privacy-configuration`, `environment-management`.
