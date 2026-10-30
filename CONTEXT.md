# Research Writing Workspace

Shared terminology for the manuscript, sources, decisions, and outputs in this research workspace. Read entries only when a term needs clarification.

## Participants and artifacts

**Researcher**:
The author directing the research ideas, scholarly judgments, final expression, and submission choices, without any assumed programming or software-engineering expertise. The researcher reviews and confirms meaningful outcomes; routine research support, document production, and technical coordination are delegated to the agent where feasible and authorized.

**Manuscript**:
The paper being developed, including its sections, figures, tables, citations, and supplementary material.
_Avoid_: Paper when it could mean a reference source.

**Reference source**:
A document or other research material collected for possible use in the manuscript, whether or not it is eventually cited.
_Avoid_: Citation when referring to an entire collected document.

**Original document**:
The archived source file as received, before conversion or annotation.

**Extracted content**:
A derived representation of an original document for reading and retrieval; it can contain extraction errors or omissions.

**Document intake**:
The receipt and identification of material intended for the workspace before its role and destination are settled; received material is not automatically adopted manuscript content.

**Manuscript adoption**:
The incorporation of an existing manuscript into a workspace's writing conventions, preserving its scientific content and identifying migration losses or unresolved items.

**Major manuscript revision**:
A coordinated, substantial change to an existing manuscript's argument, structure, evidence, or intended audience, whether initiated before submission or in response to feedback.

**Revision baseline**:
An identifiable, recoverable starting version of the manuscript and relevant inputs against which a revision's changes are assessed.

**Reference acquisition**:
Obtaining the available full text of selected reference sources; locating metadata or a landing page alone is not full-text acquisition.

**Citation**:
A reference in the manuscript identifying a source supporting or contextualizing a statement.

**Evidence locator**:
A reference to a specific passage, page, section, figure, table, or other identifiable location in a source.

**Writing constraint**:
A verified, researcher-confirmed requirement governing some aspect of the manuscript, such as language, terminology, argument, structure, or style. An agent's unconfirmed inference is not a writing constraint.

**Formulaic pattern**:
A wording or structural habit that adds emphasis, decoration, or generality without adding content, such as an inflated claim of significance, an uncited appeal to authority, or a stock connective at the start of every sentence. It is a signal for editing, not evidence of who wrote a text, and it governs writing only when the researcher confirms a rule about it.
_Avoid_: AI trace, when it implies a judgment of authorship.

**Style preset**:
An optional set of writing choices, such as tense, punctuation, or caption case, that applies to one scope of the manuscript only after the researcher chooses it. A venue requirement overrides it.
_Avoid_: Default style, when it suggests the choice was made for the researcher.

**Mock review**:
A simulated peer review of the researcher's own manuscript, scored on a venue's review form by several reviewer perspectives. Its scores are judgments tied to evidence in the workspace, not a forecast of the decision or a probability of acceptance.
_Avoid_: Predicted score, when it suggests a forecast of real reviews.

**Research decision record**:
A concise account of a consequential researcher-confirmed choice, its scope, rationale, and implications; it is distinct from evidence that the choice is scientifically valid.

**Research feedback**:
Attributed advice from a co-researcher, collaborator, coauthor, supervisor, or other contributor, retained as source material without automatically becoming a researcher decision or writing constraint. Eligibility does not depend on academic title or authorship status.

**Processing choice**:
A researcher's confirmed choice of where document parsing occurs, which service may receive documents, and which materials that choice covers.

**Training-use preference**:
A researcher's choice concerning a service provider's permission to use submitted content for model improvement. It is distinct from permission to process content and from data-retention requirements.

**Output profile**:
The requirements and formatting resources defining an intended manuscript output, such as a journal submission or thesis format.

**Submission round**:
A particular submission or revision event for a venue, with its own manuscript version and editorial correspondence.

**Idea**:
A researcher contribution that may be exploratory, developed, incorporated, or abandoned without necessarily being a verified scholarly claim.

**Result record**:
A record of one of the project's own results: its inputs, method or code version, parameters, run, outputs, checks, limitations, and the claims that use it. Its status distinguishes proposed, attempted, observed, checked, and failed work; a result whose inputs changed is stale until the work is repeated.
_Avoid_: Finding, for work that has not been checked.

**Code repository**:
A separate Git repository under `code/<name>/`, with its own history and instructions, brought in with the `code-import` skill. The workspace ignores its files and records which commit each run used.
_Avoid_: Project folder, when it could mean the whole workspace.

**Paper session**:
A session opened in the workspace root. It loads the workspace instructions and skills, reads code repositories as material, and records runs and results.

**Code session**:
A session opened inside a code repository. It does not load the workspace instructions or skills. It edits and tests the code and makes commits.

**Venue assessment**:
An examination of a journal or other venue from its current official sources, assessing the manuscript's fit separately from its impact and its readiness.
