---
name: bep-http-engineering
description: Design or fix HTTP caching, retries, conditional writes, authentication transport, or other request lifecycle semantics.
---

# HTTP Engineering

Trace the affected request far enough to establish the failing or changed
protocol behavior and its caller-visible outcome. Preserve existing supported
contracts; new projects use BEP defaults where relevant. A header fix does not
require redesigning resource ownership or unrelated lifecycle stages.

- [Contract](references/contract.md): inputs, responses, caching, compatibility,
  and framework policy. Inspect only the changed contract dimensions.
- [Writes](references/writes.md): duplicate submission, retries, concurrency,
  timeouts, and uncertain outcomes.
- [Trust boundaries](references/security.md): authentication, authorization,
  cookies, redirects, uploads, and sensitive data.
- [Correlation](references/correlation.md): request and downstream tracing changes.

Use `$bep-best-openapi-design` only when changing REST resources, routes, or
representations. Its absence does not block an independent HTTP task.
For implementation, verify the changed behavior locally through the actual
protocol boundary and relevant caller reconciliation. Fix change-caused failures
before reporting completion. Do not introduce formal proof inventories or CI
policy unless requested. Review-only work remains read-only.
