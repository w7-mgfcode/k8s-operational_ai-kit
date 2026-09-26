---
name: cluster-doctor
description: >
  Executes remediation for a diagnosed cluster issue: applies manifest changes,
  restarts workloads, and verifies recovery, gating every destructive step on
  explicit user confirmation. Triggers on: "apply the fix", "restart the failing
  workload", "execute the remediation plan", "roll the deployment", "fix it now".
  Do NOT use for: diagnosis or planning (use log-investigator), read-only
  audits (use cluster-audit), or any run where no plan has been approved.
---

# Cluster Doctor

Executes an approved plan. Never diagnoses from scratch.
