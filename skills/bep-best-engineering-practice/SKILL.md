---
name: bep-best-engineering-practice
description: Perform an explicitly requested comprehensive engineering-practice audit across relevant disciplines.
---

# Comprehensive Engineering Audit

Use only for an explicitly requested cross-discipline audit. Preserve the existing
explicit-only invocation policy. A review-only request does not authorize repairs;
a request to audit and fix includes in-scope correction and local acceptance.

Read [audit scope](references/core.md), then inspect only the relevant disciplines:

- `$bep-backend-engineering`: backend ownership and dependencies.
- `$bep-frontend-engineering`: browser state and feature boundaries.
- `$bep-http-engineering`: request lifecycle semantics.
- `$bep-best-openapi-design`: resource and representation design.
- `$bep-software-testing`: test pyramid and behavioral proof.
- `$bep-verification-gates`: explicitly scoped formal verification governance.
- `$bep-software-debugging`: an actual fault investigation.
- `$bep-delivery-engineering`: migration or deployment work.
- `$bep-production-verification`: requested deployed-environment regression.
- `$bep-engineering-review`: a concrete change's outcome and risk.

Load separately installed specialists only when their actual workflow is needed.
Missing optional specialists are a limitation of that specialist review, not a
reason to abandon independent work. Report findings with evidence, separate defects
from preference differences, and identify unresolved verification.
