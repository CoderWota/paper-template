# Framework Design Documents

Start with [design-plan.md](design-plan.md). It distinguishes confirmed researcher requirements from architectural recommendations and unresolved decisions.

Framework documents are maintained in English only; translated copies are not kept.

[Implementation status](implementation-status.md) records what has actually been built and verified, one entry per MVP. Check it before assuming that a described capability works.

These documents describe development of the reusable framework. They are not writing instructions for a future manuscript. Do not treat a proposed directory layout or policy as approved runtime behavior.

The [agent interaction specification](agent-interaction.md) records the confirmed requirements for prior user confirmation of major decisions and ASD-STE100 in English questions, including grilling. It distinguishes non-English clarity guidance and verified compliance from a prompt-only claim. Its integration and tests remain planned.

The [Markdown and export conventions](markdown-and-export-conventions.md) record GitHub-renderable LaTeX math, Mermaid explanation diagrams, and native editable Office Math/OMML equations in DOCX. They define shared source conventions, faithful conversion, and rendering/editability checks. These requirements are confirmed; the converters and validation workflows are not yet implemented.

The [research workflow review and knowledge transfer](research-workflow-review.md) assesses the gap between an organized writing workspace and a complete researcher-directed production process. Its bounded complete-path objective is confirmed for framework testing only; it does not narrow the product or prove real submission readiness. The detailed execution, result/evidence, verification, package, and user-effort implementation contracts remain proposals. The test has not been executed.

Its primary-source legwork is retained in [OpenAI scientific case notes](openai-science-source-notes.md) and [agent engineering/submission notes](agent-workflow-source-notes.md). These are dated evidence notes, not operating instructions. Read them when the relevant design choice needs evidence; do not load every source note into ordinary writing sessions.

The root [README](../README.md) explains the design philosophy and intended everyday experience for researchers. Keep technical specifications here rather than making them prerequisites for ordinary use.

[Hands-on design](hands-on.md) organizes the planned paper and Git guided-practice skills. Technical project files and operations are maintained through the agent; researchers direct the work in ordinary language.

[MVP implementation guideline](mvp-implementation-guideline.md) divides the design into nine usable increments. It specifies dependencies, implementation deliverables, acceptance evidence, deferred scope, and the first implementation stage for all 33 proposed skills. All milestones remain planned until actual implementation and verification.

Design plan v0.9 includes flexible intake, existing-manuscript adoption, batch reference acquisition and ingestion, and review extraction. It proposes research decision and research feedback records, plus a major-revision coordinator with recoverable baselines, old-to-new mappings, and checks tied to changed inputs. Research feedback includes co-researchers, collaborators, coauthors, supervisors, and other contributors, with each source retained. These exact research/revision layouts remain open for discussion. Framework architecture records, if needed later, are separate from decisions in a researcher's manuscript project.

Every designed project directory, including nested and dynamically created directories, must have a useful English README. The design tree now shows each level explicitly. Creating operations maintain the descriptions; researchers are not expected to write technical directory documentation. `python scripts/check_readmes.py` checks the workspace against this rule. Read this README to find framework documents, and inspect only the documents needed for the current task.
