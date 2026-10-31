# Literature Search and Retrieval

Use this guide for query-sharing decisions, Sciverse setup, or incomplete retrieval. Search within the researcher's confirmed question and scope; do not invent language, date, method, venue, or disciplinary restrictions.

## Authorization and provider order

Sciverse is the first external literature provider when configured and authorized. Requests send queries and supplied identifiers to OpenDataLab's Sciverse service. The researcher must confirm which material may be sent; `requirements/privacy.md` records the active scope. The agent compares every request with that scope and supplies an exact confirmed excerpt as `--scope-basis`. The script's excerpt check supplements that judgment rather than replacing it.

Use `literature.py authorize-sciverse --record PATH` only with an actual confirmation. Replace or revoke scope when instructed; changing scope does not imply deleting a credential. If needed, enter `SCIVERSE_API_KEY` through the private page. Account permissions, quota, and possible costs must be established for the actual account. The public pages inspected on 2026-10-28 did not establish query retention or training use; do not imply these are disabled.

A host search connector may broaden coverage or fill a stated gap. Discover only the relevant tools and inspect their schemas. If Sciverse is unavailable, unconfigured, blocked, or outside scope, explain that before using a fallback within its own authorized data scope. Do not silently change providers or destinations.

## Connection

`scripts/literature.py` calls the Sciverse MCP server that `scripts/setup_mcp.py` installs in `.tools/mcp/` (pinned `sciverse-mcp-server` 1.0.0). It makes no direct API request, and it never falls back to one. `python scripts/setup_mcp.py check` verifies the installed server and its tool list without sending a query.

The workspace keeps the key as `SCIVERSE_API_KEY`. The MCP server receives it as `SCIVERSE_API_TOKEN` through its environment, never in command arguments, records, or logs. The server targets `https://api.sciverse.space`.

The MCP exposes six tools: `semantic_search`, `search_metadata`, `list_catalog`, `list_paper_relations`, `read_content`, and `get_resource`. The script maps its operations onto them. It refuses `--sub-queries` above 0, because the MCP has no sub-query option. Paper Schema is not exposed by the installed MCP. Its commands record an `unavailable` result and send no request.

## Search records and source access

The script records the provider, exact query, date, scope excerpt, identifiers, locators, returned fields, gaps, and errors in `references/searches/`. Credentials and signed URLs are not research records.

| Operation | Purpose and boundary |
| --- | --- |
| `search-sciverse` | Agentic search; snippets are discovery leads, not verified evidence. |
| `search-sciverse-metadata` | Title/DOI or structured metadata lookup; metadata does not establish readable full text. |
| `resume-sciverse-metadata` | Continue one recorded page using its parameters and catalog snapshot; report incomplete or repeated cursors. |
| `sciverse-relations` | One page of citations, references, or related works from a selected recorded metadata result; relationships do not establish claim support. |
| `read-sciverse-context` | Bounded text for a `doc_id` in an authorized recorded search; keep inspected ranges and unresolved locators explicit. |
| `read-sciverse-resource` | A derived image or PDF named in recorded authorized context; size and format are checked. |
| `record-host-search` | Save the exact host query and returned leads with the reason for the extra pass or fallback. |
| `search-local` | Retrieve passages from selected local extractions; Markdown line numbers are not PDF page numbers. |

Catalog filters and sorting are validated against the account catalog. Metadata `unique_id` and text `doc_id` are different identifiers. Ask only for pages or text needed for the question, retain truncation indicators, and check consequential claims against the original. The resource operation accepts safe relative resource paths from recorded authorized context. A derived image or PDF resource does not become an archived full-text source automatically.

Live behavior of filters, cursors, relations, and resources remains unverified for this account, and account-dependent fields can be absent. Paper Schema operations are experimental, centered on AI conference papers, and not exposed by the installed MCP. Do not invoke them automatically. Verify identity and every consequential extracted claim.

Commands and record shapes are in the selected [search skill](../.agents/skills/literature-discovery/SKILL.md). Do not preload its detailed operations for unrelated tasks. Public PDF acquisition and document conversion remain separate tasks.

## Coverage and sources

A generic test query returned one result through the MCP on 2026-10-30. That establishes only that the connection works. It does not establish research relevance, exhaustive coverage, dependable account access, or verified locators. Original-source inspection is still necessary. Windows and Linux service operation remain unverified here.

Current official references: [agentic search](https://sciverse.opendatalab.org.cn/docs/sciverse/api/agentic-search), [metadata search](https://sciverse.opendatalab.org.cn/docs/sciverse/api/meta-search), [content](https://sciverse.opendatalab.org.cn/docs/sciverse/api/content), [catalog](https://sciverse.opendatalab.org.cn/docs/sciverse/api/meta-catalog), [relations](https://sciverse.opendatalab.org.cn/docs/sciverse/api/meta-paper-relations), [resources](https://sciverse.opendatalab.org.cn/docs/sciverse/api/resource), and [Paper Schema](https://sciverse.opendatalab.org.cn/docs/sciverse/api/paper-schema). Service facts above are a dated operating reference. Recheck current official sources for setup, pricing, or API changes.
