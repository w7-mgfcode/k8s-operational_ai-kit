---
card: 01
title: One Contract, Many Routers
layer: instruction
maturity: partial
source: ../cards/01-one-contract-many-routers.md
---

# One Contract, Many Routers

> Write the rules once, in one file that owns them; every other agent-instruction file is a thin adapter pointing at it.

**Status:** partial — the memory subsystem achieved the strongest form of the
pattern, while the top level had no canonical file at all and its rules directory
held five files imported from an unrelated project.

## 1. Why

A repository worked by several agents accumulates one instruction file per vendor.
Writing the rules into each produces copies that diverge within a month. The
divergence is invisible: nobody reads four instruction files side by side, and each
agent behaves consistently with the one it read.

Worse than a stale document, because instructions are **executed, not consulted**. A
stale rule does not sit inert — it confidently produces work in the wrong shape.

**Without it:** two agents follow contradictory conventions, each correctly following
the file it was given, and the inconsistency surfaces as review churn nobody can
attribute.

## 2. Core Idea

Separate two things that look alike: the **contract** owns every rule; a **router**
says where the contract is and how this vendor invokes it, and restates nothing.

The test is mechanical — *delete any router and no rule is lost. Delete the contract
and the repository has no rules at all.*

## 3. Architecture

```
        ┌─────────────────────────────┐
        │  THE CONTRACT               │  owns every rule
        │  schema · conventions       │
        │  procedures · prohibitions  │
        └──▲────────▲────────▲────────┘
           │        │        │   "read that file"
      ┌────┴───┐ ┌──┴────┐ ┌─┴──────────────┐
      │router A│ │routerB│ │router C         │  adapters — no policy
      └────────┘ └───────┘ │ (no glob load)  │
                           └─┬───────────────┘
                             │ consults by hand
                        ┌────▼─────┐
                        │  INDEX   │──▶ scoped rules (card 04)
                        └──────────┘
```

## 4. How It Works

1. Declare one file canonical; every other instruction file opens by naming it.
2. Give routers exactly three jobs: where the contract is, how this vendor invokes procedures, which mechanics are unique to it.
3. For a required-but-duplicative path, write a **stub** that names its source and says outright it must not be maintained.
4. Routers without glob loading must point at an **index** of scoped rules — which makes the index load-bearing, not decorative.
5. Put per-vendor context limits in the router; they are properties of the vendor, not the repository.

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| One declared canonical file | Establishes an owner | Four files, four opinions, no tiebreaker |
| Routers as adapters | A summary is a copy, and copies drift | Degrades into the duplication it prevents |
| Scoped-rule index | The only path for agents lacking glob loading | Rules load for one agent, silently never for the rest |
| A duplication check | The failure is invisible by construction | Drift found by accident, months later |

## 6. Decisions That Matter

- **Adopting this commits you to card 04** — every rule lands in one file, so it grows monotonically. That pressure *is* what produces path-scoped loading.
- **Routers tempt authors** — a router is the natural place to write "and by the way, always do X", because it is the file open at the time. Nothing enforces the discipline.
- **Stops paying for itself** when vendors diverge so far that routers carry real behaviour; then they are separate integrations, not adapters, and each needs an owner.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| One owner, many pointers | No drift is possible by construction | Indirection: two reads before any work |
| Routers per vendor | Honours genuinely different mechanics | Cannot verify correctness by diffing them |
| Stubs for namespace compatibility | Satisfies a tool without forking the rules | A stub silently accretes content and becomes a second source |

**Most common failure:** policy restated in a router, because an author edited the
file that happened to be open.

## 8. What To Remember

1. Contract owns rules; routers own mechanics. Nothing else.
2. The delete test settles any argument about where something belongs.
3. The index is load-bearing — a rule missing from it is invisible to every agent without glob loading.
4. Check: grep a distinctive contract phrase; it must return exactly one hit.

## 9. Lecture Cue

- **Start with:** four instruction files, one repository, and a convention that exists in three of them.
- **Draw:** the contract with routers pointing up at it — then the index hanging off the router that cannot auto-load.
- **Discuss:** indirection costs a read; on a one-agent repo the duplication would have been cheaper.
- **Name the gap:** the source system got this right where it mattered least and wrong where it mattered most — a clean executed contract inside the memory subsystem, no canonical file at the top, and a rules directory holding five files from an unrelated project. Nothing existed that could have detected either problem. That outcome is card 05.
- **End with:** a rule stated twice is a rule that will disagree with itself.

**Sits between:** *(root of the instruction layer)* → **this** → card 04 (offloads the growth) · card 05 (what happens without it)

---
Source: `../cards/01-one-contract-many-routers.md` · Skeleton: `../skeletons/01-one-contract-many-routers/`
