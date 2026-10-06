---
card: 10
title: Behavioral Evaluation Harness
layer: validation
maturity: partial
source: ../cards/10-behavioral-evaluation-harness.md
---

# Behavioral Evaluation Harness

> Whether a capability fires on the right request is a claim about model behaviour, not a property of your files — so test it the only way such a claim can be tested: replay real prompts and check what actually happened.

**Status:** partial — both harnesses were built and well built. Nothing ever ran
them routinely. No baseline survives, and no case file was retained beside the
harness that reads it.

## 1. Why

Routing failures are silent. A capability that never fires produces no error — the
agent answers generically, and the author, who knows the capability exists, reads
that as a reasonable response rather than as a miss.

Nothing in the file catches this. A description can be well-written, within limits,
and still lose to a sibling. The only observation that settles it is running the
prompt and seeing which capability engaged.

**Without it:** routing is maintained by impression, the effect of every description
edit is unknown, and capabilities silently stop firing as the set grows.

## 2. Core Idea

Structure and behaviour are different claims and need different gates. Card 09
proves well-formed; this proves *it fires*.

Keep real prompts paired with expected outcomes, run them through the real
invocation path, assert on **observable signals** — not prose — and report an
aggregate you can compare against a baseline.

## 3. Architecture

```
  STRUCTURE                BEHAVIOUR
  ─────────                ─────────
  validator        ┌──▶ trigger accuracy   "does it fire on the right prompt?"
  (card 09)        │
  well-formed?     ├──▶ functional tests   "do its scripts work end to end?"
                   │
                   └──▶ output shape       "does the result look right?"

  Both gate the same artifact. Neither substitutes for the other.
```

## 4. How It Works

1. **Harvest prompts, never invent them.** Invented phrasings test the author's idea of the wording — which is what the description already encodes, so the test passes and proves nothing.
2. Assert on stable signals: which capability activated, whether a characteristic phrase appears, whether the expected file was written. Never on exact prose.
3. **Include negative cases** — over-triggering is the more annoying daily failure, and exclusion clauses are untested until something tests them.
4. Include the **ambiguous** cases deliberately; they sit between two capabilities and are the ones worth re-running after any edit.
5. Run through the real entry point with a timeout. Testing a mock of the router tests the mock.
6. Record an aggregate. A change that improves one case and breaks two is visible only against a baseline.

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| A scriptable invocation path | Runs prompts as a user does | Only mocks testable — proves nothing about routing |
| Observable signals | Something stable to assert on | Tests assert on prose and fail constantly |
| Harvested prompts | Tests the real phrasing | A suite that always passes |
| A recorded baseline | Change is meaningful only relative to something | Results with no way to spot regression |

## 6. Decisions That Matter

- **Signal assertions are loose, and that is the right trade.** "A phrase appears" is a proxy for "the right thing happened" — proxies can pass for the wrong reason, but exact-text assertions produce a suite people disable.
- **The suite encodes today's model.** A model update can shift routing globally, invalidating the baseline with no change to the repository.
- **Fragility is neglect, not scale.** A suite not wired to something that happens anyway gets run at build time and never again.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Real invocations | The only honest evidence about routing | Time and money per case, so the suite stays small — and the dangerous cases are the ones nobody thought of |
| Behavioural testing | Catches what structure cannot | Non-deterministic: one failure may be signal or noise, and telling them apart means repetition |
| Aggregate accuracy | Makes edits comparable | Hides which specific case moved |

**Most common failure:** the self-confirming suite — everything green while real
routing failures continue, because the prompts came from the description.

## 8. What To Remember

1. Well-formed and works-correctly are different claims needing different gates.
2. Harvested prompts or the suite proves nothing.
3. Negative and ambiguous cases are where the contract actually earns its keep.
4. Check: the functional suite includes cases that **must fail**, proving the gates gate.

## 9. Lecture Cue

- **Start with:** the capability that never fires, and the generic answer the author reads as success.
- **Draw:** the structure/behaviour split — two gates, one artifact — then the fixtures split into positive, negative, ambiguous.
- **Discuss:** why asserting on exact model text guarantees the suite gets disabled.
- **Name the gap, and the lesson:** both harnesses existed and were good — ~200 lines for triggers, ~280 for the pipeline, with dry-run modes and clear failures. Nothing ran them. Seventeen capabilities accumulated with overlapping domains and **no behavioural evidence that any of them routed correctly**. The lesson is not that the harness was wrong: *a test suite with no trigger is a tool, not a gate, and tools that require remembering do not get used.*
- **End with:** wire it to the event that should trigger it — editing a description.

**Sits between:** card 03 (supplies the failure modes as test cases) · card 09 (the structural gate) → **this** → card 15 (same philosophy, knowledge bases)

---
Source: `../cards/10-behavioral-evaluation-harness.md` · Skeleton: `../skeletons/10-behavioral-evaluation-harness/`
