# MVP 2 Skill Review

Status: review completed on 2026-10-28 by the agent in the template repository. Result: `source-ingestion` and `review-ingestion` pass. The review found nine gaps, seven in skill text (one of them also in a script message) and two in the import script, and fixed them (section 6). A pass shows that the skill text and the scripts it relies on meet the documented requirements. It shows nothing about Windows, ARM64, or Codex (section 8). A live mineru.net run, made after the review, is recorded in section 10.

## 1. Rule and pass criteria

On 2026-10-28 the template maintainer ruled that a skill passes acceptance when a written review against its requirements passes, and that skills get no more live scenario runs. The ruling is recorded in [section 6 of the MVP implementation guideline](../mvp-implementation-guideline.md#6-completion-record-for-each-mvp), and the four MVP 1 skills were reviewed the same way on the same day. This document is that review for the two MVP 2 skills.

The pass criteria were fixed before the review started:

- A skill passes when every requirement that can be judged by reading is Met after fixes. A gap is fixed in its own layer: skill text, description, script, table data, or a document. No sentence is added to `AGENTS.md` or `CLAUDE.md` to close a gap.
- Most of MVP 2's behavior lives in scripts. A requirement that a script carries counts as Met only with a passing automated test or a recorded observation of a live run with synthetic material (section 2).
- A requirement that only a real platform, host, or service can show is listed in section 8. It is never counted as Met.
- These skills have had no live run. Model behavior that the MVP 1 runs make likely is listed as a residual risk (section 7), not as a review failure.

## 2. Method

Read in full: both `SKILL.md` files and their READMEs, `scripts/ingest.py`, `scripts/setup_mineru.py`, every module in `scripts/ingestion/`, `scripts/tests/test_ingest.py`, `scripts/tests/test_ingest_cloud.py`, `AGENTS.md`, `privacy-configuration/sources.md` and step 6 of that skill, and the READMEs of `references/`, `references/extracted/`, `inbox/imports/`, and `reviews/`.

Requirement sources: the MVP 2 entry (L104 to L129) and section 5 of the [MVP implementation guideline](../mvp-implementation-guideline.md); [design plan](../design-plan.md) sections 4 (README contract, L239 to L261), 5 (L263 to L339), 6 (L341 to L353), 9 (L454, L456, L485 to L499), 12 (L605 to L635), and 14 (L677, L683); `AGENTS.md`; "Writing a skill" in [`.agents/skills/README.md`](../../.agents/skills/README.md) (L15 to L21); and the [Markdown conventions](../markdown-and-export-conventions.md) (L5).

Line numbers point to the files after the fixes of section 6. `SKILL` means the `SKILL.md` of the skill under review. Script evidence names the function and its first line; test evidence names the test.

Mechanical checks, run on 2026-10-28 after the fixes. All pass:

| Command | Result |
| --- | --- |
| `python3 scripts/sync_skills.py --check` | Skill copies match: 6 packages |
| `python3 scripts/check_capabilities.py` | The availability table matches the skills folder |
| `python3 scripts/check_readmes.py` | Every project directory has a README |
| `python3 scripts/check_requirements.py` | The writing rules have the required form |
| `python3 -m unittest discover -s scripts/tests` | 49 tests, OK, on Python 3.9.6 and 3.12.9 |
| Search for `/Users/`, `scratchpad`, and the maintainer's name in both skills and their READMEs | No match |

Live observations, on macOS 26.6.2 on Apple Silicon with 16 GB, MinerU 4.0.12, and the synthetic folder of [`fixtures/make_mvp2_fixtures.py`](fixtures/make_mvp2_fixtures.py), in disposable copies of the workspace: the runs recorded in the [implementation status](../implementation-status.md#mvp-2-flexible-intake-and-mineru-batch-ingestion), and one more for this review: the Word source `word source.docx` (a heading, a table, and a figure) converted with the flash tier into `document.md` with a Markdown table and a linked image in `assets/`, coverage "whole document", no warning, the role "reference" in the import record, and `ingest.py verify` and the README check passing.

## 3. Requirements that apply to both skills

| ID | Requirement | Source | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| CC-1 | One canonical copy per skill, and generated, committed Claude copies that match | `AGENTS.md` L93 | Met | `sync_skills.py --check` |
| CC-2 | `name` equals the directory; one-line `description`; only the fields both hosts support | skills README L18 | Met | L1 to L4 of each `SKILL.md`; the same script validates them |
| CC-3 | Skill text is in English | `AGENTS.md` L88 | Met | Both `SKILL.md` files and READMEs |
| CC-4 | Each package has a README for people that links to `SKILL.md` | skills README L9; design plan L253 | Met | The last paragraph of each README |
| CC-5 | A skill does not copy shared rules: question form, confirmation, language, source material | skills README L19; design plan L497 | Met after F-1 | source-ingestion L12, L28, L42, L114; review-ingestion L12, L20, L49 keep only what is specific to the task |
| CC-6 | No dependency on a maintainer-only path | guideline section 5, row "Codex/Claude parity" | Met | The search in section 2 |
| CC-7 | Nothing unavailable is offered or promised | `AGENTS.md` L17 | Met after F-2 | source-ingestion L34, L109; review-ingestion L15, L22, L49 say "not available yet" and promise nothing |
| CC-8 | The availability table lists both skills and names the credential's user | `AGENTS.md` L27, L33, L36, L37 | Met | `check_capabilities.py` |
| CC-9 | Every created project directory has a useful English README; repeat runs keep added text; no README in an external folder | design plan L241, L251; `AGENTS.md` L74; guideline L125 | Met | `common.update_readme` L103 (maintained block); `library.archive` L71, `library.write_readmes` L126, `library.carry_readmes` L109; `reviews.Round.ensure` L44; tests `test_imports_a_folder_and_records_every_item` (the input folder is unchanged; the README check passes), `test_the_reading_status_and_added_readme_text_survive_reconversion`, `test_a_review_round_keeps_comments_changes_and_annotations` |
| CC-10 | The scripts that the skills rely on have automated tests | guideline section 5; design plan L683 | Met | 22 tests in `test_ingest.py` and `test_ingest_cloud.py` |
| CC-11 | The description routes the skill from ordinary language, with a "Use when" clause | `AGENTS.md` L93; design plan L499 | Met | L3 of each `SKILL.md` |
| CC-12 | The skill names its triggers, scope, inputs, records to read, outputs, managed files, completion checks, and handoff | design plan L495 | Met | source-ingestion L3, L8, L13, L20, L40, L119 to L123, L33; review-ingestion L3, L8, L13, L19, L26, L53 to L56 |

## 4. Requirements by skill

### 4.1 source-ingestion

| ID | Requirement | Source | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| SI-1 | One request imports one file or a folder; no MinerU command, skill name, or output name is asked of the researcher | design plan L305, L309; L454 | Met | L3, L20 to L27, L72 to L80 |
| SI-2 | Show the file count and the processing route; scan no unrelated folder; settle subfolder inclusion and say so | design plan L309 | Met | L20, L36; `pipeline.list_files` L23 includes subfolders only with `--recursive` and reports the ones left out |
| SI-3 | The researcher chooses the route; recommend a route and a tier from the documents and the computer; record the service, the scope, and the mode, and reuse them within the scope | design plan L278, L621; `AGENTS.md` L49 | Met after F-3 | L40 to L47, L55 to L63 |
| SI-4 | Never switch to cloud or to another parser on a failure | `AGENTS.md` L82; design plan L278; guideline L112 | Met | L12; the route is fixed per import (`ingest.command_run` L147 refuses a different route for an existing import); no fallback exists in `pipeline.Pipeline.run` L115 |
| SI-5 | Upload only within the confirmed service and scope, check the scope of every batch, and never upload as a test | guideline L112; design plan L621; `AGENTS.md` L83 | Met | L15, L45, L47; `ingest.cloud_route` L63 refuses unless `requirements/privacy.md` names mineru.net; `test_refuses_without_a_confirmed_choice_or_a_token` |
| SI-6 | A missing tool or credential leads to setup and then to the same batch; no question per file within the scope | design plan L310 | Met | L36, L53 to L68, L79 |
| SI-7 | An installation or a model download is described and needs consent before it starts | design plan L287, L621 | Met | L44, L54, L60 to L63; `routes.LocalRoute.env` L153 sets `MINERU_MODEL_SOURCE=local` (L161), so a missing model stops the run instead of starting a download |
| SI-8 | A cloud-only setup installs no local model or parser | design plan L276, L613; guideline L127 | Met | L67 and L68 install nothing; `routes.CloudRoute` L266 uses only the standard library |
| SI-9 | The credential is entered privately, never in chat, arguments, or logs, and the adapter loads it | `AGENTS.md` L23, L81; design plan L631 to L633 | Met | L67, L68; `ingest.cloud_route` L63 reads the environment or `load_env_local`; `common.Redactor` L126; `test_uploads_converts_and_keeps_the_token_private` finds the token in no file. The live credential is not covered (section 8) |
| SI-10 | Originals are archived unchanged; input files and folders are never changed or added to | `AGENTS.md` L72, L74; design plan L311, L321 | Met | L14, L120; `library.archive` L71 verifies the copy's checksum; `test_imports_a_folder_and_records_every_item` |
| SI-11 | A stable source ID independent of names; exact duplicates by checksum; related versions kept apart and linked | design plan L343; guideline L113 | Met after F-4 | L110; `library.lookup` L50 and `library.allocate` L63; `pipeline.Pipeline.add_file` L90; `test_entry_key_escaping_and_index` writes `relatedsource` |
| SI-12 | Readable Markdown with working images; asset links normalized and checked | design plan L299, L311; guideline L114 | Met | `extraction.rewrite_links` L139, `extraction.check_links` L464; live runs; `test_imports_a_folder_and_records_every_item` |
| SI-13 | Parser output is preserved | design plan L288, L299; guideline L113 | Met | `extraction.build` L270 copies it to `native/`; `test_imports_a_folder_and_records_every_item` |
| SI-14 | Provenance holds the source ID, checksum, converter and version, settings, mode, time, expected and processed coverage, outputs, and warnings; unknown coverage is explicit; a partial extraction stays visibly partial | design plan L285, L297; guideline L113, L122 | Met after F-6 | `pipeline.Pipeline.publish_source` L273; `extraction.check_layout` L361; `extraction.coverage_note` L319 puts a note at the top of an incomplete `document.md`; `test_problems_are_flagged_and_partial_results_stay_partial` |
| SI-15 | Publish through a temporary destination in one step; reuse a matching result; a new conversion keeps notes and corrections | design plan L301; guideline L113, L114, L126 | Met | L78, L81, L96; `library.publish` L179; `pipeline.Pipeline.earlier` L180; the scripts never write `references/notes/`; `test_matching_results_are_reused_and_a_settings_change_is_detected`, `test_hand_edits_are_never_overwritten_silently` |
| SI-16 | Each document is tracked; only open or failed work is retried; authentication and quota failures stop the batch once; provider limits and conservative concurrency | design plan L312; guideline L114, L126 | Met | L79, L80; `pipeline.Pipeline.run` L115; `routes.CloudRoute._api` L292; batches of 20 every 30 seconds (`pipeline.Pipeline.cloud_items` L316); local conversion is sequential; `test_a_stop_keeps_finished_work_and_the_import_continues`, `test_an_expired_token_stops_the_batch_once`, `test_unfinished_work_is_collected_later_without_a_second_upload` |
| SI-17 | A short report with counts and links; completion is not accuracy; retrying needs no technical step | design plan L313; guideline L114 | Met | L80, L114; `ingest.summary` L87 |
| SI-18 | Technical logs stay in the background with secrets removed | design plan L315; guideline L114 | Met | L16; `common.Log` L139 writes to `.local/logs/`; `test_uploads_converts_and_keeps_the_token_private` checks every file, logs included |
| SI-19 | The index is updated automatically and keeps the reading status | design plan L311, L345 | Met | `library.index_upsert` L232; `test_the_reading_status_and_added_readme_text_survive_reconversion` |
| SI-20 | Citation metadata comes only from the document, is marked as such, and is not confused with evidence | design plan L257, L353; `AGENTS.md` L66 | Met | L100 to L109; `library.bib_upsert` L341 writes `sourceid` and `metadatasource`; `test_entry_key_escaping_and_index`, `test_a_cited_key_is_kept` |
| SI-21 | Title, authors, date, identifiers, source type, original and extraction paths, and reading status are recorded | design plan L345 | Met | The index row (`library.index_upsert` L232) and the BibTeX entry type and fields (L106) |
| SI-22 | The same contract for Word and other formats; unsupported formats explicit; a format is advertised only after it is verified | guideline L115, L123 | Met after F-9 | L44, L59, L94; `routes.handler_for` L78 and `routes.unsupported_reason` L89; `routes.VERIFIED` L51 flags every other combination; the Word source run of section 2 |
| SI-23 | Derived math follows the conventions; delimiters are normalized without changing a formula; transcription and unsupported commands are flagged | guideline L116; conventions L5 | Met | L93; `extraction.normalize_math` L180 and `extraction.check_math` L486; `test_math_normalization_changes_delimiters_only` |
| SI-24 | Mixed intake without presorting; ask only unclear roles; an import record links input, checksum, role, destination, status, and open items; an unadopted manuscript stays out of the manifest | design plan L319, L321; guideline L117, L124 | Met after F-5 | L28 to L34; `ingest.command_note` L250; `records.ImportRecord.readme` L104 shows the role; `test_problems_are_flagged_and_partial_results_stay_partial` checks the role |
| SI-25 | No claim of OCR accuracy; checks against the original stay necessary | guideline L129 | Met | L8, L91 to L96, L114 |
| SI-26 | A correction is kept apart from the extraction and is not mixed with evidence work, which is not available | `AGENTS.md` L17, L72; design plan L301 | Met after F-8 | L81, L96 |

### 4.2 review-ingestion

| ID | Requirement | Source | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| RI-1 | Archive and extract into `reviews/<venue-id>/<round-id>/` with originals, `extracted/markdown/`, and `extracted/assets/` | design plan L337, L456; guideline L118 | Met | L8, L31; `reviews.Round` L35; `test_a_review_round_keeps_comments_changes_and_annotations` |
| RI-2 | Venue, round, and manuscript version come from the context; ask only when missing or ambiguous | design plan L337 | Met | L19 to L21, L45 |
| RI-3 | Reviewer labels, item numbers, page or line references, images, tables, and locators are kept | design plan L337; guideline L118 | Met | L40 (count and compare, never renumber); images are named `<document>--<image>` (`reviews.publish` L265) |
| RI-4 | Word comments, tracked changes, and PDF annotations are read apart from the main text; what is not captured is reported; a Markdown file is no proof of capture | design plan L339; guideline L118, L124 | Met | L38, L39, L54; `reviews.docx_structures` L131, `reviews.structures_markdown` L195, `pdf.annotations` L153; live run; `test_word_structures`, `test_pdf_page_count_and_annotations` |
| RI-5 | No response is drafted or sent; extraction needs no response skill | design plan L337, L456; guideline L118 | Met | L15, L49, L55 |
| RI-6 | Repeating an import duplicates nothing and mixes no rounds | guideline L124 | Met | L14; `reviews.Round.archive` L94; `test_a_review_round_keeps_comments_changes_and_annotations` |
| RI-7 | Confidential correspondence is uploaded only within a confirmed scope that covers it | `AGENTS.md` L49, L83; design plan L621 | Met | L12, L13 |
| RI-8 | Advice from collaborators is research feedback, not a review round | design plan L339, L488 | Met after F-7 | L22 |
| RI-9 | READMEs at the venue, round, originals, extraction, Markdown, and image levels | guideline L125 | Met | `reviews.Round.ensure` L44; the README check in `test_a_review_round_keeps_comments_changes_and_annotations` |
| RI-10 | The report names what was found and what could not be captured | design plan L456 | Met | L49, L54 |

## 5. Acceptance evidence of the guideline

The guideline's acceptance evidence for MVP 2 (L122 to L127) is a list of observations. Under the ruling, the skills are judged by review; the observations that scripts and live runs can give are mapped here.

| ID | Evidence asked for | Verdict | Where it stands |
| --- | --- | --- | --- |
| AE-1 | A fixture folder with duplicates, non-ASCII paths, images, a scanned page, columns, a table, an equation, and more than ten pages; real page coverage and links (L122) | Met | The fixture generator and the live runs in the implementation status: 12 of 12 pages, the duplicate found, the scanned page flagged by the flash tier and read by the basic tier |
| AE-2 | A representative Word source, inspected in the archive, Markdown, assets, and record; other formats only after verification (L123) | Met | The Word source run of section 2; formats outside `routes.VERIFIED` are flagged |
| AE-3 | Mixed intake, a direct external path, a Word review with comments, an annotated document, no duplicate on repetition (L124) | Met for the scripts | External folders and review rounds: live runs and tests. Mixed intake is agent behavior (source-ingestion L28 to L34), judged by this review |
| AE-4 | READMEs at every new level, unchanged sources, no README in external folders, descriptions kept on retry (L125) | Met | CC-9 |
| AE-5 | Interruption, retry, survival of results and notes, reuse, detected settings changes, corrupt input, authentication and quota without loops (L126) | Met | SI-15, SI-16; a live interrupted batch was continued |
| AE-6 | Local and cloud envelopes on their environments, no local weights for cloud, no upload after a local failure, the live credential, and the service's terms (L127) | Partly covered | The local envelope was observed on macOS; SI-4, SI-8, and SI-9 hold; the terms were read on 2026-10-28 and leave training use and retention unknown. After the review, the live credential and the live service were observed with synthetic files (section 10); the terms stay unknown |

## 6. Gaps found and fixed

| ID | Gap | Fix | Layer |
| --- | --- | --- | --- |
| F-1 | Both skills copied standing rules: imported text as source material, reports in the interaction language, and the one-question form | source-ingestion L12, L28, L42, L114 and review-ingestion L12, L20, L49 keep only what is specific to the task; `AGENTS.md` carries the rest | Skill text |
| F-2 | review-ingestion told the agent to say that a response "can be prepared later, when that capability exists", which promises an unavailable capability | L49 says that preparing a response is not available yet, only when the researcher asks | Skill text |
| F-3 | A local route confirmed at the first import was not recorded, so the next import would ask again | L47 records a confirmed choice with its documents; a local choice at once, a cloud choice through `privacy-configuration` | Skill text |
| F-4 | Related versions of a work were mentioned to the researcher but not linked | L110 records `relatedsource` in both entries after the researcher confirms | Skill text; the script already accepted the field |
| F-5 | The import record held no role for converted items, although the design asks for input, checksum, role, destination, status, and open items | `pipeline.Pipeline.add_file` L96 records `reference` or `review`; the import README has a Role column; tests check it | Script |
| F-6 | A partial extraction was marked as partial in its README and the index, but not in `document.md` itself | `extraction.coverage_note` L319 puts a note at the top of an incomplete text, marked as the workspace's and left out of the checks; a test checks it | Script |
| F-7 | review-ingestion did not say that collaborators' advice is not a review round | L22 keeps such files out of `reviews/` and says that organizing research feedback is not available yet | Skill text |
| F-8 | "Move the correction into the source note" could read as starting evidence work, which is not available | L81 and L96 keep the researcher's correction only | Skill text |
| F-9 | source-ingestion and `setup_mineru.py check` presented PowerPoint and Excel as read by the flash tier, although only PDF and Word are verified | L44 and L59 name Word as verified and say that other office formats are flagged until verified; `setup_mineru.py` L96 and L97 say the same | Skill text; script message |

No table row and no sentence of `AGENTS.md` or `CLAUDE.md` changed. The Claude copies were regenerated with `sync_skills.py`, and all 49 tests pass after the fixes.

## 7. Residual risks (model behavior)

These skills have had no live run, so no miss was observed. The MVP 1 runs with Haiku make these risks likely; the skill text asks for the right behavior in each case.

- Routing. "Is this computer ready to import PDFs?" may load `environment-management` alone. Its step 2 now points to `setup_mineru.py check` and to this skill. A cloud wish without a request to import may load no skill, as in MVP 1.
- Processing choice. The route question at the first import can be skipped, or a wish to use mineru.net can be treated as a choice. The script refuses the cloud route until `requirements/privacy.md` names mineru.net, which limits the damage to a delay.
- Citation metadata. A model may fill a field that the first page does not show. The entry is marked as read from the document, and checking it against a registry belongs to MVP 3.
- Language. Notes between tool calls can be English.

## 8. Remaining verification limits

The live run in section 10 verified PDF and Word conversion with the `vlm` model on macOS, using synthetic files. The following items remain unverified and must not be advertised as working:

- mineru.net's terms and data handling: the terms read on 2026-10-28 do not state whether uploaded documents are used for training or how long they are retained. The live run used synthetic files; re-check the terms before uploading researcher materials.
- Cloud image inputs, the `pipeline` model, and service behavior at its limits (daily quota, rate limit, and expired tokens). These paths have only been exercised against the fake service.
- Windows and ARM64: `.tools/mineru/Scripts/`, the Python launcher, long and non-ASCII paths, and MinerU's own support on those platforms.
- Codex: discovery of `.agents/skills` and loading of `AGENTS.md`.
- The standard and advanced tiers, and local formats other than PDF, Word, Markdown, and plain text.
- The accuracy of OCR, tables, and formulas on real documents. One formula was transcribed wrongly in the live basic-tier run, and no check can detect that.
- Page numbers of PDF annotations; Word footnotes, endnotes, and moved text.
- Whether a particular model follows the text (section 7).

## 9. Verdict

| Skill | Verdict |
| --- | --- |
| `source-ingestion` | Accepted by review, 2026-10-28 |
| `review-ingestion` | Accepted by review, 2026-10-28 |

"Accepted by review" does not mean verified on a platform. MVP 2 as a whole stays open for the items of section 8.

## 10. Addendum: live mineru.net run (2026-10-28, after the review)

The maintainer asked for the live test and entered a token on the private page. A token that was first pasted into the conversation was not used from there. In a disposable copy, the import script sent only synthetic files from the fixture generator to mineru.net, as references and as a review round.

- Observed: the token reached the import through `credentials.py run` and appeared in no record, log, or output; the service saw only source IDs as file names; coverage, running heads, columns, the scanned page, and tables came out as described in [MinerU integration](../mineru-integration.md#minerunet); the service ran MinerU 3.4.4.
- Three script gaps found and fixed, each with a test: the service's copy of a Word original kept in `native/`; the parser version that the service states not recorded in provenance; and a correct image link of a review document reported as broken, because links were checked in a stage laid out differently from `extracted/`.
- Two conversion defects that no automatic check detects: a mistranscribed formula, and annotation icons that cut the text under them in a review PDF. The skills already require the comparisons that catch them (source-ingestion L93, review-ingestion L40).
- PDF and Word with the `vlm` model are now verified combinations (`routes.VERIFIED`). Still not covered: the terms, images, the `pipeline` model, and the service's behaviour at its limits.

The verdicts of section 9 are unchanged.
