---
paths:
  - ".claude/skills/**"
  - ".agents/**"
---

# Skills and Vendored Agent Assets

## These are vendored copies, not managed installs

`.agents/articles/`, `.agents/commands/`, `.agents/examples/` and
`.agents/reference/` are a byte-for-byte copy of the agentic coding course repo —
all 23 files, verified with `cmp`. So are `.claude/.mcp.json` and several skills.
There is no `skills-lock.json` and no package manager tracking them. Nothing will
update them; nothing will revert your edits either.

Consequences that will bite:

- **`.claude/.mcp.json` points at `tooling/mcp/codebase_search.py`**, which
  exists in the course repo and not here. The `codebase-search` MCP server cannot
  start. Fix the path or drop the entry — do not debug it as a runtime problem.
- **`.claude/skills/maintaining-agent-docs` is a symlink outside the repository.**
  It resolves only on this machine. Any other clone gets a dangling link.
- **A 136 MB virtualenv exists twice.**
  `.claude/skills/excalidraw-diagram/references/.venv` and, since 2026-09-21,
  `.agents/skills/excalidraw-diagram/` — a full copy of the same skill, not a
  symlink. That is ~272 MB across two untracked-but-unignored directories. See
  [`anonymization.md`](anonymization.md) — never commit either.
- **A skill belongs in one place.** If a bundle must be visible to both Claude
  Code and other tools, symlink `.claude/skills/<name>` at
  `.agents/skills/<name>`; do not duplicate the tree. Two real copies drift, and
  a reviewer cannot tell which one is authoritative.

When you copy a skill in from elsewhere, record where it came from. An asset with
no provenance cannot be updated, audited, or safely deleted.

## `allowed-tools`

Six SKILL.md files here declare it in frontmatter: `analyzing-workflow-patterns`,
`preparing-skill-briefs`, `evolving-legacy-skills`, `writing-session-handoffs`,
`ai-layer-review`, `agent-browser`.

This is the documented mechanism and is fine. The rule this repo inherited
prohibited it on the grounds that it bypasses a reviewed ladder in
`.claude/settings.json` — there is no `settings.json` here, so the prohibition
had no basis and was unenforced anyway. **If a permission ladder is ever added,
this decision must be revisited in the same change, not inherited silently.**

## Writing a project-local skill

- The `description` is the routing signal — it decides whether the skill fires.
  Say when to use it *and when not to*, and name the sibling that fits better.
  This is card 03, implemented on itself.
- Keep procedure text in one place. If you edit the same instruction in two
  files, the duplication is the bug.
- A skill that operates on card or skeleton content is bound by
  [`cards.md`](cards.md) and [`anonymization.md`](anonymization.md).

See also [`subagents.md`](subagents.md) — a subagent's `tools:` is a *narrowing*
of what it may use; a skill's `allowed-tools` is a *grant*. Different mechanisms.
