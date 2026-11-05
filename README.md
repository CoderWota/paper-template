# Research Writing Workspace · 论文研究与写作模板

[中文](#中文使用指南) · [English](#english-guide)

## 中文使用指南

一个仓库用于一篇论文。你决定研究问题、科学判断、最终表述和投稿选择；助手帮助你查证、写作、处理文件和保存版本。你不需要编程知识。

### 1. 打开副本，用一句话开始

在 GitHub 点击 **Use this template** 创建自己的仓库，或下载 ZIP、克隆仓库。用 Codex 或 Claude Code 打开副本的根目录，然后在聊天中发送提示词。每篇新论文使用独立副本。

第一次使用时，可以说：

> 我第一次使用这个仓库，请介绍主要目录，并告诉我如何开始。

这会触发 `paper-hands-on` 的导览流程。导览本身不会初始化论文或处理文件。准备开始时说：

> 请初始化这个论文项目，安装并检查项目规定的必要组件。我没有编程背景，请一次问我一个必要问题。

这会触发 `project-onboarding`，并由 `environment-management` 处理环境。助手会确认研究目标、对话语言，以及当前任务需要的论文语言；不确定的选择可以暂缓。项目记录使用英文，原始笔记和工作草稿保留原语言，投稿文本使用你选择的论文语言。

初始化会复用已有工具，安装固定版本的官方 Sciverse 和 MinerU MCP，生成 Codex 和 Claude Code 的项目配置，并检查协议和工具发现。它还会检查 `pdftotext`，缺少时安装 Poppler。MCP 安装需要 Python 3.11+、Node.js 18+ 和 npm；如缺少基础运行环境，助手会先说明并征求安装许可。安装不需要 API 密钥，也不会发送检索请求或文档。

初始化还会检查并断开明确指向原模板的远程连接，保留本地文件、版本和你自己的远程地址。按助手提示重新打开项目，并处理客户端的信任提示，以加载新配置。配置检查通过不代表客户端已加载工具或密钥有效。

### 2. 配置 MCP 和密钥

MCP 让助手使用外部服务：Sciverse 用于文献检索，MinerU 用于参考资料的云端解析。Sciverse 直接提供给客户端；MinerU 由仓库导入流程调用。详细说明见 [MCP 配置](mcp/README.md)。

实际需要检索时说：

> 为这次关于 [主题] 的文献检索配置 Sciverse。先和我确认发送的检索范围；如需密钥，请打开本机私密输入页。

导入参考资料时说：

> 导入 [参考文献路径] 前检查 MinerU 配置；如需 Token，请打开本机私密输入页。

任务 skill 会调用 `environment-management`。助手提供官方取密钥页面，并在本机打开私密输入页。你只在该页输入密钥，**不要把密钥发到聊天中**。密钥保存在 Git 忽略的 `.env.local` 中；该文件没有加密，不要分享。助手只报告是否已配置，不显示密钥。Sciverse 检索需要密钥；MinerU 可使用受限的免 Token Flash 模式，需要时再配置 Token。

密钥配置不等于允许检索或上传。Sciverse 查询范围需先确认；MinerU 会把文件发送到 mineru.net，当前仅允许处理已识别的参考资料，不能上传自己的论文草稿、审稿信或合作者反馈。参见 [处理范围](requirements/privacy.md)。

### 3. 导入论文草稿和参考文献

可以把文件放进可选的 [inbox/](inbox/README.md)，也可以直接给出助手能访问的路径。将下列方括号内容换成实际文件或目录。

**导入自己的草稿**（触发 `manuscript-import`）：

> 请导入这份论文草稿 [文件路径]，保留原文件，并告诉我转换损失、未解决引用和下一步。

Word `.docx`、OpenDocument `.odt` 和 LaTeX `.tex` 使用本地 Pandoc；缺少时助手会征求安装许可。Markdown 和纯文本直接读取。PDF 或扫描版草稿不能通过 MinerU 导入，需提供可编辑版本或另行选择获准的处理方式。已有正文时，新导入版本会先暂存供比较。修订痕迹的接受或拒绝由你决定。

**导入外部参考资料**（触发 `source-ingestion`）：

> 请导入 inbox/ 里的这些参考文献；先确认文件角色，并告诉我哪些文件需要远程解析。

助手先区分参考资料、草稿、反馈和其他文件，再按获准范围处理。原文件保持不变；参考资料进入 [references/](references/README.md)，采用的论文正文进入 [manuscript/](manuscript/README.md)。导入报告会列出失败、未解决引用和需核对的公式、图片等问题。转换完成不代表内容已核实。

### 4. 用提示词写作和编辑论文

描述 **改哪里、做什么、保留什么** 即可。助手按任务选择 skill；下面的名称只是帮助理解，你不必记住。指定文件、章节或粘贴段落，可以让范围更清楚。

| 任务 | 可直接使用的提示词 | 对应 skill |
| --- | --- | --- |
| 搭建提纲 | 根据现有研究问题、材料和结果，帮我整理论文论证与章节提纲；标出证据缺口，先等我确认。 | `manuscript-outline` |
| 起草章节 | 根据已记录的方法和结果起草 [章节]；不要补造数据、引用或结论，并标出缺失证据。 | `manuscript-writing` |
| 局部润色 | 只润色 [段落/章节]，保留原意、数据、引用、限定条件和不确定性。 | `manuscript-writing` |
| 缩短摘要 | 把摘要缩短到 [字数]，保留主要结果、条件和局限。 | `manuscript-writing` |
| 翻译 | 把 [内容] 翻译成已选定的论文语言，并列出可能改变含义的地方供我检查。 | `manuscript-writing` |
| 检查自然表达 | 检查 [段落/章节] 是否有生硬或重复表达，先只报告问题，不要修改。 | `natural-prose` |
| 修改自然表达 | 修改 [段落/章节] 的生硬和重复表达，保留我的语气及全部科学含义。 | `natural-prose` |
| 核查证据 | 检查 [章节] 中每项主张的证据支持、引用和局限；不要仅凭引用存在就判断支持充分。 | `manuscript-audit`，需要时调用 `literature-and-evidence` |
| 重大修订 | 我想把全文结构调整为 [目标]。先保存基线并给出修改计划，等我确认后再改正文。 | `manuscript-revision` |

例如，可以先要求检查引言，读完问题清单后再说：

> 请修正刚才指出的表达问题，只改引言；保留科学含义，改完后重新核查这些问题。

单句、单段或单节请求限定在指定内容内。改变中心论点、跨章节结构或证据基础时，助手会建立可恢复的基线并整理修订计划；科学选择由你确认。只检查的请求不会修改正文。改写前保留副本，改写后对照原文检查数据、引用和条件，证据不足之处保持可见。

每次写入论文时，助手都会检查并同步内部论证图和推理记录，包括前提、分析、推论、判断及限制；你直接改过的文字会在下次检查时核对。这些内部记录不进入投稿正文。见 [内部论证框架](docs/logic-map-guide.md)。一次性修改不会自动成为长期写作规则。

### 5. 用 Git 保存、比较和找回

你描述想保留或找回的内容，助手操作 Git。

| 需要 | 提示词 | 对应 skill |
| --- | --- | --- |
| 设置版本记录 | 帮我为这篇论文设置本地版本记录，并说明会保存哪些内容。 | `git-setup` |
| 检查保存状态 | 我的工作保存了吗？还有哪些改动没有保存？ | `git-inspection` |
| 保存当前进度 | 保存这版论文，概括主要改动。 | `git-save` |
| 只保存指定内容 | 只保存这次修改的引言。 | `git-save` |
| 查看差异 | 比较当前版本和上次保存的版本。 | `git-compare` |
| 找回旧内容 | 找回 [章节/段落] 修改前的版本，先作为副本取回，不要覆盖当前内容。 | `git-recovery` |
| 恢复指定版本 | 我想把 [文件] 恢复到 [日期或版本]，先告诉我会替换什么，等我确认。 | `git-recovery` |

助手会检查保存范围、密钥和过大文件；第一次设置可能需要你提供版本作者名称和邮箱。保存后会报告版本编号和仍未保存的内容。旧内容默认作为副本取回。覆盖恢复前会展示范围并等待明确选择，同时保留当前内容；版本历史不会被重写。

**本地保存不等于外部备份。** 要做外部备份时，明确提供目的地和允许包含的材料；助手会通过 `git-backup` 处理并核对结果。

### 6. 继续工作、输出和目录

下次打开项目时说：

> 根据项目记录继续，并先检查当前文件和未完成事项。

助手通过 `paper-hands-on` 读取当前记录和实际文件。还可以直接请求：

> 按这些期刊要求排版论文，并检查 Word 输出。

> 整理这轮审稿意见，帮我逐条准备回复。

这分别触发 `submission-assembly` 和审稿处理流程。研究判断与投稿选择仍由你决定。

| 目录 | 内容 |
| --- | --- |
| [requirements/](requirements/README.md) | 已确认的目标、语言、写作、隐私和输出要求 |
| [inbox/](inbox/README.md) | 待导入材料的可选入口 |
| [manuscript/](manuscript/README.md) | 正文、提纲、内部论证图、图表和组装清单 |
| [references/](references/README.md) | 原始参考资料、提取文本、书目和证据笔记 |
| [ideas/](ideas/README.md) | 你选择保留的研究想法 |
| [research/](research/README.md) | 研究计划、决策、反馈、结果和来源记录 |
| [reviews/](reviews/README.md) | 按期刊和轮次整理的审稿信与回复 |
| [revisions/](revisions/README.md) | 重大修订的基线、候选稿和修改记录 |
| [outputs/](outputs/README.md) | 可重建的预览和保留的发布包 |
| [state/](state/README.md) | 当前进度、待解决事项和下次行动 |

更多说明：[操作指南](docs/README.md) · [能力与限制](docs/capabilities.md) · [MCP 配置](mcp/README.md) · [文档处理](docs/mineru-integration.md) · [论文格式与输出](docs/markdown-and-export-conventions.md)。

## English Guide

Use one workspace for one paper. You choose the research question, scientific judgments, final wording, and submission. The assistant helps check evidence, write, manage files, and save versions. You do not need programming knowledge.

### 1. Open a copy and start with a prompt

On GitHub, select **Use this template** to create your own repository, or download a ZIP or clone the repository. Open the copy's root folder in Codex or Claude Code and send prompts in the chat. Use a separate copy for each new paper.

For a first tour, say:

> This is my first time using this workspace. Explain the main folders and how to begin.

This starts the tour in `paper-hands-on`. A tour does not initialize a paper or process files. When ready, say:

> Initialize this paper project. Install and check the components required by the project. I have no programming background; ask one necessary question at a time.

This starts `project-onboarding`, with `environment-management` for setup. The assistant confirms your goal, conversation language, and the paper language when the task needs it. Unknown choices can wait. Project records use English. Original notes and working drafts keep their language; publication text uses your chosen paper language.

Initialization reuses working tools, installs pinned official Sciverse and MinerU MCP packages, generates Codex and Claude Code project configurations, and checks the protocol and available tools. It also checks `pdftotext` and installs Poppler if missing. MCP setup needs Python 3.11+, Node.js 18+, and npm. If a base runtime is missing, the assistant explains the need and asks before installing it. Installation needs no API key and sends no research queries or documents.

Initialization also checks and disconnects a clear connection to the original template repository. Local files, versions, and your own remote addresses are kept. Reopen the project and respond to client trust prompts when instructed to load the configuration. A configuration check does not prove that the client loaded the tools or that a key is valid.

### 2. Configure MCP and keys

MCP lets the assistant use external services: Sciverse for literature search and MinerU for cloud parsing of reference materials. Sciverse is exposed to the client; the workspace importer calls MinerU. See [MCP setup](mcp/README.md).

When a search is needed, say:

> Configure Sciverse for this literature search on [topic]. Confirm the query-sharing scope with me first. If a key is needed, open the private entry page on this computer.

For reference imports, say:

> Check MinerU setup before importing [reference paths]. If a token is needed, open the private entry page on this computer.

The task skill calls `environment-management`. The assistant gives you the official page for obtaining the key and opens a private entry page locally. Enter the key there. **Do not send keys in chat.** Keys are stored in `.env.local`, which Git ignores. The file is not encrypted; do not share it. The assistant reports whether a key is configured without showing it. Sciverse searches need a key. MinerU has a limited token-free Flash mode; configure a token when needed.

Entering a key does not authorize queries or uploads. Confirm the Sciverse query scope first. MinerU sends files to mineru.net. The current scope permits identified reference materials only; your drafts, review letters, and collaborator feedback cannot be uploaded. See [processing scope](requirements/privacy.md).

### 3. Import drafts and reference materials

Put files in the optional [inbox/](inbox/README.md), or give a path the assistant can access. Replace bracketed text below with your file or folder.

**Import your own draft** with `manuscript-import`:

> Import this manuscript draft [file path]. Keep the original and report conversion losses, unresolved citations, and the next step.

Word `.docx`, OpenDocument `.odt`, and LaTeX `.tex` use local Pandoc. If it is missing, the assistant asks before installing it. Markdown and plain text are read directly. PDF or scanned drafts cannot be imported through MinerU; provide an editable copy or choose another authorized route. If a manuscript already exists, a new import is staged for comparison. You decide whether to accept or reject tracked changes.

**Import external references** with `source-ingestion`:

> Import these reference materials from inbox/. Identify their roles first and tell me which files need remote parsing.

The assistant separates references, drafts, feedback, and other files before processing them within the authorized scope. Input files stay unchanged. References go into [references/](references/README.md); adopted manuscript text goes into [manuscript/](manuscript/README.md). The import report lists failures, unresolved citations, and formulas, images, or other items that need inspection. Conversion does not verify the content.

### 4. Write and edit with prompts

State **where to edit, what to do, and what to preserve**. The assistant selects the skill. The names below help explain the process; you do not need to remember them. Name a file or section, or paste a passage, to make the scope clear.

| Task | Prompt to copy | Skill |
| --- | --- | --- |
| Build an outline | Organize the argument and section outline from the current question, materials, and results. Mark evidence gaps and wait for my confirmation. | `manuscript-outline` |
| Draft a section | Draft [section] from the recorded methods and results. Do not invent data, citations, or conclusions. Mark missing evidence. | `manuscript-writing` |
| Polish a passage | Polish only [passage/section]. Keep the meaning, data, citations, conditions, and uncertainty. | `manuscript-writing` |
| Shorten an abstract | Shorten the abstract to [word count]. Keep the main results, conditions, and limitations. | `manuscript-writing` |
| Translate | Translate [content] into the chosen paper language. List any possible changes of meaning for me to check. | `manuscript-writing` |
| Check natural expression | Check [passage/section] for stiff or repetitive wording. Report problems first without editing. | `natural-prose` |
| Improve natural expression | Revise stiff or repetitive wording in [passage/section]. Keep my voice and all scientific meaning. | `natural-prose` |
| Check evidence | Check the evidence, citations, and limits for each claim in [section]. A citation alone does not establish support. | `manuscript-audit`, with `literature-and-evidence` when needed |
| Make a major revision | I want to restructure the paper toward [goal]. Preserve a baseline and propose a revision plan. Wait for my confirmation before editing the text. | `manuscript-revision` |

For example, first request an introduction audit. After reading the findings, say:

> Fix the wording problems you identified, only in the introduction. Keep the scientific meaning and recheck those findings after editing.

Sentence, paragraph, and section requests stay within the named text. Changes to the main claim, structure across sections, or evidence base use a recoverable baseline and revision plan. You confirm scientific choices. A check-only request does not edit the text. Before a rewrite, the assistant keeps a copy; afterward, it compares data, citations, and conditions with the original. Evidence gaps remain visible.

Every manuscript write includes a check and synchronization of the internal argument graph and reasoning register: premises, analysis, inferences, judgments, and limits. Direct author edits are inspected at the next check. These internal records stay out of submission text. See [the internal argument framework](docs/logic-map-guide.md). A one-time edit does not become a lasting writing rule.

### 5. Save, compare, and recover with Git

Describe what you want to keep or recover. The assistant operates Git.

| Need | Prompt | Skill |
| --- | --- | --- |
| Set up version history | Set up local version history for this paper and explain what it will include. | `git-setup` |
| Check saved work | Is my work saved? What changes are still unsaved? | `git-inspection` |
| Save progress | Save this version of the paper and summarize the main changes. | `git-save` |
| Save selected work | Save only the introduction revised in this task. | `git-save` |
| Compare versions | Compare the current work with the last saved version. | `git-compare` |
| Retrieve earlier content | Find [section/passage] before the changes. Retrieve a separate copy first; do not overwrite the current text. | `git-recovery` |
| Restore a version | I want to restore [file] to [date or version]. Show what would be replaced and wait for my confirmation. | `git-recovery` |

The assistant checks the save scope, secrets, and large files. First-time setup may need an author name and email for versions. After saving, it reports the version identifier and remaining unsaved work. Recovery retrieves a separate copy by default. Before replacing current files, the assistant shows the scope, waits for your explicit choice, and keeps the current content. Version history is not rewritten.

**A local save is not an external backup.** For a backup, name the destination and permitted material. The assistant uses `git-backup` and checks the result.

### 6. Resume, prepare output, and find files

When you return, say:

> Continue from the project records. Check the current files and unfinished work first.

The assistant uses `paper-hands-on` to inspect records and actual files. You can also ask directly:

> Format the manuscript using these journal instructions and inspect the Word output.

> Organize this review round and help me prepare point-by-point responses.

These start `submission-assembly` and the review workflows. Scientific judgments and submission choices remain yours.

| Folder | Contents |
| --- | --- |
| [requirements/](requirements/README.md) | Confirmed goals, languages, writing, privacy, and output requirements |
| [inbox/](inbox/README.md) | Optional entry point for incoming materials |
| [manuscript/](manuscript/README.md) | Text, outline, internal argument map, figures, and assembly manifest |
| [references/](references/README.md) | Original sources, extracted text, bibliography, and evidence notes |
| [ideas/](ideas/README.md) | Research ideas you choose to keep |
| [research/](research/README.md) | Plans, decisions, feedback, results, and provenance |
| [reviews/](reviews/README.md) | Review letters and responses by venue and round |
| [revisions/](revisions/README.md) | Baselines, candidate drafts, and major revision records |
| [outputs/](outputs/README.md) | Rebuildable previews and preserved release packages |
| [state/](state/README.md) | Current progress, open issues, and next action |

More help: [operation guides](docs/README.md) · [capabilities and limits](docs/capabilities.md) · [MCP setup](mcp/README.md) · [document processing](docs/mineru-integration.md) · [manuscript and output conventions](docs/markdown-and-export-conventions.md).
