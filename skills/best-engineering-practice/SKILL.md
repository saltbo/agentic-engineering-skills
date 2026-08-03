---
name: best-engineering-practice
description: Enforce technology-independent and Web-specific engineering constraints while planning, implementing, debugging, refactoring, testing, or reviewing software. Use for frontend applications, backend services, full-stack features, shared modules, tests, architecture, compatibility, or delivery work that requires explicit error handling, unified boundary observability, simple domain-oriented design, owned ports and test doubles, Clean Architecture dependency direction, layered testing, measurable coverage, reproducible verification, versioned compatibility, and independent outcome and engineering review.
---

# Best Engineering Practice

Produce correct software through explicit failure, simple design, unified
boundaries, and reproducible evidence. Apply repository conventions only when
they satisfy the non-negotiable Core.

## Load Guidance By Responsibility

Read [references/core.md](references/core.md) for every task.

Load architecture guidance for every affected runtime:

- Read [references/architecture/backend.md](references/architecture/backend.md)
  for services, handlers, workers, scheduled jobs, CLI processes, persistence,
  messaging, or external integrations.
- Read [references/architecture/frontend.md](references/architecture/frontend.md)
  for browser modules, UI, navigation, forms, design systems, client state or
  persistence, accessibility, browser security, or client performance.

Read [references/protocols/http.md](references/protocols/http.md) whenever work
or review affects an HTTP request lifecycle, browser-server interaction, Web
API, HTTP cache, authentication transport, or other HTTP contract.

Load verification guidance whenever production behavior or its proof changes:

- Read [references/verification/testing.md](references/verification/testing.md)
  for proof-layer selection, behavioral tests, deterministic execution,
  contracts, BDD specifications, and E2E evidence.
- Read [references/verification/quality-gates.md](references/verification/quality-gates.md)
  for coverage thresholds, proof identities, inventory integrity, native test
  reports, exceptions, and blocking CI gates.
- Read [references/verification/backend.md](references/verification/backend.md)
  when backend operations, repositories, adapters, consumers, migrations,
  service lifecycle, observability, or dependency direction need proof.
- Read [references/verification/frontend.md](references/verification/frontend.md)
  when frontend routes, transports, feature operations, browser behavior,
  accessibility, performance, security, or visual quality need proof.

Load both architecture profiles and both verification profiles for a vertical
full-stack feature. When designing or changing a REST/OpenAPI contract, also use
`$best-openapi-design` if it is available in the workspace.

## Preserve The Requested Task Mode

For a plan, explanation, diagnosis, inspection, or review, remain read-only.
Evaluate the artifact and describe the required change, migration, tests, gates,
and reviews. Return analysis only; implementation requires explicit change
authorization.

For an authorized build, implementation, fix, or refactor, execute the workflow
below. Repository-wide internal correction of an encountered Core violation is
part of that change authorization and does not require separate approval.

## Execute Authorized Changes In This Order

### 1. Establish The Outcome And Release Baseline

Read applicable instructions, affected code, tests, contracts, release history,
and local conventions. State:

- the observable outcome and completion evidence;
- the consumers and public interfaces involved;
- whether the affected behavior is unreleased or part of a supported release;
- the trust, data, concurrency, compatibility, and operational boundaries;
- the architecture, protocol, and verification references loaded for the task.

Resolve important ambiguity before fixing an interface or data model. Distinguish
the required capability from any suggested mechanism.

Completion criterion: every affected boundary and applicable reference is
identified, and every hard-to-reverse ambiguity is resolved.

### 2. Design The Smallest Coherent Change

Choose one vertical behavior slice at a time. Put behavior in the module that
owns the domain rule. Prefer direct data flow, explicit dependencies, immutable
values, small public interfaces, and deep implementations.

When logic becomes convoluted, inspect the data model and responsibility split.
Restructure the root cause instead of adding conditionals, fallbacks, or
defensive patches.

After identifying a Core violation or competing pattern in affected code,
define its structural signature, search the complete repository for equivalent
instances, and record every match in a migration inventory. Keep the main task
on its primary path. Delegate the migration when independent workers are
available; otherwise complete it in the main context. Finish with one pattern
and a final repository-wide search that finds no remaining match. Preserve
released behavior and apply the version and data-migration rules.

Completion criterion: the proposed slice owns one observable behavior, every
affected contract and migration is accounted for, and the migration inventory
has a defined zero-match condition.

### 3. Implement And Verify One Slice

Keep behavior and its proof together. For a bug, write a red-capable regression
test before the fix. For an established interface, prefer test-first work. Use
a throwaway prototype only to discover an uncertain interface or behavior.

Provide a canonical contract, production implementation, and mock or fake for
every substitutable cross-module capability consumed by business code. The
capability normally owns its contract. For an outward Port, the inner business
caller owns the contract and test double while the outer Adapter provides the
production implementation. Test exported pure functions, immutable values, and
UI components directly; do not manufacture interfaces or fakes for them.

Run focused checks continuously. Maintain BDD traceability when observable
product behavior changes. Meet every loaded verification profile, then run
every configured formatter, build, type, static-analysis, test, coverage,
contract, generation, and architecture gate. Never weaken or skip a gate to
manufacture success.

Completion criterion: every changed behavior has mapped executable proof, every
loaded verification gate passes, and the migration inventory is empty.

### 4. Review Independently

Review non-mechanical changes in two distinct contexts isolated from the
implementation reasoning and from each other's initial findings:

1. **Outcome:** Verify the requested behavior, scope, and supported contracts.
2. **Engineering:** Verify errors, observability, tests, coverage, module
   ownership, dependencies, compatibility, security, and operability.

Verify and fix both sets of findings, then rerun affected gates. When distinct
independent contexts are unavailable, run the axes separately, report the
missing independence, and leave the independent-review gate unmet.

Completion criterion: both reviews are recorded, every finding is resolved or
reported as unresolved, and every affected gate has been rerun.

### 5. Report Evidence

Report the outcome, important decisions, changed contracts, migrations,
compatibility behavior, unit-code coverage, integration-boundary coverage,
critical-journey coverage, BDD traceability, verification commands and results,
review findings, unmet gates, and unresolved risk. Identify every permitted
exception and link its required record.

Completion criterion: every applicable loaded-reference gate has explicit
passing evidence or is named as unmet; absence of evidence is never success.
