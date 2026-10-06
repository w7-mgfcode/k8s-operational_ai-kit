# Checkpoint {checkpoint}

Sprint: {sprint} | Environment: {environment}

## Workstreams

| WS | Name | Status | Validation |
|---|---|---|---|
{workstream_rows}

## Triggers

| Trigger | State |
|---|---|
| Transit schema agreed | [resolved/unresolved/deferred] |
| TLS stable after A | [stable/unstable/pending] |
| Benchmark items conflict with platform | [no_conflict/conflict/pending] |

## Evidence

- Lint: [PASS/FAIL]
- Syntax check: [PASS/FAIL]
- Secrets-store health: [all 5 pods healthy / issues]
- Policy violations: [before] → [after] ([delta])
