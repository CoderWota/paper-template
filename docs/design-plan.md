# Agent-Assisted Research Writing Framework: Design Plan

Status: discussion draft v0.9. Confirmed design decisions are identified below. Implementation has started with the workspace scaffold; [implementation status](implementation-status.md) records what exists.
Updated: 2026-10-26.

## 1. Intended outcome

Provide a cloneable, file-based workspace that lets researchers and agents develop a manuscript efficiently across sessions. Preserve researcher intent, connect claims to retrievable evidence, and assemble reviewable submission artifacts.

The framework is discipline-agnostic. Give researchers an organized project workspace without requiring them to invent its structure. Its value also lies in professional agent interaction: selecting appropriate skills, conducting iterative investigation and retrieval, testing reasoning, and carrying multi-step work through to inspectable artifacts.

Support Codex and Claude Code through shared policies and reusable skills. Avoid a dependency on a particular model, proprietary service, vector database, or programming background.

The intended researcher has ordinary computer literacy and no assumed coding or software-engineering knowledge. Technical project maintenance is performed through the agent; scientific understanding and decisions remain with the researcher.

The researcher is the intellectual lead and final scholarly editor: they primarily contribute ideas, domain observations and available material, assess meaning, and confirm major choices and final content. They are not the agent's workflow dispatcher or clerical operator. Within the confirmed scope, the agent owns feasible delegated retrieval, material preparation, research support, drafting, verification, formatting, and recovery. Direct human writing remains available, not a prerequisite for routine progress. Actual scientific work and author review remain necessary; execution capabilities still need implementation and demonstration.

This is a workspace template, not a promise of autonomous scientific discovery or guaranteed publication. Research judgment and authorship remain with the researcher.

## 2. Requirements supplied by the template maintainer

- Use Markdown to manage text for agent reading, analysis, retrieval, and manuscript writing.
- Give every designed project directory a `README.md` explaining its purpose, including nested, hidden skill, asset, archive, and dynamically created item directories. The agent creates and maintains it with the directory. Generated runtime caches, virtual environments, and third-party dependency trees are outside the project-directory scope.
- Archive original reference documents separately from extracted Markdown and image assets. Include possible references, not only cited works.
- Persist writing constraints, styles, and evolving researcher requirements across sessions.
- Keep venue requirements and final-format resources inside the writing specification area. Accept Word, LaTeX, or PDF source resources.
- Keep manuscript text in its own directory, with no more than one Markdown file per chapter or major section, and a dedicated assets directory.
- Preserve researcher ideas separately from finished manuscript prose.
- Archive reviewer correspondence per venue, retaining originals and extracted Markdown/assets.
- Assemble final outputs into a dedicated directory through reusable skills.
- Persist reusable workflow scripts. Let agents manage a project-local Python virtual environment when scripts need it.
- Support an optional research code directory with a skill that elicits requirements before choosing its structure.
- Guide non-programmers through missing prerequisites and reuse suitable installed CLI tools.
- Discuss AGENTS.md carefully before finalizing it. Support both Codex and Claude Code.
- Write agent-facing Markdown in English. Decide manuscript language with each researcher, and produce natural prose without unintended language mixing.
- Use MinerU as the selected document parsing tool. Let each researcher choose local processing or cloud parsing for complex PDFs.
- Persist writing rules only after verification and researcher confirmation. Do not save agent-inferred preferences as candidates in project files.
- Do not restrict disciplines or gate access by article type. Adapt the shared workspace and skills to the researcher's project.
- Treat a lightweight Windows laptop, such as a Surface, as the minimum deployment environment. A dedicated GPU or heavy local inference stack must not be required for basic use.
- Provide a skill that helps researchers configure their AI applications and service accounts to opt out of model-training use where supported, and verifies or clearly qualifies the result.
- Guide researchers through project-local OCR/API credential setup during initialization, according to their selected service; they must not need to understand environment variables or edit scripts.
- Make the root README explain the repository's design philosophy and everyday use. Keep developer-oriented architecture and operational details in supporting documentation.
- Provide straightforward single-file and batch PDF-to-Markdown ingestion through a skill, invoked in ordinary language.
- Provide a skill that helps generate creative research ideas and deepen existing ideas, drawing on the focused, sequential questioning approach of grilling.
- Treat researchers as ordinary computer users. Require no manual maintenance of Git configuration/history operations, BibTeX files, YAML/JSON configuration, scripts, or other technical project files; the agent edits and validates these in response to natural-language requests.
- Provide an agent-led paper hands-on skill covering literature collection from scratch, idea organization and development, research impact, journal prospects, and an evidence-based manuscript assembled for a selected journal.
- Provide a separate Git hands-on skill that helps researchers use version history through practical, guided actions without requiring command-line or software-engineering knowledge.
- When formatting requirements or reference templates are supplied, the agent must apply the adopted rules to the assembled manuscript and verify the actual output, rather than merely convert file formats.
- Expose the hands-on stages as independently usable skills. Retain the paper/Git guides as coordinators so a researcher can choose one task or follow a connected path without repeating earlier stages.
- Provide an intake directory and flexible skills for adopting an existing manuscript, batch downloading references, converting downloaded literature into the indexed library, and extracting reviewer correspondence from Word and other supported formats.
- Obtain explicit user confirmation before every major decision; do not commit the choice before confirmation. Clear existing instructions can provide that confirmation within their stated scope.
- Apply ASD-STE100 to English agent questions and their supporting instructions, including grilling. Preserve the chosen interaction language; use the corresponding clarity principles for other languages without claiming English-standard compliance.
- Write Markdown mathematics in GitHub-renderable LaTeX syntax and use valid Mermaid for agent-created explanation diagrams. Export manuscript formulas to Word as native, editable equations, with faithful mathematical structure and actual rendering checks.
- Accept attributed research feedback from co-researchers, collaborators, coauthors, supervisors, and other contributors; do not restrict feedback to professors, academic titles, or established authorship roles.
- Center the researcher's work on ideas, scholarly judgment, and authorship. The agent handles routine research/writing production and coordination where feasible and authorized, rather than requiring the researcher to do clerical work or route each skill and file by hand.
- Use a bounded complete path from idea/materials through actual results and supported writing to a checked submission package as a core framework test. This is a test scenario, not a restriction on the framework's disciplines, research types, materials, or scale, and not evidence of real publication readiness.

## 3. Proposed scope and boundaries

Confirmed: one workspace manages one main manuscript, including its submission rounds and revisions. Each additional paper uses its own copy of the workspace. Support different article types through configuration rather than pre-created discipline-specific directory trees.

No discipline or article-type allowlist applies. Elicit the research question, material types, methods, argument structure, and output requirements when needed, then adapt the workspace. Do not force researchers to choose an ill-fitting category or invent a code project for work that does not involve code.

The shared framework organizes work and routes skills; methodological requirements come from the researcher's confirmed instructions, applicable reporting guidance, and task-specific resources. Specialized procedures can be added when needed without making a discipline unsupported by default.

The baseline assumes an installed, usable agent host and access to its model. It does not require running that model on the laptop. Document conversion, retrieval, export, and optional research computation have separate capability requirements.

Keep drafting, evidence checking, formatting, and external submission distinct. An export is not automatically a submission-ready or researcher-approved artifact.

Do not hard-code IMRaD, English prose, a citation style, or a target journal. Record these choices during onboarding. A project without a target venue can use a neutral output profile.

### Researcher-facing experience

The researcher describes an objective; the agent selects the workflow and handles technical execution. For example: initialize this paper project; import all PDFs in this folder; explore possible research directions from these readings; examine the weaknesses of this idea; revise this section using my confirmed requirements. These are intended interaction patterns, not claims that the skills are already implemented.

Initialization should establish only what is needed to begin: the researcher's goal and language, an appropriate workspace, the selected parsing mode, and any required credentials. Unknown research directions or venues can remain undecided. Ask focused questions as they become relevant instead of administering a long technical questionnaire.

Use clear defaults for folders, identifiers, retries, and routine settings. The researcher should not have to choose YAML schemas, parser flags, environment layouts, or citation keys to get started. The agent owns those mechanics and presents meaningful research, privacy, and cost choices when they matter.

The root README should explain why the workspace exists, how material and confirmed requirements are organized, how to get started with an agent, examples of common requests, and what to do when work cannot proceed. Keep a short, approachable directory map. Every maintained directory README should explain what to put there and what the agent manages. Detailed architecture, CLI references, and metadata specifications belong in supporting developer/agent documents. Distinguish design previews from working functionality until implementation exists.

### Responsibilities and guided interaction

Researchers express goals, discuss scholarly judgments, review prose and evidence, and confirm meaningful choices. They may write or revise manuscript text and ideas directly. They are not expected to edit technical project representations to make the workflow function.

They also should not have to copy intermediate outputs between tools, manually compile source/evidence tables, coordinate each next skill, diagnose routine failures, or maintain task status. The agent prepares concrete options before a consequential question and continues routine approved work to a reviewable outcome. Ask for human-only material, access, actions, and scholarly judgment when genuinely needed; do not transfer feasible agent work back as a generic instruction to the researcher.

The agent maintains Git operations/configuration, `.bib` metadata, YAML/JSON settings and manifests, scripts, environment configuration, indexes, and machine-managed records. Explain changes in terms of their research effect and verify syntax and relevant links or output. For example, the researcher says change the citation style or preserve this version; the agent updates the necessary files or performs the version operation. Do not hand the researcher a configuration snippet and treat that as completing the change.

Guide one manageable action or decision at a time. Explain its purpose briefly, perform supported actions, and show the visible result. If only the researcher can complete a step, such as sign-in or private credential entry, provide concrete instructions appropriate to the actual interface and resume afterward. No routine memorization, programming exercises, or technical quiz is required.

A short human-readable entry guide must cover obtaining the project folder and opening a usable agent host. Skills cannot perform steps before the agent is available; do not make agent-assisted initialization circular. Detailed host-specific installation steps must be verified when written rather than guessed.

The hands-on workflow design is documented in [hands-on.md](hands-on.md). It describes planned skills, not implemented commands.

The [research workflow review and public knowledge transfer](research-workflow-review.md) audits whether the design carries an idea through actual research results to a checked submission package. The researcher/agent division and complete-path testing objective are confirmed. The bounded case is only a test; detailed execution, storage, and implementation-priority proposals still need discussion and do not silently change the skill catalog, roadmap, or general product scope.

## 4. Proposed directory structure

The tree shows representative files and explicitly includes a `README.md` at every directory level. The same rule applies to additional project directories created later. The repository scaffold now contains this tree's static directories; instance directories such as `<source-id>/` and optional ones such as `code/` are created when needed. The layout remains a proposal under discussion.

```text
.
├── AGENTS.md                                      # Shared, concise operating contract
├── CLAUDE.md                                      # Compatibility entry importing AGENTS.md
├── README.md
├── CONTEXT.md                                     # Domain glossary only
├── .agents/
│   ├── README.md
│   └── skills/                                    # Canonical portable skill packages
│       ├── README.md
│       └── <skill-id>/                            # One task package
│           ├── README.md
│           └── SKILL.md
├── .claude/
│   ├── README.md
│   └── skills/                                    # Generated, validated Claude adapters/mirrors
│       ├── README.md
│       └── <skill-id>/                            # One task package
│           ├── README.md
│           └── SKILL.md
├── inbox/                                         # Optional, mixed-material intake; no presorting required
│   ├── README.md
│   └── imports/
│       ├── README.md
│       └── <import-id>/                           # Received originals, import mapping, unresolved items
│           └── README.md
├── references/
│   ├── README.md
│   ├── index.md                                   # Compact discovery index
│   ├── bibliography.bib                           # Proposed canonical citation metadata
│   ├── originals/
│   │   ├── README.md
│   │   └── <source-id>/
│   │       └── README.md
│   ├── extracted/
│   │   ├── README.md
│   │   └── <source-id>/
│   │       ├── README.md
│   │       ├── document.md
│   │       ├── assets/
│   │       │   └── README.md
│   │       ├── provenance.json
│   │       └── native/                            # Parser JSON and other original outputs
│   │           └── README.md
│   └── notes/
│       ├── README.md
│       └── <source-id>.md                         # Interpretation and evidence notes
├── requirements/
│   ├── README.md
│   ├── project.md                                 # Purpose, contribution, audience, article type
│   ├── writing.md                                 # Active writing rules and terminology
│   ├── privacy.md                                 # Confirmed processing choices and data-use requirements
│   └── profiles/
│       ├── README.md
│       └── <profile-id>/
│           ├── README.md
│           ├── requirements.md                    # Human/agent-readable requirements
│           ├── profile.yaml                       # Executable export configuration
│           ├── originals/                         # Supplied guidelines and format examples
│           │   └── README.md
│           └── templates/                         # DOCX, CSL, LaTeX classes/templates, etc.
│               └── README.md
├── manuscript/
│   ├── README.md
│   ├── outline.md                                 # Outline, not a second body-text copy
│   ├── manifest.yaml                              # Explicit section order and inclusion
│   ├── 01-introduction.md                         # Illustrative, not a required structure
│   └── assets/                                    # Figures, tables, captions, provenance
│       └── README.md
├── ideas/
│   ├── README.md
│   └── index.md
├── research/                                      # Proposed research rationale and collaboration records
│   ├── README.md
│   ├── decisions/
│   │   ├── README.md
│   │   ├── index.md                               # Confirmed decisions, scope, and supersession links
│   │   └── 0001-short-title.md                    # Create only for a consequential confirmed choice
│   └── feedback/
│       ├── README.md
│       └── <feedback-id>/
│           ├── README.md
│           ├── originals/                         # Research feedback and meeting material
│           │   └── README.md
│           ├── extracted/
│           │   ├── README.md
│           │   ├── markdown/
│           │   │   └── README.md
│           │   └── assets/
│           │       └── README.md
│           └── actions.md                         # Attributed advice, researcher choices, actual progress
├── reviews/
│   ├── README.md
│   └── <venue-id>/
│       ├── README.md
│       └── <round-id>/
│           ├── README.md
│           ├── originals/
│           │   └── README.md
│           ├── extracted/
│           │   ├── README.md
│           │   ├── markdown/
│           │   │   └── README.md
│           │   └── assets/
│           │       └── README.md
│           ├── response.md
│           └── changes.md
├── revisions/
│   ├── README.md
│   └── <revision-id>/                             # Proposed, created only for a substantial revision
│       ├── README.md
│       ├── plan.md                                # Goal, baseline reference, scope, impact, next work
│       ├── changes.md                             # Old-to-new content mapping and actual changes
│       ├── checks.md                              # Checked input versions, results, remaining gaps
│       └── candidate/                             # Optional staged manuscript, outside active assembly
│           └── README.md
├── outputs/
│   ├── README.md
│   ├── preview/                                   # Rebuildable previews
│   │   └── README.md
│   └── releases/
│       ├── README.md
│       └── <release-id>/                          # Preserved submission packages
│           └── README.md
├── scripts/                                       # Reusable workspace automation
│   └── README.md
├── code/                                          # Optional research implementation
│   └── README.md
├── state/
│   ├── README.md
│   └── current.md                                 # Concise handoff and unresolved work
└── docs/                                          # Framework documentation and design
    ├── README.md
    ├── agent-interaction.md                       # Major decisions and question rules
    └── markdown-and-export-conventions.md         # GitHub math, Mermaid, native Word math
```

### Directory README contract

Every designed project directory has its own meaningful English `README.md`. This includes intermediate grouping directories and concrete instances such as each source archive, output profile, feedback event, review venue/round, revision, release, and skill package. Optional directories are created only when needed, together with their README. Human-facing translations can supplement the English version.

Keep each README short and specific to its directory. Explain:

- What the directory is for and what belongs there.
- What the researcher can provide or edit, and what the agent maintains.
- Which contents are originals, derived files, active work, or preserved history, as applicable.
- Important child directories, related records, and the useful next request or skill.
- Any relevant rebuilding, preservation, or access constraints, by linking their authoritative requirements rather than copying them.

The skill or operation that creates a project directory also writes its README. Update it when the role or layout changes. Dynamic creation and repeat runs must preserve existing meaningful descriptions and researcher additions. Generate a release README before freezing the package. Add directory documentation without modifying received original files; do not write READMEs into unrelated external input folders or third-party installations.

README files describe the workspace. Keep them out of manuscript assembly, literature evidence, and extracted reviewer items through explicit manifests and content roles. Skill-package READMEs introduce the task and link to SKILL.md without duplicating its procedure. Agents read relevant directory descriptions as needed rather than loading all READMEs into every session. Runtime caches, virtual environments, and installed dependency trees are not designed project directories.

Implementation checks cover both README presence and useful directory-specific content, including newly created instance directories. A generic placeholder in every folder does not satisfy the purpose requirement.

Avoid maintaining the same fact manually in multiple places. The bibliography owns citation metadata; the source index aids discovery; evidence notes own interpretations and support relationships; the section manifest owns assembly order.

`research/decisions/` replaces the earlier single `requirements/decisions.md`. It owns decision rationale and history; `requirements/` owns the current confirmed requirements and links back when useful. The `research/decisions/` and `research/feedback/` locations are confirmed; their record formats are refined in MVP 4.

Plain Markdown is the text interface, not a ban on structured formats. BibTeX, YAML, JSON, images, data, and original documents complement it where they prevent ambiguity or loss.

## 5. Document ingestion: MinerU decision and publishing options

These findings come from official documentation reviewed on 2026-10-25, not local comparative benchmarks. Versions and backend contracts must be verified again during implementation.

| Tool | Documented role | Decision or proposed place in this framework |
| --- | --- | --- |
| [MinerU](https://github.com/opendatalab/MinerU) | Current 4.0 documentation describes document parsing, OCR, document-library search, page/block continuation, and citation locators. | Selected parser. Support local use and researcher-selected cloud parsing; validate the chosen integration on the Windows baseline. |
| [MarkItDown](https://github.com/microsoft/markitdown) | Python/CLI conversion across Office, PDF, HTML, and other formats with optional dependencies. | Previously considered; not selected as the default or an automatic fallback. |
| [Docling](https://github.com/docling-project/docling) | Structured conversion including PDF layout, reading order, tables, formulas, and Markdown/JSON export. | Previously considered; not an additional required parser. |
| [Pandoc](https://pandoc.org/MANUAL.html) | Markup/document conversion, citations, templates, and DOCX/LaTeX/PDF output routes. | Proposed manuscript assembly foundation, separate from reference extraction. |
| [Quarto](https://quarto.org/docs/journals/templates.html) | Article templates and a broader publishing workflow. | Optional alternative publishing layer if its manuscript features justify the extra conventions. |
| [GROBID](https://github.com/grobidOrg/grobid) | Scholarly document structure and bibliographic extraction into XML/TEI. | Later optional metadata enrichment; not required for basic writing. |

Confirmed decision: use MinerU for supported document parsing. Read existing Markdown and plain text directly. Keep the workspace lightweight by separating the parser selection from where parsing runs: local processing when appropriate, or an explicitly selected cloud service for complex PDFs. A full local model stack is not required merely to initialize the workspace or use a remote service. Choose the smallest documented client/integration that meets the task; verify its actual dependencies rather than assuming the full MinerU package is lightweight.

Recommend a MinerU processing mode and quality tier based on the document and available capabilities. The framework supports cloud processing, but this does not authorize uploading any particular researcher's documents. Record each researcher's selected service, permitted document scope, and processing mode. Reuse that choice within its confirmed scope; revisit it when the service, scope, cost, or data-use conditions change materially. Do not silently switch a failed local parse to cloud or to another parser. Unsupported input or inadequate extraction must remain visible.

The exact cloud provider/API, account requirements, pricing, retention policy, training-use policy, and client capabilities remain integration details to verify. Do not infer them from the local open-source parser. Use a dedicated publishing system for the authored manuscript; Pandoc versus Quarto remains open.

### MinerU-specific findings that affect the design

- The current [quick start](https://opendatalab.github.io/MinerU/quick_start/) targets 4.0, requires Python >=3.10,<3.15, and distinguishes `mineru` library workflows from stateless `mineru-kit` conversion. Older command recipes must not be assumed compatible.
- `mineru parse` defaults to the first ten PDF pages and can require continuation. `mineru-kit parse` defaults to all PDF pages. The adapter must explicitly verify coverage instead of interpreting a successful command as a complete import.
- The [tier documentation](https://opendatalab.github.io/MinerU/usage/tiers/) distinguishes native/preview Flash, model-based Basic, and VLM-backed Standard/Advanced. CPU operation is possible; throughput, memory, and setup vary by tier and runtime. Do not promise GPU-free high-throughput processing.
- Model-backed parsing can download weights on first use. Installation must describe the selected runtime, download requirement, and local/remote execution mode before starting expensive setup.
- Its [output contract](https://opendatalab.github.io/MinerU/reference/output_files/) distinguishes command-response JSON, intermediate JSON, and structured content. Export options depend on the entry point. Preserve native outputs and actual asset links rather than assuming a fixed filename pattern.
- MinerU's renderers can produce several document formats, but that does not establish compliance with an arbitrary journal's authored-manuscript format. Keep ingestion and manuscript publishing separate.
- The current [license file](https://github.com/opendatalab/MinerU/blob/master/LICENSE.md) identifies Apache 2.0 with additional terms. Evaluate the selected distribution, model licenses, and intended redistribution before bundling; do not label it unqualified Apache 2.0.
- Its published agent guidance is a useful reference, not automatic project policy. Do not install global skills, change global preferences, or adopt upstream mandatory-tool rules merely because a README recommends them.

### Integration contract

Use upstream packages or existing compatible CLI installations, with a thin project-owned adapter for paths, provenance, coverage, and checks. Avoid copying or forking an entire upstream project into the template.

Each import records source ID and original checksum, converter/version, settings or tier, execution mode, time, expected and processed page coverage where measurable, output paths, and warnings. Preserve unknown coverage explicitly. A partial extraction must remain visibly partial.

Normalize asset links into the project layout without breaking references. Keep parser-native JSON for provenance and structured retrieval; use a small normalized metadata layer rather than pretending all parsers return equivalent structures.

Use a temporary destination and publish the completed extraction atomically. Re-running an unchanged import should reuse a matching result. Re-conversion must preserve researcher notes and any reviewed corrections separately.

### Simple batch PDF-to-Markdown workflow

The entry point is a request such as: import all PDFs from this folder into the reference library. A researcher can select a file or folder without knowing MinerU commands or skill names. The same ingestion skill handles one document and a batch; it should not require a separate procedure for each file.

Proposed behavior implementing the confirmed usability requirement:

1. Identify the requested files and destination. Show the file count and relevant processing choice; do not scan unrelated folders or ask the researcher to name every output file. Resolve subfolder inclusion consistently and state the scope.
2. Reuse project-local initialization settings. If credentials or a required tool are missing, invoke the setup workflow and resume the batch afterward. Do not ask for the same service or upload permission for every file within the confirmed scope.
3. Archive originals without changing the source files, run MinerU, save Markdown and associated images, retain provenance, and update the reference index automatically. Validate processed coverage and local asset links. The researcher-facing result should be readable Markdown with working images; parser-native metadata stays in the background.
4. Track each document independently. Skip a matching completed import, preserve successful results, and retry only unfinished or failed work. Respect provider batch/rate limits and use conservative local concurrency. Authentication or quota failures should produce an actionable batch-level explanation rather than repeated requests for every document.
5. Report a short summary with counts for converted, already imported, failed, and requiring review, plus links to results. Distinguish conversion completion from verified extraction accuracy. Let the researcher say retry the failed documents or check the flagged figures, without editing a manifest or reading a stack trace.

Keep the orchestration proportionate: reusable scripts and resumable local records are sufficient unless real workloads demonstrate a need for additional infrastructure. Full technical logs can be available for diagnosis, with credentials redacted; they are not the default user output.

### Flexible intake and existing-manuscript adoption

The intake and import capabilities are confirmed requirements; the following layout and skill boundaries are proposed. `inbox/` is an optional landing area for mixed files, folders, and reference lists. Researchers can instead point to an existing folder or provide files directly. The agent uses the request and inspected content to propose destinations; ask about ambiguous roles or consequences rather than making the researcher preclassify every file. An author's draft, a reference article, a journal template, and reviewer comments may all be PDFs but require different handling.

Preserve received originals and a concise import record linking input, checksum, role, destination, conversion status, and unresolved items. References and formal reviews retain their authoritative originals in their own archives; manuscript originals remain in the import archive. Avoid redundant archival copies when a stable existing archive already serves the role. Do not alter external input files or automatically clean the intake area. Drafts and intake records stay outside manuscript assembly unless explicitly adopted.

`manuscript-import` adopts an existing Word, LaTeX, Markdown, PDF, or other verified supported manuscript into workspace conventions. Prefer available editable sources over reconstructing a PDF; use MinerU for supported document extraction and format-aware handling where native structure matters. Inventory sections, figures, captions, tables, equations, notes, bibliography/citation fields, and comments or revisions before migration. Preserve the selected language and scientific content; conversion is not an instruction to rewrite the paper or treat imported claims as verified findings.

Produce a section/asset/citation mapping and a reviewable migrated draft, respecting the maximum of one Markdown file per major section. Resolve references against actual source records; retain unresolved markers and bibliography entries without inventing matches or claiming a listed reference's full text is present. Flag conversion loss, missing images, ambiguous equations, Word citation fields, comments, and tracked changes. Verify against the source and rendered pages where needed. If a working manuscript exists, compare or stage the import separately; never silently replace it, accept every tracked change, or merge competing drafts. Clearly scoped adoption requests need no repeated approval.

### Batch reference acquisition and library handoff

`reference-download` accepts a selected reading list, DOI/URL list, BibTeX or other supported reference export, or references extracted from an existing manuscript. Resolve identities and obtain accessible full text through appropriate publisher, repository, preprint, or researcher-authorized institutional routes. Source discovery and metadata lookup alone do not count as downloading a document. Prefer authoritative, relevant versions and preserve links among preprints, accepted manuscripts, and published editions.

Use conservative concurrency, service limits, resumable per-item progress, and checksum/identifier deduplication. Validate the retrieved content so a login page or error response is not archived as a successful PDF. Record retrieval URL, date, identifiers, version, and access outcome without saving credentials or secret-bearing links. Report downloaded, already present, metadata-only, login/manual-access needed, unavailable, and failed items honestly. Do not bypass access controls or promise that every listed paper is downloadable.

A request to download and import chains `reference-download` into `source-ingestion` for available files: archive, MinerU conversion, assets, metadata, index, and concise linked results. Download-only and convert-existing-files requests also work independently. Successful downloads survive conversion failures and vice versa; retry only the affected stage. Reuse confirmed cloud processing choices within scope, but a download request alone does not authorize uploading the downloaded papers or an unpublished manuscript to a new service.

### Reviewer and collaborator document extraction

`review-ingestion` archives and extracts formal editor/reviewer documents into `reviews/<venue-id>/<round-id>/`, including the requested `extracted/markdown/` and `extracted/assets/` structure. Establish venue, round, and source manuscript version from available context; ask only when missing or ambiguous. Preserve reviewer labels, original item numbering, page/line references, images, tables, and source locators. Extraction can be requested without drafting responses or editing the manuscript.

Word comments and tracked changes, PDF annotations, and main document text are distinct structures. Use documented format-aware extraction/inspection when MinerU text conversion does not preserve them; keep unsupported structures explicit. Never report all comments captured merely because a Markdown file was generated. `review-response` consumes checked extraction later. Advice from co-researchers, collaborators, coauthors, supervisors, and other contributors uses the same conversion mechanics under `research/feedback/`, without inventing a journal review round or treating suggestions as adopted requirements.

## 6. Source identity, retrieval, and evidence

Use a stable source ID independent of filenames, title corrections, and bibliography citation keys. Detect exact duplicates with checksums; treat preprints, accepted manuscripts, and published versions as related versions rather than silently merging them.

Record title, authors, date, identifiers when known, source type, original path, extraction path, and reading status. Represent unavailable full text, uncertain metadata, and extraction failure honestly. A source can be collected, screened out, relevant, or cited without moving its original file between folders.

Default retrieval sequence: inspect the compact index, search relevant extracted Markdown, read matching sections, and verify consequential claims against the original or a trustworthy locator. Avoid loading the full library into every session. Add semantic indexing only if demonstrated retrieval needs justify it; any index remains rebuildable.

Keep extraction text separate from agent summaries. Evidence notes identify supporting passages, scope and limitations, contradictory sources, and verification status. An abstract-only record cannot substantiate uninspected full-text results.

Page numbers need an explicit convention: distinguish PDF page index from printed page labels. Parser block identifiers are tied to the extraction revision unless stability across reprocessing has been established. Never invent a missing page or locator.

Do not invent references, quotations, data, experiments, or results. A well-formatted citation is not proof that its source supports a claim. Citation metadata verification and evidence verification are separate checks.

## 7. Confirmed writing requirements and durable memory

Confirmed persistence boundary:

- Persist only verified, researcher-confirmed rules with clear scope and meaning. An explicit, unambiguous researcher instruction is confirmation; do not ask the researcher to approve the same instruction again.
- An agent-inferred preference must be discussed and confirmed in conversation before it becomes a persistent rule. Do not create a candidate-preference file or save such inferences in notes, handoff state, skills, or another file under a different label.
- If confirmation is missing, keep the inference in the current conversation only; do not apply it as an established preference. Losing that inference when the session ends is preferable to contaminating future context.

Supporting recommendations, still open for discussion:

- Record material decisions with a concise rationale and scope. Avoid preserving full chat transcripts as the default memory system.
- Distinguish project-wide rules, section-specific rules, venue-profile rules, and one-time edit requests.
- Track superseded or conflicting rules rather than accumulating contradictory commands. Resolve material conflicts with the researcher. Decided 2026-10-26: `requirements/` keeps only active rules; a consequential replacement also gets a research decision record, and minor changes rely on version history.
- Keep stylistic learning separate from new scientific claims. Novel interpretations remain proposals until supported and accepted in context.

This boundary applies to behavioral and writing rules, not to all project content. Researcher-expressed ideas can be recorded as ideas; literature notes can record supported findings, uncertainties, and research hypotheses with clear status. None of these automatically becomes an instruction or a verified scientific conclusion.

Learning means refining confirmed requirements and improving execution based on checked outcomes and researcher feedback. It does not authorize the agent to rewrite the operating contract or create new mandatory workflows from its own guesses.

Rules should capture intent and useful examples, including allowed exceptions. Avoid broad lexical bans that degrade meaning or natural expression.

Record manuscript language, interaction language, and any permitted language-specific artifacts separately. English agent instructions do not require English prose. Quotations, proper names, bibliography titles, and required bilingual abstracts need explicit exceptions rather than crude language-purity checks.

Confirmed: records the researcher reads and confirms (requirements, ideas, source notes, decision and feedback records, revision plans, and project state) use the researcher's interaction language, with quotations in their original language. Agent-facing files and technical metadata stay in English.

### Research decision and feedback records

Borrow the rationale-preserving idea of ADRs, but call the researcher-facing artifact a **research decision record**. Its location, `research/decisions/`, and the feedback location, `research/feedback/`, are confirmed. The record content described below remains a recommendation refined in MVP 4, not a mandatory process. Keep framework-maintainer architecture decisions separate; a future `docs/adr/` is appropriate only when an actual consequential technical tradeoff warrants a record. Researchers need not learn ADR terminology or maintain a software-engineering process.

Record a confirmed research choice when revisiting it would be costly, its rationale matters, and meaningful alternatives or tradeoffs existed: for example, narrowing a research question, choosing a method, setting corpus/inclusion boundaries, excluding an analysis, or changing a substantial argument. Ordinary wording edits, routine imports, and file renames do not warrant individual records. Create records lazily and let the agent maintain them through existing planning/constraint workflows rather than adding a skill for every bookkeeping step.

A short record captures date, researcher-confirmed choice and scope, context, reasons and relevant alternatives, supporting evidence or feedback links, and consequences for research/manuscript work. Add replacement links when a later confirmed decision supersedes it; preserve earlier rationale. A decision is not proof that the chosen method or claim is scientifically valid. Current operating requirements remain in `requirements/`; scientific results remain with their evidence. Do not duplicate active rules in every record or load all historical records into every session.

Keep research feedback as attributed source material, separate from decisions and active requirements. It can come from co-researchers, collaborators, coauthors, supervisors, or other contributors, regardless of academic title or authorship status. Retain received documents or researcher-supplied meeting notes, the date/source, actual advice, affected passages, open questions, and requested follow-up. When a document or meeting contains several people's suggestions, preserve each suggestion's attribution rather than merging them into a single person's opinion. Distinguish exact statements, researcher recollections, and agent summaries. A record may say received, under discussion, adopted in part, declined, or implemented, with links to actual decisions/changes. Receiving advice is not the researcher's acceptance of it, and adoption is not implementation.

`research-feedback` helps interpret advice, compare it with evidence and existing requirements, identify conflicts, and propose next actions. Promote a change to a lasting rule or consequential decision only when the researcher confirms it; an explicit instruction to apply specified feedback is already confirmation. Conflicting contributors' suggestions or a template conflict require a scoped researcher choice; do not assign priority merely by title, seniority, or authorship. Agent-inferred preferences cannot be stored as feedback. A collaborator-supplied paper structure is preserved as advice until adopted, then reflected in the outline or scoped requirements. Do not force every suggestion into a full decision record.

## 8. AGENTS.md and tool compatibility

AGENTS.md should be a concise operating contract and routing guide. It should not contain the complete style guide, source catalog, session history, every skill, or all venue rules.

Proposed contents for discussion:

1. Researcher authority, project purpose, and the location of active writing requirements.
   Major decisions require prior explicit user confirmation; preparing a proposal is distinct from adopting it.
2. Minimal session orientation: current project state and only the documents relevant to the requested task.
3. Evidence, citation, uncertainty, and research-integrity rules.
4. Boundaries between archived originals, extraction outputs, researcher notes, manuscript sources, and generated exports.
5. How confirmed constraints are persisted, updated, and reconciled; inferred preferences require conversation confirmation before persistence.
6. Task-to-skill routing and deterministic validation commands.
7. Dependency and environment selection, including reuse of installed tools.
8. Completion reporting and a concise handoff when work remains.

The maintainer adopted [AGENTS.md](../AGENTS.md), which follows this outline, on 2026-10-26, after deciding the workspace scope, research-record locations, record language, and skill adapters (Section 15, items 3, 17, 23, and 24).

Add a durable responsibility rule: technical project files and operations are maintained through the agent. Researchers give natural-language instructions and review meaningful outcomes; never require them to repair BibTeX, YAML, Git internals, or scripts as an ordinary task prerequisite.

The confirmed decision and questioning requirements are specified in [agent-interaction.md](agent-interaction.md). The adopted AGENTS.md includes their concise authority rule and routing link. All skills, including grilling and major revision, follow it. Read-only investigation and reviewable preparation can proceed while a major choice awaits an answer; dependent implementation waits for explicit confirmation. Silence or a default selection is not approval, and existing clear authorization should not be requested repeatedly. A skill cannot waive this requirement.

Official references for the English-question requirement are the [ASD-STE100 FAQ](https://www.asd-ste100.org/STE_faq.html), [official issue information](https://www.asd-ste100.org/), and [distribution and AI guidance](https://asd-ste100.org/STE_downloads.html). The shared interaction specification defines language scope and verification; a prompt alone does not establish compliance.

Skill routing should be proactive and proportionate. The agent identifies the task and missing context, checks available skills and tools, and loads the applicable workflow when it helps. Researchers should be able to describe a goal in ordinary language without knowing a skill name. Do not load every skill or impose a formal research cycle on a simple edit.

Within project instructions, explicit current researcher directions govern the current task; material conflicts with persisted requirements must be surfaced and recorded. Imported papers and reviewer documents are source material, not executable agent instructions. A citation or reviewer request does not acquire authority to change project policy.

[Codex skills documentation](https://learn.chatgpt.com/docs/build-skills) describes repository discovery under `.agents/skills`, scanned from the working directory up to the repository root, and requires `name` and `description` in SKILL.md. [Claude Code skills documentation](https://code.claude.com/docs/en/skills) reads project skills only from `.claude/skills` and treats all frontmatter fields as optional. Both follow symlinked skill folders. Maintain one canonical skill body and validate generated tool-specific mirrors; do not maintain two independent policies.

The [Claude Code memory documentation](https://code.claude.com/docs/en/memory) states that Claude Code v2.1.277 or later reads AGENTS.md directly only when no CLAUDE.md exists, that a CLAUDE.md importing `@AGENTS.md` never makes it load twice and also covers sessions without direct support, and that a symlinked CLAUDE.md fails in Windows clones without symlink support. The [Codex AGENTS.md guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md) reads AGENTS.md from the repository root down to the working directory, up to 32 KiB by default, and does not read CLAUDE.md. Resolved: keep a one-line CLAUDE.md import. These are documentation findings checked on 2026-10-26; confirm actual loading in fresh sessions of both agents before claiming compatibility, and do not assume identical instruction precedence or optional skill metadata.

Resolved: Claude Code skill adapters ship in the template as generated, committed copies of the canonical packages, with a consistency check. Symlinks fail in Windows clones without symlink support, and generating adapters during initialization would leave Claude Code without the onboarding skill that performs the generation. Bootstrap must work before Python-dependent generation is available.

## 9. Skill architecture and standalone task catalog

Confirmed structure: the hands-on stages must be usable independently. Organize skills around complete tasks a researcher can request, each with a distinct outcome. The paper and Git hands-on skills coordinate those tasks. A researcher may enter at any useful stage; the agent selects the relevant skill from ordinary language.

The names and precise boundaries below are proposed. Each skill describes decisions, execution, recovery, and verification; deterministic scripts can be shared. Do not make every shell command or internal substep a separate skill, and do not duplicate task procedures in the coordinating guides. Actual SKILL.md packages remain to be implemented.

### Guided paths

| Skill | Responsibility | Outcome |
| --- | --- | --- |
| `paper-hands-on` | Identify the researcher's current position, select the next useful research/writing task, and connect its result to the next stage. | A guided, resumable paper project using the same standalone skills available for direct requests. |
| `git-hands-on` | Guide practical learning through the standalone version-management tasks. | Understandable version checkpoints and safe practice, with the agent operating Git. |

### Shared project support

| Skill | Responsibility | Outcome |
| --- | --- | --- |
| `project-onboarding` | Establish the research goal, language, immediate needs, and initial workspace. | Minimal usable project settings and a clear next action. |
| `privacy-configuration` | Identify the product/account/service, assist with supported training opt-outs, and verify or qualify the result. | Scoped settings status, official sources, and explicit unresolved items. |
| `environment-management` | Manage tools, environments, and guided project-local credential setup and recovery. | Usable configuration without requiring programming knowledge or exposing secrets. |
| `constraint-maintenance` | Persist only verified, researcher-confirmed requirements; reconcile scope and changes. | Concise, consistent writing requirements without inferred preferences. |

### Independent research and manuscript tasks

| Skill | Responsibility | Outcome |
| --- | --- | --- |
| `literature-discovery` | Turn an interest or question into a search strategy; locate and screen relevant sources and identify full-text access gaps. | A sourced reading set, search scope, and collection priorities. |
| `reference-download` | Obtain selected references in batches from identifiers, lists, or manuscript references, with access checks, provenance, deduplication, and resumption. | Available full text plus honest per-item access status, optionally handed to ingestion. |
| `source-ingestion` | Import a document or folder through MinerU, preserving originals, Markdown, images, metadata, and resumable batch progress. | Indexed, linked reading material and a concise conversion report. |
| `manuscript-import` | Adopt an existing manuscript into the section, asset, and citation conventions while preserving originals and current work. | A mapped, reviewable migrated manuscript with losses and unresolved references visible. |
| `review-ingestion` | Archive and extract formal review documents, including annotations where supported, by venue and round. | Traceable Markdown/assets and extraction gaps, without automatically replying or revising. |
| `research-feedback` | Organize attributed advice from co-researchers, collaborators, coauthors, supervisors, and other contributors, and connect researcher-confirmed choices to follow-up. | Scoped actions, decision links, and actual change status without promoting suggestions to rules. |
| `literature-and-evidence` | Read identified sources, compare passages, and verify their support for claims. | Evidence notes with locators, limitations, and contradictions. |
| `research-ideation` | Organize starting thoughts and generate substantially different research directions grounded in interests, materials, and constraints. | Researcher-selected directions, with originality still qualified by available evidence. |
| `idea-deepening` | Use grilling-inspired, one-question-at-a-time inquiry to examine an existing idea. | A clearer question, contribution, assumptions, alternatives, feasibility, and next check. |
| `impact-assessment` | Examine why a contribution matters, to whom, and what supports or limits its value. | A reasoned impact assessment and concrete ways to strengthen it. |
| `journal-selection` | Compare venues or examine a specified venue using current scope, article types, requirements, and relevant publications. | An explained target/shortlist with fit, tradeoffs, and conditions. |
| `research-planning` | Translate a selected question into methods, evidence needs, milestones, and feasible next actions appropriate to the discipline. | A research plan separating available evidence from work still required. |
| `research-investigation` | Carry out a bounded inquiry using available materials/tools, compare explanations and counterevidence, and follow identified gaps. | A source-grounded synthesis or research artifact, with uncertainty and remaining work explicit. |
| `manuscript-outline` | Shape the argument and section sequence for the question, available findings, and applicable requirements. | A researcher-reviewable outline and content/evidence gaps. |
| `manuscript-writing` | Draft or revise requested prose against the confirmed outline, requirements, and actual evidence. | Focused manuscript edits with unsupported statements identified. |
| `manuscript-audit` | Critically assess argument, evidence, terminology, citations, and confirmed writing constraints. | Prioritized findings linked to actual passages and evidence. |
| `manuscript-revision` | Coordinate a substantial change of argument, structure, evidence, or target using the existing research, writing, audit, and assembly tasks. | A recoverable revision with baseline, scoped plan, content mapping, updated checks, and a clear active draft or remaining gaps. |
| `submission-assembly` | Interpret adopted requirements/templates, implement their layout, assemble the selected format, and inspect the rendered result. | Formatted files, a readable compliance summary, and a reproducible build record. |
| `submission-readiness` | Assess a current manuscript and package against the selected venue, reusing current audit/formatting results. | Evidence-based strengths, likely reviewer concerns, and remaining submission tasks, without an invented acceptance probability. |
| `review-response` | Organize a review round and connect each response to actual changes or a justified explanation. | A traceable point-by-point response. |
| `research-code-setup` | Elicit analysis/experiment needs before choosing code structure and management. | A proportionate, reproducible code workspace only when relevant. |

### Independent version-management tasks

| Skill | Responsibility | Outcome |
| --- | --- | --- |
| `git-inspection` | Inspect tool availability, existing repository/history, and unsaved changes without modifying them. | A plain-language account of current versions and unpreserved work. |
| `git-setup` | Prepare or repair the requested local version-management setup while respecting existing history and excluding secrets. | A usable local repository and a clear description of tracked scope. |
| `git-save` | Review the intended changes and preserve a meaningful local checkpoint. | A recognizable version and concise saved-change summary; no implicit remote publication. |
| `git-compare` | Compare requested versions or current changes and explain research-relevant differences. | An understandable comparison with locations of important edits. |
| `git-recovery` | Retrieve selected earlier content or perform a scoped restoration while preserving current work and respecting the researcher's chosen scope. | Recovered material and an explicit account of what changed and how to return. |
| `git-backup` | Explain and carry out explicitly requested backup/sharing choices, checking destination and visibility. | A verified external-copy status or a clear account of what still exists only locally. |

### Common boundaries and task handoff

- Discovery locates sources; downloading obtains available files; ingestion converts and indexes them; evidence work reads and evaluates them. A broad investigation can reuse these tasks without copying their procedures.
- Intake is a shared routing capability, not a compulsory sequence or an extra skill for moving files. Manuscript adoption, reference ingestion, formal-review extraction, and research feedback share conversion mechanics but preserve different destinations and authority. Download-and-import is one request using two reusable tasks; either task can also run alone.
- Feedback records preserve what was advised; decisions preserve what the researcher chose and why; requirements describe what currently governs work. Only relevant active requirements enter ordinary task context; historical rationale and unadopted advice are read when needed as source material.
- Ideation proposes directions; deepening tests a selected direction; impact assessment examines value; journal selection examines venue fit; readiness checks a particular manuscript/package. None substitutes for another's outcome.
- Research planning specifies what work is needed; investigation advances an actual inquiry. Outlining structures an argument; writing develops it; audit evaluates it; assembly applies layout. Readiness can reuse valid recent results and identify gaps without silently rewriting the manuscript.
- Major revision coordinates these tasks around an existing manuscript and a changed goal. It is independent of a journal review round; `review-response` can invoke it for agreed changes and link its results. Routine prose edits still use `manuscript-writing` directly. Do not duplicate specialist procedures in the revision coordinator.
- Git inspection is read-only; setup establishes the mechanism; saving creates a local checkpoint; comparison explains differences; recovery retrieves/restores selected content; backup concerns an external copy. Each can be requested directly.

Every standalone skill should specify its natural-language triggers, scope, minimal inputs, relevant project records to read, expected outputs and managed files, completion checks, and next-step handoff. Reuse supplied material and ask only for missing context that materially changes the task. Do not require the researcher to complete the full course or manually manufacture a technical input file.

When a skill creates a project directory, it also creates a meaningful English `README.md` and maintains it if the directory's role changes. Apply the shared major-decision and questioning rules before adopting consequential choices. Do not duplicate that policy inside every skill.

Keep task-specific instructions in one canonical skill. A coordinating guide identifies the stage, reads the applicable skill, and connects outputs through existing project files and concise state. Load task guidance as needed, keep discovery descriptions concise, and do not duplicate the whole catalog in AGENTS.md or require a new workflow engine. Technical skill composition remains the agent's responsibility; researchers see understandable actions and outcomes.

Detailed stage mappings are in [the hands-on design](hands-on.md). Every mapped stage can also run independently, while confirmed requirements and project state remain shared.

Paper impact, journal fit, and submission readiness are separate assessments. Explain who benefits, the contribution and support, alignment with the venue, and likely reviewer concerns. Consult current official venue guidance and relevant inspected publications when assessing an actual target. Address acceptance prospects through evidence-based strengths, risks, and improvements; do not fabricate a manuscript-specific acceptance percentage or guarantee publication.

### Research ideation and idea deepening

Ideation and deepening are confirmed requirements, now exposed as separate proposed skills. `research-ideation` actively proposes a small set of meaningfully different directions grounded in interests, materials, observations, and constraints. `idea-deepening` examines a selected direction through its question, contribution, assumptions, nearest prior work, alternative interpretations, feasibility, and route to evidence or argument. Either can be requested independently and can hand useful material to the other.

For deepening, draw on grilling's focused questioning, dependency-aware exploration, and practice of offering a recommendation with each question. Adapt the method to researchers rather than transplanting a software-design interview verbatim. Do not subject an undeveloped thought to a long interrogation before helping the researcher articulate it.

Ask one substantive question at a time and wait for the answer. Explain why it matters and offer a reasoned suggestion. First investigate what existing project material or accessible literature can answer; do not transfer retrieval work to the researcher unnecessarily. Summarize progress at natural checkpoints and stop the interview when a useful next action is clear or the researcher wishes to switch tasks.

Possible sources of contribution include a new observation, explanation, concept, method, dataset, synthesis, interpretation, or boundary condition. Match evaluation to the discipline: an experimental test is not mandatory for a conceptual, qualitative, interpretive, or historical contribution. Assess originality, significance, feasibility, and support separately; replication or a negative result need not be disguised as novelty.

Use `research-investigation` and `literature-and-evidence` when checking originality. Compare the closest inspected work and identify concrete differences, rather than treating a different title or an empty search result as proof of novelty. When coverage is limited, label the novelty assessment preliminary. Never guarantee an idea is unprecedented, invent literature gaps, or fabricate supporting observations.

With the researcher's direction to retain an idea, save a concise note under `ideas/` and link it from the index. Capture the question, proposed contribution, relevant prior work, assumptions, uncertainties, status, and next check when useful; do not force a separate file for every passing thought. An explicitly retained research hypothesis may remain unverified and be labeled accordingly. It does not become an active writing rule, so the no-unconfirmed-preferences boundary still applies.

### Expected research interaction

For a substantive investigation, the agent should clarify the question and desired deliverable, inspect existing material, choose a retrieval strategy, read relevant sources, compare explanations and counterevidence, identify gaps, and iterate before producing a synthesis or manuscript change. Adapt this sequence to the task rather than treating it as a rigid checklist.

Use available connectors, scholarly/search services, browser access, and local tools as appropriate. Inspect capabilities before assuming access. Separate search snippets, abstracts, and inspected full text; verify important claims against accessible sources. If access is limited, report the gap rather than inventing results or requiring a particular account for all researchers.

Professional interaction includes challenging unsupported assumptions, distinguishing observation from interpretation, and asking focused questions when answers change the research direction. Persistent rules still require the confirmation boundary in Section 7. Research depth must come from evidence and reasoning, not from lengthy output or unnecessary tool calls.

## 10. Manuscript assembly and collaboration

Confirmed requirement: provided formatting instructions and reference templates must guide actual typesetting. The `submission-assembly` skill owns the complete process from interpreting the requirements to inspecting the delivered manuscript. A successful DOCX/PDF export alone does not establish format compliance.

### Read requirements and preserve templates

Accept researcher-supplied requirements, journal instructions, Word templates, LaTeX classes/styles and supporting files, and PDF layout examples. Archive the originals in the output profile and inspect their relevant structure, styles, and visual layout. Markdown extraction can help read instructions, but must not replace the original template resources needed for typesetting.

The researcher can simply request: use this journal's instructions and this template to format my manuscript. The agent identifies the materials, extracts the applicable explicit rules, and maintains the technical profile and templates. Adopting a supplied template authorizes its explicit formatting rules; uncertain inferences from an example must be clarified in conversation before being persisted as mandatory requirements. Do not ask the researcher to edit a style file or YAML.

Check the version, document purpose, and applicability of the resources. A journal guideline, an old example article, and a researcher preference can disagree. Resolve material conflicts and ambiguity with the researcher, then persist the confirmed interpretation. An example article's layout is not automatically the journal's current submission specification. If content required by the format is missing, identify the gap rather than inventing content or silently deleting material to fit a limit.

### Apply and check the adopted rules

Maintain a concise mapping from each requirement to its source, scope, implementation, and verification result within the output profile. Use appropriate styles, templates, bibliography settings, or reusable scripts to implement it; formatting must not depend on a researcher manually repairing every export.

| Requirement area | Examples to apply when specified |
| --- | --- |
| Page layout | Paper size, margins, columns, orientation, headers/footers, pagination, and line numbering. |
| Text and headings | Fonts appropriate to the writing language, sizes, line/paragraph spacing, indentation, alignment, heading levels, and numbering. |
| Article structure | Title block, author information or required anonymization, abstract structure, keywords, section order, declarations, and appendices. |
| Citations and notes | In-text citation conventions, bibliography style/order, footnotes/endnotes, and cross-reference presentation. |
| Figures, tables, and equations | Placement rules, sizing/resolution, captions and notes, numbering, table styling, and equation references. |
| Submission package | Required file formats, separate figures or supplements, limits, and template-specific files or metadata. |

Build, render, inspect, and repair until the adopted requirements are met or a specific unresolved limitation is identified. Combine machine checks of document properties, styles, numbering, links, and completeness with visual inspection of the rendered layout. Check clipping, overflow, broken figures, inappropriate page breaks, fonts, and language-specific typesetting. For an anonymized output, inspect relevant file metadata as well as visible content while retaining the canonical source information.

Choose the assembly approach to meet the requirements. A converter's defaults are not an acceptable substitute for required layout; add a profile-specific template or script when needed and keep it reusable. If a font, engine, template feature, or rendering capability is unavailable, explain the precise affected requirement and available remedy. Do not silently omit it or label an unchecked preview compliant.

Deliver the formatted files and a short researcher-readable result: which profile was applied, which checks passed, what still needs attention, and where the files are. The detailed rule mapping and build record stay available for the agent. Rebuilding after manuscript changes should reuse the same adopted profile, and changing the target journal should select a distinct profile without rewriting scientific content merely for layout.

### Math, diagrams, and native Word equations

Confirmed: Markdown mathematics must render on GitHub, agent-created explanation diagrams use Mermaid, and DOCX formulas must be native editable Word equations. The shared [Markdown and export contract](markdown-and-export-conventions.md) specifies source conventions, normalization, source-to-output mappings, and checks for ingestion, adoption, writing, audit, and assembly. Skills reuse this contract rather than maintain different formula or diagram rules.

Use `$...$` inline and separate-line `$$` blocks as the canonical source form; the [GitHub math guide](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions) documents MathJax-based LaTeX rendering. Mermaid explanation diagrams use fenced `mermaid` blocks and syntax compatible with GitHub's active renderer, as described in the [diagram guide](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams). Scientific plots and received images retain appropriate plotting or original formats. Preserve editable diagram source and render suitable figure assets for publication output.

Word equations must use native Office Math/OMML, the format identified in [Microsoft's math documentation](https://learn.microsoft.com/en-us/office/math/). Preserve the actual mathematical structure, inline/display placement, numbering, and references. Images, plain text, legacy embedded objects, and unparsed LaTeX strings do not satisfy this requirement. Validate every expected formula's conversion and inspect rendering/editability; an OMML element somewhere in the file is insufficient. Report unsupported constructs as unmet requirements without silent fallback or changed meaning. GitHub checks and Word checks are separate; a valid preview does not establish export fidelity.

### Canonical content, assembly, and collaboration

Use GitHub-compatible Markdown with the confirmed math and Mermaid conventions. These rendering features are not a claim that plain CommonMark alone covers the requirements. Evaluate remaining citation, numbering, footnote, table, and cross-reference conventions together with the export engine, retaining the confirmed source/rendering and native Word math requirements.

Use an explicit section manifest rather than filename globbing. Exclude README, outline, notes, and unselected drafts from exports. Support a single-file manuscript without forcing an artificial split.

Maintain stable figure/table identifiers, captions, original assets, and source/permission notes when relevant. Keep editable data or figure-generation code where reproducibility requires it. Avoid hand-numbering citations and cross-references.

For [Pandoc DOCX](https://pandoc.org/MANUAL.html#option--reference-doc), a reference document contributes styles and document properties; it does not automatically reproduce arbitrary template body content or all journal layout rules. A PDF example is a visual specification, not an executable template. Some profiles require dedicated adaptation.

LaTeX/PDF assembly needs the selected engine, templates, fonts, and packages. Model export capability per profile; unsupported features must yield visible errors or limitations. Do not promise exact equivalence among Word, LaTeX, and PDF.

Do not silently import edits from a generated DOCX into canonical Markdown. Coauthor Word edits and tracked changes need a deliberate reconciliation workflow to avoid losing or duplicating edits.

Keep previews rebuildable and releases immutable. Each release records manuscript/input checksums, profile revision, bibliography, assets, tool versions, build command, and validation results. Prevent later rebuilds from overwriting an already submitted package.

### Major revision and restructuring (proposed)

The existing file layout can hold a major revision, but version history alone does not coordinate its scientific and editorial consequences. Propose a standalone `manuscript-revision` skill for restructuring before submission, responding to major review requests, changing the central argument, incorporating genuine new findings, or adapting the content for a new venue. A venue change can also require formatting alone; determine the actual scope rather than forcing a scientific rewrite. Exact revision records and procedures remain recommendations for discussion.

Use a lightweight `revisions/<revision-id>/` record only when the scale warrants it. Its plan owns the baseline reference, researcher-directed goal and scope, affected material, ordered work, and next action; the change map owns actual old-to-new mappings; checks own the input versions and observed results. Optional candidate drafts stay outside active assembly. Formal review records and research decision records link to this work rather than duplicating it. An ordinary section edit needs no revision directory.

1. **Preserve the actual starting point.** Capture the current draft, including unsaved-to-history edits, relevant requirements/profile, citation metadata, assets, and needed data/code versions or references. Use suitable existing Git support or a scoped local snapshot and inventory if Git is unavailable; do not make installing Git or learning branches a prerequisite. A commit alone does not cover untracked/external assets. Record how to recover without overwriting later work. Keep earlier submitted packages unchanged and reuse stable source archives rather than copying the entire library.
2. **Make the proposed change concrete.** Inspect the question, argument, evidence, existing feedback, and requested goal. Identify what to keep and what may change; map sections, claims, figures, and citations to keep, move, split, merge, rewrite, or remove. Show affected title/abstract, argument, methods or materials where relevant, findings, conclusion, supplements, and venue requirements. Clarify missing scholarly choices that materially change scope. Existing explicit instructions already authorize their stated scope; no repeated approval per section is needed.
3. **Maintain a coherent target.** Update only researcher-confirmed requirements and adopted outlines, with supersession links for changed decisions. The agent's proposed framing or inferred preferences cannot become lasting rules. Work through bounded research, writing, and code tasks as appropriate; insufficient evidence remains a gap. New analyses or experiments require actual results, not rewritten findings chosen to fit the new narrative.
4. **Revise in recoverable steps.** Keep the affected-work list and completion state concise, with baseline/input references and next actions for fresh sessions. Use a staged candidate when alternative structures or replacement scope warrant one; otherwise work against the preserved baseline. Map renamed, split, or merged sections and retain recoverable removed material. Detect intervening researcher/coauthor edits before applying staged changes and reconcile them rather than overwriting them. Keep section manifests and stable figure/table/citation references consistent. This needs ordinary files and reusable operations, not a new workflow engine.
5. **Recheck what changed.** Tie evidence, audit, formatting, and readiness results to the inputs and scope they actually checked. A changed claim, figure, analysis, section, requirement, or output profile makes its affected prior checks stale; unchanged, properly scoped checks can be reused. A valid citation key does not establish support for a rewritten claim. Revisit relevant evidence and dependent passages, including summaries and conclusions, and rebuild affected figures/outputs when their inputs change. Never carry an old passed check forward as proof of the new manuscript.
6. **Compare and establish the current version.** Present research-relevant differences and remaining gaps, then apply the authorized revision as one clearly identified active manuscript with matching outline, manifest, assets, requirements, and records. Do not mix selected chapters from competing drafts accidentally. Record the application steps so an interruption during multi-file replacement is detectable and recoverable; do not claim a set of ordinary file writes is atomic. Recheck whole-manuscript coherence and affected links/support, then reassemble and inspect the requested output when that capability is available. A checked revision, a draft needing more evidence, and a submission-ready package are distinct outcomes.

Exercise this design with a substantial argument/section reorganization, a genuine change in evidence or analysis, and a venue switch. Include an interruption, a concurrent author edit, a removed section or figure, a stale claim-support check, and resumption in a fresh session. Acceptance requires recoverable earlier work, no lost edits, accurate citations/cross-references, coherent current content, and honest remaining research/formatting work. These are future implementation tests, not claims that revision support already works.

## 11. Ideas, reviews, and research code

Ideas need a light status convention such as exploratory, developed, incorporated, or abandoned, with links to relevant sections or sources. Incorporation does not convert an unsupported idea into evidence.

Within each venue, separate submission rounds so reviewer numbering, decisions, and manuscript snapshots do not collide. Preserve original comments, extracted text, response items, and corresponding manuscript changes. Do not claim that a comment has been addressed until the change or justified response exists.

Keep `scripts/` for workspace operations and `code/` for the research method or analysis. Research code may need a separate environment; adding an ingestion dependency must not silently destabilize an analysis environment. Data placement, sensitive data, reproducibility, and large artifacts are onboarding topics, not universal defaults.

## 12. Dependencies and portability

The confirmed deployment baseline is a lightweight Windows laptop such as a Surface. Exact Windows version, RAM/storage limits, and required processor architectures remain to be defined; the product family name is not a complete test specification. Do not interpret optional high-performance configurations as minimum requirements.

Reading and editing Markdown must work before Python or converters are installed. Core organization, confirmed-rule memory, local text search, agent skill routing, and ordinary writing must not depend on a dedicated GPU, local model weights, Docker, WSL, an always-on parsing service, or a vector database.

Start onboarding by inspecting the operating system, processor architecture, available memory and storage, installed Python/CLI tools, and needed capabilities. Verify tool compatibility for the actual machine; do not assume an x64 package will work on ARM64. Use native Windows paths and PowerShell-compatible instructions, including paths with spaces and non-ASCII characters. Additional operating systems should remain possible without displacing the Windows acceptance baseline.

Separate the minimal agent workspace, the selected MinerU integration, and export dependencies. For MinerU, offer local execution or a researcher-selected cloud route; do not force local inference weights onto a laptop that will use cloud parsing. Missing parsing/export capabilities must not block unrelated writing work. Verify each advertised capability on the stated baseline rather than promising universal format support from a successful install.

Reuse installed, compatible Python and CLI tools with explicit executable paths and recorded versions. If a script needs dependencies, create a local `.venv` and invoke its interpreter directly rather than relying on activation persisting across shell calls. Offer `uv` as an optional convenience, not a second mandatory bootstrap dependency.

Heavy parsing stacks can use a separate tool environment to avoid research-code conflicts. Do not overwrite a working global installation merely to match the template. An incompatible version should produce a clear choice of supported options.

When Python is absent, provide platform-appropriate installation guidance. Do not depend on Python to explain or initiate every bootstrap step. Validate native Windows onboarding first, then cover macOS and Linux progressively, and state which paths have actually been verified. Do not require administrator privileges or system-wide policy changes as a template design choice; describe any external dependency's actual requirements when applicable.

Select the MinerU processing mode with the researcher. Cloud parsing, credentials, model downloads, and remote services must be explicit project choices. Tool availability does not itself authorize uploading unpublished manuscripts or sensitive source files. Store confirmed project requirements and processing permissions in `requirements/privacy.md`; store credentials outside tracked project files.

Use reproducible dependency specifications for managed environments and record externally installed tool versions. Final pinning strategy follows compatibility testing; do not freeze arbitrary current versions before evaluation.

### Guided project-local initialization and credentials

Configuring required OCR/API access during project-local initialization is confirmed. The storage and interaction details below are a proposed implementation, intended to avoid asking researchers to perform programmer tasks.

After the researcher selects local or cloud parsing, the agent checks what that route actually needs. Local parsing should not demand an unrelated cloud key; an existing AI application subscription should not be assumed to require a new model API key. For a selected service that requires credentials, explain where to obtain them and open the official account/setup page when useful. Allow initialization to finish with conversion setup explicitly deferred if the researcher is not ready.

Provide masked entry on the researcher's own machine through a local setup form or a password-style prompt launched by the agent. Do not ask for keys in chat, show them in command arguments, or print them in logs. Reuse an existing compatible credential only with the researcher's intended service and scope. Ask only for meaningful missing choices, not SDK or environment-variable details.

A simple project-local option is an ignored `.env.local` file read by the project adapter, with an optional operating-system credential store where suitable. Ensure exclusion from Git before writing any secret. An ignored file is not encrypted storage; state the selected storage method plainly. Provide placeholders in any tracked example. The adapter must actually load the values for the selected process; do not assume upstream tools automatically read this file.

Check required fields and authentication using a documented non-content check when available, without disclosing secrets. If end-to-end access cannot be confirmed without conversion, say so and verify it on the first authorized job. Report ready, incomplete, or needs attention, with a plain next step. Keep shared project requirements separate from machine-specific settings and credentials; a new clone guides its own setup rather than inheriting another researcher's secret.

### Privacy-configuration skill: responsibility and verification

The skill is a confirmed requirement. Its proposed implementation assists with actual provider controls; a sentence in AGENTS.md or a made-up configuration key cannot change a provider's data-use policy. Keep repository memory distinct from using data to train provider model weights. A file can remain local at rest while its contents are transmitted when a cloud-backed agent reads it into context.

Run the skill during onboarding when relevant and when the researcher changes an application, login method, account/workspace, model endpoint, or cloud parsing service. Inspect nonsensitive settings first; do not send a manuscript as a privacy test. This design discussion does not change the template maintainer's current account settings.

Proposed workflow:

1. Identify the product, version, authentication route, account/workspace type, model provider, and MinerU processing endpoint. Ask only for missing information that changes applicable settings; never request passwords or API keys in chat.
2. Consult current official documentation for that exact route. Distinguish model-training use, data retention, inference/upload, telemetry/error reporting, and user-submitted feedback. Check for additional data-sharing or improvement-program opt-ins where relevant.
3. Show the specific controls and their scope. Prefer documented APIs or readable settings; where supported and authorized, change only the relevant controls and preserve a way to reverse the change. Account or organization settings can affect other projects, so explain that scope before applying them. Where only account UI or administrator access is available, guide the researcher through the actual steps.
4. Verify by reading the resulting control or effective policy when possible. Report separately what was observed, what the researcher confirmed, what is based only on a provider default, and what remains unknown or needs administrator action. Never call a setting verified just because instructions were shown or a local file was written.
5. Keep a minimal, redacted status report locally, outside Git by default, with service/scope, check date, evidence type, official sources, and remaining steps. Persist only confirmed project choices in the shared requirements. Do not record raw credentials, account identifiers, private screenshots, or manuscript content as verification evidence.

Initial official-source findings, checked on 2026-10-25:

- [OpenAI API data controls](https://developers.openai.com/api/docs/guides/your-data) state that API data is not used for model training unless the customer explicitly opts in, while retention and abuse-monitoring controls are separate. This API policy must not be assumed to describe every Codex ChatGPT sign-in/account route. For those routes, verify the current product/account controls during skill use; do not invent a universal local opt-out flag.
- [Claude Code data usage](https://code.claude.com/docs/en/data-usage) distinguishes consumer model-improvement choices from commercial-account policies and voluntary sharing. Its telemetry controls are separate. The [model-improvement settings guide](https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings) provides account-setting guidance; exact labels and availability must be checked when used.
- Training opt-outs must be described with their actual provider scope and exceptions. For example, the [Anthropic consumer privacy explanation](https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training) separately discusses safety review and feedback. Do not promise that every possible use is eliminated, or that previous use has been undone.
- Checked on 2026-10-26: OpenAI's [Data controls in ChatGPT](https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt) states that on personal ChatGPT plans the "Improve the model for everyone" setting also covers Codex tasks, and that Codex has a separate "Include environments" setting that the ChatGPT setting does not change. Business, Enterprise, and Edu workspaces are not used for training by default. The Help Center refuses automated fetching, so the skill reads it in a browser. The skill's dated source register is `.agents/skills/privacy-configuration/sources.md`.
- A MinerU cloud service is a separate data processor with its own terms and controls. Until the specific service policy is checked, its training use and retention remain unknown. A no-training preference in an AI application does not automatically apply to that service.

Telemetry reduction can be offered separately where useful. Do not disable unrelated functions or present telemetry opt-outs, session deletion, or zero-retention settings as equivalent to a verified training opt-out.

## 13. Version control and ignore policy

Ignore `.venv`, optional tool environments, Python caches, model weights, retrieval caches, temporary conversion files, editor/OS artifacts, secrets including `.env.local` and other credential-bearing local environment files, local privacy-verification reports, and rebuildable previews. Explicitly allow tracked placeholder-only environment examples if provided.

Do not globally ignore `*.pdf`, `*.docx`, `*.tex`, or images: originals, format resources, and manuscript assets can be authoritative. Ignore paths by role instead.

The public template ships placeholders and redistributable fixtures, never researchers' documents. A cloned workspace needs an explicit tracking/backup policy for originals, extracted content, datasets, and release packages. `.gitignore` is neither access control nor a backup system. Consider large-file handling only when actual corpus size requires it.

The agent handles Git commands and related technical configuration. The Git hands-on uses the researcher's tasks to explain inspecting changes, preserving a local version, comparing versions, and recovering a selected item. Demonstrate recovery on a practice file or copy while preserving real work. Repository creation or changes in a researcher's workspace are actual hands-on actions only after that workflow is requested. The template repository's own Git history serves framework development. Explain local version history and off-machine backup separately, and obtain an explicit external-sharing instruction before remote publication.

## 14. Development sequence and acceptance criteria

The detailed, proposed [MVP implementation guideline](mvp-implementation-guideline.md) expands this high-level sequence into nine researcher-usable increments with dependencies, deliverables, acceptance evidence, and a complete skill assignment. It does not mark any implementation complete or resolve the open decisions below by implication. Its revised order (2026-10-26) runs Git support and an export trial right after the minimal workspace, so the steps below are capability groups rather than a strict order.

1. **Design agreement.** Record the confirmed discipline-agnostic scope, confirmation-before-persistence rule, Windows baseline, MinerU selection, researcher choice of cloud parsing, and privacy-configuration skill; resolve remaining integration and AGENTS.md decisions. Acceptance: reviewed plan that clearly separates confirmed decisions from open proposals.
2. **Minimal workspace and instructions.** Add maintained directories and READMEs, guided project-local initialization and credentials, privacy configuration, canonical instructions, and agent adapters. Acceptance: a non-programmer can follow the README and ask the agent to initialize the project without editing code or configuration syntax; secrets stay out of chat, logs, and Git. Each agent can find requirements and the next task in a fresh session; privacy guidance distinguishes observed controls from unknown/account-admin-only settings and needs no research-content upload.
3. **MinerU ingestion.** Implement single-file and batch import on the Windows baseline with a small representative corpus. Acceptance: one natural-language folder request produces archived originals, Markdown, working images, an updated index, and a concise status summary. Check text, scans, columns, equations, tables, figures, and a document longer than ten pages for coverage and traceability. Exercise duplicate detection, partial failures, interrupted jobs, and retrying failed work without rerunning completed imports. Cloud use follows the researcher's confirmed service/scope choice; local failure never triggers an unapproved upload. A full local model installation is unnecessary for the remote route or basic writing.
4. **Ideation, writing, and research workflow.** Implement idea exploration/deepening, confirmed-constraint maintenance, investigation, source-grounded drafting, and resumable state. Acceptance: the agent can propose distinct directions and deepen a selected one through focused questions, evidence, prior-work comparison, and feasibility; it does not claim unverified originality. Confirmed requirements survive a fresh session; an inferred preference without confirmation is absent from persistent files. Exercise contrasting research scenarios without imposing one discipline's structure.
5. **One complete formatting and export path.** Prove a neutral profile and one real or representative journal profile with supplied requirements or a reference template before expanding formats. Acceptance: trace requirements to implemented styles/templates and check section inclusion, citations, assets, and references; inspect rendered typography and layout against the adopted specification and repair discrepancies. Rebuild after an edit to confirm rules remain applied. A file that merely opens is not sufficient; any unmet or unverified requirement is reported specifically.
6. **Review and optional extensions.** Add round-aware response handling, research-code onboarding, and additional export profiles or research integrations only when justified. Acceptance: reviewer items map to responses and actual changes; new dependencies do not break existing workflows.
7. **Guided hands-on acceptance.** Exercise paper and Git hands-on paths with an ordinary-computer-user scenario. Acceptance: the researcher can start from an interest, inspect collected evidence and developed ideas, discuss impact and venue prospects, and produce a checked manuscript when the required research is complete. They can also preserve, compare, and safely practice restoring a version through natural language. No task requires them to edit technical formats, diagnose stack traces, or run Git commands. Resume a later session from a useful checkpoint rather than restart the course.

Use small, rights-cleared fixtures. Test deterministic scripts where failure risks data loss, broken citation/asset relationships, incomplete imports, or misleading release success. Assess skills with concrete scenarios as well as file checks; the presence of instructions alone is not evidence that agents follow them.

Validate each independent task from a direct natural-language request using existing material, without requiring the full hands-on path. Also validate the connected path: outputs are reusable, relevant context survives handoff, and coordinating guides do not maintain duplicate task procedures or repeat completed work.

Windows acceptance must include onboarding without preinstalled Python/converters, operation without a dedicated GPU, paths containing spaces and non-ASCII characters, direct virtual-environment invocation, and useful writing operation when local MinerU is unavailable. Check that selecting a cloud route does not trigger full local-model installation. State the exact hardware, architecture, software versions, and observed setup/runtime costs when testing is performed. Do not claim Windows or ARM64 validation from tests run only on the maintainer's macOS machine.

## 15. Decision record and remaining questions

Discuss one decision at a time. Resolved items are labeled; the remaining recommendations are proposals.

1. **Parser and cloud choice — resolved:** Use MinerU. Each researcher may choose cloud parsing for complex PDFs; support does not imply blanket upload permission. Specific provider/API, client setup, and actual Windows compatibility still need verification.
2. **Rule persistence — resolved:** Only verified, researcher-confirmed rules are persisted. Do not save agent-inferred preferences as candidates. Explicit instructions already provide confirmation when their meaning and scope are clear.
3. **Workspace scope — resolved:** One main manuscript per workspace, including its submission rounds and revisions. Each additional paper uses its own copy of the workspace. Onboarding never deletes, moves, or overwrites a workspace that already holds work; a new paper starts from a fresh copy of the template (decided 2026-10-26).
4. **Publishing foundation:** Pandoc directly or Quarto as the primary interface? Recommendation: start from the smallest engine that passes a realistic export trial; do not commit before testing cross-references, equations, and the chosen profile. The export trial is scheduled right after MVP 1.
5. **Reference storage:** Which source binaries, extracted assets, and releases belong in Git versus separately backed-up storage? Recommendation: make this an onboarding choice with a documented recoverable default.
6. **First supported output:** Generic DOCX, LaTeX/PDF, or a specific venue? Recommendation: prove one real target before advertising broad format support.
7. **Platform details:** Lightweight Windows laptops are the confirmed baseline. Define exact Windows versions, memory/storage limits, and whether both x64 and ARM64 are launch requirements; verify each supported combination.
8. **Collaboration:** Must coauthor tracked changes, multiple simultaneous agents, or external reference-manager sync work in the initial version?
9. **Privacy assistance — requirement resolved:** Provide `privacy-configuration` to help researchers opt out of supported model-training uses. Provider-specific controls, verification methods, and exceptions must be checked against current official sources; do not claim settings have changed before they are verified.
10. **Researcher usability — requirements resolved:** Explain design philosophy and everyday use in README; guide project-local OCR/API credentials; provide natural-language single/batch PDF-to-Markdown ingestion. First implementation (2026-10-26): a one-time page on the researcher's own computer writes the value to the ignored `.env.local`; an operating-system credential store remains an option to evaluate.
11. **Idea development — requirement resolved:** Provide creative research ideation and idea deepening, informed by grilling, as independently usable tasks. Precise task boundaries and note format remain open to refinement.
12. **Audience and maintenance — resolved:** Ordinary computer users, with no coding/software-engineering assumptions. Technical files and operations, including Git, BibTeX, YAML/JSON, and scripts, are edited and maintained through the agent.
13. **Hands-on paths — requirements resolved:** Provide `paper-hands-on` and `git-hands-on`. The paper path includes research impact and submission-prospect assessment; specific lesson boundaries and checkpoints remain open for refinement.
14. **Template-based formatting — resolved:** Supplied rules and adopted reference templates must control the delivered layout, with actual output checks and reusable profile implementation. Engine and first target profile remain implementation choices to validate.
15. **Independent stages — resolved:** Hands-on stages are standalone skills as well as parts of guided paths. Section 9 proposes their task boundaries and names; guided and direct use share the same procedures and project records.
16. **Flexible intake — requirements resolved:** Provide an intake directory, existing-manuscript adoption, batch reference download and conversion/indexing, and reviewer-document extraction as independently usable, composable skills. Exact names, format support, access integrations, and archive mappings remain implementation choices to validate.
17. **Research decisions and feedback — locations confirmed:** Keep consequential confirmed decisions with rationale under `research/decisions/`, attributed research feedback under `research/feedback/`, and current rules under `requirements/`. Feedback includes co-researchers, collaborators, coauthors, supervisors, and other contributors. The locations were confirmed on 2026-10-26; record formats are refined in MVP 4. This is not permission to persist inferred preferences or impose a new mandatory process.
18. **Major revision — proposed coverage:** Add `manuscript-revision` and lightweight revision records for recoverable changes of argument, structure, evidence, and venue, with affected-check invalidation and an explicit active draft. It must work before peer review as well as after it, without making Git expertise or a fixed paper structure prerequisites. The workflow and exact directory layout remain design proposals.
19. **Directory descriptions — confirmed:** Every designed project directory has its own meaningful `README.md`, including nested and dynamically created directories. Creation and maintenance belong to the agent; English is the canonical language, with optional human-facing translations.
20. **Major decisions and questions — confirmed:** Obtain the user's explicit confirmation before committing any major decision. All skills, including grilling, use the shared question format. English questions follow ASD-STE100; non-English questions retain the chosen language and use corresponding clarity principles. Exact recognition examples and verification are documented for implementation in `agent-interaction.md`.
21. **Math and diagram formats — confirmed:** Markdown formulas use GitHub-renderable LaTeX; agent-created explanation diagrams use valid Mermaid. DOCX equations must be native, editable Office Math/OMML with correct mathematical structure. The shared contract and MVP checks cover actual rendering, mapping, and faithful export; publishing-engine selection remains open.
22. **Complete-path objective — confirmed for testing only:** Test an idea/materials-to-results-to-manuscript-to-submission-package path with a bounded case. Accessible inputs and small scale control the test, not the product scope. Passing this test does not establish journal acceptance, real manuscript readiness, or untested capabilities, and this decision does not adopt every workflow proposal or reorder the roadmap.
23. **Record language — resolved:** Records the researcher reads and confirms (requirements, ideas, source notes, decision and feedback records, revision plans, and project state) use the researcher's interaction language, with quotations in their original language. AGENTS.md, skills, directory READMEs, framework documents, and technical metadata stay in English; the manuscript uses its chosen language.
24. **Agent entry files and skill adapters — resolved:** AGENTS.md was adopted on 2026-10-26, and CLAUDE.md imports it with `@AGENTS.md`. Skills are written once in `.agents/skills/`; `.claude/skills/` holds generated, committed copies checked for consistency. Actual loading in fresh sessions of both agents still needs verification.

The next draft should incorporate researcher answers and narrow implementation milestones. Do not install conversion stacks while the remaining integration choices are being discussed.
