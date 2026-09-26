# Skeleton — Behavioral Evaluation Harness

```
cases.json     positive, NEGATIVE and ambiguous prompts — harvested, not invented
baseline.json  recorded accuracy per run, including a real regression
harness.py     replays cases against the skills in card 03's skeleton
```

## Try it

```bash
python3 harness.py --dry-run     # inspect the suite without invoking anything
python3 harness.py               # replay all five cases
python3 harness.py --baseline    # why a single run's number is meaningless
```

**The suite does not pass, and that is the demonstration.** The stub router
over-triggers on `neg-1` (a plain question about a file pulls it into an
investigation) and misses `amb-1` entirely. Those are two of the exact failure
modes [card 03](../../cards/03-description-as-router.md) lists — over-triggering
and silent non-trigger — and neither is visible from reading the descriptions.
You have to run the prompts.

The cases that matter are the ones people leave out. **Negative cases** catch
over-triggering, which is the more annoying failure in daily use and is
invisible to a suite of positives. The **ambiguous case** sits between two
capabilities and is the one worth re-running after any description edit.

`--baseline` shows the reason the aggregate is recorded: on the third run,
editing one skill's triggers fixed nothing and broke a neighbour. Per-case
results alone would not have shown that; only the number moving did.

## What is deliberately missing

**The real invocation.** `invoke()` scores term overlap instead of shelling out
to a CLI. A real harness runs the actual entry point in the actual project
directory, with a timeout — testing a mock of the router tests the mock.

**A trigger.** Nothing runs this when a description changes. That omission is
exactly what happened in the source system: two well-built harnesses, no
recorded baseline, and seventeen capabilities with no behavioral evidence that
any of them routed correctly.

**Repetition.** Behavioral tests are non-deterministic. One failure may be
signal or noise, and telling them apart costs more runs than this suite makes.
