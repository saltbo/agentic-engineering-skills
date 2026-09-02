# Resource Modeling

Use this reference while discovering resources, canonical URIs, representations,
and state transitions. Do not design an API operation until every addressed
resource passes this gate.

## Contents

- [Resource-Abstraction Gate](#resource-abstraction-gate)
- [Define Identity And Ownership](#define-identity-and-ownership)
- [Design URI Space](#design-uri-space)
- [Model State Transitions](#model-state-transitions)
- [Shape Representations](#shape-representations)
- [Map Capabilities After Modeling](#map-capabilities-after-modeling)
- [Review Gate](#review-gate)

## Resource-Abstraction Gate

Reject a candidate resource unless all questions have convincing answers:

1. What domain concept does it represent without referring to a UI surface?
2. What gives one instance stable identity?
3. Who owns it, and within which authorization boundary does it exist?
4. What client-visible state and relationships does it expose?
5. What creates it, changes it, and ends or deletes it?
6. What is its single canonical URI?
7. Why is it not an existing resource, a projection, or client composition?

Do not derive the API surface from navigation, screens, tabs, cards, forms,
buttons, business operations, named product features, controller methods,
service methods, or tables. Those are evidence for discovering the model, not
the model itself.

A resource need not map one-to-one to persisted storage. Derived, aggregate,
policy, request, job, attempt, and result resources are valid when they are
stable domain concepts with identity, representation, lifecycle, consistency,
freshness, and authorization semantics. A response assembled solely to fill
one screen is not a resource.

Names such as `overview`, `management`, `configuration`, `action`, and `retry`
often hide a UI-shaped aggregate or procedure. A noun in a path does not prove
that the thing is a resource.

## Define Identity And Ownership

- Use opaque, stable identifiers. Do not expose mutable names as identity.
- Keep identifiers unique within a documented scope.
- Do not encode attributes that can change or disclose sensitive information.
- Give a resource one canonical URI within a caller boundary.
- Use the same canonical URI for principals with different permissions. Express
  authority through security requirements and authorization checks.
- Treat aliases as redirects or documented alternate identifiers, not competing
  canonical resources.

## Design URI Space

- Use lowercase kebab-case nouns and plural collection names consistently:
  `/audit-logs`, never `/auditLogs`, `/AuditLogs`, or `/audit_logs`.
- Keep paths predictable and avoid implementation vocabulary such as
  `controllers`, `tables`, or service class names.
- Nest a resource only when it cannot exist outside its parent and its identity
  is scoped by that parent. A business relationship alone never justifies
  nesting.
- Use a top-level canonical URI when a child has an independent lifecycle, can
  move between parents, or is referenced from several parents.
- Put resource identity in paths. Put optional filtering, sorting, projection,
  and pagination controls in queries.
- Require every filter to reference declared resource state or a proven
  projection. A query parameter must not hide an unmodeled business decision.
- Keep the canonical URI free of API versions. When the project versions the
  contract, use its `API-Version` header policy; when it does not, do not
  introduce versioning during resource modeling.
- Do not put authorization roles or client types in paths.
- Never put verbs such as `create`, `update`, `delete`, `activate`, `approve`,
  `cancel`, `publish`, `generate`, `execute`, or `retry` in resource URIs.
- Never use RPC suffixes such as `:approve`, `:cancel`, or `:publish`.
- Never move a path action into `?action=...`, `?command=...`, or a request body
  discriminator. That preserves the RPC contract while hiding its name.
- Never use generic pseudo-resources such as `actions` or `commands` to carry a
  business verb in the request body.
- Use HTTP methods as the only operation verbs.

Audit every literal path segment. Reject the operation if a segment names a
behavior rather than an addressable resource. A noun-shaped word passes only
when the resource-abstraction gate proves its semantics.

## Model State Transitions

Before accepting an action-shaped requirement, ask what resource is created,
replaced, updated, or deleted:

| Requirement | Resource interpretation |
| --- | --- |
| Start asynchronous work | Create a job in a job collection |
| Retry failed work | Create another attempt or job that references the failure |
| Approve a request | Create or replace an approval resource |
| Revoke an active grant | Delete the grant, or create a revocation when it has its own lifecycle |
| Replace complete settings | Replace a singleton settings or policy resource |
| Rotate a credential | Create a new credential and retire the prior credential |
| Publish a draft | Create or replace a release/publication resource |
| Reserve capacity | Create a reservation resource with expiry |

Preserve historical resources when auditability matters. For example, create a
new retry attempt instead of rewriting a failed attempt.

Do not expose a business transition by accepting an action name or an arbitrary
target `status` in a generic update. When the transition itself has identity,
state, timing, authorization, retries, or audit value, model it as a resource.
When it does not, express the resulting state through a legitimate update to the
addressed resource only if that state is genuinely part of the client-writable
representation.

If no candidate passes the abstraction gate, stop with `RESOURCE MODEL
INCOMPLETE`. State which identity, ownership, representation, lifecycle, or
canonical-URI decision is missing. Do not create a command endpoint.

## Shape Representations

- Separate create, replace, patch, and response schemas when writable,
  immutable, server-managed, secret, or computed fields differ.
- Return one resource directly. Never wrap it in a generic `data` envelope.
- Return stable identifiers and absolute resource relationship URLs under
  `links`. Do not require clients to invent or resolve undocumented URI
  templates.
- Keep collection pagination metadata outside `links`; use the collection shape
  defined in the HTTP contract reference.
- Permit relationship embedding only through `include` values enumerated by the
  operation's OpenAPI schema. Keep the corresponding relationship URL in
  `links` when a related representation is embedded.
- Use a small OpenAPI-enumerated `view` parameter for supported named
  representations. Do not accept arbitrary sparse-field masks.
- Return secret material only at the creation boundary when later reads must not
  expose it.
- Make timestamps, time zones, money, units, enums, nullable fields, and absent
  fields unambiguous.
- Omit properties that are not supplied, unavailable, unauthorized, or not
  applicable. Return `null` only when null is an explicit domain value.
- Distinguish omitted values from explicit clearing in update contracts. With
  JSON Merge Patch, document every nullable property carefully because `null`
  removes a member under the patch format.
- Avoid polymorphic envelopes unless variants have real domain identity and a
  stable discriminator.
- Keep representations focused on the resource. Link or embed related resources
  according to latency, consistency, payload, and authorization constraints.

## Map Capabilities After Modeling

Build a capability matrix only after the resource inventory exists:

| Product capability | Resource reads | Resource transitions | Notes |
| --- | --- | --- | --- |
| Example capability | `GET /resources/{id}` | `POST /resources/{id}/jobs` | Explain composition |

Several capabilities may use the same resource. One capability may compose
several ordinary requests. Do not force one endpoint per capability or one
capability per endpoint.

## Review Gate

Reject the model when:

- an operation exists only because a page, button, or business verb exists;
- a path contains a business verb, RPC suffix, or command carrier;
- an `operationId` names a business command instead of a resource operation;
- `POST` invokes behavior instead of creating a collection member;
- a patchable `status` or `action` field disguises a domain command;
- two URIs represent the same resource for different callers;
- a child is nested despite independent identity and lifecycle;
- an aggregate has no stable meaning, freshness, or authorization contract;
- a persistence record leaks through a more stable domain abstraction;
- the same collection creates unrelated resource types;
- a transition mutates historical evidence that should remain auditable;
- clients must guess resource URIs or undocumented state machines.
