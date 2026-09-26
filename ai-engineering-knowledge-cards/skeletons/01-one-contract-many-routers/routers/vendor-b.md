# Vendor B router

**Read `CONTRACT.md`. It is the single source of truth for this repository.**
This file adds only mechanics specific to Vendor B.

## Mechanics
- Procedures are invoked by asking for them by name in chat.
- **No path-glob loading.** Consult `rules/README.md` and read the matching
  rule by hand before touching a file. This is why that index is load-bearing.
- Context limit: 32 KiB. Prefer reading one rule over reading the set.
