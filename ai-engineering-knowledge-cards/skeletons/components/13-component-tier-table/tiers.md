# Component Tier Table (fabricated)

Every component, ranked by what breaks when it breaks.

## Tiers

### CRITICAL

| Component | Impact | Dependents |
|---|---|---|
| mesh-net | All pod traffic stops | all pods |
| block-store | Every volume-backed workload fails | secrets-store, database, registry |
| cert-issuer | Endpoints break as certificates expire | identity, registry, secrets-store, gateway, trust-bundle |

### HIGH

| Component | Impact | Dependents |
|---|---|---|
| secrets-store | Secret sync stops; consumers fail on restart | api, worker, billing, metrics-sidecar, reports |
| identity | Every login flow breaks | dashboards, registry, cli-login |
| database | Identity and registry lose their backend | identity, registry |

### MEDIUM

| Component | Impact | Dependents |
|---|---|---|
| collector | All telemetry collection stops | logs, metrics, traces |
| metrics | Long-term metrics unavailable | dashboards |
| logs | Log loss | — |
| policy-engine | Policy reports stop | — |

### LOW

| Component | Impact | Dependents |
|---|---|---|
| registry | New pulls fail; running images unaffected | — |
| cache | Session loss | — |

## Shared single points of failure

| System | Impact if down |
|---|---|
| object-store | Every telemetry backend and every backup |
| directory | New directory logins blocked |
| dns-resolver | External name resolution breaks |
| external-idp | Production logins blocked |

## Confirmation

| Tier | Action |
|---|---|
| CRITICAL | Platform-team approval and explicit sign-off |
| HIGH | Always confirm — team-lead approval |
| MEDIUM | Confirm on first occurrence, then trust for the workstream |
| LOW | Proceed with a notification |
