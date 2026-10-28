# MVP 3 Skill Review

Status: all four skills passed written review and MVP 3 was accepted by the maintainer on 2026-10-28 under the MVP 2-style gate. Their deterministic scripts pass 30 literature-specific tests across two modules, and the full script suite passes 79 tests. This does not verify every live service route, publisher access, operating system, or agent host; see section 7.

## 1. Rule and pass criteria

The template maintainer set the acceptance bar as: “我们验收标准和mvp2差不多的标准就行”. This review follows the MVP 2 method in [section 6 of the MVP implementation guideline](../mvp-implementation-guideline.md#6-completion-record-for-each-mvp): review skill text in writing, support deterministic script claims with tests or synthetic observations, and record platform- or service-only behavior as unverified. The manual checklist is optional and no live agent scenario was required.

A skill passes when each readable requirement is met after any needed fix. A script requirement counts as met only with automated test or synthetic evidence. A live observation is used only for a claim that needs a real service. Acceptance by review is not a claim that every integration works.

## 2. Method and evidence

Read all four canonical `SKILL.md` files and their READMEs, `scripts/literature.py`, both modules in `scripts/literature/`, the literature tests, the relevant README contracts, `AGENTS.md`, the MVP 3 section of the guideline, the literature and source-identity sections of the design plan, the shared skill-package rules, and the Sciverse integration record.

The requirements reviewed are MVP 3 in the [implementation guideline](../mvp-implementation-guideline.md#mvp-3--searchable-literature-and-traceable-evidence); [design plan](../design-plan.md) sections 4 (L98–L261), 6 (L351–L364), 8 (L402–L435), 9 (L436–L514), and 14 (L681–L698); `AGENTS.md`; and [the skill-package contract](../../.agents/skills/README.md).

Mechanical and script checks, run on 2026-10-28 after the review edits:

| Check | Result |
| --- | --- |
| `python -m unittest discover -s scripts/tests` | 79 tests, OK; 30 across `test_literature.py` and `test_sciverse_extensions.py` |
| `python scripts/sync_skills.py --check` | Generated skill mirrors match |
| `python scripts/check_capabilities.py` | Availability table matches skill packages |
| `python scripts/check_readmes.py` | Every project directory has a README |
| `python scripts/check_requirements.py` | Requirement records pass form checks |
| `python scripts/ingest.py verify` | Existing ingestion records verify |
| `python scripts/literature.py audit-bibliography` | No bibliography exists yet; no citation links were claimed as checked |
| `python -m compileall -q scripts` | Pass |
| `git diff --check` | Pass |

The literature tests use synthetic Sciverse responses and a local-only HTTP fixture server. They do not contact Sciverse or publishers. Separate live observations are recorded in the [implementation status](../implementation-status.md#mvp-3-implementation-increment-literature-search-retrieval-and-evidence-records) and [Sciverse integration](../sciverse-integration.md): the initial explicitly authorized `agentic-search` check returned three snippets; after the maintainer authorized a bounded service check, `agentic-search` returned three snippets again, `meta-search` returned 25 metadata records, and one `content` request returned 71 characters under a requested limit of 200. The synthetic query was `paper-template connectivity check`. A later four-query smoke run made one `agentic-search` request per public evaluation question with `top_k=5`; all returned five records. The expected climate-paper title appeared in the top five; the expected Transformer paper and named clinical trials were not identified there by title or listed identifiers. No result was read through `content` or checked against an original. All Sciverse calls used disposable test records; their scope records, IDs, metadata, and retrieved text were removed afterward, and no project privacy scope was recorded. The 7 extension tests use synthetic responses for metadata filters, cursor resumption, relation records, duplicate versions, resources, and experimental materials.

## 3. Requirements shared by the four skills

| ID | Requirement | Source | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| CC-1 | One canonical package per skill, required frontmatter, English instructions, and a people-facing README | `AGENTS.md` (Skills); skills README L7–L21; design plan L239–L261 | Met | All four packages have `README.md` and `SKILL.md`; names match their directories; `sync_skills.py --check` passes. |
| CC-2 | The skill describes a complete task with triggers, scope, records, outputs, checks, and handoffs | Skills README L7–L13; design plan L495–L514 | Met | Four descriptions route ordinary-language requests; each skill names its read inputs, procedures, output records, completion checks, and related handoffs. |
| CC-3 | Shared confirmation, language, and source-material rules remain governed by `AGENTS.md` | Skills README L15–L21; `AGENTS.md` (Standing rules) | Met | Skills apply privacy confirmation and interaction-language outputs to their task without replacing the shared contract. |
| CC-4 | Provider identity, query scope, locators, and limits remain visible; snippets are not presented as inspected full text | Guideline MVP 3; design plan L327–L344; `literature-discovery` L18–L18, L32–L52, L77–L89 | Met | Search records and tests retain exact query, provider, timestamp, scope excerpt, IDs, locators, and snippet status; see tests `test_agentic_search_records_provider_scope_query_ids_and_locators`, `test_metadata_results_remain_metadata_only`, and `test_content_context_requires_a_recorded_id_and_active_scope`. |
| CC-5 | Originals, extracted text, and interpretation stay distinct; no source content, locator, or conclusion is invented | `AGENTS.md` (Evidence and integrity; File roles); design plan L351–L364; `literature-and-evidence` L17–L48 | Met | Library and note READMEs preserve the roles; skill instructions require original checks, extraction revisions, exact locators, and explicit uncertainty. |
| CC-6 | Deterministic script behavior has automated evidence | Guideline MVP 3; design plan L681–L698 | Met | The 30 literature tests cover query authorization and records, host/local retrieval, metadata filtering/sorting/pagination, relation provenance, bibliography links, safe public-PDF retrieval, statuses, deduplication, retries, and resumption. |

## 4. Requirements by skill

### 4.1 `literature-discovery`

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| LD-1 | Plan a bounded search from the request and existing compact index, without inventing scope | Met | L10–L14. |
| LD-2 | Ask before sending Sciverse queries, preserve the confirmed scope, check each query against it, protect credentials, and use Sciverse before an authorized host-search fallback | Met | L18–L52; `search.py` `_require_scope_basis`, `validate_scope_basis`, and `context_request`; tests `test_sciverse_search_requires_active_scope_and_matching_excerpt` and `test_cli_checks_scope_before_looking_for_a_credential`. |
| LD-3 | Record provider-specific queries, timestamps, IDs, locators, purpose, and distinct snippet/metadata/context states; keep local line locators tied to extraction revisions | Met | L38–L75; `search.py` `_save_search`, `sciverse_search`, `metadata_search`, `add_host_search`, `local_search`, and `add_context`; tests `test_agentic_search_records_provider_scope_query_ids_and_locators`, `test_host_search_requires_coverage_and_keeps_its_own_query`, `test_standalone_host_search_records_its_exact_query`, and `test_local_search_records_extraction_revision_and_non_page_locator`. |
| LD-4 | Validate metadata filters and sorting against the active catalog, preserve and resume pagination, and record relation results as leads rather than evidence | Met | `literature-discovery` L38–L48; `search.py` `metadata_search`, `metadata_resume_request`, `resume_metadata_search`, and `add_relations`; `test_sciverse_extensions.py` covers synthetic catalog validation, cursors, resumption, failure recovery, relation provenance, and active-scope checks. Live catalog and relation endpoints remain unverified. |
| LD-5 | Restrict service-resource and experimental Paper Schema calls to recorded results and bounded, explicitly enabled requests | Met | `literature-discovery` (Paper Schema); `literature-and-evidence` L15–L17; tests `test_experimental_materials_require_recorded_source_and_preserve_truncation` and `test_resource_requires_recorded_path_and_validates_content`. These operations have not been tested live. |
| LD-6 | Screen versions and access limits honestly; do not claim exhaustive coverage, novelty, or full-text inspection from a snippet | Met | L77–L90. Live metadata results were treated as metadata; the live content check was limited to 71 characters and was not checked against an original. |

### 4.2 `reference-download`

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| RD-1 | State supported inputs and access route; do not claim authenticated or unsupported formats | Met | L10–L14; `downloads.py` L28–L92. The implementation is limited to DOI/URL references from BibTeX, Markdown, or text and publicly returned PDFs. |
| RD-2 | Validate content, archive unchanged under a stable source ID, and record sanitized provenance and distinct outcomes | Met | L25–L33; `downloads.py` L123–L188, L189–L240, L292–L338; tests `test_public_pdf_download_archives_unchanged_and_records_identity`, `test_unavailable_non_pdf_and_incomplete_pdf_keep_distinct_statuses`, `test_login_page_is_not_archived_as_a_pdf`, and `test_signed_url_is_not_stored_or_requested`. |
| RD-3 | Deduplicate, respect host rate limits, resume failed work without repeating completed items, and check identity/version separately | Met | L27–L45; `downloads.py` L145–L188, L246–L357; tests `test_duplicate_doi_is_requested_once`, `test_doi_already_archived_is_not_requested_again`, `test_rate_limit_stops_further_requests_to_the_same_host`, `test_rate_limited_item_retries_only_after_explicit_reset_flag`, and `test_failed_item_retries_without_reprocessing_completed_item`. |
| RD-4 | Keep retrieval permission separate from parser upload, and hand successful archives to the existing ingestion skill only when requested | Met by review | L14, L47–L53. The instructions preserve the boundary; an agent-driven download-to-ingestion handoff was not exercised and remains unverified (section 7). |

### 4.3 `literature-and-evidence`

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| LE-1 | Retrieve only matching local sources and verify consequential passages against originals or trustworthy locators where possible | Met | L10–L15; local-search revision locator test. |
| LE-2 | Record quotations/paraphrases, stable source IDs, separate PDF and printed pages, extraction revisions, verification state, and evidence direction without altering source files | Met | L17–L33; original/extraction/note README roles; `test_local_search_records_extraction_revision_and_non_page_locator`. |
| LE-3 | Compare support, contradiction, qualifications, scope, and uncertainty; separate bibliography linkage from claim support | Met | L35–L48; `test_bibliography_audit_separates_key_link_errors_from_claim_support`. |
| LE-4 | Handle service-only passages without inventing source IDs, preserve version distinctions, and label unchecked correction/retraction status | Met | L15–L23; `literature-and-evidence` keeps service-derived context in its search record when there is no archived source and requires status checks to be scoped or marked unchecked. |

### 4.4 `research-investigation`

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| RI-1 | Keep the inquiry scoped and follow the literature-discovery privacy and provider rules | Met | L10–L21; cross-skill discovery tests. |
| RI-2 | Compare alternative explanations and contrary evidence; distinguish inspected facts, synthesis, inference, and unverified claims, with version and support direction | Met | L23–L31. |
| RI-3 | Report the answer with source links/locators, search/read limits, unresolved contradictions, and no unsupported novelty or manuscript edits | Met | L31–L41. |

## 5. Gaps fixed during implementation

The earlier core review identified and fixed two issues before this written acceptance review: the model-host search route now preserves its own exact query and requires a coverage purpose; URL sanitization is shared with the ingestion network helper and removes signed query data. Metadata filtering, sorting, pagination, and relationship provenance were also added with synthetic tests. Regression evidence is included in the literature tests. No open text or deterministic-script gap remains under the stated acceptance bar.

## 6. Verdict

| Skill | Verdict |
| --- | --- |
| `literature-discovery` | Accepted by review, 2026-10-28 |
| `reference-download` | Accepted by review, 2026-10-28 |
| `literature-and-evidence` | Accepted by review, 2026-10-28 |
| `research-investigation` | Accepted by review, 2026-10-28 |

Acceptance means the written requirements review and deterministic script evidence pass. It does not mean every endpoint, publisher, platform, or model behavior has been verified.

## 7. Remaining verification limits

- Sciverse `agentic-search`, `meta-search`, and bounded `content` each responded in the authorized checks. The small sample does not establish query-result correctness, general availability, account/quota limits, or behavior at errors. Retrieved context was not checked against an original.
- Live behavior for `meta-catalog` filters/sorting, metadata cursor continuation, and `meta-paper-relations` remains unverified; only synthetic tests cover those extensions.
- No live model-host search result has been recorded through the script's host-search input route. Provider recording behavior passes synthetic tests.
- No direct public publisher/repository PDF retrieval was performed. The downloader was tested against a local HTTP server; this proves the scripted validation and record logic, not third-party access.
- Source identity/version review is a recorded agent judgment. The actual comparison of publisher versions and a download-to-`source-ingestion` agent handoff have not been observed.
- The four-question run is only a retrieval smoke test; no source-verified corpus has been used to assess claim support, locator accuracy, semantic interpretation, or contrary-evidence retrieval.
- Windows and Codex skill discovery/loading remain unverified.

The maintainer accepted MVP 3 under the stated MVP 2-style gate: “MVP3就算验收通过吧”. These limits remain visible in the availability table; do not describe unverified routes or platforms as working.
