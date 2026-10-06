---
card: 07
title: Capability Taxonomy — Skill, Command, Subagent
layer: routing
maturity: proven
source: ../cards/07-capability-taxonomy.md
---

# Capability Taxonomy — Skill, Command, Subagent

> Not three words for the same thing: they differ in **who decides to run them** and **whose context they consume**, and those two axes decide which one a capability should be.

**Status:** proven — instanced across seventeen skills, thirteen commands and a set
of tool-narrowed subagents.

## 1. Why

The containers look interchangeable — each is a markdown file with instructions — so
they get chosen by feel, which produces three specific defects:

- Behaviour that should be user-triggered is a **skill**, so it fires when nobody asked, mid-task, derailing the work.
- Behaviour that should be model-triggered is a **command**, so it never runs, because the user forgot it exists.
- Work that should be delegated runs **inline**, filling the session with intermediate material nobody needs afterwards.

The third is the expensive one. An investigation reading forty files to answer one
question leaves thirty-nine files of residue in the context that must carry the rest
of the session.

**Without it:** capabilities fire at the wrong times, never fire, or fire correctly
while poisoning the context they run in.

## 2. Core Idea

Two axes settle it:

| | Who invokes | Whose context |
|---|---|---|
| **Skill** | The model, from a description | The main session |
| **Command** | The user, by name | The main session |
| **Subagent** | The model, by delegation | A fresh, isolated one |

Everything else follows. A skill needs a routing contract because the model must
decide; a command does not, because the user already did.

## 3. Architecture

```
                  user types a name
                         │
                         ▼
                   ┌──────────┐
                   │ COMMAND  │──┐
                   └──────────┘  │
  request ─▶ routing ─┐          ├──▶ MAIN SESSION CONTEXT
                      ▼          │
                 ┌──────────┐    │
                 │  SKILL   │────┘
                 └────┬─────┘
                      │ delegates
                      ▼
                ┌───────────┐
                │ SUBAGENT  │──▶ isolated; returns a conclusion, not the evidence
                └───────────┘
```

## 4. How It Works

1. **Who should decide?** If the user must know it exists to get value, it is a command. If the value is automatic firing, it is a skill — and it owes a routing contract (card 03).
2. **What does the work cost the context?** Large intermediate material — sweeping a codebase, replaying logs — belongs in a subagent.
3. Give commands **explicit arguments**; they are invoked deliberately, so they can demand a parameter. Skills get whatever the user happened to say.
4. **Narrow a subagent's tools, never widen them.** A read-only agent that *cannot* write is a stronger guarantee than one instructed not to.
5. Let containers compose — a skill spawning three role-specific subagents is the composition working as intended (card 11).

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| Routing contract (skills only) | The model's basis for deciding | Skills that never fire, or fire wrongly |
| User awareness (commands) | Commands are worthless unless remembered | Well-built procedures nobody invokes |
| Real context isolation | The entire benefit is the residue not returning | Delegation costs more than working inline |
| Tool narrowing | Safety from capability, not instruction | "Do not write" as a request, not a guarantee |

## 6. Decisions That Matter

- **Every skill taxes every session** — its metadata is resident whether used or not. Commands and subagents cost nothing until invoked. That alone argues for a command unless automatic firing is the point.
- **Delegation has fixed overhead** — a prompt, a summary, a round trip. For small work the ceremony costs more than the residue it avoids.
- **Stops scaling** when the kit outgrows one person's memory: commands become undiscoverable and skills become a crowded routing table. The next move is a domain dispatcher, which trades one routing decision for two.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Skill | Fires at the right moment without being remembered | Permanently resident metadata; needs a maintained routing contract |
| Command | Zero standing cost; takes real arguments | Depends on human memory — a kit with thirteen has twelve the user forgot |
| Subagent | Heavy reading without context residue | Knows nothing the session learned; a bad brief returns confident nonsense |

**Most common failure:** context poisoning — the session slows and loses the thread
after a large investigation that should have been delegated.

## 8. What To Remember

1. Two axes: who invokes, whose context. Everything else is downstream.
2. Only skills need a routing contract — and only skills tax every session.
3. A subagent's tool list is a constraint, not a convenience.
4. Check: no skill exists whose value depends on the user knowing it exists.

## 9. Lecture Cue

- **Start with:** the capability that fired mid-task when nobody asked for it.
- **Draw:** the two-axis table first, then the flow — and put a thick border on the subagent's isolated context.
- **Discuss:** isolation cuts both ways. Ask students what a subagent must be told that the session already knows.
- **Point at the counter-example:** the same kit that used subagents well for adversarial evaluation also held nineteen uniform vendored role definitions that nothing ever invoked. **Right container, no earned place** — correct taxonomy applied to material that should not have been there at all (card 05).
- **End with:** make it a command unless automatic firing is the whole point.

**Sits between:** card 03 (what skills owe) · card 02 (all three use the levels) → **this** → card 11 (the strongest subagent use)

---
Source: `../cards/07-capability-taxonomy.md` · Skeleton: `../skeletons/07-capability-taxonomy/`
