---
name: bench-triage
description: >
  Parses a CIS benchmark report and produces a triage table with a
  recommended disposition per finding. Runs alongside the gap-scan agent.
model: small
---

# Benchmark triage agent

A fabricated subagent definition in the shape the component used.

## Task

1. Read the benchmark report.
2. Run the parser script on it and keep its JSON.
3. Run the renderer script, which writes the triage table to the output path.
4. Return a short summary to the orchestrator: totals, actionable failures,
   control-plane failures, and the table's path.

## Classification

- Controls 1.x and 3.x are control plane (they need platform-team approval)
- Controls 4.x are worker node
- Controls 5.x are policy

## Tools

Use: Bash, Read
Do NOT use: Edit, Write (the renderer writes the table)
