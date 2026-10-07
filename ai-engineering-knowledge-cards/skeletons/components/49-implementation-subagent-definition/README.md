# Skeleton — Implementation Subagent Definition

A harness's view of the implementation subagent definition that sits in the
sprint-loop skill's agents directory. The card is
[component 49](../../../component-cards/subagents/49-implementation-subagent-definition.md);
the skill that names it is
[component 32](../32-role-separated-sprint-loop-orchestrator/).

```
agent.md               a fabricated definition in the component's shape: the one
                       role in its loop that is listed write tools, with a never
                       list and an output shape
capabilities.json      the tools a harness has, which of them write, and the
                       phrases that stand for one concept in prose
scope.json             a sprint's file scope and four writes the role might attempt
inspect_definition.py  the grant against the list, the scope sentence against the
                       grant, and two body sentences that overlap
```

## Try it

```bash
python3 inspect_definition.py              # grants, scope, the overlap; exits 1
python3 inspect_definition.py --narrowed   # a tools: line closes the grant gap; scope and overlap remain; exits 1
```

Exit 1 marks the findings, not an error.

**The grant.** The file lists its tools under `allowed-tools`. A harness
reading `tools:` finds no such key and grants everything; a spawn through a
general-purpose agent type never opens the file. `--narrowed` fixes the first
and leaves the second.

**The scope.** This is the role where the grant is meant to matter, since it is
the one that can write. The body says to stay inside the sprint's files, and the
grant is `Write` and `Edit` — with no path in it. Two of the four writes are
outside the scope and both are allowed, with or without `--narrowed`.

**The overlap.** The never list bans a caveat about what could be improved;
the output shape requires known gaps. The role reference
([component 39](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/references/39-generator-role-reference.md))
draws the line between them; the definition alone does not.

## What is deliberately missing

**A model and a build.** Nothing here writes a file. The attempted writes are
a list, checked, never performed.

**A path-scoped grant.** The component had none, and neither does this
skeleton: scoping a write to a set of paths needs a permission rule or a hook
outside the definition.
[Card 16](../../../cards/16-the-permission-ladder.md)'s deny rung is the part
of the pattern it belongs to.

**Discovery.** The component's file sat inside the skill's own directory, not
where a harness looks for subagents. This skeleton opens it by name.
