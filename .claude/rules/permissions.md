---
paths:
  - ".claude/settings.json"
  - ".claude/hooks/**"
---

# Permissions and Hooks

`.claude/settings.json` exists for one boundary: `.legacy-assets/` is readable by
every agent, and nothing under it is ever written or tracked
([`anonymization.md`](anonymization.md)). Everything in it serves that boundary.
Add nothing here that does not.

| Setting | What it does | Strength |
| --- | --- | --- |
| `permissions.allow: Read(/.legacy-assets/**)` | States that reading the tree is intended | Grant. Ignored in a workspace Claude Code has not trusted |
| `permissions.deny: Edit(/.legacy-assets/**)` | Blocks Edit, Write and NotebookEdit there. `Edit` covers all three; a `Write(...)` rule would be ignored | Enforced by the harness. Deny beats any allow |
| `hooks.PreToolUse` on `Bash` → `.claude/hooks/guard_legacy_assets.py` | Blocks shell commands that redirect into the tree, write, move, delete or stage under it, copy into it, run `git clean -x`, or do any of these from inside it | Enforced, but on command **text**. A script that opens a file there itself passes |
| `claudeMdExcludes: **/.legacy-assets/**` | Stops the tree's own `CLAUDE.md` and `.claude/rules/` loading when a file in it is read | Enforced. Tested: without it, one read loaded five of that tree's rule files |

A leading `/` anchors a permission path at the project root; this was verified in a
scratch repository, not assumed.

## What it does not cover

- **Other agents.** Copilot, Codex and the CI agent workflows read none of this.
  For them the boundary is an instruction in `AGENTS.md` and their adapters.
- **Indirect writes.** Permission rules do not see a subprocess opening a file,
  and the hook sees only the command line. The guard is a seatbelt, not a sandbox.
- **Tracking.** That is `.gitignore` plus `check.py`, which fails if git tracks any
  path under the tree or the ignore line disappears.

## Changing it

- Run the hook's behaviour against both lists before committing: writes that must
  be blocked, reads that must pass. A guard that blocks `cat` is a guard someone
  disables.
- Hooks fail open on malformed input. Keep it that way: a broken guard must not
  block every shell command.
- Skill `allowed-tools` was revisited when this file landed, as `skills.md`
  required. It stands: it grants a skill its tools, the documented precedence is
  deny over allow, and the hook runs on every Bash call whatever granted it. The
  deny rule has not been tested against a skill's grant specifically.

Related: [`anonymization.md`](anonymization.md), [`skills.md`](skills.md),
[`git-workflow.md`](git-workflow.md).
