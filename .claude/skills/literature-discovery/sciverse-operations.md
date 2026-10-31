# Sciverse Operations

`scripts/literature.py` sends Sciverse requests through the installed official Sciverse MCP server (`.tools/mcp/`, installed and checked by `scripts/setup_mcp.py`). It makes no direct API call and does not fall back to one. Read only the operation needed for the current search: scope recording and search first; structured pagination, relations, experimental schema, or bounded text only when requested or needed. All external requests remain subject to the active scope.

If the researcher confirms a scope, record a faithful English rendering of their confirmation and the scope in an English Markdown note under `.tmp/`, then run:

```text
python scripts/literature.py authorize-sciverse --record .tmp/sciverse-confirmation.md
```

The command records that choice in `requirements/privacy.md`. Do not run it for a wish, a suggestion, silence, or a default. A key is required for this route. The workspace stores it as `SCIVERSE_API_KEY`, and the script gives it to the Sciverse MCP server as `SCIVERSE_API_TOKEN`. Once the researcher has confirmed a scope that covers the search, check the key without reading its value:

```text
python scripts/credentials.py status SCIVERSE_API_KEY
```

If it is missing, proactively explain that Sciverse access may require an account and key, and that access or cost depends on the account. Do not create an account or incur a charge. Start the private entry page yourself, using [the credential-entry procedure](../environment-management/credential-entry.md) and page text in the researcher's language; do not merely tell them to run a command. Wait for the page to report `Saved` or `Replaced`, then check status again. Never ask for, repeat, print, or store the key in a project record, shell argument, or conversation. A missing key is a setup step, not an automatic reason to fall back to host search.

Before each request, compare its actual query with the confirmed Sciverse scope. If the scope does not cover the query, ask for a newly confirmed scope before sending it. A fallback provider needs its own authorized query scope. Quote the exact Sciverse scope sentence that covers the query as `--scope-basis`; the script checks that the excerpt occurs in the active scope and records it with the query. This excerpt check supports review but does not replace the agent's scope judgment. To search:

```text
python scripts/literature.py search-sciverse --query "..." --scope-basis "exact confirmed scope sentence" --top-k 10
```

`--top-k` accepts 1 to 100. Keep `--sub-queries` at 0: the installed MCP exposes no sub-query option, and the script refuses other values.

For a title or DOI lookup, use Sciverse metadata search. It returns bibliographic metadata, not evidence passages or proof of full-text access:

```text
python scripts/literature.py search-sciverse-metadata --query "10.1234/example" --scope-basis "exact confirmed scope sentence"
```

For structured metadata, `search-sciverse-metadata` also accepts `--filters` and `--sort` as JSON arrays and `--page`, `--page-size`, or `--cursor`. The adapter checks filters and sorting against the account's catalog. Continue an existing search with `resume-sciverse-metadata --search-id ID`: it retains each attempt in the same record and reuses the last successful page's parameters, next cursor and catalog snapshot. Request only pages needed for the question, record incomplete pagination, and stop on a repeated cursor. Resuming reuses the catalog snapshot to avoid a second catalog call; account permissions may change and service errors must be reported. Only use scope and screening constraints the researcher supplied or confirmed. A sorted search may no longer rank by relevance.

For a selected metadata result, `sciverse-relations --search-id ID --unique-id UNIQUE_ID --relation CITATIONS` retrieves one page; `REFERENCES` and `RELATED_WORKS` are the other relation choices. Use `--page` and `--page-size` to continue. Record the reason for selecting seeds, screen the new leads, and do not treat citation relationships as evidence of support or opposition. Metadata `unique_id` and full-text `doc_id` are distinct. The installed MCP exposes catalog filters, cursor continuation, relations, and resources. They remain unverified against the live service and this account. Paper Schema is not exposed (see below).

Paper Schema is experimental and currently centered on AI conference papers. Do not invoke it automatically. The installed Sciverse MCP exposes no Paper Schema tool, so `experimental-sciverse-schema-search --enable-experimental --search-id ID --unique-id UNIQUE_ID` (a DOI lookup for a recorded metadata result) and `experimental-sciverse-schema-materials --enable-experimental --search-id ID --schema-id SCHEMA_ID --goal survey` (a bounded pack for a returned ID) record `unavailable` and send no request. Use them again only after a Sciverse MCP version that exposes Paper Schema is installed and checked. Check paper identity and every consequential extracted claim against source text; retain and disclose any truncation or unresolved locator.

If the researcher changes or withdraws the scope, use `constraint-maintenance` to record only the newly confirmed active requirement and any required decision record. Then use `authorize-sciverse --replace` with the new confirmed record, or `revoke-sciverse` after removing the requirement. Do not delete the API key unless the researcher asks for that separate action.

The script stores provider, exact query, date, confirmed scope excerpt, returned identifiers and locators, account-limited fields, and service errors in `references/searches/<search-id>/`. It labels chunks as search snippets. Context retrieval checks that the requested `doc_id` belongs to the recorded Sciverse results and that its scope excerpt is still active. When a result has a `doc_id`, fetch a bounded text range only when needed to check a claim:

```text
python scripts/literature.py read-sciverse-context --search-id ID --doc-id DOC_ID --offset OFFSET --limit 2000
```

