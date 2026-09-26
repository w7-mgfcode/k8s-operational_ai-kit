---
title: "{{title}}"
cluster: "{{cluster}}"
namespace: "{{namespace}}"
date: "{{date}}"
workstream: "{{workstream}}"
ranked_option: "{{option_id}}"
prod_guard: "{{prod_guard}}"
---

# {{title}}

## Context

- **Reported symptom:** {{symptom}}
- **Cluster / Namespace:** `{{cluster}}` / `{{namespace}}`
- **Workstream:** `{{workstream}}`
- **Prod guard:** {{prod_guard}}

## Root Cause

**Status:** `{{status}}`

{{root_cause}}

**Evidence:**
{{evidence}}

## Chosen Option

**Option `{{option_id}}` — {{option_title}}**

Not chosen:
{{rejected}}

## Steps

Dry-runnable steps are marked (dry run); destructive ones (destructive).

{{steps}}

## Rollback

{{rollback}}

## Verification

{{verification}}

## Blast Radius

{{blast_radius}}

## Environment Progression

| Env | Prerequisite | Apply | Verify |
|-----|--------------|-------|--------|
{{progression}}

## Redaction Review

{{redaction}}
