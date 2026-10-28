---
name: literature-discovery
description: Use when the researcher asks to find, search for, collect, screen, or compare possible literature sources. Plans the search, queries Sciverse first when confirmed and configured, records secondary or fallback searches by provider, and reports coverage and full-text gaps without claiming exhaustiveness.
---

# Literature discovery

Outcome: a bounded, reviewable set of literature leads with a record of where and how each was found, why it is relevant, and whether the full text is available. A search result is a lead, not evidence that the source was read or that a research gap is new.

## Read before searching

1. Read `state/current.md`, `requirements/project.md`, and the relevant entries in `requirements/privacy.md`.
2. Inspect `references/index.md` and only the existing source notes or extractions that match the question. Do not load the full library.
3. Turn the request into a short search plan: core concepts, useful synonyms, dates or source types if the researcher supplied them, and the purpose of each pass. Do not narrow the question by inventing a discipline, method, language, date range, or venue.

## External search and provider order

Use OpenDataLab Sciverse as the first external literature-search provider. The query and any supplied identifiers sent to Sciverse leave this computer and go to its API. Before its first request, explain this in the interaction language and ask one scope question. The public API pages reviewed here do not establish query retention or training use; say those points are unknown. State that Sciverse search may require an account or API key and that access or cost depends on the account; do not enroll the researcher or incur a charge without explicit confirmation.

If the researcher confirms a scope, record their exact confirmation and the scope in an interaction-language Markdown note under `.tmp/`, then run:

```text
python scripts/literature.py authorize-sciverse --record .tmp/sciverse-confirmation.md
```

The command records that choice in `requirements/privacy.md`. Do not run it for a wish, a suggestion, silence, or a default. The API key is optional. If the researcher chooses to use Sciverse and it is not set, first explain the account/key requirement, then direct them to the private entry flow:

```text
python scripts/credentials.py set SCIVERSE_API_KEY --label "Sciverse API key" --help-url "https://sciverse.opendatalab.org.cn/docs"
```

Never ask for, repeat, print, or store the key in a project record, shell argument, or conversation. The API integration is attempted only when the confirmed scope covers the actual query and the credential is available. To search:

```text
python scripts/literature.py search-sciverse --query "..." --top-k 10
```

For a title or DOI lookup, use Sciverse metadata search. It returns bibliographic metadata, not evidence passages or proof of full-text access:

```text
python scripts/literature.py search-sciverse-metadata --query "10.1234/example"
```

If the researcher changes or withdraws the scope, use `constraint-maintenance` to record only the newly confirmed active requirement and any required decision record. Then use `authorize-sciverse --replace` with the new confirmed record, or `revoke-sciverse` after removing the requirement. Do not delete the API key unless the researcher asks for that separate action.

The script stores provider, query, date, returned identifiers and locators, account-limited fields, and service errors in `references/searches/<search-id>/`. It labels chunks as search snippets. When a result has a `doc_id`, fetch a bounded text range only when needed to check a claim:

```text
python scripts/literature.py read-sciverse-context --search-id ID --doc-id DOC_ID --offset OFFSET --limit 2000
```

After the Sciverse pass, use the model host's built-in search only to broaden discovery, cross-check coverage, or fill a defined gap, and only within the researcher's confirmed privacy scope. If Sciverse is unconfigured, unavailable, outside scope, or blocked by account permissions or quota, state why before any fallback. Do not reverse provider priority silently. If the built-in search's data scope is not authorized, pause before sending that query.

Save host-search results as `.tmp/host-search.json` with this shape. Append to the Sciverse record with `--search-id ID`; when Sciverse was not used, omit `--search-id` to create a standalone record:

```json
{
  "query": "the exact query used",
  "provider": "model-host built-in search",
  "coverage_note": "which gap or cross-check this pass addressed",
  "results": [
    {"title": "source title", "url": "source URL", "snippet": "short returned snippet"}
  ]
}
```

```text
python scripts/literature.py record-host-search [--search-id ID] --input .tmp/host-search.json
```

Use `search-local` when looking for passages in imported files. It streams the selected extractions and saves a local search record. Its Markdown line number is not a PDF page number:

```text
python scripts/literature.py search-local --query "..." [--source-id src-...]
```

## Screen and report

- Deduplicate exact source files by source ID/checksum. Keep preprints, accepted manuscripts, and published versions separate, with a relationship only when checked.
- For each lead, distinguish search snippet, abstract, metadata, extracted full text, and the original inspected. Report unknown, conflicting, or missing metadata without filling it from memory.
- State the search dates, providers, main query concepts, known limits, screening scope, duplicates/versions, and which full texts could not be obtained. Do not claim coverage is complete, that no prior work exists, or that an idea is unprecedented.
- Use `references/searches/<search-id>/README.md` as the durable search record. Keep interpretation in per-source notes under `references/notes/`; do not paste whole private chats into persistent notes.
- Ask a consequential question only when the choice changes a major research scope, privacy boundary, or source-collection decision. Follow the shared confirmation rule in `AGENTS.md`.

## Completion check

- The first external literature pass used Sciverse when it was authorized and available; every secondary/fallback pass has a stated purpose and provider.
- Search results retain identifiers and source locators. No snippet is described as full-text reading.
- Coverage limits, access gaps, uncertainty, and contradictory leads are visible in the report.
- No new account was created and no paid access was started without confirmation.
