# Skeleton — One Contract, Many Routers

```
CONTRACT.md               owns every rule. the only place a rule is stated.
routers/vendor-a.md       adapter: mechanics only
routers/vendor-b.md       adapter: mechanics only, no glob loading -> uses the index
routers/vendor-c-BROKEN.md  the failure: restates policy, and has already drifted
commands/commit.md        a namespace stub that names its canonical source
check_routers.py          greps routers for restated policy
```

## Try it

```bash
python3 check_routers.py        # exits 1 — vendor C carries three findings
```

Look at what it reports for vendor C. Rule 1 is a faithful copy, which is
merely duplication. Rules 2 and 3 have **already diverged** — one now demands
an issue number, the other a second reviewer, and neither requirement exists in
the contract. Nobody edited three files; somebody edited the file that was open.

Vendor B is the interesting correct case: it has no automatic rule loading, so
its router sends the agent to the scoped-rule index by hand. That is why the
index in [card 04](../04-path-scoped-rule-loading/) is load-bearing rather than
decorative.

## What is deliberately missing

**Enforcement.** This check exists and nothing runs it. In the source system no
such check existed at all, which is how a rules directory governing an entirely
different project survived for months — see
[card 05](../../cards/05-instruction-provenance-and-drift.md).

**Semantic comparison.** Word overlap catches copies and near-copies. A rule
restated in genuinely different words passes clean.
