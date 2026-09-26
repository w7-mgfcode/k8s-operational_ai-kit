---
title: "Checkout OOM"
cluster: "dev"
namespace: "shop"
date: "2026-01-12"
workstream: "feat/shop-stability"
ranked_option: "A"
prod_guard: "not-triggered"
---

# Checkout OOM

<!-- Fabricated. A plan as it can come out of the template when nothing checks it:
     every defect below is one the template's shape allows. -->

## Context

- **Reported symptom:** checkout pods crash-looping
- **Cluster / Namespace:** `staging` / `shop`
- **Workstream:** `feat/shop-stability`
- **Prod guard:** not-triggered

## Root Cause

**Status:** `confirmed`

Memory pressure on the checkout pods.

**Evidence:**
- <signal 1>

## Chosen Option

**Option `D` — Cap the cache below the limit**

Not chosen:
- A: raise the memory limit

## Steps

1. run the shop playbook against dev
2. watch pods in shop

## Rollback

<specific command>

## Verification

- no OOMKilled events in shop

## Blast Radius

Namespace-scoped.

## Environment Progression

| Env | Prerequisite | Apply | Verify |
|-----|--------------|-------|--------|
| dev | none | playbook against dev | watch pods |
| staging | dev green | same | same |
| prod | staging green | same | same |

## Redaction Review
