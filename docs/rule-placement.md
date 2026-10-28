# Rule Placement and Root Causes

Status: design principle, adopted by the template maintainer's instruction on 2026-10-27 ("solve the root, not the patch"). Implementation and test evidence are in [implementation status](implementation-status.md).

## Why this document exists

Acceptance runs 1 to 5 found fourteen defects (D-1 to D-14), and runs 6 to 9 found seven more (D-15 to D-21). Most were fixed by adding a sentence to the file where the failure was seen. The fixes worked for the sampled cases, but they made the rules longer and duplicated. The language rule ended up in four skills and in `AGENTS.md`, and it still failed in the first note of a session. The availability rule lived in one skill, so a cloud-parsing request, which loaded another skill, bypassed it. This document states where a rule must live, and what caused each family of defects.

## Where a rule lives

| Layer | When it is loaded | What it holds | Example |
| --- | --- | --- | --- |
| `AGENTS.md`, standing rules | Every session, before any task | Rules that apply at every decision point | "Say that a capability is available only if the table lists it." |
| `AGENTS.md`, availability table | Every session | The single list of what works now; a script checks it against the skills folder | "Import documents: not available yet" |
| Per-turn reminder (host hook, where supported) | Before each prompt | The interaction language recorded for this project | "Interaction language: Chinese" |
| Skills | When invoked | Procedures for one task, without copies of standing rules | The onboarding steps |
| Records and scripts | When written or run | Facts and their form, checked mechanically | A requirement needs a scope and a quoted source |

Principles:

1. **Load before the decision.** A rule must sit in a layer that is loaded before the decision it governs. A rule in a skill does not protect a path that does not load that skill (D-3).
2. **Write a rule once.** Copies in several skills drift, and they do not add protection. The language rule was copied into four skills and did not hold in the first note of a session (D-12, D-14).
3. **Facts that change live in data.** What exists is a fact. It is checked against the file system by a script, not described in prose that the model must recall (D-3).
4. **Records have a checkable form.** A requirement needs its scope and a quoted source. Examples and exceptions need a quotation, so that none can be invented (D-6, D-10).
5. **Reinforce at generation time when the host allows it.** A rule that governs the first note of a turn cannot rely on a file loaded at session start. Where the host supports it, the reminder goes in before each prompt (D-14).
6. **Freeze expectations before a run.** A behavior claim is accepted only with samples from fresh sessions. Expectations change only as recorded decisions, never to match a result (E4 and E6 were revised after run 5).
7. **Narrow each trigger to its purpose.** A rule that fires too broadly writes records that need none (D-18) and blocks questions that the researcher must answer (D-16). State the purpose and the exclusions in the rule, and re-run the neighbouring scenarios after each change.
8. **Do not patch the contract to pass a test.** `AGENTS.md` and `CLAUDE.md` state general rules. A failing scenario is traced to the layer that causes it (a skill description, a skill procedure, a script, the data in the availability table, or the expectation itself) and fixed there. A new sentence in `AGENTS.md` needs a reason that holds without the failing case. This is the maintainer's ruling of 2026-10-27. In D-17, a sentence added to `AGENTS.md` hid a stale step in `constraint-maintenance`.

## Root causes by family

| Family | Defects | Root cause | Fundamental fix | Status |
| --- | --- | --- | --- | --- |
| Availability | D-3; D-2 and D-11 in part; D-16 and D-17 (runs 7 to 9) | Availability was inferred from prose, and the rule sat in a skill that a cloud request did not load. A skill step written before the table (Step 6 of `constraint-maintenance`) still offers "update now" (D-17), and the readiness question does not name a table row (D-16) | Availability table in `AGENTS.md`, checked against the skills folder by `scripts/check_capabilities.py`; skill steps offer only what the table lists, and the row texts and skill descriptions name what each row covers (applied in run 10) | Table applied and checked by script; the patch sentences are out of `AGENTS.md`; D-17 is fixed at its cause for the skill path, and D-16 reaches the inspection in 8 of 10 Haiku samples |
| Record form | D-20, D-21 (run 9) | The layout is prose, its labels follow the interaction language, and the check script is part of no procedure | A script that writes the record, or a procedure that runs the check, whose message lists the accepted labels (applied in run 10: the skill runs the check) | Fixed in the Haiku samples taken; label drift stays possible |
| Language | D-1, D-12, D-14 | The rule was copied into skills and restated in `AGENTS.md`; the model's default for process notes is English; the first note precedes any skill rule | One standing rule in `AGENTS.md`; per-turn reminder through a host hook | Rule consolidated; reminder prototyped; adoption pending |
| Confirmation and records | D-6, D-10, D-13; D-9 in part; D-15 and D-18 (run 7) | "A clear instruction is confirmation" was read as covering wishes, offers, and invented examples; records had no form check. The record duty sat in a skill that a goal change did not load (D-15), and its trigger listed too much (D-18) | Confirmation defined as a clear answer to a scope question; record form checked by `scripts/check_requirements.py`; one standing rule for decision records with a narrow scope, which the skill links to | Definition applied; checker added; D-15 and D-18 fixed in run 7 samples |
| Side effects | D-8 | No separation between requirement records and manuscript text | Standing rule: a requirement change never edits manuscript text | Applied |
| Procedure order | D-2 (inspection skipped in some samples); D-7 and D-9 (question and edit order) | Procedures are prose that the model can reorder | Deterministic steps move into scripts; question order stays a tested behavior | Residual |
| Structure and state | D-4, D-5 | Similar names (`inbox/` and `inbox/imports/`); onboarding state split across two files | One state file; rename of the import records folder proposed | Wording fixed; rename proposed |
| Testing | Expectations of E4 and E6 changed after run 5; one to three samples per claim | Expectations were edited to match results | Freeze expectations before a run; record each change as a decision; take more samples for behavior claims | Adopted in this document |

## Residual risks

- A model can still ignore a standing rule. Each rule is accepted only with samples from fresh sessions.
- The per-turn reminder depends on the host. It is a Claude Code mechanism; Codex has no verified equivalent yet, and the reminder cannot run on a machine without Python unless the command is written to fail quietly.
- The availability table is maintained by the template maintainer. `scripts/check_capabilities.py` fails when the table and the skills folder disagree, so drift is visible.
- A sentence in `AGENTS.md` can mask a defect in a skill (D-17): the contract wins over the skill, so the symptom disappears while the skill stays wrong. Skills need review against the contract and the table.
- Even with each cause fixed, Haiku still misses a routing or a record rule in a few samples (the readiness question in about 1 of 5, the goal-change skill in 1 of 7, a record in English once). No sentence is added to `AGENTS.md` for this. The remaining levers are deterministic: a hook that runs the form check, and scripts that write the records.
- A change to a standing rule can move a neighbouring behaviour in either direction (D-16, D-18). Run 7 found this twice, and a single sample shows little, so each change needs the neighbouring scenarios re-run.
