# Skeleton — Capability Taxonomy

The same capability — a dependency audit — packaged three ways, so the
difference is the container and nothing else.

```
as-skill.md      model decides. routing contract required. always resident.
as-command.md    user decides. takes an argument. free until invoked.
as-subagent.md   delegated. isolated context. tools NARROWED.
choose.py        the two axes, applied to four worked cases
```

## Try it

```bash
python3 choose.py
python3 choose.py --interactive
```

Then read the three files in order and compare their **cost** lines. They
implement identical behavior and have completely different standing costs,
failure modes and discovery paths.

Note the `tools:` line in `as-subagent.md`. It lists three read-only tools, and
the subagent therefore *cannot* write — a runtime guarantee rather than an
instruction it might not follow. Narrowing capability is stronger than asking
for restraint, every time.

## What is deliberately missing

**A runtime.** These are declarations, not working capabilities. Nothing here
routes, invokes or spawns anything.

**Discoverability for commands.** `as-command.md` names the problem and does
not solve it. A kit with thirteen commands has twelve the user has forgotten,
and nothing in this skeleton — or in the source system — addresses that.
