# Ideas

Research ideas and directions you choose to keep, including unfinished ones. Ideas are kept apart from manuscript prose and from verified findings: saving an idea does not make it a claim, a writing rule, or evidence.

## Contents

- [`index.md`](index.md): one line per retained idea, with its status and a link to its note when one exists.
- A short note per idea worth developing, created only when useful, for example `urban-heat-and-sleep.md` (lowercase ASCII letters, digits, and hyphens).

Status values: **exploratory**, **developed** (question, contribution, and next check are clear), **incorporated** (used in the manuscript), or **abandoned**. Chinese equivalents (`探索中`, `已发展`, `已纳入`, `已放弃`) are accepted. An incorporated idea still needs evidence for its claims, and a retained hypothesis stays labeled as unverified.

## Note layout

Notes written by the agent use these labels, with values in English. Leave out a line that has nothing to say yet. Notes you write yourself can take any form; the agent adds them to the index.

```text
# <idea name>

- Status: exploratory | developed | incorporated | abandoned
- Retained: <date>; "<your words asking to keep it>"
- Question: ...
- Contribution: <the kind of contribution: an observation, explanation, method, dataset, synthesis, interpretation, ...>
- Basis: <your observation in your words, materials, or linked sources>
- Prior work: <compared sources with links, or "not yet compared">
- Originality: <not assessed | preliminary, with the search scope | compared with ...>
- Assumptions: ...
- Open questions: ...
- Next check: ...
```

`python scripts/research.py check` checks that every note is listed in the index and that each index line and note names a known status.

## Who edits what

You can write ideas here directly, in any form. The agent saves an idea only when you ask to keep it, links related sources and sections, and maintains the index.

Example requests: "Based on these readings and my interests, help me develop several distinct research ideas." "Examine this idea with me, one question at a time."

Related skills: `research-ideation`, `idea-deepening`, `impact-assessment`.
