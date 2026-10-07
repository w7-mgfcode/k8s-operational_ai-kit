# Implementation Notes: Sprint import-01

## Changes Made

- importer/reader.py:1-80 - reads rows into typed records
- importer/validate.py:1-45 - rejects a row whose key column is empty
- tests/test_importer.py:1-60 - covers the reader and the rejection

## Assumptions

- Dates are ISO 8601; the spec does not say.

## Known Gaps

- Export of rejected rows is not implemented; the spec asks for it and the file scope has no module for it.
- The reader could be improved by streaming the file instead of loading it whole.

## Files Modified

- importer/reader.py
- importer/validate.py
- tests/test_importer.py
