---
name: research-ideation
description: Explore distinct research directions from interests, observations, readings, or data; save only ideas the researcher chooses.
---

# Research ideation

Outcome: three to five research directions that differ in kind, each grounded in the researcher's interests, material, observations, and constraints, with its originality stated as not yet compared or preliminary. The directions that the researcher asks to keep are notes in `ideas/`, listed in `ideas/index.md`.

## Step 1: Gather the starting point

1. Read `state/current.md`, `requirements/project.md`, `ideas/index.md`, and the notes of related ideas. Read `references/index.md`, and only the source notes, search records, and result records that bear on the interest.
2. Restate the starting point in a few lines: the interest or puzzle, the material available (sources, data, observations, the researcher's earlier work), and the constraints the researcher stated, such as time, access, method, or language. Quote the researcher's own words where they matter.
3. Help an undeveloped thought take shape before you examine it. Ask only for missing context that would change the directions, one question at a time; first look in the workspace for the answer.

## Step 2: Propose directions

4. Propose three to five directions that differ in the kind of contribution, not only in wording: for example a new observation, an explanation, a concept, a method, a dataset, a synthesis, an interpretation, a replication, or a boundary condition. Fit them to the discipline. An experiment is not required for a conceptual, qualitative, interpretive, or historical contribution.
5. For each direction, give:
   - the question it asks;
   - the possible contribution;
   - its basis: the researcher's words, or linked workspace material;
   - the main assumption it depends on;
   - feasibility with the resources the researcher named, and what is missing;
   - the first check that would show whether it is worth pursuing.
6. Keep novelty, significance, feasibility, and support apart. Say what was compared: "not yet compared with prior work" when nothing was searched, or the search scope when something was. Never call a direction new or unprecedented, and never invent a literature gap, a finding, a dataset, or a source. A search that returns little does not show a gap.
   Identify any ambiguity in the question and a competing explanation or counterexample when the inspected material supplies one. Explain the concrete overlap and difference from inspected work rather than assigning a novelty score or a novel/not-novel label. Frame an untested alternative as a hypothesis, not as the researcher's view or a finding.
7. Recommend which direction to examine first, and why. Then ask which directions, if any, the researcher wants to keep or examine further.

## Step 3: Keep what the researcher chooses

8. Save a direction only when the researcher asks to keep it. Write `ideas/<idea-id>.md` with the layout in `ideas/README.md`, in English, with a faithful English rendering of the researcher's request quoted in the `Retained` line. Add one line to `ideas/index.md` with the link and the status `exploratory`. Several related directions can share one note when the researcher keeps them together.
9. A kept idea is not a requirement, a decision, a claim, or evidence. Do not copy it into `requirements/` or `manuscript/`. Mark a retained hypothesis as unverified.
10. Review any broken links reported by `python scripts/research.py check` (use `python3` or `py -3` when `python` is not found). Repair a broken link when it is within scope; the command does not validate the form or quality of idea records.

## Hand off

- To examine one direction closely: `idea-deepening`. To find and compare prior work: `literature-discovery`, then `literature-and-evidence` or `research-investigation`. To weigh its value: `impact-assessment`. To plan the work: `research-planning`.
- Selecting a direction as the research question changes the project goal. That is a major decision: ask the confirmation question, then record it with `constraint-maintenance`.

## Completion check

- The directions differ in kind, and each states its question, contribution, basis, assumption, feasibility, and first check.
- Originality is stated as not compared or preliminary, with the scope of any search; nothing was invented.
- Only the directions that the researcher asked to keep are in `ideas/`, each with the researcher's words, and the index lists them.
- Any reported broken link in the records you wrote was reviewed and resolved or disclosed.
