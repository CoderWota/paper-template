# Private Credential Entry

Read this procedure only when a supported, chosen service needs a credential. It is not part of every environment inspection.

## Credential entry

Do this only for a service that the researcher chose and that needs a credential. An AI application subscription does not mean that a separate API key is necessary.

Check the chosen integration in [capabilities and limits](../../../docs/capabilities.md) before starting credential entry. If it has no supported route, say so and collect no credential. 

The commands below use `python`. When it is not found, use `python3` (macOS and Linux) or `py -3` (Windows).

1. Find the exact variable name and the official page where the researcher gets the value, from the integration's documentation.
2. Explain what the credential allows and where it is stored: `.env.local`, which Git ignores but which is not encrypted.
3. Start the private entry page in the background, so that it can wait for the researcher (up to 10 minutes by default). Write the page texts in the researcher's language:

   ```text
   python scripts/credentials.py set NAME --title "..." --label "..." --note "..." --help-url "https://..." --button "..." --done-message "..." --invalid-message "..."
   ```

   The page opens in the researcher's browser and works only on the computer that runs the command. If the browser does not open, give the researcher the printed address.
4. Tell the researcher to enter the value on that page, not in the conversation. Wait until the command reports `Saved` or `Replaced`.
5. Confirm with `python scripts/credentials.py status NAME`. It shows only whether the value is set and its length.

A program receives the value through `python scripts/credentials.py run --only NAME -- <command>`, or a workspace script reads it with `load_env_local()` from `scripts/credentials.py`. Never put a value in a command argument.

If the researcher pastes a credential into the conversation, do not repeat it and do not store it from the conversation. Recommend that they revoke it at the provider, create a new one, and enter the new one on the private page.

If the command refuses because Git does not ignore `.env.local`, or already tracks it, fix that first. Never weaken this check.

