# Skeleton — Planning Subagent Definition

A harness's view of the planning subagent definition that sits in the
sprint-loop skill's agents directory. The card is
[component 48](../../../component-cards/subagents/48-planning-subagent-definition.md);
the skill that names it is
[component 32](../32-role-separated-sprint-loop-orchestrator/).

```
agent.md               a fabricated definition in the component's shape: name,
                       description and a tool list under a skill-style key; a
                       body with a job, a never list, an output shape, rules
capabilities.json      the tools a harness has, which of them can create a file,
                       and the phrases that stand for one concept in prose
inspect_definition.py  what a harness grants against what the file lists, which
                       listed tool can write the file the role must produce, and
                       what the body forbids that its own output requires
```

## Try it

```bash
python3 inspect_definition.py              # grants, the missing write tool, the contradiction; exits 1
python3 inspect_definition.py --narrowed   # a tools: line closes the first gap; the other two remain; exits 1
```

Exit 1 marks the findings, not an error.

**The grant.** The file lists its tools under `allowed-tools`, the name a skill
uses for a grant. A harness reading `tools:` finds no such key and grants every
tool it has, and a spawn through a general-purpose agent type never opens the
file at all. `--narrowed` adds the `tools:` line, which fixes the first of
those and leaves the spawn path ignoring the file.

**The write path.** The role is told to produce a file and is listed no write
tool. The shell is the only listed tool that can create it, in a role whose body
never lets it touch code.

**The contradiction.** The never list rules out rating a sprint's difficulty;
the output shape requires a size rating per sprint. Nothing compares the two,
and `--narrowed` does not touch them.

## What is deliberately missing

**A model and a spec.** Nothing here plans anything. The definition is parsed
directly, as if a harness had found it.

**Discovery.** The component's file sat inside the skill's own directory, not
where a harness looks for subagents. This skeleton opens it by name.

**A spec checker.** The sprint cap and the mandatory out-of-scope section are
sentences in the body. The component had no script that opens a spec, and this
skeleton adds none — which is the gap to
[card 11](../../../cards/11-adversarial-role-separation.md)'s mechanical gate.
