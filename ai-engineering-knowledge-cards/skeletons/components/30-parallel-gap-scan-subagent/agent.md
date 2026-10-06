---
name: gap-scan
description: >
  Scans the repository's own roles for container hardening fields that are
  missing, and returns an inventory. Runs alongside the benchmark triage agent.
model: small
---

# Gap-scan agent

A fabricated subagent definition in the shape the component used: frontmatter
with a name, a description and a model, and its limits written in the body.

## Task

1. Take the list of owned roles from the orchestrator.
2. For each role, look for these fields in its values and templates:
   `runAsNonRoot`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem`,
   `capabilities.drop: [ALL]`.
3. Return one JSON record per gap: role, file, field, whether the chart exposes
   the field as a value, and a priority.

## Skip

These roles need elevated access by design:

- reboot-daemon
- log-shipper
- node-exporter

## Tools

Use: Glob, Grep, Read
Do NOT use: Bash, Edit, Write
