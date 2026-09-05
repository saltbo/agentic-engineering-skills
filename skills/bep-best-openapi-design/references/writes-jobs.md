# Writes And Asynchronous Jobs

Use BEP defaults for new APIs; preserve compatible existing project conventions.
Apply only the contract dimensions changed by this task.

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
- Consider `Idempotency-Key` for non-idempotent `POST` and `PATCH` operations.
  Require it when clients must automatically retry an unknown outcome that they
  cannot otherwise resolve, duplicate effects are costly or irreversible, or
  the operation contract explicitly promises deduplication. Do not add it to
  every write by default.
- Specify key scope, identity binding, retention window, request fingerprint,
  replay response, and behavior when a key is reused with different content.
- Do not claim exactly-once execution. Define the observable deduplication
  guarantee instead.
- Return retry timing with `Retry-After` when the server knows it.

When an operation uses a key, bind it to the authenticated principal, HTTP
method, canonical target, selected API version when applicable, and normalized
request fingerprint. Replaying the same request returns the original observable
response. Reusing the key with different content returns `422 Unprocessable
Content`; a duplicate request received while the original is still processing
returns `409 Conflict`. Declare the retention window and quote the field value
as an RFC 8941 string, for example `Idempotency-Key: "uuid-value"`.

The Idempotency-Key header specification is an IETF Internet-Draft, not an RFC.
Treat it as work in progress, verify the current revision before implementation,
and distinguish its wire requirements from the project's decision about which
operations require the header.

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
