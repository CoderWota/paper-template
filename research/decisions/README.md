# Research Decision Records

Short records of consequential research choices you have confirmed, for example narrowing the research question, choosing a method, setting corpus or inclusion boundaries, excluding an analysis, changing the central argument, or choosing the target venue. A record is written only when revisiting the choice would be costly and its reasons matter. Ordinary wording edits, imports, and renames do not get one. A writing rule or a language setting is a requirement, not a decision: it goes in `requirements/` and gets no record.

## Contents

- [`index.md`](index.md): the list of decisions, their scope, and any later decision that replaces them.
- One record per decision, numbered in order, for example `0001-limit-corpus-to-2010-2024.md` (lowercase ASCII letters, digits, and hyphens).

## Record layout

The layout and labels below are suggestions. `python scripts/research.py check` follows recognized fields to check links between replaced decisions; unfamiliar labels and status words are ignored rather than rejected. Chinese equivalents such as `日期`, `状态`, `选择`, `适用范围`, `确认`, `取代`, and `被取代` are also understood.

```text
# 0002 <short title>

- Date: <YYYY-MM-DD>
- Status: active | replaced | withdrawn
- Choice: <the confirmed choice>
- Scope: <what it covers>
- Confirmed: <date>; "<your exact words>"
- Replaces: [0001](0001-....md)        only when it replaces an earlier decision
- Replaced by: [0003](0003-....md)     only when a later decision replaced it

## Context
## Reasons and alternatives      your reasons as given, or a statement that none was given
## Evidence and feedback         links to evidence notes, results, or feedback items
## Consequences                  what changes in the research and the manuscript
```

When a later decision replaces an earlier one, both records link to each other, the earlier one keeps its rationale with `Status: replaced`, and its line in `index.md` links to the replacement. Records are never deleted.

A decision records your choice; it is not evidence that the choice is scientifically valid. Current rules stay in [`requirements/`](../../requirements/README.md).

## Who edits what

The agent writes and maintains these records after you confirm a consequential choice. You do not need to learn a decision-record format.
