# BEP Contract Preferences

Scope: apply BEP design preferences directly to new APIs. In an existing API,
preserve established supported conventions, including version placement, naming,
and representation shapes. Do not require migration or deprecation merely for
style conformity. The checks below apply to the changed contract and selected
profile; security, protocol correctness, and supported behavior remain required.

Use this profile directly for new APIs. For existing APIs, established compatible conventions take precedence; do not introduce parallel shapes or version schemes for a local change.

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
contract. When starting a new API, choose a suitable profile from the requirements and
state the rationale. If missing scale or consistency requirements materially
change that choice, propose the options and pause only the dependent collection
contract. Continue independent work. Existing APIs keep their pagination family.

Default to individually declared, strongly typed filter parameters. Enable a
single `filter` expression only when compound predicates are required. In that
case, require the project to publish one complete grammar and type system for
the whole API. Every filter must reference a declared resource property or a
proven, documented projection. Do not translate a business predicate such as
`isEligibleForRenewal()` into `eligibleForRenewal=true` unless renewal
eligibility is first modeled as stable resource state. Otherwise apply the
field-versus-resource gate and report `RESOURCE MODEL INCOMPLETE`. Never
improvise endpoint-specific filter syntax.
