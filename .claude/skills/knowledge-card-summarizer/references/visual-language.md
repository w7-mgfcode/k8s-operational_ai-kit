# Visual language

A diagram earns its place when it explains a relationship faster than a sentence
would. If the sentence is faster, write the sentence.

## When a diagram is right

| Use | Shape |
|---|---|
| The pattern's position in a stack | vertical layers |
| Control or data flow | top-to-bottom pipeline |
| A fan-out from one source to many consumers | a branch |
| A boundary between two responsibilities | a divider with the boundary named |

## When it is wrong

- Restating a list that is already a list
- More than about eight nodes — split it or cut it
- Both the stack *and* the flow in one figure; pick the one the lecture needs
- Any box whose label repeats its parent heading

## Conventions

ASCII, not Mermaid — a teaching card is read in a terminal, a diff, and on a
projector, and ASCII survives all three. Keep to 72 columns so it does not wrap.

Layers, for "where does this sit":

```
INSTRUCTION      the one contract every agent reads
     │
ROUTING          descriptions decide which capability fires
     │
  ┌──┴──┐
SKILL  SUBAGENT  the units that do work
```

Flow, for "how does it work":

```
SOURCE ──▶ hash ──┬──▶ unchanged ──▶ skip
                  └──▶ changed ────▶ COMPILE ──▶ OUTPUT + ledger
```

Boundary, for "what separates what":

```
  plans, never executes  │  executes, never diagnoses
      cluster-doctor     │     log-investigator
                    the boundary is mutual:
                 each description names the other
```

## The rule

One idea per diagram. A lecturer draws one figure on the board and talks for five
minutes. Give them that figure, not a system map.
