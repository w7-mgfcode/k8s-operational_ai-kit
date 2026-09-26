# Skeleton — The Permission Ladder

```
policy-shared.json    reviewed. 10 allow, 1 ask, 3 deny.
policy-personal.json  uncommitted, unreviewed, accumulating.
ladder.py             evaluates a command; deny is checked FIRST
```

## Try it

```bash
python3 ladder.py                       # four demo commands
python3 ladder.py --audit               # what the personal layer has become
python3 ladder.py "kubectl delete pod x"
```

Note the proportions in the shared policy: **ten allow, one ask, three deny.**
The ask rung has exactly one entry, because every prompt is answered by a human
mid-task who has already approved eleven similar prompts. Asking often is how
you train an operator to stop reading.

`--audit` shows the two failures this pattern reliably produces. Several
personal grants are one-time API fetches from a debugging session that ended
weeks ago. And a broad personal `kubectl:*` sits next to the shared
`kubectl delete:*` deny — safe **only** because deny is evaluated first. Reverse
that ordering and the denylist is bypassable by an entry in an unreviewed file.

The fourth demo command is the honest limit: `bash cleanup.sh` runs a denied
verb inside a script, and the ladder matches command text, so it passes.

## What is deliberately missing

**Hooks.** The most powerful automatic execution in an agent system runs at
lifecycle boundaries, with no prompt and no policy applied —
[card 12](../12-lifecycle-hooks-as-capture-points/). Nothing here models that,
and it is the ladder's largest blind spot.

**Any defence in depth.** Shallow textual matching, nothing else. Treating this
as a security boundary is the most common misuse of the pattern.
