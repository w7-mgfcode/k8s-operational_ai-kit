# Skeleton — Adversarial Role Separation

```
roles/planner.md          decompose. never implement, never evaluate.
roles/generator.md        implement. NEVER score your own work.
roles/evaluator.md        critique, flaw-first, in a fresh context.
anti-sycophancy.md        the named failure patterns, read before every evaluation
contract.json             axes, thresholds, OUT-OF-SCOPE — frozen before work
evaluation-inflated.json  a real-looking evaluation that passes everything
validate_evaluation.py    catches it
```

## Try it

```bash
python3 validate_evaluation.py --contract contract.json --evaluation evaluation-inflated.json
```

Read `evaluation-inflated.json` first and decide whether you would accept it.
It scores every axis at or above threshold, sounds professional, and reports no
blocking issues.

It also contains a non-constant-time token comparison described as "sound", two
untested branches described as "might need some attention", and a penalty for
rate limiting — which the contract explicitly puts out of scope. The validator
finds all of it, because each pattern has a name and a shape.

This is the pattern's core claim: **sycophancy is specific enough to detect
mechanically.** "Be more critical" is not a control. A named catalog and a
structural check are.

## What is deliberately missing

**The loop.** No planner, generator or evaluator actually runs. Real separation
needs three agents in three contexts — the role files here are prompts, and
context isolation is what makes them more than wishes.

**The iteration cap.** The card requires a hard cap with escalation to a human,
because the alternative is either an infinite loop or a quietly lowered
threshold. Nothing here enforces one.
