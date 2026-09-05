# Deploy And Verify

## Establish The Release Boundary

Use the project's provider tooling, release command, declared target, and current
support policy. Identify the exact artifact or commit and expected deployed version.
For live data or irreversible changes, establish the supported recovery route before
execution. Do not infer production authority from a request to implement locally.
Reuse authorization already provided for the target and release scope.

## Complete Local Acceptance First

Run the checks required by the changed boundary and the project's configured
release gates. Build or start the deliverable locally as appropriate and exercise
the changed behavior. Fix failures caused by the change before deployment.
Local acceptance is mandatory; it does not mean rerunning unrelated suites until
an arbitrary checklist is full. Report a missing local environment as an unresolved
acceptance limitation, not a pass, and do not deploy past a required unmet gate.

## Deploy The Known Artifact

Execute through the project's established provider workflow and inspect its result.
Respect progressive rollout and promotion stages. A successful deploy command is
not yet proof that the intended release serves the target or that the product works.

## Regress The Deployed Result

Verify the target serves the intended build, then cover changed behavior and the
relevant critical user journeys. Prefer an explicitly selected production-safe
E2E subset sharing local assertions with environment-specific fixtures.

Before running an existing E2E suite, inspect target selection, setup, identity,
side effects, and cleanup. If a modest fixture/selector change enables live use,
implement it within the release scope and validate locally first. Never aim a
local database reset, seeding bootstrap, or unrestricted suite at production.

If automation cannot be adapted reasonably for this release, manually exercise
the affected flows through browser/API tools and record expected versus observed
outcomes. Do not replace a product journey with a liveness check. Report what
prevents reusable live E2E so the missing infrastructure is concrete.

Use the completed suite's evidence for the release report. Follow-up manual checks
should cover gaps or uncertainty, not repeat already proven version and journey
assertions on the same unchanged deployment.

Automated and manual checks must use the explicit target, approved identity for
authenticated work, bounded calls, and safe evidence. Public checks need no login.
Ordinary read-only regression is part of deployment; destructive, billed,
messaging, or customer-data side effects need existing specific authority. Use
unique runner-owned state for authorized test writes, and verify cleanup. Never
borrow an unrelated browser session or expose secrets in logs or artifacts.

When available, `$bep-production-verification` provides suite-design and execution
details. Its absence does not block the bounded checks above.

## Recover And Finish

On a failure, preserve safe evidence, identify the cause, repair change-caused
problems, repeat local acceptance, and redeploy/reverify within the authorized
release scope. Respect the rollout's recovery budget and automatic rollback policy.
Without an established budget, choose a bounded recovery budget proportionate to
release risk. Continue causal repair within it; stop repeated deployment when the
same failure recurs without new evidence or the budget is exhausted.
Do not roll back incompatible data or expand side effects without authority.

Finish only when the deployed version and scoped regression pass, or report the
concrete unresolved blocker. Include local acceptance, deployed artifact/target,
regression method and results, cleanup, and any remaining verification gaps.
Do not describe a deployed-but-unverified release as fully complete.
