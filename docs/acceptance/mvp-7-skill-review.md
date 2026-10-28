# MVP 7 Skill Review

Status: all seven Git skills passed written review on 2026-10-28 under the gate used for MVP 2 to MVP 4. `scripts/versions.py` passes 13 tests in disposable repositories on Python 3.12.9 and 3.9.6. No hosting service, Windows machine, or Codex session was exercised; see section 6.

## 1. Rule and pass criteria

Fixed before the review, as in the [MVP 4 review](mvp-4-skill-review.md#1-rule-and-pass-criteria): each readable requirement must be met by the skill text with its lines; a requirement carried by the script needs a test; platform- or service-only behavior stays unverified; a model's misses are residual risks.

## 2. Method and evidence

Read the seven `SKILL.md` files and READMEs, `scripts/versions.py`, `scripts/tests/test_versions.py`, and the changed step of `project-onboarding`, against MVP 7 in the [implementation guideline](../mvp-implementation-guideline.md#mvp-7--practical-git-control-and-explicit-backup), [design plan](../design-plan.md) sections 9 (version-management tasks and boundaries) and 13 (version control and ignore policy), the [hands-on design](../hands-on.md) Git section, and `AGENTS.md`.

The tests run Git with an empty global configuration, so the maintainer's settings cannot affect them, in temporary folders whose names contain spaces and non-ASCII characters. A bare repository on this computer stands in for an external destination.

| Check | Result |
| --- | --- |
| `python -m unittest scripts/tests/test_versions.py` | 13 tests, OK (Python 3.12.9 and 3.9.6) |
| Full suite, skill copies, availability table, READMEs | Pass; see the implementation status for the counts |
| `python scripts/versions.py inspect` on this repository | Reported 39 versions, the template's own history, no research material, and no external copy, without changing anything |

## 3. Requirements shared by the seven skills

| ID | Requirement | Verdict | Evidence |
| --- | --- | --- | --- |
| CC-1 | Canonical packages with README, frontmatter, and generated copies | Met | Seven packages; `sync_skills.py --check` passes; Claude Code listed the seven skills in this session. |
| CC-2 | The agent operates Git; the researcher never edits Git configuration or memorizes commands | Met | Every procedure runs `versions.py` or a named Git command itself; `git-hands-on` L12–L14. |
| CC-3 | Inspect existing history before any change; reuse it rather than resetting | Met | `git-setup` L12; `git-save` L12; `git-recovery` L12; `git-backup` L12. |
| CC-4 | Local history and an external copy are always distinguished; nothing is sent without an explicit instruction for that destination | Met | `git-inspection` L20; `git-save` L33; `git-backup` L12–L22; `save` prints that nothing was sent (test `test_save_needs_an_identity_and_saves_only_the_requested_scope`). |
| CC-5 | No rewriting of shared history, no discarding of uncommitted work, no force-push | Met | `git-setup` L35; `git-recovery` L29; `backup` pushes without force. |

## 4. Requirements by skill

| ID | Skill | Requirement | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| GI-1 | `git-inspection` | Read-only account of tool, history, unsaved work by area, remotes, unfinished operations, secrets | Met | L12–L21; `inspect` and `scope` commands; tests `test_inspect_changes_nothing_and_init_creates_a_protected_history`, `test_scope_reports_tracked_files_that_ignore_rules_cannot_remove_and_untrack_keeps_them`. |
| GI-2 | `git-inspection`, `git-setup`, `project-onboarding` | Recognize inherited history: the template's history, an `origin` that is the template, another paper's history; explain the choices; never push research material to the template | Met | `git-inspection` L18; `git-setup` L28–L29; `git-backup` L21; onboarding step 1; test `test_inherited_template_history_and_research_versions_are_recognized` (template root detected, remote holds no research versions, a research version counted). |
| GS-1 | `git-setup` | Install on demand with consent; create the local history with the researcher's choice; agree on tracked scope; do not blanket-ignore documents | Met | L16–L24; `init` adds secret exclusions only. |
| GS-2 | `git-setup` | Exclude secrets; handle already-tracked material that ignore rules cannot remove | Met | L33–L34; `untrack`; tests above and `test_backup_refuses_history_with_secret_files`. |
| GSV-1 | `git-save` | Review changes, agree on scope, meaningful message, local checkpoint, summary of saved and remaining work | Met | L12–L33; test `test_save_needs_an_identity_and_saves_only_the_requested_scope` (scoped save, deletions, remaining changes). |
| GSV-2 | `git-save` | Do not overwrite or absorb unrelated edits; refuse secrets and oversized files | Met | L17, L29; tests `test_a_scoped_save_never_takes_other_prepared_changes_along` and `test_secrets_and_oversized_files_are_refused`. |
| GC-1 | `git-compare` | Compare requested versions or current changes and explain research-relevant differences with locations | Met | L12–L33; test `test_compare_summarizes_by_area_with_renames_new_files_and_words`. |
| GR-1 | `git-recovery` | Retrieve selected content safely; restore only with an explicit scope; preserve current work and a way back | Met | L16–L29; test `test_history_retrieve_and_restore_keep_current_work_recoverable` (unsaved text kept before the restore; extra files left). |
| GB-1 | `git-backup` | Destination, visibility, access, and what leaves the computer established with the researcher and recorded; accounts and passwords stay with the researcher | Met | L16–L22, L26. |
| GB-2 | `git-backup` | A checked destination; an unavailable destination or account means not backed up | Met | L27–L28; tests `test_backup_needs_a_confirmed_destination_and_is_checked_after_the_push` (refused before confirmation; verified after; the copy clones with the same content) and `test_an_unreachable_destination_is_reported_as_not_backed_up`. |
| GH-1 | `git-hands-on` | Practical guidance through the standalone tasks, on a practice copy, without duplicating procedures or risking real work | Met | L12–L32; test `test_practice_copy_is_separate_and_resettable` (three practice versions; saves and comparisons there leave the workspace history unchanged; a folder not made by the script is never deleted). |

## 5. Gaps found and fixed during the review

- F-1: a scoped save used `git commit -- <paths>`, which takes file content from disk and so undid a staged "stop tracking"; it now stages exactly the listed changes and commits the index, and refuses when unrelated changes are already prepared.
- F-2: the practice copy had no author identity of its own, so a practice save failed on a computer without a global Git identity; `practice` now sets one in the practice copy only.
- F-3: Git quoted non-ASCII paths; every call now disables that quoting, and comparisons parse renames from NUL-separated output.
- F-4: `.key` files were treated as secrets, which would block Keynote presentations; private keys are now recognized by their content instead.

## 6. Verdict and limits

All seven skills are accepted by review on 2026-10-28. Not covered: any hosting service (GitHub, GitLab, institutional servers), its sign-in, and the visibility of a real repository; Windows and Git for Windows; Codex; a live guided lesson with a researcher; and repositories with very large histories.
