# Skeleton — Workstream Tracking Brief

A per-workstream brief rendered from the sprint state instead of filled by hand,
and an audit of the three things that went wrong with the hand-filled original.
The card is
[component 12](../../../component-cards/skills/workstream-hardening-orchestrator/assets/12-workstream-tracking-brief.md);
the skill it belongs to is [component 08](../08-workstream-hardening-orchestrator/).

```
state.json         fabricated sprint state: five workstreams, the state file's
                   status vocabulary, and a tier per component
brief-template.md  a shortened brief template — header, objective, blast radius,
                   rollback — with its own status list
skill-mini.md      a fabricated miniature skill: three phases and a template table
filled-brief.md    a brief for workstream A, filled by hand some days ago
brief.py           renders briefs from state.json; --audit runs three checks
```

## Try it

```bash
python3 brief.py            # one brief per workstream, derived; exits 0
python3 brief.py A          # workstream A only
python3 brief.py --audit    # orphan, vocabulary and stale-copy checks; exits 1
```

**The render.** Every block comes from `state.json`: the tier and dependent list from
the component's entry, the confirmation flag from the tier. A rendered brief cannot
disagree with the state, because it holds nothing the state does not.

**The audit.** Check 1 reads the miniature skill and lists, for each template in its
table, the phases that load it — three are loaded, the brief by none. Check 2 finds
`deferred` in the brief's status list and nowhere in the state file's. Check 3 compares
the hand-filled brief with a fresh render: its status is one the state cannot hold, its
tier and dependent count are from an older table, it says no confirmation is needed for
a HIGH component, and its rollback steps have drifted. Seven findings; exit 1 marks them.

## What is deliberately missing

**A phase that calls the renderer.** The skeleton shows the brief can be derived; it
does not add the step to a skill, which is the real fix for the orphan.

**Dependencies, checklists and trigger tables.** The source brief had them; each would
be derived the same way, from the state and the gate catalogue.

**The pattern's gap.** [Card 19](../../../cards/19-scope-lock-and-checkpoint-delivery.md)
asks for scope written down before work starts; a brief that is never filled writes
nothing down.
