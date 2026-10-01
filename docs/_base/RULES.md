# Rules & Constraints

> The full constraint matrix, and which rule owns which path.
> Normative text lives in `.claude/rules/`. This file is the map, not a copy.
> Last reviewed: 2026-10-01.

## Rule Set

Each file carries a `paths:` frontmatter glob. Claude Code loads it automatically on a match;
other agents consult `.claude/rules/README.md` and read the matching rule by hand.

| Rule | Owns | Load when |
| --- | --- | --- |
| `anonymization.md` | `ai-engineering-knowledge-cards/**`, `.gitignore` | Writing anything publishable; touching `.gitignore` |
| `cards.md` | `ai-engineering-knowledge-cards/{cards,templates,docs}/**` | Authoring or editing a card, or changing the template |
| `component-cards.md` | `ai-engineering-knowledge-cards/component-cards/**`, `…/templates/COMPONENT_CARD_TEMPLATE.md`, `…/skeletons/components/**` | Authoring a component card or its prototype |
| `skeletons.md` | `ai-engineering-knowledge-cards/skeletons/**` | Writing or changing a prototype |
| `git-workflow.md` | `.claude/**`, `.github/**`, `ai-engineering-knowledge-cards/**` | Committing anything |
| `subagents.md` | `.claude/agents/**` | Changing a subagent definition |
| `skills.md` | `.claude/skills/**`, `.agents/**` | Changing an installed skill |

## Hard Constraints

Violating any of these is a defect, not a judgment call.

| # | Constraint | Enforced by |
| --- | --- | --- |
| 1 | `.legacy-assets/` is never a source for published output, except component-card extraction under `.claude/rules/anonymization.md` | Human discipline only |
| 2 | No masked identifier in any published file | `check.py` (shapes, every file git would publish) + human review (names) |
| 3 | A card has exactly 13 `##` sections and 6 frontmatter keys in order | `check.py` |
| 4 | A card's number matches its filename; `layer` and `maturity` are from the closed sets | `check.py` |
| 5 | Every card has a skeleton directory with a conforming README | `check.py` |
| 6 | Skeleton scripts import standard library only | `check.py` |
| 7 | Every relative Markdown link resolves | `check.py` |
| 8 | A skeleton is runnable as committed and leaves the tree clean | `check.py --run`, partly |
| 9 | No virtualenv, `__pycache__`, `.env`, token or credential is committed | `.gitignore` (venv, pycache, `.env*`) + `check.py` (credential shapes) |
| 10 | Conventional Commits, one scope taxonomy, `Context:` trailer for agent assets | Human discipline only |
| 11 | No direct commits to the default branch without being asked | Human discipline only |
| 12 | A component card has exactly 11 `##` sections, 5 frontmatter keys in order, a `type` equal to its directory, `instances:` that resolve to cards, and a skeleton | `check.py` |

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

1. **Name review of the published history.** The repository has been public since it was
   created, before the human name check in `SECURITY.md` § Before Publishing was ever run over
   `git log -p`. `check.py` passes, but it catches shapes, not names. Owed by the owner.
2. **`INDEX.md` drift.** It restates each card's `maturity`, a maturity count, and each component
   card's `instances:`. Nothing checks those against the frontmatter.
3. **Deferred rules.** `.claude/rules/README.md` lists concerns not yet governed by a rule —
   the agent-instruction layer and CI gates (both owed), hooks and permissions, and the parts of
   structural lint `check.py` does not yet apply to itself
   (its own card 15).
4. **The agent workflows are unconfigured, not inert.** All three are committed and written for
   this repository — no npm toolchain, `check.py` as the gate — but none of their secrets is set,
   so each fails as soon as it runs:
   - `claude-review` runs only on a trusted `@claude-review` PR comment — its automatic
     `pull_request` trigger is commented out while the secret is unset. Needs
     `CLAUDE_CODE_OAUTH_TOKEN`.
   - `claude-create` runs on a trusted `@claude` comment or an issue opened with `@claude` in
     its body (never on `@claude-review`), and opens a draft PR. Needs `CLAUDE_CODE_OAUTH_TOKEN`.
   - `codex-create-deterministic` runs only on a trusted `@codex-create` issue comment, runs
     `check.py --run` before pushing, and opens a draft PR. Needs `OPENAI_API_KEY`. PRs it opens
     do not trigger `ci.yml` (GitHub skips `pull_request` workflows for `GITHUB_TOKEN` PRs).
