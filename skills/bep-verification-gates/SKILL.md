---
name: bep-verification-gates
description: Build or audit formal proof inventories, coverage policy, native-report reconciliation, or blocking CI gates. Not for ordinary tests.
---

# Verification Governance

Establish what the task is governing: coverage thresholds, BDD traceability,
production inventories, execution integrity, or CI enforcement. Loading this
skill does not adopt every mechanism or expand a local change to the whole repo.

For a new governance setup, use BEP preferences in the relevant references.
For an existing project, inspect its configured policy and supported runners;
preserve them unless the requested work includes a policy transition. A new
project's test pyramid does not require a bespoke proof adapter before it can
have useful tests. Introduce machinery only for the formal guarantees in scope.

- [Coverage policy](references/coverage-policy.md): BEP 90% Unit and complete
  behavioral coverage thresholds, denominators, and legacy exceptions.
- [Identities](references/identities.md): stable mappings and adopted BDD tracing.
- [Inventories](references/inventories.md): authoritative production discovery and
  applicability. Runtime details are in the backend/frontend verification profiles
  when those separately installed skills are relevant and available.
- [Execution](references/execution.md): framework adapters and native-report integrity.
- [CI](references/ci.md): enforcing the selected required gates.

A test proves one behavior at its cheapest complete layer. A native passing
report proves execution; source discovery proves expectation, never execution.
Preserve failed, skipped, and retry evidence rather than turning it into a pass.

Validate the implemented collector, adapter, or rule locally with meaningful
positive and bypass-oriented negative cases. Reconcile the declared scope with
actual execution. Report missing evidence as a limitation of that guarantee;
do not block unrelated work or invent coverage estimates. Never weaken an
adopted gate just to finish the task.
