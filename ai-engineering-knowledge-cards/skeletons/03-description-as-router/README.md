# Skeleton — Description-as-Router

Two pairs of skill stubs and a trigger-case file.

`colliding/` holds the failure: two descriptions that both claim "cluster
problems", with no triggers and no exclusions. Which one fires is a coin flip
the author cannot observe.

`corrected/` holds the same two capabilities with the contract applied. The
boundary between them is now explicit and mutual: one plans and excludes
executing, the other executes and excludes diagnosing. Each names the other.

`trigger-cases.json` is the input a behavioral harness (card 10) replays to
assert which skill actually fires. The third case is deliberately ambiguous —
it is the one worth re-running after any description edit.

Run order: read `colliding/`, predict which fires, then read `corrected/`.
