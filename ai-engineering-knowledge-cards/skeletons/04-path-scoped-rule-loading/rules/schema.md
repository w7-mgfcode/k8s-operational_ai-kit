---
paths:
  - "src/db/**/*.sql"
---

# Schema change conventions

1. Every migration MUST have both an up and a down state.
2. SQL keywords MUST be capitalized.
3. NEVER use a destructive statement without a comment explaining why.
