# Write the incident record — MEDIUM freedom

A preferred structure exists; the content varies. Fill the template; do not
reorder the sections.

```markdown
---
title: "<symptom>, not <cause>"
severity: low|medium|high
detected: <how it was noticed — this field is the most useful one>
---

## What happened
<two to four sentences, no jargon>

## Timeline
| Time | Event |

## Root cause
<one sentence that predicts the symptom>

## Why detection was slow
<omit only if detection was immediate>

## Actions
- [ ] <each one assignable to a person>
```

Rules: title names the symptom because that is what the next person will
search for. Leave `detected` honest even when the answer is "a user told us".
