---
name: bep-software-testing
description: Design, implement, or review automated tests and their proof layers. Not needed merely to run existing tests.
---

# Software Testing

## Build A Proportionate Test Pyramid

Use many fast Unit tests for rules and state transitions, focused Integration
tests for real boundaries, and a small set of critical E2E journeys. This is a
responsibility model, not a fixed numerical ratio or a demand for every layer
when the system has no corresponding boundary.

Assign each behavior to the cheapest layer that can prove it completely:

- Unit: domain decisions, deterministic transformations, orchestration behind
  fake external ports, and browserless component interaction.
- Integration: real datastore, router/middleware, codec, queue, or browser semantics.
- Contract: independently deployed consumers and providers agreeing on a wire contract.
- E2E: a critical user journey through the real application stack.

Cover the full decision matrix once at its owning layer. Higher layers prove
wiring and representative outcomes, not the same matrix again. Browser-only
semantics need real-browser proof; do not add a duplicate simulated Unit matrix.
Mocks cannot prove the boundary they replace. Use observable outcomes rather
than private methods or incidental calls.

## Fit The Project And Change

For a new project, establish a lightweight pyramid using the stack's native
runner, isolated fixtures, and clear local commands. For an existing project,
reuse its runners and conventions; add missing proof at the affected boundary.
Do not impose a suite rewrite, new BDD framework, or coverage governance for an
ordinary test change. Keep complete critical behavior coverage and fast feedback
as the goals, rather than raw test counts or duplicated line coverage.

- [Unit](references/unit.md): behavioral assertions and test doubles.
- [Integration and contracts](references/integration.md): real boundary semantics.
- [E2E](references/e2e.md): critical journeys, isolation, and failure evidence.
- [Specifications](references/specifications.md): creating product specifications
  or working in a project that already uses BDD.
- [Live E2E](references/live-e2e.md): creating or changing E2E runner/fixtures,
  or preparing a deployable regression subset.

Use `$bep-verification-gates` only when building or auditing formal coverage or
CI governance. Its metadata and thresholds are not prerequisites to testing.

## Close The Local Feedback Loop

Local acceptance is required for implementation: run the focused tests and
necessary type/build/contract checks, exercise the changed behavior, fix failures
caused by the change, and rerun affected checks. For a regression, demonstrate
that its proof catches the original symptom where practical. Broaden checks only
when changed boundaries or unresolved failures justify the extra cost.

Keep fast feedback available separately from the critical E2E suite. Measure slow
setup or suites before optimizing; improve isolation, reuse safe setup, and
parallelize independent tests. Do not hide failures using retries or skips.
If a local check cannot run, report the concrete limitation and available evidence;
do not claim acceptance passed. Local acceptance does not require writing a new
automated test for every mechanical or visual edit, nor authorize deployment.
