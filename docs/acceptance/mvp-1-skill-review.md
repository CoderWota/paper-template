# MVP 1 Skill Review

Status: review completed on 2026-10-28 by the agent in the template repository. Result: `project-onboarding`, `environment-management`, `privacy-configuration`, and `constraint-maintenance` pass. The review found seven groups of text gaps and fixed them (section 5). A pass shows that the skill text meets the documented requirements. It shows nothing about behavior on Windows, on ARM64, or in Codex (section 7). MVP 2 landed on `main` while this review was written, so the review was checked again against the merged tree: the line numbers, the counts, and every row that depends on the availability table. The two MVP 2 skills, `source-ingestion` and `review-ingestion`, are not part of it.

## 1. Rule and pass criteria

On 2026-10-28 the template maintainer ruled that a skill passes acceptance when a review against its requirements passes, and that skills get no more live scenario runs. The ruling is recorded in the [MVP implementation guideline](../mvp-implementation-guideline.md#6-completion-record-for-each-mvp). This document is that review for the four MVP 1 skills.

The pass criteria were fixed before the review started:

- A skill passes when every requirement that can be judged by reading is Met after fixes. A gap is fixed in its own layer: skill text, description, script, table data, or a document. No sentence is added to `AGENTS.md` or `CLAUDE.md` to close a gap.
- A requirement that only a real platform, host, or service can show is listed in section 7. It is never counted as Met.
- A miss that a model made in a live run is a residual risk (section 6), not a review failure, unless the skill text lacks or blurs the required behavior.

## 2. Method

Read in full: the four `SKILL.md` files and their READMEs, `sources.md`, `report-template.md`, `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `requirements/README.md`, `research/decisions/README.md`, and the parts of `scripts/credentials.py` and `scripts/inspect_environment.py` that the skills rely on.

Requirement sources: [design plan](../design-plan.md) sections 9, 12, and 14; the MVP 1 entry and section 5 of the [MVP implementation guideline](../mvp-implementation-guideline.md); the [agent interaction specification](../agent-interaction.md); [rule placement](../rule-placement.md); and "Writing a skill" in [`.agents/skills/README.md`](../../.agents/skills/README.md).

Line numbers in the matrices point to the files after the fixes of section 5. `SKILL` means the `SKILL.md` of the skill under review.

Mechanical checks, run on 2026-10-28 after the fixes. All pass:

| Command | Result |
| --- | --- |
| `python3 scripts/sync_skills.py --check` | Skill copies match: 6 packages (the four reviewed here and the two MVP 2 packages) |
| `python3 scripts/check_capabilities.py` | The availability table matches the skills folder |
| `python3 scripts/check_readmes.py` | 43 project directories |
| `python3 scripts/check_requirements.py` | The writing rules have the required form |
| `python3 -m unittest discover -s scripts/tests` | 49 tests, OK |
| Search for `/Users/`, `scratchpad`, and the maintainer's name in all six skills, `AGENTS.md`, and `CLAUDE.md` | No match |

Runs 1 to 13 on Claude Code are history (see the [checklist](mvp-1.md) and the [implementation status](../implementation-status.md)). They showed which gaps to look for. They do not decide the result.

## 3. Requirements that apply to every skill

| ID | Requirement | Source | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| CC-1 | One canonical copy per skill in `.agents/skills/`, and generated, committed Claude copies that match | `AGENTS.md` L93; skills README L3 | Met | `sync_skills.py --check` |
| CC-2 | `name` equals the directory; one-line `description`; only the fields both hosts support | skills README L18 | Met | Lines 1 to 4 of each `SKILL.md`; the same script validates the frontmatter |
| CC-3 | Skill text is in English | `AGENTS.md` L88 | Met | All `SKILL.md` and README files; the quoted Chinese words (constraint-maintenance L48, L49) are examples of what a researcher says |
| CC-4 | Each package has a README for people that links to `SKILL.md` | skills README L7 to L10 | Met | project-onboarding README L17, environment-management README L11, privacy-configuration README L14, constraint-maintenance README L13 |
| CC-5 | A skill does not copy shared rules (question form, confirmation, README contract) | skills README L19; rule placement, principle 2 | Met after F-2 | project-onboarding L13 now points to `AGENTS.md`. constraint-maintenance L13 and L14 restate only the part of the rules that is the subject of that skill |
| CC-6 | No dependency on a maintainer-only path | guideline section 5, row "Codex/Claude parity" | Met | The search in section 2 |
| CC-7 | No MVP number, and no planned skill, is offered to the researcher as available | `AGENTS.md` L16, L17 | Met after F-3, F-4, F-6 | project-onboarding L45; constraint-maintenance L27, L37; `sources.md` L27 |
| CC-8 | The availability table matches the skills folder | `AGENTS.md` L27 | Met | `check_capabilities.py` |
| CC-9 | `CLAUDE.md` is a one-line import of `AGENTS.md` | design plan L422 | Met | `CLAUDE.md` L5 |
| CC-10 | Every project directory has a useful English README | guideline MVP 1, L87 | Met | `check_readmes.py` |
| CC-11 | The scripts that the skills rely on have automated tests | guideline section 5 | Met | `scripts/tests/`: credentials (L58, L89, L98), records, workspace scripts |
| CC-12 | The description routes the skill from ordinary language, with a "Use when" or "Use during" clause | `AGENTS.md` L93; design plan L416 | Met | L3 of each `SKILL.md` |

## 4. Requirements by skill

### 4.1 project-onboarding

| ID | Requirement | Source | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| PO-1 | Establish the goal, language, immediate needs, and initial workspace; end with settings and a clear next action | design plan L443; hands-on L33 | Met | L8, L37 to L49, L80 to L81. The goal question (L43) and the single next action (L81) cover the immediate need; a deadline or venue is recorded when the researcher gives it (L69) |
| PO-2 | One question at a time, with a reason and a recommendation | `AGENTS.md` L50; interaction spec L29 to L33 | Met | L13, L60 |
| PO-3 | Record only stated or confirmed answers; no inferred preference | `AGENTS.md` L18, L60, L61 | Met | L14, L98 |
| PO-4 | The goal is in the researcher's exact words; no invented research question | `AGENTS.md` L20 | Met | L45 |
| PO-5 | Records are in the interaction language | `AGENTS.md` L87 | Met | L16, L67, L80 |
| PO-6 | Initialization can finish with setup explicitly deferred | design plan L629 | Met | L53, L63, L70 |
| PO-7 | A declined or postponed offer is not a requirement | `AGENTS.md` L18 | Met | L70, L76, L100 |
| PO-8 | Cloud processing is recorded only after its scope is confirmed, and never silently | `AGENTS.md` L82; design plan L621 | Met | L61, L70 |
| PO-9 | Inspect the computer first; install nothing during onboarding | design plan L611 | Met | L55 |
| PO-10 | Never delete, move, or overwrite a workspace that holds work; ask whether to continue or start a new paper; a new paper uses a fresh copy | guideline MVP 1, L92 | Met after F-1 | L15, L33, L85 to L93. A finished onboarding counts as holding work (L33), and the new-paper branch changes no file (L89) |
| PO-11 | The final report lists the settings, the deferred items, and exactly one next action | `AGENTS.md` L99 | Met | L81, L99 |
| PO-12 | Offer the privacy check; change no account setting without consent | `AGENTS.md` L18 | Met | L74 to L76 |
| PO-13 | A capability that is not available is not promised | `AGENTS.md` L17 | Met after F-3 | L45 says that idea development is not available; L55 and L72 name available skills only |

### 4.2 environment-management

| ID | Requirement | Source | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| EM-1 | Inspect the operating system, processor, memory, storage, and tools before changing anything; check architecture compatibility | design plan L611 | Met | L13, L18, L20 to L22, L32; `inspect_environment.py` L106 to L176 (processor and emulation, memory, interpreters, tools, workspace path) |
| EM-2 | The inspection changes nothing | guideline MVP 1, L90 | Met | L22; `inspect_environment.py` L2, and the script contains no write call |
| EM-3 | Reading and writing Markdown never needs a tool; a missing converter blocks nothing unrelated | design plan L609, L613 | Met | L14, L15, L30 |
| EM-4 | No GPU, local model, Docker, or WSL for basic work; a cloud route does not force local inference | design plan L609, L613 | Met | L14, L47 |
| EM-5 | Reuse compatible tools, record versions, and never replace a working global install | design plan L615, L617 | Met | L13, L46, L92 |
| EM-6 | A project `.venv` is called directly; `uv` is optional; heavy tools have their own environment | design plan L615 to L617; `AGENTS.md` L79 | Met | L45 to L47 |
| EM-7 | Guidance when Python is absent, without depending on Python; per-user installation; no administrator rights by design | design plan L619 | Met | L24, L39, L86, L88 |
| EM-8 | Windows paths with spaces or non-ASCII characters, the Store alias, and cloud-synced folders | design plan L611 | Met | L22, L24, L34, L86, L90 (behavior on Windows is not covered, section 7) |
| EM-9 | An install, upgrade, or removal needs explicit consent | `AGENTS.md` L49 | Met | L12, L40 |
| EM-10 | A credential is collected only for a service the researcher chose; an AI subscription does not imply an API key; setup can wait | design plan L629 | Met | L52 to L54, L91 |
| EM-11 | Masked entry on the researcher's computer; no value in chat, arguments, or logs; Git exclusion before writing; a plain statement that the file is not encrypted | design plan L631 to L633; guideline MVP 1, L99, L100 | Met | L8, L59 to L74; `credentials.py` L88 to L93 (mode 600), L103 to L121 (refuses when Git could track the file), L127 to L154 (one-time page on 127.0.0.1, secret path, password field), L270 to L281 (status shows the length only); `test_credentials.py` L58, L89, L98 |
| EM-12 | The value reaches the consuming process through the intended loader | design plan L633; guideline MVP 1, L99 | Met | L70; `credentials.py` L65 (`load_env_local`), L291 to L309 (`run`) |
| EM-13 | A non-content check, or "unverified until the first authorized job"; one status; machine facts stay out of shared requirements | design plan L635 | Met | L78 to L80 |
| EM-14 | A pasted secret is not repeated or stored | `AGENTS.md` L23 | Met | L72 |
| EM-15 | Availability comes from the table; the `python` name has a fallback on macOS, Linux, and Windows | `AGENTS.md` L17, L95; rule placement, principle 3 | Met after F-5 | L22, L54, L56 |
| EM-16 | Page texts and reports are in the researcher's language | `AGENTS.md` L16, L87 | Met | L60, L79 |

### 4.3 privacy-configuration

| ID | Requirement | Source | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| PC-1 | Identify the product, sign-in route, account type, model provider, and processing route; ask only for what is missing; never ask for a password, key, or identifier | design plan L645 | Met | L13, L20 to L28 |
| PC-2 | Use the current official documentation for the exact route; keep training, retention, upload, telemetry, and feedback apart | design plan L646, L659 | Met | L15, L16, L30 to L36; `sources.md` L5 to L13 |
| PC-3 | Explain each control and its scope, including that an account setting can affect other projects | design plan L647 | Met | L12, L40 to L42 |
| PC-4 | Change a setting only with explicit consent; keep it reversible; stop at administrator-only settings | design plan L647 | Met | L46 to L50 |
| PC-5 | Give each control one evidence type; never call a setting verified because instructions were shown | design plan L648; guideline MVP 1, L100 | Met | L52 to L64 |
| PC-6 | Keep a minimal, redacted report on this computer, outside Git, with service, date, evidence, sources, and next steps | design plan L649 | Met | L68; `report-template.md` L5 to L27; `.gitignore` L9 |
| PC-7 | Persist only confirmed choices in `requirements/privacy.md` | design plan L649; `AGENTS.md` L18 | Met | L69, L70 |
| PC-8 | State what an opt-out does not do: earlier data, safety review, submitted feedback, and opt-in programs | design plan L646, L655 | Met after F-6 | L35, L44; `sources.md` L10, L11 |
| PC-9 | A telemetry opt-out, a deleted session, or a short retention period is not a training opt-out | design plan L659 | Met | L15 |
| PC-10 | A MinerU cloud service is a separate processor with an unknown policy until checked | design plan L657 | Met | L26, L75; `sources.md` L25 to L35 |
| PC-11 | Send no manuscript as a test; do not change the maintainer's own settings during template development | design plan L641 | Met | L13, L17 |
| PC-12 | Cover Claude (consumer and commercial), ChatGPT and Codex (personal and managed), and the OpenAI API, including the separate Codex "Include environments" setting | design plan L653 to L656 | Met | `sources.md` L9 to L13, L19 to L21. The pages are dated 2026-10-26, and the skill requires a fresh read (L16) |
| PC-13 | No key or upload talk for a service that is not available | `AGENTS.md` L17 | Met | L18, L70 |
| PC-14 | The report is in the researcher's language | `AGENTS.md` L87 | Met | L68; `report-template.md` L3 |

### 4.4 constraint-maintenance

| ID | Requirement | Source | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| CM-1 | Persist only verified, researcher-confirmed requirements, each with a scope | design plan L446; `AGENTS.md` L60 | Met | L8, L13 to L15, L39 |
| CM-2 | Never save an inferred preference, including in notes, state, and the application's memory | guideline MVP 1, L89; section 5, row "Confirmed rules only" | Met | L14, L28, L88 |
| CM-3 | An explicit instruction is confirmation within its scope; no second approval | `AGENTS.md` L18; interaction spec L21 | Met | L13, L24 |
| CM-4 | A lasting rule differs from a one-time edit; for a one-time edit that conflicts with a rule, say that no rule changed and offer to change it | `AGENTS.md` L21 | Met after F-4 | L24 to L26, L49 |
| CM-5 | A replacement is named; a real conflict gets one question with a recommendation; clear "replace" or "switch" words need no question | `AGENTS.md` L21, L62; interaction spec L19 to L23 | Met | L48, L73, L74 |
| CM-6 | A rule has a scope, a date, and the researcher's exact words in quotation marks; examples and exceptions come only from the researcher; the layout is checked | `AGENTS.md` L20; rule placement, principle 4 | Met | L17, L53 to L67, L91, L92; `check_requirements.py`; `test_records.py` L92 to L127 |
| CM-7 | Each requirement goes in its own file: writing rules, languages, privacy, output profiles | `requirements/README.md` L7 to L12 | Met | L32 to L41 |
| CM-8 | Advice, decisions, and active requirements stay distinct | guideline section 5, row "Advice, decisions, and active requirements" | Met | L16, L27, L75; `research/decisions/README.md` L3 |
| CM-9 | A requirement change never edits manuscript text; the affected passages are listed; only available actions are offered | `AGENTS.md` L17, L22 | Met | L77 to L79, L93 |
| CM-10 | Rules are written in the interaction language; the labels are one fixed form that the check reads | `AGENTS.md` L87, L88; `requirements/README.md` L22; rule placement, principle 4 | Met after F-4 | L17, L53 |
| CM-11 | A consequential research choice gets a decision record; a writing rule or a language setting does not | `AGENTS.md` L19; `research/decisions/README.md` L3 | Met after F-4 | L16, L75, L90 |
| CM-12 | Requirements survive a fresh session | design plan L678 | Met | The rules live in `requirements/` (L8), and `AGENTS.md` L54 and L55 make every session read them |
| CM-13 | Routing covers goal changes, rule statements, questions about rules, and requests that conflict with a rule | `AGENTS.md` L93 | Met | L3 |
| CM-14 | No unavailable skill is offered | `AGENTS.md` L17 | Met after F-4 | L27, L37 |

## 5. Gaps found and fixed

| ID | Gap | Fix | Layer |
| --- | --- | --- | --- |
| F-1 | The case table of project-onboarding did not say that an initialized project is a workspace that holds work, so the "continue or new paper" question could be skipped. The "new paper" branch said "change nothing here" while `AGENTS.md` "Finishing work" says to update the state, and the live run wrote a note to `state/current.md` | Table row L33 names the initialized project. L89 says that no file changes, `state/current.md` included, because the new paper's state belongs to its own copy | Skill text |
| F-2 | project-onboarding L13 copied the question form of `AGENTS.md` | L13 points to `AGENTS.md` and keeps only the skill's own limit, one sentence of reason | Skill text |
| F-3 | project-onboarding L45 named two planned skills | L45 says that idea development is not available yet | Skill text |
| F-4 | constraint-maintenance told the agent to translate the labels, but the layout is English and the check reads only Chinese and English labels. Step 5 told the agent to link a decision record that a writing rule does not have. Two planned skills were named as routes. The one-time-edit row did not point to the conflict case | L53 fixes the English labels and keeps the values in the interaction language. L75 links a record only when one exists. L27 and L37 and the README mark the planned skills as not available. L25 points to step 3 | Skill text |
| F-5 | environment-management checked skills and scripts to decide whether a credential is needed, while the table is the single source. The credential commands had no fallback for the `python` name | L54 points to the "Available now" table. L56 gives the `python3` and `py -3` fallback | Skill text |
| F-6 | privacy-configuration did not list opt-in programs among the exceptions. `sources.md` named an MVP number | L35 adds "an explicit opt-in program". The MVP 2 work rewrote the document-processing section of `sources.md` (L25 to L35), which no longer names an MVP number | Skill text; the source note was rewritten in the MVP 2 work |
| F-7 | The example sentence in environment-management L54 said "importing documents is not available yet". With `source-ingestion` available (MVP 2), that example became false | L54 now uses a service that is not available yet, without naming a capability that will change | Skill text |

No script, no table row, and no sentence of `AGENTS.md` or `CLAUDE.md` changed. The Claude copies were regenerated with `sync_skills.py`.

## 6. Residual risks (model behavior)

These misses were seen in live runs with Haiku. The skill text asks for the behavior, so they are not review failures. They are not removed by this review.

- Routing. The readiness question reached the inspection in 14 of 21 samples (runs 10 to 13). A cloud wish loaded no skill in 6 of 6 samples (runs 11 and 13) and was not noted in `state/current.md`. A one-sentence rewrite against a saved rule (E6) loaded no skill in 3 of 3 samples, and its reply omitted "no rule changed" and the offer to change the rule, which `AGENTS.md` L21 and constraint-maintenance L49 require.
- Variance. An ambiguous replacement of a rule was applied at once, without the question, in 1 of 3 samples (run 13). A readiness report omitted the recommended next step in 2 of 2 samples.
- Language. 2 of 83 notes between tool calls were English in run 13, and the replies of the credential flow were Chinese in that run.
- Levers that remain, not applied, each a design decision: a host hook for the language reminder and for the form check, scripts that write the records, and a machine-readable place for the interaction language ([rule placement](../rule-placement.md)).

## 7. Not covered by this review

These stay unverified and must not be advertised as working.

- Windows and ARM64: onboarding without a preinstalled Python, paths with spaces and non-ASCII characters, and the credential page on Windows.
- Codex: discovery of `.agents/skills`, loading of `AGENTS.md`, and parity with Claude Code.
- The state of any provider setting in a real account. The review checks that the skill asks for evidence; it cannot observe an account.
- ASD-STE100 compliance of English questions. The official dictionary is not bundled, and a review of sentence length alone is not an STE review. The clarity of Chinese questions was only observed in live runs, not reviewed against a standard.
- The live mineru.net route and its terms. The terms state neither training use nor retention, so both stay unknown ([MinerU integration](../mineru-integration.md)).
- Whether a particular model follows the text (section 6).

## 8. Verdict

| Skill | Verdict |
| --- | --- |
| `project-onboarding` | Accepted by review, 2026-10-28 |
| `environment-management` | Accepted by review, 2026-10-28 |
| `privacy-configuration` | Accepted by review, 2026-10-28 |
| `constraint-maintenance` | Accepted by review, 2026-10-28 |

"Accepted by review" does not mean verified on a platform. MVP 1 as a whole stays open for the items of section 7 and for the other MVP 1 deliverables that are not skills.
