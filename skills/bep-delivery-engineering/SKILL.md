---
name: bep-delivery-engineering
description: Plan, implement, or review compatibility changes, persisted-data migrations, dependency or tool reproducibility, feature-flag transitions, releases, deployment sequencing, rollback, or roll-forward. Do not use for an unreleased internal edit with no delivery boundary.
---

# Delivery Engineering

Establish the supported release baseline before preserving compatibility. Do
not add compatibility branches for unpublished behavior or environments without
a support promise.

- Improve unreleased contracts directly and update their current callers.
- For a supported contract, follow its version and migration policy.
- Give compatibility paths, dual reads or writes, and feature flags an owner,
  supported range, observability, tests, and deletion condition.
- Use expand–migrate–switch–contract for live data or rolling deployment when
  required. Make backfills resumable and verify upgrades from every supported
  persisted version.
- Lock dependency and critical tool versions. Use deterministic generation and
  build commands shared by local development and CI.
- Publish immutable, traceable artifacts and keep generated artifacts with the
  source change when they form one logical unit.
- Define rollback or a prepared roll-forward before production release. Do not
  claim rollback safety when a data or public-contract transition is
  irreversible.

Preserve the requested task mode. Report the supported versions, transition
sequence, owners, observability, executable proof, removal conditions, and
remaining operational risk.
