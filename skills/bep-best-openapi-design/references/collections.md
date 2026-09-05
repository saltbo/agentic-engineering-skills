# Collection Contracts

Use BEP defaults for new APIs; preserve compatible existing project conventions.
Apply only the contract dimensions changed by this task.

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
