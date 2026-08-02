# Web Engineering Baseline

Apply this guidance to any system spanning a browser, HTTP server, edge runtime,
or Web-facing integration. Then load the frontend or backend reference for the
code being changed.

## Establish Runtime Ownership

For each piece of state and behavior, decide whether it belongs to:

- the URL and navigation history;
- browser-only interaction state;
- server-owned application data;
- a durable datastore;
- an edge or cache layer;
- a third-party system.

Keep one authoritative owner. Derive duplicated views when possible. Do not let
client state become an accidental authority for permissions, money, inventory,
workflow state, or other server-owned invariants.

## Design The Request Lifecycle

Trace each important interaction end to end:

1. user intent or caller request;
2. client validation and request construction;
3. authentication and server-side authorization;
4. domain operation and persistence;
5. response or asynchronous result;
6. UI reconciliation, retry, and user-visible failure.

Make loading, empty, partial, stale, success, validation-error, authorization,
conflict, timeout, and unexpected-failure states deliberate. Avoid a generic
spinner and generic error message when the user can take a specific recovery
action.

## Treat HTTP As A Contract

- Define method, path, request, response, status, headers, errors, caching,
  concurrency, and retry behavior together.
- Validate untrusted input at the server boundary even when the client already
  validates it.
- Keep authentication and authorization separate. A valid identity is input to
  a permission decision, not proof of permission.
- Make writes safe under refreshes, duplicate submissions, timeouts, and
  concurrent updates through suitable idempotency and preconditions.
- Preserve backward compatibility for published consumers or provide an
  explicit migration.
- Centralize protocol concerns such as error mapping, request correlation,
  tracing, security headers, and common serialization in framework-native
  boundaries rather than repeating them in handlers.

For REST routes or OpenAPI contracts, load `$best-openapi-design` when it is
available and let it own resource modeling and the detailed HTTP profile. When
it is unavailable, apply this Web contract guidance and report that the
specialized resource-modeling profile was not available.

## Secure Every Trust Transition

- Keep secrets and privileged credentials out of browser bundles, URLs, logs,
  and error bodies.
- Encode output for its rendering context. Avoid unsafe HTML and dynamic code
  execution.
- Protect session and credential flows with the established platform controls
  for cookie scope, CSRF, origin, redirect, and transport security.
- Authorize the addressed resource and requested fields, not only the route or
  a coarse role.
- Apply upload limits, content validation, rate or cost limits, and abuse
  controls where untrusted input can consume material resources.

Use the project's security model and threat analysis. Do not invent custom
cryptography, tokens, or authentication protocols.

## Make Production Behavior Observable

- Correlate the browser-visible failure, server request, downstream calls, and
  background work with stable request or trace context.
- Emit correlated Trace Spans and Metrics around dependency boundaries and
  important decisions. Let the request or task execution boundary own the one
  structured diagnostic log; do not log secrets or entire sensitive payloads.
- Measure latency and errors at user-meaningful boundaries, not only individual
  functions.
- Define health, readiness, timeout, retry, and graceful-shutdown behavior for
  server processes that own traffic.

## Verify Across The Right Seams

Use the narrowest check that can catch the failure:

- pure tests for deterministic domain or presentation logic;
- component tests for browser interaction through accessible UI;
- integration tests through the real HTTP or application boundary;
- contract tests between independently deployed consumers and providers;
- end-to-end tests for a small set of critical journeys;
- browser and server profiling for measured performance risks.

Do not duplicate the same assertion at every level. Each test should protect a
distinct contract or failure mode.
