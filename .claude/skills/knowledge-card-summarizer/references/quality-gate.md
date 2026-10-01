# Quality gate

Run before writing the file. Any unchecked box means the card is not ready.

## Understanding

- [ ] The central concept is stated in one quotable sentence.
- [ ] The problem is concrete and observable, not abstract.
- [ ] The mechanism is clear enough to recognize this pattern in someone else's system.
- [ ] The relationships between components are correct, not merely plausible.

## Compression

- [ ] 80–120 lines, ~2–2.5x compression. Source was ~200–250.
- [ ] No sentence restates a heading.
- [ ] No implementation detail survives without teaching value.
- [ ] Every section would be missed if removed.

## Teaching

- [ ] A student can answer: what is this, how does it work, what do I remember.
- [ ] A lecturer can open the card cold and start talking.
- [ ] The order runs problem → idea → structure → mechanism → cost → takeaway.
- [ ] The Lecture Cue names one specific thing to draw, not "draw the architecture."

## Integrity — the ones that matter most

- [ ] **A `partial` maturity still reads as partial, and the gap is named.**
      Check the Status line against the source's Provenance section.
- [ ] `maturity` was not upgraded to make the card read better.
- [ ] No conclusion appears that the source does not support.
- [ ] The `related:` edges survive; the card knows its neighbours.
- [ ] Terminology matches the source — no concept was quietly renamed.
- [ ] Nothing identifying was introduced. Nothing was read from `.legacy-assets/`.

## Mechanical checks

```bash
wc -l teaching/NN-*.md                      # 80-120
grep -c '^## ' teaching/NN-*.md             # 9
grep '^maturity:' teaching/NN-*.md cards/NN-*.md   # must match
```

## If the gate fails

Fix the card, not the gate — **with one exception**. The line-count band is the only
threshold here derived from measurement rather than principle, and it currently rests
on a single card. If a real trim pass recovers only a handful of lines, the card is
not bloated and the band is wrong; widen it and record the new measurement. Every
other box in this gate is a principle, not a number: do not negotiate with those.

The most common genuine failure is the third Compression box — an implementation
detail survives because it felt informative. Cut it, then check whether understanding
actually dropped.
