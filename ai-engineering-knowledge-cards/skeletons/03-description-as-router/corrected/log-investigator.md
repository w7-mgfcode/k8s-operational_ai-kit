---
name: log-investigator
description: >
  Investigates a reported symptom in one namespace by reading logs and events,
  ranks candidate causes by blast radius, and writes an implementation plan to
  disk. Read-only: never mutates cluster state. Triggers on: "investigate this
  issue", "what is broken in namespace X", "plan a fix for this cluster
  problem", "rank remediation options", "draft a fix plan for this symptom".
  Do NOT use for: executing the fix (use cluster-doctor), storage-backend
  symptoms (use storage-doctor), whole-cluster health sweeps (use
  cluster-audit), or any request that does not name a namespace.
---

# Log Investigator

Plans. Never executes.
