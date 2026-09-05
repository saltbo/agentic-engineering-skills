# OpenAPI And Contract Evolution

Scope: apply BEP design preferences directly to new APIs. In an existing API,
preserve established supported conventions, including version placement, naming,
and representation shapes. Do not require migration or deprecation merely for
style conformity. The checks below apply to the changed contract and selected
profile; security, protocol correctness, and supported behavior remain required.

Use this reference while publishing, reviewing, or changing the machine-readable
API contract.

## Contents

- [Select The OpenAPI Version Deliberately](#select-the-openapi-version-deliberately)
- [Enforce A Resource-Only Contract](#enforce-a-resource-only-contract)
- [Encode The Contract Profile](#encode-the-contract-profile)
- [Design Schemas For Intent](#design-schemas-for-intent)
- [Evaluate Compatibility](#evaluate-compatibility)
- [Version And Deprecate](#version-and-deprecate)
- [Contract-First Verification](#contract-first-verification)
- [Primary Specification](#primary-specification)

## Select The OpenAPI Version Deliberately

Use the newest OpenAPI feature set supported by all required validators,
generators, gateways, documentation renderers, client tooling, and runtimes.
The latest published specification is not automatically the correct project
target. Preserve the repository's current version unless the task includes a
tested migration.

## Enforce A Resource-Only Contract

Reject the OpenAPI description before schema review when any operation lacks a
proven addressed resource. For every path and operation, verify:

- every literal path segment is a resource noun or non-action infrastructure
  prefix, never a business verb;
- no RPC `:verb` suffix exists;
- no query parameter or request property named `action`, `command`, `operation`,
  or equivalent selects business behavior;
- `POST` creates and returns or locates a member of the addressed collection;
- `PUT`, `PATCH`, and `DELETE` operate on the addressed resource itself;
- no client-written `status` value serves as a disguised business command;
- the `operationId` uses a resource operation such as `createApproval`, not a
  business command such as `approveRequest`;
- request and response schemas describe the resource transition rather than a
  generic command envelope.

For new BEP contracts, use this resource-only gate. For an existing API, extend
its supported conventions consistently. Record preference differences only when
relevant; do not require resource replacement or deprecation unless the requested
work includes that migration.

At minimum, declare and verify:

- `openapi`, `info`, and applicable `servers`;
- every path, method, stable unique `operationId`, and tag;
- all parameters with location, requiredness, style, and schema;
- request body media types, schemas, and requiredness;
- every success and expected failure response, including headers and content;
- reusable schemas, parameters, responses, headers, examples, and security
  schemes under `components`;
- exact operation-level security requirements and OAuth scopes;
- representative examples that validate against their schemas.

Do not hide protocol behavior only in prose. If a behavior affects a client's
request, response, retry, authentication, or parsing logic, encode it in the
contract where OpenAPI can express it and document the remainder beside the
operation.

## Encode The Contract Profile

- If the project does not version its API, do not add a version selector merely
  because an API exists.
- When versioning is required, keep resource URIs version-free and use one
  project-wide `API-Version` request header with full-date `YYYY-MM-DD` values.
  Do not put the version in a path, hostname, query parameter, or media type.
- Encode the header's actual requiredness in OpenAPI. Mark it required only when
  the server intentionally rejects requests without an explicit version;
  otherwise document the default and supported dates.
- Echo the selected version when the contract promises that signal and include
  `API-Version` in `Vary` on cacheable responses.
- Use stable `listUsers`, `getUser`, `createUser`, `replaceUser`, `updateUser`,
  and `deleteUser` style `operationId` values. Use resource operation words even
  when the product requirement is phrased as a command.
- Give each operation exactly one primary tag for the resource's owning domain
  group. Do not derive tags from teams, controllers, services, or UI modules.
- Define single-resource success schemas directly. Do not wrap them in `data`.
- Define every collection as an object with `items` and `pagination`. Describe
  the RFC 8288 `Link` response header separately; do not add body pagination
  links.
- Declare exactly one reusable page or cursor pagination profile for the
  project. Do not attach different pagination parameter families to different
  operations.
- Enumerate `include` and `view` values per operation. Do not accept arbitrary
  relationship paths or field masks.
- Define resource relationship URLs under `links` as absolute URI strings.
- Define `application/problem+json` for every expected non-success response and
  reuse problem components only when their semantics are identical.
- Define authentication schemes separately from authorization policy. Apply
  operation security requirements and scopes, then document that resource-level
  authorization remains an independent runtime decision.
- Declare `ETag`, `If-Match`, `If-None-Match`, `Idempotency-Key`, `Location`,
  `Link`, `Preference-Applied`, `Retry-After`, `Request-Id`, and `API-Version`
  wherever the operation semantics require them. Return `Request-Id` on every
  response.
- Describe optional W3C `traceparent` and `tracestate` request headers when they
  are part of the public API boundary, while implementing their propagation in
  framework instrumentation.

## Design Schemas For Intent

- Separate create, replace, patch, and response schemas when their allowed
  fields differ.
- Define Merge Patch under `application/merge-patch+json`. Add JSON Patch under
  `application/json-patch+json` only for operations that require it; never
  describe PATCH with generic `application/json`.
- Mark required fields according to wire requirements, not implementation type
  convenience.
- Distinguish nullable values from optional properties.
- Constrain strings, numbers, arrays, identifiers, formats, and enums only as
  strictly as the service guarantees.
- Avoid closed enums when servers may add values and clients must remain
  forward-compatible; document unknown-value behavior.
- Use discriminated unions only when variants are stable and exclusive.
- Keep examples realistic and schema-valid. Do not use examples to define
  behavior absent from the schema or operation.
- Reuse a component only when semantics, validation, and evolution policy are
  identical. Shape similarity alone is insufficient.

## Evaluate Compatibility

Treat compatibility from the consumer's perspective. Run a semantic OpenAPI
diff when an existing contract changes, then inspect findings manually.

Usually breaking:

- removing or renaming a path, operation, parameter, property, response, or
  security option;
- changing a method, parameter location, media type, or status semantics;
- making an optional input required;
- narrowing accepted input or widening a response beyond what generated clients
  can decode;
- changing identifier, pagination-token, error-code, or idempotency behavior;
- tightening authorization without an announced policy migration.

Often additive but still consumer-sensitive:

- adding optional response properties;
- adding enum values or polymorphic variants;
- adding optional parameters, new operations, or new error responses;
- increasing precision, size, ordering, or consistency guarantees;
- changing defaults, rate limits, or cache policy.

Do not label a change safe solely because the OpenAPI diff tool does. Generated
clients, strict decoders, stored representations, webhooks, caches, and human
workflows may impose additional constraints.

## Version And Deprecate

Prefer additive evolution within a stable API version. Introduce a new version
only for a coherent set of incompatible changes, not every feature.

When a breaking change is authorized:

1. identify affected operations and consumers;
2. publish the replacement contract and migration mapping;
3. define coexistence, rollout, telemetry, and rollback;
4. mark deprecated operations and fields in OpenAPI;
5. communicate a support and sunset timeline through the project's established
   channel and protocol headers when applicable;
6. remove old behavior only after the compatibility commitment is satisfied.

For a new BEP API, keep resource URIs version-free. For an existing API, keep
its established version scheme, including path versions for new operations in
that API. Do not introduce date headers or a migration solely to satisfy BEP.
When a version-policy migration is explicitly in scope, publish its supported
versions, defaults, coexistence, deprecation, and rejection behavior.

When a project explicitly selects date-based header versioning, `API-Version:
YYYY-MM-DD` is a reasonable profile. It is a project-defined field, not an IETF
standard. Define whether it is required, whether a default exists, which dates
are supported, what the response echoes, and how caches vary. Do not prefix a
new field with `X-`.

## Contract-First Verification

Run the narrowest available checks:

1. parse and validate the OpenAPI document with the project's validator;
2. lint naming, operation identifiers, errors, security, and examples;
3. run a semantic diff against the published baseline;
4. validate examples and generated fixtures against schemas;
5. run contract tests against the implementation;
6. generate at least one representative client when code generation is a
   supported consumer;
7. verify documentation renders without losing required semantics.

Record the tool versions and commands. A valid OpenAPI file can still describe
the wrong runtime behavior; contract tests and representative HTTP exchanges
must close that gap.

## Primary Specification

- [Latest published OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [Fielding: REST Architectural Style](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
- [Google AIP-121: Resource-oriented design](https://google.aip.dev/121)
- [Google AIP-136: Custom methods rejected by this skill](https://google.aip.dev/136)
- [Google AIP-158: Pagination](https://google.aip.dev/158)
- [GitHub REST API versioning](https://docs.github.com/en/rest/about-the-rest-api/api-versions)
- [GitHub REST API pagination](https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api)
