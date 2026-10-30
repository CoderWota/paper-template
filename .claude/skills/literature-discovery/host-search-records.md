# Host Search Records

Use this format only when an authorized host search supplements Sciverse or fills a declared fallback gap. Discover the relevant host tools before searching, and retain the exact provider and query.

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

