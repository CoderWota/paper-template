---
name: submission-readiness
description: Assess manuscript and package readiness for a venue, with supported strengths, concerns, and remaining work; no acceptance odds.
---

# Submission readiness

Outcome: an assessment of the current manuscript and package against the selected venue: strengths with their evidence, likely reviewer concerns, and a prioritized list of remaining tasks with who must do each. It reuses only current checks. It states no acceptance probability and submits nothing.

## Step 1: Gather the current state

1. Read `requirements/project.md` (target venue), the venue note in `research/venues/` (scope, article types, requirements, AI policy, data, code, and reporting policies, required files and declarations), the profile's `requirements.md`, `manuscript/outline.md`, and `state/current.md`. Read [argument and impact guidance](../manuscript-writing/argument-and-impact.md) for the venue-fit and contribution assessment.
2. Run the state checks: `python scripts/manuscript.py check` (problems and open `[TODO: ...]` markers), `python scripts/manuscript.py checks` (audits and evidence checks, current or stale), `python scripts/research.py check` (stale results), `python scripts/export.py verify --profile <id>` (the latest build and whether it is still current), and `python scripts/literature.py audit-bibliography`. Inspect publication text and figure and table captions against the confirmed target paper language; the format checks do not prove language readiness.
3. A check whose inputs changed is stale: run it again (`manuscript-audit`, `submission-assembly`) or report that part as not checked. Never carry an old pass forward as evidence for the changed manuscript.

## Step 2: Assess each part separately

4. **Scientific support and contribution.** Compare the main and supporting claims with current audits, evidence checks, results, and material limitations. Assess whether the paper explains what it contributes, why the field or intended audience should care, and how that value fits the venue. Tie concerns to inspected support and a specific consequence. Missing validation cannot be counted as complete; a potential impact is not a demonstrated effect, and an unpromised extension is not automatically required.
5. **Venue policies.** The AI-use policy and the disclosure it requires, prepared only from what actually happened; data and code availability; reporting guidelines for the article type; ethics, consent, and permissions for reused material; preprint and prior-publication rules.
6. **Document and format.** A current, passing build with the venue's profile; the rendered inspection; length and required sections; references and citation style.
7. **Package completeness.** The venue's list of files: manuscript, title page, separate figures or tables, supplementary material, cover letter, response letter for a revision, and declarations. Mark each as present (with its location), prepared but awaiting the researcher, or missing.
8. **Facts only the authors can give.** Author names and contributions, affiliations, funding, conflicts of interest, approvals, consent, and data availability statements. Ask the researcher for them; never invent, infer, or fill them from earlier projects.

## Step 3: Report

9. Report in the interaction language:
   - **Strengths**, each with its evidence (a checked result, an inspected source, a passed check).
   - **Likely reviewer concerns**, each tied to the venue's scope or policy, an audit finding, or a known limitation of the evidence, and labeled as `manuscript-audit` labels the weaknesses in a reviewer's view: presentation or substance, and fixable within a revision or structural.
   - **Remaining tasks**, prioritized as blocking, important, or minor, each with its owner (agent, researcher, coauthor, or another person) and the skill or step that addresses it.
10. Discuss prospects only through these strengths, risks, and improvements. Never state a probability of acceptance or treat a venue's acceptance rate as this paper's chance; never promise an outcome. A scored mock review on the venue's form is `mock-review`; its scores are not a probability either.
11. Write the report to `outputs/checks/<date>-readiness-<venue-id>.md` and record it with `python scripts/manuscript.py record-check --kind readiness --input <the manuscript files, the build record, and the venue note> --result passed|findings|failed --summary "..." --report <report>`.
12. Preparing a package is not submitting it. Contacting the venue, uploading files, or filling a submission form is the researcher's own action; do it only on their explicit instruction for that destination, and never as part of this skill.

## Completion check

- Each part was assessed separately, and every reused check was current; stale ones were rerun or reported as not checked.
- Strengths, concerns, and tasks are each tied to evidence, and author-only facts were asked for, not invented.
- No acceptance probability appears, and nothing was submitted or sent.
- The report exists with a check record naming its inputs.
