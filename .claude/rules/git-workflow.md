---
paths:
  - ".claude/**"
  - ".github/**"
  - "ai-engineering-knowledge-cards/**"
---

# Git Workflow

Conventional Commits. One commit is one logical unit — if the subject needs an
"and", it is two commits.

```text
<type>(<scope>): <description>
<type>(<scope>): <description> (#<issue>)
```

Branch: `<type>/<scope>-<slug>`, or `<type>/<scope>-<issue>-<slug>`.
Branch scope and commit scope are the same word. One taxonomy, defined once here.

## Types

`feat` `fix` `docs` `chore` `refactor` `test` `ci`

## Scopes

| Scope | Covers |
| --- | --- |
| `cards` | `ai-engineering-knowledge-cards/cards/**`, `templates/**` |
| `skeletons` | `ai-engineering-knowledge-cards/skeletons/**` |
| `docs` | `ai-engineering-knowledge-cards/docs/**`, README, INDEX |
| `agents` | `.claude/**`, `.agents/**`, root `AGENTS.md` and `CLAUDE.md` |
| `ci` | `.github/**` |

Pick the scope that owns the **blast radius**, not the file count. A one-line
edit to `templates/CARD_TEMPLATE.md` is `cards`, because it changes the contract
every card obeys.

Examples:

```text
feat(cards): add card 14 index-guided retrieval
fix(skeletons): make compile.py idempotent on repeated runs (#3)
docs(docs): record the anonymization rule for .legacy-assets
chore(agents): delete the three imported intentguard-docs rules
```

## The `Context:` trailer

**Required when a commit changes agent-context assets** — anything under
`.claude/rules/`, `.claude/agents/`, `.claude/skills/`, `.agents/`, or a root
`AGENTS.md`. It records what an agent reading this repo later will now see
differently. It names the change in the agent's terms, not the diff's.

```text
Context: deleted components.md and generated-docs.md (imported from
intentguard-docs; 0/6 globs matched). Added anonymization.md (paths:
ai-engineering-knowledge-cards/**) and indexed it in README.md.
```

## Prohibited

- Committing directly to `main` unless the user explicitly asks. Branch first.
- Bundling an unrelated fix into a feature commit.
- A `Context:` trailer that restates the diff instead of naming what changed for
  the next agent.
- Committing anything [`anonymization.md`](anonymization.md) excludes. Check the
  staged diff, not the working tree.

Note: the branch is currently `master` while `main` is the intended default.
`ci.yml` triggers on both; renaming is the user's call. Either way, branch first.
