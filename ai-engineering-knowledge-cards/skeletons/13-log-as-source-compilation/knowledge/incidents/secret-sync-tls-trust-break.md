---
title: "Secret-sync operator stops reconciling after enabling TLS on the secret store"
category: incidents
tags: [tls, secrets-operator, trust-distribution]
sources: ["daily/2026-01-05.md"]
created: 2026-01-05
updated: 2026-01-05
---

# Secret-sync operator stops reconciling after enabling TLS on the secret store

Enabling TLS on the secret store broke the sync operator's connection: it had no
CA in its trust bundle. Roughly two dozen workloads held stale credentials
without any alert firing, because running pods keep their injected secrets and
only fail on the next restart.

## Key points

- The operator needs the CA explicitly; it does not inherit the cluster trust store.
- Distributing the CA cluster-wide beats mounting it per client — every client needs it.
- Failure is restart-delayed, so monitoring stays green while the fault is live.

## Details

1. Confirm the handshake failure in the operator logs.
2. Distribute the CA as a secret via the trust distributor.
3. Point the operator's CA reference at that secret; restart it.
4. Verify every sync resource reports ready before declaring recovery.

## Related

- [[connections/tls-trust-blast-radius]] — the full dependency chain
- [[debugging/restart-delayed-failures]] — why monitoring stayed green

## Sources

- [[daily/2026-01-05.md]]
