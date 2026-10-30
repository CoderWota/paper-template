---
name: literature-discovery
description: Find and assess prior work for research questions, topic ideas, and related-work checks. Use the project's Sciverse API first; guide query-scope and private-key setup when needed.
---

# Literature discovery

Outcome: a bounded, reviewable set of literature leads with a record of where and how each was found, why it is relevant, and whether the full text is available. A search result is a lead, not evidence that the source was read or that a research gap is new.

## Read before searching

1. Read `state/current.md`, `requirements/project.md`, and the relevant entries in `requirements/privacy.md`.
2. Inspect `references/index.md` and only the existing source notes or extractions that match the question. Do not load the full library.
3. Turn the request into a short search plan: core concepts, useful synonyms, dates or source types if the researcher supplied them, and the purpose of each pass. Do not narrow the question by inventing a discipline, method, language, date range, or venue.

## External search and provider order

Use the project's Sciverse adapter in `scripts/literature.py` for Sciverse requests. A missing Sciverse MCP or host connector does not mean this route is unavailable. Discover model-host search tools only for an authorized host-search pass; inspect their schemas before calling. No startup enumeration of MCP servers or resources is needed. Provider discovery does not authorize a new destination.

Use OpenDataLab Sciverse as the first external literature-search provider. The query and any supplied identifiers sent to Sciverse leave this computer and go to its API. First check the active confirmed query-sharing scope in `requirements/privacy.md`: reuse it without another question when it covers the request. If no active scope covers the query, explain the transfer in the interaction language and ask one scope question before sending it. The public API pages reviewed here do not establish query retention or training use; say those points are unknown. Sciverse access and cost depend on the account; do not enroll the researcher or incur a charge without explicit confirmation.

After a confirmed scope covers Sciverse queries, check `python scripts/credentials.py status SCIVERSE_API_KEY`. If the key is missing, proactively explain the account/key requirement and start the private entry flow in the researcher's language using [credential entry](../environment-management/credential-entry.md). Do not stop at “not configured,” wait for the researcher to request setup, or silently switch to host search. Never read or request the key value in chat. If the researcher declines key setup or Sciverse access fails, use host search only when its own query-sharing scope is authorized; otherwise pause before sending a query. A key-entry choice does not authorize a search query, and permission for one provider does not authorize another.

For an actual Sciverse request, read the relevant section of [Sciverse operations](sciverse-operations.md). It specifies scope recording, private credential entry, exact scope excerpts, and search commands. Read structured pagination, relations, experimental Paper Schema, or context retrieval only when that operation is needed. Do not invoke experimental operations automatically.

After the Sciverse pass, use the model host's built-in search only to broaden discovery, cross-check coverage, or fill a defined gap, and only within its confirmed privacy scope. If Sciverse is unavailable, outside scope, or blocked by account permissions or quota, state why before any authorized fallback. Do not reverse provider priority silently. If the built-in search's data scope is not authorized, pause before sending that query.

When host search is used, record its exact query, provider, returned leads, and coverage gap using [the host-search record format](host-search-records.md). Do not load this format for a Sciverse-only search.

Use `search-local` when looking for passages in imported files. It streams the selected extractions and saves a local search record. Its Markdown line number is not a PDF page number:

```text
python scripts/literature.py search-local --query "..." [--source-id src-...]
```

## Screen and report

- Before a paper informs manuscript claims, background, interpretation, or structure, or is cited, confirm that the original for that exact version is archived at `references/originals/<source-id>/`. A result without that archive remains a search lead. Use [reference-download](../reference-download/SKILL.md) for an authorized public PDF or [source-ingestion](../source-ingestion/SKILL.md) for a researcher-provided document. Abstracts, snippets, Sciverse-only text, search records, source notes, and BibTeX metadata do not count as archived originals. If no authorized full text is available, report the access gap; do not cite or use the paper in manuscript content.
- Deduplicate exact source files by source ID/checksum. If a result is an arXiv preprint, check whether a peer-reviewed published version exists before using it as a citation source. Prefer that version when its identity and support for the cited claim are verified. Keep preprints, accepted manuscripts, and published versions separate, and link versions only after checking their identity. If a published version is found but its original cannot be archived, report the access gap and do not substitute a preprint. If no published version is found in the checked sources, an arXiv preprint may be cited under `requirements/writing.md` only when its original is archived; identify it in the bibliography entry or source record, never in manuscript body text. Do not claim that no version exists beyond the search scope.
- For each lead, distinguish search snippet, abstract, metadata, extracted full text, and the original inspected. Report unknown, conflicting, or missing metadata without filling it from memory.
- State the search dates, providers, main query concepts, known limits, screening scope, duplicates/versions, and which full texts could not be obtained. Do not claim coverage is complete, that no prior work exists, or that an idea is unprecedented.
- Use `references/searches/<search-id>/README.md` as the durable search record. The host-search input must include its exact query and a non-empty `coverage_note` naming the gap or cross-check; the script rejects either omission and timestamps the provider route. Keep interpretation in per-source notes under `references/notes/`; do not paste whole private chats into persistent notes.
- Ask a consequential question only when the choice changes a major research scope, privacy boundary, or source-collection decision. Follow the shared confirmation rule in `AGENTS.md`.

## Completion check

- The first external literature pass used Sciverse when its scope was authorized; a missing key triggered private setup before fallback. Every secondary/fallback pass has a stated purpose and its own authorized provider.
- Search results retain identifiers and source locators. No snippet is described as full-text reading.
- Any paper used as a manuscript source has an archived original for the exact version; unavailable originals remain leads or access gaps.
- Coverage limits, access gaps, uncertainty, and contradictory leads are visible in the report.
- No new account was created and no paid access was started without confirmation.
