# Official Sources for Model Selection

Starting points for the `model-selection` skill, checked on 2026-10-29 and 2026-10-30 by reading each page. Model offers, names, defaults, and plans change often: read the current page again before you rely on any statement here. The summaries are short paraphrases of what each page said on those dates, not the page text.

## Claude Code

| Topic | Source | What the page said |
| --- | --- | --- |
| Models and aliases | [Model configuration](https://code.claude.com/docs/en/model-config) | Aliases `default`, `best`, `fable`, `opus`, `sonnet`, `haiku`, `opusplan`, and `[1m]` variants. On the Anthropic API, `opus` resolved to Opus 5.5, `sonnet` to Sonnet 5.5, and `haiku` to Haiku 5.5; other providers resolved some aliases to older versions. The page suggested Fable for the hardest and longest tasks, Opus for complex reasoning, Sonnet for daily work, and Haiku for simple tasks. |
| Defaults and plans | Same page | `default` resolved to Opus 5.5 on most plans and providers. Fable was the default on no plan; it could draw on usage credits, and the picker showed when it did. Organizations can restrict the available models. |
| How to switch | Same page | `/model <alias>` in a session (it also saves the choice for new sessions unless the session-only key in the picker is used), `claude --model <alias>` at launch, the `ANTHROPIC_MODEL` environment variable, or the `model` key in a settings file. A model in project or managed settings applies again at every launch. |

## Codex

| Topic | Source | What the page said |
| --- | --- | --- |
| Models | [Models](https://learn.chatgpt.com/docs/models) (the older address `developers.openai.com/codex/models` redirects here) | Recommended models: Astra (`gpt-6-astra`) for demanding multi-step projects, 6.1 Sol (`gpt-6.1-sol`) for long-running work where cost matters, 6.1 Terra (`gpt-6.1-terra`) for fast drafting and reading charts or screenshots, and 6 Luna (`gpt-6-luna`) for narrow, high-volume work. Reasoning effort ranges from Light or Low to Max, with Ultra for work that divides into parallel parts. |
| Plans and retirements | Same page | Available models depend on the subscription tier, administrator settings, and staged releases; with an API key, on the key's organization and project. GPT-5.5 was removed from Codex for ChatGPT sign-ins on 2026-10-14. |
| How to switch | Same page | `codex --model <id>` (or `-m`), the `/model` command in a session, the `model` key in `config.toml` (shared by the app, the terminal, and the IDE extension), or the model and effort control in the desktop app. |

## Cursor

| Topic | Source | What the page said |
| --- | --- | --- |
| Models and plans | [Models](https://cursor.com/docs/models) | Cursor's own models and third-party models from several providers, including Anthropic, OpenAI, and Google. Third-party models were available from the Premium plan up. An Auto mode lets Cursor choose the model per request; which Auto modes exist depends on the plan. |

## Other applications

For a chat application or another agent, read the provider's current help page on choosing a model, and record it here with its date when the template maintainer adopts it.
