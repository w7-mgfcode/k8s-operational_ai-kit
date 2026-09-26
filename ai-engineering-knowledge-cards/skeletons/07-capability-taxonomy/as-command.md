---
description: Audit declared dependencies against actual imports
argument-hint: [path-to-manifest]
---

# /dependency-audit (as a COMMAND)

Fires only when the user types the name. Takes an explicit argument:
`$ARGUMENTS` is the manifest path.

**Cost:** nothing, until invoked.

**Why a command:** it takes a target, it runs to completion, and the user
knows when they want it. No routing contract is needed because the user has
already decided.

**The catch:** a user who has forgotten this exists gets zero value from it.
Discoverability is this container's unsolved half.
