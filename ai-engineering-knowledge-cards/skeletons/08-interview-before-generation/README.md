# Skeleton — Interview Before Generation

```
tier_rules.json     which sections are required, defaulted or optional per tier
                    + which persona asks each one
partial-brief.yaml  a brief that arrives half-filled
validate_brief.py   decides completeness mechanically, not by judgment
```

## Try it

```bash
python3 validate_brief.py --brief partial-brief.yaml --tier moderate   # exits 0
python3 validate_brief.py --brief partial-brief.yaml --tier complex    # exits 1
```

The same brief, two verdicts. That is the tier model working: a simple
artifact should not be interrogated like a complex one, and a complex one must
not pass with a defaulted safety section.

Note what the run prints first — the four sections it found already filled, and
that it will not ask about them. That is the fast path, and it is the
difference between an interview a user finishes and one they abandon.

Note also that applied defaults are **announced**. A default is a decision made
by the system rather than the user; silently applying one is how a user
discovers a behavior nobody chose.

## What is deliberately missing

**The interview itself.** No questions are asked here. This is only the gate the
interview loops against — the part that has to be mechanical, because the part
that is a judgment call will always be answered optimistically.

**Tier estimation.** The tier is passed in. In a real implementation it is
inferred from the request, which happens when the least is known, and a
misjudged tier is this pattern's most likely failure.

**Sync with the generated artifact.** Once something is built from this brief,
the brief is stale immediately and nothing keeps the two aligned.
