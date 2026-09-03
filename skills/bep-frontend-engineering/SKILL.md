---
name: bep-frontend-engineering
description: Design, restructure, or review frontend architecture involving feature boundaries, browser state, remote data, rendering, forms, accessibility, browser security, persistence, compatibility, or client performance. Do not use for a small visual or mechanical edit.
---

# Frontend Engineering

Apply browser-runtime architecture guidance without loading backend or general
verification policy by default.

- Read [references/architecture.md](references/architecture.md) when the task
  changes feature ownership, state, effects, transport boundaries, rendering,
  forms, accessibility, security, offline behavior, storage, observability,
  compatibility, or performance.
- Read [references/verification.md](references/verification.md) only when the
  task designs or reviews frontend proof inventories, browser gates, visual or
  accessibility proof, or architecture enforcement.
- Use `$bep-http-engineering` only when browser-server protocol behavior is in scope.
- Use `$bep-software-testing` for general test-layer decisions and
  `$bep-verification-gates` only for formal coverage or CI governance.

Preserve the requested mode and the repository's UI conventions. Keep each
state and effect with one owner, treat external values as untrusted at runtime,
and keep server policy authoritative.
