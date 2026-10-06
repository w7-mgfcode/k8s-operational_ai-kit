---
paths:
  - ".claude/agents/**"
---

# Subagents

Three subagents live in `.claude/agents/`. Each exists to do work in an **isolated
context** and hand back a dense report — that is the whole value. A subagent that
returns raw file dumps has wasted the isolation.

| Agent | For | Not for |
| --- | --- | --- |
| `codebase-analyst` | Depth on one system: how it works, where it will bite | Fast breadth; judging a diff |
| `research-agent` | Fast breadth, several instances in parallel | Deep single-system analysis |
| `code-reviewer` | Judging a finished diff against this repo's standards | Exploration |

Their roles must stay distinct. If two agents would answer the same question,
one of them is redundant.

## Writing one

- **`tools:` is a narrowing, not a grant.** It restricts what the subagent may
  use. Keep read-only agents on `Read, Grep, Glob`; add `Bash`, `WebSearch`, and
  `WebFetch` only when the role genuinely needs them. A skill's `allowed-tools`
  is the opposite mechanism — see [`skills.md`](skills.md).
- **The `description` is the routing signal.** It is what the dispatching agent
  matches on, so it must say when to reach for this agent *and when not to* —
  name the sibling that fits better. Include worked examples.
- **State the repo's shape up front.** This repository publishes anonymized
  AI-engineering pattern cards extracted from a private agent kit. It has no
  application code, no `package.json`, no build, and no test suite. Content is
  Markdown cards under `ai-engineering-knowledge-cards/cards/` and stdlib-only
  Python skeletons beside them. `.legacy-assets/` is readable, never written —
  see [`anonymization.md`](anonymization.md). An agent missing this context reports
  the absence of a linter or a test runner as a finding.
- **Cite or admit.** Every claim carries `path/to/file.ext:line`, or is explicitly
  flagged unverified. Confident-but-wrong is the failure mode that makes a
  subagent worse than useless.
- **Read-only agents do not write code.** `codebase-analyst` and `research-agent`
  analyze and explain. `code-reviewer` reports findings and explicitly instructs
  the main agent not to fix anything without the user's approval.
- An agent judging card or skeleton content is bound by [`cards.md`](cards.md)
  and [`skeletons.md`](skeletons.md) — those define the standards it reviews
  against.

## Registering one

Adding an agent means adding a row to the table above, and naming it in its
siblings' descriptions. The `.claude/rules/README.md` row for this rule changes
only if its Covers text does. An agent nothing references will never be dispatched.

Subagents are Claude Code-only. No other tool in this repo has an equivalent, so
never make a procedure *depend* on one — name a subagent as an optimization
("where subagents are available…") and always state the sequential fallback.
