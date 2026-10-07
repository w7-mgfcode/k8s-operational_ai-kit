# Benchmark Triage Table

Report: [path to the benchmark report]
Date: YYYY-MM-DD
Total findings: [N] | PASS: [N] | FAIL: [N] | WARN: [N]

## Failed controls

| Control ID | Description | Classification | Disposition | Rationale | Owner | Sprint target |
|---|---|---|---|---|---|---|
| 1.x.x | [description] | control_plane | TBD | | | |
| 4.x.x | [description] | worker_node | TBD | | | |

## Disposition legend

| Code | Meaning |
|---|---|
| implement | Fix in this sprint |
| defer | Move to a later sprint with a reason |
| NA | Not applicable here |
| TBD | Not yet decided |

## Decision rules

- Sections 1 and 3 (control plane) need platform-team approval before `implement`.
- Section 4 (worker nodes) may be implemented without further approval.
- Section 5 (policies) is reviewed against the admission-policy workstream.
- Deprecated-pattern items are pre-filled `NA`.

## Summary

- Actionable failures: [N]
- Control-plane failures needing approval: [N]
- Deferred: [N]
- Not applicable: [N]
- Still undetermined: [N]
