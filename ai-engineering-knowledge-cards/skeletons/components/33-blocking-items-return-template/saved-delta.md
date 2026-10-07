# Return Report: Sprint s1 - Iteration 1 to 2

Rule: address every item below. Focus only on blocking issues.

## Blocking Items

### 1. Missing column raises KeyError

- **Axis:** error_handling
- **Current score:** 2/5 (threshold: 3/5)
- **Location:** importer.py:41
- **What is wrong:** a row with a missing column raises KeyError
- **What passing looks like:** wrap the lookup in a try block and report a row error

### 2. Accented header names are rejected

- **Axis:** correctness
- **Current score:** 3/5 (threshold: 4/5)
- **Location:** [file:line]
- **What is wrong:** headers containing accents fail to parse
- **What passing looks like:** headers containing accents parse

### 3. Function names mix two styles

- **Axis:** code_quality
- **Current score:** 3/5 (threshold: 3/5)
- **Location:** importer.py:5
- **What is wrong:** function names mix two styles
- **What passing looks like:** one naming style

## Constraints

- Stay inside the file list this sprint was given.
- Do not address non-blocking notes.
