---
name: bep-best-engineering-practice
description: Run an explicit cross-cutting engineering audit spanning architecture, failure handling, compatibility, delivery, verification, and review. Use only when the user invokes this skill or requests a comprehensive engineering-practice audit; use a narrower engineering skill for ordinary work.
---

# Best Engineering Practice

Audit a software change or system across engineering disciplines. This is the
explicit umbrella workflow, not the default entry point for ordinary coding.

Read [references/core.md](references/core.md), then load only the independently
installed skills relevant to the requested audit:

- `$bep-backend-engineering` for backend ownership and dependency direction;
- `$bep-frontend-engineering` for browser architecture and UI runtime behavior;
- `$bep-http-engineering` for HTTP lifecycle and protocol semantics;
- `$bep-software-testing` for proof-layer and test-design decisions;
- `$bep-verification-gates` for coverage governance and blocking CI policy;
- `$bep-production-verification` for deployed-environment verification;
- `$bep-software-debugging` for a fault or regression investigation;
- `$bep-delivery-engineering` for compatibility, migration, release, or rollback;
- `$bep-engineering-review` for risk classification and review disposition;
- `$bep-best-openapi-design` for REST/OpenAPI resource and contract design.

Preserve the requested task mode. An audit, plan, diagnosis, or review remains
read-only unless the user separately authorizes implementation.

Do not load every skill mechanically. State which disciplines apply, inspect
only those areas, and report the observable outcome, blocking findings,
unresolved risk, and evidence used.
