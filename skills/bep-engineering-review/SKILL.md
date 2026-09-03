---
name: bep-engineering-review
description: Review a concrete software change for requested-outcome correctness, engineering risk, supported-contract impact, and unresolved findings. Use for explicit code review or engineering audit requests, not as an automatic second pass for every implementation.
---

# Engineering Review

Remain read-only unless the user separately asks to resolve findings.

Review on two independent axes:

1. **Outcome:** compare observable behavior with the request, authorized scope,
   supported contracts, and migration expectations.
2. **Engineering:** compare the implementation with repository conventions and
   only the narrow engineering skills relevant to the changed boundaries.

Classify each non-mechanical change before choosing review depth:

- **High risk:** public or cross-service contracts; authentication,
  authorization, security, or privacy; money, billing, credit, or quota;
  persisted data or migration; concurrency, transactions, distributed work;
  production delivery or another hard-to-reverse decision.
- **Low risk:** localized, reversible, internal, and none of the high-risk
  conditions.
- **Medium risk:** every other non-mechanical change.

Verify every finding against the artifact. Classify severity independently from
scope: `blocking` means the requested outcome is wrong or incomplete, a
supported contract breaks, security or data integrity is at risk, or an
applicable configured gate fails; otherwise it is `non-blocking`. A finding is
`in-scope` only when the current request authorizes its resolution.

Lead with findings ordered by severity and include precise file and line
locations. Then state assumptions, unanswered questions, verification evidence,
and a concise change summary. If there are no findings, say so and identify any
remaining test or review limitation.
