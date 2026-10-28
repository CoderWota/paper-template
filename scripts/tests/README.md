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

The agent and the template maintainer run these tests after changing a script. Researchers do not need to run them.
