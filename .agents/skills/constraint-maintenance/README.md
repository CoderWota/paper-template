# Constraint Maintenance

Keeps your confirmed requirements in one place, so that every later session, with any agent, follows the same rules. Tell the agent a lasting rule in ordinary words, for example "From now on, use British spelling in the manuscript," and it records the rule with its scope in `requirements/`.

## What to expect

- A clear instruction is enough; you are not asked to approve it again. A one-time request, such as "shorten this paragraph," does not become a rule.
- The agent never saves a guess about your preferences. If it notices a pattern in your edits, it may ask you once whether you want it as a rule.
- When a new rule conflicts with an existing one, the agent shows both and asks which applies. A replaced rule is removed; an important change also gets a short decision record in `research/decisions/`.
- Rules are written in your language. Examples and exceptions appear only when you give them or confirm them.
- A change to a requirement or to your research goal never edits your manuscript text on its own: the agent lists the passages that it affects and asks first.

Ask "Which writing rules apply to this paper?" at any time. The agent instructions are in [SKILL.md](SKILL.md). Related skills: `project-onboarding`, `privacy-configuration`, and `research-feedback`.
