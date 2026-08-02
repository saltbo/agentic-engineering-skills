# Framework Integration

Use this reference whenever implementing or evolving an API in an existing
project. Apply the contract through the project's web framework instead of
repeating protocol logic in handlers.

## Contents

- [Inspect Before Designing](#inspect-before-designing)
- [Build One Contract Layer](#build-one-contract-layer)
- [Use Framework-Native Extension Points](#use-framework-native-extension-points)
- [Centralize OpenAPI](#centralize-openapi)
- [Migrate Without Duplicating Policy](#migrate-without-duplicating-policy)
- [Verify The Framework Boundary](#verify-the-framework-boundary)
- [Review Gate](#review-gate)

## Inspect Before Designing

Before editing an endpoint, identify:

- the web framework, router, serializer, validator, and dependency-injection
  model;
- existing middleware, filters, interceptors, exception mappers, base handlers,
  and response types;
- OpenAPI generation, linting, code generation, and contract-test tooling;
- authentication context, authorization hooks, request context, logging,
  metrics, and tracing instrumentation;
- existing error, pagination, versioning, idempotency, ETag, retry, and header
  conventions;
- published compatibility commitments and active clients.

Classify each existing convention as compliant, incompatible, or missing.
Preserve compliant framework mechanisms. Replace or migrate incompatible policy;
do not build a second parallel convention for new endpoints.

## Build One Contract Layer

Provide one framework-level implementation for each cross-cutting concern:

| Concern | Framework responsibility |
| --- | --- |
| API version | Parse required `API-Version`, select the date contract, echo a successfully selected value, set `Vary`, reject invalid values |
| Errors | Map validation, authentication, authorization, conflicts, preconditions, rate limits, and unexpected failures to RFC 9457 |
| Pagination | Parse the selected project profile, enforce bounds, serialize `pagination`, and build the RFC 8288 `Link` header |
| Filtering and sorting | Validate declared fields, types, grammar, cost limits, and `orderBy` tie-breakers |
| Representations | Apply named `view`, enumerated `include`, omission/null rules, and relationship links |
| Concurrency | Generate `ETag`, require and evaluate `If-Match` or `If-None-Match` |
| Idempotency | Validate keys, fingerprint requests, store outcomes, replay responses, and detect conflicting reuse |
| Correlation | Generate `Request-Id`, manage request context, extract/inject W3C Trace Context, and enrich logs |
| Shared headers | Apply `Location`, `Link`, `Retry-After`, `Preference-Applied`, cache, security, and version headers |
| Authentication | Validate credentials and produce one normalized immutable principal without making permission decisions |
| Authorization | Consume the principal, resolve the addressed resource, and enforce resource-level policy consistently |

Handlers should receive validated domain-oriented input and return a resource or
domain result. They must not construct protocol error bodies, parse pagination,
negotiate versions, generate correlation identifiers, or reproduce shared
headers. They must not parse credentials or implement role, group, or scope
branches in place of the authorization policy boundary.

## Use Framework-Native Extension Points

Prefer the framework's native middleware, filters, interceptors, validators,
serializers, exception mapping, request-scoped context, and OpenAPI hooks. Add a
dependency only when it removes real complexity and conforms to the existing
stack.

Keep the shared layer narrow and explicit. Do not create a custom framework or a
generic repository/service hierarchy merely to centralize behavior. Centralize
wire protocol policy; keep domain rules in the owning domain.

Ensure middleware ordering is intentional. At minimum, correlation and tracing
must surround authentication, version selection, validation, routing, and error
mapping so every response, including an early failure, has the required
correlation and contract headers. Authentication must establish the principal
before authorization. Authorization must run after the framework knows the
resource operation and before a handler mutates state.

## Centralize OpenAPI

- Define reusable parameters, headers, responses, pagination schemas, Problem
  Details schemas, security schemes, and examples under `components`.
- Generate operation declarations from the same framework policy where the
  toolchain supports it; otherwise lint every operation for the shared refs.
- Keep `operationId`, resource tags, security, status codes, and media types
  explicit at the operation boundary.
- Run a semantic OpenAPI diff against the published baseline.
- Prevent runtime middleware and OpenAPI components from defining different
  defaults, limits, headers, or error shapes.

## Migrate Without Duplicating Policy

When the project lacks a shared contract layer, create the smallest
framework-native layer before implementing the requested endpoint. Move every
touched endpoint onto it. Do not leave copied helper logic in handlers.

When existing public endpoints are incompatible, design one canonical policy,
document the deviations, and use the selected API-version boundary or an
explicit migration to converge. Do not silently change published behavior and
do not preserve incompatible behavior as the template for new code.

If the task is limited in scope, report untouched deviations and the migration
boundary. If the task authorizes project-wide unification, migrate all endpoints
and remove dead parallel helpers.

## Verify The Framework Boundary

Write focused tests proving the shared layer once and representative contract
tests proving endpoints use it:

- missing, malformed, supported, and unsupported `API-Version`;
- malformed input and field validation as Problem Details;
- required and stale preconditions;
- idempotent replay and conflicting key reuse;
- page or cursor parsing, body metadata, terminal pages, and `Link` consistency;
- filter and ordering validation;
- `Request-Id` on success and every failure path;
- incoming and outgoing W3C Trace Context propagation;
- authentication failures and normalized principal creation independently from
  authorization allow/deny, resource, tenant, and concealment decisions;
- OpenAPI reusable components and runtime response agreement.

Use the project's narrowest meaningful test commands. Test middleware ordering
through an early failure such as authentication or malformed input.

## Review Gate

Reject an implementation when:

- handlers construct Problem Details, pagination, version, correlation, or
  conditional-request behavior themselves;
- multiple pagination or error helpers encode competing rules;
- runtime defaults differ from OpenAPI;
- framework-native hooks exist but endpoint-local code bypasses them;
- tracing is manually propagated in business code;
- authentication and authorization are combined, or handlers parse credentials
  and make scattered role, group, or scope decisions;
- a refactor adds a generic framework abstraction without reducing protocol
  duplication;
- touched endpoints remain on copied legacy policy without an explicit
  compatibility reason.
