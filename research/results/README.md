# Research Results

Result records for the project's own results: what was done, with which inputs and which method or code version, what it produced, how it was checked, and which claims rely on it. External literature stays in [`references/`](../../references/README.md); a result here is the project's own observation, analysis, derivation, or documentary finding.

## Contents

- [`index.md`](index.md): one line per result with its status and a link.
- One record per result, for example `r001-placebo-test.md` (lowercase ASCII letters, digits, and hyphens).

## Record layout

The values are in your interaction language; the labels and status words stay as shown (Chinese equivalents such as `已提议`, `已尝试`, `已观察`, `已检查`, and `失败` are accepted), because `python scripts/research.py check` reads them.

```text
# r001 <short title>

- Status: proposed | attempted | observed | checked | failed
- Kind: computational | documentary | theoretical | qualitative | other
- Question: <what the result answers; a link to the plan item>
- Method: <code path, or the procedure or argument>
- Inputs:
  - `code/data/raw/survey.csv` sha256:<checksum>     or source IDs with locators
- Parameters: <settings, seeds, inclusion rules>
- Run: `code/runs/<run-id>/run.json`                  when the result came from a recorded run
- Outputs:
  - `code/outputs/table-1.csv` sha256:<checksum>
- Checks: <what was checked and how: reproduction, a reference result, sensitivity, counterexamples, source comparison; and what it found>
- Limitations: <scope and caveats>
- Used by: <manuscript passages or claims that rely on it, or "none yet">
- Researcher review: <not yet, or the date and your words>
```

Status words: **proposed** (planned, not run), **attempted** (started, no usable output yet), **observed** (output exists, not yet checked), **checked** (output exists and the listed checks were made), **failed** (the work or a check failed; kept when it matters to a conclusion). Your review is a separate line: a checked result is not approved by you until you say so.

## Rules

- A result is recorded only from work that was actually done. Anticipated findings belong in the plan, not here; nothing is invented or selected silently.
- When an input, output, or code version in a linked run changes, `python scripts/research.py check` reports the result as stale and names its recorded dependents. A stale result supports no claim until the work is run and checked again. The check does not infer unrecorded dependencies or validate the scientific argument.
- Failed or negative results that matter to a conclusion are kept.
- In the existing result narrative, separate observations, interpretations, and open hypotheses, with evidence and limits. `Used by` names dependent manuscript passages, figures, tables, and checks; keep it current when writing uses the result. If the list is incomplete, say which area needs inspection. Do not silently rewrite author text or update hashes to hide an upstream change.

## Who edits what

The agent writes these records when it runs an analysis or completes an investigation that you authorized, and keeps the checksums current. You review what the results show.

Related skills: `research-code-setup`, `research-investigation`, `research-planning`.
