# README and INDEX — outlines only

Drafted at outline depth pending your framing decision. Both need one input from
you before they can be written: **[you fill this in: the public repo name, and one
line on how you want it positioned to a reader arriving cold — portfolio, teaching
resource, or reference]**. That choice changes the opening paragraph and the order
of the first two sections; everything below is stable either way.

---

## README.md — outline

**1. Title and one-line positioning** *(needs your input)*
One sentence. What this is and who it is for. No hedging, no "a collection of".

**2. The premise — three short paragraphs**
- These patterns come from one agent kit, used and extended daily to operate a
  Kubernetes platform. Not a thought experiment.
- The kit's identity is removed; its architecture is not. Link to
  [ANONYMIZATION.md](ANONYMIZATION.md).
- What a Knowledge Card is: one pattern, ten fixed sections, every claim traceable to
  something that actually ran.

**3. The extraction pipeline** — the diagram, as a compact ASCII or Mermaid figure:
real system → engineering concept → anonymized architecture → prototype → card.
Two sentences of explanation. The diagram carries it.

**4. Start here** — a three-row table, not a list of twenty links:

| If you want | Read |
|---|---|
| The single best example of the method | Card 13 (a pattern with its gaps stated) |
| The cheapest idea to steal today | Card 03 (routing contract) |
| The architecture end to end | [INDEX.md](../INDEX.md) |

**5. How to read a card** — the ten sections named, with one clause each on why that
section exists. Emphasize `maturity: partial` and the Failure modes table: those are
the sections that make this an engineering record rather than a portfolio.

**6. What this is not** — short and firm. Not a framework, not installable, not a
product, not advice for systems unlike the one it came from. Prevents the most likely
misreading.

**7. Skeletons** — each card ships a minimal runnable prototype; what "runnable"
means here (stdlib only, offline, model calls stubbed).

**8. Provenance and license.**

**Length target:** one screen before the first table. A reader decides in fifteen
seconds whether this is serious.

---

## INDEX.md — outline

**Primary axis: architectural layer.** Cards are ordered structural-first, which is
also the order they build on each other.

```
INSTRUCTION   01 One Contract, Many Routers
              04 Path-Scoped Rule Loading
              05 Instruction Provenance and Drift
              06 Calibrated Degrees of Freedom
ROUTING       02 Progressive Disclosure
              03 Description-as-Router
              07 Capability Taxonomy: Skill / Command / Subagent
AUTHORING     08 Interview Before Generation
              09 Scaffold -> Validate -> Package
              10 Behavioral Evaluation Harness
SUBAGENT      11 Adversarial Role Separation
MEMORY        12 Lifecycle Hooks as Capture Points
              13 Log-as-Source Knowledge Compilation
              14 Index-Guided Retrieval
              15 Structural Lint for Knowledge Bases
EXECUTION     16 The Permission Ladder
              17 Blast-Radius Gating
              18 The Redaction Boundary
              19 Scope Lock and Checkpoint Delivery
VALIDATION    20 Repo Projection Pipeline
```

**Secondary axis: a table with one row per card** — number, title, layer, maturity,
one-line hook, and the cards it relates to. This is the table a reader scans; the
layer grouping above is what they navigate by.

**Third view: by question** — six or eight entries of the form *"My agent loads the
wrong skill" → card 03*. This is how people actually arrive, and it is the cheapest
section to write once the cards exist.

**Maturity summary** — a count of proven / partial / abandoned. Stating up front that
a meaningful share are `partial` sets the right expectation and is the most credible
thing on the page.
