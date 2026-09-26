# Anti-sycophancy

Evaluator sycophancy is the single largest threat to this workflow. Each
pattern below is literally accurate and converts a failure into a pass.

## 1. Score inflation
> "Handles most cases well. 4/5."

"Most cases" is not "all specified cases". Score the gap, not the intention.

Correct: "3 of 5 specified error branches are tested. 2 (expired token,
malformed header) have no coverage. 2/5."

## 2. Hedge-as-pass
> "This might need some attention, but the approach is sound."

A blocker disguised as a suggestion. If an axis is below threshold, say
blocking.

Correct: "Query at routes.py:23 interpolates user input into SQL. Injection
vulnerability. Blocking. 1/5."

## 3. Praise sandwich
> "Great type annotations. The auth logic hardcodes a secret. Nice structure."

Framing a critical flaw between positives anchors the reader on the praise.

Correct: lead with the blocking issue. Praise, if any, goes last and separate.
