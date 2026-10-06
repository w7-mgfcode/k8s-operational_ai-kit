---
card: 04
title: Path-Scoped Rule Loading
layer: instruction
maturity: partial
source: ../cards/04-path-scoped-rule-loading.md
---

# Path-Scoped Rule Loading

> Attach each convention to the file globs it governs, so the agent gets the database rules only while touching the database and never while touching a stylesheet.

**Status:** partial — the source system documented the doctrine thoroughly and never
applied it to itself: five rule files with no glob frontmatter, governing a project
the kit was not, with no index and no verification.

## 1. Why

A single instruction file grows monotonically, because every new convention has
exactly one place to go. Growth causes three distinct problems:

| Problem | Cost |
|---|---|
| Context bloat | Paying for migration conventions while editing CSS — the cheapest of the three |
| **Instruction ignorance** | Past a length, rules buried mid-document stop being prioritised — present, correct, disobeyed |
| Separation of concerns | A file mixing frontend, backend and infra is one nobody maintains, because nobody owns all of it |

**Without it:** the contract grows until the agent honours its beginning and its end
and treats its middle as decoration.

## 2. Core Idea

Card 02 loads on the **request**. This loads on the **files being touched**. A rule
declares its own globs; matching injects it for the duration of the work, then drops it.

Two tiers: **tier 1** small and always present, **tier 2** large in aggregate and
never present in aggregate.

## 3. Architecture

```
 TIER 1  ┌──────────────────────────────────────┐
         │ Contract — always loaded              │  card 01
         │ true everywhere, deliberately small   │
         └──────────────────┬───────────────────┘
 TIER 2  ┌──────────────────▼───────────────────┐
         │ Scoped rules — injected on glob match │  ← this card
         │   rules/api.md     paths: api/**      │
         │   rules/schema.md  paths: db/**       │
         └──────────────────┬───────────────────┘
         ┌──────────────────▼───────────────────┐
         │ The INDEX — manual path in, for       │  load-bearing
         │ agents with no glob loading           │
         └──────────────────────────────────────┘
```

## 4. How It Works

1. Declare the globs **inside** the rule. Moving the rule moves its scope; no separate registry to desync.
2. Keep each rule atomic — one concern. Working limit 50–100 lines; exceeding it means the globs need to be *more granular*, not the file longer.
3. Write declaratively — MUST, NEVER, ALWAYS. A rule that loads for a few tool calls has no room to hedge.
4. Maintain the index: file, triggering globs, what it covers.
5. **Verify every glob against the real tree.** Highest-value maintenance action in the pattern.

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| Glob frontmatter | The trigger itself | Rules become documentation nobody reads |
| The index | Only access path for agents lacking glob loading | Rules apply for one agent, silently not for others |
| Globs matching the real tree | A rule that never fires *looks like coverage* | Silent non-coverage, indistinguishable from compliance |
| A drift check | Repositories get restructured; globs do not | Card 05 |

## 6. Decisions That Matter

- **The index knowingly violates card 01's no-restatement rule.** Globs live in the frontmatter *and* the index, and they can disagree. Accepted, because it is the only way to serve agents without glob loading — but accepted deliberately, not accidentally.
- **Rules arrive without surrounding context**, so each must stand alone. That forces a terse imperative style that reads badly to humans.
- **Evolution is driven by change, not scale.** Every restructuring invalidates some globs; without a check in that same change, the set decays into card 05 within months.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Invisible until matched | Irrelevant rules never enter context | A broken rule produces no error — nothing distinguishes "correctly did not apply" from "dead" |
| Atomic rules | Loading is precise | Granular globs multiply files; finding the governing one becomes its own problem |
| Declarative style | Actionable on first read | Reads badly to humans |

**Most common failure:** the dead glob — repository restructured, or the rule
imported from a different tree, and the agent violates a documented convention with
no warning at all.

## 8. What To Remember

1. Tier 1 is what is true everywhere; tier 2 is everything else, and it costs nothing until it applies.
2. Invisibility is the mechanism *and* the danger.
3. A glob matching nothing is a rule that never loads and cannot announce its own uselessness.
4. Check: resolve every glob against the tree. Automate it — this is the one that matters.

## 9. Lecture Cue

- **Start with:** the instruction file that only grows, and the rule in its middle that nobody obeys.
- **Draw:** the two tiers, then hang the index off the side — and say why the index is load-bearing rather than decorative.
- **Discuss:** the index duplicates the frontmatter. That is card 01 being violated on purpose; make students argue whether it is worth it.
- **Name the gap:** the source system understood this pattern completely and did not apply it to itself. Five rules, no globs, governing a different project, no index, and therefore no possibility of noticing. **Documented as knowledge, never built as infrastructure** — that is card 05 seen from the other side.
- **End with:** this pattern degrades silently, so the check is not optional.

**Sits between:** card 01 (tier 1) · card 02 (same principle, different trigger) → **this** → card 05 (its failure at full scale)

---
Source: `../cards/04-path-scoped-rule-loading.md` · Skeleton: `../skeletons/04-path-scoped-rule-loading/`
