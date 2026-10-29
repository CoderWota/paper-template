# Implementation Status

Agent-maintained record of what has actually been implemented and verified, one entry per MVP from the [MVP implementation guideline](mvp-implementation-guideline.md). Acceptance by review follows the maintainer’s 2026-10-29 MVP 2-style gate; claims about specific platforms, services or live behavior require observed evidence. The presence of a directory, a README, or a SKILL.md is not evidence.

Updated: 2026-10-29.

## Summary

| MVP | Researcher-visible outcome | Status |
| --- | --- | --- |
| 1 | Usable project and confirmed memory | Accepted under the MVP 2-style gate on 2026-10-29; the four skills passed [written review](acceptance/mvp-1-skill-review.md). Earlier live-run misses, Codex/Windows behavior and English question checks remain recorded or unverified. |
| 2 | Flexible intake and MinerU batch ingestion | Accepted under the MVP 2-style gate on 2026-10-29; both skills passed [written review](acceptance/mvp-2-skill-review.md), script tests passed, and local and mineru.net routes were observed on macOS with synthetic files. Windows, Codex, and mineru.net training-use and retention terms remain unverified. |
| 3 | Searchable literature and traceable evidence | Accepted by the maintainer on 2026-10-28 under the MVP 2-style gate: all four skills passed written review, 79 tests and mechanical checks pass, and live Sciverse checks were recorded. Catalog filters/relations, resources, Paper Schema, live public-PDF access, model-host fallback, Windows, and Codex remain explicitly unverified |
| 4 | Ideas, impact, journal choice, and feasible research plans | Accepted by review on 2026-10-28: seven skills and the result-record extension of `research-investigation` passed written review ([skill review](acceptance/mvp-4-skill-review.md)); `scripts/research.py` and feedback import pass their tests. Live venue reading, fresh-session behavior, Windows, and Codex are unverified |
| 5 | Evidence-based writing, audit, and major revision | Accepted by review on 2026-10-29: five skills passed written review ([skill review](acceptance/mvp-5-skill-review.md)); the convention check, check records, revisions, and Pandoc adoption of Word, LaTeX, and OpenDocument pass their tests. Real manuscripts, PDF adoption, Windows, and Codex are unverified |
| 6 | Template-driven layout and readiness | Accepted by review on 2026-10-29: both skills passed written review ([skill review](acceptance/mvp-6-skill-review.md)); the Word route was built, rendered by Word, and inspected with a neutral and a synthetic journal profile on macOS. A real journal template, other PDF routes, Windows, and Codex are unverified |
| 7 | Practical Git control and explicit backup | Accepted by review on 2026-10-28: seven skills passed written review ([skill review](acceptance/mvp-7-skill-review.md)); `scripts/versions.py` passes 13 tests in disposable repositories. No hosting service, Windows, or Codex was exercised |
| 8 | Review rounds and coauthor reconciliation | Accepted by review on 2026-10-29 ([skill review](acceptance/mvp-8-skill-review.md)); `scripts/review.py` passes 5 tests with synthetic material. No real round or coauthor file was used |
| 9 | Connected paper hands-on and release candidate | Accepted under the MVP 2-style gate on 2026-10-29; [written review](acceptance/mvp-9-skill-review.md) and scripted integration evidence are recorded. The optional [complete-path live exercise](acceptance/mvp-9-complete-path.md) is partial and not a pass; its limitations remain. |

Execution order (revised 2026-10-26): 1 → 7 → 2 → 3 → 4 → 5 → 6 → 8 → 9, with the export trial running alongside MVP 7; see the [MVP implementation guideline](mvp-implementation-guideline.md#3-mvp-overview-and-dependencies). The export trial ran on 2026-10-28 ([record](export-trial.md)).

All 33 skills are implemented and passed their written reviews; MVPs 1–9 are accepted under the MVP 2-style gate confirmed by the maintainer on 2026-10-29. On 2026-10-29 the maintainer confirmed this wording in the session (reply: “是，我确认过”), covering MVPs 1–9, their status updates, and the retained complete-path records and findings. This replaces the prior requirement that MVP 9 acceptance await the stricter complete-path live test. Acceptance is distinct from verification: untested platform, service, real-manuscript and researcher-experience claims remain unverified. Earlier run statuses below describe the evidence at the time, not the current acceptance gate.

## MVP 1, partial increment: workspace scaffold

Status: in progress. This increment is narrower than MVP 1 and does not meet its acceptance evidence.

Request: the template maintainer asked to initialize the Git repository, implement the basic project structure described by the design documents, write project documents in English, and delete the Chinese translations (2026-10-26).

Implemented:

- A local Git repository on branch `main`, with no remote.
- `.gitignore` by role, following [design plan Section 13](design-plan.md#13-version-control-and-ignore-policy): credentials (`.env*` except `.env.example`), `.local/`, environments, caches, `.tmp/`, the temporary files that scripts leave behind when they stop midway, rebuildable previews, the parser's own output for imported documents (`references/extracted/*/native/`, except its README), Claude Code personal settings, and editor, office, and operating-system artifacts. Documents, templates, and images are not ignored by type. `.gitattributes` normalizes text line endings.
- Every static directory of the [design plan Section 4](design-plan.md#4-proposed-directory-structure) tree, each with a directory-specific English README. Instance directories (`<source-id>/`, `<profile-id>/`, `<venue-id>/`, and so on) are left for the skills that create them.
- Empty-state records that agents can read in a fresh session: `requirements/project.md`, `requirements/writing.md`, `requirements/privacy.md`, `state/current.md`, `references/index.md`, `ideas/index.md`, `research/decisions/index.md`, `manuscript/outline.md`, and `manuscript/manifest.yaml` (no sections).
- A draft `AGENTS.md` following design plan Section 8, and a `CLAUDE.md` that imports it. The draft was adopted later the same day; see the next section.
- `scripts/check_readmes.py`, a standard-library check of the README contract.
- The Chinese translations of the README, design plan, hands-on design, MVP guideline, and workflow review were removed; the maintainer confirmed that they matched the English documents one to one. Links to them were removed or updated.

Deliberately not created yet:

- `code/`: created by `research-code-setup` only when the research needs code (MVP 4).
- `references/bibliography.bib`: the canonical citation-metadata representation is decided in MVP 2; BibTeX is the current proposal.
- Skill packages and their Claude Code mirrors, and the mirror generation and validation step: these arrive with the first implemented skills.
- `.env.example`: credential variable names depend on the verified MinerU route (MVP 2).

Verification observed (macOS, Apple Silicon, Python 3.12.9 and 3.9.6):

- `check_readmes.py` passes on the scaffold (27 project directories).
- On a disposable copy, it ignores intake material in `inbox/`, preview output, `.venv/`, and folders inside an archived original; accepts a README with a byte order mark and non-ASCII text; and reports a missing README, a lowercase `readme.md`, a too-short README, a placeholder marker, and two identical READMEs.
- All relative Markdown links and heading anchors in the repository resolve.

Not verified:

- Loading of `AGENTS.md` and `CLAUDE.md` in fresh Codex and Claude Code sessions.
- Any behavior on Windows, including the README check.

## MVP 1, partial increment: AGENTS.md adoption

Status: the contract text is adopted; its loading in fresh agent sessions has not been observed yet.

The template maintainer reviewed the draft one decision at a time and adopted `AGENTS.md` on 2026-10-26. Decisions:

- Workspace scope: one main manuscript per workspace, including its submission rounds and revisions. Each additional paper uses its own copy of the workspace.
- Research records: `research/feedback/` holds advice and `research/decisions/` holds confirmed choices with their reasons, from the first session. Record formats are refined in MVP 4.
- Record language: records the researcher reads and confirms use the interaction language; agent-facing files and technical metadata stay in English. Agent guidance moved from the requirement files into `requirements/README.md`, so the records themselves can be written entirely in the researcher's language.
- Skill adapters: skills are written once in `.agents/skills/`; `.claude/skills/` holds generated, committed copies with a consistency check. Both arrive with the first skill.
- Adopted with the text: the one-line `CLAUDE.md` import, the rule that no skill can waive the confirmation rules, role identification by the subject of the request, and the ignored local paths `.tools/`, `.cache/`, `.tmp/`, and `.local/`.

Documentation checked on 2026-10-26 (sources linked in [design plan Section 8](design-plan.md#8-agentsmd-and-tool-compatibility)):

- Claude Code reads project skills only from `.claude/skills/`. Version 2.1.277 or later reads `AGENTS.md` directly only when no `CLAUDE.md` exists, and an `@AGENTS.md` import never loads it twice.
- Codex reads repository skills only from `.agents/skills/` and requires `name` and `description`. It reads `AGENTS.md` from the repository root down to the working directory, up to 32 KiB by default, and ignores `CLAUDE.md`.
- Both follow symlinked skill folders, but symlinks fail in Windows clones without symlink support.

Copied workspaces (decided 2026-10-26): onboarding never deletes, moves, or overwrites a workspace that already holds work. It asks whether to continue that paper; a new paper starts from a fresh copy of the template, and the reference library can be imported into it later.

## Execution order review (2026-10-26)

The maintainer reviewed the MVP dependencies and confirmed four changes to the [MVP implementation guideline](mvp-implementation-guideline.md):

- MVP 7 (Git) moves to immediately after MVP 1, before MVP 2.
- An export trial, which is not an MVP, runs alongside MVP 7. It decides the publishing engine and the citation and cross-reference syntax before MVP 2 fixes the metadata representation and before MVP 5 fixes the writing conventions.
- `journal-selection` moves from MVP 6 to MVP 4.
- MVP 1 verifies the credential mechanism with a test consumer; MVP 2 verifies the live MinerU credential and the selected service's data-use policy. Read-only MinerU service research starts during MVP 1.

## MVP 1, partial increment: skill copies and project-onboarding

Status: implemented, not verified.

Implemented (2026-10-26):

- `scripts/sync_skills.py` validates each canonical package (directory name, README, and one-line `name` and `description` frontmatter that YAML can read) and regenerates its Claude Code copy with a generated README. `--check` reports differences without writing. It removes only copies that it generated itself. `scripts/check_readmes.py` now leaves the contents of generated copies to this script.
- `.agents/skills/project-onboarding/` and its generated copy in `.claude/skills/`. The skill inspects the workspace before it asks anything; confirms the interaction language, research goal, manuscript language, and processing choice one question at a time; records each confirmed answer in the interaction language; offers the AI application privacy check; and ends with one next action. It hands off to `environment-management`, `privacy-configuration`, and `constraint-maintenance`, which do not exist yet.

Verification observed (macOS, Python 3.12.9):

- On a disposable copy, `sync_skills.py` created, updated, and removed generated copies correctly. It reported a hand-edited copy, an extra file, invalid frontmatter (an unquoted `: `, a wrong name, a missing description, a missing README, and an invalid directory name), and a directory that it did not generate, which it kept. It accepted a generated README with CRLF line endings.
- On the repository, the copies match and the README check passes (29 project directories).

Not verified:

- The skill's behavior in a conversation. A fresh headless Claude Code session could not run because the local Claude Code CLI (2.1.170) is not logged in, and the Codex CLI is not installed. That CLI version predates direct `AGENTS.md` reading (2.1.277), so on this machine `AGENTS.md` reaches Claude Code only through the `CLAUDE.md` import.

## MVP 1, partial increment: environment-management

Status: implemented, not verified.

Decision (2026-10-26): researchers enter credentials on a one-time local browser page, which the maintainer chose over native system dialogs and a terminal prompt.

Implemented (2026-10-26):

- `scripts/inspect_environment.py`: a read-only report of the operating system, native and Python process architecture (including x64 emulation on ARM64 Windows and Rosetta on macOS), memory, free storage, Python interpreters (including the Windows launcher and the Microsoft Store alias), optional tools, workspace path risks (spaces, non-ASCII characters, long Windows paths, cloud-synced folders), and project-local setup.
- `scripts/credentials.py`: `set` serves a one-time page on 127.0.0.1 at a secret path, checks the Host and Origin headers, and writes the value to `.env.local` (mode 600 on macOS and Linux) through an atomic replacement. It refuses before asking when Git does not ignore `.env.local` or already tracks it, and it never prints a value. `status`, `remove`, `run` (passes values to another process), and `load_env_local()` complete the loading path. Researcher-facing page texts are arguments, so they can be in the researcher's language.
- `.agents/skills/environment-management/` and its generated copy: inspection, comparison with the task, consented installation or repair, `.venv/` and `.tools/` rules, private credential entry, verification, and common problems.
- `scripts/tests/`: 13 standard-library tests for the credential script, the README check, the skill copy script, and the environment report.

Verification observed (macOS, Apple Silicon):

- All 13 tests pass on Python 3.12.9 and 3.9.6. The tests found that the skill copy script removed an empty directory it had not generated; the cleanup is now limited to its own copies.
- The environment report ran correctly on this computer.
- In the desktop app's built-in browser, with page texts in Chinese and a synthetic test value: the page rendered and the value was saved in `.env.local` (mode 600) without appearing in any output, `status` showed only its length, and `run` passed the exact value to a child process. This test found that a real browser sends `Origin: null` under `Referrer-Policy: no-referrer`, so the first submission was rejected and nothing was saved. The page now uses `same-origin`, and a regression test covers it.
- This desktop session listed `project-onboarding` among its available skills after the copy was committed, which shows that Claude Code discovers skills from `.claude/skills/` and reads their frontmatter. It was not a fresh session.

Not verified:

- The Windows code paths (architecture detection through `IsWow64Process2`, memory, the Python launcher), which have not run on Windows.
- A live service credential, which arrives with the MinerU integration in MVP 2.
- The skill's behavior in a conversation, in fresh Claude Code and Codex sessions.

## MVP 1, partial increment: privacy-configuration

Status: implemented, not verified.

Implemented (2026-10-26):

- `.agents/skills/privacy-configuration/` and its generated copy. The skill identifies the application, sign-in, account type, and document-processing route; reads the current official sources; explains each training control separately from retention, telemetry, and feedback; changes a setting only with explicit consent and records how to reverse it; classifies each control as observed, confirmed by the researcher, provider default only, unknown, or needing an administrator; and writes a redacted local report.
- `sources.md`: a dated register of official sources for Claude (consumer and commercial routes, Claude Code telemetry and feedback) and OpenAI (ChatGPT and Codex on personal and managed plans, and the API), checked on 2026-10-26.
- `report-template.md`: the layout of the local report in `.local/privacy-report.md`, which holds no account identifiers, credentials, screenshots, or research content.

Verification observed:

- The official pages listed in `sources.md` were read on 2026-10-26. The OpenAI Help Center refuses automated fetching and was read in the desktop app's built-in browser. It showed that on personal ChatGPT plans the training setting also covers Codex tasks, and that Codex has a separate "Include environments" setting.
- The skill copies match, and the README and link checks pass.

Not verified:

- The skill's behavior in a conversation, including reading an account setting in a signed-in browser. No researcher or maintainer account settings were read or changed.
- The MinerU cloud service's data-use terms, which arrive with MVP 2.

## MVP 1, partial increment: constraint-maintenance

Status: implemented, not verified.

Decision (2026-10-26): `requirements/` keeps only active rules. A replaced rule is removed; a consequential replacement also gets a research decision record, and minor changes rely on version history.

Implemented (2026-10-26):

- `.agents/skills/constraint-maintenance/` and its generated copy. The skill tells lasting rules apart from one-time edits, advice from other people, and inferences; places each rule in the right file with a scope; checks for duplicates and conflicts before it writes; records rules in a fixed layout in the interaction language; removes replaced rules and writes a decision record for a consequential change; and never saves an inferred preference, including in the agent application's own memory feature.
- `requirements/README.md` now explains that only active rules stay in `requirements/`.

Verification observed:

- The skill copies match, and the README and link checks pass.

Not verified:

- Behavior in conversations, including the MVP 1 persistence tests: a fresh session follows an explicit saved rule, and an unconfirmed inference is absent from every memory location.

## MVP 1 acceptance run 1: Claude Code (2026-10-26)

Status: run 1 is complete for Claude Code on macOS. MVP 1 is not verified: four checklist rows failed on minor points, nine defects were open, and Codex and Windows have not been run. Run 2, below, fixed four of the nine defects.

Method. The template-repository agent acted as the researcher in headless Claude Code sessions on a disposable clone of commit `51f93e7` (no Git remote), with the scripted answers of the [MVP 1 checklist](acceptance/mvp-1.md). Environment: Claude Code 2.1.170, model `claude-sonnet-5-5`, macOS 26.6.2 on Apple Silicon (16 GB), Python 3.12.9. The run used 37 session logs and 189 agent turns, about nine minutes of agent time, and about $4.23 in API-equivalent cost. The logs were kept in the maintainer's scratchpad, not in the repository. The scratchpad was cleared on 2026-10-27; see run 4 for the evidence that remains.

Results: 14 rows pass (A1, B2, C1, D3, D4, E1, E2, E3, E4, E5, E6, F1, F2, H1), 4 fail on minor points (B1, D1, D2, G1), and 2 were not run (G2 and the Windows baseline). E4, F1, and F2 passed after their scripts were corrected; the checklist holds the corrected scripts.

What the run showed:

- The agent found `AGENTS.md` through the `CLAUDE.md` import and discovered all four skills.
- Onboarding resumed from the files after an interruption and never asked again for a recorded answer. It recorded the goal in the researcher's words and invented no research question. A workspace that already held work stayed unchanged.
- The privacy check separated training use from retention, telemetry, and feedback, labeled the controls that nobody read as unknown, and wrote a report without identifiers.
- The private credential page saved a fake value that appeared in no log, command, session transcript, or workspace file, and the removal worked. A key pasted into the conversation was neither repeated nor stored.
- An explicit rule was recorded with its scope and date. A one-time edit and an inferred habit were not recorded, and the application's memory folder stayed empty for the whole run. The rule persisted into a fresh session.
- A conflicting statement produced a question, and a conflicting one-time request left the rule unchanged.
- A consideration changed no file. An explicit confirmation produced a decision record and an index entry.

Test limits:

- The sessions loaded only project and local settings, so the maintainer's user-level settings and skills were absent. The maintainer's `~/.claude/CLAUDE.md` still loaded.
- Permission mode `acceptEdits` with an allow-list. Some compound shell commands were refused, and the agent adapted. The interactive question tool was disabled, so every question was plain text. Web tools were allowed in C1 only. A no-op browser kept pages from opening on screen.
- A plain headless run ends the session when the agent ends its turn, which also ends its background tasks. The first two D3 attempts therefore lost the page server. D3 passed in a session that stays open, where the completion of the page task woke the agent, as in an interactive session.
- Not exercised: Codex, Windows, the interactive question tool, the simulation of missing Python or tools, an account control that the researcher can read, the ASD-STE100 checks, onboarding in English (G2), and a live service credential.

Defects. Changing a skill or `AGENTS.md` needs the maintainer's decision; the fixes for D-1, D-3, D-6, D-8, D-10, D-11, and D-12 were made on the maintainer's instruction of 2026-10-26, and runs 2 and 3 tested them.

| ID | Severity | Status | Observed | Fix or proposed fix |
| --- | --- | --- | --- | --- |
| D-1 | Medium | Fixed in runs 2 and 3 | Records that the researcher reads were written in English: `state/current.md` after onboarding, and the first decision record. The adopted decision says these records use the interaction language. | Applied: the last step of `project-onboarding` and the decision-record step of `constraint-maintenance` say "in the interaction language". Runs 2 and 3: every record and both decision records were in Chinese. The interim narration is a separate defect (D-12). |
| D-2 | Low | Partly fixed (run 5) | The readiness report did not say that reading and writing work without the converter, and its closing message bundled two questions. In runs 2 and 3, two of four samples skipped the inspection script. | Applied to `environment-management`, Rules: run the inspection before saying whether the computer is ready, say what still works without the missing tool, and ask at most one question. Run 5, two samples: both ran the inspection and asked one question; one said that reading and writing Markdown needs no tool, the other only implied it. |
| D-3 | Medium | Fixed in run 5 (three D2 samples) | The agent treated PDF import as available once MinerU is installed, and implied that a key would soon be entered for parsing. No ingestion skill exists yet. | Applied in `AGENTS.md`, "Skills" (run 2); in `environment-management`, step 5 (run 4); and, for the routing gap, in `privacy-configuration`, Rules (run 5). Run 5, three D2 samples: each checked the skills and scripts for MinerU, said that cloud parsing is not available yet and that no key is needed now, and looked up no key page. |
| D-4 | Low | Fixed in run 5 (one sample) | The final onboarding report named `inbox/imports/` as the place for documents. That folder holds import records; documents go in `inbox/`. | Applied to `project-onboarding`, step 8: name `inbox/` as the place for documents. Run 5: the final report named `inbox/`. |
| D-5 | Low | Fixed in run 5 (one sample) | `project-onboarding` detected an interrupted onboarding from `state/current.md` only, which it updates at the end. | Applied to `project-onboarding`, step 1: `requirements/project.md` counts as a sign too. Run 5: the fresh session resumed from `requirements/project.md` and asked only the open question. |
| D-6 | Medium | Fixed in run 2 | When recording the British-spelling rule, the agent added an exception (quotations, proper names, and bibliography titles keep their spelling) that the researcher had not stated. | Applied: `constraint-maintenance` adds an example or an exception only when the researcher gave or confirmed it. Run 2, two samples: none recorded; one run asked whether the researcher wanted an exception. |
| D-7 | Low | Fixed in run 5 (one sample each form) | "改用美式拼写" (switch to American spelling) replaced the old rule without a question. That follows `AGENTS.md` but not step 3 of the skill. | Applied to `constraint-maintenance`, step 3: when the researcher's words say to replace or switch to the new rule, record it as a replacement without a question; the ambiguous form still asks. Run 5: the explicit form replaced the rule without a question; the ambiguous form asked one question and changed no file. |
| D-8 | Medium | Fixed in run 2 | After a confirmed change of the research goal, the agent rewrote the manuscript introduction, both times unasked. | Applied: a new step in `constraint-maintenance` lists the manuscript passages that the change affects and asks before editing them. Run 2, two samples: the introduction stayed unchanged until the answer, and both answers worked. |
| D-9 | Low | Fixed in run 5 (one sample) | In E6 the reply rewrote the sentence before it asked whether the request was a one-time exception. | Applied to `constraint-maintenance`, step 3: a request that names one sentence is a one-time edit; the agent makes it, says that no rule changed, and offers to change the rule. Run 5: the rewrite was made and the reply said so. |
| D-10 | Low | Fixed in run 3 | Onboarding recorded the declined privacy check in `requirements/privacy.md` as a confirmed item, with the added sentence "do not check or change any account setting without the researcher's consent". The researcher had said only "not now" to the offer. | Applied: `project-onboarding` notes a declined or postponed offer only in `state/current.md`, and does not write it to `requirements/privacy.md`. Run 3, two samples: `privacy.md` stayed unchanged and the deferral is only in `state/current.md`; one sample gave the reason. |
| D-11 | Low | Fixed in runs 3 and 4; one residual in run 5 (see D-14) | Replies to the researcher named internal terms: "MVP 2", the skill id `source-ingestion`, and "想法发展技能" (the idea-development skill). | Applied: `AGENTS.md`, "Skills", asks the agent to describe a missing capability in the researcher's own terms and not to use MVP numbers or skill ids unless asked. Run 3: none of 36 messages used them. Run 4: none of 24 text blocks. Run 5: none of 44 text blocks except one first note before a skill call (D-14). |
| D-12 | Low | Fixed in runs 4 and 5 (few samples); one residual (see D-14) | The sentence before the first tool call of several turns was in English, although the researcher wrote Chinese. | Applied to `AGENTS.md`, "Language and formats", and to the rules of all four skills. Run 3: 2 of 16 English-only notes (12%). Run 4: 0 of 17. Run 5: 1 of 22, the first note before a skill call (D-14). |
| D-13 | Low | Fixed in run 5 (three D2 samples) | When the researcher states a wish to use cloud parsing, the agent records the choice in `requirements/privacy.md` before the scope of documents is known: in 2 of 3 samples in run 4 and 2 of 3 in run 3. | Decided 2026-10-27: a wish is not a confirmed choice. `privacy-configuration`, step 6: a cloud choice is recorded only after the researcher answers a scope question; until then the wish stays open in `state/current.md`. Run 5: no sample wrote `privacy.md`, and each kept the wish open. |
| D-14 | Low | New in run 5; open | The first note of a session, written before a skill call, was English and named a skill id (`constraint-maintenance`). The skill's rules are not loaded yet at that point; only `AGENTS.md` applies. Run 5: 1 of 22 notes. | Proposed: in `AGENTS.md`, "Language and formats" and "Skills", say that the short notes before a skill call follow the same rule, and never name a skill id in them. |

## MVP 1 acceptance run 2: Claude Code (2026-10-26)

Status: the fixes for D-1, D-3, D-6, and D-8 worked in every sample that run 2 took. B1 and D2 moved from Fail to Pass, and the regression rows still pass. MVP 1 is not verified: D1 and G1 still failed on minor points, eight defects were open (D-2, D-4, D-5, D-7, D-9, D-10, D-11, and D-12), and Codex and Windows have not been run.

Correction from run 3: the D2 pass and the verdict "fixed" for D-3 did not hold up under more samples. D2 does not pass, and D-3 is fixed only for direct questions about importing. See the run 3 section.

Fixes applied on the maintainer's instruction of 2026-10-26:

- `AGENTS.md`, "Skills": a paragraph says that only the skills in `.agents/skills/` exist, and that the agent must say so plainly when a task needs a missing skill, such as importing and converting documents. It adds that the agent can still help in conversation, so that the rule does not turn into a refusal (D-3).
- `project-onboarding`: the last step writes `state/current.md` and the report in the interaction language (D-1). The step also stops listing "importing documents" and similar examples as next actions, because they name capabilities that do not exist yet; the next action must be one that the agent can carry out now. That second change goes beyond the proposal, and D-3 needed it.
- `constraint-maintenance`: examples and exceptions only when the researcher gave or confirmed them (D-6); decision records and their index entries in the interaction language, with the reason as the researcher gave it (D-1); a new step that lists the manuscript passages that a change affects and asks before editing them (D-8); matching completion checks and README text.

Method. The same as run 1, on a new disposable copy, `/Users/wota/Projects/paper-template-mvp1-test-claude-r2`. It was cloned from the template, with `docs/` restored to its state at `51f93e7` (no checklist and no defect table) and the fixed `AGENTS.md` and skills laid over it, so that the agent under test saw the run 1 environment plus the four fixes. The run used 30 session logs and 156 agent turns, about 6.5 minutes of agent time, and about $3.21 in API-equivalent cost. Most scenarios were sampled once. A single sample cannot show that a fix always works, so E1, F1, and D1 were sampled twice, and F1 was answered both ways.

| Defect | Evidence in run 2 | Verdict |
| --- | --- | --- |
| D-1 | B1: `state/current.md` and the other records were in Chinese. F1: both decision records and their index entries were in Chinese (in run 1, one of two was in English). | Fixed for records. |
| D-3 | D1 (two samples), D2, and the B1 report said that no import or parsing skill exists and promised nothing, while they still offered to discuss in conversation. E2 still wrote the introduction without a writing skill. | Fixed for direct questions; the D2 pass did not repeat (run 3). |
| D-6 | E1 (two samples): no example or exception was recorded. One run asked whether the researcher wanted a quotation exception. | Fixed. |
| D-8 | F1 confirmation (two samples): the introduction stayed unchanged until the researcher answered, and the agent listed the affected passage and recommended an edit. "Later" left it unchanged and recorded the deferral. "Now" rewrote it in British spelling, with no unsupported claim. | Fixed. |

Regression. A1, B2, E3, E4 (mirrored wording), E5, and E6 behaved as in run 1. H1 passes on the run 2 copy, and the application's memory folder stayed empty.

Not re-run: C1, D3, D4, F2, G1 as a whole, G2, Codex, and Windows. Their instructions did not change, but `AGENTS.md` did, so a full run must follow the next fixes.

Test limits are those of run 1. In addition, the samples are few, and the model varies between samples, as D1 showed.

## MVP 1 acceptance run 3: Claude Code (2026-10-26)

Status: D-10 and D-11 are fixed in the samples taken. D-12 is applied but not shown to work. Run 3 also showed that the earlier fix for D-3 is not reliable, and it corrected the D2 result of run 2. MVP 1 is not verified: by each row's latest result, 15 rows pass, 3 fail on minor points (D1, D2, G1), and 2 were not run. Codex and Windows have not been run.

Fixes applied on the maintainer's instruction of 2026-10-26:

- `project-onboarding` (D-10): a declined or postponed offer is not a requirement. The agent notes it as deferred, in the researcher's words, only in `state/current.md`, and does not write it to `requirements/privacy.md` or add a rule that the researcher did not state. The completion check says so too.
- `AGENTS.md`, "Skills" (D-11): the agent describes a missing capability in the researcher's own terms, for example "importing documents is not available yet", and does not use MVP numbers or skill ids unless the researcher asks for them.
- `AGENTS.md`, "Language and formats" (D-12): the language rule covers every message that the researcher sees, including the short notes between tool calls.

Method. The same as run 2, on a third disposable copy, `/Users/wota/Projects/paper-template-mvp1-test-claude-r3`, which holds the run 1 environment plus all fixes so far. Run 3 re-ran B1 (two samples), D1 (two), and D2 (three): 20 session logs, 118 agent turns, about five minutes of agent time, and about $2.44 in API-equivalent cost. To tell whether the new D-11 wording had weakened D-3, D2 was also sampled three more times on the run 2 copy, which has the older `AGENTS.md` (3 logs, about $0.64).

| Defect | Evidence | Verdict |
| --- | --- | --- |
| D-10 | B1, two samples: `requirements/privacy.md` stayed unchanged, and the declined check appears only in `state/current.md`, under "deferred". One sample said why: a postponement is not a requirement. In run 2, the same step wrote it to `privacy.md` as a confirmed item. | Fixed in the samples taken. |
| D-11 | In B1, D1, and D2, none of 36 messages to the researcher used MVP numbers or skill ids (3 of 49 before the fix). Both D1 samples said in plain words that importing is not available yet. | Fixed in the samples taken; the samples are few. |
| D-12 | English-only notes between tool calls: 2 of 16 (12%), against 4 of 25 (16%) before. Both remaining ones are the first note of a session, written right after the agent loaded an English skill. | Applied, not shown to work. |
| D-3 | Asked directly about importing PDFs (D1), the agent said that no import skill exists in 4 of 4 samples (runs 2 and 3). Talking about cloud parsing and keys (D2), it said so in 1 of 7 samples (run 2: 1 of 4; run 3: 0 of 3). The older `AGENTS.md` did no better on D2 (1 of 4), so the new wording did not cause the misses. The other samples treated parsing as working once a key exists. | Partly fixed. |

Corrections to run 2: the D2 pass was the first sample of four, so D2 does not pass, and "D-3 fixed" held only for direct questions about importing.

Other observations: in two of three D2 samples the agent recorded the wish for cloud parsing at once, because an explicit statement counts as confirmation under `AGENTS.md`; the record lists the conditions before any upload (terms, document scope, key). One D2 sample took the scripted answer "可以，就这样记录" as consent to browse the web, which the test setup did not allow.

Test limits are those of run 2. The samples are few, and the counts for D-11 and D-12 are counts of messages, not measures of the researcher's experience.

## MVP 1 acceptance run 4: Claude Code (2026-10-27)

Status: the two additions for D-3 and D-12 are committed as bed8899. D-11 and D-12 show no failure in the samples taken. D-3 is partly fixed: two of three D2 samples behaved as the rule says, and the third never reached the rule, because the skill that handles a cloud choice does not carry it. MVP 1 is not verified. By each row's latest result, 15 rows pass, 3 fail on minor points (D1, D2, and G1), and 2 were not run. Codex and Windows have not been run.

Method. The fourth disposable copy, `/Users/wota/Projects/paper-template-mvp1-test-claude-r4`, was cloned from the template with `docs/` restored to its state at `51f93e7` and the current skills and `AGENTS.md` laid over it, as in run 3. The test subject stayed `claude-sonnet-5-5`, as in runs 1 to 3; the `/model` change to Haiku 5.5 applies only to the orchestrating session. The first B1 session reached the account's session limit during its fresh-session step; that step was repeated on 2026-10-27 in a new session. Samples: B1 once (its first three turns ran in the first session, the rest in the new one); D2 three times from the same state after B1, restored from a snapshot before each sample (A with the scripted confirmation, B and C with the first message only); E1 once. The harness was rebuilt on 2026-10-27 with the same tool allow-list and settings.

Results.

- B1 (Pass). After the interruption the continuation asked only the open question (manuscript language), recorded each answer in Chinese, and then asked the processing choice and the AI privacy check. The declined check is only in `state/current.md`. `requirements/privacy.md` holds "以后再定" as a deferred processing choice, which the skill lists as a choice to record.
- D2 (Fail, minor). A and B searched the skills and scripts for MinerU, looked up no key page, collected no value, said that no import skill exists and that no key is needed now, and recorded the credential as deferred in `state/current.md`. C loaded `privacy-configuration` but not `environment-management`, ran no check, and said that the key is needed at the first upload, which implies that parsing exists. No sample tried a web search or a key lookup. On the cloud scope: A asked which documents the route covers before its record was complete; B and C recorded the wish first (D-13).
- E1 (Pass). The rule was recorded with its scope, no example or exception was added, and the notes were in Chinese.
- H1 (Pass). The README and skill-copy checks pass on the run 4 copy; its memory folder is empty; no MVP number or skill id appears in its text.

Defect verdicts.

- D-12: 0 English-only notes of 17 across all run 4 sessions. Run 3 had 2 of 16. The sample is small.
- D-11: no MVP number or skill id in any of the 24 text blocks of the run 4 sessions.
- D-3: partly fixed. The rule lives in `environment-management`, but a cloud choice is routed through `privacy-configuration` (sample C). The same check there would close the gap; that is a decision for the maintainer.

Evidence. The scratchpad was cleared on 2026-10-27. The stream logs of runs 1 to 3, and of the first three B1 turns of run 4, are gone from it. The numbers recorded for those runs were taken from the logs at the time and stay as recorded. Claude Code keeps a session transcript for each test copy under `~/.claude/projects/` (run 4 has 7 files, including the first B1 session), and the run 4 counts for D-11 and D-12 were checked against them. The surviving run 4 logs cost about $1.2 in API-equivalent terms, not counting the first three B1 turns.

## MVP 1 acceptance run 5: Claude Code (2026-10-27)

Status: the decisions for the open items after run 4 are applied and tested. D-3 (routing) and D-13 pass in all three D2 samples; D-4, D-5, D-7, and D-9 pass in one sample each; D-2 is partly fixed. One new residual, D-14, shows up in the first note of a session before a skill call. The skill changes are committed as 83f1839. MVP 1 is not verified. By each row's latest result, 16 rows pass, 2 fail on minor points (D1 and G1), and 2 were not run. Codex and Windows have not been run.

Decisions, made on the maintainer's instruction "do what you think is best" (2026-10-27):

- D-3 routing: `privacy-configuration` gets the same check as `environment-management`, step 5. A cloud service is available only through a skill or script that calls it. Without one, say so plainly, defer the setup, and do not look up a key page or promise a key for the first upload.
- D-13: a wish to use cloud parsing is not a confirmed choice. It stays open in `state/current.md`, and `requirements/privacy.md` is written only after the researcher answers a scope question with the agent's recommendation. This was chosen over recording the wish with its scope marked as unconfirmed, because a processing choice is a major decision that needs explicit confirmation under `AGENTS.md`.
- D-2: `environment-management` runs the inspection before it reports readiness, names what still works without the missing tool, and asks at most one question.
- D-4 and D-5: `project-onboarding` names `inbox/` as the drop folder in its final report, and detects an interrupted onboarding from `requirements/project.md` as well as from `state/current.md`.
- D-7 and D-9: `constraint-maintenance`, step 3. A request that says to replace or switch the rule is a replacement, recorded without a question. A request that names one sentence is a one-time edit: it is made at once, the reply says that no rule changed, and the agent offers to change the rule.

Results.

- B1 (Pass). One sample across a fresh-session continuation. The continuation resumed from `requirements/project.md` (D-5), the final report named `inbox/` (D-4), and every note was in Chinese.
- D2 (Pass). Three samples, each with the same two messages. Each checked the skills and scripts for MinerU, said that cloud parsing is not available yet and that no key is needed now, looked up no key page, kept the wish open in `state/current.md`, and left `requirements/privacy.md` unchanged after both messages (D-3 routing, D-13).
- D1 (Fail, minor). Two samples. Both ran the inspection (D-2) and asked one question. One said that reading and writing Markdown needs no tool; the other only implied it.
- E1 (Pass). Two sessions, with the scope and the source recorded and no example or exception added. One session's first note, before its skill call, was English and named the skill id (D-14).
- E4 (Pass, revised expectation). The explicit form ("这篇论文改用美式拼写") replaced the rule without a question, and the replaced rule was named. The ambiguous form ("这篇论文用美式拼写") asked one question with options and a recommendation, and changed no file until the answer.
- E6 (Pass, revised expectation). A one-sentence request ("这一句请用英式拼写重写") was rewritten at once. The reply said that the saved rule had not changed and offered to change the rule. `requirements/writing.md` held only the American rule afterwards.
- H1 (Pass). The README and skill-copy checks pass on the run 5 copy, and its memory folder is empty.

The expectations of E4 and E6 in the checklist were revised to match the decisions for D-7 and D-9, so the checklist now shows both forms of E4. Their run 1 results are unchanged.

Defect verdicts.

- D-2: partly fixed. The inspection ran in 2 of 2 samples (run 3: 2 of 4 skipped it). "Writing continues" was said in 1 of 2.
- D-3 and D-13: fixed in the samples taken (three D2 samples each).
- D-4, D-5, D-7, and D-9: fixed in one sample each. The samples are small.
- D-11 and D-12: fixed in the samples taken, with one residual (D-14).
- D-14 (new, open): the first note of a session can be English and can name a skill id before any skill's rules are loaded; only `AGENTS.md` applies at that point. Run 5: one English note in 22 across all run 5 sessions, and that note also named the skill id. Proposed: say in `AGENTS.md` that the short notes before a skill call follow the same rule, and never name a skill id in them.

Evidence and cost. The run 5 copy was built from the working tree on 2026-10-27, before commit 83f1839, which holds the same skill content. The harness was the one rebuilt for run 4, and the subject model stayed `claude-sonnet-5-5`. The 22 sessions cost about $2.1 in API-equivalent terms.

## MVP 1 acceptance runs 6 and 7: Claude Code (2026-10-27)

Status: run 7 fixed the missing decision record for a confirmed research-goal change (D-15) and a decision-record trigger that was too broad (D-18). Its samples also show two open defects: an availability rule that blocks required questions and offers (D-16), and an offer to rewrite the introduction in every confirmation sample (D-17). MVP 1 is not verified.

Method. Disposable copies without a Git remote, each cloned from commit `3e1e08e`, the run 6 baseline. That commit includes the prototype per-turn reminder (`scripts/turn_reminder.py`, a `UserPromptSubmit` hook), so the copies ran with it. The fixes were laid over the baseline in each copy and were not committed. Subject model `claude-sonnet-5-5`, with the scripted answers of the checklist. Copies: r7 (run 6: E1, E4, E6, D2), r8 (run 6: B1 and F1 on a clean baseline), r9 (run 7: first decision fix), r10 (run 7: scope fix), and r11 (run 7: final wording, with B1 and F1 again, D1 twice, E1, and E4).

Incident. While restoring the F1 baseline of r7, I reset its `requirements/project.md` and `state/current.md` to the template state with `git checkout`. I could not rebuild the pre-F1 state from the saved patch, because the RTK filter rewrote the `git diff` output. Also, r7's `writing.md` showed no rule, although its run logs wrote one, and I could not establish when that happened. The F1 scenario was therefore repeated on r8, built afresh. The r7 results are recorded from the run logs and the notes of the earlier session.

Results.

- B1 (r8, run 6): Fail (minor). Records and `privacy.md` were correct, and no decision record was written, but the final report gave two next actions, inbox and conversation (D-19).
- B1 (r9, run 7): Fail. The language answer was recorded as a decision (D-18); the rest matched r8.
- B1 (r10, run 7): Fail (minor). No decision record. `privacy.md` got a deferral line, and the final report gave two next actions (D-19).
- B1 (r11, run 7): Fail. The document-processing question was skipped, because no document was at hand, which step 5 of `project-onboarding` allows. The scripted answer "以后再定" was then applied to the privacy-check question; the script, not the skill, was wrong (corrected in run 10).
- F1 (r8, run 6): the question turn changed no file and gave a recommendation. The confirmation updated the goal and the state file, left the manuscript unchanged, and wrote no decision record or index entry (D-15).
- F1 (r9, r10, and r11, run 7): decision record and index entry in 3 of 3; manuscript unchanged in 3 of 3; the question turn changed no file in 3 of 3. All three offered to rewrite the introduction as a choice (D-17).
- E1 and E4, explicit forms: r9 Fail, with a decision record for spelling and the rule in `project.md` (D-18). r10 and r11 Pass: the rule is in `writing.md`, a replacement names the rule it replaces, and no decision record is written.
- D1: r10 (one sample) Fail. The skill was not loaded, and no check was run, because the agent treated the check as part of an unavailable capability (D-16). r11 (two samples): both loaded the skill and ran the inspection, which reported the system, processor, and Python. One listed several next steps (minor); the other gave one question.
- H1 (r10 and r11): pass. The README and skill-copy checks pass, the availability table and writing-rule form pass, and the memory folder is empty.

Defects.

- D-15 (Medium; fixed in run 7 in 3 of 3 samples): A confirmed research-goal change got no decision record (0 of 1 samples in run 6). The record duty sat only in a step of `constraint-maintenance` for replacing a rule, and the agent did not load that skill for a goal change. Applied: a standing rule "Decisions" in `AGENTS.md`; the skill's description names the research question or goal; the skill's step now only links the record.
- D-16 (Medium; open): The availability rule removed required questions and checks. In r10, D1 loaded no skill and ran no check, saying that no checks exist for an unavailable capability, although the environment check is available. In r11, the document-processing question was skipped; run 10 showed that step 5 of `project-onboarding` allows this, so it is not a defect. Applied so far: the description of `environment-management` names the readiness question (D1 loaded it in 2 of 2 samples in r11), and the "Capabilities" rule says to answer the part that an available capability covers and to say which part is not available. Still open: "offer it as a choice" is broad enough to suppress decisions the researcher must make, such as the processing mode, which `AGENTS.md` requires to be confirmed.
- D-17 (Low; open): The introduction-rewrite option ("现在按新目标重写") appeared in all four confirmation samples (one in run 6, three in run 7), although the availability table lists manuscript revision as not available yet. The wording "do not offer it as a choice" did not change this. Proposed: the manuscript-text standing rule names the choices that may be offered (keep the passage as an open item, or the researcher edits it) and says that revising manuscript text is not available yet.
- D-18 (Medium; fixed in r10 and r11, 2 of 2 samples): The decision-record rule listed the manuscript language and central terminology as consequential. Spelling therefore got a decision record (r9, E1 and E4), the language answer got one (r9, B1), and the spelling rule went to `project.md`. Applied: consequential choices are research choices only (the research question or goal, a method, corpus or inclusion boundaries, an excluded analysis, the central argument); writing rules, language settings, and wording get no record. `constraint-maintenance`, Step 2, places spelling in `requirements/writing.md` and language settings in `requirements/project.md`.
- D-19 (Low; open): The final onboarding report gave two next actions (r8 and r10). r10 also wrote the postponed processing choice into `requirements/privacy.md` as a status line, although a postponed choice is not a requirement. Proposed: one next action, and postponed choices only in `state/current.md`, as D-10 says.

Changes made in the working tree (committed on 2026-10-28 in `68b92f4`, after run 10 had changed them again): `AGENTS.md` (the "Decisions" standing rule, the "Capabilities" rule, the availability row "Record standing rules and research decisions", and the decision sentence removed from "Confirmed requirements only"); `constraint-maintenance` (description, the decision-record rule, Step 2 on spelling and language settings, Step 5 links the record, and the README wording); and `environment-management` (description). The Claude Code copies are regenerated, and `scripts/sync_skills.py --check` passes.

Decisions for the maintainer.

1. Availability wording (D-16, D-17; approved and applied on 2026-10-27, see runs 8 and 9). Recommended: separate required decisions from offers to perform an unavailable action. A required decision, such as the processing mode, is still asked. The agent offers nothing that it cannot do, and the manuscript-text rule names the permitted choices. Then re-test B1, F1, and D1 on a new copy.
2. Commit the working-tree changes of runs 6 and 7. Done on 2026-10-28 in `68b92f4`, together with the run 10 changes, and the records in a second commit.
3. Adoption of the per-turn reminder hook. It remains a prototype; the test copies include it.

Limits. One or two samples per scenario. The run 6 results of E1, E4, E6, and D2 come from the run logs and the earlier notes. The harness refused some compound Bash commands during D1, and the agent worked around that. The samples are too few to measure a rate.

## MVP 1 acceptance runs 8 and 9: Claude Code (2026-10-27)

Status: the availability wording that the maintainer approved was applied and tested (run 8 with Sonnet, run 9 with Haiku). It made the F1 reply behave as intended. The maintainer then ruled that `AGENTS.md` and `CLAUDE.md` must not be patched to pass a test. Run 9, the first with Haiku, shows record-format errors and a routing miss that Sonnet did not show. MVP 1 is not verified.

Maintainer decisions (2026-10-27).

- The subject model of the acceptance tests is Haiku (`claude-haiku-5-5`). For GPT, the maintainer named "luna"; its exact model ID is not known yet. Runs 1 to 8 used `claude-sonnet-5-5` and stay recorded as Sonnet results.
- `AGENTS.md` and `CLAUDE.md` are not patched with constraints that exist only to resolve failing tests. A failure is traced to the layer that causes it and fixed there.

Method. Copies r12 and r13 (run 8, Sonnet) and r14 and r15 (run 9, Haiku), each cloned from commit `3e1e08e` with the 23 rule files laid over it from the working tree and compared byte by byte. Samples: B1 twice per model, F1 twice per model, D1 twice (Sonnet) and three times (Haiku), E1 once (Sonnet) and twice (Haiku), and H1 on r14. The harness `cc.py` now sets the subject model to `claude-haiku-5-5`.

Results.

- B1: all four samples asked the document-processing question after the manuscript language (the r11 skip did not return), wrote no decision record, and left `requirements/privacy.md` unchanged. Sonnet (r12, r13): Pass with minor findings; the final report gave two next actions (D-19). Haiku: r14 Pass with one minor finding (the pending list kept the goal after it was recorded); r15 Fail (minor), because the goal was recorded as a paraphrase labeled as the researcher's words (D-21), and the report gave two next actions.
- F1: the question turn changed no file in 4 of 4. In the confirmation turn all four wrote the decision record and the index entry, left the manuscript unchanged, listed the affected passage, and asked one question, without offering to rewrite it. Sonnet and Haiku r14 also said that revising manuscript text is not available yet; Haiku r15 did not, and it recorded the new goal as a paraphrase labeled as the researcher's words (D-21).
- E1: Sonnet (r12) wrote a rule that passes the form check. Haiku wrote none that does: r14 has no Scope line, and r15 used the label "范围" (not accepted) and no quotation on the Confirmed line (D-20). No sample wrote a decision record for spelling.
- D1: Sonnet (r12, two samples): the skill was loaded and the inspection ran in both. Haiku (r14, three samples): the skill was loaded and the inspection ran in 1; in 2, the agent said that PDF import is not available, offered to run the check, and ran nothing (D-16).
- H1 (r14): the README, skill-copy, and availability checks pass and the memory folder is empty; the rule-form check fails (D-20).

Skill use and compliance. The question was whether `AGENTS.md` should require the agent to follow skills. The logs from r10 to r15 show:

- The matching skill was loaded in every B1 session start (Sonnet 8 of 8, Haiku 4 of 4) and in every goal change or rule (Sonnet 9 of 9, Haiku 4 of 4). The exception is the readiness question in D1: Sonnet 4 of 5, Haiku 1 of 3.
- After a skill was loaded, the saved rule followed the layout in 3 of 3 Sonnet copies (r10, r11, r12) and in 0 of 2 Haiku copies (r14, r15).
- The agent follows a loaded skill closely, even where the skill is stale. Step 6 of `constraint-maintenance` still asks "update them now, later, or not at all". It was written before the availability table existed, and it is the source of the repeated "rewrite the introduction now" option (D-17). The sentences added to `AGENTS.md` for D-17 overrode that step and hid the defect. A general rule to follow skills would have made the stale step stronger.

The gaps are therefore routing (D1 on Haiku), layouts that only prose enforces (D-20, D-21), and skill text that disagrees with the contract (D-17). None of them is solved by another sentence in `AGENTS.md`.

Defects.

- D-16 (Medium; open): D1 on Haiku loaded the skill and ran the inspection in 1 of 3 samples. Routing depends on the skill description and the table row, and the question names an unavailable capability (importing PDFs). The description of `environment-management` names the readiness question, and Sonnet loaded the skill in 4 of 5 samples since, but Haiku in 1 of 3.
- D-17 (Low; the symptom is suppressed, the cause is open): the cause is Step 6 of `constraint-maintenance`, plus a table row that does not say that rewriting a passage belongs to "revise the manuscript". The `AGENTS.md` sentences that suppress the symptom are patches.
- D-19 (Low; open): the final onboarding report gave two next actions (Sonnet r12 and r13, Haiku r15); Haiku r14 gave one.
- D-20 (Medium; open): Haiku wrote the spelling rule without the Scope line (r14), or with another label and no quotation (r15). `check_requirements.py` catches both, but no procedure runs it, and its message does not list the accepted labels.
- D-21 (Low; open): Haiku recorded a paraphrase as the researcher's words (r15, in B1 and in F1). The rule to quote the words is in `AGENTS.md`; the layout that carries the quotation is prose.

Patch-like sentences that `AGENTS.md` held after run 8, and the layer each one belongs to (applied in run 10):

- "Capabilities": "Answer the part of a request that an available capability covers, using it" (added for D1) belongs to the text of the table rows and the skill descriptions, which route the request.
- "Capabilities": "offer to perform it" and "A decision that the researcher must make is still asked ..." (added for D-16 and D-17) are removed. The original sentence stays, without the word "checks", which the agent read as the computer check.
- "Decisions": the examples and the list of exclusions (added for D-18) move to `research/decisions/README.md`, which already says what counts. `AGENTS.md` keeps one sentence for the duty and its place, because D-15 showed that a duty held only in a skill is not reached.
- "Manuscript text": the named choices and "Do not offer to revise or delete a passage yourself" (added for D-17) are removed. Step 6 of `constraint-maintenance` offers only what the availability table lists, and the table row names rewriting a passage.

Other fixes in the layers that cause the failures (applied in run 10, except the routing test): a rule writer script, or a procedure that runs `check_requirements.py` and a message that lists the accepted labels (D-20, D-21); a routing test that sends the scripted researcher messages and checks which skill loads, so that routing is measured on Haiku and not guessed.

Limits. Two to three samples per scenario and model. The Haiku harness refused several compound Bash commands in D1, which the agent worked around.

## MVP 1 acceptance run 10: Claude Code with Haiku (2026-10-28)

Status: the maintainer approved the restructure on 2026-10-28. The case-specific sentences are out of `AGENTS.md`, and their causes are fixed in the skills, the table data, the decisions README, and the form check. Haiku, now the subject model, passes most samples of B1, F1, E1, and D1, with residual misses for which no sentence should be added to the contract. MVP 1 is not verified.

Maintainer decisions (2026-10-28).

- Move the patch-like sentences out of `AGENTS.md`, fix the causes in skills, table data, and scripts, and re-test with Haiku.
- The GPT-side model for the later Codex run is `gpt-6-luna`. Codex is not installed on this computer, so that run still needs an installation and a sign-in.

Changes (committed on 2026-10-28 in `68b92f4`).

- `AGENTS.md`: "Capabilities" is back to its general sentence, without the word "checks" (in D1 the agent echoed "records, checks, or outputs" when it declined to run the computer check). "Decisions" keeps one sentence for the duty and points to the README of the folder. "Manuscript text" is back to its general sentence. Two table rows are data: the computer check names "whether it is ready for a task", and the manuscript row names "rewriting a passage".
- `research/decisions/README.md` says that a writing rule or a language setting is a requirement, not a decision.
- `constraint-maintenance`: the Confirmed line carries the researcher's exact words in quotation marks; the skill runs `check_requirements.py` after it writes a rule; Step 6 offers only what the availability table lists (today: keep the passage as an open item, or let the researcher revise it); the completion check names the script.
- `project-onboarding`: the goal is quoted exactly; a postponed choice is listed as open in `project.md` and `state/current.md` and is not written to `privacy.md`; the report gives exactly one next action; the finish step sets the status and rewrites `state/current.md` as a whole, with its heading.
- `environment-management`: the description leads with its triggers and names the readiness question.
- `scripts/check_requirements.py`: its message lists the accepted labels. Two tests were added; 27 tests pass.

Corrections to earlier records.

- B1 in r11 (run 7) was recorded as a skipped required question (D-16). It was not a defect. Step 5 of `project-onboarding` says to ask about document processing only when documents are at hand or the researcher wants to settle it, and otherwise to list the choice as open. The scripted answer "以后再定" then fit the wrong question, because the tester gave it without checking which question the agent had asked. The checklist now says to answer the question actually asked.
- The sentence "A decision that the researcher must make is still asked ..." (added to `AGENTS.md` for that case) was therefore unjustified, and it is removed.

Method. Copies r16 and r17 (the first version of the new text), r18a to r18c (the final text, with the state of a finished B1 taken from the r17 output; used for F1 and D1), and r19 and r20 (B1 with the final text), all cloned from `3e1e08e`. The subject model is `claude-haiku-5-5` in every run, which the 70 session logs from run 9 on confirm. The rule files were compared byte by byte with the working tree.

Results (Haiku).

- B1 (r16, r17, r19, r20): Pass in all four. The goal is quoted word for word, the report gives one next action, no decision record is written, `privacy.md` is unchanged, and the postponed processing choice is listed as open. Minor: r19 wrote `project.md` in English (D-22); r16 left the status as in progress, because its scripted answers did not fit the questions asked; the heading of `state/current.md` stayed in English in r16 and r17 and was in Chinese in r19 and r20, after the finish-step change.
- F1: decision record and index entry in 5 of 5, manuscript unchanged in 5 of 5. With the final wording (r18a to c), r18b and r18c loaded the skill, ran the check, said that revising is not available, and offered only to keep the passage as an open item or to let the researcher revise it. r18a loaded no skill and offered to rewrite the introduction. In r17 (first wording), choice 2 was an edit by the agent after the researcher's direction. The confirming words were quoted, with small changes in punctuation in r18b and r18c and a changed word in r18c; r15 (run 9) labeled a paraphrase as the researcher's words.
- E1 and E4: in r16, the agent wrote the label "范围", the check named the accepted labels, and the agent corrected the file; in r17 it read the script first. Both pass the form check, and no decision record was written. E4 (explicit form, r16): replaced without a question, no decision record.
- D1: the skill was used and the inspection ran in 8 of 10 samples with the readiness wording (r16: 2 of 3, r17: 2 of 2, r18: 4 of 5), against 1 of 3 before it (r14). In 2 samples the agent said that PDF import is not available and offered to run the check.
- H1 (r16, r17): pass.

Skill use in all 70 Haiku sessions (run 9 and run 10): the matching skill was loaded in 12 of 12 B1 session starts, in 6 of 7 goal changes (F1), and in 5 of 5 rule records (E1, E4); for the readiness question (D1), the Skill tool was used in 8 of 13 samples. English-only notes between tool calls: 5 of 136 (r17, 4 in one D1 sample, where the per-turn reminder could not read the language label "交互语言"; r18a, 1).

Defects after run 10.

- D-15: fixed (decision record in 7 of 7 Haiku F1 samples).
- D-16: residual. The readiness question reached the inspection in 8 of 10 samples; text changes did not remove the other 2.
- D-17: fixed at its cause for the skill path (Step 6). On the path without the skill (1 of 7 goal changes), the contract's general sentence leaves the choices open and the agent offered a rewrite. No sentence is added to the contract for this.
- D-18: fixed (no decision record for spelling or language in any Haiku sample).
- D-19: fixed in the samples taken (one next action in 4 of 4 B1 samples).
- D-20: fixed in the samples taken (2 of 2 E1 samples end with a record that passes the check, after the agent used the check or the script).
- D-21: mostly fixed (exact words in quotation marks in B1 4 of 4; in F1 small changes in 2 of 5).
- D-22 (new, Low): the record `project.md` was written in English once (r19, 1 of 5 Haiku B1 writes of that file).
- D-14: not re-tested.

Findings about the checklist.

- E2 asks the agent to write manuscript text, which the availability table lists as not available. An agent that follows `AGENTS.md` now declines the first request, so the scenario needs a revised script. The checklist notes this.
- The passes of A1, B2, C1, D3, D4, E2, E3, E5, F2, and G1 date from runs 1 and 2 with Sonnet. The checklist asks for a full repeat after changes to the rules.

Other levers that remain (proposed; not applied): a hook that runs the form check after a write to `requirements/`; scripts that write the records; a routing test that sends the scripted messages and checks which skill loads; a machine-readable place for the interaction language, so that the per-turn reminder does not depend on a prose label.

Limits. Two to ten samples per scenario. The fixture copies r18a to r18c reproduce the B1 output of r17, not a fresh B1. The Haiku harness refused several compound shell commands, which the agent worked around.

## MVP 1 acceptance runs 11 and 12: Claude Code with Haiku, full checklist (2026-10-28)

Status: run 11 is the first full pass of the checklist with Haiku as the subject model. It ran on a clean copy of the committed repository (commit `68b92f4` and the records after it), without the per-turn reminder or any other test overlay. Of the 18 scenarios that were run, 9 pass, 8 fail on minor points, and E2 cannot pass as written. Run 12 retested D1 and C1 after two skill fixes. MVP 1 is not verified.

Method. Copy r21 is a clone of the repository without `docs/acceptance`. A1, B1, and B2 ran in r21. Copies r22 to r30 are copies of r21 after B2, one per group of scenarios, so that each scenario starts from the state that the checklist assumes (r22: D1, D2, D4; r23: C1; r24: D3; r25 to r27: E1 to E6; r28: F1 and F2; r29 and r30: two more D2 samples). Every session used `claude-haiku-5-5`. Three harness changes were needed. C1 ran with web tools allowed, and the account type came from the CLI (a personal Pro plan; no identifier was printed). D3 ran in a session that stays open: a controller fed messages through a queue, and the credential script's browser call wrote the page address to a file, so that the page could be opened in the desktop app's browser and the fake value from the checklist entered there. Scripted answers followed the question that the agent actually asked.

Results.

- A1 Pass. B1 Pass. D4 Pass. E1 Pass. E3 Pass. E4 Pass (explicit form: replaced without a question; ambiguous form: one question and no change before the answer; no decision record in either). E5 Pass. F2 Pass. H1 Pass in 10 copies.
- B2 Fail (minor): the first reply did not ask whether to continue or start a new paper; it asked two questions, one offering a Git commit, which the availability table lists as not available. The second reply passed.
- C1 Fail (minor): everything held except that the report in `.local/` was in English, although Step 6 asks for the researcher's language. Run 12: after a language reminder in the report template, the report was in Chinese (1 sample).
- D1: the skill ran the inspection in 2 of 3. In the third sample, `python` was not found, and the agent stopped and asked for permission, because Step 1 named `py -3` for Windows but not `python3` for macOS and Linux (D-23, fixed in run 12 in the skill). Run 12: the inspection ran in only 2 of 5 samples; in the other 3, the agent said that importing is not available and offered the check. Over all 18 Haiku samples with the readiness wording, it ran in 12.
- D2 Fail (minor), 3 samples: no key was asked, `privacy.md` stayed unchanged, and `.env.local` did not exist. No sample noted the cloud wish in `state/current.md`, and no sample loaded a skill.
- D3 Fail (minor): the page ran in the background with Chinese texts; the value appeared nowhere in the session; `.env.local` had mode 600 and Git ignored it; the removal worked. The confirmations were in English and did not give the length. An earlier, aborted attempt passed English page texts.
- E2 cannot pass as written: the agent declined to write manuscript text, as the availability table requires; no file changed and no rule was recorded.
- E6 Fail (minor): the first sentence had no word that differs between British and American spelling, so the rewrite changed nothing; the reply did not say that the saved rule was unchanged or offer to change it. The script needs a variant word (a note was added to the checklist).
- F1: the confirmation passed (the skill, the decision record and index entry, the manuscript unchanged, two choices, and revising named as not available). The question turn failed on minor points: two questions, no request to confirm, and `project.md` not read.
- G1 Fail (minor): B2 and the F1 question turn bundled two questions, and D1 asked again about a choice that was deferred.

Skill use in the 42 sessions of run 11: the matching skill was loaded in every B1 session start (4 of 4), in the goal change (1 of 1), and in the rule scenarios (3 of 4, with the first turn of each loading it). For the readiness question, the Skill tool was used in 3 of 3 samples in r22. For the cloud wish (D2) no skill was loaded in 3 of 3. English-only notes between tool calls: 3 of 46, all in D1; the D3 session had 2 English notes and 2 English replies.

Defects after runs 11 and 12.

- D-23 (Low; fixed in the skill): Step 1 of `environment-management` named `py -3` for Windows only. It now names `python3` for macOS and Linux. In run 12, no sample stopped for this reason.
- D-16 (extended; residual): the readiness question reaches the inspection in 12 of 18 Haiku samples. A cloud wish loads no skill (0 of 3) and is not noted in `state/current.md`. Text changes in the skill description, the table row, and the skill did not remove these misses.
- D-22 (extended; residual): records and replies in English on Haiku: `project.md` once (run 10), the privacy report (C1, fixed by a language reminder in the template), and the replies in the credential flow (D3, 2 of 3). Replies that follow a background event are the likeliest to be English.
- D-24 (new, Low): replies that bundle two questions (B2, the F1 question turn), and one offer of a capability that is not available (a Git commit in B2).
- D-25 (new, Low; test scripts): E2 asks for manuscript text, and E6 needs a variant word. The checklist notes both.
- D-15, D-18, D-19, D-20, and D-21 held: the decision record in F1 (1 of 1), no decision record for spelling (E1, E4: 3 of 3), one next action (B1), the form check run and passing (E1, E4: 3 of 3), and exact quotation of the researcher's words (B1 and F1).

Changes in run 12 (skills only; committed in `67607d8`): `environment-management` Step 1 names `python3`; `report-template.md` of `privacy-configuration` tells the agent to write the report in the researcher's language. No sentence was added to `AGENTS.md`.

Limits. One sample per scenario, except D1 (18 samples), D2 (3), and C1 (2 with different answers). D3 needed a harness that does not exist in the repository; it lives in the maintainer's scratchpad, with the other test tools.

## MVP 1 acceptance run 13: Claude Code with Haiku, second full checklist (2026-10-28)

Status: run 13 is the second full pass of the checklist with Haiku and the last live run. It ran on a new clean copy of the committed repository (commit `3b491ec`, without `docs/acceptance`), with the revised scripts of E2 ("a declined request records no rule") and E6 ("the first sentence needs the word color"). Of the 18 scenarios, 11 pass (run 11: 9) and 7 fail on minor points. The maintainer then ruled that a skill passes acceptance by review, not by live runs (see [the skill review](acceptance/mvp-1-skill-review.md)), so no further live run is planned.

Method. Copy r34 is a clone of the repository without `docs/acceptance`. A1, B1 (two sessions), and B2 ran in r34. B2 appended a note to `state/current.md`, so copies r35 to r54 were made from r34 with that note removed, which is the state after B1. r35: D1 (three samples) and D4; r36: C1 (web tools allowed; the account type came from the CLI, a personal Pro plan); r37 to r39: D2, one copy per sample; r40: D3 (an open session fed through a queue, with the fake value entered in the desktop app's browser on `127.0.0.1`); r41: E1; r47 and r48, copies of r41: E2 and E3; r49, a copy of r41: E4 (explicit form), then E5, then E6; r50 to r52, copies of r41: E4 (ambiguous form, three samples); r53 and r54, copies of r49: two more E6 samples; r46: F1 and F2; r55: G2 (onboarding in English). r42 to r45 were made but not used. Every session used `claude-haiku-5-5`.

Results.

- Pass (11): A1, B1, C1, D3, D4, E1, E2, E3, E5, F2, H1 (13 copies).
- B2 Fail (minor): the first reply summarized the recorded settings and asked what to do next, not whether to continue or start a new paper. After "new paper" it explained the fresh copy and that no remote exists, but it appended a note to `state/current.md`.
- D1 Fail (minor): the inspection ran in 2 of 3 samples, but neither report recommended a next step or said that writing continues; the third offered the check. Over runs 10 to 13 it ran in 14 of 21 samples.
- D2 Fail (minor), 3 samples: no key asked, `privacy.md` unchanged, no `.env.local`; no sample loaded a skill or noted the cloud wish in `state/current.md`.
- E4 Fail (minor): the explicit form passed. In the ambiguous form, 1 of 3 samples replaced the rule at once; the other 2 asked one question with a recommendation and changed no file before the answer.
- E6 Fail (minor), 3 samples: the rewrite was right (`colour`), but no reply said that the saved rule was unchanged or offered to change it; no skill was loaded.
- F1: the confirmation passed (skill, decision record 0001 with an index entry, manuscript unchanged). The question turn failed on minor points: no recommendation and no request to confirm the change.
- G1 Fail (minor): D4 bundled two asks, and three questions gave no recommendation.
- D3 passed with Chinese confirmations that gave the length (19 characters); the value is absent from the whole session log. C1 passed with a Chinese report and no identifier.
- G2 (observations only): one question per message with a reason and a recommendation, in short sentences with a few of 23 to 24 words; the STE check is not implemented.

Skill use. `project-onboarding` loaded in both B1 sessions and in B2. `constraint-maintenance` loaded in E1, in E4 (4 of 4 first turns), and in the F1 confirmation, but in none of the 3 E6 samples. `environment-management` loaded in 2 of 3 D1 samples, and no skill loaded in the 3 D2 samples. `privacy-configuration` loaded in C1. English-only notes between tool calls: 2 of 83 text blocks.

New defects (all Low).

- D-26 (skill): in B2, the case table did not make the agent ask whether to continue; the "new paper" reply changed `state/current.md`, where the skill says to change nothing and `AGENTS.md` "Finishing work" says to update the state when work remains.
- D-27 (routing): the one-time-edit reply of E6 omits "no rule changed" and the offer in 3 of 3 samples (and in run 11). The clause is in `AGENTS.md` and in `constraint-maintenance` Step 3, but the skill did not load.
- D-28 (variance): the ambiguous E4 form replaced the rule at once in 1 of 3 samples.
- D-29: the D1 reports omit a recommended next step and the statement that writing continues.
- D-30: capability remarks: one reply offered a paragraph-by-paragraph spelling check of the manuscript (an audit, which is not available), and one remarked that a change was not committed to Git.
- D-31 (checklist): E1 expects Chinese labels, but the skill's layout has English labels, which the checker accepts.
- D-16 and D-22 stay residual: the readiness question reaches the inspection in 14 of 21 samples, and a cloud wish loads no skill.

Limits. One sample per scenario, except D1 (3), D2 (3), E4 ambiguous (3), and E6 (3). The harness (`cc.py`, `ctl.py`, and the helper scripts) lives in the maintainer's scratchpad, not in the repository.

## Skill acceptance by review (2026-10-28)

Ruling. The maintainer ruled twice on 2026-10-28: skills get no more hard (live scenario) tests, and a passed review counts as the skill passing acceptance. The [MVP implementation guideline](mvp-implementation-guideline.md#6-completion-record-for-each-mvp) records the rule. The pass criteria were fixed before the review started.

Result. The [skill review](acceptance/mvp-1-skill-review.md) checks 12 cross-cutting requirements and 57 requirements of the four skills against the design plan, the guideline, `AGENTS.md`, the interaction specification, and the rule-placement principles. All four skills pass. The review found seven groups of text gaps (F-1 to F-7) and fixed them in the skills; the source note was rewritten in the MVP 2 work. No script, availability row, `AGENTS.md` sentence, or `CLAUDE.md` line changed. MVP 2 landed on `main` while the review was written, so it was checked again against the merged tree; that second look changed one example sentence in `environment-management` (F-7). The mechanical checks pass on the merged tree: 6 skill packages, the availability table, 43 directory READMEs, rule form, and 49 script tests.

Mapping to the defects of run 13. D-26 is F-1 (the case table and the new-paper branch of `project-onboarding`). D-31 is F-4 (the label rule of `constraint-maintenance`, with its decision-record link and the planned skills). D-27, D-28, D-29, and D-30 are model behavior, so they stay residual risks (review section 6); the skill text already asks for the behavior.

Not covered. Windows and ARM64, Codex, real provider settings, ASD-STE100 compliance, the live MinerU credential, and whether a given model follows the text (review section 7). These stay unverified.

Documents changed to match: the guideline (status, section 1 step 4, sections 5 and 6), the design plan (section 14), rule placement (principle 6, the testing row, and the residual risks), the acceptance README and checklist, the documents README, the skills READMEs, and the root README.

## Additional verification and residual risks for MVP 1

MVP 1 is accepted under the 2026-10-29 gate. The four skills passed review on 2026-10-28 and Claude Code runs 1–13 remain historical evidence. The following are additional verification or residual risks, not acceptance blockers:
- Decide whether a deterministic lever is worth adding for the residual model risks (the readiness routing, a cloud wish that is not noted in the state, the one-time-edit reply, and English notes): a host hook for the language reminder and the form check, scripts that write the records, or a machine-readable interaction-language setting. The review accepts the skills without it. Add no sentence to `AGENTS.md`. D-14 (an English first note before a skill call) belongs here.
- Codex: a targeted fresh-agent recovery was observed during the later complete-path exercise, but this does not verify every MVP 1 flow; check current skill discovery, `AGENTS.md` loading and relevant scenarios before broad platform claims.
- Windows baseline: no Windows machine yet, so Windows and ARM64 stay unverified.
- English question checks against the official ASD-STE100 issue, and the clarity review for questions in other languages. The standard and its dictionary are not bundled with the template; they need access under the publisher's terms.
- Optional: the scenarios that the live runs could not exercise (the interactive question tool, missing Python or tools, and an account control that the researcher can read).

The read-only MinerU service research, which this list carried earlier, was done on 2026-10-28 with MVP 2; see [MinerU integration](mineru-integration.md).

The [MVP 1 skill review](acceptance/mvp-1-skill-review.md) holds the requirements and the verdicts, and the [checklist](acceptance/mvp-1.md) holds the scenarios and the results of the live runs. The disposable test copies have no Git remote: `/Users/wota/Projects/paper-template-mvp1-test-claude` (run 1), `...-claude-r2` (run 2), `...-claude-r3` (run 3), `...-claude-r4` (run 4), and `...-claude-r5` (run 5) each hold the changes of their run. `...-claude-r7` to `...-claude-r11` hold runs 6 and 7; the state files of r7 were lost (see the runs 6 and 7 section). `...-claude-r12` and `...-r13` hold run 8, and `...-claude-r14` and `...-r15` hold run 9. `...-claude-r16` to `...-r20` hold run 10 (`...-r18fix` is the prepared fixture). `...-claude-r21` to `...-r33` hold runs 11 and 12 (`r21` is the clean copy; `r22` to `r30` are copies of its state after B2, one per group of scenarios; `r31` to `r33` carry the two skill fixes). `...-claude-r34` to `...-r55` hold run 13 (`r34` is the clean copy; `r35` to `r54` are copies of its state after B1, of the E1 state, and of the E4 state; `r55` is the English run; `r42` to `r45` were not used). `/Users/wota/Projects/paper-template-mvp1-test-codex` is untouched, cloned from `51f93e7`, so it predates the fixes.

## MVP 2: flexible intake and MinerU batch ingestion

Status: MVP 2 accepted under the MVP 2-style gate on 2026-10-29; both skills passed [written review](acceptance/mvp-2-skill-review.md) on 2026-10-28. Platform and service claims outside the observed evidence remain unverified. The scripts pass their tests, and both routes were observed working on macOS with synthetic files: the local route, and the mineru.net route with the maintainer's token. Windows and Codex have not been run. Under the maintainer's ruling of 2026-10-28 ([guideline section 6](mvp-implementation-guideline.md#6-completion-record-for-each-mvp)), skills pass acceptance by a written review instead of live scenario runs.

Request: on 2026-10-28 the template maintainer asked to implement MVP 2 in a new worktree and to merge it into the main branch when done. The planned order put MVP 7 and the export trial first; the maintainer chose MVP 2.

Decisions (2026-10-28), the maintainer's answers to three questions:

- Routes: both MinerU on this computer and the official mineru.net service (precision API v4). The token-free Agent API is not used: at most 10 MB and 20 pages, and Markdown without images.
- Test installation: MinerU 4.0.12 in the worktree's ignored `.tools/mineru/`, tested with the flash and basic tiers on synthetic files. The standard tier was not tested.
- Citation metadata: BibTeX in `references/bibliography.bib` is canonical from now on, before the export trial.

The research behind these choices, the observed MinerU behaviour, and the mineru.net terms are in [MinerU integration](mineru-integration.md).

Implemented:

- `scripts/ingest.py` with its modules in `scripts/ingestion/` (standard library, Python 3.9 or later): `plan`, `run`, `status`, `verify`, `metadata`, and `note`. It archives each original under a checksum-based source ID, converts it with the confirmed route only, checks page coverage, pages without text, text left out of the Markdown, image links, and math delimiters, publishes the extraction in one rename with `provenance.json` and READMEs, updates `references/index.md`, and keeps a resumable record in `inbox/imports/<import-id>/`. It reuses matching results, converts again only on request, refuses to overwrite a hand-edited `document.md`, and stops a whole run once for failures that would repeat (missing models, a rejected or expired token, the daily limit, the network). Review documents go to `reviews/<venue>/<round>/`, with Word comments, replies, insertions, and deletions read from the file's XML and PDF comment annotations from a best-effort scan.
- The mineru.net route runs only when `requirements/privacy.md` names mineru.net and the `MINERU_API_TOKEN` credential exists. The token goes only to the API address; the service sees the source ID instead of the file name; signed addresses and the token are removed from records and logs; batches are paced below the service's rate limit.
- `scripts/setup_mineru.py`: `check`, `install` (MinerU 4.0.12 into `.tools/mineru/`), and `models` (into `.cache/mineru/`).
- Skills `source-ingestion` and `review-ingestion`, with generated Claude Code copies.
- `.env.example` names `MINERU_API_TOKEN`. The fixture generator `docs/acceptance/fixtures/make_mvp2_fixtures.py` and the [MVP 2 checklist](acceptance/mvp-2.md).
- Changes to MVP 1 files: the availability table in `AGENTS.md` (two new rows, and the credential row now names its user); `privacy-configuration` (a cloud choice is recorded with the service's address, and `sources.md` holds the mineru.net findings); one sentence in `environment-management` pointing to `setup_mineru.py check`; the status sentence of the root README; and the READMEs of `references/`, `references/extracted/`, `inbox/imports/`, `reviews/`, `scripts/`, `scripts/tests/`, `.agents/skills/`, `docs/`, and `docs/acceptance/`.

Verification observed (macOS 26.6.2 on Apple Silicon, 16 GB; Python 3.9.6 and 3.12.9; MinerU 4.0.12):

- 49 script tests pass on both Python versions: 16 for the local route with a fake parser, 6 for the cloud route with a fake service, and the 27 earlier tests.
- Live local runs on a disposable copy of the workspace with the synthetic fixture folder: with the flash tier, the 12-page report converted 12 of 12 pages; the exact duplicate with a non-ASCII name was recognized; the unsupported file and the corrupt PDF were reported with their reasons; the scanned page was flagged as having no text; the Markdown file was read directly; and a different file with the same name in a subfolder got its own source ID. The first run stopped at a Python 3.9 incompatibility, which is fixed; continuing the same import finished the interrupted file and the open ones.
- Importing the folder again with the basic tier reused the three earlier results and reported their other settings. Converting two files again with the basic tier read the scanned page's text, structured the table, and moved the report to revision 2 with its earlier revision listed. One printed formula was transcribed wrongly, and a formula image was merged into it; no automatic check can detect that, and the extraction README says that formulas are not verified.
- A review round from the Word decision letter and the annotated PDF listed 2 comments with their anchored text, 1 insertion, 1 deletion, and the text of 2 PDF annotations; MinerU alone had shown the tracked changes as accepted and lost the comments. Importing the round again created no duplicate.
- On the copy, the README check passed for every folder that the import created, `ingest.py verify` passed, and `metadata` wrote a BibTeX entry with special characters escaped.
- `setup_mineru.py check` reported the installation, both tiers' models, and the disk use correctly. In a second disposable copy, `setup_mineru.py install`, started with Python 3.9.6, chose Python 3.12.9, installed MinerU 4.0.12 with pip (1.37 GB), and the check that followed reported both tiers' models as not installed.
- Live mineru.net runs, on 2026-10-28, in a disposable copy with the maintainer's token. The maintainer first pasted a token into the conversation; it was not used from there, and the value that the import used was entered on the private page. Only synthetic files went up: the 12-page report, the scanned PDF, the Word source, and the review round (Word letter and annotated PDF). The service ran MinerU 3.4.4 (hybrid backend, model `vlm`) and returned three results in about 12 seconds: 12 of 12 and 2 of 2 pages, the scanned page read, columns in order, running heads recognized, tables as HTML. It mistranscribed the printed formula like the local basic tier, and it took the annotation icons of the review PDF and the text under them for images ("Comment 1" became "mment 1"). No file or log held the token or a signed address, and the service saw only source IDs as file names. The runs found three gaps, now fixed and covered by tests: a Word original's copy kept in `native/`, the service's parser version not recorded, and a correct image link of a review document reported as broken because the stage was laid out differently from `extracted/`. PDF with the `vlm` model is a verified cloud combination. Word conversion was observed, but the service output has no `is_full_document` marker, so its completeness is unknown and results need review. The token was removed from `.env.local` after the runs.

Review (2026-10-28). The [skill review](acceptance/mvp-2-skill-review.md) checked both skills, and the scripts they rely on, against the guideline, the design plan, and `AGENTS.md`, with pass criteria fixed before it started. It found nine gaps and fixed them: copied standing rules and a promise of an unavailable response in the skill text; no record of a local route confirmed at the first import; related versions not linked; no role in the import record; no note in the text of a partial extraction; collaborators' advice not kept out of review rounds; a correction step that could read as evidence work; and PowerPoint and Excel presented as verified. For the review, a Word source with a heading, a table, and a figure was imported live with the flash tier: a Markdown table, a linked image, coverage of the whole document, and no warning.

Not verified:

- How a model follows these skills: no live run was made, and the review lists the risks that the MVP 1 runs make likely. The [MVP 2 checklist](acceptance/mvp-2.md) was written before the review ruling and was not run.
- At mineru.net: the training use and retention of uploaded documents, which its terms do not state; behaviour at its limits (daily quota, rate limit, an expired token), with images, and with the `pipeline` model, which only the fake service exercised.
- The standard tier; local formats other than PDF, Word, Markdown, and text (they are converted but flagged as unverified); Windows and Linux.
- Page numbers of PDF annotations, Word footnotes and endnotes, and the accuracy of OCR, tables, and formulas.

Effect on MVP 1: scenarios D1 and D2 of the [MVP 1 checklist](acceptance/mvp-1.md) assume that document import is not available. Under the review ruling the checklist is history, so they need no revision; the [MVP 1 skill review](acceptance/mvp-1-skill-review.md) was checked again against the tree with MVP 2.

Remaining for MVP 2:

- A fresh read of the mineru.net terms before uploading researcher materials; the live run used synthetic files, and the terms do not state training use or retention.
- Windows runs of both routes, and Codex discovery of the two skills.
- A decision on testing the standard tier.

## MVP 3, implementation increment: literature search, retrieval, and evidence records

Additional Sciverse development on 2026-10-28: metadata pagination now resumes one page at a time from the recorded query, scope, filters, sorting and cursor, reusing the saved catalog snapshot to reduce calls. Experimental DOI-based Paper Schema discovery and material packs and bounded service-resource retrieval have synthetic tests; individual endpoints have not been verified live. The [quality evaluation](acceptance/sciverse-quality-evaluation.md) now has a four-query retrieval smoke run, but the expected sources and evidence have not been checked against originals. No change in capability status is established by these additions.

Status: accepted by the maintainer on 2026-10-28. Confirmation: “MVP3就算验收通过吧”. The maintainer's acceptance standard was: “我们验收标准和mvp2差不多的标准就行”. Under that gate, all four skills passed written review, 79 script tests and the mechanical checks pass, and required live-service evidence was recorded. The [MVP 3 skill review](acceptance/mvp-3-skill-review.md) records the evidence and remaining limits. The [MVP 3 checklist](acceptance/mvp-3.md) remains an optional manual aid.

Implemented on 2026-10-28:

- `scripts/literature.py` and `scripts/literature/` use the Python standard library. `search-sciverse` and `search-sciverse-metadata` require an exact scope excerpt from the active confirmation and record it with the query; the agent must still judge whether the scope covers the query. `authorize-sciverse` records a confirmation supplied by the skill and supports confirmed scope replacement or revocation, and the API key is loaded through the existing private credential flow. Requests use the documented fixed host, bearer header, bounded retries for server errors, and no retry for HTTP 429. `read-sciverse-context` requires a returned document ID from the recorded search and an excerpt that remains active; it stores full-text ranges separately from search snippets.
- Search records under `references/searches/<search-id>/` retain each provider route's exact query and timestamp, Sciverse scope basis, source identifiers/locators, metadata, limitations, errors, and separately appended model-host results. Host-search records require a non-empty coverage note. Local retrieval streams selected extracted Markdown and reports line numbers with extraction revisions; it does not claim that a line number is a PDF page locator.
- `download` reads BibTeX, Markdown, and text DOI/URL lists; it archives only publicly returned PDF files after checking the PDF signature and end marker. It retains per-item retrieval status, checksum, source ID, sanitized locator, duplicate information, and identity/version review in `references/downloads/<batch-id>/`. It does not store signed query-string URLs or use publisher credentials. Conversion is handed to `source-ingestion`; download records and archived originals are independent of conversion success.
- `audit-bibliography` checks BibTeX key uniqueness and links to archived source IDs. It explicitly does not assess claim support. Evidence support, quotes, page numbering, extraction revision, and limitations are governed by `literature-and-evidence`.
- The four canonical skills are `literature-discovery`, `reference-download`, `literature-and-evidence`, and `research-investigation`. All passed written review and are listed in `AGENTS.md` with their current support boundaries. `.env.example`, the references directory descriptions, and the acceptance checklist document those boundaries.
- The Sciverse API facts checked from public documentation are recorded in [Sciverse integration](sciverse-integration.md). On 2026-10-28, an authorized synthetic check observed `agentic-search` twice (three snippets per call), `meta-search` once (25 metadata records), and `content` once (71 returned characters with a limit of 200). The temporary scope, identifiers, metadata, and retrieved text were isolated under `.tmp/` and removed; no project privacy scope was recorded.

Verification observed:

- The full script suite (79 tests), CLI/help behavior, README, capability-table, skill-mirror, writing-rule, ingestion-record, and Python syntax checks pass. The optional manual scenarios were not run end to end.
- The authorized live checks cover `agentic-search`, query-only `meta-search`, and bounded `content`. The downloader's validation, deduplication, status, and resumption behavior passes local synthetic HTTP tests.
- A four-query Sciverse smoke run made one `agentic-search` request per public test question (`top_k=5`; four requests, no retries). Each returned five records; the expected climate-paper title appeared, while the expected Transformer paper and named clinical trials were not identified in the top five by title or listed identifiers. No content was fetched or checked against originals.

Not verified:

- Catalog filters, filtered metadata pagination, relations, resources, and Paper Schema have synthetic tests only. Repeat availability, quota behavior, returned-content correctness against originals, and model-host fallback ordering remain unverified.
- No live public publisher/repository PDF retrieval or actual download-to-ingestion handoff has been observed. The implementation supports direct public PDFs only; authenticated integrations are not implemented.
- The four-query run is not a source-verified quality evaluation; claim support, locator accuracy, semantic interpretation, and contrary-evidence retrieval remain unverified. Windows and Codex skill discovery/loading remain unverified.

MVP 3 acceptance passed under the maintainer's MVP 2-style ruling. Live public-PDF access, the model-host fallback, original-checked evidence quality, catalog filters/relations, resource and Paper Schema operations, and Windows/Codex operation remain unverified; do not describe these integrations as working.

## Decisions of 2026-10-28 for MVP 4 to 9

The maintainer asked to implement all MVPs from MVP 4 on (“继续完成MVP4开始的所有mvp的实装”) and answered four questions the same day:

- Result production: `research-code-setup` and `research-investigation` carry authorized research work through to actual results, each recorded in a result record (inputs, method or code version, parameters, outputs, checks, limitations, and the claims that use it) in `research/results/`. No new skill is added. This settles the open item that the guideline placed before MVP 4.
- Export trial: only Pandoc is installed for the trial (with pandoc-crossref), in the ignored `.tools/`. Quarto is not installed or compared.
- First output profile for MVP 6: a neutral profile and a synthetic representative journal profile with explicit rules, Word (DOCX) first and PDF later.
- Version control of this work: commit on `main` in one batch per MVP, without a branch and without pushing. The pending MVP 3 acceptance changes were committed first (`8810f41`), as the maintainer asked (“先提交上一次会话留下的、未提交的 MVP 3 验收改动”).

Implementation choices made without a separate question, because they are reversible layout details inside the confirmed scope: the research plan is `research/plan.md`, kept impact assessments are `research/impact.md`, venue notes are in `research/venues/`, and research runs are recorded in `code/runs/`.

## MVP 4: ideas, impact, journal choice, research plans, feedback, and research code

Status: all seven skills accepted by review on 2026-10-28 ([skill review](acceptance/mvp-4-skill-review.md)), together with the extension of `research-investigation` to project results. MVP 4 as a whole is not verified: no venue page was read live, no skill ran in a fresh session, and Windows and Codex were not exercised.

Implemented:

- Skills `research-ideation`, `idea-deepening`, `impact-assessment`, `journal-selection`, `research-planning`, `research-feedback`, and `research-code-setup`, with generated Claude Code copies. `research-investigation` now writes a result record for documentary, qualitative, or theoretical research work.
- Record formats, refined as the design plan scheduled for MVP 4, in the READMEs of `research/decisions/` (decision records with supersession links in both directions), `research/feedback/` (`actions.md` with author, source, kind, status, decision, and change), `research/results/` (result records), `research/venues/` (venue notes with dated official sources), and `ideas/` (idea notes and index lines). Values are in the interaction language; the labels are fixed, and the listed Chinese labels are accepted.
- `scripts/research.py`: `check` validates those records and reports a result as stale when an input or output checksum changed; `code-init` creates only the requested parts of `code/` with READMEs and, on request, the separate environment `code/.venv`; `run` records a research run (command, code checksum, Git commit, interpreter, inputs and outputs with checksums, logs, exit status, and optionally the package list) in `code/runs/<run-id>/`; `runs` lists the runs and the files that changed since.
- `scripts/ingest.py` accepts `research/feedback/<feedback-id>` as a destination, with the same extraction as a review round: Word comments, replies, and tracked changes keep their authors. The README helper now names the script that maintains each README block.
- Earlier skills no longer call research feedback or idea development unavailable (`constraint-maintenance`, `review-ingestion`, `source-ingestion`, `project-onboarding`). `constraint-maintenance` writes decision records with the folder's layout and runs the record check.
- New folders `research/results/` and `research/venues/`, each with a README and an empty index; the `research/` README, the root README, the skills README, the scripts READMEs, and the glossary (result record, venue assessment).

Verification observed (macOS 26.6.2, Apple Silicon; Python 3.12.9, and Python 3.9.6 for the research tests):

- 96 script tests pass, 17 of them new: 15 in `test_research.py` (decision chains in Chinese and English, feedback attribution and decisions, ideas, venue notes, result records with a stale input, the code folder, a run in the separate `code/.venv` with its package list, failures, missing outputs, and refused inputs) and 2 in `test_ingest.py` (a feedback event with two comment authors, and destination validation).
- The skill copies match, the availability table matches the skills folder, every project directory has a README, and the template's empty research records pass `research.py check`.
- Claude Code listed the seven new skills in this session after their copies were generated.

Not verified:

- Reading venue pages through the agent application's web access; the behavior of a model in the interview, planning, and feedback procedures; research runs on Windows, in other languages, with large data, or for long runs; Codex discovery.

## MVP 5: evidence-based writing, audit, and major revision

Status: the five skills were accepted by review on 2026-10-29 ([skill review](acceptance/mvp-5-skill-review.md)). MVP 5 as a whole is not verified: no model followed the procedures in a fresh session, and real manuscripts, Codex, and Windows were not exercised.

Decision (2026-10-29): the researcher's own editable manuscript (Word, OpenDocument, LaTeX) is converted with Pandoc on this computer; PDFs and every other document keep the MinerU routes. The maintainer chose this (“可编辑稿件用 Pandoc（推荐）”) and asked for a comparison with more widely adopted open-source converters (“或者你看看有没有更先进，星多的开源实现也可以”). The comparison, in the [skill review](acceptance/mvp-5-skill-review.md#5-the-converter-decision-and-its-evidence), found MarkItDown, Docling, MinerU's Office engine, and mammoth worse on formulas, footnotes, and tracked changes, so Pandoc was kept. `AGENTS.md` names the exception in its MinerU rule.

Implemented:

- Skills `manuscript-import`, `manuscript-outline`, `manuscript-writing`, `manuscript-audit`, and `manuscript-revision`, with generated copies. `constraint-maintenance`, `source-ingestion`, and `git-recovery` route to them.
- `scripts/manuscript.py`: `check` (the conventions: manifest, math and equation labels, figure, table, equation, and section references, citation keys against the bibliography, images, hand numbering, words repeated before references, currency, open `[TODO: ...]` markers); `set-sections`; `assemble` with word counts; `record-check` and `checks` (check records with input checksums in `outputs/checks/`, stale when an input changes); `adopt` (a converted manuscript into section files with its images, metadata, footnotes, and a mapping report, refusing tracked-change marks and never writing over a manuscript, or into a revision candidate); and `revision-start`, `revision-status`, `revision-apply` (resumable, refusing unreconciled author edits), and `revision-restore`.
- `scripts/ingest.py --to manuscript` keeps the original and the extraction in the import record; `--route pandoc` (only for the manuscript) reads Word with citation fields and tracked changes as marks (`--track-changes all|accept|reject`), OpenDocument, and LaTeX; `scripts/ingestion/adopt-conventions.lua` applies the workspace conventions (formulas, label paragraphs, prefixed labels, `@`-references, inline formulas in OpenDocument text, bookmark removal). Word comments and tracked changes are listed beside the text in `<document>.annotations.md`.
- The `[TODO: ...]` marker and the Mermaid figure caption (`: Caption {#fig:id}` after the block) in the [conventions](markdown-and-export-conventions.md); the READMEs of `manuscript/`, `outputs/`, and `revisions/`; `check_readmes.py` treats revision baselines and research data folders as received or generated content, and quoted syntax as documentation.

Verification observed (macOS, Python 3.12.9; Pandoc 3.12.1): 15 tests, 4 of them live Pandoc conversions; a live adoption of the export-trial Word file (four sections, its image and metadata, three typed equation numbers flagged, a second adoption refused).

Not verified: real Word manuscripts with complex fields, cross-references, or old equation-editor objects; a PDF manuscript through MinerU; model behavior in the writing, audit, and revision procedures; Codex; Windows.

## MVP 6: template-driven layout and readiness

Status: both skills accepted by review on 2026-10-29 ([skill review](acceptance/mvp-6-skill-review.md)). The Word (DOCX) route is observed on macOS with a neutral and a synthetic journal profile; a real journal template, other PDF routes, Windows, and Codex are not verified.

Implemented, after the export trial's decisions:

- Skills `submission-assembly` and `submission-readiness`, with generated copies; `constraint-maintenance` now routes formatting requirements to the profile through `submission-assembly`.
- `scripts/export.py` with `scripts/export/`: `tools` and `install` (Pandoc 3.12.1 and pandoc-crossref 0.3.26 from their official releases with checked SHA-256 digests, and mermaid-cli 12.0.0 with npm, using an installed Chrome-family browser); `profile-init`; `reference-doc`, which rebuilds the Word reference document from settings kept in `profile.yaml` and writes the section properties in schema order; `build`, which refuses a manuscript with convention problems, renders Mermaid diagrams as figures, builds the DOCX with the workspace's Lua filters, pandoc-crossref, and citeproc, and checks every source formula against a native Word equation with matching structure, figures, references, citations, layout expectations, length, anonymization, and open markers, recording inputs, tools, and command in `build.json`; `verify`; `render` (Word on macOS and Windows, or LibreOffice); and `release`, which freezes only a passing, current build and never overwrites a release.
- The profile layout of `requirements.md` (each rule with its source, implementation, check, result, and confirmation) in `requirements/profiles/README.md`; the README check treats quoted syntax as documentation, not as a placeholder.

Verification observed (macOS 26.6.2, Apple Silicon; Word 16.114.2; Chrome 156): 10 export tests, two of them real builds and one a Mermaid figure. A live synthetic manuscript built with both profiles: 9 of 9 formulas native, 2 of 2 figures, all references and citations resolved, and every journal expectation met; Word's PDF was inspected page by page (A4, line numbers, Times New Roman, double spacing, numbered black headings, equations, the diagram with a Chinese label, the table, the references). The inspection found a missing plural prefix ("Eq. 1, 2"), fixed in the build. Releases were frozen once, refused for a reused ID, and refused after an edit made the build out of date.

Not verified: a real journal's own template and current guidelines; editing an equation in Word; Word fields for figure and table numbers; Word on Windows and LibreOffice rendering; PDF routes other than Word's rendering of the checked DOCX; missing fonts; Codex.

## MVP 8: review rounds and coauthor reconciliation

Status: `review-response` accepted by review on 2026-10-29 ([skill review](acceptance/mvp-8-skill-review.md)). No real review round or coauthor file was used.

- Skill `review-response` with its generated copy; `review-ingestion` now hands over to it.
- `scripts/review.py`: `check` validates a round's `response.md` and `changes.md` (every item's reviewer, source, comment, status, and response; addressed items link a done change in the same round whose location exists; declined items give a justification); `reconcile` compares a coauthor's Word file with the version they received (its tracked changes, or a separate file) and with the current manuscript, locating each edited paragraph and marking it as applying cleanly or conflicting with a later change, and lists Word comments with their authors, without changing anything.
- 5 tests with synthetic records and Word files.

Not verified: real rounds and complex coauthor edits (moved paragraphs, tables, equations, fields), which the paragraph-based comparison reports for a manual check; Codex; Windows.

## MVP 9: connected paper hands-on

A synthetic Claude Code live run began on 2026-10-29 but was interrupted during idea deepening. Codex continued through analysis, a fictional title page and abstract, independent evidence checks, a five-page Word render, review response, revision and local checkpoints; a fresh agent recovered an interrupted revision in a separate copy. A history-free agent detected both planted defects in reconstructed excerpts, but the untouched original draft was not archived; the full path was split across agents, and actual-author and venue-policy checks remain unresolved. The optional live exercise is not a full pass. See the [complete-path record](acceptance/mvp-9-complete-path.md).

Complete-path run 2 (2026-10-29, maintainer request "完整路径你继续测试"): from a clean copy of commit `3f5e423`, `claude-haiku-5-5` ran all 16 stages in fresh sessions, with two interruptions and fresh resumes. The path reached readiness and a review response, but it did not pass: no resume used `paper-hands-on`, invented or unsourced claims appeared and were caught by the researcher or on resume, decision records were not superseded, the Word output is out of date, and `review.py` reports two problems. Defects D-5 to D-8 were open in the template (metadata omitted from the build, MinerU prescribed for Markdown letters, in-place revisions never complete, and the change-record check); D-4 is fixed in the working tree. D-5 to D-8 were fixed on 2026-10-29 (see [the fixes](#defect-fixes-from-complete-path-run-2-2026-10-29)). Details and verdicts: [complete-path record, run 2](acceptance/mvp-9-complete-path.md#run-2-complete-path-from-a-clean-copy-2026-10-29).

Status: MVP 9 accepted under the MVP 2-style gate on 2026-10-29; `paper-hands-on` passed [written review](acceptance/mvp-9-skill-review.md). The complete-path live exercise is optional follow-up and has not fully passed; acceptance does not verify untested platforms or real submission readiness.

- Skill `paper-hands-on` with its generated copy, coordinating the standalone skills without repeating their procedures.
- `scripts/status.py`: a read-only summary of the project's records and the gaps that suggest a next task, for recognizing the stage of a project in a fresh session; 2 tests.
- `scripts/tests/test_complete_path.py`: a scripted integration pass over the deterministic layer with synthetic, labeled material: a source imported and cited, an idea, a plan, a target decision, a venue note, a recorded run with a checked result, a manuscript that cites the source and reports the result, an audit record, a build and a release (where Pandoc is installed), a review round answered with a recorded change (which makes the audit stale), a major revision applied from a candidate, a saved version, and the status summary. It passes; it does not test the agent's judgment or a researcher's decisions.

## MVP 7: practical Git control and explicit backup

Follow-up (2026-10-29): a workspace-scope check incorrectly flagged the public `SCIVERSE_API_KEY` environment-variable name in the literature client as a secret. The detector now exempts that exact public declaration in that file while continuing to flag a separate credential assignment; a regression test covers both. This does not exempt credentials from version checks. The full script suite passed 146 tests on this Mac after the fix.

Status: the seven skills were accepted by review on 2026-10-28 ([skill review](acceptance/mvp-7-skill-review.md)). MVP 7 as a whole is not verified: no hosting service, Windows machine, or Codex session was used, and no live guided lesson was run.

Implemented after MVP 4, as part of the maintainer's request to implement every MVP from MVP 4 on; the planned order had placed MVP 7 directly after MVP 1.

- Skills `git-inspection`, `git-setup`, `git-save`, `git-compare`, `git-recovery`, `git-backup`, and `git-hands-on`, with generated copies. `project-onboarding` now reads the version history (read-only) and offers `git-setup` when it finds the template's history, an external copy, or research versions that the folder does not show.
- `scripts/versions.py`: `inspect` and `scope` (read-only, including the template's root commit, versions with research material, remotes and what they were seen to hold, unfinished operations, tracked secrets, and tracked files that ignore rules exclude); `init` and `identity`; `save` (exact scope, refusing secrets, files over 100 MB, and other prepared changes); `history` and `compare` (by area, renames, never-saved files, changed words); `retrieve` (to `.tmp/recovered/`) and `restore` (keeps the current content first); `untrack`; `practice` (a separate practice copy); `remotes`; and `backup`, which pushes only to a destination named in `requirements/privacy.md`, never with force, and checks the remote afterwards.

Verification observed: 13 tests in disposable repositories with an empty global Git configuration, on Python 3.12.9 and 3.9.6, including a clone of the backed-up copy and an unreachable destination. `inspect` on this repository reported its state without changing it.

Not verified: GitHub or another hosting service, sign-in, and repository visibility; Git for Windows; Codex; a guided lesson with a researcher.

## Export trial (2026-10-28)

Status: done; its decisions are recorded in the [export trial record](export-trial.md#6-decisions). Pandoc 3.12.1 and pandoc-crossref 0.3.26 were installed into `.tools/` from their official releases (checksums verified), and `@mermaid-js/mermaid-cli` 12.0.0 with npm, using the installed Chrome. Quarto was not trialed.

Observed on a synthetic manuscript: all 11 formulas, including one in a footnote, became separate native OMML equations with matching structure, and Word 16.114.2 rendered them correctly after the maintainer handled a Word dialog; citations and section, figure, table, and equation references resolved, and missing keys or labels produce warnings that a build can treat as failures; a reference document carried page size, margins, line numbers, fonts, and spacing. GitHub's Markdown API, given synthetic samples with the maintainer's permission, showed that a `{#eq:...}` label on the closing `$$` line stops GitHub from rendering the equation, while a label paragraph after a blank line keeps it; the maintainer adopted that form, attached at export by a project Lua filter. Mermaid flowcharts with Chinese labels, punctuation, and a long label rendered with mmdc.

Not exercised: editing an equation in Word, Word fields for figure and table numbers, the PDF route, Windows, and Quarto.

## Generated files in saved versions (2026-10-29)

Status: done and checked by tests; not tried with a real interrupted script or a real parser run.

The maintainer decided that the repository is for people without programming knowledge: saved versions stay clear and concise, and nobody has to guess what a generated file is for ([design plan Section 13](design-plan.md#13-version-control-and-ignore-policy), decision 25). Every file that the scripts write was checked against the ignore rules and against the README of its folder.

- **Newly ignored.** The hidden temporary names that scripts use next to their targets (`.writing-*`, `*.copying-*`, `*.replaced-*`, `*.part`; set in `ingestion/common.py`, `ingestion/library.py`, `export.py`, and `export/docx.py`), which a crash or a full disk can leave in a tracked folder; `.ipynb_checkpoints/`; and the parser's own output in `references/extracted/*/native/`, except its README. The parser output was the one bulky, non-paper file set that no script or skill reads. It replaces the earlier plan to keep it for provenance and structured retrieval, and it now exists only on the computer that ran the import. `document.md`, `assets/`, and `provenance.json` stay tracked.
- **Texts changed to match.** The generated README of each `native/` folder and of each extraction, `references/extracted/README.md`, the design plan (tree, Section 5, Section 13, decision 25), the MinerU integration record, and the scaffold entry above.
- **Gaps found in the explanations.** The optional `environment.txt` of a recorded run, and the `mapping.md`, `references.yaml`, `references.bib`, and `metadata.yaml` of an adopted manuscript, were described nowhere that a researcher would look. The run README, `code/runs/README.md`, and `inbox/imports/README.md` now name them. Every other generated record (`import.json`, `provenance.json`, `search.json`, `batch.json`, `checks.json`, `run.json`, `release.json`, `baseline.json`, `apply.json`, `profile.yaml`) was already named in the README of its folder.

Verification observed: 59 sample paths (21 script by-products, 26 paper and record files, 9 leftovers, 3 parser files) were checked against the new rules in a disposable repository, with no mismatch. Three new tests cover the rules: `TemplateIgnoreRulesTests` in `test_versions.py`, and two in `test_ingest.py` (a finished import leaves no temporary files; the parser output stays out of saved versions while its README stays in). The two ignore tests fail with the previous `.gitignore`. The full suite (150 tests), `check_readmes.py`, `check_capabilities.py`, `sync_skills.py --check`, and `research.py check` pass.

Not verified: the leftovers are known from reading the code, not from interrupting a script. The size of real parser output was not measured, because no real extraction exists on this machine. The cloud parser's version is set by the service, so importing a document again may not give the same output. A workspace saved before this change may still track `native/` files; `versions.py inspect` lists them as tracked files that the ignore rules exclude, and `untrack` removes them from later versions.

## Defect fixes from complete-path run 2 (2026-10-29)

Status: done and checked by tests; not tried in a fresh agent session. The maintainer asked to fix the open defects of [complete-path run 2](acceptance/mvp-9-complete-path.md#run-2-complete-path-from-a-clean-copy-2026-10-29) (“修复缺陷”, after D-5 to D-7 were offered as the fixes to make). Each is fixed in the layer that caused it; `AGENTS.md` and `CLAUDE.md` did not change. D-8 needed a decision on skill wording; the options were put to the maintainer, who chose the recommended one (“按推荐修”), and it is fixed the same way. The other model misses of the run were decided the same way (last bullet below).

- **D-5, metadata dropped from the build.** `scripts/manuscript.py` has `metadata_name`: the metadata file is the one the manifest names, else `manuscript/metadata.yaml` when it exists. The check, the preview (`assemble`), and the Word build all use it, and the build records it as an input. The build has a new check, “front matter” (`docx.front_matter` and `docx.compare_front_matter`): the title and each author that the effective metadata declares must be in the Word text, and each keyword in the file properties or the text (Pandoc writes keywords to the file properties only). In Pandoc 3.12.1 an author written as a mapping (`- name:` with `affiliation:`) is left out of the Word file, so such a build now fails and names the author. `submission-assembly` and `manuscript-writing` say where the title, authors, and keywords go, and that authors are plain names. A manuscript with no metadata still builds, and the check says that the Word file has no title.
- **D-6, MinerU prescribed for Markdown letters.** `review-ingestion` now says in its description, rules, and steps 2 and 3 that Markdown and plain-text letters need no converter, route, tier, or upload, and gives the command without `--route`. The script already handled this path; a test now covers it with no parser installed.
- **D-7, in-place revisions never complete.** `manuscript.py revision-complete` writes `revisions/<id>/closed.json` (outcome, date, in place or candidate, a note, and how many manuscript problems, open markers, and stale check records remained). It refuses while a candidate is staged but not applied or an application is interrupted. `revision-restore` writes the same record as abandoned. `revision-status` and `status.py` read it, so a closed revision is no longer reported as open. `manuscript-revision` says when to close a revision, and `revisions/README.md` and the README that `revision-start` writes describe the file.
- **D-8, a change recorded only in the revision.** A response cited C2, which was recorded only in `revisions/<id>/changes.md`; the check reported it, but its message did not say which `changes.md` it meant, and `review-response` called both files `changes.md`. Options put to the maintainer: say it plainly in the skill and the message (chosen), record it as a residual model risk, or let the check accept the revision's change numbers (rejected: it would mix two numbering spaces and break “each round keeps its own records”). `review-response` (steps 2 and 3 and the completion check) now names the round's own `changes.md` as the file that holds an entry for every change that answers an item, also when a revision made the change, with a `Revision:` line, and says that the `changes.md` inside the revision folder is a different file. The message of `review.py check` names the round's file and the remedy. What the check accepts did not change, and `manuscript-revision` was left alone, so the rule is written once.
- **The model misses of run 2, and the resume trigger.** The options were put to the maintainer, who chose the recommended handling (“按推荐处理”). The harness script shows that both interruptions were resumed with the same generic request, “我们继续上次的工作。”, which the description of `paper-hands-on` already named as a trigger (“to continue where the work stopped”), but at the end of a long sentence. The fresh Haiku sessions made no Skill call, and the first one then asked which item to do first and edited a finished note. The description now leads with the resume case, limited to a request that names no task and written to match in any language, and says that a request for one named task goes to that task's skill. The body of the skill, `status.py`, and every line number are unchanged, and the README of the skill gained one example request. The precedent is the readiness question: a description that led with its triggers raised the use of `environment-management` with Haiku from 1 of 3 to 8 of 10 samples (run 10). That raises the odds and does not guarantee the call, and it cannot be measured now, because live runs ended with the 2026-10-28 ruling. The written review of `paper-hands-on` was checked again ([second look](acceptance/mvp-9-skill-review.md#6-second-look-after-the-resume-trigger-change-2026-10-29)), and three line citations in it were corrected. Every other miss stays a recorded residual risk: an unsupported attribution and two unsourced sentences, a research question recorded before its confirmation, a kept idea not saved, a replaced decision not marked as superseded, summary values viewed before the plan was confirmed, repeated questions, a permission asked for a routine audit, Git history created without asking, and a finished evidence note edited after a resume. Their rules already exist in the skills, and the maintainer's ruling not to patch `AGENTS.md` stands. The deterministic levers (a session-start hook, the per-turn reminder, scripts that write the records) stay proposals for a separate decision.

Verification observed (macOS 26.6.2, Apple Silicon; Python 3.12.9; Pandoc 3.12.1): the full suite passes with 162 tests (150 before). Eleven of the 12 new tests fail against the code from before the fixes; the test for Markdown letters passes there too, because that defect was in the skill text. The extended scripted complete-path test also fails there. The skill copies match, the availability table matches the skills folder, and the README check (103 directories), the rule-form check, and the research-record check pass.

Not verified: how a model follows the changed text of `review-ingestion`, `manuscript-revision`, `manuscript-writing`, `submission-assembly`, `review-response`, and `paper-hands-on` (for the last, whether a model now calls the skill after a bare request to continue). The written reviews of `review-response` and `paper-hands-on` were checked again on 2026-10-29 and still pass ([second look at `review-response`](acceptance/mvp-8-skill-review.md#6-second-look-after-the-d-8-change-2026-10-29), [second look at `paper-hands-on`](acceptance/mvp-9-skill-review.md#6-second-look-after-the-resume-trigger-change-2026-10-29)); the written reviews of the other four were not redone, and the line citations in them refer to the text as reviewed; a build of a real manuscript whose metadata has other author forms, such as Word-converted ones; other Pandoc versions (the author behavior is observed only in 3.12.1); Windows; Codex.

Remaining: no defect of run 2 is open. Its other model misses stay recorded residual risks (last bullet above), and the deterministic levers stay proposals.

## Credential saves keep every other value (2026-10-29)

Status: done and checked by tests; the Windows lock code has not run on Windows. The maintainer asked to be sure that saving the key of one service never removes the key of another in `.env.local`.

Confirmed first. Saving B after A keeps A, replacing A keeps B, and removing one keeps the other: `write_value` in `scripts/credentials.py` rereads the file and drops only the lines of the name it is given, and an in-process check and the new end-to-end tests (which also pass on the previous code) show it. What was not safe was two saves at the same moment. All writers used one temporary file, `.env.local.tmp`, and read the old lines without any lock. In a reproduction with 12 processes saving different names at once, 11 of the 12 stopped with `FileNotFoundError` (`.env.local.tmp` had already been moved by another writer) and did not save their value, in every one of 15 rounds. Even without that error, two writers that start from the same old lines lose one value (a lost update). In normal use the window is a few milliseconds, but nothing guarded it.

The fix is in the same function:

- Reading, changing, and replacing the file happen under an exclusive lock on `.tmp/credentials.lock`, so writers take turns (`fcntl.flock` on macOS and Linux, `msvcrt.locking` on Windows). The operating system frees the lock when a process ends, so a crash leaves nothing stale. A writer waits up to 30 seconds and then stops with “Not saved: … Try again.” instead of overwriting. A file system that cannot lock is used without a lock, as before.
- Each write uses a temporary file of its own (`.env.local.*.tmp`, mode 600), flushed to disk before the replacement. If anything fails, that file is removed and the old `.env.local` stays as it was.
- `write_value` returns whether the name was set before, so that “Saved” and “Replaced” stay right when two saves overlap.

Verification observed (macOS 26.6.2, Apple Silicon; Python 3.12.9): the same reproduction on the fixed script lost nothing in 15 rounds of 12 writers and 10 rounds of 24 writers, with no errors. The credential tests pass (14, six of them new), and four of the six fail on the previous code: ten processes saving at once, a writer that waits for the lock, a failed replacement that left `.env.local.tmp` behind, and the lock file. The two sequential tests pass on the previous code too, because that part was already correct. The full suite passes with 168 tests (162 before), and the availability, README (103 directories), rule-form, research-record, and skill-copy checks pass.

Not verified: the Windows branch (`msvcrt.locking`), a cloud-synced or network folder where file locks may not work (the script then saves without the lock), and a very slow disk. Saving the same variable name twice replaces the value by design, which is how a token is renewed. Different services must therefore keep different names (`MINERU_API_TOKEN`, `SCIVERSE_API_KEY`), and `credentials.py status NAME` shows whether a name is already set.

## Open items affecting the order

- Result production for the complete-path test: decided on 2026-10-28 (see the decisions above).
- Verification resources: a Windows test machine matching the baseline (x64 or ARM64), access to Codex, and rights-cleared test fixtures. Without them, Windows and other unobserved behavior cannot be marked verified; MVP acceptance under the 2026-10-29 review gate is separate.
