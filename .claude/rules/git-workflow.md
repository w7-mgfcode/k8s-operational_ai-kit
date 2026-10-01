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
| `cards` | `ai-engineering-knowledge-cards/cards/**`, `component-cards/**`, `templates/**` |
| `skeletons` | `ai-engineering-knowledge-cards/skeletons/**`, including `components/` and `pipelines/` |
| `docs` | `ai-engineering-knowledge-cards/docs/**`, README, INDEX, root `docs/_base/**` |
| `agents` | `.claude/**`, `.agents/**`, root `AGENTS.md` and `CLAUDE.md`, `.gitignore` |
| `ci` | `.github/**`, root `check.py` |

Pick the scope that owns the **blast radius**, not the file count. A one-line
edit to `templates/CARD_TEMPLATE.md` is `cards`, because it changes the contract
every card obeys.

Examples:

```text
feat(cards): add card 14 index-guided retrieval
fix(skeletons): make compile.py idempotent on repeated runs (#3)
docs(docs): record the anonymization rule for .legacy-assets
chore(agents): delete three imported rules whose globs matched nothing
```

## The `Context:` trailer

**Required when a commit changes agent-context assets** — anything under
`.claude/` or `.agents/`, a root `AGENTS.md` or `CLAUDE.md`, or
`.github/copilot-instructions.md`. It records what an agent reading this repo later will now see
differently. It names the change in the agent's terms, not the diff's.

```text
Context: deleted components.md and generated-docs.md (imported from
another repository; 0/6 globs matched). Added anonymization.md (paths:
ai-engineering-knowledge-cards/**) and indexed it in README.md.
```

## Prohibited

- Committing directly to `main` unless the user explicitly asks. Branch first.
- Bundling an unrelated fix into a feature commit.
- A `Context:` trailer that restates the diff instead of naming what changed for
  the next agent.
- Committing anything [`anonymization.md`](anonymization.md) excludes. Check the
  staged diff, not the working tree.

The default branch is `main`, and `ci.yml` runs the gate on every push and pull
request to it. Work reaches `main` by pull request.
