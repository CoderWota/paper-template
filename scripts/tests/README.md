# Script Tests

Automated tests for the workspace scripts in [`scripts/`](../README.md). They use only the Python standard library and temporary folders whose paths contain spaces and non-ASCII characters, so the same tests can confirm behavior on Windows, macOS, and Linux.

Run them from the workspace root:

```text
python -m unittest discover -s scripts/tests -v
```

- `test_credentials.py` covers private credential entry through the one-time local page, the Git exclusion check, passing a value to another process, and the rule that no value is ever printed. All values are synthetic.
- `test_workspace_scripts.py` covers the README check, the skill copy script, and the environment report.
- `test_records.py` covers the availability table check and the writing rule check, including the drift each one exists to catch.
- `test_ingest.py` covers document import with the local route, using `fake_mineru_kit.py` in place of MinerU: archiving, duplicates, unsupported files, page coverage and the other checks, interruption and continuation, reuse and re-conversion, protection of hand edits, review rounds with Word comments, tracked changes, and PDF annotations, citation metadata, and the README contract of every new folder.
- `test_ingest_cloud.py` covers the mineru.net route against a fake service on this computer: the refusal without a confirmed choice or a token, uploads that never carry the token, an expired token that stops the batch once, collecting unfinished work without a second upload, and a file that fails at the service. It cannot prove compatibility with the live service.
- `test_research.py` covers the research record checks (decision chains, feedback attribution and decisions, ideas, venue notes, and result records with stale inputs, in Chinese and English), the research code folder and its separate environment, and recorded runs with failures, missing outputs, and refused inputs. `test_ingest.py` also covers research feedback events, whose Word comments keep their authors.
- `test_versions.py` covers the Git operations in disposable repositories with an empty global Git configuration: inspection of inherited template history, scoped saves, refused secrets and oversized files, comparisons with renames, retrieval and restore with the current content kept, the practice copy, and backups to a local bare repository, refused without a confirmed destination and reported as failed when the destination is unreachable.
- `test_literature.py` covers Sciverse privacy and scope gates, provider-specific search records, snippets versus metadata and content, local extraction locators, bibliography links, 429 handling, and resumable public-PDF retrieval against synthetic responses and a local HTTP fixture. `test_sciverse_extensions.py` covers metadata filters, sorting, cursor resumption and recovery, relation provenance, duplicate-version handling, bounded resources, opt-in Paper Schema materials, and scope checks with synthetic responses. Live endpoint observations are recorded separately in the implementation status.

The agent and the template maintainer run these tests after changing a script. Researchers do not need to run them.
