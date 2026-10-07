# Skeleton — Evaluation Subagent Definition

A harness's view of the evaluation subagent definition that sits in the
sprint-loop skill's agents directory. The card is
[component 50](../../../component-cards/subagents/50-evaluation-subagent-definition.md);
the skill that names it is
[component 32](../32-role-separated-sprint-loop-orchestrator/).

```
agent.md               a fabricated definition in the component's shape: a role
                       that may read everything and is told to change nothing
capabilities.json      the tools a harness has, and the shell shapes that write
commands.json          six shell commands the role might run, and the file it is
                       told to write
inspect_definition.py  the grant against the list, each command classified as a
                       read or a write, and the output file against the ban
```

## Try it

```bash
python3 inspect_definition.py              # grants, shell writes, the output file; exits 1
python3 inspect_definition.py --narrowed   # a tools: line closes the grant gap; the shell remains; exits 1
```

Exit 1 marks the findings, not an error. The commands are classified and never
run.

**The grant.** The file lists its tools under `allowed-tools`. A harness
reading `tools:` finds no such key and grants everything, write tools included;
a spawn through a general-purpose agent type never opens the file. `--narrowed`
fixes the first and leaves the second.

**The shell.** The role is listed `Bash` and no write tool, so the review it is
told to write has to be written through the shell. Two of the six commands
change the repository instead — an in-place edit and a deletion — and are
granted by the same word. Nothing in a tool grant tells the review file from
the source file.

**The sentence.** The body says to change no file and also to write the result
to one. Both are true of the same role, and only the path separates them.

## What is deliberately missing

**A model and a review.** Nothing here grades anything. The commands are a
fixture, and the output is a verdict about the definition.

**A way to close it.** A read-only shell, or an evaluator that returns its review
as text for the dispatcher to save, would remove the gap; the component had
neither. [Card 16](../../../cards/16-the-permission-ladder.md)'s deny rung is the
part of the pattern both belong to.

**Discovery.** The component's file sat inside the skill's own directory, not
where a harness looks for subagents. This skeleton opens it by name.
