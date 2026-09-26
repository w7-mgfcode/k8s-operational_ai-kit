---
paths:
  - "src/api/**"
---

# API conventions

1. Every endpoint MUST validate its input at the boundary.
2. Errors MUST use the shared error shape. NEVER return a bare string.
3. NEVER log request bodies — they carry credentials.
