---
title: "Operator stops reconciling after TLS enablement"
category: incidents
created: 2026-01-05
---

# Operator stops reconciling after TLS enablement

The sync operator had no CA in its trust bundle, so it failed the handshake.
Roughly two dozen workloads held stale credentials with no alert firing,
because running workloads keep what they already hold.

## Key points

- The operator needs the CA explicitly.
- Failure is restart-delayed, so monitoring stays green.

## Related

- [[debugging/restart-delayed]] — why nothing paged
- [[connections/trust-chain]] — the full dependency chain

## Sources

- [[daily/2026-01-05.md]]
