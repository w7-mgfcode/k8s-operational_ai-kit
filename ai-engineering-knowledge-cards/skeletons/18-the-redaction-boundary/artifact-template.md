# Investigation plan: <symptom>

## Context
<what was examined, which environment, when>

## Findings
<evidence — all of it passed through redact.py first>

## Recommended actions
1. <...>

## ⚠ Redaction review

**This section is mandatory.** It is what makes conservative redaction safe to
adopt: over-redaction becomes visible and correctable instead of silently
degrading the artifact.

| Pattern | Line | Was it important? |
| --- | --- | --- |
| secret-data-block | 14 | no — base64 credentials |
| bearer | 21 | no |
| config-block | 25 | no — whole kubeconfig |

## ⚠ Not opened
| Path | Why |
| --- | --- |
| `inventories/prod/group_vars/all/30-vault.yml` | restricted path — check manually |
