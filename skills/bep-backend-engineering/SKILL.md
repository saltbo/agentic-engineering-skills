---
name: bep-backend-engineering
description: Design, restructure, or review backend ownership, dependencies, transactions, messaging, or lifecycle. Not for ordinary handler edits.
---

# Backend Engineering

For a new project, apply BEP dependency and ownership preferences directly.
For an existing project, inspect the affected boundary and preserve its working
conventions and supported contracts. Improve local design without turning a
feature or fix into an architecture migration.

Read only what the decision needs:

- [Ownership](references/ownership.md): module boundaries, dependency injection,
  use cases, ports, models, and stable errors.
- [Persistence](references/persistence.md): transactions, repositories, and caches.
- [Messaging](references/messaging.md): queues, durable jobs, and events.
- [Lifecycle](references/lifecycle.md): startup, readiness, and shutdown.
- [Verification](references/verification.md): only when designing or auditing
  formal backend proof inventories and architecture enforcement.

Use `$bep-http-engineering` only for an HTTP semantic change and
`$bep-best-openapi-design` only for REST resource or representation design.
These are optional specialist workflows, not prerequisites for backend work.

For implementation, complete local acceptance: run the smallest meaningful
checks and exercise the changed behavior, fix failures caused by the change,
and report evidence. For test design use `$bep-software-testing`; merely running
existing tests does not require loading it. Review-only requests remain read-only.
