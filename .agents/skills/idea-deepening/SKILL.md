---
name: idea-deepening
description: Challenge an existing research idea or question against evidence, alternatives, nearest work, and feasibility.
---

# Idea deepening

Outcome: a clearer idea: its question, intended contribution, assumptions, nearest prior work and the concrete difference from it, alternative explanations or interpretations, feasibility, the route to evidence or argument, and the next check. When the idea is retained, its note in `ideas/` holds the result.

## Step 1: Prepare before you ask

1. Identify the idea: the researcher's words, or a note in `ideas/`. Read that note, its linked source notes, search records, and result records, `requirements/project.md`, and `state/current.md`.
2. List the open points in dependency order: question, contribution, assumptions, nearest prior work, alternatives, feasibility, route to evidence or argument, next check. Resolve first the points that the others depend on.
3. Before each question, check whether the workspace or an authorized search can answer it. Do that retrieval yourself with `literature-and-evidence`, `research-investigation`, or `literature-discovery` within its confirmed scope. Ask the researcher only for judgments, intentions, and facts that only they have.

## Step 2: Examine one point at a time

4. Ask one substantive question per turn, in the shared question form: the point, why it matters, your recommendation and its reason, then the question. Wait for the answer before you build on it.
5. Challenge a weak premise directly: name the assumption, the evidence against it or missing for it, and what would change your view. Grilling means focused examination. It never means pressure, a long questionnaire, or deciding for the researcher.
6. Compare the nearest prior work that was actually inspected: what it did, how the idea differs concretely, and how certain that difference is given the search scope. Call the originality assessment preliminary when coverage is limited. A different title or an empty search result is not novelty. Never invent a gap, a source, or a finding.
   Present the overlap and difference with source locators and access limits, not a novelty score or binary verdict. State which assumption or alternative a concrete next check would distinguish; do not manufacture a rival account solely to fill a comparison.
7. Keep four questions apart: novelty (what is new compared with inspected work), significance (who would care and why; `impact-assessment` goes deeper), feasibility (resources, access, skills, time, cost), and support (what evidence exists or would be needed). A replication or a negative result need not be presented as novelty.
8. Offer alternatives where they help: a rival explanation or interpretation, a narrower or broader question, or a different kind of contribution.

## Step 3: Checkpoints and stopping

9. At natural checkpoints, summarize what is settled (in the researcher's words), what is open, and what evidence is pending.
10. Stop when a useful next action is clear, when the researcher wants to switch tasks, or when the next questions need evidence that does not exist yet. Name that next action.
    In a broader authorized task, this ends the interview, not the whole task: hand the settled question, inspected comparisons, remaining hypotheses, and next check to the owning skill and continue within scope. A scientific choice still awaiting confirmation blocks its dependent action.

## Step 4: Record

11. When the idea is retained, update its note with the layout in `ideas/README.md`: settled points with the researcher's words, compared prior work with links and the search scope, assumptions, open questions, and the next check. Keep text that the researcher wrote. Set the status to `developed` when the question, the contribution, and the next check are clear. When the idea is not retained, offer once to keep it; save nothing without a clear yes.
12. A choice that changes the research question, the main claim, the method, or the material scope is a major decision: ask the confirmation question, then record it with `constraint-maintenance`, which writes the requirement and the decision record. An answer to a deepening question is not a decision record by itself.
13. Review facts reported by `python scripts/research.py check`, such as broken links. Repair a broken link when it is within scope; the command does not validate the form or quality of the idea note.

## Completion check

- Each question examined one point, gave a recommendation with its reason, and waited for the answer.
- Facts that the workspace or an authorized search could supply were looked up, not asked for.
- Novelty, significance, feasibility, and support are stated separately; originality is qualified by the actual search scope.
- No source, gap, or finding was invented, and no answer was turned into a rule or a decision without confirmation.
- The idea note, if any, holds the settled points in the researcher's words. Any reported link issue was reviewed and resolved or disclosed.
