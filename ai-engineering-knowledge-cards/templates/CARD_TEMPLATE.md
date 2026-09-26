---
card: NN
title: <Pattern name — a noun phrase, not a verb phrase>
layer: instruction | routing | skill | subagent | memory | execution | validation
maturity: proven | partial | abandoned
instanced_by:
  - <component type>/<generic component name>
related:
  - <NN-other-card>
---

# <Pattern name>

> One sentence a reader can quote. What the pattern does, in plain language.

## What this pattern is

Two to four sentences. Define the pattern in terms of mechanism, not benefit.
A reader should be able to recognize an instance of it in someone else's system
after reading this section alone.

## Why it exists

The pressure that produced it. Name the concrete thing that goes wrong without
it — not "better organization" but the specific failure the author hit.

**Without it:** <the failure, stated as an observable symptom>

## Where it belongs

Which layer of the agent architecture owns this, and what sits above and below it.

```
<a three-to-six line ASCII sketch placing the pattern in its stack>
```

## How it works

The mechanism, step by ordered step. Include the real control flow: what triggers
it, what it reads, what it writes, what it hands off to.

1. …
2. …
3. …

## What it depends on

| Dependency | Why it is needed | What happens if absent |
|---|---|---|
| … | … | … |

## How it interacts with other patterns

| Pattern | Relationship |
|---|---|
| [<NN-card-name>](NN-card-name.md) | <feeds / constrains / duplicates / competes with> |

## Constraints and trade-offs

What the pattern costs. Every entry is a real cost paid, not a hypothetical.

- **<Constraint>** — <what it forecloses>
- **<Trade-off>** — <what was chosen over what, and why>

## Failure modes

Observed or structurally inevitable ways this goes wrong.

| Failure | Symptom | Root cause |
|---|---|---|
| … | … | … |

## Diagram

```mermaid
%% Control flow or layer relationship. Keep it to one idea.
```

## How to validate an implementation

Checks a reader can actually run against their own system. Prefer mechanical
checks over judgment calls.

- [ ] …
- [ ] …

## How it evolves

What changes about this pattern as the system grows: at ten components, at fifty,
at two hundred. Name the point where the pattern stops paying for itself.

## Skeleton

Minimal prototype in [`../skeletons/NN-<slug>/`](../skeletons/NN-<slug>/).
Generic, runnable, no domain specifics.

## Provenance

Instanced in the source system by: <generic description of the real components>.
<If partially implemented, say exactly what was missing.>
