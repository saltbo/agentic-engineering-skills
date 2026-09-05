---
name: bep-frontend-engineering
description: Design, restructure, or review frontend ownership, state, effects, or browser boundaries. Not for small visual or copy edits.
---

# Frontend Engineering

Apply BEP preferences directly to a new project. In an existing project, work
within its feature and framework conventions and improve the affected boundary;
do not introduce an architecture or tooling migration merely to match this skill.
Keep server business policy authoritative and each state/effect with one owner.

Read only the relevant reference:

- [Ownership and state](references/ownership.md): features, dependencies, state,
  and effect lifecycles.
- [Remote data](references/remote-data.md): transport, decoding, and reconciliation.
- [Interaction](references/interaction.md): components, forms, and accessibility.
- [Security and storage](references/security-storage.md): identity, scripts,
  durable browser data, and offline behavior.
- [Performance](references/performance.md): rendering, telemetry, and compatibility.
- [Verification](references/verification.md): only for formal frontend inventories,
  architecture enforcement, or browser-quality governance.

For implementation, local acceptance is required: use focused checks and inspect
affected interaction and responsive behavior in a local browser when applicable.
Fix change-caused failures and report what was exercised. Choose test layers with
`$bep-software-testing` when designing tests; do not load it just to run them.
Use `$bep-http-engineering` only when HTTP semantics change. Missing optional
skills do not block independent frontend work. Reviews remain read-only.
