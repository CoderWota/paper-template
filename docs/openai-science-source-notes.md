# Public evidence for transferring AI-assisted research practice

Status: research note for design discussion; no architecture or dependency is adopted by this note.

Checked: 2026-10-26. Scope: public OpenAI research reports, linked manuscripts, and first-party research repositories. This is a selected source review, not an exhaustive survey or a correctness review of the mathematics and biology.

## What the evidence supports

Public materials contain useful, concrete research practices. They support delegating substantial retrieval, coding, analysis preparation, exploration, and manuscript preparation to agents. They do not disclose a complete internal operating procedure that can be copied into this template. An output collection, an evaluation result, a formally checked theorem, a preprint, and a journal-accepted article establish different things.

The proposed division of work is therefore credible: the researcher supplies scientific direction, chooses among consequential alternatives, and judges the scientific meaning; the agent carries technical and administrative work through to inspectable artifacts. The remaining design task is to make those artifacts and checks easy to review without requiring the researcher to become a programmer. This conclusion is a design inference from the sources below.

## Sources and publication status

| Source | Date or version checked | What this source establishes |
| --- | --- | --- |
| [Sharing AI progress in mathematics](https://openai.com/index/sharing-ai-progress-in-mathematics/) and [openai/math](https://github.com/openai/math) | Announcement 2026-10-06; announcement updated 2026-10-15; repository checked 2026-10-26 | Released mathematical manuscripts and proof artifacts, with varying verification status. This is not evidence that the collection has passed journal peer review. |
| [Scientific computing in the age of agentic AI](https://openai.com/index/scientific-computing-agentic-ai/) and its [field report](https://cdn.openai.com/pdf/scientific-computing-in-the-age-of-agentic-ai-an-exploratory-field-report.pdf) | Announcement 2026-07-28; [bioRxiv v2](https://www.biorxiv.org/content/10.64898/2026.07.29.741496v2.full) posted 2026-08-05 | Exploratory case reports. The available manuscript record is a preprint; the cases are not a controlled estimate of general agent productivity. |
| [Early science acceleration experiments with GPT-5](https://arxiv.org/abs/2511.16072) | Initial submission 2025-11-20; [v1 full text](https://arxiv.org/html/2511.16072v1) | A cross-disciplinary case-study preprint that separates rediscovery, literature search, collaboration, and new results. |
| [Point Convergence of Nesterov's Accelerated Gradient Method: An AI-Assisted Proof](https://arxiv.org/abs/2510.23513) | v1 2025-10-27; v2 2026-01-19 | Research preprint with a detailed account of human–AI collaboration and a correction to an earlier subsidiary claim. No journal reference was displayed in the checked arXiv record. |
| [Single-minus gluon tree amplitudes are nonzero](https://arxiv.org/abs/2602.12176) | v1 2026-02-12; v2 2026-03-09 | Research preprint. No journal reference was displayed in the checked arXiv record. |
| [Using a GPT-5-driven autonomous lab to optimize the cost and titer of cell-free protein synthesis](https://www.biorxiv.org/content/10.64898/2026.02.05.703998v1) | Posted 2026-02-05; [full manuscript](https://cdn.openai.com/pdf/5a12a3bc-96b7-4e07-9386-db6ee5bb2ed9/using-a-gpt-5-driven-autonomous-lab-to-optimize-the-cost-and-titer-of-cell-free-protein-synthesis.pdf) | Lab research preprint describing a closed experimental loop with substantial physical infrastructure. |
| [Our First Proof submissions](https://openai.com/index/first-proof-submissions/) | 2026-02-20 | Public proof attempts and evolving correctness assessments for research-level evaluation problems. This is not journal acceptance or evidence of fully autonomous publication. |
| [Distributed AI agents enable comprehensive discovery of biological insights at scale](https://www.biorxiv.org/content/10.64898/2026.10.15.759436v1), [official account](https://openai.com/index/scaling-ai-research-for-complex-biological-data/), and [research code](https://github.com/jinlabneurogenomics/distributed_agent) | Preprint identifier dated 2026-10-15; OpenAI account 2026-10-21 | A biological interpretation preprint and reproducibility artifacts. The preprint server returned HTTP 403 during this review; process claims below are limited to the accessible official account and repository. |

These status labels describe the records inspected. An absent journal reference is not proof that no later acceptance exists. No checked source establishes a discipline-independent, end-to-end guarantee of submission readiness or acceptance.

## Concrete process evidence

### 1. A large manuscript collection is useful evidence, with important selection and correction records

The current `openai/math` README lists 719 manuscripts in 372 result families, produced after approximately 4,000 attempted problems. It reports an average of three hours of ChatGPT Pro thinking compute per result, using an unreleased internal model. It publishes only ten abridged reasoning summaries, describes varying verification status, and reports that approximately 42% of top-line results have formalizations. The procedure and model are therefore only partly transferable from public materials. [Repository README](https://github.com/openai/math#readme)

Its history records three withdrawals after a sign error broke a construction and two dependent papers, fourteen other manuscript repairs, and thirteen downstream citation/version updates. Previous versions remain available. [Correction history](https://github.com/openai/math/blob/main/history.md)

**Design inference:** preserve the relationship between a result and the results, data, citations, and assumptions it depends on. A correction must trigger review of affected manuscript claims and outputs. Do not count manuscripts as independent discoveries, equate formalization coverage with journal review, or treat a selected success collection as a success probability for a new project.

### 2. The strongest scientific-computing workflow transfers engineering work to agents and makes correctness observable

The July field report describes eight projects, including Codex-only and combined Codex/Claude Code work. Researchers generally defined the tasks and judged scientific validity; agents supplied implementation effort. MHCflurry's backend migration was checked against existing predictions. Other projects used reference outputs, simulated data, statistical behavior, and representative workloads. The report's author-contribution statement assigns study coordination and the initial manuscript to human authors, with case reports and manuscript review from the contributors. [Field report, overview, author contributions, and case-study appendices](https://cdn.openai.com/pdf/scientific-computing-in-the-age-of-agentic-ai-an-exploratory-field-report.pdf)

The accompanying account emphasizes staged iteration and the difficulty of numerical differences and realistic edge cases. Confident agent self-assessment was not reliable completion evidence. [Official account](https://openai.com/index/scientific-computing-agentic-ai/)

**Design inference:** define the observable research outcome before execution. Have the agent build and run the checks, investigate discrepancies, and deliver a compact evidence report. The researcher reviews the scientific adequacy of the checks and implications of the results, rather than manually fixing package installations or comparing generated CSV files.

### 3. Successful mathematical collaboration included failed candidates, simplification, and a correction

Jang and Ryu describe an interactive search in which approximately 80% of candidate arguments were incorrect. Humans filtered arguments, consolidated valid facts, and selected directions; a simplified continuous-time problem made progress possible. The paper also states that an earlier subsidiary result for the subcritical regime was entirely invalidated because plausible model-generated arguments received insufficient scrutiny. This correction does not withdraw the principal convergence result. The original discovery is not reproducible simply by rerunning its prompt: the original model is unavailable, and later models may encounter the published solution. [Paper v2, Sections 4–4.3](https://arxiv.org/html/2510.23513v2)

The public interview separately reports that Ryu developed and wrote the traditional paper, and found fresh conversations useful for checking work. That is a case-specific writing division, not a requirement that future researchers manually prepare all prose. [Official researcher account](https://openai.com/index/gpt-5-mathematical-discovery/)

**Design inference:** let agents explore bounded alternatives and produce reviewable reasoning. Use a fresh verification context as one additional check, with explicit assumptions and evidence. Another model's agreement must not substitute for a proof check, external reference, empirical test, or expert judgment. Validate secondary claims as carefully as principal claims.

### 4. The physics result combined human-selected structure, model discovery, and multiple checks

The authors calculated low-order cases and the model proposed a simpler general expression. An internal model supplied a proof; the paper reports hand checks using a recursion and several independent consistency identities. The selected physical regime and the humans' base calculations were important inputs. [Paper v2, introduction and derivation](https://arxiv.org/html/2602.12176v2)

OpenAI's account identifies the internal scaffolded model's extended reasoning and makes clear that the released artifact was a preprint submitted for publication. It does not disclose a generally available package reproducing the internal scaffold. [Official account](https://openai.com/index/new-result-theoretical-physics/)

**Design inference:** supply the agent with explicit assumptions, simple cases, limiting cases, and known constraints. For a theoretical result, an automated symbolic check can supplement the argument. It cannot establish every mathematical condition of the theorem.

### 5. Early cross-disciplinary reports distinguish hypothesis generation from experimentally new evidence

The early-science report's immunology case supplied an unpublished figure from an existing laboratory program. Several proposed explanations and predictions could be compared with experiments the lab had already performed; it was not a fresh autonomous experimental program generated from a blank workspace. Other chapters distinguish rediscovery from new mathematical results and include expert checks. [Early-science report, Sections I.3 and IV](https://arxiv.org/html/2511.16072v1)

**Design inference:** an idea-development skill should label retrospective agreement, a newly proposed hypothesis, an experiment not yet performed, and an observed new result separately. Figures digitized from an image must not silently become authoritative raw observations. The workspace should help the researcher choose the next informative test rather than reward a plausible narrative alone.

### 6. An autonomous laboratory relied on a narrow task, a validated interface, and substantial external resources

The CFPS work connected GPT-5 to a custom cloud-lab interface. Structured validation checked experiment specifications; software translated them into robotic protocols and returned measurements. Humans prepared and handled reagents and consumables and addressed instrument-related variability. The study ran six rounds over six months; some mechanistic interpretations remained hypotheses requiring further validation. [Full manuscript, methods, results, and discussion](https://cdn.openai.com/pdf/5a12a3bc-96b7-4e07-9386-db6ee5bb2ed9/using-a-gpt-5-driven-autonomous-lab-to-optimize-the-cost-and-titer-of-cell-free-protein-synthesis.pdf)

The official account reports more than 36,000 unique reaction compositions and explicitly limits the demonstrated optimization to a particular protein and CFPS system. [Official account](https://openai.com/index/gpt-5-lowers-protein-synthesis-cost/)

**Design inference:** separate proposed work, executed work, returned observations, and validated conclusions. A laptop can prepare analysis and coordinate a permitted remote execution; the template cannot provide lab access or physical experiments by creating directories. Define resource limits, objective measures, and stopping conditions before an agent begins expensive work.

### 7. First Proof shows why an apparent success needs a changeable validation state

The February announcement reports that an attempt initially considered likely correct was later judged incorrect after external feedback. It also describes manual strategy suggestions, clarification after expert feedback, and use of another model for verification and presentation. Its prompt appendix contains representative patterns intended to simulate those manual interactions, not a complete original interaction log. [Official announcement and linked attempts](https://openai.com/index/first-proof-submissions/)

**Design inference:** a workspace should report what was checked, by what method, and what remains open. Preserve rejected or superseded results when they explain a consequential decision. Do not promote a model's internal confidence, repeated self-review, or an illustrative reconstructed prompt into proof of an autonomous successful research run.

### 8. Recent distributed biological reasoning offers a reproducibility pattern, rather than a default requirement for thousands of agents

The October account describes agents assigned to separate perturbations, each connecting cellular responses with literature and proposing explanations. Their reports were synthesized into a reasoning atlas. The reported leads require follow-up experiments; blinded expert preference for reports is not biological validation of every proposed mechanism. [Official account](https://openai.com/index/scaling-ai-research-for-complex-biological-data/)

The public repository separates saved reports, prompts, and run measurements from reference inputs, prepared tables, and figure notebooks. It says the saved manuscript analyses can be regenerated without model calls or API keys. Its full-atlas setup downloads a pinned 10.8 GB file and needs about 35 GB of free space; hosted read-only access omits raw-data recomputation. [Research repository, data and manuscript-analysis instructions](https://github.com/jinlabneurogenomics/distributed_agent#readme)

**Design inference:** save expensive model outputs as inputs to deterministic analysis, and distinguish browsing existing findings from recomputing them. Separate independent questions when this improves evidence coverage, but make serial execution and limited concurrency sufficient for the template. Do not assume thousands of cloud workers are available to an ordinary researcher.

## Transfer recommendations for this workspace

The following are proposals for discussion. They are derived from the evidence, not descriptions of an unpublished OpenAI procedure or already approved template architecture.

| Required behavior | Agent's work | Researcher's decision or review | Evidence to retain |
| --- | --- | --- | --- |
| Convert an idea into a researchable question | Compare nearby work, expose assumptions, propose distinct routes, identify a useful first test | Select the question, intended contribution, and material limits | Confirmed question, comparison with prior work, rationale |
| Define what would establish the claim | Propose suitable data, analysis, proof obligations, comparisons, and failure criteria | Confirm consequential method and interpretation choices | Plan with assumptions and observable checks |
| Carry the research task through to results | Obtain permitted materials, clean and inspect data, write and run code, record failures, produce analyses | Supply inaccessible inputs, approve material scope changes, judge meaning | Preserved inputs, reusable code, parameters, run records, results |
| Challenge results before drafting conclusions | Check sources and methods; run sensitivity, baseline, limiting-case, or counterexample checks as appropriate | Assess whether the evidence supports the contribution | Check outputs, unresolved issues, alternative explanations |
| Connect results to the paper | Maintain links from claims to sources, analyses, figures, and assumptions | Approve substantive claims and the argument | Traceable result and claim records; source locators |
| Produce the manuscript and journal package | Draft and revise prose, citations, figures, tables, supplementary files, and formatting; validate each output | Exercise authorial control and approve the final scientific narrative | Editable manuscript, checks, inspectable submission package |
| Respond to feedback and corrections | Assess affected claims, update dependent artifacts, explain actual changes, preserve earlier releases | Choose consequential changes and approve responses | Attributed feedback, decision rationale, versioned changes |

The user should not have to copy data between folders, repair BibTeX, edit configuration formats, re-run scripts manually, or interpret stack traces to complete these tasks. The agent should present a short research-facing review: what changed, what supports it, what is uncertain, and which decision is needed. A requirement for scientific review is not a reason to send technical execution back to the researcher.

Keep one small, completed research task as an acceptance scenario: a permitted input and confirmed question should lead to inspectable analysis, source-backed prose, checked figures, and a properly assembled output. A directory tree or a collection of skill descriptions cannot demonstrate this outcome.

## Lightweight Windows constraints

These are proposed implementation constraints, rather than performance claims verified by the cited studies:

- Treat the laptop as the project workspace and control point. Do not require local model inference, a GPU, a cloud-lab subscription, or a multi-agent cluster.
- Run small checks locally and make larger computation optional. Have the agent explain the data, runtime, cost, and service implications before a consequential choice; preserve existing confirmed authorization within its scope.
- Download only the data needed for the task. Inspect size and available storage first; support cached inputs, resumed downloads, and small representative checks.
- Retain model-generated working outputs and deterministic analysis inputs so figure or table rebuilds do not repeatedly consume model calls.
- Maintain separate states for a plan, a run attempt, observed results, checks, and author-approved claims. An unavailable remote service must leave a recoverable task, not a fabricated result.
- Test the actual supported Windows architecture and office/export path. Neither the sources reviewed here nor execution on this maintainer's Mac proves Surface or Windows ARM compatibility.

## Evidence gaps and claims to avoid

No complete public internal playbook was found. The current mathematical collection uses an unreleased model and selected outputs, with only partial process disclosure. The cases span different scientific tasks, resources, and verification methods; they cannot be reduced to a single productivity number or a guarantee that an ordinary user can finish any study without domain expertise.

This review did not independently verify the mathematical proofs, reproduce the lab experiments, obtain journal acceptance records for all manuscripts, or test the software on Windows. The distributed-biology preprint itself was inaccessible in this tool session; the repository and official account were read, and no full-text-only claim is asserted here. The full First Proof PDF was intermittently inaccessible; the official announcement is the basis for the process and correction claims above.

The useful transfer is a reviewable research process with explicit evidence, suitable tools, controlled execution, preserved artifacts, and consequential human decisions. It is not an assertion that the template inherits the capabilities, compute, unpublished scaffolds, or publication record of OpenAI's research collaborations.
