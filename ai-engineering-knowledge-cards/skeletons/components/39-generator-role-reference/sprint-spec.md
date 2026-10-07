# Spec: CSV importer

## Sprint 1: Row reader

- **Scope:** read a CSV file into typed records and reject rows with a missing key.
- **Files:**
  - importer/reader.py
  - importer/validate.py
  - tests/test_importer.py
- **Acceptance targets:** every documented column type parses; a row with no key is rejected.
