# Capabilities and Operational Limits

Consult this guide when support, setup, or access is uncertain. It is not startup context. A packaged workflow is not proof that its tools are installed, an account has access, or a source supports a claim. Use the current task's actual checks before reporting success.

## Available tasks

| Research task | Skill entrypoints | Requirements and limits |
| --- | --- | --- |
| Start or resume a project | `project-onboarding`, `paper-hands-on` | Records confirmed answers; a bounded request can go straight to its task. |
| Computer setup | `environment-management` | Inspects first; installations, repairs, and system changes need consent. Ordinary Markdown needs no additional tools. |
| Privacy and standing rules | `privacy-configuration`, `constraint-maintenance` | Checks current provider policies and actual controls; only confirmed rules and decisions are recorded. |
| Import reference documents | `source-ingestion` | Confirmed local MinerU or mineru.net route; Markdown/text read directly. See [processing guide](mineru-integration.md). |
| Import an existing draft | `manuscript-import` | Local Pandoc for Word, OpenDocument, and LaTeX; PDF uses confirmed MinerU. Resolve tracked changes and comments before adoption. |
| Import review correspondence | `review-ingestion` | Retains venue and round, comments and tracked changes separately; PDF annotation extraction has limits. |
| Find literature | `literature-discovery` | Sciverse first when configured and within confirmed query scope; permitted host search fills stated gaps. Metadata and snippets are not inspected full text. |
| Obtain public PDFs | `reference-download` | Public PDF responses from supported DOI or direct URLs. Publisher and institutional access are not established; unavailable items remain recorded. |
| Compare source evidence | `literature-and-evidence`, `research-investigation` | Retrieve bounded local passages or authorized service context; check locators and conclusions against originals where needed. No claim of exhaustive coverage. |
| Develop questions and contribution | `research-ideation`, `idea-deepening`, `impact-assessment` | Qualified comparisons, alternatives, feasibility, audiences, and value; no invented novelty or acceptance probability. |
| Plan research and organize advice | `research-planning`, `research-feedback` | Preserve evidence gaps, confirmed choices, and attribution; advice does not automatically govern the paper. |
| Compare venues | `journal-selection` | Needs current official sources through available web access; fit, impact, and readiness are separate. |
| Run analyses and record results | `research-code-setup` | Creates code only when needed; records inputs, versions, parameters, outputs, checks, and limitations. Laboratory or inaccessible data work remains an external dependency. |
| Outline, write, and revise | `manuscript-outline`, `manuscript-writing`, `manuscript-revision` | Current author text and confirmed requirements govern work; major revisions preserve a baseline and reconcile intervening edits. |
| Check manuscripts and natural prose | `manuscript-audit`, `natural-prose` | Located findings and meaning-preserving edits. Pattern lists do not establish authorship or guarantee an AI-detector outcome. |
| Simulate peer review | `mock-review` | Scores tied to a stated form and evidence through several perspectives; no prediction of real scores or acceptance. |
| Choose AI models | `model-selection` | Uses current official information for the actual application, plan, and provider route; no setting changes without consent. |
| Format and assess a package | `submission-assembly`, `submission-readiness` | DOCX with output profile, editable equations, and rendered inspection. PDF is a rendering of checked DOCX; no independent PDF publishing route or automatic submission. |
| Preserve and compare versions | `git-inspection`, `git-setup`, `git-save`, `git-compare`, `git-recovery`, `git-hands-on` | Local history, scoped saves and recovery; practice uses a separate copy. Research-project setup disconnects a clear link to the original template repository without deleting local history. |
| Make an external backup | `git-backup` | Only to explicitly confirmed fetch and push addresses; refuse the original template repository, verify the copy, and never force-push. |
| Respond to reviews | `review-response` | Point-by-point records tied to actual changes; compare coauthor Word edits with both sent and current versions. Sends nothing. |

## Supporting tools

Workspace scripts use Python 3.9 or later and generally the standard library. Reuse compatible installed tools. Create environments only for a task that needs packages; keep heavy parser tools isolated in `.tools/`. Research analysis has its own environment.

The private credential page (`scripts/credentials.py`) stores supported credentials in ignored `.env.local`; it refuses a trackable storage file. The local store is not encrypted. MinerU cloud uses `MINERU_API_TOKEN`; Sciverse uses `SCIVERSE_API_KEY`. Collect neither until the corresponding service and scope are chosen. No other service integration or credential workflow is implied.

DOCX output uses Pandoc, pandoc-crossref, citeproc, and Mermaid rendering when needed. Installation pins remain in the tools. Previously observed versions include Pandoc 3.12.1, pandoc-crossref 0.3.26, and Word 16.114.2 on macOS; check installed versions before building. A real venue template and each manuscript's equations still require inspection.

## Limits to disclose when relevant

- Earlier local observations cover macOS with small non-research documents. They do not establish Windows/Linux behavior, a complete researcher-led workflow, or correctness on real corpora and complex journal templates.
- MinerU can omit text, misread formulas, or lose annotation details. Local formats beyond PDF/Word, larger model tiers, cloud images, and cloud pipeline output remain unverified here. Check the actual original-to-extraction mapping.
- Sciverse agentic search, query-only metadata, and bounded text returned responses for one configured account. Search relevance, filters, cursor continuation, relations, resources, experimental Paper Schema, and account limits remain unverified against a research corpus or live account. See [search guide](sciverse-integration.md).
- Training settings, service access, cost, retention, and provider offers can change. Read current official sources for the actual route. Do not describe unknown retention or training use as disabled.
- Generated adapters and documentation do not prove client loading or model compliance. Ordinary archive downloads are supported by real file copies; Windows operation still needs direct observation.

When support is absent, say so plainly and do not collect a key, promise an output, or create records for an unimplemented route. A missing optional tool must not block independent authorized work.
