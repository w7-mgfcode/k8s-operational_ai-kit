# Benchmark Triage Table

Report: reports/bench-run-a.md
Date: 2026-01-12
Total findings: 41 | PASS: 30 | FAIL: 8 | WARN: 3

## Failed controls

| Control ID | Description | Classification | Disposition | Rationale | Owner | Sprint target |
|---|---|---|---|---|---|---|
| 1.1.12 | Ensure the scheduler profiling endpoint is disabled | control_plane | implement | one flag, low risk | platform | this sprint |
| 1.2.16 | Ensure the API server audit log path is set | control_plane | implement | approved by platform lead in review | platform | this sprint |
| 2.1.4 | Ensure etcd peer TLS uses client certificate auth | other | implement | quick fix | node-ops | this sprint |
| 3.2.1 | Ensure a minimal audit policy is created | control_plane | defer | needs audit sink sizing | platform | next sprint |
| 4.2.6 | Ensure the kubelet protects kernel defaults | worker_node | implement | node config change | node-ops | this sprint |
| 4.1.9 | Ensure the kubelet config file permissions are 600 | worker_node | TBD | | | |
| 5.2.3 | Minimize admission of privileged containers | policy | NA | Deprecated/NA | | |
| 5.1.6 | Ensure service account tokens are mounted only where needed | policy | later | waiting on app teams | apps | next sprint |

## Disposition legend

| Code | Meaning |
|---|---|
| implement | Fix in this sprint |
| defer | Move to a later sprint with a reason |
| NA | Not applicable here |
| TBD | Not yet decided |

## Summary

- Actionable failures: 5
- Control-plane failures needing approval: 2
- Deferred: 1
- Not applicable: 1
- Still undetermined: 0
