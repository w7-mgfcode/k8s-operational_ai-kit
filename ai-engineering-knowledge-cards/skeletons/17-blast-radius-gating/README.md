# Skeleton — Blast-Radius Gating

```
matrix.json   components ranked by DEPENDENT COUNT, plus shared SPOFs
gate.py       lookup -> environment resolution -> confirmation -> dry run
```

## Try it

```bash
python3 gate.py --list
python3 gate.py --component registry     --target staging        # low, proceeds
python3 gate.py --component secret-store --target staging        # high
python3 gate.py --component network-layer --target staging       # typed phrase
python3 gate.py --component network-layer --target staging --confirm "confirm critical change"
python3 gate.py --component registry     --target prod-cluster   # read-only
python3 gate.py --component registry     --target ""             # ambiguous -> STRICT
```

Start with `--list` and notice that the rankings are counter-intuitive on
purpose. The container registry and the API gateway sit at the bottom — cached
images keep working, services stay reachable directly — while certificate
issuance sits at the top. Prominence and blast radius are unrelated, and
ranking by prominence is how people get this wrong.

The last command is the one to internalize. An unqualified target resolves to
**protected**, because the alternative default is the single most expensive
error this pattern can make.

## What is deliberately missing

**Derivation.** The matrix is asserted by hand, so it goes stale with every
architectural change — and a stale matrix is worse than none, because it is
trusted. The real evolution is deriving dependents from live configuration; see
[card 20](../../cards/20-repository-projection-pipeline.md).

**A dry run.** The gate tells you to run one and cannot run one. The final
check before reality is not modelled here.

**Per-change granularity.** Four tiers cannot express that a component is
critical for one operation and isolated for another.
