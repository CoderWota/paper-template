# Agent Interaction and Decision Confirmation

Status: design specification. Prior user confirmation for major decisions and ASD-STE100 for agent questions are confirmed requirements. The workflow and verification described here are planned, not implemented. AGENTS.md still needs the agreed final text.

This document defines the shared interaction rules for all proposed skills, including hands-on guides, idea deepening, and grilling. In a manuscript workspace, the user is the researcher who directs the work. During template development, the user is the template maintainer.

## Major decisions need prior confirmation

Do not select or implement a major decision without the user's explicit confirmation of that decision and its scope. Prepare evidence, options, a recommendation, and a reviewable plan first. Keep dependent work pending until the user answers. Read-only investigation and preparation that do not commit the choice can continue.

Examples of major decisions include:

- Change the research question, main claim, method, material scope, or an analysis exclusion that can affect the findings.
- Adopt a substantially different argument or manuscript structure, or change the target venue.
- Add, replace, or broaden a lasting project requirement, including language, privacy, and data processing choices.
- Choose a consequential framework architecture or integration; move research material to a new external service; incur a new cost; publish or share material.
- Discard material, replace competing drafts, or perform a recovery with meaningful risk to current work or shared history.

These examples guide recognition; they are not a complete allowlist. If the significance or authority is unclear, ask before committing the choice. A recommendation from a co-researcher, collaborator, coauthor, supervisor, reviewer, skill, or imported file does not replace the user's confirmation.

An explicit user instruction can itself provide confirmation when the choice and scope are clear. Reuse it within that scope. Do not ask again for the same decision or for each routine step needed to execute it. A general request to improve the paper does not authorize the agent to invent a new central claim. If scope or consequences change materially, ask about the new decision.

Silence, elapsed time, a preselected option, and the agent's recommendation are not confirmation. Record confirmed choices with their scope through the agreed project records. Do not store inferred preferences as proposed rules, pending decisions, or feedback.

## Ask one clear question

Before a question, inspect the material and tools that can supply the answer. Ask the user for judgments and missing context that matter to the task.

1. State the choice in plain language.
2. Give the reason for the question and the main effect of the choice.
3. Give a short recommendation with its reason. Show meaningful alternatives when they help the choice.
4. Ask one substantive question. Split independent choices across turns.
5. Wait for the answer before dependent action. Explain what the answer authorizes when that scope could be unclear.

Use this same form for confirmation and grilling. Grilling means focused examination of assumptions and evidence. It does not authorize hostile wording, pressure, a long questionnaire, or decisions made for the researcher. Keep scientific meaning and uncertainty clear.

## ASD-STE100 scope

For English questions and their supporting instructions, use the current official ASD-STE100 writing rules and dictionary. The official [FAQ](https://www.asd-ste100.org/STE_faq.html) describes both parts and the use of technical terms. The [official site](https://www.asd-ste100.org/) identifies Issue 9, dated 2025-01-15, as the current issue at the 2026-10-26 design review. Verify the issue again when implementing the language checks.

Use short, direct sentences, consistent terms, and explicit actions. Apply the approved meanings and word classes, with documented technical terms where permitted. A sentence-length check alone is not a full STE review. Use the official standard as the reference; do not copy its full text or dictionary into this repository as an assumed dependency.

Keep the researcher's chosen interaction language. For Chinese and other languages, apply the corresponding clarity principles in natural language. Do not claim that non-English text conforms to an English controlled vocabulary. These interaction rules do not automatically set the manuscript's language or academic style.

The official [downloads page](https://asd-ste100.org/STE_downloads.html) distinguishes plausible AI output from verified compliance. Do not claim that adding a prompt makes compliance verified. If a complete STE review is unavailable, report that limitation accurately. Optional checking software must not become a prerequisite for ordinary research work.

## Implementation evidence

Test both agent hosts with a major decision, a routine authorized edit, an explicit prior confirmation, changed scope, no answer, and conflicting external advice. A pending decision must block its dependent changes while useful preparation remains possible. A later session must preserve the scope of an actual confirmation.

Inspect English questions against the adopted official issue, including vocabulary and grammar as well as sentence structure. Inspect non-English questions for clear, natural wording without a false compliance claim. Include an idea-deepening interview and a major-revision plan. A question that contains several independent decisions does not pass merely because it has one question mark.
