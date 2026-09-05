---
name: bep-best-openapi-design
description: Design, change, or review REST/OpenAPI resource models, routes, or representations. Not for HTTP-only fixes or documentation wording.
---

# Resource-Oriented OpenAPI Design

## Choose The Project Baseline

For a new API, apply [BEP contract preferences](references/bep-profile.md):
resource-oriented paths, version-free URIs, and the defined representation profile.
These are deliberate engineering preferences, not all requirements of HTTP.
Use the [standards index](references/http-contract.md#standards) when checking
a normative protocol requirement.

For an existing API, preserve supported routes, version placement, names, errors,
pagination, and client expectations. Extend its established contract consistently,
including `/v1` paths when that is its convention. Do not require style migration,
deprecation, or a second protocol just because this skill is loaded. Apply BEP
preferences where no convention exists and doing so creates no inconsistency.
A requested migration needs an explicit compatibility plan; security or behavioral
bugs still require correction and are not excused as legacy style.

## Read For The Actual Decision

- [Resource modeling](references/resource-modeling.md): new resources or lifecycle
  changes. Prove identity, ownership, representation, and lifecycle; a noun-shaped
  command is not enough. Reuse the established model for a local field change.
- [Resource organization](references/resource-organization.md): deciding field,
  value object, independent resource, or owning domain.
- [Methods and errors](references/methods-errors.md): methods, statuses, and errors.
- [Collections](references/collections.md): pagination, filters, and representations.
- [Writes and jobs](references/writes-jobs.md): preconditions, retries, and job lifecycle.
- [Cache and correlation](references/cache-correlation.md): caching and tracing.
- [Authentication and authorization](references/authentication-authorization.md):
  designing or changing a protected contract, not every unrelated authenticated route.
- [OpenAPI evolution](references/openapi-evolution.md): schema publication,
  compatibility, versioning, and generated clients.
- [Framework integration](references/framework-integration.md): shared protocol
  infrastructure is being implemented or changed.
- [Canonical examples](references/canonical-http-examples.md): concrete BEP shapes.
- [Export example](references/dataset-export-example.md): an end-to-end resource
  lifecycle example is needed to resolve modeling uncertainty.

References describe BEP defaults; the existing-project baseline above takes
precedence over their style rules. Never load every reference mechanically.

## Complete The Affected Contract

For new BEP resources, expose creation, reads, updates, and deletion through
resource semantics rather than action paths. If a domain decision is missing,
identify it, prepare a reasoned proposal from available requirements, and pause
only the dependent operation when the choice needs product authority. Continue
independent work. Do not invent a resource just to pass a naming check.

Use the path helper from this skill's directory for new BEP paths:

```bash
python3 scripts/check_resource_paths.py --profile bep '/orders/{orderId}'
```

For an existing contract, `--profile existing` checks path structure without
imposing BEP naming, version placement, or action conventions. Compare against
the actual project contract separately. `--file` accepts one path per line.
The helper cannot prove resource semantics, request-body design, or API correctness.

When implementing, update the affected OpenAPI contract and callers, then run
local contract validation and the narrowest tests that prove changed behavior.
Use `$bep-http-engineering` only when deeper HTTP lifecycle work is needed.
Implementation ends after local acceptance, not at the first draft. Deployment
and live verification are separate unless included in the user's request.
For review, keep code read-only and distinguish defects from preference differences.
Report the actual decisions, changed contract, validation, and unresolved blockers;
scale detail to the change rather than filling a fixed audit template.
