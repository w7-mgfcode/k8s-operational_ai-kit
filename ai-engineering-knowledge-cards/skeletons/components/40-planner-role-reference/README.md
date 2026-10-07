# Skeleton — Planner Role Reference

The reference that tells a planning agent what a spec contains, how to cut sprints and
what to check before the user sees it — and what a program could check of that list.
The card is
[component 40](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/references/40-planner-role-reference.md);
the skill that loads it is [component 32](../32-role-separated-sprint-loop-orchestrator/).

```
spec_good.md    a fabricated spec that meets every item of the reference's checklist
spec_bad.md     one with too many files, a forward dependency, a single target, no goal and no out-of-scope list
spec_vague.md   one that is complete in shape and empty in content
rules.json      the structure's required fields beside the bans the role also carries
check_spec.py   the checklist as code: counts and sections, nothing judged
```

## Try it

```bash
python3 check_spec.py spec_good.md       # mechanically complete; exits 0
python3 check_spec.py spec_bad.md        # five findings; exits 1
python3 check_spec.py spec_vague.md      # complete again, and its targets are empty; exits 0
python3 check_spec.py --rules rules.json # a required field the role is banned from filling; exits 1
```

**The checklist is countable, partly.** Sprint count, targets per sprint, files per sprint,
dependency order and an out-of-scope list are all arithmetic, and `spec_bad.md` trips each.
The reference leaves all of them as boxes for the model to tick.

**The vague spec passes.** "Code is clean and well-structured" is the reference's own
example of a bad target, and the checker cannot tell: concreteness is the one thing
the reference asks for that is not countable. Neither is the last box, that the user
approved — nothing here has a place to record it.

**The conflict.** The structure requires an estimated complexity per sprint; the role
that fills it is told not to estimate effort. `--rules` shows the two statements
meeting. Exit 1 marks findings, not a crash.

## What is deliberately missing

**A reader.** In the component, nothing opens the spec: the orchestrator's state keeps its path
and no script parses it. This checker is the missing consumer; it is not in the component.

**Judgement.** No attempt to score whether a target is concrete or testable. A word list
would be a different, weaker rule than the reference states.

**Approval.** The reference's last checklist item is the user's, recorded in the
component only as a free-text note in the state file.
