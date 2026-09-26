---
title: "Restart-delayed failures: when green dashboards hide a live fault"
category: debugging
tags: [diagnostics, alerting, secrets]
sources: ["daily/2026-01-05.md"]
created: 2026-01-05
updated: 2026-01-05
---

# Restart-delayed failures: when green dashboards hide a live fault

A class of fault where the broken dependency does not affect running processes,
only ones that restart. Every health signal stays green while the fault is live,
and the outage arrives later, detached from its cause.

## Key points

- Injected credentials, mounted configs, and cached tokens all behave this way.
- Liveness and readiness probes cannot detect it by construction.
- Detect it by probing the dependency directly, not by watching the consumers.

## Details

After any change to an injected dependency, restart one non-critical consumer
deliberately and verify it comes back. That converts a latent fault into an
immediate, attributable signal.

## Related

- [[incidents/secret-sync-tls-trust-break]] — the instance
- [[connections/tls-trust-blast-radius]] — the chain it hides in

## Sources

- [[daily/2026-01-05.md]]
