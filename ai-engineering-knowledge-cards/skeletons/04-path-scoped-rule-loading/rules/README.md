# Scoped rule index

Agents without path-glob loading read this table and open the matching rule by
hand. A rule missing from this table is invisible to them.

| File | Loads when touching | Covers |
| --- | --- | --- |
| `api.md` | `src/api/**` | Input validation, error shape, logging prohibitions |
| `schema.md` | `src/db/**/*.sql` | Up/down states, keyword case, destructive statements |
