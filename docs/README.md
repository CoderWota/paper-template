# Framework Design Documents

Start with [design-plan.md](design-plan.md). It distinguishes confirmed researcher requirements from architectural recommendations and unresolved decisions.

Framework documents are maintained in English only; translated copies are not kept.

[Implementation status](implementation-status.md) records what has actually been built and verified, one entry per MVP. Check it before assuming that a described capability works. The skill reviews that decide acceptance, and the scenario checklists of the earlier live runs, are in [acceptance/](acceptance/README.md). The [rule placement](rule-placement.md) note explains where each standing rule must live and what caused each family of acceptance defects.

These documents describe development of the reusable framework. They are not writing instructions for a future manuscript. Do not treat a proposed directory layout or policy as approved runtime behavior.

The [agent interaction specification](agent-interaction.md) records the confirmed requirements for prior user confirmation of major decisions and ASD-STE100 in English questions, including grilling. It distinguishes non-English clarity guidance and verified compliance from a prompt-only claim. Its integration and tests remain planned.

The [MinerU integration](mineru-integration.md) note records the MinerU research of 2026-10-28, the maintainer's integration decisions, the observed behaviour of the local route, the mineru.net API and terms, and the contract that the import scripts implement.

The [Markdown and export conventions](markdown-and-export-conventions.md) record GitHub-renderable LaTeX math, Mermaid explanation diagrams, and native editable Office Math/OMML equations in DOCX. They define shared source conventions, faithful conversion, and rendering/editability checks. These requirements are confirmed; the converters and validation workflows are not yet implemented.

The [Sciverse integration note](sciverse-integration.md) records the API fields and limits checked for MVP 3, the query-sharing gate, and the distinction between documented service behavior and unverified account access.

The [research workflow review and knowledge transfer](research-workflow-review.md) assesses the gap between an organized writing workspace and a complete researcher-directed production process. Its bounded complete-path objective is confirmed for framework testing only; it does not narrow the product or prove real submission readiness. The complete-path live exercise is optional follow-up under the 2026-10-29 acceptance decision; its partial execution and limits are in [the test record](acceptance/mvp-9-complete-path.md). The detailed execution, result/evidence, verification, package, and user-effort implementation contracts remain proposals.

Its primary-source legwork is retained in [OpenAI scientific case notes](openai-science-source-notes.md) and [agent engineering/submission notes](agent-workflow-source-notes.md). These are dated evidence notes, not operating instructions. Read them when the relevant design choice needs evidence; do not load every source note into ordinary writing sessions.

The root [README](../README.md) explains the design philosophy and intended everyday experience for researchers. Keep technical specifications here rather than making them prerequisites for ordinary use.

[Hands-on design](hands-on.md) organizes the paper and Git guided-practice skills. Technical project files and operations are maintained through the agent; researchers direct the work in ordinary language.

[Export trial](export-trial.md) records the 2026-10-28 trial of Pandoc with pandoc-crossref: native Word equations, citations, cross-references, a reference document, Mermaid rendering, and GitHub's rendering of the label syntax, with the decisions that followed.

[MVP implementation guideline](mvp-implementation-guideline.md) divides the design into nine usable increments. It specifies dependencies, implementation deliverables, acceptance evidence, deferred scope, and the first implementation stage for all 33 proposed skills. The [implementation status](implementation-status.md) records which increments are implemented, accepted by review, or verified, with the evidence observed.

Design plan v0.9 includes flexible intake, existing-manuscript adoption, batch reference acquisition and ingestion, and review extraction. It defines research decision and research feedback records, whose locations were confirmed on 2026-10-26, plus a major-revision coordinator with recoverable baselines, old-to-new mappings, and checks tied to changed inputs. Research feedback includes co-researchers, collaborators, coauthors, supervisors, and other contributors, with each source retained. The record formats and the revision layout remain open for discussion. Framework architecture records, if needed later, are separate from decisions in a researcher's manuscript project.

Every designed project directory, including nested and dynamically created directories, must have a useful English README. The design tree now shows each level explicitly. Creating operations maintain the descriptions; researchers are not expected to write technical directory documentation. `python scripts/check_readmes.py` checks the workspace against this rule. Read this README to find framework documents, and inspect only the documents needed for the current task.
