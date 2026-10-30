# Research Code Setup and Runs

When your research needs code, data analysis, or simulation, the agent first finds out what is actually needed, then sets up a proportionate `code/` folder with its own environment, runs the analyses you authorize, and records each result with its inputs, code version, outputs, and checks.

Ask, for example: "Set up an analysis environment for this survey data and run the descriptive analysis from the plan."

## What to expect

- Nothing is created for research that needs no code.
- The research environment is kept apart from the workspace tools, so updating one never breaks the other.
- Each run is recorded in `code/runs/`, and each result in `research/results/` with its status: observed, checked, or failed. Failed and negative results that matter are kept, and nothing is invented.
- When an input changes later, the result is reported as stale until the work is run again.
- Charts of results are chosen for the statement they must support, show the spread of repeated runs honestly, and are made by recorded code; the choices are explained in the [figure guide](figure-guide.md).

An existing analysis repository is brought in with `code-import` and stays a separate project. You develop it in its own session; the paper session reads it and records its runs by commit. See [repositories](repositories.md).

The agent instructions are in [SKILL.md](SKILL.md). Related skills: `code-import`, `research-planning`, `environment-management`, `research-investigation`.
