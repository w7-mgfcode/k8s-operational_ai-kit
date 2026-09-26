# Rules & Constraints

> The full constraint matrix, and which rule owns which path.
> Normative text lives in `.claude/rules/`. This file is the map, not a copy.
> Last generated: 2026-09-21.

## Rule Set

Each file carries a `paths:` frontmatter glob. Claude Code loads it automatically on a match;
other agents consult `.claude/rules/README.md` and read the matching rule by hand.

| Rule | Owns | Load when |
| --- | --- | --- |
| `anonymization.md` | `ai-engineering-knowledge-cards/**`, `.gitignore` | Writing anything publishable; touching `.gitignore` |
| `cards.md` | `cards/**`, `templates/**`, `docs/**` | Authoring or editing a card, or changing the template |
| `skeletons.md` | `skeletons/**` | Writing or changing a prototype |
| `git-workflow.md` | `.claude/**`, `.github/**`, `ai-engineering-knowledge-cards/**` | Committing anything |
| `subagents.md` | `.claude/agents/**` | Changing a subagent definition |
| `skills.md` | `.claude/skills/**`, `.agents/**` | Changing an installed skill |

## Hard Constraints

Violating any of these is a defect, not a judgment call.

| # | Constraint | Enforced by |
| --- | --- | --- |
| 1 | `.legacy-assets/` is never a source for published output | Human discipline only |
| 2 | No masked identifier in any published file | `check.py` (shapes) + human review (names) |
| 3 | A card has exactly 13 `##` sections and 6 frontmatter keys in order | `check.py` |
| 4 | A card's number matches its filename; `layer` and `maturity` are from the closed sets | `check.py` |
| 5 | Every card has a skeleton directory with a conforming README | `check.py` |
| 6 | Skeleton scripts import standard library only | `check.py` |
| 7 | Every relative Markdown link resolves | `check.py` |
| 8 | A skeleton is runnable as committed and leaves the tree clean | `check.py --run`, partly |
| 9 | No virtualenv, `__pycache__`, `.env`, token or credential is committed | `.gitignore` |
| 10 | Conventional Commits, one scope taxonomy, `Context:` trailer for agent assets | Human discipline only |
| 11 | No direct commits to the default branch without being asked | Human discipline only |

## Soft Constraints

Deviating needs a reason, not permission.

- Cards run to roughly 230 lines. Shorter usually means a section was skipped; much longer
  usually means two patterns.
- `maturity: partial` is expected on a meaningful share of cards. A set that is entirely
  `proven` is a set that stopped being honest.
- Failure-modes rows are observed or structurally inevitable — never hypothetical.
- Skeletons stay minimal. A skeleton with nine scripts has become a project.

## What is Deliberately Absent

Do not add these without being asked. Their absence is a decision.

| Absent | Why |
| --- | --- |
| Build system (`Makefile`, `package.json`, `pyproject.toml`) | Nothing to build. `check.py` is the whole toolchain |
| Linter / formatter | The content is prose and stdlib Python; a linter would generate noise, not signal |
| Test framework | The skeletons are the tests; `check.py --run` executes them |
| Dependencies | The stdlib-only rule is the skeleton contract, not a preference |
| `docs/_kB/repo-map/` | The structured KB was never generated for this repo; its only possible input is the excluded legacy tree |

## Known Open Items

Carried forward rather than hidden.

1. **Branch name.** The working branch is `master`; `main` is the intended default.
   `ci.yml` triggers on push and pull request to both, and the three agent workflows are
   event-triggered, so no workflow is blocked by the name. Unresolved by design — renaming a
   branch is the user's call.
2. **`INDEX.md` drift.** It restates each card's `maturity` and a maturity count. Nothing checks
   that against the cards' frontmatter.
3. **Deferred rules.** `.claude/rules/README.md` lists concerns not yet governed by a rule —
   the agent-instruction layer and CI gates (both owed), hooks and permissions, and the parts of
   structural lint `check.py` does not yet apply to itself
   (its own card 15).
4. **Three agent workflows are broken, not inert.** They assume npm and secrets that do not
   exist here, and each fails as soon as it runs:
   - `claude-review` runs on **every** pull request opened or marked ready, with no comment
     gate. `setup-node` with `cache: npm` fails without a lockfile, so the first PR goes red.
   - `claude-create` runs only on a trusted `@claude` comment, then fails at the same
     `setup-node` cache step or at `npm ci`.
   - `codex-create-deterministic` runs only on a trusted `@codex-create` comment; the global
     Codex install works, and the run fails without `OPENAI_API_KEY`.
