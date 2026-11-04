---
name: manuscript-outline
description: Propose an evidence-linked manuscript structure from the confirmed question, actual results, and venue requirements.
---

# Manuscript outline

Outcome: `manuscript/outline.md` and `manuscript/logic-map.md`: a researcher-confirmed plan of the argument and sections, plus an internal Mermaid flowchart that makes the paper-level argument and local reasoning visible. Neither file is assembled into the manuscript.

## Step 1: Gather the inputs

1. Read `requirements/project.md` (question, contribution, article type, languages, target venue), `requirements/writing.md`, [argument and impact guidance](../manuscript-writing/argument-and-impact.md), `research/plan.md`, `research/results/index.md` (with each result's status), the evidence notes and search records that the plan links, the selected idea note, the venue note in `research/venues/` when a target is set, adopted suggestions in `research/feedback/`, and the existing `manuscript/outline.md`, `manuscript/logic-map.md`, and manifest.
2. If the research question or the main contribution is not settled, say so and offer `idea-deepening` or `research-planning`; never invent the claim the paper makes.

## Step 2: Build the argument

3. State the main claim in one or two sentences, with its support: the result records and evidence notes behind it, and their status (checked, observed, or still missing).
4. List the supporting claims in the order the argument needs them. For each: the evidence it needs, what exists (with links), and what is missing. A claim whose support is missing stays in the outline as a gap; it is never presented as a finding.
   Identify the steps from observation to interpretation, alternatives the evidence has not excluded, and claims that exceed or understate support. Make the contribution, its value to the relevant field, and its fit with the target venue explicit. Keep missing support as a gap, distinguish potential impact from demonstrated effects, and connect material limitations to the claims they affect. Offer a concrete way to strengthen the argument or obtain support; a different main claim remains a proposal for the researcher.
   Every paper used to support a claim or shape the manuscript's background, interpretation, or structure, including a paper underlying a linked result record, must link through its source ID to the original for that exact version in `references/originals/`. Unarchived search records can identify leads or evidence gaps, but abstracts, snippets, and service-only text do not support the outline.
   If a needed paper is not yet archived, use [reference-download](../reference-download/SKILL.md) for an authorized public original or [source-ingestion](../source-ingestion/SKILL.md) for a researcher-provided document before treating it as unavailable. Follow those skills' access, version-identity, and processing requirements. If acquisition is blocked, report the exact access or authorization gap and continue independent outline work without using that paper as support.
5. Fit the structure to the discipline, the article type, and the venue: use a fixed structure such as IMRaD only when the article type or the venue requires it or the researcher asks. Respect the venue's limits (length, required sections, abstract form) as recorded in its venue note, and name the source.

## Step 3: Map the sections

6. For each section: its file (one file per major section, for example `02-methods.md`, or a single file for a short paper), its title in the manuscript language, its purpose in the argument, its key content, the evidence and results it uses, the figures and tables with their planned labels (`fig:...`, `tbl:...`) and the form that suits each one's message (see the [figure guide](../research-code-setup/figure-guide.md)), and a target length when a limit applies.
7. List the gaps: evidence to obtain, results still to produce, sources to read, and decisions the researcher must make. Name the skill that would close each gap.

## Step 4: Confirm

8. The overall argument and structure is a major decision. Present the proposed structure with your recommendation and, when they help, one or two alternatives with their trade-offs; ask one question and wait. A clear instruction with a structure ("use the structure my coauthor suggested") confirms it within its scope.
9. After confirmation of the overall argument and structure, record that major decision with `constraint-maintenance`, then write the outline and logic map. Reuse a decision record that already confirms this structure and scope. When the structure came from a collaborator, record its adoption through `research-feedback`; the researcher's explicit instruction in step 8 is already confirmation and needs no second question.

## Step 5: Write the outline

10. Write `manuscript/outline.md` in English, with planned section titles in the manuscript language: the main claim and its support, the supporting claims with evidence status, the section map, the figure and table plan, the constraints with their sources, the gaps, and open questions. Keep text that the researcher wrote. Replace outdated parts; the outline states the current plan.
11. Replace the scaffold in `manuscript/logic-map.md` with the confirmed map in English, and remove the "No manuscript logic map yet" marker and unused placeholder nodes. Use a Mermaid `flowchart TD` to show how the question connects to the main claim, how local claims and checked or pending evidence lead through each inferential step, and how alternatives, contrary evidence, gaps, and limitations affect the conclusion. Group nodes by the manuscript's actual sections where useful. Label the real relationship on every edge; do not use an arrow that implies unsupported causality. Keep the whole-paper chain readable, and add a focused local flowchart in the same file only when one section's reasoning needs more detail. The map exposes gaps; it does not validate evidence.
12. The outline and logic map do not create or change section files. Drafting starts with `manuscript-writing`, which creates the files and lists them in the manifest. Never list `logic-map.md` in the manifest.

## Completion check

- Every claim in the outline has its evidence status, and missing support is a visible gap, not a finding.
- Every paper used as manuscript evidence or writing input has an archived original for its exact version; unarchived papers remain leads or gaps.
- The structure fits the discipline, article type, and venue limits, each with its source; no structure was forced.
- The structure was confirmed by the researcher before the outline was written as the plan.
- The outline holds no body text and is not listed in the manifest.
- The logic map reflects the confirmed argument, shows both whole-paper and section-level reasoning, marks evidence gaps and limits, and is not listed in the manifest.
