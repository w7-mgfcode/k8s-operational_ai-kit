# k8s-operational_ai-kit — Claude Code Operating Index

> **Read `@AGENTS.md` first.** It is the shared cross-tool brief — stack, setup, commands,
> validation gates, architecture, conventions, safety, and git flow. This file adds only
> Claude-specific operating context and does not repeat it.

@AGENTS.md

## Deep-Dive References

Pulled in on demand — load only what the task touches.

- Layer structure & blast radius:  @docs/_base/ARCHITECTURE.md
- Constraint matrix & rule paths:  @docs/_base/RULES.md
- Anonymization & publishability:  @docs/_base/SECURITY.md
- Adding a card or skeleton:       @docs/_base/DEV_GUIDE.md
- Repository navigation map:       @docs/_base/REPO_MAP_INDEX.md

## Path-Scoped Rules

Claude Code auto-loads a rule from `.claude/rules/` when a matching path is touched — the
index in `.claude/rules/README.md` lists every glob. Other agents have no glob loading and
are told to consult that index by hand, which makes it load-bearing: **a rule missing from
that table is invisible to every agent except this one.** If you add a rule, add its row.

This repository is itself an instance of the pattern it documents in card 04, and the rule set
was rebuilt in September 2026 after an audit found the inherited one described a project that
does not exist here. Do not reintroduce a glob that matches nothing.

## Safety

Hard rules and stop-and-ask gates: `@AGENTS.md` § Safety. Full constraint matrix:
`docs/_base/RULES.md`.

The one that bites silently: `.legacy-assets/` is un-anonymized source material. It is easy to
read by accident when searching the tree, and reading it into any output is the single
highest-cost mistake available here. Scope searches to `ai-engineering-knowledge-cards/` unless
you have a reason not to.

## Verification

```bash
python3 check.py --run     # must exit 0 before any commit
wc -l CLAUDE.md            # must stay ≤ 150 lines
```

## Workflow

1. Branch — never commit to `master` directly (`.claude/rules/git-workflow.md`).
2. Read the card or skeleton you are changing, and the rule that governs its path.
3. Make the change. If it touches a contract, expect every artifact under it to need review.
4. `python3 check.py --run` until it exits 0 and the tree is clean.
5. Commit with the scope taxonomy; add a `Context:` trailer if you touched agent-context assets.

## Learnings

- `check.py --run` classifies exit 2 as "needs arguments", not failure; several skeletons exit 1
  on purpose to demonstrate a failure mode. Only a crash is a real failure.
- Skeleton READMEs under `skeletons/pipelines/` sit one directory deeper — card links need
  `../../../cards/`, and the link check will catch it if you get this wrong.
- The `docs/_kB/repo-map/` KB does not exist; `REPO_MAP_INDEX.md` here was written by hand, not
  generated, because its generator's only input would have been the excluded legacy tree.
