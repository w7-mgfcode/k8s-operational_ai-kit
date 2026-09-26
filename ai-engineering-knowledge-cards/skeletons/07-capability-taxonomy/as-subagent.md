---
name: dependency-auditor
description: Audits dependencies across a large tree and returns only findings.
tools: Read, Glob, Grep
---

# dependency-auditor (as a SUBAGENT)

Runs in a fresh context. Reads every source file in the tree, returns a summary.

**Cost:** one prompt, one summary, one round trip. Nothing before invocation.

**Why a subagent:** auditing a large repository means reading hundreds of files.
Done inline, all of that residue stays in the main session's context for the
rest of the conversation. Done here, the main session receives a conclusion.

**`tools:` is a NARROWING, not a grant.** This agent *cannot* write. That is a
guarantee from the runtime, not a promise in a prompt — which is the difference
between a constraint and a request.

**The catch:** it knows nothing the main session learned. Everything it needs
must be in its prompt, or it will re-derive context and return a confident
answer that ignores what was already established.
