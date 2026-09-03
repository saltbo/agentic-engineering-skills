---
name: bep-software-debugging
description: Diagnose a reproducible software defect, regression, intermittent failure, or unexplained performance change and identify its causal fix. Do not use for feature implementation, broad refactoring, or speculative hardening without a symptom.
---

# Software Debugging

Preserve diagnosis as read-only unless the user also asks for a fix.

1. State the exact observable symptom and establish a fast deterministic
   reproduction or the closest controlled probe available.
2. Minimize the reproduction and rank falsifiable causes from available
   evidence. Test one cause at a time.
3. Trace the failing path through its real public seam and affected external
   boundary. Add temporary instrumentation only where it distinguishes causes.
4. When a fix is authorized, first preserve the symptom as a red-capable
   regression test at the cheapest layer that proves it completely.
5. Apply the smallest causal correction, rerun the focused test and original
   scenario, then remove temporary instrumentation.

For performance regressions, measure a comparable baseline before changing
code and inspect unbounded queries, fan-out, concurrency, memory, collections,
and per-item external calls before micro-optimizing.

Report the actual cause, the evidence that falsified alternatives, the changed
behavior when fixed, and any remaining uncertainty. Do not convert an unknown
or corrupted state into success with a catch, retry, fallback, or timeout
increase.
