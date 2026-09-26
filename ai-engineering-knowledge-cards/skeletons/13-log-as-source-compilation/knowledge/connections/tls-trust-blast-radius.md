---
title: "TLS trust blast radius: CA issuer -> secret store -> sync operator -> workloads"
category: connections
tags: [blast-radius, tls, trust-distribution]
sources: ["daily/2026-01-05.md"]
created: 2026-01-05
updated: 2026-01-05
---

# TLS trust blast radius: CA issuer -> secret store -> sync operator -> workloads

A single trust chain links certificate issuance to roughly two dozen workloads.
Each hop is owned by a different component, so no single owner sees the whole
chain — which is why this belongs in connections rather than in any one article.

## Key points

- Four hops: issuer, secret store, sync operator, consuming workloads.
- Every hop needs the CA independently; none inherits it.
- Impact is restart-delayed at the last hop, which defeats liveness-based alerting.

## Details

Change anything in the first two hops and audit all four. Ordering matters:
distribute trust before enabling TLS, never after.

## Related

- [[incidents/secret-sync-tls-trust-break]] — the incident that exposed the chain
- [[debugging/restart-delayed-failures]] — the detection gap

## Sources

- [[daily/2026-01-05.md]]
