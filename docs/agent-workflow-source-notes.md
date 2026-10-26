# Public Sources for Agent Workflow and Submission Readiness

Status: research notes for design review, not adopted runtime instructions or an implementation claim.
Verified: 2026-10-26.

This note uses public first-party sources. It separates what a source documents from recommendations for this repository. Public engineering reports do not reveal all of OpenAI's research or publication practices. They do not establish that an agent can produce a valid journal article from ideas alone.

## Transferable agent engineering practices

| Primary source | Verified public claim | Proposed transfer and limitation |
| --- | --- | --- |
| [OpenAI: Harness engineering](https://openai.com/index/harness-engineering/) | In its reported software project, OpenAI uses a short AGENTS.md as a map to repository knowledge. Versioned execution plans include progress and decision records. Mechanical checks and feedback support agent work. The article explicitly limits the generalizability of its results. | Keep AGENTS.md concise. Make current manuscript state, approved decisions, evidence, and active work discoverable. Check observable invariants. This is a software engineering case study, not evidence of scientific validity or a universal paper-production process. |
| [OpenAI Cookbook: Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans) | The published plan pattern requires enough context for a fresh agent, current progress, decisions, acceptance evidence, and safe retry or recovery. Its completion criterion is demonstrable behavior. | Save a compact work record for a complex research or revision task: purpose, input versions, approved scope, completed outputs, unresolved blockers, and next verification. Adapt the pattern; do not copy its autonomous decision guidance over this project's requirement for prior confirmation of major choices. |
| [OpenAI: A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/) | The guide describes models, tools, and instructions as foundations. It recommends expanding a single agent before adding orchestration complexity. Retry thresholds and consequential actions are reasons for human intervention. | Define each skill's inputs, outputs, checks, recovery, and stop conditions. Continue routine approved work without repeated permission requests. Ask about consequential research choices or a genuinely exhausted recovery path. More named agents or more skills do not themselves establish reliability. |
| [OpenAI: Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | The guide recommends task-specific evaluations, continuous evaluation, and calibration with human feedback. It rejects judging success from a favorable impression alone. Model grading has biases and requires validation. | Test citation support, original-to-extraction fidelity, resumption, revision consistency, document rendering, and ordinary-user effort. Use mechanical checks for syntax and links; use knowledgeable human review for scholarly adequacy. An agent's own favorable review is insufficient acceptance evidence. |
| [OpenAI: Introducing deep research](https://openai.com/index/introducing-deep-research/) | The launch report describes multi-step browsing and cited research reports. It also records hallucinations, incorrect inferences, difficulty distinguishing authority, and weak uncertainty calibration. | Provide a search-and-verification loop with retrievable source locations and explicit evidence limitations. Citations aid checking; their presence does not prove that a source supports a claim. This historical launch report is not a current product-access or capability specification. |

These sources support transferring operating methods rather than imitating an undisclosed internal organization. No framework choice should depend on a claim that OpenAI has already solved the entire scholarly writing process.

## Submission requirements extend beyond manuscript formatting

[PLOS One's submission guidelines](https://journals.plos.org/plosone/s/submission-guidelines) distinguish the manuscript from other submission material. The page specifies a separate cover letter, author contributions, separate figure and supporting-information files, funding and competing-interest information, and data reporting requirements. Some requirements depend on the study. Its contribution section expects authors to agree their contributions before submission.

**Proposed transfer:** build a venue- and article-specific deliverable list early. For each applicable item, track the official source, evidence or draft, unresolved information, and required human confirmation. Formatting a DOCX or PDF cannot alone establish readiness. PLOS One's language, section order, taxonomy, or study checklists must not become universal defaults for unrelated disciplines or venues.

[Taylor & Francis's AI policy](https://taylorandfrancis.com/our-policies/ai-policy/) states that AI does not meet authorship criteria, that authors retain responsibility, and that journal instructions may be more restrictive. This source is a publisher policy, not a guarantee about each individual journal.

Its [detailed author guidance on AI use](https://authorservices.taylorandfrancis.com/editorial-policies/using-ai-in-your-research-and-manuscript-preparations/) currently distinguishes permitted uses: its table disallows generative AI creating first manuscript drafts or sections, while permitting language refinement within stated boundaries. It requests disclosure information including tool name and version and author responsibility. It also sets additional records for some research uses.

**Proposed transfer:** check a target journal's current AI rules before substantive drafting, and check again before submission or a venue change. Record the actual assistance performed and the guidance consulted. A later disclosure cannot retroactively make a prohibited workflow permitted. Where drafting is restricted, offer permitted support and explain the resulting division of work. Do not silently relabel generated argument as copyediting.

[Nature Portfolio's AI policy](https://www.nature.com/nature-portfolio/editorial-policies/ai) is a further primary-policy pointer. Only search-index text was available during this review; direct retrieval encountered the publisher's identity redirect. No detailed Nature-specific permission is treated here as a fully retrieved, verified policy contrast. Retrieve and inspect the actual current policy for a real submission.

**Proposed transfer:** keep scholarly judgment and final author approval visible while allowing substantial agent assistance where applicable policy permits. Verify the actual target's current rules rather than giving a universal assurance that all AI drafting is allowed.

## Design gaps these sources expose

The existing design already covers many necessary ingredients: material intake, source conversion, evidence notes, constraints, independent skills, major revision, formatting, confirmation, and recoverable outputs. Its next design review should connect those ingredients through explicit operating behavior. The following are recommendations for discussion, not newly confirmed requirements.

1. **An end-to-end work record.** Show the active objective, approved scope, artifacts in progress, blockers, next agent action, and questions requiring research judgment. Keep one authoritative current status and link to detailed task records when needed. The researcher must not become the person who routes files and tracks every handoff.
2. **Claim and result dependencies.** Distinguish literature-supported claims, findings from this project, interpretation, and proposed future work. Link substantive claims to source locations or research artifacts and relevant limitations. Mark affected checks stale when evidence, analysis, or a main claim changes. Avoid a mandatory sentence-by-sentence bureaucracy for every article.
3. **Execution of research support.** A code-directory setup skill is not an analysis capability. When the project needs computation or material analysis, define how the agent performs authorized work, records inputs and decisions, verifies outputs, and obtains appropriate expert review. Where physical research, permissions, or inaccessible data are required, identify the actual missing contribution. Prose cannot substitute for it.
4. **A complete submission package.** Derive applicable files, declarations, permissions, anonymization, metadata, supplements, and author approval needs from the venue and article. Keep scientific readiness, document compliance, package completeness, and submission authorization distinct.
5. **Policy-aware assistance and truthful disclosure.** Keep a minimal factual activity record sufficient for the target requirements; do not collect private hidden reasoning, secrets, or unnecessary personal data. Prepare the disclosure and identify facts the authors must confirm. The agent cannot invent coauthor agreement, ethics approval, contributions, conflicts, consent, or data availability.
6. **Realistic end-to-end verification.** Demonstrate ordinary-user success with actual artifacts and injected failures, not only isolated scripts or a long list of proposed skills. Record recovery, unperformed checks, human effort, and the environment actually tested. A generic model self-score is not evidence of publication quality or acceptance probability.

## Proposed acceptance scenario

Use a rights-cleared, bounded test project with enough genuine evidence for its chosen article type. Include a second, noncomputational project so the template is not validated only against a coding study. No real external submission is part of this test.

The researcher supplies a plain-language idea, a mixed folder of papers and an existing draft, available research materials, the intended contribution, and feedback from a collaborator. They confirm consequential choices and inspect scholarly outputs. They do not edit BibTeX, YAML, Git history, environment files, or technical status records.

| Stage | Agent carries the operational work | Researcher supplies or confirms | Observable acceptance evidence |
| --- | --- | --- | --- |
| Establish the project | Inspect materials, prepare necessary dependencies, route imports, identify missing facts, and check target instructions and AI-use limits. | Goal, language, relevant constraints, permitted processing and any required sign-in. | Preserved originals, accurate imports, one understandable status, and no manual technical-file editing. |
| Develop the argument | Search, obtain available documents, convert and deduplicate them, collect evidence locations, and test alternatives and counterarguments. | Scientific intent and choice among consequential alternatives. | Supported and unsupported claims are distinguishable; missing full texts and contrary evidence remain visible. |
| Prepare research outputs | Perform authorized feasible analysis or material organization; produce inspectable figures, tables, or argument evidence as appropriate. | Actual materials, consequential method decisions, domain judgments, and any work only humans or external facilities can perform. | Results are connected to their inputs and methods. Unperformed work remains pending. |
| Draft or revise within policy | Use the permitted writing mode, maintain references and assets, reconcile feedback, and prepare a coherent manuscript. | Review of scientific meaning and approval of substantive changes. | Text and exhibits agree, citation support is checked, and generated work is described accurately. |
| Recover and continue | Resume after a forced session boundary and a failed download or conversion. Preserve a concurrent author edit. | Only genuinely missing authority or facts. | No duplicate library entries, silent overwrite, forgotten scope, or request for the researcher to reconstruct the workflow. |
| Make a major change | Preserve the baseline, prepare an impact map, obtain approval, update affected sections and rerun dependent checks. | The new direction and major tradeoffs. | Obsolete conclusions, figures, abstracts, and responses do not survive as apparently verified text. |
| Prepare the submission | Apply the actual template, inspect rendering and native Word equations where relevant, assemble applicable supplements and declarations, and produce a checked package. | Factual declarations, author agreement and final scholarly approval. | A package manifest links each applicable requirement to its artifact or an explicit unresolved blocker. |

The test passes only if the evidence is adequate for the demonstrated article, the package has no unresolved blocking requirements, and the ordinary researcher completes the workflow without clerical project management. It may correctly conclude that more research is needed. In that case it has demonstrated an honest readiness assessment, not a completed submission-ready paper.

Record the time spent by the researcher on scientific review separately from clerical effort, the number of avoidable questions, and any manual technical operations. Review the failed cases and improve the tools or instructions that caused them. A completed local package still requires separate authorization for upload, publication, payment, or communication with a journal.

## Limits and follow-up

All links above were checked as public primary sources on the stated date. Product and publisher policies can change. A real submission needs a fresh check of the selected journal, article type, publisher rules, and any institutional obligations. This note does not select a discipline-wide reporting standard or establish legal compliance.

The acceptance scenario is proposed. It has not been run, and no Windows/ARM64, live conversion, scientific analysis, export, or journal submission capability is claimed here. Adopted framework changes still require the maintainer's confirmation under the existing interaction specification.
