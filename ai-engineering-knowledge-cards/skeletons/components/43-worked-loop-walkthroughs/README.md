# Skeleton — Worked Loop Walkthroughs

Two fabricated walkthroughs of a sprint loop, replayed against a stand-in tool to see
which steps reproduce. The card is
[component 43](../../../component-cards/skills/role-separated-sprint-loop-orchestrator/references/43-worked-loop-walkthroughs.md);
the skill that loads it is [component 32](../32-role-separated-sprint-loop-orchestrator/).

```
loop_tool.py      a small tool with init, sprint, record and gate subcommands and an honest gate
walkthroughs.json one first-try pass and one recovery: each step is a command with the
                  output the walkthrough shows, or a sentence with no command
replay.py         runs each command in a temporary directory and compares
```

## Try it

```bash
python3 replay.py                # steps that do not reproduce; exits 1
python3 replay.py recovery       # a failure is recorded and the gate is never run; exits 1
```

**Command form.** Step 2 of the first walkthrough is written in flags alone, the way a
skill body might summarize it; the tool takes subcommands and rejects it with exit 2.

**Shown against printed.** Step 4 shows a passing gate before any result has been
recorded; the tool prints `pending`. A walkthrough written from what should happen,
rather than from a run, reads the same until someone replays it.

**Prose steps.** "The delta report is generated" and "the final report is generated" name
work with no command to run, so a replay cannot reach them.

**The failure path.** The recovery walkthrough records a failure and moves on. The one
place the gate is shown is the pass.

Exit 1 marks steps that did not reproduce, not a crash. The temporary directory is removed.

## What is deliberately missing

**The real tool.** `loop_tool.py` is a fresh and much smaller tool whose gate is correct.
What the real gate prints is the subject of
[component 44](../44-loop-gate-and-history-harness/).

**The agents.** The roles' steps are sentences in the real walkthroughs and are absent here.

**The fix, for the pattern.** Walkthroughs generated from a replay, so a step that does
not run cannot be written down.
