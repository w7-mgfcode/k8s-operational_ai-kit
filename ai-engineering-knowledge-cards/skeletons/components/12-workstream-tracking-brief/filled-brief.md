# Workstream A: Secrets-store TLS

Priority band: quick_win
Status: deferred

## Objective

Serve the secrets store over TLS behind a flag

## Blast radius

- Component: secrets-store
- Tier: MEDIUM
- Dependents: 3 (api, worker, billing)
- Confirmation required: no

## Rollback plan

Turn the flag off and apply
