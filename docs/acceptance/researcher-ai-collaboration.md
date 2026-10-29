# Researcher–AI Collaboration: Review and Test Record

Date: 2026-10-30 (Asia/Tokyo). Scope: the maintainer's approved plan, “借鉴 AI Scientist，增强研究者与 AI 的协作”. Written review: the changed instructions cover the plan. Deterministic integration evidence is recorded below. This is not acceptance evidence for independent research, real manuscript readiness, or a complete guided run with a researcher.

## Inputs examined and concurrent work

Reviewed the adopted AGENTS.md, the approved plan in this conversation, [interaction specification](../agent-interaction.md), [collaboration design](../researcher-ai-collaboration.md), existing result and state READMEs, `research.py`, `status.py`, manuscript check/revision procedures, and the ten changed canonical skill entrypoints: `research-ideation`, `idea-deepening`, `research-planning`, `research-investigation`, `research-code-setup`, `manuscript-outline`, `manuscript-writing`, `manuscript-audit`, `manuscript-revision`, and `paper-hands-on`.

At the maintainer's request, the implementing agent read the local Claude Code session titled “集成开源仓库能力” and its writing-prompts fork. The writing/editing guides, style presets and reviewer-view work were preserved; only small collaboration additions were made to overlapping skill entrypoints. The main session was researching separately requested scored-review and model-recommendation skills at the last progress inspection. This extension neither implements nor prohibits them and does not claim them as available. No message was sent to that session. No existing work was reset or discarded.

## Requirement review

| Approved requirement | Implementation and review evidence | Limit |
| --- | --- | --- |
| Support the human researcher, not independent scientific selection | The guide outcome centers evidence, alternatives and the researcher's choices; idea and planning tasks prepare comparisons and recommendations. | Instruction review; no measured improvement to scientific judgment. |
| Ground questions in available material | Ideation/deepening use inspected comparisons, ambiguity, assumptions and counterevidence; no novelty score or binary verdict. Planning explains what a method can and cannot establish. | Search quality is not evaluated by the synthetic cases. |
| Distinguish observation, interpretation and hypothesis | Investigation and computation return these distinctions with checks, negative evidence and limits; unexpected results trigger technical/source checks before a proposed scientific change. | The test narratives are scripted. |
| Continue routine authorized work toward the goal | Guide goal/scope/completion conditions and handoffs; audit/write follow through when correction/recheck was already requested. Planning-only and audit-only boundaries remain. | Model compliance and question frequency remain unverified. |
| Major choices wait; independent work can proceed | Guide and revision rules block dependent scientific changes only; re-use prior confirmations. | No test framework impersonates real consent. |
| Writing follows the confirmed argument and author's expression | Writing reads current text, separates claims from evidence, maintains existing outline/result support links and rechecks earlier findings; revision preserves its existing conflict gate. | Semantic fidelity still requires inspection; a resolving key is insufficient. |
| Report affected prose, figures and checks when results change | `research.py check` reports existing `Used by` text on stale inputs/outputs/code, with a missing-map warning; audit instructions include underlying sources/code in check inputs. | No inferred dependency graph or automatic rewriting. Recorded code folders can conservatively invalidate multiple results. |
| Resume from light existing records | State README and guide name goal/scope, artifact/check links, exact pending choice/blocker, next action; status/checks read actual files. | Fresh CLI processes are tested; a fresh model session is not. |
| Bound technical repairs and retain failures | Guide/computation instructions limit repairs to two per failing action, earlier stop for repeated failure without progress; existing run logs remain separate. | One repair is exercised by the integration case; the retry ceiling is a prompt instruction, not a new scheduler. |
| Preserve negative findings and evidence gaps | Zero-change computation, conflicting documentary records, and visible unsupported causal extension are retained in the cases. | Assertions check these fixture artifacts, not how a model generates them. |
| No new engine, services, runtime dependencies or researcher content | No workflow database or additional capability; fixtures are generated in temporary workspaces; template project/state remain uninitialized. | Initially no package was installed. In the authorized follow-up, PyYAML was installed only in the ignored local validation environment; ordinary workspace scripts still use the standard library. |

## Executed deterministic scenarios

The [new collaboration tests](../../scripts/tests/test_collaboration_path.py) generate their own original, labeled, rights-cleared fixtures in temporary workspaces. They copy only the template record areas needed, never this acceptance folder or the agent's conversation/memory. No network provider, real publication, private data, credential, or new conversion route is used.

**Computational path.** A fixture question asks for mean paired change, with a descriptive method and a separate pending causal-study choice. The first analysis intentionally fails; one parser repair produces a distinct successful run and preserves the original failed run/log. Pairs `(1,2)`, `(2,1)`, `(3,3)` give mean change `0`, verified against the JSON output and the generated SVG. The result narrative distinguishes that observation from interpretation and an untested population hypothesis. It hands off to a paragraph, figure and audit with an open causal-evidence marker. A new CLI process reports the existing result and gap without adding runs or changing the pending plan. A staged wording change is refused after an author edit, then succeeds after explicit scripted reconciliation, retaining that edit. A follow-up audit keeps the research gap open. Changing an input then flags the recorded prose and figure uses and makes audits stale.

**Documentary path.** Two original Markdown records say respectively that `2 of 4` north entries and `0 of 4` south entries mention shade. Both are imported through the existing direct Markdown route, with inspected sections and access scope recorded in notes. A documentary result compares the mentions while keeping climate and reporting-practice explanations as untested alternatives. A draft contains the supported comparison and an open cooling-effectiveness marker. The initial audit identifies the missing evidence; a scripted local correction replaces the proposed efficacy extension with an explicit limitation, and a follow-up audit checks both sources. A later extraction change makes the result and its audits stale while originals and author text remain unchanged. No `code/` folder is created.

The [research regression tests](../../scripts/tests/test_research.py) additionally demonstrate the previously missing code-freshness check: changing or deleting recorded `code/src` used to leave the checked result valid; it now produces stale status and reports the recorded prose/exhibit/check uses, without editing the result. An unreadable or failed linked run is reported as a problem instead of accepted as a checked observation.

## Behavioral observations, kept separate

The implementing agent reviewed the two scenario traces against the revised instructions. For the zero-change case, the supported statement is a descriptive mean of zero, not intervention failure in a population or a reason to change the agreed method. For the source comparison, different word mentions do not establish cooling efficacy, and either proposed explanation remains untested. The corresponding scripted prose and follow-up findings preserve these distinctions. This is an informed, non-blind walkthrough by the implementer, not independent behavioral testing.

The real maintainer interaction also supplied the design boundary: the user redirected the earlier automation-centered proposal toward human research assistance and then approved the replacement plan. During implementation the user identified concurrent Claude Code work; the agent inspected it and preserved its additions. These observations concern this maintenance session, not a scientific collaboration trial.

Not observed: a model independently applying all revised skills to unfamiliar research material; a researcher making the synthetic study's choices; an actual pause/resume across model sessions; measured clerical time or avoidable-question reduction; comprehensive STE compliance; Windows behavior. These remain explicit limits, rather than positive results inferred from written procedures or unit tests. The deterministic path does not establish novelty, publishability, author approval or acceptance prospects.

## Verification commands

Run from the workspace root with Python 3.14.4 on macOS/Apple Silicon. All script dependencies for the added tests are in the standard library.

| Check | Observed result |
| --- | --- |
| `python3 -m unittest discover -s scripts/tests -p test_collaboration_path.py -v` | 2 tests passed. |
| `python3 -m unittest discover -s scripts/tests -p test_research.py` | 17 tests passed, including the two added regression cases. |
| `python3 -m unittest discover -s scripts/tests -v` | 196 tests passed in 103.503 seconds. |
| `python3 scripts/sync_skills.py` then `--check` | 10 canonical entrypoint changes mirrored; 34 packages match. |
| `python3 scripts/check_capabilities.py` | Availability table matches existing skills. |
| `python3 scripts/check_readmes.py` | 105 project directories passed. |
| `python3 scripts/check_requirements.py` | Writing-rule forms passed; no project requirement was invented. |
| `git diff --check` | No whitespace errors. |
| Generic `skill-creator/scripts/quick_validate.py` | Initially blocked by missing PyYAML. Authorized follow-up: all 34 existing packages passed using `.venv/bin/python`, Python 3.14.4 and PyYAML 6.0.3. Concurrent new skills were outside this submission scope. |

## Authorized validation and save follow-up (2026-10-30)

The maintainer explicitly authorized installing the missing dependency, rechecking, repairing issues and committing this work. Following the [official PyYAML installation instructions](https://pyyaml.org/wiki/PyYAMLDocumentation), PyYAML 6.0.3 was installed in the workspace's ignored `.venv/`, with Python 3.14.4. The system interpreter, document tools and research environments were not changed. The environment was inspected before and after installation.

The generic validator passed for all 34 tracked canonical skill packages. Content review found a conflict between the new statement that confirmation is not empirical evidence and the older writing step that allowed any researcher-confirmed statement to support a finding. The writing step and completion check now distinguish author accounts of their own choices/procedures from empirical findings, which still require checked evidence. Its Claude Code mirror was regenerated.

The complete script suite was rerun with `.venv/bin/python`: all 196 tests passed in 102.733 seconds. The final scope snapshot passed the README check (105 directories), capability-table check, writing-rule check, and mirror check (34 packages). Git whitespace checking also passed.

The concurrent agent began registering `mock-review` and `model-selection` while checks ran. A first snapshot mixed its edited capability table with the older 34-package set and correctly failed the capability check. The final scope snapshot is constructed from Git HEAD plus only the 35 approved collaboration files; it excludes the concurrent agent's packages, table and other changes. Its capability check passes. This transient mixed snapshot is not treated as a defect in either agent's capability.

Validation and commit cover the collaboration work only. The local environment and verification snapshots are ignored and are not committed. Remaining concurrent edits are left in place for their owning session.

Further behavioral evaluation can use these two kinds of material with fresh, unseen fixtures and genuine researcher choices. It must keep consent boundaries and observations distinct from scripted inputs, and must not read this expected-outcome record as task instructions.
