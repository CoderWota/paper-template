---
name: literature-discovery
description: Find and screen literature within a confirmed scope; record providers and coverage, with Sciverse first when authorized.
---

# Literature discovery

Outcome: a bounded, reviewable set of literature leads with a record of where and how each was found, why it is relevant, and whether the full text is available. A search result is a lead, not evidence that the source was read or that a research gap is new.

## Read before searching

1. Read `state/current.md`, `requirements/project.md`, and the relevant entries in `requirements/privacy.md`.
2. Inspect `references/index.md` and only the existing source notes or extractions that match the question. Do not load the full library.
3. Turn the request into a short search plan: core concepts, useful synonyms, dates or source types if the researcher supplied them, and the purpose of each pass. Do not narrow the question by inventing a discipline, method, language, date range, or venue.

## External search and provider order

Discover relevant host search tools only when this task needs them; inspect the selected schemas before calling. No startup enumeration of MCP servers or resources is needed. Provider discovery does not authorize a new destination.

Use OpenDataLab Sciverse as the first external literature-search provider. The query and any supplied identifiers sent to Sciverse leave this computer and go to its API. First check the active confirmed query-sharing scope in `requirements/privacy.md`: reuse it without another question when it covers the request. If no active scope covers the query, explain the transfer in the interaction language and ask one scope question before sending it. The public API pages reviewed here do not establish query retention or training use; say those points are unknown. State that Sciverse search may require an account or API key and that access or cost depends on the account; do not enroll the researcher or incur a charge without explicit confirmation.

For an actual Sciverse request, read the relevant section of [Sciverse operations](sciverse-operations.md). It specifies scope recording, private credential entry, exact scope excerpts, and search commands. Read structured pagination, relations, experimental Paper Schema, or context retrieval only when that operation is needed. Do not invoke experimental operations automatically.

After the Sciverse pass, use the model host's built-in search only to broaden discovery, cross-check coverage, or fill a defined gap, and only within the researcher's confirmed privacy scope. If Sciverse is unconfigured, unavailable, outside scope, or blocked by account permissions or quota, state why before any fallback. Do not reverse provider priority silently. If the built-in search's data scope is not authorized, pause before sending that query.

When host search is used, record its exact query, provider, returned leads, and coverage gap using [the host-search record format](host-search-records.md). Do not load this format for a Sciverse-only search.

Use `search-local` when looking for passages in imported files. It streams the selected extractions and saves a local search record. Its Markdown line number is not a PDF page number:

```text
python scripts/literature.py search-local --query "..." [--source-id src-...]
```

## Screen and report

- Deduplicate exact source files by source ID/checksum. Keep preprints, accepted manuscripts, and published versions separate, with a relationship only when checked.
- For each lead, distinguish search snippet, abstract, metadata, extracted full text, and the original inspected. Report unknown, conflicting, or missing metadata without filling it from memory.
- State the search dates, providers, main query concepts, known limits, screening scope, duplicates/versions, and which full texts could not be obtained. Do not claim coverage is complete, that no prior work exists, or that an idea is unprecedented.
- Use `references/searches/<search-id>/README.md` as the durable search record. The host-search input must include its exact query and a non-empty `coverage_note` naming the gap or cross-check; the script rejects either omission and timestamps the provider route. Keep interpretation in per-source notes under `references/notes/`; do not paste whole private chats into persistent notes.
- Ask a consequential question only when the choice changes a major research scope, privacy boundary, or source-collection decision. Follow the shared confirmation rule in `AGENTS.md`.

## Completion check

- The first external literature pass used Sciverse when it was authorized and available; every secondary/fallback pass has a stated purpose and provider.
- Search results retain identifiers and source locators. No snippet is described as full-text reading.
- Coverage limits, access gaps, uncertainty, and contradictory leads are visible in the report.
- No new account was created and no paid access was started without confirmation.
