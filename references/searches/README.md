# Literature Search Records

Search records, one folder per search, preserve each provider route's timestamp, exact query, source identifiers and locators, coverage purpose, errors, and access limits. Sciverse routes also retain the exact excerpt from the active query-sharing scope that the agent checked. Provider snippets are discovery leads; a record does not say that full text was read. The agent maintains these records with `scripts/literature.py`.

Metadata searches can be resumed one page at a time. Each page and failed attempt is retained in the same record. A continuation reuses the last successful page's query, filters, sort, page size, next cursor and catalog snapshot, and checks that its original scope remains active. Account permissions may have changed since that snapshot; the service may reject the request. A missing cursor or repeated cursor stops continuation; a failed request leaves the prior successful page available for retry.

Results sharing a normalized DOI are listed as unverified duplicate candidates. All result records remain present: the agent checks identity, version relationships and any corrections or retractions independently before making claims about them.
