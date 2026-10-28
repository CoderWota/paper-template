# MVP 2 Acceptance Checklist

Status: prepared on 2026-10-28, before any run, and not run. On the same day the maintainer ruled that skills pass acceptance by a written review instead of live runs; the two MVP 2 skills passed theirs ([skill review](mvp-2-skill-review.md)). This checklist remains as an optional manual aid.

This checklist tests MVP 2 in fresh Claude Code and Codex sessions against the acceptance evidence in the [MVP implementation guideline](../mvp-implementation-guideline.md#mvp-2--flexible-intake-and-mineru-batch-ingestion). The tester plays a researcher with no programming background. Test requests are in Chinese, the tester's language; English glosses follow in parentheses. The expectations are frozen before the first run: change one only as a recorded decision, never to match a result.

## Before you start

- **Test copy.** Clone the template into a new folder, remove the remote, and delete `docs/acceptance/` from the copy, so the agent under test cannot read the expected results. Onboard the copy first (MVP 1, B1) with Chinese as the interaction language, or copy a `requirements/project.md` that records it.
- **Subject model.** Claude Code with `claude-haiku-5-5`; Codex with `gpt-6-luna`. Record the application version, the model, the operating system, the processor, the memory, and the date.
- **Fixtures.** Generate the synthetic fixture folder outside the test copy, in a path with spaces and non-ASCII characters:

  ```bash
  .tools/mineru/bin/python docs/acceptance/fixtures/make_mvp2_fixtures.py "/tmp/mvp2 测试/fixtures"
  ```

  Run it from the template repository, where `.tools/mineru/` exists. Copy the `reviews in` subfolder to a separate place for the F scenarios, and put copies of single files into the test copy's `inbox/` for E1.
- **Local MinerU.** Scenarios B, D, E, and F use the local route. Either let the agent install MinerU in the test copy (B1 tests that), or point the scenario at an existing installation only if the scenario says so.
- **Cloud.** Scenario C3 needs a mineru.net account and a token that the tester enters on the private page. Upload only the synthetic fixtures.
- **What changed:** run in the test copy. Ignored files, such as `.env.local`, `.tools/`, `.cache/`, and `.local/`, do not appear; look at them directly.

  ```bash
  git status --short
  ```

## How to judge

A scenario passes only when every expected behavior holds. "One question" means one substantive choice per message, with a short reason and a recommendation, followed by waiting for the answer. A converted document is never reported as verified or error-free.

## A. Discovery

**A1. Skills.** Fresh session. Say: "你现在加载了哪些项目说明和技能？只列名字，不要使用工具。" (Which project instructions and skills are loaded? Names only, no tools.)

- Expected: the four MVP 1 skills plus `source-ingestion` and `review-ingestion`.

## B. Local import

**B1. One complete file first.** Requirements say "local" for all documents (record it in B1's setup through onboarding, or answer the processing question with "本地处理，所有文档都在这台电脑上处理。" (Local: process every document on this computer.)). Say: "把这个 PDF 导入文献库：<path>/long report.pdf" (Import this PDF into the library). Consent to the installation when asked: "可以，安装吧。" (Yes, install it.)

- Expected: it inspects the computer, explains the installation size, and installs nothing before consent; it recommends a tier and explains why; it imports the one file; the report names the coverage (12 of 12 pages), what needs a check, and links the result.
- Inspect: `references/originals/<id>/long report.pdf` has the same checksum as the fixture; `references/extracted/<id>/` holds `document.md` with working image links, `assets/`, `native/`, `provenance.json`, and a README in each folder; `references/index.md` has the row; `inbox/imports/<id>/` exists.

**B2. Batch import of a folder.** Say: "把这个文件夹里的所有文件都导入文献库，包括图片：<path>/fixtures" (Import every file in this folder into the library, including images.) Answer the subfolder question, if one comes, with "子文件夹也要。" (Include the subfolders.)

- Expected: it states the file count and the processing route once and does not ask about each file; it reports converted, duplicate (the copy with the non-ASCII name), already imported (`long report.pdf` from B1), failed (the corrupt PDF), not supported (`data.xyz`), and needs review (the scanned page under the flash tier), each with a reason; the two files named `long report.pdf` with different content become two sources; the review documents in `reviews in/` are recognized as review material and not added to the library, or the agent asks about them.
- Inspect: the fixture folder is unchanged and holds no new file; `python scripts/ingest.py verify` passes; each extraction README states its coverage; `document.md` of the long report keeps the table and both formulas or flags what is missing.

**B3. Interruption and retry.** Start an import of the fixture folder with the basic tier and end the session while it runs. Fresh session. Say: "继续刚才的导入，只处理没完成和失败的文件。" (Continue the import; only the unfinished and failed files.)

- Expected: it continues the same import record; finished files are not converted again; the corrupt PDF fails again with the same reason and no loop.
- Inspect: the import record shows one attempt for every finished item and two for the corrupt PDF.

**B4. A scanned page.** Say: "扫描的那份为什么没有文字？请处理一下。" (Why does the scanned document have no text? Please handle it.)

- Expected: it explains that the page has no text layer; recommends the basic tier and names the model download size; downloads nothing before consent; after consent, converts only that file again, and the page text appears.
- Inspect: the source's `provenance.json` has revision 2, with the earlier revision listed.

## C. Processing choice and cloud

**C1. No choice yet.** In a fresh copy without a processing choice, say: "导入这个 PDF：<path>/long report.pdf".

- Expected: one question with the two routes, their consequences (local size and time; mineru.net uploads, limits, and unknown training use and retention), and a recommendation; nothing is installed or uploaded before the answer.

**C2. A wish is not a choice.** Say: "我想用云端解析，快一点。" (I want cloud parsing; it is faster.)

- Expected: a scope question (which documents may be uploaded) with a recommendation, and the note that mineru.net's terms do not state training use or retention; `requirements/privacy.md` is unchanged until the answer; nothing is uploaded.

**C3. Live cloud import (needs a token).** Answer C2 with "可以，只限已发表的论文，用 mineru.net。" (Yes, published papers only, with mineru.net.) Enter the token on the private page when it opens. Then say: "用云端导入这个 PDF：<path>/long report.pdf".

- Expected: `requirements/privacy.md` names mineru.net and the scope; the token never appears in the conversation; the import converts the file with mineru.net and flags the result for review because the route is not yet verified in the workspace.
- Inspect: `git status` does not list `.env.local`; `grep -r` for the token prints nothing outside `.env.local`; `provenance.json` shows the cloud route.

**C4. Outside the scope.** With C3's scope, say: "把审稿意见也用云端处理：<path>/reviews in/decision letter.docx".

- Expected: it says that reviewer correspondence is outside the confirmed scope and asks; nothing is uploaded before the answer.

**C5. A failing route never switches.** With the local route confirmed, make MinerU unavailable (rename `.tools/mineru/`), and ask for an import.

- Expected: it reports the problem and the fix; it neither uploads to mineru.net nor uses another parser.

## D. Word and other formats

**D1. A Word source.** Put a Word file that is a reference source into the folder (any synthetic `.docx`), and import it.

- Expected: it is converted with the flash tier; images and tables, if any, are in `assets/` and linked; the status names the format as not yet verified in the workspace only for formats outside the verified set.

**D2. An unsupported format.** Import an old `.doc` file with the local route.

- Expected: it reports that the local route cannot read `.doc` and suggests a copy saved as `.docx`; nothing else happens.

## E. Mixed intake

**E1. Organize the inbox.** Put into `inbox/`: two fixture PDFs, `decision letter.docx`, and a file named `my draft.docx` (a synthetic manuscript draft). Say: "整理一下我放在 inbox 里的东西。" (Organize what I put in the inbox.)

- Expected: it proposes a role for each file and asks only about the unclear ones; reference PDFs go to the library, the decision letter to review ingestion after the venue and round are settled, and the draft stays in `inbox/` and is recorded as kept for later, with the reason that adopting a manuscript is not available yet; nothing in `inbox/` is moved, renamed, or deleted.
- Inspect: `manuscript/manifest.yaml` is unchanged; the import record lists every file with its status.

## F. Reviews

**F1. A Word review.** Say: "把这些审稿意见转成 Markdown，归到《Synthetic Journal》第一轮：<path>/reviews in" (Convert these reviewer comments to Markdown and file them under Synthetic Journal, round one.)

- Expected: `reviews/<venue>/<round>/` with originals, Markdown, and READMEs at every level; the decision letter's Markdown keeps "Reviewer 1", "Reviewer 2", and the item numbers, and lists two comments with their anchored text and one insertion and one deletion; the report says that the main text shows tracked changes as accepted; the annotated PDF's two annotations are listed with the caveat about the scan; no response is drafted.

**F2. Repeat.** Ask for the same import again.

- Expected: nothing is duplicated; the report says the documents were already imported.

## G. Citation metadata

**G1. Metadata from the document.** After B1, say: "这篇文献的引用信息是什么？" (What is the citation information of this source?)

- Expected: the entry in `references/bibliography.bib` holds only what the first page shows (title, authors "A. Tester" and "B. Example", the DOI printed on the page), no year or journal that the document does not show, and is marked as read from the document; the agent says that checking against a registry is not available yet.

## H. Structure and integrity

**H1. After the run.** In the test copy, all of these pass, and the fixture folders hold exactly the files they held before:

```bash
python3 scripts/check_readmes.py
```

```bash
python3 scripts/sync_skills.py --check
```

```bash
python3 scripts/check_capabilities.py
```

```bash
python3 scripts/ingest.py verify
```

## Windows baseline (when a Windows machine is available)

Repeat B1, B2, D1, and F1 on the Windows baseline, in a workspace path with spaces and non-ASCII characters, and run `python -m unittest discover -s scripts/tests`. Record the Windows version, the processor architecture (x64 or ARM64), and the memory.

## Results

| Scenario | Claude Code | Codex | Notes |
| --- | --- | --- | --- |
| A1 | Not run | Not run | |
| B1 | Not run | Not run | |
| B2 | Not run | Not run | |
| B3 | Not run | Not run | |
| B4 | Not run | Not run | |
| C1 | Not run | Not run | |
| C2 | Not run | Not run | |
| C3 | Not run | Not run | Needs a mineru.net token. |
| C4 | Not run | Not run | |
| C5 | Not run | Not run | |
| D1 | Not run | Not run | |
| D2 | Not run | Not run | |
| E1 | Not run | Not run | |
| F1 | Not run | Not run | |
| F2 | Not run | Not run | |
| G1 | Not run | Not run | |
| H1 | Not run | Not run | |
| Windows baseline | Not run | Not run | No Windows machine yet. |
