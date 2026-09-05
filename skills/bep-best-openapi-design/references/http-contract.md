# HTTP Contract Reference Map

Apply BEP defaults to new APIs and preserve supported conventions in existing APIs.
Read only the relevant contract area:

- [Methods and errors](methods-errors.md): method semantics, statuses, and Problem Details.
- [Writes and jobs](writes-jobs.md): preconditions, retries, idempotency, and asynchronous work.
- [Collections](collections.md): pagination, filters, ordering, and representations.
- [Cache and correlation](cache-correlation.md): caching, content negotiation, and tracing.
- [Authentication and authorization](authentication-authorization.md): protected contracts.

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
- [Idempotency-Key HTTP Header Field Internet-Draft (work in progress)](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)
