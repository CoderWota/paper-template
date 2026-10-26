# MVP Implementation Guideline

Status: proposed implementation roadmap v0.3. No MVP is implemented or verified yet; MVP 1 has started with the workspace scaffold.
Updated: 2026-10-26.

This is the agent-facing implementation guide for the [design plan v0.9](design-plan.md) and [hands-on design](hands-on.md). Researchers are not expected to edit this technical document.

The current repository contains design documents, researcher-facing README files, and the initial workspace scaffold: the designed directories with their READMEs, empty-state records, a draft AGENTS.md, and a README check script. It does not yet contain adopted operating instructions, skills, conversion/export scripts, or a functioning research workspace. [Implementation status](implementation-status.md) records progress. This roadmap does not authorize external uploads, account changes, Git publication, or implementation of the entire framework during a planning request.

The [research workflow review](research-workflow-review.md) proposes a stronger result-production and verification contract based on public scientific and agent-engineering sources. The complete-path objective is confirmed only as a framework test; detailed scope and priority changes remain proposals. The researcher's role as intellectual lead and reviewer, with the agent carrying feasible routine production and coordination, is already confirmed. Do not treat the hands-on as a compulsory course or make the researcher dispatch each skill.

## 1. How to implement this roadmap

Build each MVP as a usable researcher outcome: a natural-language request produces useful files, a meaningful decision, or a recoverable version. A collection of empty directories, skill manifests, or configuration stubs is not a completed MVP.

1. Read the current design, relevant requirements, and actual repository state. Preserve work already present; do not regenerate or overwrite existing research material.
2. Select one MVP and resolve only the decisions that affect it. Keep confirmed requirements separate from implementation recommendations. AGENTS.md still needs the discussion requested by the maintainer before its operating contract is settled.
   Before committing any major decision, obtain explicit user confirmation of the concrete choice and scope under the [interaction specification](agent-interaction.md). Prepare evidence and options first; leave dependent changes pending until the answer. Clear existing authorization can satisfy this requirement.
3. Implement a narrow complete path, including the relevant skill, deterministic operations, user guidance, failure handling, and checks. Use one canonical skill body and validated Codex/Claude adapters, with English agent-facing instructions.
4. Demonstrate the outcome through a direct natural-language request and inspect the actual artifacts. Test meaningful failure and recovery cases, not merely the existence of instructions.
5. Record changed files, resolved decisions, observed behavior, test environment, remaining limitations, and the next useful task. Update researcher-facing documentation to distinguish working, partial, and planned capabilities.
6. Continue to a dependent MVP only when its prerequisites are demonstrated. An unrelated branch can proceed independently. Do not create a new mandatory approval ceremony for routine work; honor the researcher's existing directions and clarify choices that genuinely change scope, data transfer, or consequences.

The MVP numbers describe implementation slices, not a mandatory course for researchers. A researcher with existing materials can directly request any implemented task for which sufficient inputs are available.

## 2. Decisions to resolve at the relevant milestone

| Decision | Resolve by | Guideline |
| --- | --- | --- |
| Workspace scope | MVP 1 | One main manuscript per workspace remains a recommendation, not a confirmed decision. Adopt an explicit initial scope without hard-coding a discipline or article structure. |
| AGENTS.md contract and skill adapters | MVP 1 | Discuss the concise shared rules, adopt the agreed text, and verify actual loading in both agents. Do not copy the full roadmap into AGENTS.md. |
| Exact Windows baseline | MVP 1; validate again in MVPs 2 and 6 | Record OS, RAM/storage, x64/ARM64, installed tools, and available model access. Surface is a product-family reference, not a complete hardware specification. Do not invent a verified minimum or claim untested architectures. |
| Source metadata and file tracking | MVP 2 | Choose the canonical metadata representation; BibTeX is the current proposal. Specify identifiers, citation keys, extraction provenance, tracking, and backup responsibilities without asking researchers to edit technical formats. |
| Intake and research records | Intake in MVP 2; research records in MVP 4 | Intake capabilities are required; exact archive mappings remain proposed. Discuss the proposed decision/feedback layout before adopting it. Keep current requirements distinct from rationale and unadopted advice; add no inferred-preference storage or compulsory decision ceremony. |
| MinerU service and local/cloud routes | MVP 2 | MinerU is already selected. Verify the actual version, API, client dependencies, authentication, cost/limits, data-use/retention policy, supported local tiers, and package/model redistribution terms before coding against or bundling them. |
| Remaining Markdown conventions, publishing engine, first journal/output | Before drafting conventions stabilize in MVP 5; prove in MVP 6 | GitHub-renderable math, Mermaid explanation diagrams, and native editable Word equations are confirmed. Evaluate remaining citation/numbering conventions with an actual template trial. Pandoc versus Quarto and the first output format remain open; validate formula fidelity as well as layout. |
| Major-revision records and recovery | MVP 5; extend through MVPs 6 and 8 | The revision coordinator and exact layout are proposals. Specify recoverable baselines, active versus candidate drafts, input-versioned checks, interruption recovery, and a local snapshot route without Git. Do not impose this machinery on ordinary edits. |
| External backup/collaboration | MVP 7; coauthor reconciliation in MVP 8 | Establish the researcher's intended destination, visibility, permissions, and what leaves the machine. Local version preservation does not authorize publication. |

Do not stop unrelated drafting because an optional provider, journal, architecture, or research-code path is undecided. Record the affected capability accurately and continue work that does not depend on it.

## 3. MVP overview and dependencies

| MVP | Researcher-visible outcome | Development prerequisites | Status |
| --- | --- | --- | --- |
| 1 | Initialize an understandable project and retain confirmed requirements across sessions. | None beyond a usable agent host/model; provide a human-readable entry guide. | In progress (scaffold only) |
| 2 | Route intake and convert literature or review documents into archived, readable, resumable results. | MVP 1 environment, privacy, and storage conventions. | Planned |
| 3 | Find and batch acquire literature, import available full text, and retrieve checkable evidence. | MVP 1; MVP 2 for converted inputs, or existing readable sources. | Planned |
| 4 | Develop ideas and research plans, work through feedback, and retain consequential confirmed rationale if adopted. | MVP 1; MVP 3 for source-backed investigation; existing material can also be used. | Planned |
| 5 | Adopt, write, audit, or substantially revise a manuscript with recoverable prior work. | MVP 1, source/evidence contracts from MVP 3; MVP 2 for converted drafts; existing inputs can substitute for earlier research stages. MVP 7 is optional: local snapshots must support revision without Git. | Planned |
| 6 | Choose a journal and produce a manuscript/package checked against its actual format requirements. | MVP 5 conventions or an existing manuscript; source/citation integrity from MVP 3. | Planned |
| 7 | Preserve, compare, recover, and explicitly back up versions through the agent. | MVP 1 only; this branch can be implemented immediately after MVP 1. | Planned |
| 8 | Process review rounds and reconcile coauthor edits without losing the canonical manuscript. | MVP 5; MVP 2 for converted correspondence, MVP 6 for re-export, MVP 7 when version history is used. | Planned |
| 9 | Follow or resume the complete paper hands-on using the same independent skills. | MVPs 1–6; MVP 7 for demonstrated Git handoff and MVP 8 for the revision extension. | Planned |

Recommended main sequence: 1 → 2 → 3 → 4 → 5 → 6 → 8 → 9. MVP 7 is a separate branch available after MVP 1 and is useful before substantial manuscript editing. These are development dependencies, not a requirement that every researcher complete all previous activities.

### Confirmed end-to-end test objective

Use a bounded case to test **idea/materials → actual results → supported manuscript → checked submission package**. This is an integration and researcher-effort test, not a new product scope or a restriction to existing data, accessible literature, small projects, a particular discipline, or a fixed research method. The nine MVPs, skill catalog, and individual capability checks remain in place; this decision does not reorder them.

Prepare a rights-cleared fixture and explicit expected outcomes when the relevant capabilities can be exercised. Assert result provenance, source support, coherent writing, required output/package properties, recovery, and absence of manual technical chores. Use deliberate failures to check honest blocker reporting. Label test manuscripts, synthetic examples, and test packages clearly. Do not require an actual journal submission or claim a new publishable discovery to pass a framework test.

Record test pass/fail, real manuscript readiness, and author/submission approval separately. An expected blocked case can pass its test without being submission-ready. Report only the services, formats, environments, and workflows actually exercised; retain separate tests for other capabilities. No end-to-end test has been executed yet.

At least one positive case must complete the full path and deliver the expected linked results and package. Correct blocker reporting in a negative case validates failure handling, not successful end-to-end production.

## MVP 1 — A usable project and confirmed memory

**Example request:** “Help me initialize this paper project. I do not know programming.”

**First skills:** `project-onboarding`, `environment-management`, `privacy-configuration`, `constraint-maintenance`.

**Implement:**

- The agreed AGENTS.md contract, a verified CLAUDE.md entry/adaptation, canonical `.agents/skills` packages and portable `.claude/skills` adapters, `.gitignore`, plain-language README/entry guidance, and the maintained workspace directories with their READMEs. Create optional research-code content only when relevant.
- A meaningful English README in every designed directory, including hidden skill directories, intermediate grouping directories, assets, archives, and dynamically created instances. Directory-creating operations own creation and maintenance. Check purpose and content roles, not only file existence; keep README files out of manuscript/evidence/reviewer inputs. No framework scaffold is complete with placeholder descriptions alone.
- The shared major-decision confirmation rule and question guidance in both agent entry paths and skill routing. Include grilling, scoped reuse of prior confirmation, and waiting for an answer before dependent work. Implement English STE checks against the adopted official rules/dictionary and corresponding clarity review for other languages, without changing the manuscript language/style by default or claiming unverified compliance.
- Initial project/language/privacy requirements and concise current state. Keep inferred preferences out of persistent files, including notes and handoffs. Separate confirmed rules from retained exploratory ideas and research hypotheses.
- Tool detection and reuse of compatible installed Python/CLI tools, on-demand project-local `.venv` management without overwriting working global environments, private local credential entry and ignored storage, plus documented privacy-setting assistance. A cloud route must not require installing a full local inference stack. A missing converter must not prevent ordinary reading/writing.

**Acceptance evidence:**

- In fresh Codex and Claude Code sessions, a researcher can initialize through ordinary language, inspect the resulting choices, and continue a task. A later session follows an explicit saved rule; an unconfirmed inferred preference is absent from persistent files.
- Inspect all created project directories for useful READMEs, including generated skill mirrors and a newly created example instance. Repeat creation without losing existing explanations. Verify that directory documentation cannot enter manuscript assembly or be reported as scholarly evidence or review comments.
- Present a consequential choice in each agent host: the agent prepares a concrete recommendation, asks one clear question, and makes no dependent change before an answer. Silence and default selections do not authorize it; an explicit instruction with clear scope does. Routine authorized work does not trigger repeated confirmation. Inspect English questions against the adopted STE issue and dictionary, including a grilling example; sentence length alone is insufficient. Verify natural non-English questions without a false STE claim.
- Simulate missing Python/tools, unavailable account controls, and deferred service credentials. The researcher receives an actionable next step without editing Git, BibTeX, YAML/JSON, scripts, or environment syntax. A credential file actually reaches the intended process; writing an unused file is not success.
- Check that test credentials do not appear in chat output, commands, logs, or tracked files. Privacy reports distinguish observed controls, researcher confirmation, policy defaults, and unknown/admin-only states; no manuscript is uploaded to test privacy.

**Not yet:** literature conversion, publication-ready output, or a claim that every account/provider setting has been changed. Preserve incomplete setup states honestly.

## MVP 2 — Flexible intake and MinerU batch ingestion

**Example request:** “Import all PDFs in this folder, including the images. Continue only the failed items if interrupted.”

**First skills:** `source-ingestion`, `review-ingestion`. Extend MVP 1 setup only for the chosen MinerU integration.

**Implement:**

- A thin project adapter around documented MinerU routes. Prove one complete file first, then batch handling, then the other supported local/cloud route. Honor the confirmed service and upload scope; never switch to cloud or another parser silently.
- Original archives, stable source IDs/checksums, extracted Markdown/assets, parser-native results, provenance/coverage records, citation metadata, and a compact index. Preserve originals and researcher notes on re-import; distinguish related source versions and incomplete extraction.
- Per-document progress, deduplication using input/settings, temporary-result publication, retry/resume, asset-link repair, rate-limit handling, and a concise converted/skipped/failed/review-needed summary. Keep technical logs in the background and redact credentials.
- Apply the same ingestion contract to Word and other documented supported input formats. Prove PDF conversion first, but do not equate the first PDF path with completion of the broader document-ingestion requirement; unsupported formats remain explicit.
- Apply the shared [Markdown and export conventions](markdown-and-export-conventions.md) to derived math. Preserve originals/native results, normalize supported delimiters without changing mathematics, and flag unverified transcription or unsupported commands rather than silently repairing scientific content.
- An optional `inbox/` and import records linking originals, roles, destinations, and unresolved items. Also accept files where they already live. Route mixed material without compulsory presorting; keep unadopted manuscripts out of the body manifest. Full manuscript adoption is delivered in MVP 5.
- Direct formal-review extraction into venue/round originals and `extracted/markdown/` plus assets. Keep numbering, reviewer labels, locators, images, and conversion gaps. Inspect native comments, annotations, and revisions separately where needed; Markdown text conversion alone does not prove they were captured. No response-writing dependency is required for extraction.

**Acceptance evidence:**

- Use a rights-cleared fixture folder with duplicate names/content, non-ASCII/spaced paths, images, scanned pages, columns, a table, an equation, and a document longer than ten pages. Inspect page coverage and actual Markdown/image links; do not accept an initial page window as full-document success.
- Import a representative Word source and inspect the archive, Markdown, assets, and source record. Verify other input formats before declaring them supported; do not silently change parsers to satisfy the test.
- Route a mixed intake folder and a direct external path while preserving original files and existing manuscript work. Extract a Word review with inline comments and a supported annotated document; account for each supplied item or explicitly report the unsupported structure. Repeating the task must not duplicate comments or mix rounds.
- Inspect READMEs at every newly created source, extraction, asset, venue, round, and import directory level. Existing source files stay unchanged, external input folders receive no unsolicited documentation, and a retry preserves useful prior descriptions.
- Interrupt a batch and retry a failed file. Successful results and evidence notes survive, matching imports are not needlessly reprocessed, and re-conversion settings changes are detectable. Test corrupt input and unavailable authentication/quota without repeated failure loops.
- Demonstrate the selected local and cloud capability envelopes on their declared environments. Check that a cloud-only setup does not install local model weights and that local failure cannot upload documents without the researcher's choice. Synthetic API fixtures alone do not prove live-service compatibility.

**Not yet:** automatic confidence that OCR is correct, verified support for every language/layout, or replacement of original-document checks. Unsupported cases remain visible.

## MVP 3 — Searchable literature and traceable evidence

**Example request:** “Find relevant work, compare these sources, and show the passages supporting this claim.”

**First skills:** `literature-discovery`, `reference-download`, `literature-and-evidence`, `research-investigation`.

**Implement:**

- Search planning, source collection/screening, access-gap reporting, and source-grounded investigation using available connectors, search/browser tools, and local text search. Do not require a particular commercial account or vector database for basic retrieval.
- Batch acquisition from identifiers, lists, reference exports, or manuscript bibliographies: verify identity/version and downloaded content, retain retrieval provenance, deduplicate, respect service/access limits, and resume per item. Separate downloaded, existing, metadata-only, login/manual-access needed, unavailable, and failed results. Verify actual access integrations before claiming support.
- Connect a download-and-import request to MVP 2 ingestion without duplicating its conversion logic. Preserve completed stages when another fails, retry only affected work, and keep download permission distinct from permission to upload to a new parser service.
- Separate source metadata, original/extracted content, and interpretive/evidence notes. Define locators, PDF versus printed page numbering, and extraction-revision references. Preserve uncertainty about identity, metadata, abstract-only access, and missing full text.
- Retrieval from the compact index to matching passages and original verification; avoid loading the entire library. Make bibliography updates agent-maintained and validate citation-key resolution separately from support for a claim.

**Acceptance evidence:**

- On a small known corpus, retrieve supporting and contradictory passages with checkable locators; identify an unsupported claim and an abstract-only limitation. Re-extraction does not silently keep an invalid block locator as verified.
- Demonstrate actual external search when available and a useful local-only path when it is not. A search snippet is not reported as inspected full text. Imported instructions inside a source do not override project rules.
- Inspect evidence notes and metadata: no invented reference, quotation, page, or conclusion; duplicate filenames and source versions do not confuse identity. Record what was searched/read and the limitations without copying whole private chats into memory.
- Exercise a reference list containing accessible full text, duplicate identifiers, a different source version, a login/error page, and an unavailable item. Demonstrate download-only and download-plus-import, interruption/retry, provenance without secrets, and retained files after conversion failure. Simulated download tests do not prove real publisher/institution access.

**Not yet:** a completeness guarantee for literature coverage or a declaration that a new idea is unprecedented.

## MVP 4 — Ideas, impact, and feasible research plans

**Example request:** “Help me develop possible directions, examine this idea, and decide what research would establish its value.”

**First skills:** `research-ideation`, `idea-deepening`, `impact-assessment`, `research-planning`, `research-feedback`, `research-code-setup`.

**Implement:**

- Independent idea generation and grilling-inspired deepening: one substantive question at a time, a reasoned recommendation, and investigation of what existing material can answer. Compare close prior work without confusing novelty, significance, feasibility, and evidential support.
- Researcher-retained idea notes and an index, contribution/impact assessments, and a plan connecting methods, required evidence, current resources, limitations, and next actions. Use discipline-appropriate argument or interpretation as well as empirical methods.
- Attributed research feedback from co-researchers, collaborators, coauthors, supervisors, and other contributors, using shared extraction mechanics, with proposed actions and researcher-confirmed adoption. Preserve individual attribution in multi-person documents or meetings. If the proposed research-record design is adopted, preserve consequential confirmed choices and rationale under `research/decisions/` and feedback under `research/feedback/`. Keep active requirements canonical, record supersession, and avoid a full decision record for every edit. This exact layout is still a discussion choice.
- The optional code-setup skill: elicit actual needs before creating `code/`, its README, structure, environment, and reproducibility guidance. Keep research dependencies separate from ingestion utilities. No code workspace is required for non-code research.

**Acceptance evidence:**

- Demonstrate distinct proposed directions, direct deepening of an existing idea, and a value assessment grounded in sources/assumptions. The agent challenges a weak premise and qualifies unverified originality; it does not manufacture a literature gap.
- Exercise an empirical and a conceptual/interpretive scenario. Both yield a useful research plan without forcing the same article structure or an unnecessary experiment. Retained hypotheses are labeled; inferred writing preferences are not saved.
- Work through conflicting suggestions from a co-researcher and a supervisor, including a collaborator-supplied outline and a multi-person feedback document. Preserve each source and do not prioritize by title or authorship status. No suggestion becomes a rule before researcher adoption. After an explicit choice, update only the relevant outline/requirements, link important rationale where appropriate, and distinguish accepted from implemented. A fresh session must not apply declined advice or a superseded decision as an active rule.
- For a code-requiring example, set up the requested structure and run a small reproducible smoke task on clearly labeled test data. Changing a document-conversion dependency does not silently break it. The non-code example creates no compulsory code project.

**Not yet:** fabricated research findings, automatic execution of work requiring researcher participation, or a universal research-code platform.

## MVP 5 — Evidence-based writing, audit, and major revision

**Example request:** “Use these findings and my requirements to structure the paper, draft this section, and review its argument.”

**First skills:** `manuscript-import`, `manuscript-outline`, `manuscript-writing`, `manuscript-audit`, `manuscript-revision`.

**Implement:**

- A documented Markdown dialect and manageable section conventions, an outline and explicit assembly manifest, stable figure/table/citation references, and the manuscript assets area. Keep one file per major section at most and allow a single-file manuscript.
- GitHub-compatible inline/display LaTeX math and Mermaid explanation diagrams under the shared conventions, with syntax checks and target-renderer inspection. Preserve editable diagram source, selected-language labels, and scientific plots in suitable formats. Remaining scholarly markup must work with these confirmed requirements and the selected export engine.
- Existing-manuscript adoption from verified supported editable formats and PDF: preserve originals, inventory sections/assets/citations/comments, map them to workspace conventions, and expose losses or unresolved references. Prefer available editable sources. Stage or compare against an existing working manuscript instead of silently overwriting it; conversion itself must not rewrite science or accept every revision.
- Focused drafting/revision using confirmed constraints and actual evidence, with separate checks for argument, terminology, style, citation integrity, and claim support. Keep unresolved claims visible without presenting them as findings.
- Resume through concise state; keep outlines and notes out of assembled body content and preserve direct researcher edits. Technical metadata and manifests are maintained by the agent.
- If adopted, the major-revision coordinator and lightweight revision records: actual baseline including current edits and relevant inputs, researcher-directed scope, old-to-new section/claim/asset mapping, bounded work and resumption, candidate handling when useful, and one explicit active manuscript. Reuse specialist skills rather than duplicating research/writing procedures. Preserve previous releases and detect intervening author edits before applying staged changes; recovery must not depend on Git.
- Input-versioned evidence/audit checks and affected-work tracking. Changed claims need renewed support checks even when citation keys still resolve. Mark affected downstream results stale; recheck narrative consistency across the whole manuscript without needlessly repeating unrelated valid checks. Missing analyses/results remain research gaps.

**Acceptance evidence:**

- Draft and revise in the chosen language with natural expression, handling required quotation/proper-name/bilingual exceptions explicitly. Check that a new session applies the correct scoped rules without adopting inferred ones.
- Change an asset/section order and verify links and the manifest; README, notes, and unselected drafts cannot leak into body assembly. A missing citation or unsupported claim produces a useful finding rather than a fabricated repair.
- Audit a planted contradiction and unsupported passage, then inspect the requested correction and preserved author edits. Simple wording changes do not trigger a full literature/course workflow.
- Exercise inline/display math, fractions, scripts, matrices or multiline structures, literal currency, and unsupported commands. Exercise a Mermaid diagram with non-ASCII and punctuation labels, a long label, and a syntax error. Inspect actual target rendering and relevant version support; local parser success alone does not prove GitHub behavior. Do not publish research material or use a new external preview service without the required confirmation.
- Adopt a representative Word manuscript containing figures, tables, equations, citation fields, and comments/revisions; verify content and links against the source and report unsupported pieces. Exercise another supported editable input and a PDF, unresolved bibliography entries, and a conflicting current draft. A bibliography entry alone is not claimed as acquired full text. Re-import preserves existing work without duplicate sections/assets.
- Directly request a substantial revision before any journal review exists. Change the argument and section structure, split/merge/move content, remove a figure, and incorporate an actual supplied evidence change. Inspect title/abstract/conclusion and relevant material/method/analysis consistency, bibliography/support, assets, cross-references, and the explicit active manifest. Do not fabricate results to complete the revision.
- Interrupt and resume in a fresh session; introduce an intervening author edit and interrupt application of a staged multi-file change. Verify detectable/recoverable state, no lost edit, earlier content recoverability, no accidental candidate assembly, and replacement of stale passed checks with accurate current results. Exercise this without Git and, when MVP 7 exists, with Git. Small edits create no compulsory revision records.

**Later integration checks:** MVP 6 must prove that a changed target profile or manuscript invalidates affected formatting/readiness results and produces a newly inspected output without overwriting a release. MVP 8 must reuse the same revision coordinator for reviewer-driven major changes and link truthful responses to the new manuscript; revision must remain usable independently of review rounds.

**Not yet:** a promise of journal layout compliance before MVP 6 or a substitute for unfinished research.

## MVP 6 — Journal choice, template-driven layout, and readiness

**Example request:** “Assess which journal fits, then format this manuscript using its rules and template and tell me what remains.”

**First skills:** `journal-selection`, `submission-assembly`, `submission-readiness`.

**Implement:**

- Current target-venue research and evidence-based fit/readiness analysis, separately from impact. Archive supplied guidelines and Word/LaTeX/PDF resources under the selected profile; resolve material conflicts and retain only confirmed interpretations as rules.
- A per-rule source/scope/implementation/check mapping, bibliography/CSL or equivalent style handling, profile templates and reusable scripts, explicit assembly inputs, and render–inspect–repair. Preserve the original resources; a PDF text extraction is not an executable layout template.
- A faithful source-math-to-OMML route for DOCX. Each authored manuscript formula must become correctly structured native editable Word math, including inline/display placement, tables/captions as used, and numbering/references. No silent image, plain-text, unparsed-LaTeX, or legacy-object fallback. Unsupported constructs identify the source location and unmet requirement.
- Mermaid-to-figure rendering for output formats that need image assets, preserving source, figure identities, captions, and suitable vector/raster quality. Keep conversion dependency setup on demand rather than a prerequisite for ordinary Markdown writing.
- Immutable release packages with source/profile/tool checksums or versions, build commands, assets, bibliography, and validation results. Previews remain rebuildable. The author receives files and a short passed/outstanding summary, not a technical configuration task.

**Implementation increments:** first prove one real or representative journal and one required output route. Then extend the declared output set to the planned Word, LaTeX, and PDF routes with appropriate templates, engines, fonts, and checks. Each route is advertised only after verification; the first working export does not establish all-format or arbitrary-journal support.

**Acceptance evidence:**

- Compare an actual rendered document with adopted rules: page/column layout, fonts, spacing, headings, captions, equations, citations, cross-references, and required metadata/anonymization when applicable. Fix discrepancies; an openable file alone does not pass.
- For the Word route, reconcile expected source formulas with native OMML structures in the relevant DOCX parts and inspect representative native editing and rendered math in Word when available. Include fractions, scripts, matrices, limits, alignment, numbering, and references. A template's existing math element, an unparsed string inside a math object, or a formula screenshot must not pass as a converted formula. Report the actual application and verification scope.
- Inspect generated Mermaid figures at publication size in each declared output route, including non-ASCII labels, fonts, arrows, clipping, captions, and references. A raw Mermaid block, missing image, or changed formula cannot be reported as a complete output. Unsupported conversion cases remain explicit failures of the affected requirement.
- Rebuild after a body edit and switch between a neutral and a journal profile without silently rewriting research content. Missing fonts, ambiguous instructions, unavailable renderers, limits, and unmet requirements are explicitly reported, not silently ignored.
- Inspect each declared output route and preserved release package. Readiness identifies a real remaining task/reviewer concern and gives grounded improvements, without an invented acceptance percentage or automatic external submission.
- Switch venues after a major revision and verify the new profile, content requirements, and actual output. Reuse only checks whose inputs/scope still apply; an old compliant package is not evidence that the changed manuscript passes. A format-only switch must not silently rewrite scientific claims.

**Not yet:** automatic fidelity to every possible template. Additional profiles and untested output/platform combinations remain explicit follow-up increments, not hidden assumptions.

## MVP 7 — Practical Git control and explicit backup

**Example request:** “Save this version, compare it with the earlier draft, and help me retrieve the old paragraph.”

**First skills:** `git-inspection`, `git-setup`, `git-save`, `git-compare`, `git-recovery`, `git-backup`, `git-hands-on`.

**Implement:**

- Direct agent-operated inspection/setup/saving/comparison/recovery and a guide that reuses these tasks. Inspect existing history first; never require a researcher to edit Git configuration or memorize commands.
- Scoped checkpoints and readable diffs, safe retrieval/practice copies, clear recovery scope and a way back, and correct exclusions. Do not blanket-ignore authoritative PDFs/templates, commit secrets, overwrite unrelated edits, or rewrite shared history as a lesson.
- A distinction between local history and an external copy, with destination/visibility configuration only for an explicit backup/sharing request. Test mechanical backup using disposable destinations; verify an actual remote provider separately before claiming that integration works.

**Acceptance evidence:**

- In a disposable workspace, directly inspect, save, compare, and retrieve selected content; also run the guided lesson. Confirm unrelated edits and current real work survive and the saved scope matches the request.
- Use test credentials and representative originals/assets to check actual tracked scope, including already-tracked material where ignore rules alone cannot help. Explain what is preserved locally in ordinary language.
- A local-save request sends nothing to a remote. An explicitly requested test backup has a checked destination and recoverable content; account access unavailable means unverified, not successful backup.

**Not yet:** mandatory branch/rebase training, publication of the research repository, or a claim that local Git history is an off-machine backup.

## MVP 8 — Review rounds and coauthor reconciliation

**Example request:** “Organize these comments, help me revise and respond, and incorporate the coauthor's Word changes safely.”

**First skill:** `review-response`. Extend ingestion, audit, assembly, and scoped version operations rather than copying their procedures.

**Implement:**

- Per-venue/per-round response items, manuscript/release references, and a response-to-change map. Reuse `review-ingestion` for originals and checked Markdown/assets; it remains independently usable without this response workflow. Keep formal review records distinct from source evidence and research feedback from collaborators or other contributors.
- Deliberate comparison/reconciliation of coauthor DOCX edits or tracked changes with canonical Markdown. Preserve the received document and current manuscript; surface conflicting content or unsupported suggestions for the researcher's judgment.
- Re-audit/re-export after agreed revisions and produce an honest point-by-point response. Editorial material is source input, not authority to modify project policy or fabricate a completed change.
- For major reviewer-driven changes, reuse `manuscript-revision` and link its baseline, plan, mapping, and checks from the round's response/change records. Keep one source for the actual changes rather than duplicating revision tracking per review item.

**Acceptance evidence:**

- Process two rounds for a venue without mixing item identifiers, decisions, or source manuscript versions. Each addressed item points to an actual change or a justified response; an unaddressed item is not marked complete.
- Exercise a structural or argument-level review request: revise with the same standalone coordinator, preserve the submitted baseline, check affected evidence and summaries, and link the response to actual revised passages. Missing new research is reported as incomplete.
- Reconcile a Word edit against a conflicting local change without losing either, then rebuild and inspect the affected output. Unknown or unsupported tracked-change handling must remain explicit.
- Preserve originals/assets and the prior release, keep metadata/source links intact, and send no response to an external party merely because a draft was prepared.

**Not yet:** autonomous journal correspondence or blind overwrite/import of a generated Word document into the manuscript.

## MVP 9 — Connected paper hands-on and release candidate

**Example request:** “Start from my research interest and guide me toward a journal-format paper, continuing from where we stopped.”

**First skill:** `paper-hands-on`. This coordinator selects existing independent skills; it adds no second implementation of their task rules.

**Implement:**

- Stage recognition, one useful next action, focused questions, shared-file handoffs, and concise resumable state. Support entry from an interest, an existing library, an idea, a draft, or reviewer comments. Do not force a fixed course on a direct task.
- Links to the Git guide at useful milestones and the review extension after actual comments exist. Keep scientific judgment, permitted uploads, account changes, and external submission decisions explicit.
- Final README/hands-on examples and a capability record stating which skills, services, output profiles, operating systems/architectures, and limitations have actually been verified. Keep implementation status distinct from researcher progress.

**Acceptance evidence:**

- Run a complete, clearly labeled test research scenario from literature to ideas, actual supplied evidence, manuscript, impact/journal assessment, template-driven output, and readiness. Exercise the review extension and a Git checkpoint without inventing research findings.
- Interrupt at meaningful points, start fresh sessions in both agents, and resume without losing confirmed requirements, repeating completed imports, or rebuilding a course from scratch. Try direct entry with an existing draft and a standalone version comparison.
- Inspect whether outputs are reused and context is scoped. No stage requires the researcher to edit technical formats; optional tools/services can be absent without making unrelated tasks unusable. Repair detected integration failures before claiming the connected path works.
- Record scientific decision/review effort separately from clerical work. No manual technical-file maintenance, copying between stages, routine failure diagnosis, or task-status reconstruction is required of the researcher. Investigate avoidable questions and work returned to the user; a long tutorial or a list of instructions is not evidence that the agent completed the requested production work.
- Apply the confirmed test-only boundary above: a bounded complete-path exercise does not narrow supported research or establish real publication readiness. Its result is a test report with explicit assertions and limits, not authorization to submit or publish the test package.

**Not yet:** an unqualified promise of every journal/format/platform or acceptance of any manuscript. The release states exactly what has passed and what requires further validation.

## 4. Complete skill-to-MVP assignment

This table assigns every proposed skill in design-plan Section 9 to its first implementation slice. Later MVPs may extend it; task procedures remain canonical.

| Skill | First MVP |
| --- | --- |
| `paper-hands-on` | MVP 9 |
| `git-hands-on` | MVP 7 |
| `project-onboarding` | MVP 1 |
| `privacy-configuration` | MVP 1 |
| `environment-management` | MVP 1 |
| `constraint-maintenance` | MVP 1 |
| `literature-discovery` | MVP 3 |
| `reference-download` | MVP 3 |
| `source-ingestion` | MVP 2 |
| `manuscript-import` | MVP 5 |
| `review-ingestion` | MVP 2 |
| `research-feedback` | MVP 4 |
| `literature-and-evidence` | MVP 3 |
| `research-ideation` | MVP 4 |
| `idea-deepening` | MVP 4 |
| `impact-assessment` | MVP 4 |
| `journal-selection` | MVP 6 |
| `research-planning` | MVP 4 |
| `research-investigation` | MVP 3 |
| `manuscript-outline` | MVP 5 |
| `manuscript-writing` | MVP 5 |
| `manuscript-audit` | MVP 5 |
| `manuscript-revision` | MVP 5 |
| `submission-assembly` | MVP 6 |
| `submission-readiness` | MVP 6 |
| `review-response` | MVP 8 |
| `research-code-setup` | MVP 4 |
| `git-inspection` | MVP 7 |
| `git-setup` | MVP 7 |
| `git-save` | MVP 7 |
| `git-compare` | MVP 7 |
| `git-recovery` | MVP 7 |
| `git-backup` | MVP 7 |

## 5. Cross-MVP invariants and verification

| Requirement that must survive every increment | Evidence to inspect |
| --- | --- |
| Ordinary-computer-user experience | A task completes through natural language; the researcher reviews meaningful results and never has to repair a technical file. |
| Every designed project directory explains its role | Inspect useful English READMEs in static and dynamic directories, including nested archives/assets/skills; exclude runtime dependencies and keep documentation out of manuscript and evidence inputs. |
| Explicit confirmation before major decisions | Inspect the concrete question, user answer and scope, blocked dependent changes while unanswered, and reuse of clear existing authorization. No silence/default approval or skill-specific exception. |
| Clear questions, including grilling | Inspect one substantive choice per question, a brief reason/recommendation, English STE rules and dictionary review, and natural non-English clarity without an English-compliance claim. |
| Codex/Claude parity with English agent instructions | Fresh-session discovery and task scenarios on both hosts; canonical/adapted skill consistency and no dependency on local maintainer-only paths. |
| Confirmed rules only | Persistence tests after explicit instructions and unconfirmed inferences; inspect all managed memory locations, not just the main writing file. |
| Advice, decisions, and active requirements stay distinct | Inspect attributed feedback, researcher adoption, actual changes, supersession, and scoped context loading. Advice and historical decisions do not silently become active instructions. |
| Integrity of research and citations | Inspect original/evidence locators, claim support, uncertainty, and known contradictions; no invented data, quotations, sources, or acceptance probabilities. |
| Markdown-centered, discipline/language flexibility | Preserve originals/native structures; test contrasting research scenarios and chosen-language prose without forcing one methodology or unintended language mixing. |
| Local secrets and explicit data processing | Inspect effective credential handling and exclusions, redacted diagnostics, upload scope, and per-service policy status. Local failure cannot silently broaden data transfer. |
| Reliable files and repeatability | Check identifiers, links, interrupted jobs, unchanged versus changed inputs/settings, preserved notes/releases, and safe migrations when representations change. |
| Recoverable major revision and current checks | Inspect the real baseline, preserved edits, old-to-new mappings, active/candidate separation, interruption recovery, and affected-check invalidation; a passed result belongs to its checked inputs and scope. |
| Actual rule-based typesetting | Requirement-to-implementation checks and rendered output inspection, including the relevant language, figures, numbering, and metadata. |
| GitHub math/Mermaid and native Word equations | Inspect actual Markdown target rendering, diagram syntax/version support, source-to-native-OMML mappings, mathematical structure, editability, and publication figures. No silent formula rasterization or claim that a generic export proves fidelity. |
| Windows baseline and optional heavy dependencies | Record the exact tested machine/architecture, paths, setup/runtime/resource observations, and capability envelope. macOS-only tests do not prove Windows or ARM64. |
| Independent tasks and connected guidance | Demonstrate direct requests and result reuse across skills, without copying procedures, loading every skill, or forcing unrelated setup. |

Use small rights-cleared fixtures with known expected outcomes. Label synthetic research examples clearly. Automate checks where deterministic failures threaten data, links, credential handling, import completeness, or truthful build success; combine them with actual agent-task and visual-output checks. Do not add tests that merely mirror a low-impact documentation edit.

A test double can prove error handling, but not a live API or privacy control. A local disposable remote can prove Git mechanics, but not access to an online backup provider. Record unavailable external evidence as unverified. A reviewer should be able to tell which claims were demonstrated and which remain assumptions.

## 6. Completion record for each MVP

During implementation, maintain a short agent-edited status record, for example `docs/implementation-status.md`, with one entry per MVP. Do not create empty status/process files until they are useful. Record:

- Status: planned, in progress, or verified; use precise partial/unverified notes when only part of the outcome exists.
- Researcher request, implemented skill/version and changed artifacts, decisions resolved, and actual supported capability scope.
- Test scenarios and environment, commands or operations actually performed, result/output locations, and inspection evidence, redacted as needed.
- Failures/limitations, affected behavior, what remains, and the next actionable task.

Mark an MVP verified only when its stated researcher outcome and acceptance evidence are satisfied. Do not infer completion from a checkbox, green command, README claim, or the presence of a SKILL.md. If a chosen initial slice is narrower than the full MVP, label it as that partial increment and keep the remaining requirements scheduled.

Before a release, reconcile this assignment table with the current skill catalog, inspect every declared capability, and update the README/hands-on status. Additional journal profiles, remaining output routes, other OS/architecture combinations, or new integrations can be delivered in later increments, but must not be advertised as working before they are verified.
