# Backend Ownership

Apply BEP preferences to new architecture. In an existing project, improve the affected boundary within its conventions; do not require unrelated restructuring.

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

## Define Ports At Real System Boundaries

Call an interface a **Port** only when it represents a real system or
nondeterministic boundary, including:

- database, cache, queue, blob store, or filesystem access;
- external HTTP, RPC, SDK, or process interaction;
- time, randomness, identifier generation, or process/runtime events.

Call internal pure helpers and deterministic collaborators directly. An
internal substitutable capability may still expose an interface and mock or
fake, but it is not a Port merely because it has an interface.

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
handle. Keep the taxonomy finite and test meaningful production and handling behavior.
Use the backend verification profile only for formal inventory governance.
