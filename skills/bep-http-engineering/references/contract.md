# HTTP Contract

## Define One Complete HTTP Contract

For the affected interaction, establish the relevant contract dimensions:

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

Use `$bep-best-openapi-design` only when changing REST resource models, routes,
or representations. A protocol-only change can proceed independently. Preserve
existing contract conventions rather than importing BEP style as a prerequisite.

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
