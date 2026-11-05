# Internal Argument and Logic Map

Maintain the paper's public argument in `manuscript/logic-map.md`: what the author starts from, what analysis or inference is performed, what judgment follows, and how that judgment advances the paper. Original deductions, analyses, interpretations, and reasoned judgments can be contributions in their own right. Represent unclear or disputed reasoning too, with its open issue, so the map can expose a gap.

## What belongs in the framework

| Role | What to capture | What to examine |
| --- | --- | --- |
| Question and main claim | The question, intended answer, and contribution | Does the conclusion answer the stated question within its scope? |
| Premise | An observation, source proposition, definition, theory, assumption, or scope condition | Where does it come from, is it accepted or contested, and when does it apply? |
| Analysis or inference | The operation or rule that connects premises to a result: deduction, induction, explanation, comparison, interpretation, or another stated method | Does this step follow, under which conditions, and what alternatives remain? |
| Intermediate conclusion or judgment | What the author derives or judges at this point | Is its strength and uncertainty warranted by the premises and reasoning? |
| Evaluative criterion | The standard, value, or priority used to judge, compare, or recommend | Is the criterion explicit and justified for this question? Would another criterion change the judgment? |
| Objection, alternative, or limit | Contrary evidence, competing explanations, counterexamples, and boundaries | Which premise, inference, or conclusion does it challenge or qualify? |

Include reasoning needed to assess the manuscript, rather than a transcript of private deliberation. Keep one readable Mermaid overview. Group local chains by actual sections; add a focused local graph in the same file when needed. A section may supply definitions, a method, or context for a later argument rather than make a separate claim. Do not impose a fixed article structure.

## Make the reasoning inspectable

Use stable node IDs and concise statements. In a short reasoning register below the graph, link each material inference or judgment to its premises, the analytical operation or warrant, its conditions or criteria, the resulting claim, and the manuscript location. Keep detailed source passages and derivations in their existing source notes or result records and link them. Update IDs in place when possible so authors can follow changes.

Arrows state a relation such as `is a premise of`, `supports`, `derives`, `interprets`, `evaluates by`, `challenges`, or `limits`. For a substantive inferential step, use an explicit analysis/inference node; a bare evidence-to-conclusion arrow can hide the very reasoning that needs review. Dashed edges identify a named unresolved dependency. Reading order and causation need their own justified relation labels.

Keep three judgments separate:

- **Basis:** evidence may be checked, observed but not checked, unchecked, or missing; a definition, assumption, or evaluative criterion is identified as such. Archive each external paper used as support and check its relevant passage. An unarchived citation is a source-access gap, not checked support.
- **Reasoning:** state whether the inference was examined, remains conditional, is disputed, or needs review, and say what was checked. A valid deduction preserves truth only if its premises hold. Induction needs a justified generalization; an explanatory inference needs alternatives considered; interpretation needs a defensible reading; an evaluative judgment needs explicit criteria. Do not force every argument into formal deduction.
- **Author status:** distinguish a confirmed plan, an assertion present in the current draft, and a proposed change awaiting the researcher's decision. A graph update does not turn a draft assertion into a verified finding or an adopted scientific choice.

An original derived claim need not have a separate citation when its stated premises and reasoning provide its support. Check empirical premises against evidence and check the derivation or judgment on its own terms. Author approval alone does not validate either. If reasoning is incomplete, show the missing premise, rule, analysis, or decision; do not invent a bridge to make the graph look coherent.

## Check the whole and the parts

1. Trace the main conclusion back through intermediate conclusions, analytical steps, premises, and any evidence or declared assumptions. Expose circular support and changes in meaning or scope.
2. For each material inference or judgment, inspect its premises, operation or warrant, conditions, criteria, and conclusion. Check the strength of the conclusion as well as whether the step is internally consistent.
3. Connect each section's contribution to the whole-paper argument. Check transitions between local chains, including assumptions introduced late, conclusions used before they are established, and conclusions that exceed the analysis.
4. Attach material alternatives, contrary evidence, counterexamples, and limits to the steps they affect. Distinguish a logical gap from an evidence gap and from a researcher decision.
5. Compare the graph and register with the selected draft and outline. During import, map what the draft actually says and mark ambiguous links. During planning, mark proposed claims as planned. Show planned-versus-written differences explicitly; a descriptive refresh does not silently change the confirmed plan. Report disagreements without rewriting the manuscript to fit the map.

## Synchronize automatically during writing

The writing agent maintains the map as part of the authorized writing task; the researcher need not request a separate update. Apply this to drafting, rewriting, shortening, translation, section moves, and changes to premises, analysis, judgments, scope, criteria, or support. Preserve the author's current map before a substantial rewrite and reconcile their direct edits. Update the affected graph and register, inspect their connections to the whole argument, and adjust the outline within the already authorized scope. A new scientific choice still needs the researcher's decision.

This loop applies to text saved to the maintained manuscript or its candidate. A detached passage returned only in the conversation does not change the active framework until incorporated. A bounded edit needs no project initialization or full-paper redesign: map the available local reasoning and show unknown whole-paper links. Describing the current argument is routine maintenance, not approval of a new scientific plan.

Use the selected target throughout: `manuscript/` by default, or `revisions/<revision-id>/candidate/` for a staged revision. The outline, graph, register, and synchronization record belong to that same target.

1. At entry, run `python scripts/manuscript.py logic-status [--revision-id ID] --json`. Inspect changed inputs, recorded dependencies, and any author edits to the map before writing.
2. After writing, compare the actual text changes with the reasoning framework and refresh affected premises, inference steps, judgments, locations, and open issues. For a spelling or format change with no logical effect, keep the graph unchanged after inspecting the change.
3. After that semantic comparison, run `python scripts/manuscript.py logic-record [--revision-id ID] --input <each new shared dependency>`. Inputs include source notes, exact source originals, result/derivation records, and other files whose change affects the argument. Existing dependencies are retained by default. When the argument no longer uses some, inspect the full list and use `--replace-inputs --input <each dependency still used>`; `--replace-inputs` alone deliberately clears that list. The command also tracks the target's manifest, section files, outline, metadata, project requirements, bibliography, and this guide automatically. Never run it merely to silence a stale status.
4. Confirm `logic-status` is current. If the refresh cannot be completed, leave its status pending and report the exact missing file, unresolved interpretation, or failed operation. A map can faithfully show open reasoning issues and still be synchronized; synchronization is not a finding that the argument is sound.

`logic-status` exits with 2 for a pending state; use the reported state and changed inputs to continue the refresh. `manuscript.py check` retains its source-convention exit status and reports map synchronization separately. If a synchronization record is invalid, preserve it, inspect its dependency list where readable, and recreate it with `--replace-inputs` only after comparing the map and actual inputs.

`logic-map.sync.json` records input fingerprints and the reviewed map version. `manuscript.py check` and project status expose missing, scaffold, unrecorded, stale, invalid, or current states. The record uses target-relative paths so a candidate and its map can be applied together. Scripts detect file changes; the agent performs the semantic update.

Freshness covers automatically tracked files and declared dependencies. An omitted dependency is a coverage gap rather than a change the script can detect; inspect the register and dependency list rather than assuming they are exhaustive.

Direct author edits made while the agent is idle are detected at the next project check or writing session. This workflow does not run a background model on every keystroke. A read-only audit reports staleness and logic findings without rewriting the map; an already authorized correction includes its refresh.

Keep the map and synchronization record outside the assembly manifest and publication output. Follow [Markdown and output conventions](markdown-and-export-conventions.md) for Mermaid syntax and rendering checks.
