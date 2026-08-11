---
name: best-engineering-practice
description: Apply cross-cutting engineering constraints while planning, implementing, debugging, refactoring, testing, or reviewing software. Use for frontend, backend, full-stack, shared-module, compatibility, migration, and delivery work that needs explicit failure handling, boundary observability, simple domain-oriented design, clear dependency ownership, proportional executable proof, and reproducible verification. Load runtime, HTTP, and verification references only when their stated boundaries are affected.
---

# Best Engineering Practice

Produce correct software through explicit failure, simple ownership, unified
boundaries, and reproducible evidence. Apply repository conventions unless they
conflict with the Core.

## Load Only Applicable References

Read [references/core.md](references/core.md) for every task.

Load architecture guidance only for affected runtimes:

- Read [references/architecture/backend.md](references/architecture/backend.md)
  for services, handlers, workers, scheduled jobs, CLI processes, persistence,
  messaging, external integrations, or backend dependency direction.
- Read [references/architecture/frontend.md](references/architecture/frontend.md)
  for browser modules, UI, navigation, forms, design systems, client state,
  accessibility, browser security, or client performance.

Read [references/protocols/http.md](references/protocols/http.md) only when work
affects an HTTP lifecycle, browser-server interaction, Web API, cache,
authentication transport, upload, redirect, webhook, or HTTP middleware. Also
use `$best-openapi-design` when designing or changing a REST/OpenAPI contract.
Let that skill own resource modeling and the detailed REST profile.

Load verification guidance by the proof actually required:

- Read [references/verification/testing.md](references/verification/testing.md)
  when production behavior, tests, contracts, migrations, proof-layer choice,
  or test infrastructure changes.
- Read [references/verification/quality-gates.md](references/verification/quality-gates.md)
  when work affects coverage policy, proof inventories, native reports,
  exceptions, architecture enforcement, browser gates, or blocking CI policy.
- Read [references/verification/backend.md](references/verification/backend.md)
  when work affects HTTP or RPC operations, repositories, external adapters,
  caches, queue consumers, migrations, authentication, authorization, service
  lifecycle, execution-boundary observability, or backend dependency direction.
  Load testing and quality gates first.
- Read [references/verification/frontend.md](references/verification/frontend.md)
  when work affects browser routes, typed transports, feature operations, forms,
  navigation, browser state, accessibility, security, compatibility,
  performance, responsive behavior, visual quality, or frontend dependency
  direction. Load testing and quality gates first.

Do not load a runtime verification profile for an isolated pure-function,
documentation, formatting, or mechanical change unless its boundary or gate is
actually affected. For a vertical full-stack feature, load both architecture
profiles, testing, HTTP when applicable, and only the runtime verification
profiles required by the changed boundaries.

## Preserve The Requested Task Mode

Remain read-only for a plan, explanation, diagnosis, inspection, or review.
Describe required changes, migrations, tests, gates, and unresolved decisions.

For an authorized build, implementation, fix, or refactor, execute the workflow
below within the authorized scope. Inventory equivalent Core violations across
the repository, but require explicit repository-wide migration authorization
before mutating instances outside that scope.

## Execute Authorized Changes

### 1. Establish The Outcome And Baseline

Read applicable instructions, affected code, tests, contracts, release history,
and local conventions. Identify the observable outcome, consumers, supported
release baseline, trust and data boundaries, and the references required by the
loading rules above. Resolve hard-to-reverse ambiguity before changing an
interface or data model.

### 2. Design One Coherent Slice

Choose the smallest vertical behavior slice. Put each rule in its owning domain
module, keep dependencies and state explicit, and account for affected
contracts, persisted data, concurrency, and compatibility. Define the structural
signature of a corrected Core violation and search the complete repository for
equivalent instances. Correct the authorized scope and report the remaining
inventory; require a zero-match result only for an explicitly authorized
repository-wide migration.

### 3. Implement With Proportional Proof

Keep behavior and proof together. For a bug, first create a red-capable
regression. Use the cheapest test layer that proves the behavior completely and
real integration semantics at actual boundaries. Run focused checks while
working, then every configured gate applicable to the changed scope. Never skip
or weaken a gate to manufacture success.

### 4. Review And Report

Classify the change risk using the Core. Review the outcome against the request
and supported contracts, then review the engineering against the loaded
references and repository standards with risk-appropriate reviewer independence.
Verify findings, classify their severity and scope, resolve in-scope blocking
findings, and rerun affected checks.

Report the outcome, important decisions, changed contracts, migrations,
compatibility behavior, verification commands and results, finding severity and
scope, unmet gates, and unresolved or accepted risk. Do not claim success
without evidence.
