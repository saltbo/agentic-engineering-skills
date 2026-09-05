# Canonical HTTP Examples

Scope: apply BEP design preferences directly to new APIs. In an existing API,
preserve established supported conventions, including version placement, naming,
and representation shapes. Do not require migration or deprecation merely for
style conformity. The checks below apply to the changed contract and selected
profile; security, protocol correctness, and supported behavior remain required.

Use these examples as the default output shape. Replace the domain names and
schemas, but preserve the protocol rules. The examples use the `identity-access`
domain group and a page-pagination project profile. They intentionally omit an
API version selector because versioning is a separate project decision, and the
ordinary user-creation example does not promise idempotent replay.

## Contents

- [Resource And Group Proof](#resource-and-group-proof)
- [List Resources](#list-resources)
- [Create With Server Identity](#create-with-server-identity)
- [Create At A Known URI](#create-at-a-known-uri)
- [Read One Resource](#read-one-resource)
- [Replace A Resource](#replace-a-resource)
- [Partially Update A Resource](#partially-update-a-resource)
- [Delete A Resource](#delete-a-resource)
- [Cursor Profile Alternative](#cursor-profile-alternative)
- [Problem Details](#problem-details)
- [Operation Identifiers](#operation-identifiers)

## Resource And Group Proof

| Concern | Decision |
| --- | --- |
| Resource | User account, not a screen or account-management command |
| Identity | Stable opaque user ID |
| Lifecycle | Created, retrieved, replaced, partially updated, and deleted |
| Domain group | `identity-access`, which owns account identity and invariants |
| Canonical URI | `https://api.example.com/users/{userId}` |
| Relationship | Manager is another user addressed by its canonical URI |

`displayName` remains a field because it has no independent identity, lifecycle,
authorization, query, or retention policy. A separately retained access grant
would be a resource because it has its own identity, policy, and lifecycle.

## List Resources

Use strongly typed filter parameters by default and the standard `orderBy`
syntax:

```http
GET /users?page=1&pageSize=2&state=active&orderBy=createdAt%20desc%2Cid%20asc HTTP/1.1
Host: api.example.com
Accept: application/json
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
Request-Id: req_01K1D2A6PXQ9
Vary: Accept
Link: <https://api.example.com/users?page=2&pageSize=2&state=active&orderBy=createdAt%20desc%2Cid%20asc>; rel="next", <https://api.example.com/users?page=487&pageSize=2&state=active&orderBy=createdAt%20desc%2Cid%20asc>; rel="last"

{
  "items": [
    {
      "id": "usr_02",
      "displayName": "Grace",
      "state": "active",
      "createdAt": "2026-08-01T12:00:00Z",
      "links": {
        "self": "https://api.example.com/users/usr_02"
      }
    },
    {
      "id": "usr_01",
      "displayName": "Ada",
      "state": "active",
      "createdAt": "2026-07-31T12:00:00Z",
      "links": {
        "self": "https://api.example.com/users/usr_01"
      }
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 2,
    "totalItems": 973,
    "totalPages": 487
  }
}
```

Pagination URLs occur only in `Link`. Resource relationship URLs inside each
item remain under that resource's `links` property.

An empty collection is still `200 OK`:

```json
{
  "items": [],
  "pagination": {
    "page": 1,
    "pageSize": 50,
    "totalItems": 0,
    "totalPages": 0
  }
}
```

## Create With Server Identity

Use `POST` when the server assigns the canonical URI:

```http
POST /users HTTP/1.1
Host: api.example.com
Content-Type: application/json
Accept: application/json
Prefer: return=representation

{
  "displayName": "Ada",
  "email": "ada@example.com"
}
```

```http
HTTP/1.1 201 Created
Location: https://api.example.com/users/usr_01
Content-Type: application/json
Request-Id: req_01K1D2B8GJ5A
ETag: "user-01-v1"
Preference-Applied: return=representation

{
  "id": "usr_01",
  "displayName": "Ada",
  "email": "ada@example.com",
  "state": "active",
  "createdAt": "2026-08-02T14:00:00Z",
  "links": {
    "self": "https://api.example.com/users/usr_01"
  }
}
```

The body is the resource itself, not `{ "data": { ... } }`. Define whether an
unknown outcome may be retried. If this operation instead promises deduplication,
require or accept `Idempotency-Key` explicitly and define its complete replay,
retention, concurrency, and conflicting-reuse contract.

## Create At A Known URI

Use idempotent `PUT` when the client owns a stable identifier:

```http
PUT /users/usr_client_01 HTTP/1.1
Host: api.example.com
Content-Type: application/json
If-None-Match: *

{
  "displayName": "Lin",
  "email": "lin@example.com"
}
```

The first successful creation returns `201 Created` and `Location`. If the URI
already exists, the create-only precondition fails with `412`.

## Read One Resource

Use only enumerated `view` and `include` values:

```http
GET /users/usr_01?view=full&include=manager HTTP/1.1
Host: api.example.com
Accept: application/json
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
Request-Id: req_01K1D2C3VH6N
ETag: "user-01-v3"

{
  "id": "usr_01",
  "displayName": "Ada",
  "email": "ada@example.com",
  "state": "active",
  "manager": {
    "id": "usr_00",
    "displayName": "Grace",
    "links": {
      "self": "https://api.example.com/users/usr_00"
    }
  },
  "links": {
    "self": "https://api.example.com/users/usr_01",
    "manager": "https://api.example.com/users/usr_00"
  }
}
```

## Replace A Resource

`PUT` supplies the complete client-writable representation and requires the
current validator:

```http
PUT /users/usr_01 HTTP/1.1
Host: api.example.com
Content-Type: application/json
If-Match: "user-01-v3"

{
  "displayName": "Ada Lovelace",
  "email": "ada@example.com"
}
```

Return `200 OK`, a new `ETag`, and the replaced resource. Use `201 Created` only
when the addressed resource did not previously exist.

## Partially Update A Resource

Use JSON Merge Patch by default:

```http
PATCH /users/usr_01 HTTP/1.1
Host: api.example.com
Content-Type: application/merge-patch+json
If-Match: "user-01-v4"

{
  "displayName": "Ada King"
}
```

Return `200 OK`, the current representation, and a new `ETag`. Add
`application/json-patch+json` only when the operation genuinely requires array
member or exact path operations. Never accept an `action`, `command`, or target
business `status` as a disguised RPC.

## Delete A Resource

```http
DELETE /users/usr_01 HTTP/1.1
Host: api.example.com
If-Match: "user-01-v5"
```

```http
HTTP/1.1 204 No Content
Request-Id: req_01K1D2D02B4T
```

`DELETE` removes the association represented by the target URI. Retention,
tombstone, and audit behavior remain explicit domain policy.

## Cursor Profile Alternative

This is an alternative project profile, not an endpoint-level alternative to
the page profile above:

```http
GET /events?pageSize=50 HTTP/1.1
Host: api.example.com
```

```http
HTTP/1.1 200 OK
Content-Type: application/json
Request-Id: req_01K1D2EJ6M31
Link: <https://api.example.com/events?pageSize=50&pageToken=opaque-token>; rel="next"

{
  "items": [],
  "pagination": {
    "pageSize": 50,
    "nextPageToken": "opaque-token"
  }
}
```

On the terminal page, omit both `nextPageToken` and the `rel="next"` link. Never
return `totalItems` or `totalPages` in the cursor profile.

## Problem Details

Malformed JSON or protocol parameters return `400`. A syntactically valid body
that violates declared content constraints returns `422`:

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json
Request-Id: req_01K1D2F0QAB8

{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Request validation failed",
  "status": 422,
  "detail": "One or more request values are invalid.",
  "instance": "urn:request:req_01K1D2F0QAB8",
  "errors": [
    {
      "pointer": "#/body/email",
      "detail": "must be a valid email address"
    }
  ]
}
```

Use these protocol distinctions consistently:

| Condition | Status |
| --- | --- |
| Missing required `If-Match` | `428 Precondition Required` |
| Stale `If-Match` | `412 Precondition Failed` |
| Reused idempotency key with different content | `422 Unprocessable Content` |
| Concurrent request with the same idempotency key | `409 Conflict` |
| Unsupported PATCH media type | `415 Unsupported Media Type` |
| Missing or invalid authentication | `401 Unauthorized` with `WWW-Authenticate` |
| Authenticated principal lacks resource authority | `403 Forbidden` |
| Rate limit exceeded | `429 Too Many Requests` with `Retry-After` when known |

Every error uses Problem Details and returns `Request-Id`. Do not add separate
`code`, `requestId`, or `traceId` properties.

## Operation Identifiers

Use stable resource-operation identifiers:

| HTTP operation | `operationId` |
| --- | --- |
| `GET /users` | `listUsers` |
| `POST /users` | `createUser` |
| `GET /users/{userId}` | `getUser` |
| `PUT /users/{userId}` | `replaceUser` |
| `PATCH /users/{userId}` | `updateUser` |
| `DELETE /users/{userId}` | `deleteUser` |

Do not use command identifiers such as `activateUser`, `cancelOrder`, or
`generateReport`.
