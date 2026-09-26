# Handoff — 2026-01-05

## Next steps

1. Run `make lint` against `roles/gateway` — it fails with an undefined
   variable at `tasks/tls.yml:34`; the name is likely `gateway_tls_secret`,
   defined in `inventories/staging.yml`.
2. Re-run the dry run for workstream A once lint is clean.

## State (gathered mechanically)

- Branch: fix/tls
- Changed files: roles/gateway/tasks/tls.yml
- Recent commits: 3

## Decisions and why

| Decision | Rationale |
| --- | --- |
| Distribute the CA cluster-wide instead of mounting per client | every client needs it; per-client mounts would be four separate changes |

## Dead ends

- Tried setting the CA via the chart's `extraVolumes` — the operator reads its
  trust bundle before volume mounts are ready, so it never sees the file.

## Open questions

- Does the metrics sidecar need the same CA? Unverified.
