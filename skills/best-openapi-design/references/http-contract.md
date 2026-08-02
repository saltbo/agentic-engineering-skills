# HTTP Contract

Use this reference after the resource model is coherent. Preserve standard HTTP
semantics so generic clients, caches, proxies, gateways, and operators can
understand the protocol.

## Contents

- [Methods](#methods)
- [Success Statuses](#success-statuses)
- [Client And Server Failures](#client-and-server-failures)
- [Conditional Requests And Concurrency](#conditional-requests-and-concurrency)
- [Retries And Idempotency](#retries-and-idempotency)
- [Collections](#collections)
- [Representations And Relationships](#representations-and-relationships)
- [Asynchronous Work](#asynchronous-work)
- [Request And Trace Correlation](#request-and-trace-correlation)
- [Caching And Content Negotiation](#caching-and-content-negotiation)
- [Authentication And Authorization](#authentication-and-authorization)
- [Standards](#standards)

## Methods

| Method | Use | Semantics |
| --- | --- | --- |
| `GET` | Read a representation or collection | Safe, idempotent, cacheable unless constrained |
| `HEAD` | Read the metadata a `GET` would return | Safe, idempotent, no response content |
| `POST` | Create a server-identified member in the addressed collection | Neither safe nor inherently idempotent; require `Idempotency-Key` |
| `PUT` | Create or completely replace the resource at a known URI | Idempotent |
| `PATCH` | Partially update a resource | Define patch media type and idempotency behavior |
| `DELETE` | Remove the association represented by the target URI | Idempotent intended effect |
| `OPTIONS` | Describe communication options when supported | Safe, idempotent |

Do not use `GET` for mutation. Do not describe a partial update as `PUT`.
Default `PATCH` to `application/merge-patch+json`. Add
`application/json-patch+json` only when the contract needs precise array-member
or path operations. Never use ambiguous `application/json` patch semantics.

When the client controls a stable identifier, create the known URI with
idempotent `PUT`. When the server assigns the identifier, create through `POST`
on the collection and require `Idempotency-Key`. A create-only `PUT` can use
`If-None-Match: *`; replacement of an existing resource requires `If-Match`.

Do not use any method to invoke a business command. `POST` does not grant an
escape hatch for RPC. It creates the resource represented by the target
collection. `PUT`, `PATCH`, and `DELETE` operate on the addressed resource; they
must not conceal an unrelated action.

## Success Statuses

| Status | Use |
| --- | --- |
| `200 OK` | Return a representation or result |
| `201 Created` | A resource exists now; return `Location` and usually its representation |
| `202 Accepted` | Processing was accepted but is incomplete; identify a monitor resource |
| `204 No Content` | The operation succeeded and intentionally returns no content |
| `206 Partial Content` | Serve a valid range response, not ordinary collection pagination |

Do not return `202` merely because the server performed background work if the
created job resource already exists and is the result of the request; creating
that job commonly returns `201`. Do not return `204` with response content.

Return the current resource representation by default for successful creation,
replacement, and update. Support RFC 7240 `Prefer: return=minimal` and
`Prefer: return=representation` where response-size control is useful, and emit
`Preference-Applied` when honoring it. A `201` response always identifies the
created resource with `Location`, even when its body is minimal.

## Client And Server Failures

Use status codes according to protocol semantics, then add domain detail in the
error representation:

| Status | Meaning |
| --- | --- |
| `400 Bad Request` | Malformed syntax, framing, encoding, or invalid protocol parameter |
| `401 Unauthorized` | Authentication is missing or invalid; include the required challenge when applicable |
| `403 Forbidden` | The authenticated principal lacks authority |
| `404 Not Found` | The resource is absent or deliberately concealed |
| `405 Method Not Allowed` | The resource exists but the method is unsupported; include `Allow` |
| `406 Not Acceptable` | No acceptable response representation is available |
| `409 Conflict` | The request conflicts with current resource state |
| `410 Gone` | The resource intentionally no longer exists and that fact is durable |
| `412 Precondition Failed` | A conditional request precondition failed |
| `415 Unsupported Media Type` | The request content type or encoding is unsupported |
| `422 Unprocessable Content` | Valid syntax violates domain constraints |
| `428 Precondition Required` | The server requires a conditional write |
| `429 Too Many Requests` | A rate limit was exceeded; provide retry metadata when known |
| `500 Internal Server Error` | An unexpected server failure occurred |
| `502` / `503` / `504` | An upstream or availability boundary failed with the corresponding semantics |

Adopt RFC 9457 Problem Details (`application/problem+json`).
Use a stable problem `type` URI as machine identity. Keep `title` stable for the
type, make `detail` occurrence-specific and human-readable, and add typed
extensions for fields clients must process. Never require clients to parse
human prose. Do not expose stack traces, secrets, internal identifiers, or
authorization-sensitive facts.

Use this validation shape without a duplicate top-level or per-field `code`:

```json
{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Request validation failed",
  "status": 422,
  "detail": "One or more request values are invalid.",
  "instance": "urn:request:01JZ8Y6M8W7Q",
  "errors": [
    {
      "pointer": "#/body/displayName",
      "detail": "must not be empty"
    }
  ]
}
```

Define `pointer` as a JSON Pointer fragment into this logical request document:
`body`, `query`, `path`, and `headers`. For example,
`#/query/pageSize`, `#/path/userId`, and `#/headers/If-Match`. This is the
skill's extension convention; RFC 9457 standardizes Problem Details but not this
logical request tree.

## Conditional Requests And Concurrency

- Return `ETag` for mutable resource representations and for reads that clients
  can revalidate.
- Require `If-Match` for `PUT`, `PATCH`, and `DELETE` against an existing mutable
  resource.
- Return `412 Precondition Failed` when the supplied validator is stale.
- Return `428 Precondition Required` when a required write precondition is
  absent.
- Use `If-None-Match` and `304 Not Modified` for cache revalidation.
- Define whether collection validators cover membership, member state, or both.

Do not invent a parallel version field protocol when standard conditional
headers already fit, unless an existing contract requires the field.

## Retries And Idempotency

State whether each operation can be retried after connection failure, timeout,
or unknown outcome.

- Rely on method idempotency for `PUT` and `DELETE`, while preserving the same
  intended effect across repetitions.
- Require `Idempotency-Key` for `POST` resource creation. Require it for any
  non-idempotent `PATCH` exposed at a network boundary.
- Specify key scope, identity binding, retention window, request fingerprint,
  replay response, and behavior when a key is reused with different content.
- Do not claim exactly-once execution. Define the observable deduplication
  guarantee instead.
- Return retry timing with `Retry-After` when the server knows it.

Bind a key to the authenticated principal, HTTP method, canonical target
collection, selected API version, and normalized request fingerprint. Replaying
the same request returns the original observable response. Reusing the key with
different content returns `409 Conflict` as Problem Details. Every API must
declare the retention window; the Idempotency-Key header specification remains
an IETF Internet-Draft rather than an RFC.

## Collections

Paginate every collection that can grow. Choose one project-level profile and
use it for every collection in that project. Do not select pagination per
endpoint.

Base the choice on project-wide evidence: caller navigation, exact-count needs,
dataset scale, write frequency, consistency guarantees, and the published
contract. If that decision is missing, return `PAGINATION PROFILE INCOMPLETE`;
do not invent page or cursor parameters for the current endpoint.

Always return this top-level shape:

```json
{
  "items": [],
  "pagination": {}
}
```

Never place pagination URLs under a body `links` object. Return navigation URLs
through the RFC 8288 `Link` response header. Do not invent `X-Page`,
`X-Total-Count`, or similar pagination headers.

### Page profile

Use for bounded back-office datasets whose UI needs direct page access and exact
counts:

- accept one-based `page` and bounded `pageSize`;
- return exact `page`, `pageSize`, `totalItems`, and `totalPages` numbers;
- provide applicable `first`, `previous`, `next`, and `last` relations as
  absolute URLs in `Link`;
- define deterministic ordering with a unique tie-breaker.

```json
{
  "items": [],
  "pagination": {
    "page": 1,
    "pageSize": 50,
    "totalItems": 973,
    "totalPages": 20
  }
}
```

### Cursor profile

Use for large, frequently changing, consumer-facing datasets:

- accept bounded `pageSize` and an opaque `pageToken`;
- return `pageSize` and omit `nextPageToken` on the terminal page;
- never return a total count;
- traverse a stable snapshot with deterministic ordering and a unique
  tie-breaker;
- bind the token to the effective filter, ordering, authorization scope, API
  version, and snapshot; declare token expiry;
- provide the next absolute URL as `rel="next"` in `Link` when another page
  exists.

```json
{
  "items": [],
  "pagination": {
    "pageSize": 50,
    "nextPageToken": "opaque-token"
  }
}
```

The `Link` URL and body metadata must describe the same page state. For cursor
pagination, the `pageToken` in the next link must equal `nextPageToken`. A
mismatch is a server contract defect. Do not use HTTP range statuses for
ordinary collection pagination.

Default to separately declared, strongly typed filter parameters. When compound
predicates require `filter`, define one project-wide formal grammar, field type
system, operator set, precedence, escaping, null behavior, and complexity limit.
Allow only pure predicates over declared resource fields; prohibit action or
command functions. A derived predicate is filterable only when it is an explicit
stable property or proven projection in the resource contract. Otherwise run
the field-versus-resource gate instead of renaming a business function into a
boolean query parameter. Never create endpoint-specific filter dialects.

Use `orderBy=createdAt desc,id asc`. Enumerate sortable fields, define the
default order, and append a unique tie-breaker when the caller omits one.

Search a resource collection with `GET` and query parameters when the query is
short, non-sensitive, cache-friendly, and URI-safe. Model a search request or
job resource when queries are large, sensitive, asynchronous, reusable, or have
their own lifecycle.

## Representations And Relationships

- Return a single resource object directly, with no generic `data` envelope.
- Return relationship URLs as absolute URIs under the resource's `links`
  property. These are resource relationships, not pagination metadata.
- Permit `include` only with values enumerated in OpenAPI. Embed the selected
  relationship in its named resource property and retain its relationship URL.
- Permit only OpenAPI-enumerated named `view` values such as `compact` or
  `full`; do not implement arbitrary `fields` masks.
- Omit unavailable, unauthorized, not-applicable, or unrequested optional
  properties. Return `null` only when it is a meaningful domain value.

## Asynchronous Work

Model long-running work as a domain-specific job, request, or attempt resource.
Do not expose a generic `/operations` collection:

- create it in a collection and return its canonical URI;
- expose explicit, forward-compatible states and timestamps;
- define polling cadence or server-provided retry guidance;
- link to results rather than overloading the job representation;
- represent cancellation as its own resource when the request has state,
  timing, authorization, failure, or audit semantics;
- delete the work resource only when removal is the actual contract, not as a
  hidden synonym for a retained cancellation transition;
- define terminal-state retention and audit behavior;
- create a new attempt for retry when history matters.

Avoid returning an unaddressable status token that forces clients to construct
polling URLs.

## Request And Trace Correlation

Keep request correlation and distributed tracing distinct:

- `Request-Id` identifies exactly one inbound HTTP request attempt at the API
  boundary. Generate a new opaque, high-entropy value on the server and return
  it on every response, including errors.
- `trace-id` identifies an entire distributed trace and can span many services,
  messages, and HTTP requests. Never reuse it as `Request-Id`; one trace can
  contain many request IDs.
- Use the W3C `traceparent` and `tracestate` request headers for trace
  propagation. Extract and validate incoming context, start a context when none
  is valid, and inject the current context into downstream requests.
- Implement propagation with the web framework's OpenTelemetry or equivalent
  instrumentation. Never parse, generate, or forward trace headers inside
  endpoint handlers.
- Do not expose separate `traceId` or `requestId` properties in Problem Details.
  Identify the occurrence with `instance: urn:request:{requestId}` and return
  the same value through `Request-Id`.
- Correlate structured logs with `requestId`, `traceId`, and `spanId`. Also log
  `operationId`, selected API version, status, and latency where available.
- Do not place personal, tenant, authentication, or business data in any
  correlation identifier or `tracestate` entry.

`Request-Id` is this skill's house header, not an IETF standard. Do not prefix it
with `X-`; RFC 6648 discourages new `X-` parameters. Do not trust an inbound
caller value as the server request ID. When client-side correlation is required,
define and validate a separate `Client-Request-Id` contract.

Use `Request-Id` as the public support correlation key. Trace context is the
cross-service propagation mechanism, not a replacement for the per-request key.
Do not return `tracestate` to callers. Expose response trace context only when
the project's observability and privacy policy explicitly requires it.

## Caching And Content Negotiation

- Define cacheability for every read that materially benefits from caching.
- Use `Cache-Control`, validators, and `Vary` deliberately.
- Do not cache personalized or secret data in shared caches unless directives
  make that safe.
- Declare request and response media types explicitly.
- Return `415` for unsupported request media and `406` when negotiation cannot
  produce an acceptable response.
- Use content negotiation for representation media types, not API versioning;
  this skill versions the contract only through `API-Version`.

## Authentication And Authorization

- Authenticate at the request boundary and produce a normalized principal.
- Authorize separately against the addressed resource, resource operation,
  current state, and requested representation.
- Treat validated roles, groups, scopes, and tenant claims as authorization
  inputs, never as authorization decisions.
- Keep principal roles out of resource paths and declare exact operation
  security requirements in OpenAPI.
- Use least-privilege OAuth scopes; never use scopes as a replacement for
  resource-level authorization.
- Apply authorization before collection pagination and total calculation, and
  prevent filters, links, views, and embedded resources from crossing tenant or
  ownership boundaries.
- Decide consistently when unauthorized resource existence is concealed as
  `404` rather than exposed through `403`.
- Return `401` for missing or invalid authentication and `403` for an
  authenticated principal that lacks authority.

## Standards

- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [RFC 9111: HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111)
- [RFC 5789: PATCH Method for HTTP](https://www.rfc-editor.org/rfc/rfc5789)
- [RFC 8288: Web Linking](https://www.rfc-editor.org/rfc/rfc8288)
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457)
- [RFC 7240: Prefer Header for HTTP](https://www.rfc-editor.org/rfc/rfc7240)
- [RFC 7396: JSON Merge Patch](https://www.rfc-editor.org/rfc/rfc7396)
- [RFC 6902: JSON Patch](https://www.rfc-editor.org/rfc/rfc6902)
- [RFC 6585: Additional HTTP Status Codes](https://www.rfc-editor.org/rfc/rfc6585)
- [RFC 6648: Deprecating the X- Prefix](https://www.rfc-editor.org/rfc/rfc6648)
- [RFC 6750: OAuth 2.0 Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
- [OpenTelemetry Context Propagation](https://opentelemetry.io/docs/concepts/context-propagation/)
- [Idempotency-Key HTTP Header Field Internet-Draft](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)
