# Cross-Skill Consistency Review and Repairs

Date: 2026-10-30. Scope: the 36 canonical skills, their READMEs and linked resources, their generated Claude Code copies, and the relevant standing rules. This is a review of the current working copy, including concurrent template development. Existing work was retained; this task neither committed nor published it.

## Authority and criteria

The maintainer requested a review for logical conflicts, then authorized repairs: “你根据你的方式解决问题”. During the repairs, the maintainer clarified that impact language should allow some exaggeration for persuasive presentation: “impact也得允许夸张一些的描述”. This is a template behavior instruction, not a writing requirement for an initialized research project. No research requirements or project state were initialized.

The repair criteria follow the findings: preserve the meaning of style edits; isolate candidate work from the active manuscript; record confirmed major structures; reuse existing search scopes; distinguish new-paper setup from history repair; and disclose whether simulated reviewer perspectives have isolated contexts. The impact clarification requires accepting emphatic evaluations and ambitious prospects while checking concrete factual assertions and validation status.

## Findings and dispositions

| Finding | Repair | Evidence and limit |
| --- | --- | --- |
| Natural-prose examples silently lost claims, comparison strength, properties, or author positions, despite the skill's preservation rule | Revised all three language lists where needed. The first examples now illustrate removal of actual repetition; comparison and outlook claims stay in the impact examples; the rhythm examples retain independent properties and degree limits; letter examples retain substantive agreement and consideration; passive validation does not gain an invented actor | All 18 Before/After pairs were read for proposition preservation and passed through `check_edit.compare`. Token comparisons alone cannot establish semantic preservation |
| Impact and statistical language was treated too mechanically | Natural prose, its pattern families, manuscript audit, the results-writing guide, and impact assessment now allow persuasive contribution language and ambitious outlook. The check must identify a concrete unsupported assertion. Statistical significance is distinguished from qualitative importance or a large measured difference | English “paves the way”, Chinese “具有广阔的应用前景”, and Japanese future-development wording remain in the examples. Their presence alone triggers no automatic deletion or TODO marker |
| Revision candidates were delegated to a writer whose operations targeted the active manuscript | Prepare the candidate before specialist work; hand off the revision ID and target paths. Added `check --revision-id ID` and `set-sections --revision-id ID FILE ...`, selecting candidate text, metadata, labels, assets, and manifest with the workspace bibliography. Writing, shortening, and figure handoffs honor that target | Four new candidate workflow tests; active files remain byte-for-byte unchanged before application. No candidate assembly/export interface was added. Scientific support and reconciliation still require their existing checks |
| Outline confirmation was classified as major but decision recording was conditional | Every confirmed overall argument/structure is recorded; an existing decision that already covers the scope is reused. A collaborator's adoption record reuses the researcher's explicit instruction | Written comparison of outline, constraint-maintenance, research-feedback, and AGENTS.md. No live agent session was run |
| Sciverse's first-request wording could repeat a decision already recorded | Reuse an active scope that covers the query; ask only when no active scope covers it | Written comparison with the standing no-repeat rule and the per-query scope check. No service request was made |
| Git setup mixed new-paper setup with resetting history in the current folder | A new paper uses a separate template copy. A fresh history in the current folder is a separate explicit request for the same paper, with the existing risky-recovery safeguards | Written comparison with project-onboarding; no Git history was changed |
| Mock review promised independence without defining a fallback when isolated contexts were unavailable | Use isolated sessions when supported; otherwise produce three labeled passes with shared context and disclose that they are not independent reviewers. The README, description, report, and completion criteria agree | Written review only; no claim about human-review agreement or independence follows from the spread of same-session scores |
| Completion review found stale discovery summaries: the Claude Code directory overview listed only four initial skills, and the framework index called implemented conversion/interaction work planned | Removed the separate capability list from the host overview and linked the canonical directory, availability table, and implementation evidence. Updated the framework index to distinguish current implementation from unverified behavior | Read the host entry point, overview, synchronization script, canonical catalog, AGENTS.md, and implementation status. The host entry point imports the same contract; the sync script manages package copies, not the root overview |

## Complete skill coverage

The inventory remains 36 canonical `SKILL.md` files. Each skill's body, README, and linked skill-local reference files were read. The review examined task triggers and exclusions, confirmation and privacy gates, source versus interpretation boundaries, record ownership, handoffs, completion criteria, and agreement with the shared contract. The current-source completion pass rechecked changed packages, host entry points, the catalog, and repair dispositions. The table accounts for every skill; “no additional conflict found” describes this static review, not proof of every possible model behavior.

| Area | Skills reviewed | Cross-skill boundaries and disposition |
| --- | --- | --- |
| Setup and rules (4) | `project-onboarding`, `environment-management`, `privacy-configuration`, `constraint-maintenance` | Confirmed instructions versus wishes/inferences; requirement changes versus manuscript edits; installations, account controls, credentials, and processing scope. No additional conflict found |
| Intake and acquisition (3) | `source-ingestion`, `review-ingestion`, `reference-download` | Input-role routing, originals, direct text reading versus conversion, confidential letters, public retrieval versus upload permission, failed-job resumption. No additional conflict found |
| Literature and evidence (3) | `literature-discovery`, `literature-and-evidence`, `research-investigation` | Search authorization reuse repaired; provider order, snippets versus inspected evidence, source versions and locators, source notes versus project results otherwise align |
| Ideas and contribution (3) | `research-ideation`, `idea-deepening`, `impact-assessment` | Exploratory ideas versus selected questions; retained notes versus requirements; scientific choices; persuasive impact framing clarified without inventing a finding |
| Planning and execution (3) | `research-planning`, `research-feedback`, `research-code-setup` | Proposed versus confirmed work, adopted versus implemented feedback, plan-only scope versus authorized execution, recorded runs/results, negative evidence, freshness. Candidate figure handoff repaired |
| Venue and delivery (3) | `journal-selection`, `submission-assembly`, `submission-readiness` | Fit versus impact/readiness; target choice, sourced profile requirements, author-only facts, current builds, releases versus submission. No additional conflict found |
| Manuscript work (6) | `manuscript-import`, `manuscript-outline`, `manuscript-writing`, `manuscript-audit`, `manuscript-revision`, `natural-prose` | Structure decision records, candidate targets, meaning-preserving examples, author voice, and impact treatment repaired. Import, staged comparison, ordinary edits, final checks, evidence gaps, and major-revision boundaries rechecked |
| Review and model choice (3) | `review-response`, `mock-review`, `model-selection` | Round-specific response/change records, coauthor reconciliation, review scores versus acceptance forecasts, current provider-specific model advice. Reviewer execution fallback repaired |
| Versions (7) | `git-inspection`, `git-setup`, `git-save`, `git-compare`, `git-recovery`, `git-backup`, `git-hands-on` | Read-only inspection versus save/recovery/backup, scope and destination confirmation, practice versus real work, new-paper versus same-paper history. The latter boundary repaired |
| Coordination (1) | `paper-hands-on` | Named tasks route to their own skills; the coordinator preserves authorization across routine handoffs, pauses dependent work for major choices, and resumes from records. No additional conflict found |

The generated Claude Code packages are checked against the canonical packages rather than treated as independently maintained procedures. `CLAUDE.md` imports `AGENTS.md`, so both hosts share the same standing rules.

## Example comparison

Each language has six examples (families 1, 2, 3, 4, 9, and 10).

| Family | Proposition check |
| --- | --- |
| 1: emphasis | The method still uses one pass; English retains the two-pass comparator. Only roadmap text and repeated wording are removed |
| 2: impact | Numeric values, comparison scope and strength, evaluative emphasis, and outlook remain; tone is not used to infer a missing test |
| 3: authority | The many-studies attribution and close relationship remain. The marker requests the missing sources and clarification rather than silently weakening the relationship |
| 4: rhythm | All listed properties remain, including those not established merely by one GPU. Time, comparison degree, modality, and the Chinese degree limit remain |
| 9: translation | English retains widespread use; Chinese retains validation without naming its actor; Japanese keeps the passive experimental validation and ability modality |
| 10: responses | The actual addition, location, count, recency, reviewer attribution, author agreement or recognition, and careful consideration remain. Courtesy is shortened |

The comparison reported six intentionally added TODO markers for missing source/validation details, one removed duplicate numerical occurrence in the Japanese repetition example, and reduced redundant hedge words in the English and Chinese rhythm examples. The remaining hedges preserve uncertainty; Chinese “在一定程度上” is retained. Every difference was inspected. There were no unexplained protected-item changes. The semantic comparison supersedes the earlier natural-prose review's implication that protected-token checks established preservation of every claim.

## Verification

- `python -m unittest scripts.tests.test_manuscript scripts.tests.test_export scripts.tests.test_complete_path scripts.tests.test_collaboration_path`: 56 tests passed, including four new candidate workflow tests. These cover candidate-local failures, shared bibliography, unchanged active files, candidate manifest replacement and application, path boundaries, and refused missing/closed/applying candidates, plus existing assembly/export/revision behavior.
- All 36 skills passed `quick_validate.py`; `sync_skills.py --check` reported 36 matching packages; the capability table matched the skills folder; `check_readmes.py` passed for 109 project directories; both staged and unstaged `git diff --check` passed. Python: 3.12.9 on macOS. The full suite was not rerun for this change.
- Completion checks found every current canonical skill in the coverage table (36, none missing), no missing relative link targets across 170 canonical/mirror Markdown files, 36 matching package copies, an agreeing capability table, and 109 passing directory READMEs. These were repeated after correcting the stale overviews; only documentation changed in that completion pass.

Not verified: model behavior on the changed instructions, real manuscripts, reviewer independence on every host, or operation on Windows. A written review and deterministic tests do not establish those behaviors.
