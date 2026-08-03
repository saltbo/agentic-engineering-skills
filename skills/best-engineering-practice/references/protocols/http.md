# HTTP Protocol Constraints

Apply these constraints whenever work or review affects an HTTP request
lifecycle, browser-server interaction, Web API, HTTP cache, authentication
transport, upload, redirect, webhook, or other HTTP contract. The frontend and
backend architecture references own runtime structure; this file owns protocol
semantics shared across that boundary.

## Contents

- [Trace The Complete Request Lifecycle](#trace-the-complete-request-lifecycle)
- [Define One Complete HTTP Contract](#define-one-complete-http-contract)
- [Separate Identity From Permission](#separate-identity-from-permission)
- [Make Writes Safe Under Repetition And Concurrency](#make-writes-safe-under-repetition-and-concurrency)
- [Centralize Protocol Policy](#centralize-protocol-policy)
- [Secure Every HTTP Trust Transition](#secure-every-http-trust-transition)
- [Correlate The Complete Interaction](#correlate-the-complete-interaction)
- [Apply The HTTP Completion Gate](#apply-the-http-completion-gate)

## Trace The Complete Request Lifecycle

Trace each affected interaction end to end:

1. user intent or caller request;
2. client validation and request construction;
3. authentication and server-side authorization;
4. domain operation and persistence;
5. response or asynchronous result;
6. caller reconciliation, retry, and visible failure.

Account for applicable success, validation, authentication, authorization,
conflict, timeout, cancellation, duplicate, uncertain-result, and unexpected-
failure behavior. Each state has an owner and stable protocol semantics.

Completion criterion: every lifecycle stage and applicable outcome maps to its
owning runtime module, contract representation, and required proof profile.

## Define One Complete HTTP Contract

Define together:

- method and canonical path;
- path, query, header, cookie, and body inputs;
- success and error representations;
- status codes and stable error identities;
- authentication and authorization expectations;
- caching, freshness, validators, and invalidation;
- idempotency, concurrency, retry, cancellation, and timeout semantics;
- correlation and Trace propagation;
- compatibility and migration behavior.

Validate untrusted input at the server transport even when a client already
validates it. Translate domain and application failures into HTTP only at the
transport boundary. Preserve published consumer compatibility or introduce the
change through the supported version and migration policy.

For REST routes or OpenAPI contracts, load `$best-openapi-design` when it is
available and let it own resource modeling and the detailed REST profile. When
it is unavailable, leave the specialized resource-modeling gate explicitly
unmet rather than inventing a competing local profile.

## Separate Identity From Permission

Authenticate at the HTTP execution boundary and produce a normalized immutable
principal. Authorize separately against the addressed resource, operation,
ownership, tenant, state, and requested fields. A valid identity is input to a
permission decision, never proof of permission.

Keep raw tokens and provider claims out of business code. Expose stable
authentication and authorization failure categories without leaking credential
details or turning denial into resource success.

## Make Writes Safe Under Repetition And Concurrency

Define write behavior for refresh, double submission, timeout, client retry,
concurrent update, and an unknown response outcome. Use operation-appropriate
idempotency identity, conditional request semantics, version checks, or
datastore constraints.

Retry only a transient failure at the boundary that owns the complete operation
semantics. Require idempotency, finite attempts, backoff, jitter, and an overall
deadline. A client or intermediary may not infer that an uncertain write failed
and silently repeat a non-idempotent operation.

## Centralize Protocol Policy

Use framework-native request and response boundaries for:

- validation and normalized input;
- stable error mapping;
- authentication extraction;
- request and Trace correlation;
- security headers;
- common serialization and content negotiation;
- access-event observability;
- audit derivation when canonical resource operations make it possible.

Handlers own operation-specific translation and invocation, not duplicated
framework policy. Business modules remain independent from HTTP status codes,
headers, request objects, response objects, and provider authentication types.

## Secure Every HTTP Trust Transition

Keep credentials and privileged data out of URLs, redirects, ordinary logs,
error bodies, caches, and browser-readable configuration. Apply established
platform controls for cookie scope, transport security, CSRF, CORS or origin
policy, redirects, uploads, and content handling.

Authorize the addressed resource and fields, not only the route or coarse role.
Apply upload size, decoded-size, content, rate, and cost limits where untrusted
input can consume material resources. Use mature protocol and cryptography
implementations; never invent an authentication or token format.

## Correlate The Complete Interaction

Propagate stable request and Trace context from the caller through the HTTP
boundary, downstream dependencies, and asynchronous work. Extract incoming
Trace context according to the supported standard, start a new root only when
no valid parent exists or scheduled semantics require it, and inject context
into traced downstream calls.

Let the server request boundary own the one structured diagnostic completion
event. Use Metrics for aggregation and Traces for causal flow. Browser-visible
failure, server execution, dependency calls, and asynchronous continuation must
be correlatable without logging request or response bodies.

## Apply The HTTP Completion Gate

Reject completion when any of the following is true:

- an affected lifecycle stage or outcome has no explicit owner or semantics;
- method, path, representation, error, cache, concurrency, retry, timeout, or
  compatibility behavior is implicit or contradictory;
- client validation is treated as server validation;
- authentication is treated as authorization;
- a repeated or uncertain write can silently duplicate irreversible work;
- HTTP request, response, status, header, or provider identity types cross into
  business policy;
- protocol policy is repeated in individual handlers instead of its shared
  boundary;
- credentials or sensitive bodies can enter URLs, logs, caches, or errors;
- request, downstream, and asynchronous work cannot be correlated;
- an applicable REST/OpenAPI or loaded verification gate remains unmet.
