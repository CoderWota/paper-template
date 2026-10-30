# Researcher-led paper work loop

This guide describes how the existing research and manuscript skills connect during a broad, authorized goal. It is a flexible loop, not a required sequence or a new workflow system. Start at the stage that fits the researcher's request and current materials. A project may not need computation, experiments, a venue choice, or every record described below.

## Shared roles

- The researcher sets the question, chooses consequential methods and scope, judges what the evidence means, and owns the paper's final claims and expression.
- The agent inspects available material, retrieves and compares evidence within the confirmed scope, proposes checks and alternatives, carries out authorized research support, drafts within confirmed findings, and connects resulting artifacts.
- A script reports or blocks on facts it can establish, such as an unresolved citation key, a changed input checksum, or a missing file. Its output does not judge scientific importance, argument quality, or whether a conclusion is true.
- A model's review, score, or agreement with another model is feedback to inspect. It is not evidence or scientific verification.

## The loop

### 1. Frame a question from the researcher's starting point

Begin with the researcher's request, retained idea, existing draft, or documented question. Inspect the linked project material before asking for information it may already contain. Clarify ambiguity with one substantive question at a time. For each direction, separate its motivation, inspected prior work, assumptions, feasibility, and evidence. Give a recommendation with its basis; the researcher chooses the direction and any consequential scope.

Use `research-ideation` or `idea-deepening` when the question is not settled. Use `literature-discovery`, `literature-and-evidence`, or `research-investigation` to check what sources can establish. A small or empty search does not establish novelty or a gap.

### 2. Connect the question to evidence and a workable plan

When planning is useful, link each intended claim to evidence that would support or weaken it. Mark what already exists, what remains to be gathered, and which work item will produce it. Describe what a method can answer, its limits, the resources it needs, and meaningful alternatives. Mark unconfirmed choices as proposed. The researcher confirms consequential methods, material boundaries, and research decisions; once confirmed, the agent carries out the authorized routine work across the relevant skills.

The plan is a guide to the inquiry, not a prediction of its results. Keep work items, prerequisites, owners, outputs, checks, and status in `research/plan.md` when a plan is warranted. Do not create a parallel task tracker.

### 3. Do and preserve the authorized work

For each work item, use the existing specialist skill and record the actual source, method, inputs, outputs, and checks in the appropriate record. Computational work uses its recorded run and result; source-based work keeps source versions and locators; other disciplines record the procedure or argument they actually used. Keep important failed attempts, negative results, and limits when they affect the conclusion.

Stop at a missing permission, resource, or researcher-only judgment. Name the exact dependency and prepare independent authorized work that can continue. A technical failure may receive a bounded repair within the same method. Do not rerun a substantive negative result merely to obtain a preferred outcome.

### 4. Bring findings back for interpretation

Report three things separately:

1. **Observation:** what the checked source, calculation, document, or run shows.
2. **Interpretation:** what that observation supports in the context of the question, and how strongly.
3. **Hypothesis:** a possible explanation that still needs a discriminating check.

Compare the result with the plan and its expectations, check technical integrity and contrary evidence, and explain which alternatives remain. Recommend whether the current account is supported, needs narrowing, or needs further evidence. Do not change the researcher's main explanation, method, or claim without confirmation. A negative result remains part of the evidence when it matters.

Record project findings in `research/results/` when they are research outputs, and link the result to the work item and to the claims, figures, tables, or checks that use it. A result marked checked records which checks were performed; it does not mean the researcher has endorsed its interpretation.

### 5. Build the paper from confirmed argument and evidence

Use `manuscript/outline.md` to connect the confirmed question and argument to sections, claims, sources, and project results. Draft from those records, not from expected findings. Keep unsupported claims visible as gaps or TODOs. Link important statements to source locators or result records; a citation key resolving in the bibliography does not show that the source supports the claim.

The manuscript follows the researcher's chosen paper language. Working notes can remain in another language. Preserve the researcher's wording and edits, and do not insert an AI signature or claim authorship.

### 6. Review, revise, and return upstream when needed

An audit identifies a specific passage, the evidence or rule behind a concern, and a feasible remedy. The researcher decides changes that alter scientific meaning, scope, or argument. Carry out authorized wording corrections and rechecks; use a recoverable revision for a major change. Reviewer and collaborator advice remains advice until the researcher adopts it.

When an audit or new result exposes a gap, route it back to the work that can address it: inspect a source, run an authorized analysis, revisit a proposed method with the researcher, update the outline, or revise the prose. If upstream evidence or code changes, inspect its recorded dependents, refresh affected results and checks, and recheck the affected passages, figures, and tables. Preserve author edits made since the revision began.

After the fix, revisit the original finding and confirm whether it is resolved, partly resolved, or still open. Then check the wider argument for consequences. This return to evidence is what closes the loop; a polished draft alone does not.

## Handoffs and continuation

Use the records already owned by each part of the work:

| Handoff | Keep the detail in | Pass forward |
| --- | --- | --- |
| Question to plan | `requirements/`, confirmed decisions, retained idea | The selected question, boundaries, open assumptions |
| Plan to research | `research/plan.md` | The work item, needed inputs, method status, expected record and check |
| Research to argument | Source notes and `research/results/` | Actual observations, locators, checks, alternatives, limitations, dependent claims |
| Argument to writing | `manuscript/outline.md` and evidence records | Confirmed claim order, support, gaps, figure and table links |
| Audit to repair | Audit report and check record | Exact finding, basis, recommended repair, affected inputs |
| Repair to recheck | Manuscript or revision records, refreshed results | Actual change and fresh evidence/check; unresolved reason |

Keep `state/current.md` short. It names the authorized goal, completed artifacts and checks, the exact open judgment or dependency, and the next useful action. Put the detailed reasoning in its existing plan, result, source, outline, audit, feedback, review, or revision record. On resumption, inspect those files and their inputs; the handoff note does not prove that a result is still current.

## What counts as a useful stopping point

Complete the authorized goal when its requested artifact exists, its relevant evidence and checks have been inspected, and the remaining limitations or choices are clear. A goal can be complete while a scientific question remains open, if resolving it requires a new researcher decision, external access, or new research outside the authorization. State that dependency plainly and leave a useful next step. Do not call a paper submission-ready solely because scripts report no problem or an AI reviewer is favorable.

## Design reference

The [AI Scientist repository](https://github.com/sakanaai/AI-Scientist) documents a connected pattern of preparing a template and baseline, launching research runs, generating a paper, and obtaining a review. This workspace borrows the useful connection between research outputs and review, while keeping question selection, consequential choices, interpretation, and final expression with the researcher. It does not adopt autonomous research execution or treat a model review score as validation.
