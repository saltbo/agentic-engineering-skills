---
name: bep-backend-engineering
description: Design, restructure, or review backend architecture for services, workers, CLI processes, persistence, messaging, external integrations, dependency ownership, transactions, or service lifecycle. Do not use for a small backend edit that does not affect these boundaries.
---

# Backend Engineering

Apply backend-specific architecture guidance without loading unrelated frontend,
HTTP, delivery, or verification policy.

- Read [references/architecture.md](references/architecture.md) when the task
  changes module responsibilities, dependency direction, use cases, ports,
  persistence, caching, queues, events, configuration, or process lifecycle.
- Read [references/verification.md](references/verification.md) only when the
  task designs or reviews backend proof inventories, boundary tests, migrations,
  architecture enforcement, or lifecycle verification.
- Use `$bep-http-engineering` only when HTTP protocol behavior is in scope.
- Use `$bep-best-openapi-design` only when a REST/OpenAPI contract is designed or
  changed.
- Use `$bep-software-testing` for general test-layer decisions and
  `$bep-verification-gates` only for formal coverage or CI governance.

Preserve the requested mode and repository conventions. Keep business policy
independent from transports and providers, make state and dependency ownership
explicit, and avoid layers that only forward calls.
