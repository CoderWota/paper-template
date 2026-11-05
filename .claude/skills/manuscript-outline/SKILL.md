---
name: manuscript-outline
description: Structure a manuscript and map its argument with Mermaid. Use when the researcher wants an evidence-linked outline for a new paper or needs to connect claims, results, and sections.
---

# Manuscript outline

Outcome: `manuscript/outline.md` and `manuscript/logic-map.md`: a researcher-confirmed plan of the argument and sections, plus an internal Mermaid flowchart that makes the paper-level argument and local reasoning visible. Neither file is assembled into the manuscript.

## Step 1: Gather the inputs

1. Read `requirements/project.md` (question, contribution, article type, languages, target venue), `requirements/writing.md`, [argument and impact guidance](../manuscript-writing/argument-and-impact.md), `research/plan.md`, `research/results/index.md` (with each result's status), the evidence notes and search records that the plan links, the selected idea note, the venue note in `research/venues/` when a target is set, adopted suggestions in `research/feedback/`, and the existing `manuscript/outline.md`, `manuscript/logic-map.md`, and manifest.
2. If the research question or the main contribution is not settled, say so and offer `idea-deepening` or `research-planning`; never invent the claim the paper makes.

Ready to build the argument when the question and contribution are settled and the linked evidence is available or its access gap is clear.

## Step 2: Build the argument

3. State the main claim in one or two sentences, with its support: the result records and evidence notes behind it, and their status (checked, observed, unchecked, or missing).
4. List the supporting claims in the order the argument needs them. For each: the evidence it needs, what exists (with links), and what is missing. A claim whose support is missing stays in the outline as a gap; it is never presented as a finding.
   Identify the steps from observation to interpretation, alternatives the evidence has not excluded, and claims that exceed or understate support. Make the contribution, its value to the relevant field, and its fit with the target venue explicit. Keep missing support as a gap, distinguish potential impact from demonstrated effects, and connect material limitations to the claims they affect. Offer a concrete way to strengthen the argument or obtain support; a different main claim remains a proposal for the researcher.
   Every paper used to support a claim or shape the manuscript's background, interpretation, or structure, including a paper underlying a linked result record, must link through its source ID to the original for that exact version in `references/originals/`. Unarchived search records can identify leads or evidence gaps, but abstracts, snippets, and service-only text do not support the outline.
   If a needed paper is not yet archived, use [reference-download](../reference-download/SKILL.md) for an authorized public original or [source-ingestion](../source-ingestion/SKILL.md) for a researcher-provided document before treating it as unavailable. Follow those skills' access, version-identity, and processing requirements. If acquisition is blocked, report the exact access or authorization gap and continue independent outline work without using that paper as support.
5. Fit the structure to the discipline, the article type, and the venue: use a fixed structure such as IMRaD only when the article type or the venue requires it or the researcher asks. Respect the venue's limits (length, required sections, abstract form) as recorded in its venue note, and name the source.

Done when the main claim and every supporting claim have an evidence status and a source, result, or visible gap; the structure follows the paper type and cited venue requirements.

## Step 3: Map the sections

6. For each section: its file (one file per major section, for example `02-methods.md`, or a single file for a short paper), its title in the manuscript language, its purpose in the argument, its key content, the evidence and results it uses, the figures and tables with their planned labels (`fig:...`, `tbl:...`) and the form that suits each one's message (see the [figure guide](../research-code-setup/figure-guide.md)), and a target length when a limit applies.
7. List the gaps: evidence to obtain, results still to produce, sources to read, and decisions the researcher must make. Name the skill that would close each gap.

Done when every section has a role in the argument, its material claims and support are linked, and remaining gaps have an owner or next step.

## Step 4: Confirm

8. The overall argument and structure is a major decision. Present the proposed structure with your recommendation and, when they help, one or two alternatives with their trade-offs; ask one question and wait. A clear instruction with a structure ("use the structure my coauthor suggested") confirms it within its scope.
9. After confirmation of the overall argument and structure, record that major decision with `constraint-maintenance`, then write the outline and logic map. Reuse a decision record that already confirms this structure and scope. When the structure came from a collaborator, record its adoption through `research-feedback`; the researcher's explicit instruction in step 8 is already confirmation and needs no second question.

Done when the researcher has confirmed the argument and structure and the required decision record exists. If confirmation is pending, stop before writing either file.

## Step 5: Write the outline

10. Write `manuscript/outline.md` in English, with planned section titles in the manuscript language: the main claim and its support, the supporting claims with evidence status, the section map, the figure and table plan, the constraints with their sources, the gaps, and open questions. Keep text that the researcher wrote. Replace outdated parts; the outline states the current plan.
11. Replace the scaffold in `manuscript/logic-map.md` with the confirmed map in English. Remove the "No manuscript logic map yet" marker and unused placeholder nodes. Follow the [internal logic map guide](../../../docs/logic-map-guide.md) for evidence status, labeled edges, local reasoning, alternatives, limitations, and the traceability check.
12. The outline and logic map do not create or change section files. Drafting starts with `manuscript-writing`, which creates the files and lists them in the manifest. Never list `logic-map.md` in the manifest.

Done when the outline and map match the confirmed argument, each argumentative section can be traced to the paper-level claim or is marked as local context, every evidence node is marked checked, observed, unchecked, or missing, and neither file appears in the manifest.

## Completion check

- The question, contribution, and structure are confirmed; no scientific claim was invented or changed.
- Each material claim has an evidence link and status, or an explicit gap; no unchecked source is treated as checked support.
- Every paper used as support has an archived original for its exact version.
- Each argumentative section's local reasoning traces to the whole-paper claim or is marked as local context.
- The outline and logic map match; the map follows the guide's traceability check and is absent from the manifest.
