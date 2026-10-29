# Researcher–AI Collaboration

Status: implemented in the existing skill instructions on 2026-10-30 under the maintainer's approved plan. Script checks and behavioral observations have different evidentiary limits; see the [review and test record](acceptance/researcher-ai-collaboration.md). This is a framework change, not a research project's initialization or a scientific decision record.

## Confirmed purpose

The maintainer clarified: “我们不追求ai独立完成研究，应该思考借鉴如何让ai更好辅助人类研究者完成研究和论文写作这件事”. The approved plan states: “研究者主导研究方向、学术判断和最终表达。AI 主动提供证据、比较方案、提出质疑，并承担授权范围内的研究支持和技术工作。” It also authorizes “连续完成约定目标，遇到需要研究者判断的重大选择时再暂停”.

These instructions replace the guided path's default of finishing one step and proposing the next. They do not change the confirmation rules for scientific choices, expand any individual request, or prescribe a research discipline. A goal may be an analysis, an explanation, a paragraph, or a larger manuscript task. Learning remains optional.

## Collaboration through the existing tasks

| Research need | Agent contribution | Researcher judgment | Handoff and completion |
| --- | --- | --- | --- |
| Formulate a question | Clarify ambiguities; compare genuinely different directions against inspected material; name assumptions, contrary evidence, and a useful next check. | Which question or direction to pursue. | Retained idea note and inspected comparisons; unsettled hypotheses remain explicit. |
| Assess a contribution | Explain overlap and differences from prior work with locators and search limits. | Whether the difference matters for the intended contribution. | Source notes and scoped comparison, without a novelty score or binary novelty verdict. |
| Choose an approach | Explain what alternative methods can answer, their inputs, checks, limits, and trade-offs; recommend an approach. | Consequential method and material choices. | Existing plan items link their prerequisites, expected artifacts, checks, and confirmed decisions. |
| Investigate and interpret | Carry out authorized computation or source inquiry; inspect errors and contrary findings; separate observation, interpretation, and hypothesis. | Whether to retain, narrow, or change a scientific explanation or claim. | Inspectable outputs and result records, including checks and negative findings; changed claims stay proposed until confirmed. |
| Build the argument and write | Connect the author's argument to evidence; identify missing reasoning and overstatement; draft or edit within scope and applicable policy. | Main claim, structure, final expression, and choices that change them. | Current text, outline/evidence links and result `Used by` references; open support remains visible. |
| Review and revise | Tie each finding to a passage, evidence, remedy, actual change, and fresh check. | Scientific changes and unresolved trade-offs. | Existing audit, change map, and check records distinguish addressed from unresolved findings. |

The agent first resolves discoverable facts from available material. It asks one substantive question when a judgment is needed. Human leadership does not require manual dispatch of each stage or technical-file maintenance.

## Scope, recovery, and dependencies

`paper-hands-on` coordinates the requested goal through specialist skills without copying their procedures. Task completion requires usable artifacts and relevant checks, not an exit code, an existing file, or the end of a skill. Audit-only and planning-only requests remain bounded; an audit-and-repair request need not ask again for its already-authorized corrections.

Use the current plan, source notes, results, outline, audit records and revision maps as the durable record. Keep `state/current.md` short: agreed goal and scope, completed work and check links, the precise pending question or blocker, and next action. Store no inferred preferences. There is no new workflow engine, task database, or `workflow.json`.

On resumption, inspect the actual current artifacts and relevant freshness checks before reuse. A pending scientific decision blocks dependent work; other authorized work can continue. Preserve intervening author edits and reconcile them before a staged revision is applied. An unavailable source or physical experiment is an explicit dependency, not a reason to fabricate a result.

Keep technical failure logs and make at most two repair attempts for the failing action within the existing method and permissions; stop earlier when the same failure repeats without progress. Record attempts in the owning work item or result, with a short link from state. A substantive negative finding is not a technical error. A new method, service, resource scope or consequential cost needs its existing confirmation gate.

Use the existing outline's claim/evidence links, source locators and result `Used by` field to identify affected passages, figures, tables and checks. The script checks recorded input/output hashes and recorded run code, and reports the recorded uses when stale. It does not infer all scientific dependencies or judge semantic support. Missing links require inspection, not an assertion that the map is complete. Audit records must include relevant underlying sources and code as inputs, not just the Markdown result note. Do not refresh a checksum to conceal changed evidence.

## What transfers from AI Scientist

The reference repository was inspected on 2026-10-29: [main orchestration](https://github.com/SakanaAI/AI-Scientist/blob/main/launch_scientist.py), [idea generation and prior-work search](https://github.com/SakanaAI/AI-Scientist/blob/main/ai_scientist/generate_ideas.py), [experiment execution](https://github.com/SakanaAI/AI-Scientist/blob/main/ai_scientist/perform_experiments.py), [writing](https://github.com/SakanaAI/AI-Scientist/blob/main/ai_scientist/perform_writeup.py), and [review](https://github.com/SakanaAI/AI-Scientist/blob/main/ai_scientist/perform_review.py). The inspected design connects results and notes to writing, bounds some execution/repair loops, and can revise and review a writeup. These are design references, not evidence of scientific validity or a benchmark for this workspace.

Here those ideas support inspectable handoffs and informed human discussion. We do not import their code, prompts, dependencies, ML experiment templates, autonomous scientific selection, or score aggregation. The ordinary audit remains qualitative. A separately requested scored-review capability is a separate task; neither a score nor an accept/reject recommendation establishes scientific verification or an acceptance probability.

## Evaluation

Judge assistance by whether questions and assumptions become clearer, important reasoning is tested, evidence and uncertainty are intelligible, expression remains faithful, and clerical effort is reduced. Count automated stages only as an auxiliary observation.

Run bounded, original synthetic computational and documentary cases. Keep deterministic assertions, the implementing agent's own walkthrough, independent behavioral testing, and real researcher experience separate. A scripted decision quote is a fixture, not real consent. A script cannot prove that a model asks good questions or respects author intent. Do not infer novelty, submission readiness, publication success, platform coverage, or measured time savings from these tests.
