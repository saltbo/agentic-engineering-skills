# Backend Verification Profile

Apply this profile only when designing or auditing formal runtime proof
inventories or architecture/browser-quality governance. New governance uses BEP
preferences; existing projects retain their adopted policy unless transition is
in scope. Ordinary runtime edits require focused local acceptance, not these
inventories. Prove each behavior at its cheapest complete layer; additional layers
cover distinct integration risks. Use `$bep-verification-gates` for shared identity,
coverage, and execution protocols only when that governance is in scope.

## Contents

- [Generate Backend Inventories](#generate-backend-inventories)
- [Derive Required Profiles](#derive-required-profiles)
- [Exercise Real Integration Boundaries](#exercise-real-integration-boundaries)
- [Prove Stable Port Errors](#prove-stable-port-errors)
- [Prove Migrations](#prove-migrations)
- [Prove Authentication And Authorization](#prove-authentication-and-authorization)
- [Prove Observability And Entry Wiring](#prove-observability-and-entry-wiring)
- [Prove Service Lifecycle](#prove-service-lifecycle)
- [Enforce Architecture Mechanically](#enforce-architecture-mechanically)
- [Apply The Backend Verification Gate](#apply-the-backend-verification-gate)

## Generate Backend Inventories

Generate these kinds from production-owned declarations, registries, composition,
and architecture-enforced directories:

- `operation` for every HTTP, RPC, or other request operation;
- `repository` for every production persistence Port implementation;
- `external-adapter` for every external protocol or vendor Adapter;
- `consumer` for every queue or durable-message Consumer;
- `migration-history` for the complete migration chain;
- `migration-upgrade` for every supported production schema version;
- `port-error` for every stable error category declared by an inward Port;
- `observability-boundary` for every shared request or task wrapper;
- `observability-entry` for every concrete request, Consumer, scheduled, and CLI
  entry wired through a shared boundary;
- `service-lifecycle` for each deployable service process.

Use authoritative protocol operation IDs when available. Otherwise derive
operations from the real router or handler registry plus code-adjacent access,
validation, and concurrency metadata used to construct it. Derive Repository,
Adapter, and Consumer identities from production registries or mechanically
enforced directories. Derive migrations from history on disk and the supported
version policy.

## Derive Required Profiles

For an operation, always require `success`. Derive:

- `validation` when it accepts input;
- `authentication` when it is not public;
- `authorization` when it addresses owned, tenant, role, or field-scoped data;
- `conflict` when it performs a state transition, conditional write,
  uniqueness-sensitive write, or concurrency-sensitive command.

For a Repository, derive `read`, `write`, `constraint`, `transaction`, and
`concurrency` from its Port operations and declared invariants.

For an external Adapter, require `success`, `protocol-failure`, and production
of every declared stable Port error category.

For a Consumer, require `success`, `duplicate`, `retryable`, and
`non-retryable`.

For a migration history, require `empty-history` and `schema-drift`, plus
`backfill-resume` when a backfill exists. Generate one `migration-upgrade` item
for every supported schema version and require its `upgrade` profile with
representative data.

## Exercise Real Integration Boundaries

The boundary named by an Integration test must be real. Dependencies outside
that boundary may use a protocol-level Fake.

- Repository tests use the production datastore engine at a
  production-compatible version, the real schema, and real migrations. Never
  mock the datastore driver or substitute an engine with materially different
  semantics.
- API tests run the real router, middleware order, request validation,
  authentication propagation, serialization, error mapping, and application
  assembly.
- External-Adapter tests use a local fake server that speaks the real HTTP,
  RPC, webhook, or SDK-level protocol. CI never calls a production third party.
- Consumer tests exercise the real message codec and Consumer entry boundary
  with an isolated queue or faithful protocol implementation.

Assert stable outputs, structured fields, error categories, and protocol
behavior rather than provider message text or incidental formatting.

## Prove Stable Port Errors

Give every stable Port failure category a machine-readable identity. Require:

- a production Adapter test proving the category can be produced from the real
  dependency protocol;
- an owning upper-layer test proving the category is handled or propagated
  according to its contract;
- preservation of the original cause for boundary diagnostics;
- deletion of any category that no Adapter can produce or no consumer handles.

Coverage is 100% of declared categories with both production and handling proof.

## Prove Migrations

Migration Integration tests must:

- apply the complete history to an empty production-compatible datastore;
- upgrade representative data from every supported production schema version;
- compare the result with the declared canonical schema to detect drift;
- prove backfills idempotent, resumable, and safe after interruption whenever
  those properties are required;
- exercise rolling expand, migrate, switch, and contract stages when the release
  plan uses them.

Validating only the ORM's current schema or only an empty database does not
prove migration compatibility.

## Prove Authentication And Authorization

API Integration tests exercise the production authentication boundary or a
protocol-faithful local identity provider. Prove signature and algorithm policy,
issuer, audience, time validity, normalized principal propagation, and stable
authentication failure mapping.

Prove authorization separately against resource identity, ownership, tenant,
role, state, and requested fields wherever applicable. A valid test identity
does not imply authorization.

E2E may use test keys, local JWKS, or a test authentication Adapter only when
that bypass is structurally impossible in a production build or configuration.
Test the production authentication Adapter at its Integration boundary.

## Prove Observability And Entry Wiring

An `observability-boundary` requires:

- `completion` for exactly one structured completion event per attempt;
- `correlation` for synchronous or asynchronous context continuity;
- `redaction` for absence of credentials, secrets, bodies, and uncontrolled
  sensitive content;
- `unexpected-failure` for complete cause, stack, and stable classification.

Derive `trace-extract` when incoming context is accepted, `trace-new-root` when
parentless or scheduled work must create a root, `trace-inject` when the
boundary invokes a traced downstream dependency, and `start` only for a
declared long-running task that needs a progress signal.

An `observability-entry` requires `wired`. Its production record names the entry
mode and shared boundary. Lint that request, Consumer, scheduled, and CLI modes
match their boundary, and that scheduled entries use a new-root-only scheduled
boundary.

Integration proof for the shared boundary exercises telemetry semantics.
Integration proof for every concrete entry establishes that production wiring
actually passes through that boundary. Audit-event verification remains
separate from diagnostic logging while proving required identity and Trace
context.

## Prove Service Lifecycle

For every deployable service, prove:

- invalid required configuration fails startup;
- critical dependency readiness follows the declared policy;
- liveness does not depend on every transient external dependency;
- shutdown marks the service unready before stopping intake;
- in-flight work drains or cancels within the declared deadline;
- telemetry and durable work flush according to their guarantees;
- workers, pools, servers, and resources close in the declared order;
- failure to preserve required shutdown invariants terminates unsuccessfully.

Use isolated process-level or Integration proof appropriate to the lifecycle
mechanism. Source configuration alone is not execution evidence.

## Enforce Architecture Mechanically

Use compiler or package visibility, module boundaries, import rules, dependency
graph analysis, static analysis, or their combination. At minimum, fail CI when:

- Domain imports Transport, Infrastructure, framework, ORM, or vendor modules;
- Application imports a concrete Adapter or Transport;
- Transport imports Adapter-specific errors or datastore types;
- an Adapter leaks ORM, SDK, or wire types through an inward Port;
- composition or container lookup occurs outside the Composition Root;
- dependency cycles cross business-module boundaries.

Every custom rule has positive and bypass-oriented negative fixtures. A
documented directory diagram without mechanical enforcement leaves the gate
unmet.

## Apply The Backend Verification Gate

Reject completion when any of the following is true:

- a production backend inventory item or required profile is missing,
  manually cloned from production, stale, skipped, or uncovered;
- an Integration test replaces the named real boundary with a mock or
  semantically different substitute;
- a stable Port error lacks both production and handling proof;
- a supported migration start version lacks representative upgrade proof;
- authentication or authorization is proven only by a bypass unavailable in
  production semantics;
- an observability boundary lacks correlation, failure, or redaction proof, or
  a concrete entry lacks production wiring proof;
- service startup, readiness, draining, shutdown, or failure semantics lack
  executable proof;
- backend dependency direction exists only in prose;
- an explicitly applicable testing or verification gate remains unmet.
