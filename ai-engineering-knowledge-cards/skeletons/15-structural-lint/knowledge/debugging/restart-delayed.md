---
title: "Restart-delayed failures"
category: debugging
created: 2026-01-05
---

# Restart-delayed failures

A class of fault where the broken dependency does not affect running processes,
only ones that restart. Health signals stay green while the fault is live, and
the outage arrives later, detached from its cause. Probe the dependency
directly rather than watching the consumers, and restart one non-critical
consumer deliberately after any change to an injected dependency.

## Sources

- [[daily/2026-01-05.md]]
