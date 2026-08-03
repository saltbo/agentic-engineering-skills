# Testing Engineering Constraints

Apply these constraints whenever production behavior, test architecture,
contracts, migrations, or test infrastructure changes. This reference defines
proof-layer semantics and test behavior. The quality-gate and runtime-specific
verification references define inventories, thresholds, metadata, and CI proof.

## Contents

- [Choose The Cheapest Complete Proof](#choose-the-cheapest-complete-proof)
- [Keep Test Layers Honest](#keep-test-layers-honest)
- [Write Behavioral Unit Tests](#write-behavioral-unit-tests)
- [Exercise Real Integration Boundaries](#exercise-real-integration-boundaries)
- [Test Deployment Contracts](#test-deployment-contracts)
- [Prove Critical Journeys With E2E](#prove-critical-journeys-with-e2e)
- [Write Traceable Product Specifications](#write-traceable-product-specifications)
- [Keep Tests Deterministic And Isolated](#keep-tests-deterministic-and-isolated)
- [Capture E2E Failure Evidence](#capture-e2e-failure-evidence)
- [Apply The Testing Completion Gate](#apply-the-testing-completion-gate)

## Choose The Cheapest Complete Proof

Assign each behavior to the cheapest layer that can prove it completely:

- use Unit for domain rules, state transitions, application orchestration,
  deterministic transformations, stable error handling behind fake Ports, and
  browserless component behavior through its public UI contract;
- use Integration when correctness depends on a real router, middleware chain,
  serializer, datastore, migration, queue protocol, browser runtime, or external
  protocol;
- use Contract at independent deployment boundaries where producers and
  consumers must prove one versioned wire contract;
- use E2E for a small set of critical cross-stack user journeys.

Test the complete decision matrix once at its cheapest complete layer. Use
higher layers to prove wiring, protocol translation, and representative success
and failure paths. Repeat a critical invariant only when cross-layer integration
is itself a material risk.

Make every test prove one complete behavior. Multiple related assertions are
appropriate when they jointly describe that outcome. Name the test after the
behavior and observable result, not the implementation method.

## Keep Test Layers Honest

Give each test one structural source of proof-layer classification. Use suite
directories, established filename patterns, runner projects, or native metadata;
never classify one test through conflicting conventions.

Keep each runner configuration explicit about included files, environment,
dependencies, setup, timeout, isolation, and parallelism. A fast test using a
mocked datastore driver is not Integration. A browser test bypassing the backend
or durable storage is not E2E.

Use `unit`, `integration`, and `e2e` as the canonical BDD proof-layer vocabulary.
A `web`, `component`, or `jsdom` runner project is a runtime subdivision of Unit
unless it crosses a real application boundary. Contract proof is additional
deployment-boundary verification and does not create another BDD denominator.

Use Builders or Factories with valid defaults for test data. Keep scenario-
relevant values explicit. Reject giant hand-written objects, cross-suite mutable
fixtures, and opaque global fixture state.

Use snapshots only for small, stable structures that reviewers can understand
as a whole. Understand every changed value before accepting an update. Snapshots
do not encode business semantics by default.

## Write Behavioral Unit Tests

Test a public module through its public contract. For a substitutable capability,
use in-memory Fakes and simple Stubs supplied with the Port or contract. Test
pure functions, immutable values, and UI components directly.

Assert returned values, state transitions, emitted domain facts, stable failure
categories, and observable UI behavior. Use interaction assertions only when
the interaction is itself the contract, such as charging exactly once,
publishing one event, or avoiding a forbidden write.

Keep private methods, implementation structure, pure internal collaborators,
and incidental call order out of assertions. Derive expected results from the
specification, worked examples, or another independent source rather than
reproducing the production algorithm in the test.

Inject time, random values, identifiers, and nondeterministic boundaries. Cover
normal behavior, meaningful error handling, and critical invariants.

Apply mutation testing periodically to critical pure business modules such as
money calculations, authorization rules, and state machines, or when those
modules change materially. Track mutation score separately from statement
coverage. Mutation testing is not a universal per-PR gate.

## Exercise Real Integration Boundaries

The named boundary must be real. Dependencies outside it may use a
protocol-faithful Fake. Run the production codec, schema, middleware,
configuration, and assembly that define the boundary's semantics.

Use runtime-specific verification profiles to derive every required boundary
case. Assert stable protocol results, classifications, state transitions, and
structured fields rather than incidental prose, timestamps, formatting, or
vendor messages.

An Integration test cannot claim a datastore, router, queue, browser, identity,
or external protocol that it replaced with an in-process imitation lacking the
same semantics.

## Test Deployment Contracts

Use Contract tests only at independent deployment boundaries. For an OpenAPI or
other owned protocol contract, validate the artifact, verify runtime responses
against it, and require provider and consumer to use compatible versions.

Add consumer-driven contracts only when independently released consumers need
to express requirements the provider contract cannot safely capture. Do not add
Contract tests between modules deployed as one process. Contract compatibility
does not replace provider Integration proof of middleware, authorization,
storage, or behavior.

For versioned events, test producer encoding and consumer decoding against the
same published schema, including supported-version compatibility and stable
failure handling.

## Prove Critical Journeys With E2E

An E2E test exercises the real frontend, backend, router, application
authorization, and storage for one user-observable journey. Reserve E2E for
journeys involving at least one of these risks:

- authentication, session continuity, permissions, or tenant isolation;
- onboarding, initialization, or first successful product use;
- the product's core create, submit, or completion flow;
- money, irreversible action, sensitive data, or realistic data-loss risk;
- a serious historical cross-stack regression.

Mark each required journey with a stable `critical` classification. Adding,
removing, or weakening that classification changes the verification
specification and requires deliberate review.

Exercise the behavior the journey exists to prove. Frontend mocks or direct
backend setup cannot replace authentication, permission, persistence, or
cross-stack behavior inside that journey.

Fix E2E races, readiness signals, selectors, and environment isolation. Required
journeys may not rely on runner retries, quarantine, fixed sleeps, or skips.
Full execution may remain primarily in CI when slow, but the same bootstrap and
command must be available locally.

## Write Traceable Product Specifications

Write BDD scenarios in domain language and observable outcomes. Keep database
tables, HTTP paths, CSS selectors, classes, mocks, and implementation steps out
of product specifications.

Use the quality-gate reference for stable scenario identities, canonical proof
layers, proof mappings, and traceability lint. Update the specification before
new or changed user-visible behavior, then implement its cheapest complete
proof.

A pure refactor, dependency update, performance-only change, or behavior-
preserving migration does not change the scenario. For a bug, add a scenario
only when the product specification was missing or ambiguous; otherwise add a
regression test linked to the existing scenario.

## Keep Tests Deterministic And Isolated

Tests must not depend on execution order, wall-clock time, uncontrolled random
values, public network access, fixed sleeps, default development ports, or
residue from another test. Inject clocks, random generators, and identifiers.
Seed randomized tests and print the seed on failure. Wait on observable
readiness or state.

Reset or uniquely isolate databases, queues, caches, files, accounts, browser
state, and namespaces. Parallelize by isolation. Run a suite serially only when
a real global resource cannot be isolated, and record the resource and reason
beside the runner configuration.

Every local or CI E2E run must:

- dynamically allocate ports;
- create unique temporary configuration and state locations;
- migrate and initialize from a clean starting point through the CI bootstrap;
- register cleanup for success and failure after diagnostic evidence is saved.

Never share ordinary local-development configuration or persistent state with
E2E.

## Capture E2E Failure Evidence

Before cleanup, preserve:

- browser trace, screenshots, console output, and network failure summary;
- structured server and worker boundary logs;
- request, correlation, and Trace identities;
- native test report, random seed, and isolated-environment identifiers.

Publish the evidence as CI artifacts with an explicit retention policy. Redact
credentials, tokens, sensitive bodies, and personal data. Do not upload a full
database snapshot by default.

## Apply The Testing Completion Gate

Reject completion when any of the following is true:

- a behavior is proven only at a more expensive layer without justification;
- a Fake replaces the boundary that an Integration or E2E test claims to prove;
- a test asserts implementation structure instead of observable behavior;
- a required test depends on order, fixed sleeps, public services, default
  development ports, shared development data, or uncontrolled nondeterminism;
- a required E2E journey uses retries, quarantine, skips, or cross-run residue;
- BDD scenarios contain implementation details or changed behavior lacks its
  traceable specification;
- snapshots or interaction assertions conceal the behavior under test;
- failure cleanup removes required diagnostic evidence;
- the loaded quality-gate or runtime verification profile remains unmet.
