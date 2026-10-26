# Official Sources for Privacy Checks

Starting points for the `privacy-configuration` skill, checked on 2026-10-26 by reading each page. Providers change their products and policies: read the current page again before you rely on any statement here. The summaries are short paraphrases, not policy text.

## Claude (Anthropic)

| Route | Source | What the page said on 2026-10-26 |
| --- | --- | --- |
| Claude Code on a consumer plan (Free, Pro, Max) | [Claude Code data usage](https://code.claude.com/docs/en/data-usage) | Sessions can be used for training when the account's model-improvement setting is on. Retention is 5 years with the setting on and 30 days with it off. |
| Consumer training setting | [Change model-improvement settings](https://privacy.claude.com/en/articles/12109829-how-do-i-change-my-model-improvement-privacy-settings) | The toggle "Help Improve our AI models" is under Settings, Privacy (claude.ai/settings/data-privacy-controls) and also covers coding sessions. Turning it off does not remove data from training that has already started or from trained models. |
| Consumer exceptions | [Is my data used for model training?](https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training) | Conversations flagged for safety review, explicit opt-in programs, and rated feedback (thumbs up or down) can still be used. Incognito chats are not used. |
| Claude Code on commercial terms (Team, Enterprise, API, cloud platforms) | [Claude Code data usage](https://code.claude.com/docs/en/data-usage) | Not used for training unless the organization opts in, for example through the Development Partner Program. Standard retention is 30 days. |
| Claude Code telemetry and feedback | [Claude Code data usage](https://code.claude.com/docs/en/data-usage) | Separate from training. `DISABLE_TELEMETRY`, `DISABLE_ERROR_REPORTING`, `DISABLE_FEEDBACK_COMMAND`, and `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY` turn off single items. `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` turns off all non-essential traffic and can make Remote Control unavailable. Feedback reports include the conversation. Session transcripts are also kept on the computer under `~/.claude/projects/`. |

## OpenAI

| Route | Source | What the page said on 2026-10-26 |
| --- | --- | --- |
| ChatGPT and Codex on a personal plan (Free, Plus, Pro) | [Data controls in ChatGPT](https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt) | Training is on by default. "Improve the model for everyone" under Settings, Data controls also covers Codex tasks; "Do not train on my content" in the OpenAI Privacy Portal is an alternative. Codex has a separate "Include environments" setting for environment context, which the ChatGPT setting does not change. Rated feedback can still be used. |
| ChatGPT Business, Enterprise, Edu | [Data controls in ChatGPT](https://help.openai.com/en/articles/7730893-data-controls-in-chatgpt) | Not used for training by default; the organization's policies apply. |
| OpenAI API | [Your data](https://developers.openai.com/api/docs/guides/your-data) | Not used for training unless the organization opts in. Abuse-monitoring logs are kept for up to 30 days by default; zero data retention needs approval. |

The OpenAI Help Center refuses automated page fetching. On 2026-10-26 it was read in a browser.

## Document processing

A MinerU cloud service is a separate data processor. Its training use and retention have not been checked. Check its terms before the first upload (MVP 2).
