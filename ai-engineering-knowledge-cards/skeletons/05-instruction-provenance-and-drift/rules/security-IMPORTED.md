# Security patterns

> Vision principle: "Credential safety." See `VISION.md`.

Forbidden in all code under `widgets/`:
- `eval()` with user-controlled input
- Writing credentials to `.registry/packages.json`
- `verify=False` in HTTP clients

Validate every manifest against `schemas/manifest.json` before install.
