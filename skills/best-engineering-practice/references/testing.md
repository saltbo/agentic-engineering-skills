# Testing Engineering Constraints

Use this reference whenever a change adds or changes production behavior, test
architecture, a contract, a migration, or a CI quality gate. Apply
`references/core.md` first; this reference makes its testing requirements
measurable across Unit, Integration, Contract, BDD, and E2E suites.

## Contents

- [Choose The Cheapest Complete Proof](#choose-the-cheapest-complete-proof)
- [Keep Test Layers Honest](#keep-test-layers-honest)
- [Write Behavioral Unit Tests](#write-behavioral-unit-tests)
- [Exercise Real Integration Boundaries](#exercise-real-integration-boundaries)
- [Prove Critical Journeys With E2E](#prove-critical-journeys-with-e2e)
- [Use BDD As A Traceable Product Specification](#use-bdd-as-a-traceable-product-specification)
- [Test Deployment Contracts](#test-deployment-contracts)
- [Prove Migrations And Authentication](#prove-migrations-and-authentication)
- [Keep Tests Deterministic And Isolated](#keep-tests-deterministic-and-isolated)
- [Define Inventory Applicability Mechanically](#define-inventory-applicability-mechanically)
- [Measure Coverage By Behavior](#measure-coverage-by-behavior)
- [Derive Inventories And Enforce CI Gates](#derive-inventories-and-enforce-ci-gates)
- [Capture E2E Failure Evidence](#capture-e2e-failure-evidence)
- [Apply The Testing Completion Gate](#apply-the-testing-completion-gate)

## Choose The Cheapest Complete Proof

Assign each behavior to the cheapest layer that can prove it completely:

- use a Unit test for domain rules, state transitions, application orchestration,
  deterministic transformations, stable error handling behind fake ports, and
  browserless component behavior through its public UI contract;
- use an Integration test when correctness depends on a real router, middleware
  chain, serializer, datastore, migration, queue protocol, or external protocol;
- use a Contract test when independently deployed producers and consumers need
  to prove the same versioned wire contract;
- use E2E only for a small set of critical cross-stack user journeys.

Do not repeat the complete business decision matrix mechanically at every
layer. Test the rule once at its cheapest complete layer, then use higher layers
to prove wiring, protocol translation, and a representative success and failure
path. A higher-layer test may repeat a critical invariant when the cross-layer
integration is itself a material risk.

Make every test prove one complete behavior. Multiple related assertions are
appropriate when they jointly describe that outcome. Name the test after the
behavior and observable result, not the method under test.

## Keep Test Layers Honest

Give each test one structural source of layer classification:

- when the repository has dedicated suite directories, use ordinary filenames
  such as `integration/orders.test.ts`; do not repeat `integration` in the name;
- when tests are colocated, classify them with the established filename pattern
  or runner configuration;
- do not classify the same test through conflicting directory, suffix, tag, and
  configuration conventions.

Keep each runner configuration explicit about its included files, environment,
dependencies, setup, timeout, and parallelism. A fast test that uses a mocked SQL
driver is not an Integration test. A browser test that bypasses the backend or
storage is not E2E.

Use `unit`, `integration`, and `e2e` as the canonical BDD proof-layer vocabulary.
A `web`, `component`, or `jsdom` project is a runtime subdivision of the Unit
proof layer unless it crosses a real application boundary. Do not create a fifth
coverage denominator merely because React needs a different test runtime.

Use Builders or Factories with valid defaults for test data. Make the few values
that matter to the scenario explicit. Reject giant hand-written objects,
cross-suite mutable fixtures, and opaque global fixture state.

Use snapshots only for a small, stable structure that is meaningfully reviewed
as a whole. Do not use snapshots as the default assertion style or to encode
business semantics. Understand every changed value before accepting an update.

## Write Behavioral Unit Tests

Test a public module through its public contract. For a substitutable capability,
prefer in-memory Fakes and simple Stubs supplied with the Port or contract.
Test pure functions, immutable values, and UI components directly. Assert
returned values, state changes, emitted domain facts, and stable failure
categories.

Use interaction assertions only when the interaction is part of the contract,
such as charging once, publishing one event, or avoiding a forbidden write. Do
not mock pure functions, private methods, implementation details, or every
internal collaborator. Do not assert call order unless ordering is itself a
business or protocol guarantee.

Inject time, random values, identifiers, and nondeterministic boundaries. Cover
normal behavior, meaningful error handling, and critical invariants. Derive
expected results from the specification, worked examples, or another independent
source of truth rather than reproducing the production algorithm in the test.

Apply mutation testing periodically to critical pure business modules such as
money calculations, authorization rules, and state machines, or when those
modules change materially. Track mutation score separately from statement
coverage. Do not make mutation testing a universal per-PR gate.

## Exercise Real Integration Boundaries

The boundary named by an Integration test must be real. Dependencies outside
that boundary may use a protocol-level Fake.

- Repository tests use the production datastore engine at a production-compatible
  version, the real schema, and real migrations. Never mock the SQL or datastore
  driver and never substitute SQLite for PostgreSQL, D1, or another engine whose
  semantics differ.
- API tests run the real router, middleware order, request validation,
  authentication propagation, serialization, error mapping, and application
  assembly.
- External-adapter tests use a local fake server that speaks the real HTTP, RPC,
  webhook, or SDK-level protocol. Never use a production third party from CI.
- Queue-consumer tests exercise the real message codec and consumer entry
  boundary with an isolated queue or faithful protocol implementation.

Require the following profiles when applicable:

- API operation: success and applicable validation failure, authentication
  denial, authorization denial, and state conflict as separate profiles;
- Repository adapter: reads and writes through the real schema and migrations,
  plus critical constraints, transactions, and concurrency semantics;
- External adapter: success, protocol failure, and translation into every
  declared stable port error category;
- Queue consumer: success, duplicate delivery, retryable failure, and
  non-retryable failure;
- Observability boundary: exactly one structured completion log per attempt,
  stable fields, correct synchronous or asynchronous correlation, trace
  extraction and injection, complete failure classification, and absence of
  secrets and ordinary body data. Require a separate start-event profile only
  when a declared long-running task contract enables it.

Assert stable structured fields and classifications, not incidental prose log
messages.

## Prove Critical Journeys With E2E

An E2E test exercises the real frontend, backend, router, authentication-context
propagation, and storage for one user-observable journey. Keep the suite small
and reserve it for journeys involving at least one of these risks:

- authentication, session continuity, permissions, or tenant isolation;
- onboarding, initialization, or the first successful product use;
- the product's core create, submit, or completion flow;
- money, irreversible action, sensitive data, or realistic data-loss risk;
- a serious historical cross-stack regression.

Mark each required journey with a stable `critical` classification. Adding,
removing, or weakening that classification changes the product verification
specification and requires deliberate review. Do not replace a critical journey
with isolated frontend mocks or direct backend setup that skips the behavior the
journey exists to prove.

Do not hide E2E instability with runner retries, quarantine, fixed sleeps, or
required-test skips. Fix the race, readiness signal, selector, or environmental
isolation. Full E2E execution may remain primarily in CI because it is slow;
local full-suite execution is optional, but the same command and bootstrap must
be available locally. A focused local subset is encouraged.

## Use BDD As A Traceable Product Specification

Use lightweight Gherkin `.feature` files as the source of truth for
user-visible product behavior. Write scenarios in domain language and observable
outcomes. Do not mention database tables, HTTP paths, CSS selectors, classes,
mocks, or implementation steps.

Every scenario has one unique stable ID and declares its cheapest canonical
proof layer, for example `@id:ORD-001 @proof:unit`. The proving test carries a
machine-readable reference such as `[spec:ORD-001]`. A lint gate must prove that:

- every scenario ID is unique and maps to at least one executable test;
- the referenced test exists in the declared proof layer;
- no required scenario or proving test is skipped;
- deleted or renamed scenarios leave no orphaned test reference.

Do not require a Cucumber-style runner by default. Plain Unit, Integration, or
E2E tests can prove the scenario. Add an executable Gherkin runner only when
nontechnical stakeholders genuinely need to read and run that representation.

Update or add the scenario before implementing a new or changed user-visible
capability. A pure refactor, dependency update, performance-only change, or
behavior-preserving migration does not require a scenario change. For a bug,
add a scenario only when the product specification was missing or ambiguous;
otherwise add a regression test linked to the existing scenario.

## Test Deployment Contracts

Use Contract tests only at independent deployment boundaries. For an OpenAPI or
other owned protocol contract, validate the artifact, verify runtime responses
against it, and require both provider and consumer to use a compatible version.
Add consumer-driven contracts only when independently released consumers need
to express requirements the provider contract cannot safely capture.

Do not add Contract tests between modules deployed as one process. Do not let a
Contract test replace the provider's Integration test: schema compatibility does
not prove middleware, storage, authorization, or behavior.

For versioned events, test producer encoding and consumer decoding against the
same published schema, including compatibility rules and stable error handling.

## Prove Migrations And Authentication

Migration Integration tests must:

- apply the complete migration history to an empty production-compatible
  datastore;
- upgrade representative data from every supported production schema version;
- compare the resulting schema with the declared canonical schema to detect
  drift;
- prove backfills are idempotent, resumable, and safe after interruption where
  those properties are required.

Never validate only an ORM's current schema or only an empty database.

E2E may use a test authentication adapter, test signing keys, or local JWKS, but
the bypass must be structurally impossible in a production build or
configuration. Test the real production authentication adapter separately at
its Integration boundary. E2E must still exercise application authorization,
permissions, ownership, and tenant rules rather than treating test identity as
automatic authorization.

## Keep Tests Deterministic And Isolated

Tests must not depend on execution order, wall-clock time, uncontrolled random
values, public network access, or residue from another test. Inject clocks,
random generators, and identifiers. Seed randomized tests and print the seed on
failure. Wait on observable readiness or state instead of sleeping for a fixed
duration.

Reset or uniquely isolate databases, queues, caches, files, accounts, and
namespaces. Parallelize by isolation. Run a suite serially only when a real
global resource cannot be isolated, and record the resource and reason next to
the configuration.

Every local or CI E2E run must create a clean, isolated environment:

- dynamically allocate ports instead of using the project's default development
  port;
- create unique temporary configuration, storage, database, cache, queue, and
  browser-state locations or namespaces;
- run migrations and initialization from a clean starting point through the
  same bootstrap used in CI;
- register cleanup that runs after success or failure, after failure evidence
  has been preserved.

Never share the ordinary local-development configuration or persistent state
with E2E.

## Define Inventory Applicability Mechanically

Generate one normalized inventory record for every testable boundary:

```text
kind | stable id | production source | required profiles
```

Derive the records from production-owned declarations, not a parallel testing
checklist:

- use OpenAPI `operationId` when OpenAPI is authoritative;
- otherwise use the framework's route registry plus code-adjacent access,
  validation, and concurrency metadata that also constructs the route;
- derive Repository, external Adapter, and Consumer identities from their
  production registries or architecture-enforced directories, with capability
  metadata exported beside the contract;
- derive migration paths from migration history and the supported-version
  policy;
- derive each shared observability-boundary implementation and every concrete
  request, Consumer, scheduled, and CLI entry wired through it from production
  composition and registries;
- derive stable errors from the Port's enumerable error taxonomy;
- derive frontend routes from the production router and user-visible queries and
  commands from the feature operation registry;
- derive BDD and critical journeys from feature tags.

For an API operation, require `success`; require `validation` when it accepts
input, `authentication` when it is not public, `authorization` when it addresses
owned, tenant, role, or field-scoped data, and `conflict` when it performs a
state transition, conditional write, uniqueness-sensitive write, or other
concurrency-sensitive command. For a Repository, derive `read`, `write`,
`constraint`, `transaction`, and `concurrency` from the Port operations and
declared invariants. External Adapters require `success`, `protocol-failure`,
and every stable error mapping. Consumers always require `success`, `duplicate`,
`retryable`, and `non-retryable`.

A migration-history item requires `empty-history` and `schema-drift`, plus
`backfill-resume` when a backfill exists. Generate one separate
`migration-upgrade` item for every supported production schema version and
require its `upgrade` proof with representative data. A single generic upgrade
tag may not stand in for several supported starting versions.

Give observability two explicit inventory kinds:

- `observability-boundary` represents one shared middleware or task wrapper. It
  requires `completion`, `correlation`, `redaction`, and `unexpected-failure`.
  Derive `trace-extract` when it accepts incoming trace context,
  `trace-new-root` when it must create a root in the absence of parent context,
  and `trace-inject` only when the boundary invokes a traced downstream
  dependency. Add `start` only for a task explicitly classified as long-running.
- `observability-entry` represents every registered route, Consumer, scheduled
  handler, or CLI command and requires `wired`. Its production record names the
  entry mode and shared boundary that owns its execution. Lint that the modes
  match and that scheduled entries use a new-root-only scheduled boundary. This
  keeps the denominator independent of how many entries happen to share one
  middleware implementation.

Integration proof for the boundary exercises its telemetry semantics;
Integration proof for each entry establishes that the concrete production
entry actually passes through that boundary. A scheduled entry creates a new
root Trace; it does not pretend to extract an originating request context.

An omitted default profile is allowed only when it is semantically impossible,
not merely inconvenient. Record the reason, owner, and expiry or removal
condition beside the production declaration. This exception metadata is part of
the generated inventory and is linted like a manual special-case entry.
Do not except an observability boundary's derived contract or a concrete
entry's production wiring.

Use this exact shape for an exception in a generated inventory item:

```json
{
  "profileExceptions": [
    {
      "profile": "authentication",
      "reason": "The operation is reachable only through an authenticated private service binding",
      "owner": "orders",
      "removalCondition": "Remove when the operation becomes directly network-addressable"
    }
  ]
}
```

Prefer deriving a profile as inapplicable from authoritative operation metadata;
use an exception only when that derivation cannot express the semantic fact.

Tag each covered inventory pair explicitly, for example
`[case:operation:updateOrder:authorization]` or
`[case:repository:postgres-order-repo:transaction]`. Repeat `[case:*]` in one
test title when one coherent test genuinely proves several related pairs; do
not duplicate setup and execution merely to satisfy metadata. The inventory
linter must fail on an unregistered production boundary, duplicate ID, unknown
case, missing required profile, wrong proof layer, skipped proof, or stale
exception. Its denominator is every generated `(item, required profile)` pair;
an item is covered only when every pair maps to an executable test in a required
passing suite.

Keep governance metadata as literal tokens in a statically named `test(...)` or
`it(...)` title so the lint does not need to execute test discovery. Parameterized
tests may implement the matrix underneath, but each required profile and BDD ID
still needs one static, layer-classifiable proof title.

Treat that source scan only as preflight. It generates an expected artifact for
every statically declared test in every required root, keyed by proof layer,
source file, and title; it does not establish coverage. Require each test file
to contain at least one supported static `test` or `it` declaration, including
the explicit concurrent/sequential forms, so runner include patterns cannot
silently omit a whole file. After each required suite runs,
parse the runner's native machine-readable report and require every expected
file/title pair in that layer to have executed and passed. Reject interrupted or
empty reports, pending or skipped tests, expected failures, retries, repeats,
and reports whose total, passed, and executable assertion counts disagree.
Static source text alone is never proof that a test ran. Use a runtime integrity
reporter when the native JSON format omits retry or expected-failure metadata.

## Measure Coverage By Behavior

Enforce these independent blocking thresholds:

| Gate | Required threshold |
| --- | ---: |
| Unit production-code coverage | at least 90% |
| BDD scenario traceability | 100% |
| Integration boundary coverage | 100% |
| Frontend behavior inventory | 100% |
| Critical E2E journey coverage | 100% |

Also require zero skipped tests in every required suite.

The Unit threshold uses statement coverage, or the ecosystem's closest
production-code equivalent, for modules assigned to the Unit layer. Apply it
per production package or module and to changed code; exclude generated code
and generated mocks. Do not reclassify business logic as an adapter or execute
it only through Integration/E2E to evade the Unit gate. Apply the Core's
documented legacy-debt exception only to pre-existing code, never to added or
modified behavior.

Do not represent Integration and E2E confidence with line coverage. Compute
behavioral coverage from machine-derived inventories:

```text
boundary coverage = passing required (inventory item, profile) pairs
                    / all required (inventory item, profile) pairs

critical journey coverage = passing required critical journeys
                            / all declared critical journeys
```

A mapping without an executable passing test is uncovered. A skipped test,
wrong-layer mapping, missing required profile case, or stale tag is uncovered.

Give every stable port failure category a machine-readable identity. Tag
adapter production tests and upper-layer handling tests with equivalent metadata
such as `[case:port-error:payments/timeout:produce]` and
`[case:port-error:payments/timeout:handle]`. Require 100% of declared
categories to be both produced by the adapter and handled by the owning upper
layer. Delete an obsolete category instead of keeping an untestable inventory
entry.

## Derive Inventories And Enforce CI Gates

Generate inventories from authoritative project artifacts whenever possible:

- API operations from OpenAPI `operationId` values;
- production repositories, external adapters, and queue consumers from their
  architecture-enforced directories or explicit runtime registries;
- frontend routes from the actual router plus production route metadata, and
  frontend transports, queries, and commands from typed-client and feature-owned
  runtime declarations;
- shared observability boundaries from production middleware and task-wrapper
  composition, and their concrete request, Consumer, scheduled, and CLI entry
  wiring from the corresponding runtime registries;
- migration paths from migration metadata and the supported-version policy;
- BDD scenarios and critical journeys from feature IDs and tags;
- proofs and required profiles from test metadata such as
  `[case:operation:createOrder:success]` or
  `[case:repository:postgres-order-repo:transaction]`.

Use a manual manifest only for a special case that cannot be derived. Each
manual entry must include the reason, owner, and expiry or removal condition.
Lint inventories, tags, duplicates, unknown references, and required profiles in
CI. Do not let a manually maintained checklist become the primary coverage
source.

Make the generator consume production-owned route, adapter, Consumer,
observability, and enumerable Port-error registries that are also used by
composition. Compare declared routes to the runtime router and registered
adapter files to architecture-owned directories; read migration history from
disk. Emit deterministic per-kind counts and a content digest, then have the
linter recompute both. CI regenerates the artifact before linting, so a hand-
edited denominator cannot substitute for production discovery.

A generic collector cannot prove its own provenance. Add a stack-specific
source or import-graph gate that proves the collector imports the actual router,
composition registries, and feature wrappers rather than cloned arrays. Treat
the supplied collector comparison as incomplete until that gate exists; review
the adapter whenever the production composition mechanism changes.

Run the source lint before the suites to produce a versioned expected-proof
artifact. Run the native-report verifier after Unit and Integration, and make
the isolated E2E supervisor verify the Playwright JSON report before reporting
success. The report is authoritative for execution status; the source scan is
authoritative only for the expected mapping.

Every pull request must block on applicable Unit, Integration, Contract, BDD
traceability, coverage, and Critical E2E gates. A required gate cannot run only
nightly. Fail on focused-only tests, required `.skip` or `.todo` tests, and empty
required suites. Run mutation testing, load tests, and long pressure tests on a
schedule or when relevant modules change. Use the same declared commands in
local and CI environments.

## Capture E2E Failure Evidence

Before E2E cleanup removes the isolated environment, preserve enough evidence
to diagnose the failed journey:

- browser trace, screenshots, console output, and network failure summary;
- structured server and worker boundary logs;
- request, correlation, and Trace IDs;
- the test report and seed or allocated-environment identifiers.

Publish the evidence as CI artifacts with an explicit retention policy. Redact
credentials, tokens, sensitive bodies, and personal data. Do not upload a full
database snapshot by default.

## Apply The Testing Completion Gate

Reject completion when any of the following is true:

- a behavior is proven only at a more expensive layer without justification;
- a fake replaces the boundary that an Integration or E2E test claims to prove;
- a required profile, stable error category, BDD scenario, or critical journey
  is missing, stale, skipped, or unmapped;
- the Unit production-code threshold is below 90%, or any behavioral coverage
  inventory is below 100%;
- a required pull-request test gate is nightly-only, retried into success,
  quarantined, weakened, or suppressed;
- a required suite contains `.only`, `.skip`, `.todo`, or zero executed tests;
- a test depends on order, fixed sleeps, public services, default development
  ports, shared development data, or uncontrolled time or randomness;
- repository or migration tests use a datastore with materially different
  semantics from production;
- an E2E failure is cleaned up before safe diagnostic evidence is preserved;
- BDD scenarios describe implementation details instead of product behavior;
- snapshots or interaction assertions conceal the behavior under test.
