---
name: manuscript-outline
description: Structure a manuscript and maintain its Mermaid argument framework. Use when connecting premises, evidence, author analysis, inference, judgments, and sections.
---

# Manuscript outline

Outcome: an argument and section plan in `outline.md` and an internal Mermaid framework in `logic-map.md`, or a descriptive refresh of an existing draft's framework. New plans require researcher confirmation; routine reconstruction and synchronization preserve the current scope. The map includes a concise reasoning register and a recorded input version. Neither file is assembled into the manuscript.

Use `manuscript/` by default. A revision handoff may select `revisions/<revision-id>/candidate/`; write the outline, map, register, and synchronization record there. Paths below refer to that selected target. At entry, inspect `python scripts/manuscript.py logic-status [--revision-id ID] --json` and reconcile direct author edits before updating the map.

## Step 1: Gather the inputs

1. Read `requirements/project.md` (question, contribution, article type, languages, target venue), `requirements/writing.md`, [argument and impact guidance](../manuscript-writing/argument-and-impact.md), `research/plan.md`, `research/results/index.md` (with each result's status), the evidence notes and search records that the plan links, the selected idea note, the venue note in `research/venues/` when a target is set, adopted suggestions in `research/feedback/`, and the existing `manuscript/outline.md`, `manuscript/logic-map.md`, and manifest.
2. For a new outline, if the question or contribution is unsettled, use `idea-deepening` or `research-planning` for that choice. For a descriptive refresh of existing text, mark an unclear question, claim, or missing whole-paper context and continue mapping what is present; do not invent or endorse a claim to fill the gap.

Ready when the inputs needed for the selected task are available or their gaps are explicit. A new plan needs a settled question and contribution; a bounded descriptive map may retain open whole-paper links.

## Step 2: Build the argument

3. State the main claim in one or two sentences and identify how it is supported: empirical evidence or results, an explicit derivation or analysis, a reasoned interpretation or judgment, or a combination. Distinguish the basis of the premises from the adequacy of the reasoning and the author's adoption of the claim.
4. List the supporting claims in the order the argument needs them. For each, state the premises, assumptions, analysis or inferential step, relevant criteria and conditions, and resulting claim. Link external premises or observations to evidence; original reasoning can justify a derived claim without a separate citation for that step. Mark a missing premise, weak inference, unchecked observation, or unresolved judgment explicitly rather than inventing a bridge.
   Identify the steps from observation to interpretation, alternatives the evidence has not excluded, and claims that exceed or understate support. Make the contribution, its value to the relevant field, and its fit with the target venue explicit. Keep missing support as a gap, distinguish potential impact from demonstrated effects, and connect material limitations to the claims they affect. Offer a concrete way to strengthen the argument or obtain support; a different main claim remains a proposal for the researcher.
   Every paper used to support a claim or shape the manuscript's background, interpretation, or structure, including a paper underlying a linked result record, must link through its source ID to the original for that exact version in `references/originals/`. Unarchived search records can identify leads or evidence gaps, but abstracts, snippets, and service-only text do not support the outline.
   If a needed paper is not yet archived, use [reference-download](../reference-download/SKILL.md) for an authorized public original or [source-ingestion](../source-ingestion/SKILL.md) for a researcher-provided document before treating it as unavailable. Follow those skills' access, version-identity, and processing requirements. If acquisition is blocked, report the exact access or authorization gap and continue independent outline work without using that paper as support.
5. Fit the structure to the discipline, the article type, and the venue: use a fixed structure such as IMRaD only when the article type or the venue requires it or the researcher asks. Respect the venue's limits (length, required sections, abstract form) as recorded in its venue note, and name the source.

Done when each material claim has an inspectable empirical or analytical support path, or a named gap, and the structure follows the paper type and applicable venue requirements.

## Step 3: Map the sections

6. For each section: its file (one file per major section, for example `02-methods.md`, or a single file for a short paper), its title in the manuscript language, its purpose in the argument, its key content, the evidence, results, analytical steps, or judgments it uses, the figures and tables with their planned labels (`fig:...`, `tbl:...`) and the form that suits each one's message (see the [figure guide](../research-code-setup/figure-guide.md)), and a target length when a limit applies.
7. List the gaps: evidence to obtain, results or analyses still to produce, sources to read, inferences to examine, and assumptions, criteria, or other choices the researcher must decide. Name the skill that would close each gap.

Done when every section has a role in the argument, its material claims and support are linked, and remaining gaps have an owner or next step.

## Step 4: Confirm

8. A proposed new or changed overall argument or structure is a major decision. Present it with your recommendation and useful alternatives; ask one question and wait unless the existing instruction already confirms that choice. A descriptive map of current text or a routine synchronization needs no new confirmation; distinguish current draft assertions from adopted plans.
9. Record a newly confirmed major decision with `constraint-maintenance`; reuse an existing decision that covers the scope. For an adopted collaborator structure, use `research-feedback`. Routine synchronization creates no new scientific decision record.

Done when any new scientific choice is confirmed and recorded, or the work is explicitly a descriptive refresh within the existing scope. A pending choice blocks only the proposed new plan; current-draft reasoning and its open issues can still be represented.

## Step 5: Write the outline

10. Write or update the selected target's `outline.md` within scope in English, with planned section titles in the manuscript language: the main claim and its support, the supporting claims with their premise basis and reasoning review, the section map, the figure and table plan, the constraints with their sources, the gaps, and open questions. Keep text that the researcher wrote. For a map-only refresh, preserve the confirmed outline and show any divergence between its plan and the current draft in the framework; do not silently adopt a new plan.
11. Replace the scaffold in the target's `logic-map.md` with the argument graph and reasoning register in English. Remove the "No manuscript logic map yet" marker and unused placeholders. Follow the [logic map guide](../../../docs/logic-map-guide.md) to expose premises, analysis, inference, judgments, criteria, conditions, alternatives, and gaps. Distinguish a confirmed plan from current draft assertions. Complete the guide's semantic synchronization loop and run `logic-record [--revision-id ID] --input <each shared dependency>` after comparing the files; verify `logic-status` is current.
12. The outline and logic map do not create or change section files. Drafting starts with `manuscript-writing`, which creates the files and lists them in the manifest. Never list `logic-map.md` in the manifest.

Done when the framework faithfully represents the selected plan or draft and marks any divergence from the confirmed outline, each argumentative section can be traced to the paper-level claim or is marked as local context, premise basis and reasoning review are stated separately, synchronization is current, and neither file appears in the manifest.

## Completion check

- New planned choices are confirmed; a descriptive reconstruction is labeled as current-draft content, with uncertainty visible. Routine updates required no repeated approval.
- Each material claim has an evidence or reasoned argument path, or an explicit gap. Original deductions, analyses, and judgments are represented with their premises and conditions; an unchecked empirical premise is not treated as established.
- Every paper used as support has an archived original for its exact version.
- Each argumentative section's local reasoning traces to the whole-paper claim or is marked as local context.
- The target outline, graph, and register match the authorized plan or selected draft; the guide's checks were made, `logic-status` is current, and internal files are absent from the manifest.
