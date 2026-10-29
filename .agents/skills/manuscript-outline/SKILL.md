---
name: manuscript-outline
description: Use when the researcher asks how to structure the paper, wants an outline or section plan, asks what each section should argue, or wants the argument reorganized around a question or a target venue. Builds the main claim and the supporting argument from the confirmed question, actual evidence and results, confirmed requirements, and the venue's article type and limits, maps sections, figures, and tables with their evidence and gaps, and proposes the structure for the researcher to confirm without forcing a fixed article structure.
---

# Manuscript outline

Outcome: `manuscript/outline.md`, a researcher-reviewable plan of the argument and the sections: the main claim, the supporting claims in order with the evidence each needs and its status, each section's purpose and content, planned figures and tables with their labels, the constraints that apply, and the gaps. The outline guides writing; it is never assembled into the manuscript.

## Step 1: Gather the inputs

1. Read `requirements/project.md` (question, contribution, article type, languages, target venue), `requirements/writing.md`, `research/plan.md`, `research/results/index.md` (with each result's status), the evidence notes and search records that the plan links, the selected idea note, the venue note in `research/venues/` when a target is set, adopted suggestions in `research/feedback/`, and the existing `manuscript/outline.md` and manifest.
2. If the research question or the main contribution is not settled, say so and offer `idea-deepening` or `research-planning`; never invent the claim the paper makes.

## Step 2: Build the argument

3. State the main claim in one or two sentences, with its support: the result records and evidence notes behind it, and their status (checked, observed, or still missing).
4. List the supporting claims in the order the argument needs them. For each: the evidence it needs, what exists (with links), and what is missing. A claim whose support is missing stays in the outline as a gap; it is never presented as a finding.
5. Fit the structure to the discipline, the article type, and the venue: use a fixed structure such as IMRaD only when the article type or the venue requires it or the researcher asks. Respect the venue's limits (length, required sections, abstract form) as recorded in its venue note, and name the source.

## Step 3: Map the sections

6. For each section: its file (one file per major section, for example `02-methods.md`, or a single file for a short paper), its title in the manuscript language, its purpose in the argument, its key content, the evidence and results it uses, the figures and tables with their planned labels (`fig:...`, `tbl:...`) and the form that suits each one's message (see the [figure guide](../research-code-setup/figure-guide.md)), and a target length when a limit applies.
7. List the gaps: evidence to obtain, results still to produce, sources to read, and decisions the researcher must make. Name the skill that would close each gap.

## Step 4: Confirm

8. The overall argument and structure is a major decision. Present the proposed structure with your recommendation and, when they help, one or two alternatives with their trade-offs; ask one question and wait. A clear instruction with a structure ("use the structure my coauthor suggested") confirms it within its scope.
9. After a clear yes, write the outline. When the choice was consequential, for example between two argument structures or a structure that departs from the venue's usual form, record a decision with `constraint-maintenance`. A collaborator's suggested structure is adopted only through `research-feedback`.

## Step 5: Write the outline

10. Write `manuscript/outline.md` in the interaction language, with planned section titles in the manuscript language: the main claim and its support, the supporting claims with evidence status, the section map, the figure and table plan, the constraints with their sources, the gaps, and open questions. Keep text that the researcher wrote. Replace outdated parts; the outline states the current plan.
11. The outline does not create or change section files. Drafting starts with `manuscript-writing`, which creates the files and lists them in the manifest.

## Completion check

- Every claim in the outline has its evidence status, and missing support is a visible gap, not a finding.
- The structure fits the discipline, article type, and venue limits, each with its source; no structure was forced.
- The structure was confirmed by the researcher before the outline was written as the plan.
- The outline holds no body text and is not listed in the manifest.
