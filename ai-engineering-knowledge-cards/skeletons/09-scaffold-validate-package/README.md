# Skeleton — Scaffold, Validate, Package

```
scaffold.py       validates the name BEFORE creating anything
validate.py       mechanical checks only; errors block, warnings inform
package.py        re-runs validation and REFUSES on failure
malformed/        a capability with four planted defects
test_pipeline.py  drives the pipeline, including cases that must fail
```

## Try it

```bash
python3 test_pipeline.py                 # ten cases, exits 0
python3 validate.py malformed            # exits 1 — see the four defects
python3 package.py malformed --out /tmp  # exits 1 — REFUSES
python3 scaffold.py Bad-Name             # exits 1 — rejected before any mkdir
```

The third command is the pattern. Everything else here is checks; the refusal
is the enforcement. A validator that can be skipped is a style guide.

`test_pipeline.py` is the part most people leave out. Half its cases assert
that something **fails** — because a silently broken gate passes everything,
including the malformed input it exists to stop, and looks exactly like a
working one.

## What is deliberately missing

**Quality.** Every check here is decidable. None of them can tell you the
capability is useless, and a green result must never be read as approval.

**A reason per rule.** The limits are enforced and unexplained, so relaxing one
under pressure looks like a small edit rather than a decision. Erosion is this
pattern's slow failure.

**Format-change coupling.** When the format gains a rule, this pipeline is
stale until someone updates it, and a stale validator enforces last year's
format confidently.
