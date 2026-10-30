---
name: research-planning
description: Plan methods, evidence, resources, work items, and milestones for a selected question; confirm consequential choices.
---

# Research planning

Outcome: `research/plan.md`, a current plan that connects the question and the intended contribution to methods or lines of argument, the evidence each claim needs, what is available and what is missing, work items with owners and status, risks, and the next action. Parts that the researcher has not confirmed are marked as proposed.

## Step 1: Gather the inputs

1. Read `requirements/project.md`, the selected idea note, `research/decisions/index.md` (active decisions), `research/results/index.md`, `research/plan.md` if it exists, the relevant venue note when a target constrains methods, and `references/index.md`.
2. If no question has been selected, offer `research-ideation` or `idea-deepening`. Never invent the question.

## Step 2: Build the plan

3. **Claims and evidence.** For each intended claim, state what evidence would support it and what would weaken it; which evidence already exists (link evidence notes and result records with their status); and which is still required.
4. **Methods or lines of argument.** Fit them to the discipline: empirical, computational, documentary or archival, theoretical or formal, qualitative or interpretive, or conceptual. Do not force an experiment, a fixed article structure, or a method the question does not need. For each, give the inputs, the procedure, the checks (for example reproduction, a reference result, sensitivity, counterexamples, or comparison with sources), and what would count as failure.
   Explain which question each method can answer, which conclusion it cannot establish, and the trade-offs of meaningful alternatives. Recommend an approach from the available evidence and resources so the researcher can judge the choice, rather than only listing tools.
5. **Resources.** Data, sources, access, tools, compute, skills, people, time, cost, and permissions such as ethics approval or licenses. Inspect the workspace and the computer (`environment-management`) before you assume a resource. Mark work that needs the researcher or another person, such as fieldwork, laboratory work, institutional access, or consent, as an external dependency with a prepared next step.
6. **Work items.** Ordered items, each with an owner (agent, researcher, or another person), a status (proposed, confirmed, in progress, done, or blocked), and the result record or evidence it should produce.
   State each item's prerequisite, usable output and completion check, and which scientific choice, if any, it needs. Keep these in the existing work table or a short accompanying note. After confirmation, carry requested execution through the matching skills without asking the researcher to dispatch routine handoffs. A planning-only request stops at the plan.
7. **Risks, limitations, and alternatives.** What could fail and the fallback for each, and the limits that the plan accepts, such as scope, generalizability, or missing access.

## Step 3: Confirm the choices

8. The plan proposes; the researcher chooses. A method, a material or corpus scope, an inclusion boundary, or an excluded analysis is a major decision: ask one question at a time with your recommendation. After a clear yes, record the decision with `constraint-maintenance`, mark that part of the plan as confirmed, and link the decision record.
9. A plan is not a result. Never write an expected finding as if it were observed; anticipated outcomes are labeled as expectations.

## Step 4: Record

10. Write `research/plan.md` in the interaction language with these sections: question and contribution (quoted from `requirements/project.md`, with the idea link), claims and evidence (a table: claim, evidence needed, available now, still required), methods or lines of argument (each marked proposed or confirmed), resources, work items (a table: ID, work, owner, status, produces), risks, limitations, and alternatives, and the next action. Keep text that the researcher wrote.
11. Keep the plan current: replace outdated parts instead of appending history. Confirmed choices keep their history in decision records.
12. Update `state/current.md` with the next action.

## Hand off

- Literature: `literature-discovery`, `reference-download`, `source-ingestion`. Source-based inquiry: `research-investigation`. Computation and analysis: `research-code-setup`, which runs the work and writes result records. Structuring the paper: `manuscript-outline`, as the availability table in `AGENTS.md` allows.

## Completion check

- Every claim lists the evidence it needs, separated into available now and still required, with links.
- Methods fit the question and discipline, each with checks and failure criteria.
- Every work item has an owner and a status; external dependencies have a prepared next step; risks and accepted limitations are stated.
- Unconfirmed choices are marked proposed; confirmed ones link their decision records.
- No expected finding is written as a result.
