# Technology-Independent Engineering Core

Apply these constraints to every task using this skill. Runtime, protocol, and
verification references add specialist rules without replacing this Core.

## Contents

- [Start From Observable Behavior](#start-from-observable-behavior)
- [Handle Failure Explicitly](#handle-failure-explicitly)
- [Observe Execution Boundaries](#observe-execution-boundaries)
- [Keep Design And Ownership Simple](#keep-design-and-ownership-simple)
- [Keep Dependencies State And Lifecycles Explicit](#keep-dependencies-state-and-lifecycles-explicit)
- [Protect Compatibility And Security](#protect-compatibility-and-security)
- [Deliver Reproducibly](#deliver-reproducibly)
- [Prove And Diagnose Behavior](#prove-and-diagnose-behavior)
- [Review The Changed Scope](#review-the-changed-scope)
- [Apply The Completion Gate](#apply-the-completion-gate)

## Start From Observable Behavior

- Define success in terms a user, caller, operator, or downstream system can
  observe.
- Read the requirement, current behavior, supported contracts, and release
  baseline before changing code.
- Separate the required capability from a mechanism suggested by the request.
- Resolve hard-to-reverse interface and data-model ambiguity before implementation.
- Work in vertical slices that keep one behavior, its implementation, and its
  proof together.
- Preserve the requested task mode. Analysis and review remain read-only unless
  the user authorizes a change.
- For products, services, CLI tools, and other systems with behavior observable
  by users, callers, operators, or downstream systems, maintain BDD
  specifications as `specs/**/*.feature`. Pure libraries need not adopt BDD
  solely to satisfy this profile.
- Keep `specs/` limited to BDD Feature files. Let each file describe a
  cohesive subject: extend it when new behavior belongs there, and create or
  split files when distinct behavior would weaken its cohesion. Judge that
  boundary from product semantics, not code layout or fixed size limits.

## Handle Failure Explicitly

Classify predictable failures as errors and unexpected failures as exceptions
or fatal invariant violations using the platform's native model.

- Check returned failures where they occur and return when the current layer
  cannot resolve them.
- Preserve the original cause while adding useful operation context. Expose
  stable types or codes for programmatic decisions; never parse error text.
- Keep domain errors independent from HTTP, storage, SDK, or provider types.
  Translate them only at the owning boundary.
- Retry only transient failures at the boundary that owns the complete
  operation. Require idempotency, finite attempts, backoff, jitter, and a total
  deadline.
- Recover unexpected failures only at a request, task, process, or declared UI
  execution boundary. Do not convert corrupted or unknown state into success.
- Add fallback or degraded behavior only when it is an explicit product or
  architecture capability with semantics, observability, tests, and recovery.
- Validate untrusted input at real system boundaries. Do not scatter redundant
  internal checks for states that established invariants exclude.

## Observe Execution Boundaries

- Emit one structured completion event at each request, job, consumer, process,
  or independently recoverable UI execution boundary.
- Record stable operation identity, result, duration, correlation or Trace
  context, and safe error classification. Never log credentials or bodies by
  default.
- Return failures through internal layers and log once at the execution
  boundary instead of logging the same error repeatedly.
- Use low-cardinality Metrics for aggregation, Traces for causal flow, Logs for
  execution context, and audit events for security-sensitive or regulated
  operations.
- Propagate cancellation, deadlines, and Trace context through synchronous and
  asynchronous work.

## Keep Design And Ownership Simple

- Choose the simplest design that satisfies the current requirement. Inspect
  the data model and responsibility split before adding conditionals, helpers,
  layers, or fallback branches.
- Give each business rule and mutable state one owner. Organize by stable domain
  capability rather than controller, datastore, screen, or generic utility
  categories.
- Prefer small public interfaces with cohesive implementations. Delete
  forwarding layers, dead code, obsolete branches, and abstractions without a
  real boundary.
- For a substitutable capability consumed by business code, keep one canonical
  contract, production implementation, and contract-owner-provided test double.
  Let an inner caller own each outward Port it requires.
- Keep protocol parsing at transport boundaries, business rules in their domain
  modules, and provider or persistence details in outer implementations.
- Prefer clear names and data flow over comments and clever expressions.

## Keep Dependencies State And Lifecycles Explicit

- Pass databases, clients, clocks, configuration, and other dependencies through
  constructors or explicit parameters. Avoid mutable global state.
- Prefer immutable values. When mutation is required, make its owner, scope,
  synchronization, and lifetime visible.
- Read and validate configuration once at startup, convert it to typed immutable
  values, and fail startup for missing required configuration.
- Give every external call a timeout or deadline derived from the operation
  budget.
- Give every thread, coroutine, goroutine, or asynchronous task an owner,
  concurrency bound, cancellation path, error propagation, and cleanup or join
  behavior. Do not create fire-and-forget work.
- Enforce critical data invariants in one authoritative place with transactions,
  atomic operations, and datastore constraints where appropriate.
- Prefer the standard library for reliable simple work and mature libraries for
  standards, protocols, authentication, cryptography, and established algorithms.

## Protect Compatibility And Security

- Compare compatibility against published versions still covered by a support
  promise, not an earlier state of unreleased work.
- Improve unreleased contracts directly and update their current callers. For a
  supported contract, use its version and migration policy.
- Give temporary compatibility paths, feature flags, dual reads, and dual writes
  an owner, supported range, observability, tests, and deletion condition.
- Use an expand-migrate-switch-contract sequence for live data or rolling
  deployment when required, and remove temporary branches after migration.
- Authenticate at the execution boundary and produce a normalized principal.
  Authorize separately against the resource, operation, ownership, tenant,
  state, and requested fields.
- Keep credentials, tokens, private keys, and secrets out of source, version
  control, URLs, ordinary logs, caches, and error responses.
- Use established implementations for OAuth, OIDC, cryptography, signatures,
  and token formats.

## Deliver Reproducibly

- Lock dependency and critical tool versions. Make generation and builds
  deterministic from a clean environment through declared commands shared by
  local development and CI.
- Keep generated artifacts with the source change when they form one logical
  unit. Publish immutable tags and traceable build artifacts.
- Use Conventional Commits for commits. Mark breaking changes explicitly and
  keep each commit focused on one coherent reason for change.
- Define a rollback or prepared roll-forward path before production release.
- Give every temporary feature flag an owner, observation plan, and deletion
  condition. Remove migration and compatibility branches when their supported
  transition ends.

## Prove And Diagnose Behavior

- Map changed observable behavior to the cheapest executable proof that proves
  it completely.
- Use real semantics for transports, persistence, external adapters, consumers,
  migrations, browser boundaries, and deployment contracts. Internal mocks do
  not prove an external boundary.
- Run every configured formatter, compiler, type checker, static analyzer, test,
  contract validator, generator check, architecture gate, coverage gate, and
  build applicable to the changed scope.
- Require at least 90% coverage of added or modified production logic assigned
  to the unit layer. Require complete proof for every affected integration
  boundary profile and critical E2E journey. Use passing native reports rather
  than estimates; load the quality-gate reference when its inventory, exception,
  or CI protocol is needed.
- Never skip a check, suppress a valid finding, or lower a threshold to create a
  passing result.

For a bug or regression:

1. Create one fast deterministic reproduction of the exact symptom.
2. Minimize it and rank falsifiable causes.
3. Test one cause at a time with a targeted probe.
4. Convert the reproduction into a failing test at the correct public seam.
5. Apply the smallest causal fix and rerun both focused and original scenarios.
6. Remove temporary instrumentation and report the actual cause.

Measure a baseline before performance work. Treat unbounded queries, fan-out,
concurrency, memory, collections, and per-item dependency calls as design defects.

## Review The Changed Scope

- Keep public contracts and critical operational behavior documented beside the
  system they govern. Record project architecture decisions worth preserving
  for future engineering work under `docs/adr/`. Use judgment about their
  continuing architectural relevance; do not exclude a decision merely because
  it is reversible or include incidental implementation detail.
- Treat a change as mechanical only when it cannot alter compiled behavior,
  runtime behavior, stored data, generated contracts, public output, dependency
  resolution, or execution order.
- Classify every non-mechanical change before review:
  - **High risk:** affect a public or cross-service contract; authentication,
    authorization, security, or privacy; money, billing, credit, or quota;
    persisted data or migration; concurrency, transactions, or distributed
    workflow; production delivery or rollback; or another hard-to-reverse
    decision.
  - **Low risk:** remain localized, reversible, and internal; affect no runtime
    or external boundary; and meet none of the high-risk conditions.
  - **Medium risk:** include every other non-mechanical change.
- Review every non-mechanical change on two axes: **Outcome** against the request,
  authorized scope, and supported contracts; **Engineering** against this Core,
  loaded references, and repository standards.
- Scale reviewer independence by risk:
  - For low risk, run the axes as two separate self-review passes.
  - For medium risk, prefer one reviewer context independent from implementation
    to review both axes. When unavailable, run the axes as two separate
    self-review passes and report the limitation.
  - For high risk, use two independent reviewer contexts isolated from the
    implementation reasoning and from each other's initial findings.
- When high-risk independent reviewer capability is unavailable, run both axes
  separately, report the limitation, and leave the independent-review gate
  unmet.
- Verify each finding against the artifact, then classify it on two independent
  dimensions:
  - **Severity:** `blocking` when the requested outcome is wrong or incomplete,
    a supported contract breaks, security or data integrity is at risk, or an
    applicable loaded or configured gate fails; otherwise `non-blocking`.
  - **Scope:** `in-scope` when resolution is authorized by the current request;
    otherwise `out-of-scope`.
- Resolve in-scope blocking findings and rerun affected checks. For an
  out-of-scope blocking finding, report the blocker and request direction without
  expanding mutation authority. Report non-blocking findings and any explicitly
  accepted risk without representing them as fixed.
- When authorized implementation encounters a Core violation or competing
  internal pattern, define its signature and search the complete repository.
  Correct instances inside the authorized scope and report the remaining
  inventory. Mutate every equivalent instance and require a zero-match result
  only when the user explicitly authorizes repository-wide migration. Preserve
  supported public behavior and apply versioning or data migration when a
  correction crosses a published or persisted boundary.

## Apply The Completion Gate

Reject completion when any applicable condition holds:

- the requested outcome lacks observable executable proof;
- an error is swallowed, downgraded, repeatedly logged, or disguised as success;
- an unrequested fallback or redundant internal defense exists;
- business rules, mutable state, concurrent work, or external calls lack a clear
  owner and lifecycle;
- provider, storage, framework, or protocol details leak into business policy;
- a supported contract or persisted-data transition lacks a versioned migration;
- secrets can enter source, logs, URLs, caches, or ordinary errors;
- an applicable loaded or configured gate is skipped, weakened, or unresolved;
- a high-risk change lacks the required independent review;
- outcome or engineering review has an unresolved blocking finding.

## Influence

The feedback-loop, vertical-slice, deep-module, seam, behavior-testing,
diagnosis, and two-axis review ideas were adapted and reorganized from Matt
Pocock's MIT-licensed [`skills`](https://github.com/mattpocock/skills)
repository, copyright 2026 Matt Pocock. The enforcement model and combined
constraints reflect the preferences established for this skill.
