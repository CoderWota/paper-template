# Implementation Status

Agent-maintained record of what has actually been implemented and verified, one entry per MVP from the [MVP implementation guideline](mvp-implementation-guideline.md). A capability counts as working only after its acceptance evidence has been observed. The presence of a directory, a README, or a SKILL.md is not evidence.

Updated: 2026-10-26.

## Summary

| MVP | Researcher-visible outcome | Status |
| --- | --- | --- |
| 1 | Usable project and confirmed memory | In progress: scaffold, adopted AGENTS.md, skill copy script, and all four skills implemented. Claude Code runs 1 to 3 are done: by each row's latest result, 15 of 20 checklist rows pass, 3 fail on minor points (D1, D2, G1), and 2 were not run. Rows that a later run did not repeat keep their earlier result. Codex and Windows have not been run, so nothing is verified |
| 2 | Flexible intake and MinerU batch ingestion | Planned |
| 3 | Searchable literature and traceable evidence | Planned |
| 4 | Ideas, impact, journal choice, and feasible research plans | Planned |
| 5 | Evidence-based writing, audit, and major revision | Planned |
| 6 | Template-driven layout and readiness | Planned |
| 7 | Practical Git control and explicit backup | Planned |
| 8 | Review rounds and coauthor reconciliation | Planned |
| 9 | Connected paper hands-on and release candidate | Planned |

Execution order (revised 2026-10-26): 1 → 7 → 2 → 3 → 4 → 5 → 6 → 8 → 9, with the export trial running alongside MVP 7; see the [MVP implementation guideline](mvp-implementation-guideline.md#3-mvp-overview-and-dependencies). The export trial is planned.

The four MVP 1 skills are implemented and have had three acceptance passes on Claude Code; none is verified. No end-to-end test has been run.

## MVP 1, partial increment: workspace scaffold

Status: in progress. This increment is narrower than MVP 1 and does not meet its acceptance evidence.

Request: the template maintainer asked to initialize the Git repository, implement the basic project structure described by the design documents, write project documents in English, and delete the Chinese translations (2026-10-26).

Implemented:

- A local Git repository on branch `main`, with no remote.
- `.gitignore` by role, following [design plan Section 13](design-plan.md#13-version-control-and-ignore-policy): credentials (`.env*` except `.env.example`), `.local/`, environments, caches, `.tmp/`, rebuildable previews, Claude Code personal settings, and editor, office, and operating-system artifacts. Documents, templates, and images are not ignored by type. `.gitattributes` normalizes text line endings.
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

Method. The template-repository agent acted as the researcher in headless Claude Code sessions on a disposable clone of commit `51f93e7` (no Git remote), with the scripted answers of the [MVP 1 checklist](acceptance/mvp-1.md). Environment: Claude Code 2.1.170, model `claude-sonnet-5-5`, macOS 26.6.2 on Apple Silicon (16 GB), Python 3.12.9. The run used 37 session logs and 189 agent turns, about nine minutes of agent time, and about $4.23 in API-equivalent cost. The logs stay in the maintainer's scratchpad, not in the repository.

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
| D-2 | Low | Open | The readiness report did not say that reading and writing work without the converter, and its closing message bundled two questions. In runs 2 and 3, two of four samples skipped the inspection script. | In `environment-management`, state what still works, run the inspection first, and ask one question. |
| D-3 | Medium | Partly fixed (runs 2 and 3) | The agent treated PDF import as available once MinerU is installed, and implied that a key would soon be entered for parsing. No ingestion skill exists yet. | Applied: `AGENTS.md`, "Skills", says that only the skills in `.agents/skills/` exist and that the agent must say so plainly when a task needs a missing skill, while it can still help in conversation. Result: asked directly about importing PDFs (D1), the agent said that no import skill exists in 4 of 4 samples; talking about cloud parsing and keys (D2), in 1 of 7. Proposed addition: in `environment-management`, step 5, research or collect a credential only when a skill or script in this workspace uses it; when none does, say so plainly and defer the credential. |
| D-4 | Low | Open (not seen in runs 2 and 3) | The final onboarding report named `inbox/imports/` as the place for documents. That folder holds import records; documents go in `inbox/`. | Name `inbox/` in the last step of `project-onboarding`. The report no longer lists import as an example next action. |
| D-5 | Low | Open | `project-onboarding` detects an interrupted onboarding from `state/current.md`, which it updates only at the end. Detection worked through the status line in `requirements/project.md`, in every run. | Detect through `requirements/project.md`, or update `state/current.md` after the first answer. |
| D-6 | Medium | Fixed in run 2 | When recording the British-spelling rule, the agent added an exception (quotations, proper names, and bibliography titles keep their spelling) that the researcher had not stated. | Applied: `constraint-maintenance` adds an example or an exception only when the researcher gave or confirmed it. Run 2, two samples: none recorded; one run asked whether the researcher wanted an exception. |
| D-7 | Low | Open | "改用美式拼写" (switch to American spelling) replaced the old rule without a question. That follows `AGENTS.md` (a clear instruction is confirmation) but not step 3 of the skill. | Align the skill: replace without asking when the instruction itself says to replace or switch; ask when the relation is unclear. |
| D-8 | Medium | Fixed in run 2 | After a confirmed change of the research goal, the agent rewrote the manuscript introduction, both times unasked. | Applied: a new step in `constraint-maintenance` lists the manuscript passages that the change affects and asks before editing them. Run 2, two samples: the introduction stayed unchanged until the answer, and both answers worked. |
| D-9 | Low | Open | In E6 the reply rewrote the sentence before it asked whether the request was a one-time exception. Nothing was saved. It happened again in run 2. | Ask first, as step 3 says, or accept the combined reply. |
| D-10 | Low | Fixed in run 3 | Onboarding recorded the declined privacy check in `requirements/privacy.md` as a confirmed item, with the added sentence "do not check or change any account setting without the researcher's consent". The researcher had said only "not now" to the offer. | Applied: `project-onboarding` notes a declined or postponed offer only in `state/current.md`, and does not write it to `requirements/privacy.md`. Run 3, two samples: `privacy.md` stayed unchanged and the deferral is only in `state/current.md`; one sample gave the reason. |
| D-11 | Low | Fixed in run 3 (few samples) | Replies to the researcher named internal terms: "MVP 2", the skill id `source-ingestion`, and "想法发展技能" (the idea-development skill). | Applied: `AGENTS.md`, "Skills", asks the agent to describe a missing capability in the researcher's own terms and not to use MVP numbers or skill ids unless asked. Run 3: none of 36 messages used them (3 of 49 before). |
| D-12 | Low | Applied; not shown to work | The sentence before the first tool call of several turns was in English, although the researcher wrote Chinese. Only the records are covered by the language decision. | Applied: `AGENTS.md`, "Language and formats", says that the rule covers the short notes between tool calls. Run 3: English-only notes 2 of 16 (12%), against 4 of 25 (16%) before. Both are the first note of a session, written right after the agent loaded an English skill. Proposed addition: put the same rule in the rules of each skill. |

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

## Remaining for MVP 1

All four MVP 1 skills have first implementations, and runs 1 to 3 on Claude Code are complete. Remaining:

- Decide on the open defects (D-2, D-4, D-5, D-7, and D-9) and on the two additions that run 3 proposes: for D-3, a credential step that requires an existing integration, and for D-12, the language rule inside each skill. Fix those that are accepted, and repeat the affected scenarios.
- Repeat the whole checklist on Claude Code after those fixes, because `AGENTS.md` and two skills changed after run 1.
- Run the checklist in Codex, which is not installed on the maintainer's computer yet, and on the Windows baseline. Recreate the Codex test copy first: it still holds the state before the fixes.
- Run the scenarios that the runs could not exercise: the interactive question tool, missing Python or tools, onboarding in English, and an account control that the researcher can read.
- Start the read-only MinerU service research.
- Implement the English question checks against the official ASD-STE100 issue, and the clarity review for questions in other languages. The standard and its dictionary are not bundled with the template; they need access under the publisher's terms.

The [MVP 1 acceptance checklist](acceptance/mvp-1.md) holds the scenarios and the results table. The disposable test copies have no Git remote: `/Users/wota/Projects/paper-template-mvp1-test-claude` (run 1), `/Users/wota/Projects/paper-template-mvp1-test-claude-r2` (run 2), and `/Users/wota/Projects/paper-template-mvp1-test-claude-r3` (run 3) each hold the changes of their run, and `/Users/wota/Projects/paper-template-mvp1-test-codex` is untouched, cloned from `51f93e7`, so it predates the fixes.

## Open items affecting the order

- Result production for the complete-path test: no MVP yet owns producing actual research results. Decide before MVP 9, preferably before MVP 4.
- Verification resources: a Windows test machine matching the baseline (x64 or ARM64), access to Codex, and rights-cleared test fixtures. Without them, MVP 1 and MVP 2 can be implemented but not marked verified.
