# Test requirements

When adding or modifying code under `widgets/`:

1. New modules (`widgets/<name>.py`) MUST have a test at
   `spec/unit/spec_<name>.py`.
2. Use fixtures from `spec/conftest.py`, not setUp/tearDown.
3. Run `invoke spec-unit` before committing.
4. See `VISION.md` for the lean-over-sprawling principle this supports.

Minimum coverage target: 80%.
