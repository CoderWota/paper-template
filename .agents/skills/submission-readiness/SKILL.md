---
name: submission-readiness
description: Assess manuscript and package readiness for a venue, with supported strengths, concerns, and remaining work; no acceptance odds.
---

# Submission readiness

Outcome: an assessment of the current manuscript and package against the selected venue: strengths with their evidence, likely reviewer concerns, and a prioritized list of remaining tasks with who must do each. It reuses only current checks. It states no acceptance probability and submits nothing.

## Step 1: Gather the current state

1. Read `requirements/project.md` (target venue), the venue note in `research/venues/` (scope, article types, requirements, AI policy, data, code, and reporting policies, required files and declarations), the profile's `requirements.md`, `manuscript/outline.md`, `manuscript/logic-map.md`, and `state/current.md`. Read the [internal logic map guide](../../../docs/logic-map-guide.md) and [argument and impact guidance](../manuscript-writing/argument-and-impact.md) for the coherence and venue-fit assessments. Inspect `python scripts/manuscript.py logic-status --json`. Report missing, scaffold, unrecorded, stale, or invalid synchronization; a read-only assessment does not refresh the graph.
2. Run the state checks: `python scripts/manuscript.py check` (problems and open `[TODO: ...]` markers), `python scripts/manuscript.py checks` (audits and evidence checks, current or stale), `python scripts/research.py check` (stale results), `python scripts/export.py verify --profile <id>` (the latest build and whether it is still current), and `python scripts/literature.py audit-bibliography`. Inspect publication text and figure and table captions against the confirmed target paper language; the format checks do not prove language readiness.
3. A check whose inputs changed is stale: run it again (`manuscript-audit`, `submission-assembly`) or report that part as not checked. Never carry an old pass forward as evidence for the changed manuscript.

## Step 2: Assess each part separately

4. **Scientific support and contribution.** Compare the manuscript with its outline and logic map, then check the main and supporting claims against current audits, evidence checks, results, and material limitations. Use the graph and reasoning register to locate missing premises and inferential steps. Verify empirical premises against sources/results, and inspect original deductions, analyses, interpretations, and judgments through their assumptions, operations, conditions, and criteria. A sound argument can support an original derived claim; current map fingerprints alone do not establish soundness. Assess whether the paper explains what it contributes, why the field or intended audience should care, and how that value fits the venue. Tie concerns to inspected support and a specific consequence. Missing validation cannot be counted as complete; a potential impact is not a demonstrated effect, and an unpromised extension is not automatically required.
5. **Venue policies.** The AI-use policy and the disclosure it requires, prepared only from what actually happened; data and code availability; reporting guidelines for the article type; ethics, consent, and permissions for reused material; preprint and prior-publication rules.
6. **Document and format.** A current, passing build with the venue's profile; the rendered inspection; length and required sections; references and citation style.
7. **Package completeness.** The venue's list of files: manuscript, title page, separate figures or tables, supplementary material, cover letter, response letter for a revision, and declarations. Mark each as present (with its location), prepared but awaiting the researcher, or missing.
8. **Facts only the authors can give.** Author names and contributions, affiliations, funding, conflicts of interest, approvals, consent, and data availability statements. Ask the researcher for them; never invent, infer, or fill them from earlier projects.

## Step 3: Report

9. Report in the interaction language:
   - **Strengths**, each with its evidence (a checked result, an inspected source, a passed check).
   - **Likely reviewer concerns**, each tied to the venue's scope or policy, an audit finding, or a known limitation of the evidence, and labeled as `manuscript-audit` labels the weaknesses in a reviewer's view: presentation or substance, and fixable within a revision or structural.
   - **Remaining tasks**, prioritized as blocking, important, or minor, each with its owner (agent, researcher, coauthor, or another person) and the skill or step that addresses it.
10. Discuss prospects only through these strengths, risks, and improvements. Never state a probability of acceptance or treat a venue's acceptance rate as this paper's chance; never promise an outcome. Publication-prospect forecasts and a scored review on the venue's form belong to `mock-review`; its diagnostic scores are not probabilities.
11. Write the report to `outputs/checks/<date>-readiness-<venue-id>.md` and record it with `python scripts/manuscript.py record-check --kind readiness --input <the manuscript files, outline, logic map, build record, and venue note> --result passed|findings|failed --summary "..." --report <report>`.
Record only existing inspected files as inputs; name missing framework files in the report rather than passing nonexistent paths to `record-check`.

12. Preparing a package is not submitting it. Contacting the venue, uploading files, or filling a submission form is the researcher's own action; do it only on their explicit instruction for that destination, and never as part of this skill.

## Completion check

- Each part was assessed separately, and every reused check was current; stale ones were rerun or reported as not checked.
- The framework was compared with the manuscript and included as an input; its synchronization state and any empirical, inferential, or evaluative gaps were reported separately.
- Strengths, concerns, and tasks are each tied to evidence, and author-only facts were asked for, not invented.
- No acceptance probability appears, and nothing was submitted or sent.
- The report exists with a check record naming its inputs.
