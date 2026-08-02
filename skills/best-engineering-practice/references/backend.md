# Backend Architecture Constraints

Apply these constraints to services, Web handlers, workers, scheduled jobs,
CLI processes, persistence, messaging, and external integrations. The Core is
authoritative; this reference defines backend ownership and dependency rules
without replacing its failure, observability, testing, or compatibility gates.

Express the architecture through the language and framework's native mechanisms.
Preserve the dependency direction and responsibilities below; do not imitate a
particular directory tree, class diagram, or dependency-injection syntax.

## Contents

- [Use Clean Architecture For Dependency Direction](#use-clean-architecture-for-dependency-direction)
- [Inject Dependencies Without Hiding The Graph](#inject-dependencies-without-hiding-the-graph)
- [Create Use Cases Only For Application Behavior](#create-use-cases-only-for-application-behavior)
- [Put Transactions Around Business Operations](#put-transactions-around-business-operations)
- [Define Ports At Real System Boundaries](#define-ports-at-real-system-boundaries)
- [Let The Inner Consumer Own Each Port](#let-the-inner-consumer-own-each-port)
- [Keep Models Inside Their Semantic Boundaries](#keep-models-inside-their-semantic-boundaries)
- [Shape Repositories Around Domain Resources](#shape-repositories-around-domain-resources)
- [Translate Dependency Failures Into Stable Errors](#translate-dependency-failures-into-stable-errors)
- [Keep Caching Semantically Transparent](#keep-caching-semantically-transparent)
- [Model Queues And Long-Running Work Explicitly](#model-queues-and-long-running-work-explicitly)
- [Separate Domain Events From Integration Events](#separate-domain-events-from-integration-events)
- [Own The Complete Service Lifecycle](#own-the-complete-service-lifecycle)
- [Verify Observability As Behavior](#verify-observability-as-behavior)
- [Enforce Architecture Mechanically](#enforce-architecture-mechanically)
- [Apply The Backend Completion Gate](#apply-the-backend-completion-gate)

## Use Clean Architecture For Dependency Direction

Use Clean Architecture to isolate business policy from delivery and
infrastructure mechanisms:

- **Domain** owns business vocabulary, invariants, and state transitions. It
  does not import Web frameworks, databases, queues, serializers, vendor SDKs,
  or runtime configuration.
- **Application or Use Case** owns business-operation orchestration,
  authorization decisions that require domain context, consistency intent, and
  transaction semantics. It depends on Domain and inward-owned ports.
- **Transport** owns protocol parsing, boundary validation, normalized principal
  extraction, application invocation, and protocol response mapping.
- **Infrastructure Adapter** owns database, cache, queue, filesystem, process,
  clock, random, identifier, and external-service mechanisms. It implements
  inward-owned ports and translates provider behavior.
- **Composition Root** is the one place allowed to know concrete transports,
  adapters, configuration, and the complete dependency graph.

Dependencies point inward. Framework and infrastructure types may not cross
into Domain or Application merely because doing so is convenient.

Do not create layers to resemble an architecture diagram. Delete a controller,
service, use case, repository, or mapper whose only purpose is forwarding the
same arguments and result. The desired outcome is isolated business behavior,
explicit ownership, and testable boundaries.

Organize directories around business capabilities when practical. A repository
may choose packages, modules, classes, functions, or another stack-native
structure as long as imports and ownership follow these rules.

## Inject Dependencies Without Hiding The Graph

Inject every stateful, configurable, side-effecting, or nondeterministic
dependency through a constructor, explicit parameter, or equivalent native
mechanism. Dependency injection is required; a DI container is not.

Use manual construction in the Composition Root when the graph remains clear.
Use a DI container only when the ecosystem has a mature, idiomatic solution and
the container measurably reduces real graph-management complexity. Never add a
container to satisfy an architecture label.

Regardless of mechanism:

- keep registrations and concrete bindings in the Composition Root;
- make missing, duplicate, and cyclic bindings fail at build or startup time;
- prohibit service locators and runtime dependency lookup inside business code;
- keep lifecycle ownership visible for resources that must start and stop;
- let each use case or module receive only its narrow dependency bundle.

The Composition Root may know the full graph. No business object may receive a
global application-wide `Deps`, context, or container that grows whenever an
unrelated module adds a dependency.

## Create Use Cases Only For Application Behavior

Create a Use Case when an operation owns at least one of these responsibilities:

- a business rule or state transition;
- transaction or consistency semantics;
- orchestration across multiple dependencies;
- authorization requiring domain state;
- retry, idempotency, or workflow semantics visible to the product.

A transport that validates input, invokes one port, and maps the result may call
that port directly. Do not manufacture one Use Case per endpoint when the Use
Case would be a pass-through wrapper.

Keep pure cross-entity business collaboration in a Domain service or function.
Keep I/O, transaction, and external dependency orchestration in the Use Case.
Do not move business rules into handlers, repositories, or queue consumers to
avoid creating the application behavior that actually owns them.

## Put Transactions Around Business Operations

The Use Case owns transaction semantics because it knows which complete
business operation must be atomic. The infrastructure layer provides a
transaction or Unit-of-Work mechanism without deciding the business boundary.

- Never open or coordinate a transaction in an HTTP handler, RPC handler, or
  queue consumer.
- Pass transaction-scoped repositories or an explicit transaction context only
  within the operation that owns it.
- Keep external network calls out of database transactions unless the chosen
  consistency design explicitly requires and proves the consequences.
- Prefer a single atomic repository operation when one datastore statement and
  constraint can guarantee the invariant.
- Use an outbox or another explicit consistency protocol when one operation
  changes durable state and publishes a message.

Do not disguise a read-then-write race as a transaction. Use constraints,
conditional updates, version checks, locks, or atomic datastore operations that
actually preserve the invariant under concurrency.

## Define Ports At Real System Boundaries

Call an interface a **Port** only when it represents a real system or
nondeterministic boundary, including:

- database, cache, queue, blob store, or filesystem access;
- external HTTP, RPC, SDK, or process interaction;
- time, randomness, identifier generation, or process/runtime events.

Call internal pure helpers and deterministic collaborators directly. An
internal substitutable capability may still expose an interface and mock or
fake under the Core, but it is not a Port merely because it has an interface.

Keep each Port cohesive and narrow around the consuming business capability.
Do not expose vendor clients, ORM query builders, transport request types, or a
generic infrastructure facade through it.

## Let The Inner Consumer Own Each Port

The inner Domain or Application module that needs a capability owns the Port
contract. Define together in that owning module:

1. the canonical Port interface;
2. its stable input, result, and error semantics;
3. the standard mock, fake, or test builder needed by consumers.

The outer adapter supplies the production implementation. It does not redefine
the interface according to the database or vendor SDK it happens to wrap.

When multiple inner consumers need genuinely different views of one external
system, give them separate capability-shaped ports. Share one Port only when
the consumers depend on the same stable semantics, not merely the same vendor.

## Keep Models Inside Their Semantic Boundaries

Never let ORM rows, schema-generated records, database null wrappers, vendor
SDK objects, or wire serialization types escape their adapter or transport.
Map them at the owning boundary.

Domain and transport DTOs may be the same type when their fields, invariants,
lifecycles, and compatibility semantics are genuinely identical. Split them
when any of these differ, especially when:

- Domain hides internal state or enforces construction invariants;
- an API exposes only a selected or versioned representation;
- persisted data has storage-only fields or historical encoding;
- one representation must remain stable while another evolves.

Do not add mappers and duplicate types by ritual. Do not reuse a type across
boundaries merely to avoid an explicit semantic conversion.

Domain owns every business invariant exactly once. Use rich objects or
immutable data plus pure functions according to the language's idioms; preserve
the same single ownership either way.

## Shape Repositories Around Domain Resources

Define a repository around a Domain aggregate or cohesive resource, never
automatically around each database table. Its methods express business-needed
persistence operations and return Domain values or stable Port results.

When a write decision depends on existing aggregate state, load that state and
apply the transition through Domain behavior before persisting it. When an
invariant can be expressed completely by one constraint or conditional write,
prefer the atomic repository operation and map a rejected or zero-row write to
its stable Domain or Port failure. Do not add a read-before-write race merely to
construct an aggregate. For complex read-only views, define a separate Query or
Read Port that may return a purpose-built DTO without constructing an aggregate
that will not enforce behavior.

A generic CRUD implementation may exist only as private infrastructure reuse.
Use it to remove mechanical adapter duplication while keeping all of these out
of the business contract:

- generic CRUD interfaces;
- ORM models and query builders;
- table-oriented filters, sort syntax, or pagination internals;
- datastore-specific options or transactions.

Every Use Case depends on its domain-specific narrow repository or Query Port.
Add non-generic adapter operations when the domain capability cannot be
expressed safely through the private CRUD mechanism.

Make cursor pagination use a stable total order. When the primary sort field is
not unique, add a unique tiebreaker such as the resource ID to the ordering,
cursor, and seek predicate. Keep cursor encoding opaque and Adapter-owned; a
cursor over only a non-unique timestamp can silently skip or repeat rows.

## Translate Dependency Failures Into Stable Errors

Each Port defines the complete stable failure taxonomy its inner consumers can
act on. Use programmatically identifiable categories such as not found,
conflict, unavailable, timeout, or invalid provider response only when those
meanings are part of the Port contract.

The adapter must:

- map database, SDK, protocol, and runtime failures into that taxonomy;
- preserve the original cause for diagnostics;
- distinguish retryable from permanent failure according to the operation;
- avoid leaking provider error classes, status codes, or message text inward.

The Use Case handles only failures for which it owns meaningful business,
retry, or consistency behavior and returns the rest. The Transport maps stable
Domain, Use Case, and Port failures to its protocol. It must never import an
adapter error type or parse an adapter message.

Delete a declared error category that no adapter can produce or no consumer can
handle. Keep the taxonomy finite and verify production plus handling coverage
through the testing reference.

## Keep Caching Semantically Transparent

Implement a cache as an adapter or decorator when it preserves the Port's
observable semantics. The cache owns keys, encoding, expiration mechanics,
stampede control, and cache-provider errors without leaking them inward.

Stale reads, partial data, fail-open behavior, or degraded responses change
product semantics. Model them explicitly in the Use Case or product contract,
including their validity window, recovery condition, tests, and observability.
Never introduce them as an adapter's silent fallback.

Keep invalidation ownership aligned with the business write. Prove concurrent
miss, stale entry, write/invalidate ordering, and outage behavior when those
risks exist.

## Model Queues And Long-Running Work Explicitly

Treat queue publication as a Port and the queue consumer as a Transport. The
consumer establishes the execution boundary, validates and normalizes the
message, invokes application behavior, and lets boundary policy acknowledge,
retry, reject, or archive the result.

Every durable task message has:

- a stable message identifier and version;
- correlation or Trace identity;
- an idempotency or deduplication identity;
- explicit payload semantics independent from queue SDK types.

Assume at-least-once delivery unless stronger semantics are proved. Make every
consumer idempotent, bound retries with backoff and jitter, distinguish
retryable from permanent errors, and define poison-message or dead-letter
handling. Do not acknowledge failed work as success.

Use an outbox when a committed database change and message publication must not
diverge. For long-running work, persist an explicit lifecycle including queued,
running, succeeded, failed, cancelled, or timed-out states as applicable.
Define progress, deadlines, cancellation, retry limits, and failure archive or
repair behavior instead of hiding them in an in-memory task.

## Separate Domain Events From Integration Events

A Domain Event is an internal business fact. Keep it in Domain vocabulary and
free from broker names, serialization annotations, delivery metadata, and
external compatibility concerns.

An Integration Event is a versioned public message contract. Map Domain Events
to Integration Events at the application commit boundary, persist them through
the outbox when consistency requires it, and publish only committed facts.

Consumers must be idempotent and tolerate delivery repetition. Evolve
Integration Events through the supported protocol-version policy; do not force
Domain types to retain obsolete wire fields for compatibility.

## Own The Complete Service Lifecycle

At startup:

- read, parse, and validate configuration once;
- construct the dependency graph in the Composition Root;
- validate every critical dependency required for readiness;
- register background workers, connection pools, servers, and cleanup owners;
- fail startup when required configuration or invariants are invalid.

Define liveness as whether the process can make progress. Define readiness as
whether the instance may receive its intended traffic or work. Do not make
liveness depend on every transient external dependency and create restart
storms.

At shutdown:

1. mark the instance unready and stop accepting new requests or tasks;
2. cancel or drain in-flight work within an explicit deadline;
3. flush owned telemetry and durable work according to their guarantees;
4. close workers, pools, servers, and other resources in a defined order;
5. terminate with failure when safe shutdown cannot preserve required
   invariants.

For an optional dependency, define at design time whether its absence prevents
readiness, fails only the affected operation, or enables an explicit degraded
product mode. Do not discover that policy through an accidental catch block.

## Verify Observability As Behavior

Integration-test the observability contract instead of assuming middleware and
instrumentation are wired correctly. Prove that:

- exactly one structured completion log represents each request or task attempt;
- a long-running task has one additional start event only when its declared
  observability profile requires that progress signal;
- synchronous and asynchronous work retain their correlation or Trace link;
- incoming Trace context is extracted when the protocol supplies it, a new root
  Trace is created for scheduled or parentless execution, and context is
  injected when the boundary invokes a traced downstream dependency;
- stable log fields carry route or task identity, outcome, duration, principal
  context where allowed, and error classification;
- ordinary logs omit secrets, credentials, and bodies;
- unexpected failures retain cause and stack at the execution boundary.

Assert stable structured fields and propagation behavior, not prose wording,
timestamps, or incidental formatting. Keep audit-event verification separate
from diagnostic logging while proving that both share the required identity
and Trace context.

## Enforce Architecture Mechanically

Encode the inward dependency rules in CI using the strongest native mechanism
available: compiler/package visibility, module boundaries, import rules,
dependency graph analysis, static analysis, or a combination.

At minimum, fail the build when:

- Domain imports Transport, Infrastructure, framework, ORM, or vendor modules;
- Application imports a concrete adapter or transport;
- a Transport imports adapter-specific errors or datastore types;
- an adapter leaks ORM, SDK, or wire types through an inward Port;
- composition or container lookup occurs outside the Composition Root;
- dependency cycles cross business-module boundaries.

Do not rely on code review or a documented directory diagram as the only
enforcement. A generic reference fixes roles and direction; a stack-specific
reference may fix exact directories and tool configuration.

## Apply The Backend Completion Gate

Reject completion when any of the following is true:

- a business rule depends on framework, storage, queue, or vendor types;
- dependency injection is hidden behind globals, service lookup, or a broad
  application-wide dependency bag;
- a pass-through layer exists only to imitate Clean Architecture;
- a Handler or Consumer coordinates a business transaction;
- an adapter owns the inward Port contract or leaks its provider errors;
- ORM rows, schema records, SDK objects, or wire types escape their boundary;
- a public generic CRUD contract replaces a domain-specific repository or
  Query Port;
- a cache silently changes correctness or availability semantics;
- a durable consumer is not idempotent under duplicate delivery;
- a database commit and required event publication can diverge without an
  explicit consistency design;
- Domain and Integration Events are coupled as one wire-shaped type;
- startup, readiness, draining, or shutdown ownership is undefined;
- observability propagation and redaction lack integration proof;
- dependency direction is documented but not mechanically enforced.
