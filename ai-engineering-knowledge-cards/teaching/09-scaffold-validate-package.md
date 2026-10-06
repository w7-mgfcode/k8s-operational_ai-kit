---
card: 09
title: Scaffold, Validate, Package
layer: skill
maturity: proven
source: ../cards/09-scaffold-validate-package.md
---

# Scaffold, Validate, Package

> Give capabilities a build pipeline: create from a template, check mechanically, and refuse to package anything that fails the check.

**Status:** proven — three scripts (~140/200/200 lines) plus a ~280-line functional
harness driving them over crafted cases, including cases that must fail.

## 1. Why

The rules governing a capability's format are numerous, individually trivial, and
individually **silent when broken**. A name that is not lowercase; a description over
the limit; a body past the cap; a README where the format forbids one; a reference
nested one level too deep. Each is small, none produces an error, and together they
yield a capability that loads badly or not at all.

Checking by reading is unreliable. Nobody counts lines by eye, and the author is the
worst-placed person to notice their own description drifted past a limit.

**Without it:** capabilities are malformed in small ways, discovered by strange
behaviour rather than by an error, and the format's rules become folklore.

## 2. Core Idea

Three stages, with the third **gated on the second**.

That gate is the whole pattern. A validator that can be skipped is advice; a
validator whose failure blocks packaging is a rule.

## 3. Architecture

```
  brief (card 08)
       │
       ▼
  ┌──────────┐  name rules  ┌────────┐  format rules  ┌──────────┐
  │ SCAFFOLD │ ───────────▶ │ AUTHOR │ ─────────────▶ │ VALIDATE │
  └──────────┘              └────────┘                └────┬─────┘
                                 ▲                         │
                                 │ fix and re-run     pass │ fail
                                 └─────────────────────────┤
                                                           ▼
                                                    ┌──────────┐
                                                    │ PACKAGE  │
                                                    └──────────┘
                                          re-runs validation · REFUSES on failure
```

## 4. How It Works

1. **Validate the name before creating anything** — cheapest rejection point is before a directory exists.
2. Scaffold the full structure including *empty* conventional directories; their presence teaches where scripts, references and assets go. Card 02 expressed as a filesystem.
3. Emit a stub with required fields present and marked incomplete — the requirement is visible where the work happens.
4. Check **only mechanically decidable** properties. Whether the capability is *good* is not decidable, and a validator attempting it produces noise that trains people to ignore it.
5. Separate errors from warnings; let only errors block. All-fatal gets bypassed, none-fatal gets ignored.
6. **Test the pipeline itself** — including inputs that must fail, verifying packaging actually refuses.

## 5. Key Components

| Component | Role | Without it |
|---|---|---|
| Mechanical rule set | Only decidable properties can be validated | Validator drifts into taste and gets ignored |
| Non-zero exit | Everything downstream keys off it | The gate silently passes |
| Packager re-running validation | Enforcement lives here, not in habit | Validation becomes optional, therefore skipped |
| Tests for the pipeline | The enforcement mechanism is itself code | A silently broken gate is worse than no gate |

## 6. Decisions That Matter

- **The validator guarantees "well-formed", never "good."** Treating a green check as quality approval is the likeliest misuse.
- **Leave undecidable rules out.** When the format acquires a rule that cannot be checked mechanically, enforce it by review or behavioural test — do not make the validator opinionated.
- **Stops being the interesting work** once the rule set stabilises; the binding constraint moves to behaviour (card 10), and the pipeline's job becomes preventing regression.

## 7. Trade-offs

| Choice | Benefit | Cost |
|---|---|---|
| Gate packaging on validation | Converts documentation into a build error | Creates pressure to weaken the gate — relaxing the rule is easier than fixing the artifact, and each relaxation is invisible |
| Scaffold from a template | Nothing starts malformed | Encodes today's structure, mistakes included, into everything built after |
| Mechanical checks only | Trustworthy, never noisy | A capability can pass everything and be useless |

**Most common failure:** rule erosion — limits relaxed one exception at a time until
they bind nothing, because no record exists of why each rule was there.

## 8. What To Remember

1. The gate is the pattern; the three scripts are just scripts without it.
2. Mechanically decidable or not enforced here — no third option.
3. Errors block, warnings inform. Collapse that distinction and the check dies either way.
4. Check: feed the packager a known-bad artifact and confirm it actually refuses.

## 9. Lecture Cue

- **Start with:** five trivial format violations, none of which produce an error message.
- **Draw:** the pipeline with the fix-and-re-run loop, and a thick border on REFUSE.
- **Discuss:** rule erosion — ask who decides when a failing rule is wrong versus when the artifact is wrong.
- **Point at the second use:** the same kit added a fourth script that analysed existing capabilities across ~30 structural axes and scored complexity 1–10. That score fed the tier model in card 08. **The pipeline was not only a gate — it was the measuring instrument that told the author what a complex capability looks like.**
- **End with:** the validator says well-formed. It never says good.

**Sits between:** card 08 (produces the brief) → **this** → card 10 (structure vs behaviour; neither substitutes)

---
Source: `../cards/09-scaffold-validate-package.md` · Skeleton: `../skeletons/09-scaffold-validate-package/`
