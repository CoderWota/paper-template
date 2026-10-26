# Script Tests

Automated tests for the workspace scripts in [`scripts/`](../README.md). They use only the Python standard library and temporary folders whose paths contain spaces and non-ASCII characters, so the same tests can confirm behavior on Windows, macOS, and Linux.

Run them from the workspace root:

```text
python -m unittest discover -s scripts/tests -v
```

- `test_credentials.py` covers private credential entry through the one-time local page, the Git exclusion check, passing a value to another process, and the rule that no value is ever printed. All values are synthetic.
- `test_workspace_scripts.py` covers the README check, the skill copy script, and the environment report.

The agent and the template maintainer run these tests after changing a script. Researchers do not need to run them.
