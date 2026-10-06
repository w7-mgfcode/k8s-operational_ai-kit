---
component: NN
title: <Component name — generic, never the source system's own name>
type: skill | reference | asset | script | command | rule | subagent | hook
instances:
  - <NN-pattern-card-slug>
related:
  - <NN-other-component-slug>
---

# <Component name>

> One sentence a reader can quote. What this component does and what it refuses to do.

## What it is

Two to four sentences. Name the kind of artifact, the job it does and where it sits
in an agent kit. A pattern card describes an idea; this card describes one concrete
artifact that puts several of them into practice.

## Trigger and routing

How the agent decides to use it: the description text, trigger phrases, and the
explicit "do not use for" list with the sibling that fits better. For a rule, the
path glob; for a hook, the lifecycle event; for a command, the invocation; for a
reference, asset or script, the skill and the phase that load or run it.

## Inputs

| Input | Required | Where it comes from |
|---|---|---|
| … | … | … |

## Procedure

The ordered steps the component actually follows, with each gate named: what must be
true before it moves on, and who confirms it.

1. …
2. …

## Tools and permissions

What it may call, what it is denied, and whether that denial is enforced by the
harness or only by the component's own instructions.

| Tool or verb | Allowed | Enforced by |
|---|---|---|
| … | … | … |

## Outputs

What it produces, in what shape, and where it goes. State whether writing it needs
confirmation.

## Failure modes

Observed or structurally inevitable — never hypothetical.

| Failure | Symptom | Root cause |
|---|---|---|
| … | … | … |

## Patterns it instances

| Card | Where it shows up in this component |
|---|---|
| [NN Pattern name](<up>/cards/NN-slug.md) | … |

`<up>` depends on where the card sits: `../../..` for a skill card, `../../../..` for a
reference, asset or script beneath it, `../..` for a standalone card.

## Provenance

What the source component was, described generically: its size, its parts, and
anything its design inherited. Every sentence is subject to
`.claude/rules/anonymization.md`.

## Prototype

Minimal runnable prototype in
[`<up>/skeletons/components/NN-<slug>/`](<up>/skeletons/components/NN-<slug>/).
Standard library, offline, fixture data only.

## What is deliberately missing

The gap between the prototype and the real component, and between the real
component and the patterns it instances. Hiding a gap turns the card into an
advertisement.
