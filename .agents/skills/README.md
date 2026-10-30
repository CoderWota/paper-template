# Research Task Skills

These 36 packages provide independent tasks that a researcher can request in ordinary language. Each directory contains a `SKILL.md` with its name, concise trigger description, essential procedure, and completion criteria. Read only the matching task and the references needed for that request.

## Maintain one source

This directory is the only editable skill source. Claude Code copies are generated in [`.claude/skills/`](../../.claude/skills/README.md). After any source change, run `python scripts/sync_skills.py`, then `python scripts/sync_skills.py --check`. Keep generated copies committed so a normal download works without symlinks.

Use portable `name` and `description` frontmatter. Keep descriptions focused on the task and its boundary, normally at most 180 English characters. The root contract supplies shared constraints; do not repeat it in each skill. Move lengthy commands or conditional modes to linked references, retaining essential safeguards in the entrypoint. Short skills need no extra files.

Maintain a short English README for a new package or supporting directory. Keep automatic selection enabled and task names stable. [Capabilities and operational limits](../../docs/capabilities.md) are available when a task's support or setup is uncertain; they are not startup context. [Loading guidance](../../docs/context-loading.md) explains both clients' discovery and adapter behavior.
