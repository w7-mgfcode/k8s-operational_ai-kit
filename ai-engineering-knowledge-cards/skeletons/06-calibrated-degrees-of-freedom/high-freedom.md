# Triage an incoming alert — HIGH freedom

Use when several approaches are valid and the right one depends on context
that cannot be predicted here.

## Guidance

Start from the symptom, not the alert name — alerts are named after what fired,
which is often a consequence rather than a cause.

Work outward from the affected component to the things it depends on, checking
the dependency directly rather than the health of its consumers. A consumer can
look healthy while the dependency it needs on restart is already broken.

Prefer the cheapest observation that would distinguish between your two leading
hypotheses. If no observation distinguishes them, you have one hypothesis.

Stop when you can state the cause in a sentence that predicts the symptom. If
your explanation does not predict the symptom, it is a finding, not a cause.
