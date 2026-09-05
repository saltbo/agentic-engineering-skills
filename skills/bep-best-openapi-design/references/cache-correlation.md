# Caching And Correlation

Use BEP defaults for new APIs; preserve compatible existing project conventions.
Apply only the contract dimensions changed by this task.

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
- Use content negotiation for representation media types, not API versioning.
  When versioning is selected, use the project's `API-Version` header policy.
