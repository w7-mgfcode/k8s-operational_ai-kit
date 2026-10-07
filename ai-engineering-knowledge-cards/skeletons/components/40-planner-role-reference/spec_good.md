# Spec: CSV import module

## Goal
Rows from a supplier CSV file load into the inventory table, with bad rows reported
rather than dropped.

## Constraints
- Python standard library only
- The existing `inventory/schema.py` is not modified

## Sprint Breakdown

### Sprint 1: Row parser
- **Scope:** Turn one CSV line into a typed record or a named error
- **Files:** inventory/parse_row.py, tests/test_parse_row.py
- **Dependencies:** none
- **Acceptance targets:**
  - A row with a non-numeric quantity returns an error naming the column
  - A row with a missing sku returns an error naming the line number
  - Every public function has a type annotation and a docstring
- **Estimated complexity:** simple

### Sprint 2: File loader
- **Scope:** Read a whole file through the row parser and report totals
- **Files:** inventory/load_file.py, tests/test_load_file.py
- **Dependencies:** Sprint 1
- **Acceptance targets:**
  - A file with two bad rows loads the good rows and reports exactly two errors
  - An empty file returns a zero-row report without raising
- **Estimated complexity:** moderate

## Out of Scope
- Streaming very large files
- A command-line wrapper
