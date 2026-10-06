# k8s-operational_ai-kit

**Twenty engineering patterns extracted from an agent kit that ran a production Kubernetes platform — including the ones that only half worked.**

The kit this comes from was not a demonstration. It captured operational knowledge
from AI-assisted infrastructure sessions; it investigated every external network
destination leaving a cluster and produced a firewall-ready evidence matrix; it
took a reported symptom in one namespace, cross-referenced it against the platform
repository and current upstream sources, ranked remediations by repository alignment
and blast radius, and wrote a plan to disk without touching the cluster; it
orchestrated multi-workstream hardening sprints with dependency ordering,
blast-radius gates and a dry-run before every apply; it ran an adversarial
planner/generator/evaluator loop to keep the model from grading its own work.

It was used and extended daily for months, by one engineer, against infrastructure
where a wrong command is an outage rather than a failed test.

This repository is what survives when you remove that system's identity and keep
its architecture.

## What a Knowledge Card is

One pattern, thirteen fixed sections, every claim traceable to something that
actually ran.

A card answers more than "what is this". It states **why the pattern exists** — the
specific failure that produced it — **where it belongs** in the agent architecture,
**how it works** mechanically, **what it depends on**, **how it interacts** with the
other patterns, **what it costs**, **how it fails**, **how to validate** an
implementation, and **how it evolves** as the system grows.

Two sections do the work that makes this an engineering record rather than a
portfolio:

- **`maturity: partial`** — the source system implemented part of the pattern and
  not the rest, and the card says exactly which part. Several cards carry it. The
  gaps are the most instructive content here, and none of them have been smoothed
  over.
- **Failure modes** — every row is observed or structurally inevitable. No
  hypotheticals.

## How this was extracted

```
REAL-WORLD SYSTEM        a private agent kit operating a Kubernetes platform
       │                 extract the engineering knowledge
       ▼
ENGINEERING CONCEPT      the pattern, separated from the installation
       │                 remove the identity
       ▼
ANONYMIZED ARCHITECTURE  no organization, no hosts, no paths, no topology
       │                 reconstruct
       ▼
PROTOTYPE / SKELETON     minimal, runnable, standard library only
       │                 explain through layers
       ▼
KNOWLEDGE CARD
```

Public technology names stay, because they carry the engineering meaning. Anything
pointing at a *specific installation* of them is gone. The full policy and the
audit record — what was removed, in what quantity, under which rule — is in
[`docs/ANONYMIZATION.md`](docs/ANONYMIZATION.md).

## Start here

| If you want | Read |
| --- | --- |
| The method at its most honest | [Card 13 — Log-as-Source Compilation](cards/13-log-as-source-compilation.md), a `partial` pattern with its four gaps named |
| The cheapest idea to steal today | [Card 03 — Description-as-Router](cards/03-description-as-router.md) |
| The architecture end to end | [INDEX.md](INDEX.md) |
| Every diagram at a glance | [diagrams/](diagrams/README.md) |
| Proof the anonymization is real | [docs/ANONYMIZATION.md](docs/ANONYMIZATION.md) |

## Skeletons

Every card ships a minimal prototype under [`skeletons/`](skeletons/). Four rules
hold across all of them: **standard library only**, **offline** (model calls are
stubbed behind a named function that prints instead), **runnable as committed**
(example data ships with it), and **generic**.

Each skeleton's README ends with *What is deliberately missing* — a gap that is
faithful to the source system is card content, and hiding it would turn the
skeleton into a demo.

Four cards compose into one engine; that walkthrough is at
[`skeletons/pipelines/session-memory-loop/`](skeletons/pipelines/session-memory-loop/).

## What this is not

Not a framework. Not installable. Not a product. Not advice for systems unlike the
one it came from — a single-operator platform where changes are hard to reverse
and blast radius, not severity, is the unit of risk. Several patterns here would be
wrong on a team with code review and a staging environment, and the cards say so in
their Constraints sections.

Where a pattern was inherited from published work rather than invented, the card
says so.

## Provenance

Extracted from one engineer's working kit. The source material is not in this
repository and never will be — see [`docs/ANONYMIZATION.md`](docs/ANONYMIZATION.md)
for what was excluded and why.
