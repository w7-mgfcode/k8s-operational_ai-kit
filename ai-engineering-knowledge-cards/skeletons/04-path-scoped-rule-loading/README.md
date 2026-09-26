# Skeleton — Path-Scoped Rule Loading

```
rules/api.md              scoped to src/api/**        — loads, and should
rules/schema.md           scoped to src/db/**/*.sql   — loads, and should
rules/frontend-DEAD.md    scoped to a tree that does not exist
rules/README.md           the index — the manual path in for agents
                          without glob loading
resolve_globs.py          resolves every glob against the real tree
src/, docs/               a tiny tree for the globs to match
```

## Try it

```bash
python3 resolve_globs.py        # exits 1 — two dead globs, one unindexed rule
```

The dead rule is the point. Read `rules/frontend-DEAD.md`: it is clear,
declarative, well-scoped and completely inert. Nothing about working in this
repository would ever reveal that it is not applying. That silence is the
pattern's defining hazard, and resolving globs mechanically is the only cheap
cure.

Then notice the warning: `frontend-DEAD.md` is also missing from the index, so
even an agent reading rules by hand would never reach it. Two independent
failures, neither visible from inside a session.

## What is deliberately missing

**Overlap detection.** Two globs matching one file inject both rules at once.
Fine when they complement, a real problem when they conflict, and nothing here
checks for it.

**A trigger.** This resolves globs when you run it. Repository restructures are
what invalidate globs, so the check belongs in the same change that
restructures — see [card 05](../../cards/05-instruction-provenance-and-drift.md).
