---
name: best-openapi-design
description: Design, review, implement, and enforce strictly resource-oriented RESTful HTTP APIs and OpenAPI contracts. Use whenever deciding whether a concept is a field, value object, or resource; assigning resources to domain groups; defining or changing routes, canonical URIs, methods, representations, pagination, errors, authentication, authorization, request and trace correlation, idempotency, concurrency, versioning, compatibility, or framework-level API infrastructure. Prevent business-action APIs, verb or RPC-style paths, command endpoints, UI- or database-shaped contracts, arbitrary resource placement, endpoint-local protocol logic, and mixed authentication/authorization concerns. Require every operation to address a proven resource through standard HTTP semantics, and stop when no valid resource model or owning domain exists.
---

# Best OpenAPI Design

Treat an HTTP API as a long-lived resource protocol. Discover stable domain
resources before defining routes, then preserve HTTP semantics through the
OpenAPI contract, implementation, and verification.

## Apply Authority In Order

Resolve design questions in this order:

1. obey applicable IETF HTTP RFC requirements;
2. preserve Fielding REST constraints, especially resource identification,
   representations, self-descriptive messages, and the uniform interface;
3. preserve compatible published contracts and explicit project-level policy;
4. apply this skill's baseline profile where the project has no conflicting
   requirement or established convention.

Treat Google AIP, GitHub REST, and other mature APIs as evidence, not authority.
Do not copy RPC transcoding, protobuf conventions, legacy pagination, custom
error envelopes, or compatibility baggage. The absolute ban on action-oriented
paths is an intentionally stricter policy than the URI grammar required by HTTP
or REST.

## Non-Negotiable Rule: Expose Resources Only

Never translate business logic, a use case, workflow step, screen, button,
controller method, service method, or domain command directly into an API
operation. Business behavior belongs behind resource creation, retrieval,
replacement, partial update, or deletion. The API surface exposes the resources
and their representations, never the business action itself.

Allow only resource nouns, stable identifiers, and non-action infrastructure
prefixes in paths. Never place a business verb or command in a path segment,
RPC suffix, query parameter, or body discriminator:

```text
Reject: POST /orders/{orderId}/cancel
Reject: POST /users/{userId}/activate
Reject: POST /exports/{exportId}/retry
Reject: POST /reports/generate
Reject: POST /documents/{documentId}:publish
Reject: POST /orders/{orderId}?action=cancel
Reject: POST /orders/{orderId} {"action": "cancel"}

Model:  POST /orders/{orderId}/cancellation-requests
Model:  PUT  /users/{userId}/activation
Model:  POST /export-jobs with a sourceJob reference
Model:  POST /report-jobs or POST /reports
Model:  PUT  /documents/{documentId}/publication
```

The replacement noun must represent a real resource. Renaming `cancel` to
`cancellation`, `approve` to `approval`, or `retry` to `attempt` is insufficient
unless the candidate has domain meaning, identity, ownership, representation,
lifecycle, and one canonical URI.

Fail closed. If any requested capability cannot be expressed through a proven
resource model, stop and report the missing domain decision. Do not emit paths,
an OpenAPI operation, or implementation code for that capability. Never fall
back to a command-style endpoint.

## Apply The Core Rules

- Model domain resources, not business operations, screens, forms, buttons,
  controller methods, service methods, or database tables.
- Give each resource one canonical URI within a caller and authorization
  boundary.
- Use HTTP methods as the only operation verbs. Keep paths resource-only.
- Use standard HTTP methods according to their safety and idempotency
  semantics.
- Make representations, errors, retries, concurrency, authorization, and
  compatibility explicit.
- Follow repository conventions only when they preserve resource orientation
  and HTTP semantics. Reject and report conflicting action-oriented conventions.
- Preserve existing public contracts unless the task authorizes a breaking
  change and provides a migration path.

## Apply The Baseline Contract Profile

Use these rules where the project has no compatible established convention:

- name plural collection path segments in lowercase kebab-case;
- name query parameters and JSON properties in lowerCamelCase;
- keep resource URIs version-free; when API versioning is needed, use
  `API-Version: YYYY-MM-DD`, with requiredness and default behavior selected at
  the project level rather than imposed on every API;
- return a single resource directly, never inside a generic `data` envelope;
- return collections as `items` plus `pagination`, never body pagination links;
- put pagination navigation URLs in the RFC 8288 `Link` response header;
- expose resource relationships as absolute URLs under `links`, independently
  of collection pagination;
- permit embedding only through OpenAPI-enumerated `include` values;
- use OpenAPI-enumerated named `view` values instead of arbitrary field masks;
- distinguish an omitted property from a domain value of `null`;
- use `orderBy=field desc,otherField asc` for multi-field sorting;
- use `listResources`, `getResource`, `createResource`, `replaceResource`,
  `updateResource`, and `deleteResource` style `operationId` values;
- use RFC 9457 Problem Details and the validation extension defined in the HTTP
  contract reference;
- return one server-generated `Request-Id` per HTTP request and propagate W3C
  `traceparent` and `tracestate` through framework instrumentation;
- separate authentication from authorization: authentication produces a
  validated principal; authorization evaluates that principal against the
  addressed resource and resource operation;
- require conditional writes for mutable existing resources;
- prefer idempotent `PUT` creation when the client controls the URI; for `POST`
  creation, decide whether `Idempotency-Key` is required from the operation's
  retry, duplicate-effect, and unknown-outcome risks;
- model long-running work as a domain-specific job or request resource, never a
  generic `/operations` collection.

Choose exactly one pagination profile for the project and apply it to every
growing collection:

- **page profile:** `page` and `pageSize`; return exact `page`, `pageSize`,
  `totalItems`, and `totalPages` values;
- **cursor profile:** `pageSize` and opaque `pageToken`; return `pageSize` and an
  optional `nextPageToken`, use snapshot traversal, and never return a total.

Never choose a pagination profile from one endpoint in isolation. Inspect the
project's callers, data scale, mutation rate, navigation needs, and existing
contract. When no project-level decision or sufficient evidence exists, report
`PAGINATION PROFILE INCOMPLETE` and stop before defining collection parameters
or response metadata.

Default to individually declared, strongly typed filter parameters. Enable a
single `filter` expression only when compound predicates are required. In that
case, require the project to publish one complete grammar and type system for
the whole API. Every filter must reference a declared resource property or a
proven, documented projection. Do not translate a business predicate such as
`isEligibleForRenewal()` into `eligibleForRenewal=true` unless renewal
eligibility is first modeled as stable resource state. Otherwise apply the
field-versus-resource gate and report `RESOURCE MODEL INCOMPLETE`. Never
improvise endpoint-specific filter syntax.

## Step 1: Establish The Design Boundary

Read repository instructions, existing routes, OpenAPI descriptions, schemas,
clients, tests, and API conventions before proposing a change. Determine:

- the callers and whether the API is public, partner, or internal;
- the authentication and authorization boundary;
- the affected existing operations and consumers;
- compatibility, latency, consistency, retention, and regulatory constraints;
- whether the task requests design, review, evolution, or implementation.

Treat product requirements as capabilities to compose, not endpoints to
transcribe. Extract domain nouns, ownership, state, lifecycle, and transitions;
ignore endpoint names suggested by requirements until the resource model passes
the mandatory gate.
When behavior-first or contract-first workflow exists, follow it before editing
implementation code.

## Step 2: Build The Resource Model

Read [references/resource-modeling.md](references/resource-modeling.md). Do not
design paths or methods until the resource inventory is coherent.
Read [references/resource-organization.md](references/resource-organization.md)
whenever adding a concept, field, resource, group, tag, namespace, or module.

For every candidate resource, record:

| Concern | Required answer |
| --- | --- |
| Meaning | What stable domain concept exists independently of this UI or workflow? |
| Identity | What identifies one instance over its lifetime? |
| Ownership | Who owns it and within which authorization boundary? |
| Domain group | Which stable business domain owns its vocabulary, invariants, and lifecycle? |
| Representation | Which client-visible state and links does it expose? |
| Lifecycle | What creates, changes, expires, archives, or deletes it? |
| Canonical URI | Where is it addressed exactly once? |
| Relationship | Why is it not an existing resource or client-side composition? |

Model transitions as creation, replacement, partial update, or deletion of a
resource. Use jobs, requests, attempts, approvals, grants, policies, results,
and other process resources only when they have stable identity and lifecycle.
Do not rescue an RPC by placing an arbitrary noun in its path.

Before adding a field, value object, or resource, apply the organization gate.
Keep a concept inside an existing representation only when it shares the
resource's identity, lifecycle, ownership, authorization, concurrency,
retention, and consistency boundary. Create a resource when the concept has an
independent identity or lifecycle, forms a collection, needs its own URI,
authorization, history, query, cache, concurrency, or retention policy, or can
be referenced independently.

Assign every resource to exactly one owning domain group. Group by stable domain
language and rule ownership, never by UI, current team, controller, database,
repository package, deployment service, or generic `common`/`misc` buckets.
Represent cross-group relationships with canonical resource URLs. Never publish
duplicate resource URIs merely to make a resource appear under two groups.

Produce a resource proof for every proposed path before proceeding. If a group
owner cannot be proven, mark the design `RESOURCE GROUP INCOMPLETE`. If any
other row lacks a required answer, mark it `RESOURCE MODEL INCOMPLETE`. List the
missing decisions and stop. Do not infer a route from the business capability.

Map every requested capability to one or more reads or state transitions after
the inventory is complete. Remove duplicate resources and unjustified
aggregates.

## Step 3: Define The HTTP Contract

Read [references/http-contract.md](references/http-contract.md). Define each
operation completely:
Read
[references/authentication-authorization.md](references/authentication-authorization.md)
for every protected operation or identity-related API.

- canonical path, method, and stable unique operation identifier;
- the `API-Version` header contract when versioning is used, including
  requiredness, defaults, supported dates, and response signaling;
- path, query, header, and cookie parameters;
- request and response media types and schemas;
- success statuses, headers, and response bodies;
- all expected client and server failures in one consistent error model;
- authentication, authorization scopes, and resource-level checks;
- distinct authentication failures and authorization denials;
- retry and idempotency behavior;
- optimistic concurrency and preconditions where writes can conflict;
- cacheability and validation behavior for reads;
- ordering, filtering, pagination, and consistency for collections;
- polling, cancellation, retention, and result discovery for asynchronous work.

Apply these mandatory operation rules:

- use `GET` only to retrieve a resource or collection;
- use `POST` only to create a member in the addressed collection;
- use `PUT` only to create or completely replace the resource at a known URI;
- use `PATCH` only to partially update the addressed representation;
- use `DELETE` only to remove the addressed resource or association;
- never use `PATCH {"status": ...}` as a disguised business command;
- use `application/merge-patch+json` by default and add
  `application/json-patch+json` only for required array or path operations;
- name `operationId` values after the resource operation, such as
  `createOrderCancellationRequest`, never the business command `cancelOrder`.

Audit every literal path segment before publishing. Classify it as a resource
noun, stable identifier placeholder, or proven stable domain/infrastructure
namespace. Reject the whole operation when a segment expresses behavior rather
than resource identity or durable namespace.

Run the deterministic explicit-violation check on every proposed path:

```bash
python scripts/check_resource_paths.py \
  /orders '/orders/{orderId}' \
  '/orders/{orderId}/cancellation-requests'
```

Treat any reported violation as a failed design. This check catches explicit
verbs, RPC suffixes, and command selectors; it does not prove that a noun-shaped
segment is a real resource. The resource proof remains mandatory.

## Step 4: Publish And Evolve OpenAPI

Read [references/openapi-evolution.md](references/openapi-evolution.md). Produce
or update an OpenAPI description that is the complete machine-readable
contract, not a partial documentation overlay.

Use the newest OpenAPI feature set supported by every required validator,
generator, gateway, documentation tool, and runtime. Do not upgrade the
project's OpenAPI version as an unrelated side effect.

Describe every operation exactly once, including stable `operationId` values,
security requirements, schemas, headers, errors, and useful examples. Reuse
components for concepts with identical semantics, not merely similar shapes.
Evaluate changes against existing clients and publish migration and deprecation
behavior for incompatible evolution.

Do not document or preserve an action-oriented route merely because it already
exists. When compatibility prevents immediate removal, mark it as a violation,
design the canonical resource-oriented replacement, and provide a deprecation
and migration plan. Do not add another action-oriented operation beside it.

## Step 5: Implement Or Review At The Contract Boundary

Read [references/framework-integration.md](references/framework-integration.md)
before implementing an API in an existing project.

When implementation is requested, keep validation and authorization at system
boundaries, centralize shared contract types, and preserve domain independence
from transport details. Update the contract and the narrowest meaningful tests
with the implementation.

Inspect the project's web framework and its native middleware, filters,
interceptors, exception mappers, validators, serializers, OpenAPI integration,
and observability hooks. Implement cross-cutting protocol rules once in that
framework layer. Never scatter version negotiation, Problem Details mapping,
pagination serialization, conditional requests, idempotency, request IDs, trace
propagation, or shared headers across endpoint handlers.
Keep authentication middleware and authorization policy enforcement as separate
components. Handlers consume a validated principal and authorized resource
context; they never parse credentials or treat authentication claims as an
authorization decision.

When review is requested, do not mutate code. Classify findings by contract
impact and cite the exact path, operation, schema, or behavior. Distinguish
standards violations from project-style preferences.

Use [references/dataset-export-example.md](references/dataset-export-example.md)
when an independent end-to-end example would clarify resource modeling,
asynchronous work, retries, concurrency, and results.
Use [references/canonical-http-examples.md](references/canonical-http-examples.md)
for the mandatory CRUD, pagination, filtering, concurrency, and error shapes.

## Step 6: Verify And Report

Run the repository's narrowest contract validation, schema diff, typecheck, and
tests that prove the design. When a deployed API is available, exercise
representative reads, writes, failures, retries, preconditions, and pagination
without mutating production data unless explicitly authorized.

Report:

1. `RESOURCE GATE: PASS|FAIL` with the completed resource proof;
2. `PATH VERB AUDIT: PASS|FAIL` for every literal path segment;
3. `RPC SHAPE AUDIT: PASS|FAIL` covering suffixes, query parameters, request
   bodies, status patches, and `operationId` values;
4. the boundary, assumptions, and compatibility constraints;
5. the resource inventory and canonical URIs;
6. the field-versus-resource decisions and domain-group placement proof;
7. the capability-to-resource mapping;
8. the method, path, status, error, retry, concurrency, and cache contract plus
   separate authentication and authorization contracts;
9. the OpenAPI artifact or exact proposed diff;
10. compatibility, migration, and deprecation decisions;
11. validation commands and results;
12. unresolved design decisions that require product or protocol ownership.

Treat any failed gate as a failed design. Do not continue to implementation and
do not describe the rejected operation as an acceptable alternative.

Reject the design until every operation is justified, every growing collection
is bounded, every write has defined conflict and retry behavior, every failure
uses the agreed error contract, and the OpenAPI description matches the actual
surface. Reject it immediately when any operation exposes business logic instead
of a resource or any path contains a business verb.
