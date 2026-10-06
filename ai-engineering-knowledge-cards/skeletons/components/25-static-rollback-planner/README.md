# Skeleton — Static Rollback Planner

A rollback recipe per workstream, printed the same way whatever was changed,
and a paper replay of its git commands against what a change actually touched.
The card is
[component 25](../../../component-cards/skills/workstream-hardening-orchestrator/scripts/25-static-rollback-planner.md);
the skill that runs it is [component 08](../08-workstream-hardening-orchestrator/).

```
changes.json   a fabricated change log: two TLS attempts on workstream A, each
               file marked as committed, uncommitted, or both
plan.py        five constant recipes keyed by workstream; with --audit, the A
               recipe's git commands replayed against changes.json
```

Nothing here runs git. The audit reasons about what each command would do.

## Try it

```bash
python3 plan.py                    # the workstream A recipe; exits 0
python3 plan.py --workstream C     # another workstream's recipe; exits 0
python3 plan.py --audit            # the A recipe against two attempts; exits 1
```

**The recipe.** Steps and git commands, and nothing in them depends on the
attempt. Run it for either attempt in `changes.json` and the output is
identical, because the plan is a constant.

**The audit.** The first attempt changed four files: the TLS task, the main
install task, the values template and the security variables file. The recipe
restores one of them. That restore does nothing for the committed part of the
change, since `git checkout HEAD` brings back the commit that holds it. It also
overwrites the uncommitted edits on top without a word. The second attempt
touched only the values template, which no command restores at all.

Exit 1 marks the six gaps, not an error.

## What is deliberately missing

**A plan from the change.** The obvious input is `git diff --name-only` against
the sprint's starting commit, with a restore or revert for each file, chosen by
whether the change is committed. The component reads only the workstream's
status from the state file; the skeleton reads nothing from git at all.

**The cluster commands.** The component adds operator commands (replica status,
manual unseal) when the sprint has cluster access. They are text either way,
and omitted here.

**The load-failure path.** With no YAML library installed and no state file,
the component's own error handler raises before it can fall back. That is
described on the card; reproducing it would mean importing a non-standard
library.

**The pattern's gap.** Card [17](../../../cards/17-blast-radius-gating.md)
prepares the way back before the change. A recipe written before the change is
known cannot be that way back.
