---
name: bep-delivery-engineering
description: Plan, execute, or review releases, deployments, data/contract migrations, or rollback. Not for ordinary local implementation.
---

# Delivery Engineering

Distinguish preparation, review, and an authorized deployment. Preserve the
requested mode: a release plan is not authority to publish. Once deployment is
authorized, carry it through post-deployment regression within that authority.

- [Compatibility](references/compatibility.md): supported versions, persisted-data
  migrations, feature-flag transitions, rollback, and reproducible artifacts.
- [Deployment](references/deployment.md): local acceptance, target and artifact
  selection, provider execution, live regression, and recovery.

For a new project, establish BEP delivery conventions appropriate to its actual
runtime. In an existing project, use its release commands, support promise, API
version policy, and rollout strategy. Do not force modernization as part of a
routine deployment. Improve unpublished behavior directly where no supported
consumer or persisted-data boundary requires compatibility.

Use `$bep-production-verification` for post-deployment regression when available.
If it is not installed, follow the bounded regression requirements in the
Deployment reference; missing optional skills must not erase the release checks.
Report preparation, deployment, and regression outcomes distinctly.
