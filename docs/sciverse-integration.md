# Sciverse Literature Integration

Checked against OpenDataLab's public documentation on 2026-10-28. These are integration facts, not researcher consent, a credential, or proof that an account has access.

## Documented API

Sciverse documents a Bearer-token API at `https://api.sciverse.space`. The integrated `agentic-search` endpoint is `POST /agentic-search`; it accepts a natural-language query, optional `top_k` (1–100), `sub_queries` (0–4), and filters. The query limit is 4096 characters. Results may include snippets, `doc_id`, `chunk_id`, character offset, PDF page number, title, abstract, and metadata. Fields vary by account permissions, so callers must tolerate missing values. [Official agentic-search reference](https://sciverse.opendatalab.org.cn/docs/sciverse/api/agentic-search)

The structured `POST /meta-search` endpoint returns bibliographic metadata for title, DOI, and field-based searches; it does not return evidence passages. Its documentation directs clients to `meta-catalog` before building filters. The workspace integration supports query-only title/DOI metadata lookup and does not construct filters. [Official meta-search reference](https://sciverse.opendatalab.org.cn/docs/sciverse/api/meta-search)

The `GET /content` endpoint can retrieve source text by `doc_id`, `offset`, and `limit`. Offsets count Unicode characters; a source may have no readable full text. This adapter records the retrieved range separately from initial search snippets. [Official content reference](https://sciverse.opendatalab.org.cn/docs/sciverse/api/content)

The API documentation says HTTP 429 means an account quota/rate limit and recommends waiting instead of retrying; 500/502/503 may be retried with backoff. The adapter follows that distinction for Sciverse requests. [Official agentic-search reference](https://sciverse.opendatalab.org.cn/docs/sciverse/api/agentic-search)

Sciverse documentation also lists the `meta-catalog` endpoint, resources, MCP Skills, CLI, and SDKs. This workspace integrates agentic search, query-only metadata search, and bounded content retrieval. It does not claim those other interfaces work here. [Official API overview](https://sciverse.opendatalab.org.cn/docs)

## Privacy and account boundary

A Sciverse request sends the research query and any supplied identifiers to OpenDataLab. Before the first request in a workspace, the researcher must confirm which queries and identifiers may be sent. The exact confirmation and its scope belong in `requirements/privacy.md`; a machine marker lets `scripts/literature.py` refuse an unconfirmed request. The agent must still check that each query fits the human-readable scope.

The public docs say API keys are created through the account console and that a basic trial quota may be available, with actual access depending on account permissions. They do not establish this researcher's account access or a fixed price. Do not create an account, start a paid plan, or incur a charge without confirmation. Store a key only through `scripts/credentials.py` as `SCIVERSE_API_KEY`; requests are sent only to the fixed documented API host, and the key is not written to search records.

The API and overview pages reviewed here do not state how search queries are retained or whether they are used for training. This review did not establish a separate query-data policy. Do not claim that query retention or training use is off; disclose that these points are unknown when asking whether a query scope may be sent.

## Implementation boundary

`scripts/literature.py` records the provider, query, date, response fields, source identifiers, locators, and errors in `references/searches/`. A returned snippet remains labeled as a discovery snippet. The local search reads extracted Markdown without a vector database. Public PDF retrieval is a separate route; it does not use Sciverse downloads or the account's full-text endpoint to create an archived PDF.

The Sciverse API, account permissions, live search, full-text retrieval, quota behavior, and Windows/Codex operation have not been exercised in this workspace. A successful code path or public API reference does not establish that the service works for a particular account.
