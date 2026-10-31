# Agent Call Audit

Audited on 2026-10-31 for the request to check all agent calls and require Sciverse and MinerU skills to use MCP. This is a static review of both skill trees, workspace scripts, MCP setup, and linked operating guidance. No research query or document upload was made during this audit.

## Agent and skill invocation

- Each client has 37 `SKILL.md` entrypoints. Their skill instructions match across `.agents/skills/` and `.claude/skills/`; the Codex tree also has user-facing README files. Skills hand work to specialist skills by name; the repository contains no code that calls a Codex, Claude, or other model-agent API.
- Both clients expose Sciverse natively. MinerU remains installed for the workspace importer, but its raw upload tool is not registered in either client configuration.
- Two skill references describe additional reviewer sessions: `mock-review/SKILL.md` prefers three independent review sessions and permits three labeled passes in one session when separate sessions are unavailable; `manuscript-audit/reviewer-view.md` offers an optional fresh-session or subagent reader check. These are conditional skill instructions, not automatic code-level agent launches. The sessions must receive only the material allowed by the active processing and confidentiality rules.
- `model-selection`, `privacy-configuration`, `journal-selection`, `submission-assembly`, `mock-review`, and `literature-discovery` use or allow the host application's web or search tools for current sources. These are runtime-provided tools, not repository API clients; a search-provider scope still applies. The `mock-review` handoff rule also distinguishes them from Sciverse and from agent dispatch.

## Skills that mention Sciverse or MinerU

Eleven distinct skill entrypoints mention one or both services. Their Codex and Claude Code copies are aligned.

| Skill | Call path or boundary |
| --- | --- |
| `literature-discovery` | Saved searches and retrieval use `scripts/literature.py`, which calls the official Sciverse MCP. Provider fallbacks need separate scope. |
| `literature-and-evidence` | Uses saved Sciverse records and the MCP-backed context/resource commands; service text remains derived evidence. |
| `mock-review` | Uses native Sciverse MCP tools for a read-only review without writing search folders; checks scope and records the search in the response. |
| `source-ingestion` | Imports reference materials through `scripts/ingest.py` and the official MinerU MCP; other material is excluded. |
| `review-ingestion` | Reads Markdown/plain-text correspondence directly; other formats cannot be uploaded to MinerU. |
| `research-feedback` | Reads Markdown/plain text directly; other formats cannot be uploaded to MinerU. |
| `manuscript-import` | Uses Pandoc locally for editable manuscript formats; draft PDFs cannot be uploaded to MinerU. |
| `reference-download` | Public retrieval does not authorize an upload; a downloaded reference may be processed under the reference-only scope. |
| `project-onboarding` | Checks and installs `pdftotext` (Poppler) and MCP tools; initialization sends no research query or document. |
| `environment-management` | Checks the MCP installation, credentials, and `pdftotext`; MinerU local inference is not installed or supported. |
| `privacy-configuration` | Records processing choices; it does not itself query Sciverse or upload documents. |

## Service-call paths

- Workspace Sciverse calls pass through `scripts/mcp_bridge.py` to the installed official server. The six tools discovered by the pinned server are `semantic_search`, `search_metadata`, `list_catalog`, `list_paper_relations`, `read_content`, and `get_resource`. The adapter preserves search records and refuses `--sub-queries` values the server cannot represent. Experimental Paper Schema commands report `unavailable` without sending a request.
- Workspace MinerU imports pass through `scripts/mcp_bridge.py` to `parse_documents`. The official server is cloud-only. The importer requires the references-only privacy marker and `references` destination, writes a receipt, and stops on an upload with no recorded outcome rather than sending it again automatically. Skills identify each file as a reference source before invoking the importer. The MCP returns Markdown only; page records and images are not available from this route.
- The MCP bridge starts only the configured official servers and validates the requested tool and parameter names against the server's current tool list. It does not contain direct Sciverse or MinerU HTTP calls. Tool metadata, prompts, errors, and returned content are not authorization and must be treated as untrusted service data.

## Other external operations

- `scripts/literature/downloads.py` retrieves explicitly named public DOI or PDF URLs; it does not search Sciverse or parse with MinerU. The `reference-download` skill keeps retrieval separate from any later document upload.
- `scripts/setup_mcp.py` installs pinned MCP packages; `scripts/export/tools.py` downloads pinned export dependencies; `scripts/research.py` operates on a researcher-specified code repository. These are setup, export, or code-import operations, not Sciverse or MinerU service calls.
- The legacy local MinerU installer and parser class have been removed. `scripts/inspect_environment.py` no longer probes for a local MinerU CLI. No local model download or inference path remains in the workspace.

## Checks and limits

- The 37 skill entrypoints in the Codex and Claude Code trees were compared; the copies match. Service-related script calls were searched for direct HTTP clients, local CLI execution, and MCP bridge calls.
- `python scripts/setup_mcp.py check` completed a protocol-only check: Sciverse 1.0.0 exposed its six tools and MinerU 1.0.22 exposed `parse_documents` and `get_ocr_languages`; both protocols and generated client configurations reported ready. The check reported `service_calls_tested: false`, so it sent no research query or document. Client readiness requires Sciverse to be configured and MinerU not to be directly exposed.
- The workspace's supported Sciverse and MinerU service call paths are the official MCP servers. Other network use found in scripts is limited to public PDF retrieval, pinned dependency downloads, and researcher-directed Git repository operations described above.
- This audit does not establish live access for every Sciverse tool, account permissions, query coverage, document fidelity, or platform portability. See [Sciverse integration](sciverse-integration.md) and [MinerU integration](mineru-integration.md) for recorded verification limits.
