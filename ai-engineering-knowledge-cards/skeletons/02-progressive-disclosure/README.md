# Skeleton — Progressive Disclosure

The same capability, structured two ways.

```
good/SKILL.md            body is procedure only
good/references/         knowledge, loaded when the body says to
good/scripts/            executed, never read into context
good/assets/             appears in the output
bloated/SKILL.md         one file: procedure + taxonomy + algorithm + template
levels.py                reports the cost of each level, finds dead resources
```

## Try it

```bash
python3 levels.py
echo "feat!: drop the v1 endpoint" | python3 good/scripts/detect_breaking.py
```

The second command is the pattern's central economy: that script's cost to an
agent is the line it prints, not the file it lives in. The bloated skill
expresses the same logic as a paragraph of prose that is paid for on every
single trigger, and which a model may or may not execute correctly.

Compare the two L1 lines in the report. The bloated skill's description is
shorter — and routes worse, because it carries no triggers and no exclusions.
Small is not the goal; **carrying the right thing at each level** is.

## What is deliberately missing

**A real runtime.** Nothing here actually defers loading; `levels.py` only
measures what would be deferred. The saving is real only if the runtime
executes `scripts/` without reading them.

**Grep hints.** `references/taxonomy.md` is small. A long reference needs the
body to name search patterns instead of instructing a full read, and the body
here does not model that.
