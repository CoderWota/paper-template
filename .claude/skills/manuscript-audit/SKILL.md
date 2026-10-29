---
name: manuscript-audit
description: Use when the researcher asks to review, check, critique, or audit the manuscript or a section, to find unsupported claims, contradictions, weak arguments, inconsistent terms, citation problems, formulaic wording, or violations of their writing rules, or wants a final check before sharing or submitting, or a reviewer's view of the paper. Examines argument, evidence and claim support, results, terminology, confirmed rules, language, style patterns, conventions, and known venue limits as separate checks, and returns prioritized findings linked to exact passages and evidence, recorded with the inputs they examined, without a score and without editing the text unless asked.
---

# Manuscript audit

Outcome: a prioritized list of findings, each tied to an exact passage and to the evidence or rule behind it, with a suggested remedy; a report in `outputs/checks/` and a check record that names the inputs examined, so that the result becomes stale when they change. The manuscript is not edited unless the researcher asks.

## Step 1: Set the scope

1. Name what is audited: the whole manuscript or named sections, and which checks (by default all of step 2). Read `requirements/project.md`, `requirements/writing.md`, `manuscript/outline.md`, the manifest and the section files in scope, the bibliography, the evidence notes and result records the text relies on, and the venue note when a target is set.
2. Run `python scripts/manuscript.py checks`. A recorded check whose inputs changed is stale: do not reuse its result.
3. A final check, requested for a text that has already been revised, reports only blocking problems: statements that contradict each other, a key term that changes without explanation, a sentence whose meaning is unclear or wrong, and numbers that disagree between passages. When there are none, say so plainly. Offer the minor findings separately instead of listing them, and record the scope as a final check.

## Step 2: Examine, one check at a time

4. **Mechanics.** `python scripts/manuscript.py check` (labels, citation keys, images, math, hand-numbered references, open `[TODO: ...]` markers) and `python scripts/literature.py audit-bibliography` (keys linked to archived sources). A key that resolves is not support.
5. **Argument.** Does the text make the main claim of the outline? Are steps missing, claims stronger than their support, alternatives or limitations ignored? Do sections contradict each other, for example a number in the abstract that differs from the results, or a conclusion that the methods cannot support?
6. **Support.** For each substantive claim: the cited source's passage, checked with `literature-and-evidence` (support, contradiction, qualification, or not checked), or the result record and its status. `python scripts/research.py check` reports stale results; a stale or unchecked result does not support a finding.
7. **Terminology and rules.** Each active rule in `requirements/writing.md`, applied within its scope; the terminology table; consistency of terms across sections.
8. **Language.** The manuscript language throughout, with the confirmed exceptions; unintended mixing; clarity.
9. **Style patterns.** The [pattern families](../natural-prose/patterns.md) and the list for the manuscript language beside them. Report a strong pattern, or a cluster of weak ones, as a minor finding, and as important when it misstates the evidence, such as "significant" without a test or a claim of novelty without a search. A pattern is never evidence about who wrote the text.
10. **Venue limits**, when a target is set: length (`python scripts/manuscript.py assemble` prints word counts), required sections, the abstract form, and the AI policy. A full readiness assessment is `submission-readiness`.

## Step 3: Report the findings

11. For each finding give: its priority (blocking, important, or minor), the location (file and line, with a short quotation), what is wrong, the evidence or rule behind the finding (with locators), and a suggested remedy. A missing source or result is reported as a research gap; never repair it with an invented citation or number.
12. When the researcher asks for a reviewer's view, follow [the reviewer's view](reviewer-view.md): its inputs, its checks (including the optional reader check), and its report. The report gives no score, rating, or chance of acceptance.
13. Write the report in the interaction language to `outputs/checks/<date>-audit-<scope>.md`, then record it:

    ```text
    python scripts/manuscript.py record-check --name "Audit of <scope>" --kind audit --input <each audited section> --input references/bibliography.bib [--input <evidence notes and result records used>] --result passed|findings|failed --summary "..." --scope "<checks made>" --report outputs/checks/<file>.md
    ```

14. Tell the researcher the most important findings first, with links. For an audit-only request, ask which to address. If correction and rechecking are already authorized, continue through `manuscript-writing`, `natural-prose` for formulaic wording, or `manuscript-revision` for structural ones within its confirmation requirements. Keep the researcher's current edits, and pause only the work dependent on a new scientific choice.

For a follow-up audit, identify each prior finding by its existing heading or location and link the actual change and the fresh evidence/check, or explain why it remains open. Reinspect the passage and support rather than accepting a completion label. Include the source inputs and run code needed to detect upstream changes in the check record. A model score, an accept/reject recommendation, or agreement between models is not scientific verification.

## Completion check

- The scope and the checks made are stated, and stale earlier results were not reused.
- Each finding points to an exact passage and to its evidence or rule; support and citation resolution were checked separately.
- Nothing was invented to close a gap, and the text was not edited without a request.
- The report exists and its check record names the inputs examined.
- A reviewer's view gives no score, rating, or chance of acceptance.
