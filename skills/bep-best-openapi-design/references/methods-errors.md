# Methods And Errors

Use BEP defaults for new APIs; preserve compatible existing project conventions.
Apply only the contract dimensions changed by this task.

## Methods

| Method | Use | Semantics |
| --- | --- | --- |
| `GET` | Read a representation or collection | Safe, idempotent, cacheable unless constrained |
| `HEAD` | Read the metadata a `GET` would return | Safe, idempotent, no response content |
| `POST` | Create a server-identified member in the addressed collection | Neither safe nor inherently idempotent; define retry behavior and require `Idempotency-Key` only when the operation needs deduplication |
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
on the collection and define the duplicate and unknown-outcome behavior. Require
`Idempotency-Key` when callers must automatically retry an unknown outcome and
cannot reliably discover the original result, or when duplicate effects are
costly or irreversible. A create-only `PUT` can use `If-None-Match: *`;
replacement of an existing resource requires `If-Match`.

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
