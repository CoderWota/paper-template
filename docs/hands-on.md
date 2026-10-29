# Agent-Led Research and Versioning Hands-On

Status: implemented. Every task below and both guided paths (`paper-hands-on` and `git-hands-on`) exist as skills and passed written review by 2026-10-29; the availability table in [`AGENTS.md`](../AGENTS.md) states the verified limits of each. No complete guided run with a researcher has been recorded yet.

This guide organizes the intended learning experience for researchers with ordinary computer literacy and no assumed coding or software-engineering knowledge. The [design plan](design-plan.md) defines the wider framework.

## How the guidance works

Start by describing what you want to achieve. The agent explains the next useful action, carries out technical work, shows the result, and asks one focused question when your judgment is needed. Work on real research material, with small examples or copies when practicing recovery.

You do not need to learn skill names, terminal commands, or configuration syntax. The agent maintains Git operations and settings, BibTeX citation records, YAML/JSON configuration, scripts, and indexes. You can say add this source, change the journal format, or save this version; the agent performs and checks the corresponding operation.

Your role is to direct the research, understand and assess the evidence and argument, review the work, and confirm meaningful choices. You can write prose or ideas directly. Logging in, privately entering a credential, or making a decision may still require your participation; the agent should guide that specific step in ordinary language.

The guide is optional support for completing the work, not a compulsory training course. The agent carries routine production and handoffs within the approved scope; you need not operate each stage, copy intermediate results, or maintain the work plan. It should request your ideas, domain judgments, genuinely unavailable material/access, and major choices, then return concrete outputs for review.

The agent must obtain your explicit confirmation before committing a major decision. It first prepares a concrete recommendation and explains the main effect, then asks one substantive question. Clear instructions you already gave apply within their scope; silence or a default option is not agreement. This also governs grilling and idea deepening. English questions use ASD-STE100; other languages retain natural expression and the same clarity principles, without claiming English-standard compliance. See the [interaction specification](agent-interaction.md).

## Use one task or follow a guided path

Every task below is an independently usable skill. Ask for just a literature search, impact assessment, journal comparison, manuscript check, or version comparison when that is all you need. The agent reuses existing material and asks only for missing context; it does not make you begin the course again.

`paper-hands-on` and `git-hands-on` select and connect these tasks when you want broader guidance. The same task procedures and project records serve both direct and guided use. Skill names in the tables explain the design; researchers do not need to memorize them. The task boundaries and catalog are maintained in Section 9 of the [design plan](design-plan.md).

## Paper hands-on: from an interest to a journal-format manuscript

Suggested entry request: “I have an area of interest but no organized project or paper yet. Guide me from collecting literature to developing and writing a paper for a suitable journal.”

The `paper-hands-on` skill coordinates the following independently usable tasks. It does not duplicate their instructions or require you to repeat work you already have.

| Task | Independent skill | What the researcher and agent do | Visible outcome |
| --- | --- | --- | --- |
| 1. Get started | `project-onboarding` | Clarify the initial interest, writing language, immediate goal, and practical constraints; invoke environment/privacy support only as needed. | A usable starting point and one clear next action. |
| 2. Find literature | `literature-discovery` | Search OpenDataLab Sciverse first, then use the model's built-in search to broaden or cross-check results; screen relevant sources and identify access gaps. | A sourced reading set with search routes and collection priorities. |
| 3. Import documents | `source-ingestion` | Import selected files or folders through MinerU, preserving originals, Markdown, and images. | An indexed library and concise batch status. |
| 4. Read and compare evidence | `literature-and-evidence` | Inspect relevant passages, check support, and compare limitations and contradictions. | Evidence notes with source locators. |
| 5. Generate directions | `research-ideation` | Organize starting thoughts and propose meaningfully different research ideas. | Directions the researcher chooses to keep. |
| 6. Deepen an idea | `idea-deepening` | Examine a selected idea through focused questions and prior-work comparison. | A clearer question, assumptions, contribution, and next check. |
| 7. Examine impact | `impact-assessment` | Discuss who benefits, why the question matters, and what supports or limits the contribution. | A reasoned assessment of value and improvements. |
| 8. Choose or compare journals | `journal-selection` | Examine current scope, article types, requirements, and relevant publications. | An explained target or shortlist with fit and tradeoffs. |
| 9. Plan and advance research | `research-planning`, `research-investigation` | Define methods and evidence needs, then carry out bounded inquiries and organize actual findings. | A feasible plan, supported research artifacts, and remaining evidence gaps. |
| 10. Structure the argument | `manuscript-outline` | Organize sections and reasoning around the question and available findings. | An outline the researcher can assess, with content gaps identified. |
| 11. Draft or revise | `manuscript-writing` | Write requested sections using confirmed requirements and actual evidence. | Reviewable prose with unsupported statements identified. |
| 12. Critically review the manuscript | `manuscript-audit` | Examine the argument, evidence, terminology, citations, and confirmed writing rules. | Prioritized, passage-linked findings. |
| 13. Format and assemble | `submission-assembly` | Apply the adopted requirements/templates, then render, inspect, and repair the result. | Formatted files with compliance checks and explicit limitations. |
| 14. Check submission readiness | `submission-readiness` | Assess the current manuscript/package against the selected venue, using relevant prior checks. | Strengths, likely reviewer concerns, and concrete remaining tasks. |

Research planning and investigation are separate requests within task 9: a plan can be useful before the necessary research can be completed. Other standalone tasks remain available, including `review-response` for an actual review round and `research-code-setup` when the research needs code. None requires completing the full hands-on path.

### Start with existing material or a specific import

Use the `inbox/` area or point to the material where it already lives. The agent routes mixed files by the task and their content, without requiring presorting or restarting the paper path.

| Starting point | Independent skills | Visible outcome |
| --- | --- | --- |
| An existing Word, LaTeX, Markdown, PDF, or other supported manuscript | `manuscript-import` | Preserved original, mapped sections/assets/citations, and a reviewable migrated draft with unresolved items. |
| A reference list, identifiers, or references from a draft | `reference-download`, optionally `source-ingestion` | Available documents and access gaps; if requested, converted and indexed Markdown/assets. |
| Editor/reviewer documents | `review-ingestion`, optionally `review-response` | Round-specific originals and checked extraction; responses only when requested. |
| Research feedback or meeting notes from co-researchers, collaborators, coauthors, supervisors, or other contributors | `research-feedback` | Attributed advice and follow-up, with only researcher-confirmed changes promoted to requirements. |

These are alternative entry points, not extra compulsory lessons. A download-and-import request connects the two tasks and retries only the affected stage. Consequential confirmed choices are recorded with concise rationale in `research/decisions/` through the planning/constraint workflows; ordinary edits do not need a decision record. Advice is not automatically accepted, and accepted advice is not marked implemented before the change exists.

Revisit earlier stages when findings change the idea or target. Researchers who already have a draft can begin with assessment or revision. Pause and resume through a concise project checkpoint instead of repeating the entire interview.

### Substantially revise an existing manuscript

Suggested request: “The central argument needs to change. Preserve the current version, help me reorganize the paper, and check the revised manuscript.”

The independent `manuscript-revision` skill coordinates existing research, outline, writing, audit, and assembly tasks. Start before submission, after research feedback, or during a review round. The agent identifies the actual starting version and scope, maps retained/moved/rewritten/removed material, works in recoverable steps, and resumes across sessions. It handles version mechanics; Git knowledge or installation is not a prerequisite.

Changed evidence or claims trigger renewed checks of their support and related passages, including summaries and conclusions. The agent preserves current author edits and earlier submission packages, keeps one active manuscript distinct from candidate drafts, and explains important differences and remaining work. Research still requiring evidence remains incomplete. Routine edits go directly to the writing skill without this extra record; formal responses can link to a major revision without duplicating its workflow.

### Impact and acceptance prospects

Assess the paper's contribution, its support, the audience it serves, and its fit with a venue separately. Journal prestige or a metric alone does not establish the value of a particular paper. Match the discussion to the discipline and article type.

For an actual target, use current official journal information and relevant inspected sources. Explain acceptance prospects as evidence-based strengths, risks, and changes that may improve readiness. Do not invent a manuscript-specific acceptance percentage, treat an aggregate acceptance rate as its probability, or promise an editorial outcome.

The workflow can expose missing evidence, suggest how to obtain it, and support genuine research. It cannot replace an unfinished experiment, investigation, interpretation, or argument with fabricated findings. A journal-formatted file and a scientifically ready manuscript are different milestones. Actual external submission is a separate researcher-directed action.

## Git hands-on: keep control of your versions

Suggested entry request: “I do not know Git. Help me save versions of this paper, see what changed, and practice recovering an earlier version.”

The `git-hands-on` skill teaches through the independent tasks below. The agent operates Git; you decide which work to preserve and understand the visible result. Reuse an existing history when appropriate rather than resetting it. A direct request to compare or save a version does not require a full Git lesson.

| Task | Independent skill | What happens | What the researcher learns |
| --- | --- | --- | --- |
| Inspect the project | `git-inspection` | Read tool availability, existing history, and current changes without modifying them. | What exists and what has not yet been preserved as a version. |
| Prepare local history | `git-setup` | If requested and needed, guide installation and local setup while preserving existing history and excluding secrets. | Which project material the history covers. |
| Preserve a version | `git-save` | Review the intended changes and save a local checkpoint with a meaningful description. | How to keep a recognizable milestone. |
| Compare versions | `git-compare` | Compare requested versions or edits and explain important differences. | What changed before choosing a version. |
| Retrieve earlier content | `git-recovery` | Recover selected material with appropriate scope and a way back; use a practice copy for a lesson. | How to retrieve earlier material while preserving current writing. |
| Arrange an external copy | `git-backup` | Discuss local versus external storage and carry out an explicitly requested destination/visibility choice. | What remains local, what leaves the computer, and who can access it. |

Do not require branch/rebase lessons or command memorization for ordinary version preservation. Explain additional concepts only when they help a real task. Ordinary requests should be enough: “Save the current version,” “Show what changed since yesterday,” or “Retrieve the previous paragraph so I can compare it.”

Do not overwrite real manuscript changes or rewrite shared history as a demonstration. Show the intended scope before a recovery that could replace work, preserve a way back, and obtain the researcher's specific choice where needed. Creating a remote repository, pushing research material, or sharing it externally is separate from saving a local version and requires an explicit instruction.

## What counts as success

The researcher finishes useful work and understands the relevant choice without manually editing `.bib`, YAML/JSON, scripts, or Git configuration. The agent reports completed work, links visible results, identifies gaps, and leaves a clear next action. Skills should be tested with this experience, not merely by checking that instruction files exist.

Each task must work directly with relevant existing material and also hand its results to another task through shared project records. The coordinating skill must not duplicate procedures, force unnecessary onboarding, or repeat completed tasks merely to follow the teaching sequence.
