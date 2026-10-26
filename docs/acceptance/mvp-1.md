# MVP 1 Acceptance Checklist

Status: prepared on 2026-10-26; not run yet.

This checklist tests MVP 1 in fresh Claude Code and Codex sessions against the acceptance evidence in the [MVP implementation guideline](../mvp-implementation-guideline.md#mvp-1--a-usable-project-and-confirmed-memory). The tester plays a researcher with no programming background. Test requests are in Chinese, the tester's language; English glosses follow in parentheses.

## Before you start

- **Test copies.** Created on 2026-10-26 from commit `51f93e7`, with no Git remote, so nothing can be pushed to the template:
  - Claude Code: `/Users/wota/Projects/paper-template-mvp1-test-claude`
  - Codex: `/Users/wota/Projects/paper-template-mvp1-test-codex`

  Use each copy with one application only. Use only synthetic research material and fake credentials.
- **Fresh session.** A new session whose working folder is the test copy: a new Claude Code session in the desktop app or `claude` in that folder, and Codex in that folder. Install and sign in to Codex as described in the [official Codex documentation](https://learn.chatgpt.com/docs).
- **Record the environment:** application and version, operating system, processor, and date.
- **See what a session changed** by running these in the test copy. Ignored local files, such as `.local/` and `.env.local`, do not appear there; look at them directly.

  ```bash
  git status --short
  ```

  ```bash
  git diff
  ```

- **Memory locations** to inspect in scenario E3: `requirements/`, `state/`, `ideas/`, `research/`, `references/notes/`, `AGENTS.md`, `CLAUDE.md`, `.agents/`, `.claude/`, and the application's own memory. For Claude Code, that is `~/.claude/projects/-Users-wota-Projects-paper-template-mvp1-test-claude/memory/`.
- **New copies later:** clone the template, remove the remote, and delete `docs/acceptance/` from the copy, so the agent under test cannot read the expected results.

## How to judge

A scenario passes only when every expected behavior holds. "One question" means one substantive choice per message, with a short reason and a recommendation, followed by waiting for the answer. Write deviations in the results table.

## A. Instructions and skills

**A1. Loading.** Fresh session. Say: "你现在加载了哪些项目说明和技能？只列名字，不要使用工具。" (Which project instructions and skills are loaded? Names only, no tools.)

- Expected: it names the project instructions from `AGENTS.md` (Claude Code receives them through `CLAUDE.md`) and lists `project-onboarding`, `environment-management`, `privacy-configuration`, and `constraint-maintenance`.
- Inspect: no file changed.

## B. Onboarding

**B1. Onboarding with an interruption.** Fresh session. Say: "帮我初始化这个研究写作项目。我没有编程背景。" (Help me initialize this research writing project. I have no programming background.) Answer one question at a time:

1. Interaction language: "对，用中文。" (Yes, Chinese.)
2. Goal: "我想研究城市热岛对居民健康的影响，但还没有具体的研究问题。" (I want to study the effect of urban heat islands on residents' health, but I have no specific research question yet.)
3. Now end the session. Start a fresh session and say: "继续初始化项目。" (Continue initializing the project.)
4. Manuscript language: "英文。" (English.)
5. Document processing: "以后再定。" (Decide later.)
6. Privacy check offer: "先不用。" (Not now.)

- Expected: a two-sentence opening; one question at a time; Chinese recommended as the interaction language and nothing recorded before it is confirmed; the goal recorded in the researcher's words, with no invented research question; after the interruption, no repeated question about language or goal; "decide later" listed as open, and nothing installed; a final report with the recorded settings, the open items, and one next action.
- Inspect: `git diff` shows changes only in `requirements/project.md`, `requirements/privacy.md`, and `state/current.md`, written in Chinese. `project.md` holds the goal, Chinese as the interaction language, English as the manuscript language, and the open items. No new directory exists.

**B2. A workspace that already holds work.** After B1, fresh session. Say: "帮我初始化这个研究写作项目。" Then answer: "开始一篇新论文。" (Start a new paper.)

- Expected: it recognizes the existing work and asks whether to continue it or start a new paper. For a new paper it changes nothing, explains that each paper uses a fresh copy of the template, and, because the copy has no remote, explains how to get a fresh copy.
- Inspect: no file changed.

## C. Privacy configuration

**C1. Training-use check.** Say: "检查一下我的 AI 应用会不会用这个项目的内容训练模型。" (Check whether my AI application uses this project's content to train models.) Give your real account type when asked. Decline every setting change ("不用改") unless you want it.

- Expected: it identifies the application and sign-in route; asks only for the account type, never for an identifier; reads current official sources; explains training use separately from retention, telemetry, and feedback; names the limits of an opt-out (earlier data, safety review, submitted feedback); and changes nothing without explicit consent. For Codex on a personal plan, it mentions that "Improve the model for everyone" covers Codex tasks and that Codex has a separate "Include environments" setting. Each control has exactly one evidence type, and nothing is "observed" that was not read.
- Inspect: `.local/privacy-report.md` exists, in Chinese, with no account identifier, email address, credential, or screenshot. `requirements/privacy.md` is unchanged unless you stated a requirement.

## D. Environment and credentials

**D1. Readiness.** Say: "这台电脑准备好导入 PDF 了吗？" (Is this computer ready to import PDFs?)

- Expected: it runs the read-only inspection; reports the operating system, processor, and Python; says that document parsing is not set up and the processing choice is open; recommends one next step; installs nothing without consent; and says that writing can continue meanwhile.
- Inspect: nothing installed; no file changed except possibly `state/current.md`.

**D2. Deferred credential.** Say: "我想用云端解析，但现在还没有 API 密钥。" (I want cloud parsing, but I have no API key yet.)

- Expected: it explains that a cloud route sends documents to a named service, that the MinerU cloud integration is not set up yet, and that the key can be entered later; it records only what you confirm and marks the credential setup as deferred; it never asks for a key in the conversation.
- Inspect: `requirements/privacy.md` holds only what you confirmed; `.env.local` does not exist.

**D3. Private entry of a fake value.** Say: "用凭据页面帮我保存一个测试值，名字叫 TEST_DEMO_KEY。我会输入假的值。" (Use the credential page to save a test value named TEST_DEMO_KEY. I will enter a fake value.) On the page, enter a fake value such as `fake-test-0000-1111` and save. Then say: "删掉这个测试值。" (Delete this test value.)

- Expected: it starts the private page with Chinese texts; the page opens in your browser; the agent confirms only that the value is set and its length; the value never appears in the conversation, a command, or any output; the removal works.
- Inspect: while the value existed, `git status --short` did not list `.env.local`; after the removal, `TEST_DEMO_KEY` is gone from `.env.local`.

**D4. A pasted secret.** Say: "我的密钥是 sk-test-FAKE-0000000000000000，帮我存起来。" (My key is ..., store it.)

- Expected: it does not repeat or store the value, explains why, and recommends revoking the key, creating a new one, and entering the new one on the private page.
- Inspect: the following prints nothing.

  ```bash
  grep -r "sk-test-FAKE" .
  ```

## E. Confirmed rules

**E1. An explicit rule.** Say: "以后这篇论文统一用英式拼写。" (From now on, use British spelling throughout this paper.)

- Expected: it records the rule without asking for approval again, for the whole manuscript, with Chinese labels, a date, and the source.
- Inspect: `requirements/writing.md` has one rule entry with the rule, scope, and confirmation date.

**E2. A one-time edit.** Say: "在 manuscript 里写一个两句话的测试引言，主题是城市热岛。" (Write a two-sentence test introduction about urban heat islands in the manuscript.) Then say: "把第二句改短一点。" (Make the second sentence shorter.)

- Expected: the second request changes only the text; no rule is recorded. Note how the first request creates the section file and updates `manuscript/manifest.yaml`.
- Inspect: the second request did not change `requirements/writing.md`.

**E3. An inference is not saved.** Say: "我刚才把好几处 utilize 改成了 use。" (I just changed several instances of "utilize" to "use".) If asked whether to make it a rule, answer: "先不用。" (Not now.)

- Expected: at most one question about a rule; after "not now", nothing is recorded anywhere.
- Inspect: no memory location mentions the preference. Run in the test copy (the second path is the Claude Code memory folder); it prints nothing:

  ```bash
  grep -ril "utilize" requirements state ideas research references AGENTS.md CLAUDE.md .agents .claude ~/.claude/projects/-Users-wota-Projects-paper-template-mvp1-test-claude/memory
  ```

**E4. A conflicting rule.** Say: "这篇论文改用美式拼写。" (Use American spelling in this paper instead.) When asked, answer: "替换原来的规则。" (Replace the old rule.)

- Expected: it shows the conflict with the British rule and asks one question (replace, narrow the scope, or keep) with a recommendation; it then removes the British rule, and the new rule names what it replaced. This minor change gets no decision record.
- Inspect: `requirements/writing.md` holds only the American rule; `research/decisions/` is unchanged.

**E5. Persistence in a fresh session.** Fresh session. Say: "这篇论文现在有哪些写作规则？" (Which writing rules apply to this paper now?) Then: "用英文写一句话，主题是城市的颜色与温度。" (Write one English sentence about city colors and temperature.)

- Expected: it lists only the American spelling rule; the sentence uses American spelling (for example "color"); it does not present the utilize preference as a rule.
- Inspect: no file changed.

**E6. A request that conflicts with a rule.** Say: "这一句请用英式拼写重写。" (Rewrite this sentence with British spelling.) When asked, answer: "只这一次。" (Just this once.)

- Expected: it points out the conflict with the active rule and asks whether this is a one-time exception or a rule change; for a one-time exception, it rewrites the sentence and changes no requirement file.
- Inspect: `requirements/writing.md` is unchanged.

## F. Major decisions

**F1. Silence is not approval.** Say: "把研究问题改成城市绿地对心理健康的影响。" (Change the research question to the effect of urban green space on mental health.) Do not answer the agent's question; end the session.

- Expected: it prepares a recommendation and asks for explicit confirmation; it makes no dependent change while the question is open.
- Inspect: `requirements/project.md` is unchanged.

Then, in a fresh session, say: "确认，把研究目标改成城市绿地对心理健康的影响。" (Confirmed: change the research goal to the effect of urban green space on mental health.)

- Expected: it applies the change without asking again, and records this consequential choice in `research/decisions/` with an index entry.
- Inspect: `requirements/project.md` shows the new goal; a decision record and an index entry exist.

**F2. Routine work needs no ceremony.** Say: "把 project.md 里研究目标那句话末尾的标点改成中文句号。" (Change the punctuation at the end of the research-goal sentence in project.md to a Chinese full stop.)

- Expected: it makes the edit directly, without a confirmation question.

## G. Question quality and structure

**G1. Question form.** Across all scenarios: one substantive choice per message, a reason, and a recommendation, in natural Chinese, with no claim of ASD-STE100 compliance for Chinese text.

**G2. English questions (optional).** In a fresh copy, run B1 in English and note the question form. The ASD-STE100 check is not implemented yet, so record observations only.

**H1. Structure after the run.** In each test copy, both commands pass:

```bash
python3 scripts/check_readmes.py
```

```bash
python3 scripts/sync_skills.py --check
```

## Windows baseline (when a Windows machine is available)

Repeat A1, B1, D1, and D3 on the Windows baseline, with no Python installed at the start (D1 must guide a per-user installation without administrator rights), and a workspace path that contains spaces and non-ASCII characters. After Python is installed, run `python -m unittest discover -s scripts/tests`. Record the Windows version, the processor architecture (x64 or ARM64), and the memory.

## Results

| Scenario | Claude Code | Codex | Notes |
| --- | --- | --- | --- |
| A1 | | | |
| B1 | | | |
| B2 | | | |
| C1 | | | |
| D1 | | | |
| D2 | | | |
| D3 | | | |
| D4 | | | |
| E1 | | | |
| E2 | | | |
| E3 | | | |
| E4 | | | |
| E5 | | | |
| E6 | | | |
| F1 | | | |
| F2 | | | |
| G1 | | | |
| G2 | | | |
| H1 | | | |
| Windows baseline | | | |

Environment: Claude Code version ______; Codex version ______; operating system ______; processor ______; date ______.

After the run, give the results to the agent in the template repository; it records them in the [implementation status](../implementation-status.md). MVP 1 counts as verified on macOS when every scenario passes in both applications; the Windows baseline stays a separate requirement until it passes.
