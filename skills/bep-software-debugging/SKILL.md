---
name: bep-software-debugging
description: Investigate software failures or performance regressions and implement causal fixes. Not for typos or speculative hardening.
---

# Software Debugging

A fix request authorizes local diagnosis, causal correction, and acceptance;
do not ask again whether to fix it. A diagnosis-only request remains read-only
for product implementation; use non-mutating probes or disposable reproductions.

Establish the observable symptom and the smallest deterministic reproduction or
controlled probe. Rank falsifiable causes from evidence and choose probes that
distinguish them. Trace the real public seam and affected dependency boundary.

When fixing, preserve a regression proof that catches the original symptom at
the cheapest sufficient layer where practical. Apply the smallest causal change,
run it locally, exercise the original scenario, and remove temporary instrumentation.
Continue until local acceptance passes or a concrete blocker prevents it.

For performance regressions, compare a baseline and investigate queries, fan-out,
concurrency, memory, and dependency calls before micro-optimizing. In an existing
project, preserve working contracts and architecture; do not turn a bug fix into
an unrelated BEP migration. Never disguise an unknown or corrupted state as success
with a catch, retry, fallback, or timeout increase.

Report the cause, evidence, changed behavior, verification, and remaining uncertainty.
