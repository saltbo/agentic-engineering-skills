---
name: bep-verification-gates
description: Design, implement, or audit formal verification governance such as proof inventories, coverage denominators, native test reports, exceptions, architecture enforcement, browser gates, or blocking CI policy. Do not use for ordinary test writing or merely running existing checks.
---

# Verification Gates

Apply these gates only when formal coverage or CI governance is in scope. They
define a proof protocol that runtime verification profiles may adopt; loading a
runtime architecture skill does not by itself require this skill.

## Contents

- [Use Stable Proof Identities](#use-stable-proof-identities)
- [Use Ecosystem Proof Adapters](#use-ecosystem-proof-adapters)
- [Trace Product Behavior Through BDD](#trace-product-behavior-through-bdd)
- [Derive Inventories From Production](#derive-inventories-from-production)
- [Define Applicability Mechanically](#define-applicability-mechanically)
- [Measure Independent Coverage Denominators](#measure-independent-coverage-denominators)
- [Permit Only Recorded Legacy Coverage Exceptions](#permit-only-recorded-legacy-coverage-exceptions)
- [Verify Test Execution From Native Reports](#verify-test-execution-from-native-reports)
- [Enforce Blocking CI Gates](#enforce-blocking-ci-gates)
- [Apply The Quality-Gate Completion Gate](#apply-the-quality-gate-completion-gate)

## Use Stable Proof Identities

Give every governed production item and proof a stable machine-readable identity.
Generate one normalized inventory record for every testable item:

```text
kind | stable id | production source | required profiles
```

Represent coverage as `(inventory item, required profile)` pairs. A pair is
covered only when it maps to an executable test in the required proof layer and
the native runner reports that test executed and passed.

Give every BDD scenario, critical journey, public operation, Repository,
external Adapter, Consumer, migration path, observability boundary, frontend
route, frontend transport, and frontend feature operation its profile-defined
stable identity. Give every stable Port failure category both a production and
handling proof identity.

Keep governance identities as literal, statically discoverable metadata in the
ecosystem's canonical test declaration. Parameterized execution may implement
the matrix underneath, but every required proof identity remains independently
discoverable and attributable to one proof layer.

## Use Ecosystem Proof Adapters

Do not force one test framework's declaration syntax or report format onto
another. Require each governed ecosystem to provide a deterministic proof
adapter that emits this normalized record for every expected and executed test:

```text
proof layer | stable proof ids | source file | test id | status |
skipped | retried | repeated | expected failure
```

The adapter must define:

- the supported static test declarations and parameterized forms;
- how stable proof identities are attached;
- how source files and proof layers are classified;
- the native machine-readable report and integrity reporter;
- how skipped, pending, focused, retried, repeated, expected-failure, aborted,
  and empty execution are represented;
- how expected source declarations reconcile with executed native-report items.

A JavaScript adapter may use literal metadata in statically named `test(...)`
or `it(...)` titles. Other ecosystems must use their native stable declaration
or metadata mechanism. An ecosystem without a complete adapter leaves the
quality gate unmet; an Agent may not invent an unverifiable estimate.

## Trace Product Behavior Through BDD

Use lightweight `.feature` files as the source of truth for user-visible product
behavior. Write scenarios in domain language and observable outcomes, without
database tables, HTTP paths, CSS selectors, classes, mocks, or other
implementation details.

Every scenario has one unique stable ID and declares its cheapest canonical
proof layer, for example `@id:ORD-001 @proof:unit`. The proving test carries the
same stable ID through the ecosystem proof adapter. The BDD lint gate proves:

- every scenario ID is unique and maps to at least one executable test;
- every mapped test exists in the declared proof layer;
- no required scenario or proving test is skipped;
- deleted or renamed scenarios leave no orphaned proof identity.

Map each scenario to the Unit, Integration, or E2E tests that prove it.

Update or add the scenario before implementing new or changed user-visible
behavior. A behavior-preserving refactor, dependency update, performance-only
change, or behavior-preserving migration does not change the scenario. For a
bug, add a scenario only when the product specification was missing or
ambiguous; otherwise link the regression test to the existing scenario.

## Derive Inventories From Production

Generate inventories from authoritative production artifacts, never a parallel
testing checklist:

- API operations from authoritative protocol operation identities;
- routes from the real runtime router and production route metadata;
- Repositories, external Adapters, Consumers, and observability boundaries from
  production registries or architecture-enforced directories;
- concrete request, Consumer, scheduled, and CLI wiring from production
  composition registries;
- stable Port errors from the Port's enumerable error taxonomy;
- migrations from migration history and supported-version policy;
- frontend routes, transports, operations, and bindings from production router,
  contract, and feature-operation declarations;
- BDD scenarios and critical journeys from feature IDs and tags.

Make the generator consume declarations also used by production composition.
Compare declared routes with the runtime router, registered adapters with
architecture-owned files, and migration declarations with history on disk.
Emit deterministic per-kind counts and a content digest, and have the linter
recompute both.

A generic collector cannot prove its own provenance. Add a stack-specific
source or import-graph gate that proves the collector reaches the actual router,
composition registries, and feature wrappers. Keep the collector gate unmet
until that provenance is mechanically established.

Use a manual inventory entry only when production derivation is impossible.
Every manual entry records its reason, owner, and expiry or removal condition.
Frontend verification permits no manual item or profile exception.

## Define Applicability Mechanically

Derive required profiles from production-owned capability metadata. An omitted
default profile is allowed only when semantically impossible, never merely
inconvenient. When metadata cannot express the semantic fact, record this exact
exception shape beside the production declaration:

```json
{
  "profileExceptions": [
    {
      "profile": "authentication",
      "reason": "The operation is reachable only through an authenticated private service binding",
      "owner": "orders",
      "removalCondition": "Remove when the operation becomes directly network-addressable"
    }
  ]
}
```

Lint the exception like a production declaration. Reject an unknown profile,
missing owner, vague reason, stale condition, or exception that metadata can
express directly. Do not except an observability boundary's derived contract,
a concrete entry's production wiring, or any frontend inventory profile.

## Measure Independent Coverage Denominators

Enforce these independent blocking thresholds:

| Gate | Required threshold |
| --- | ---: |
| Unit production-code coverage | at least 90% |
| BDD scenario traceability | 100% |
| Integration boundary coverage | 100% |
| Frontend behavior inventory | 100% |
| Critical E2E journey coverage | 100% |

Require zero skipped tests in every required suite.

Measure Unit production code with statement coverage, or the ecosystem's
closest production-code equivalent, per production package or module and for
changed code. Exclude generated code and generated mocks. Do not reclassify
business logic as an Adapter or execute it only through Integration or E2E to
evade the Unit denominator.

Require at least 90% coverage of added and modified production logic assigned
to the Unit layer without exception. Raise every touched Unit-tested production
package to at least 90% unless it satisfies the complete legacy exception below.

Do not represent Integration, BDD, frontend behavior, or E2E confidence with
line coverage. Compute them from passing required inventory pairs:

```text
behavioral coverage = passing required (item, profile) pairs
                      / all required (item, profile) pairs
```

A skipped test, wrong-layer mapping, missing profile, stale identity, or mapping
without an executable passing native-report item is uncovered.

## Permit Only Recorded Legacy Coverage Exceptions

Permit a touched Unit-tested package to remain below 90% only when its
pre-existing legacy code cannot be tested adequately without a large
production-architecture refactor. The exception never applies to added or
modified Unit-owned logic and never weakens an Integration, BDD, frontend, or
E2E mapping gate.

Require all of the following:

- package coverage does not decrease;
- all current-task behavior is tested;
- changed Unit-owned production code reaches at least 90%;
- the record states current coverage, uncovered behavior, architectural cause,
  refactoring direction, owner, and risk;
- refactoring work exists in the project's issue tracker or established
  Markdown debt file;
- the completion report links the exception and refactoring work.

Any completion statement that reports a Unit package below 90% must identify
this complete exception. No other coverage waiver exists.

## Verify Test Execution From Native Reports

Run source preflight before the suites. It produces the versioned expected-proof
artifact for every supported static declaration, keyed by proof layer, source
file, test identity, and stable proof identities. Source discovery establishes
expectation, never execution.

After every required suite runs, parse its native machine-readable report and
reconcile every expected item. Reject:

- an interrupted, missing, malformed, or empty report;
- an expected file or test identity absent from execution;
- pending, skipped, focused, quarantined, expected-failure, retried, or repeated
  required tests;
- mismatched total, passed, executable, and assertion counts;
- a report format that cannot expose required integrity metadata without an
  installed runtime integrity reporter.

The native report is authoritative for execution status. Static source text is
authoritative only for the expected inventory and mapping.

## Enforce Blocking CI Gates

Block every pull request on all applicable Unit, Integration, Contract, BDD,
coverage, architecture, frontend behavior, browser-quality, and Critical E2E
gates. A required gate cannot run only nightly. Run mutation, load, and long
pressure tests on a schedule or when their governed modules change materially.

Run the same declared commands locally and in CI. Regenerate inventories before
linting so a hand-edited denominator cannot substitute for production discovery.
Fail on focused tests, required skips, empty suites, unknown identities, stale
exceptions, missing profiles, wrong layers, invalid digests, or native-report
reconciliation failure.

Every custom static rule has positive fixtures and bypass-oriented negative
fixtures. Use the strongest native compiler, package-visibility, AST, type,
import-graph, runtime-report, or security mechanism available. Do not claim that
a name-based text scan proves aliases, computed access, framework construction,
or data flow it does not analyze.

## Apply The Quality-Gate Completion Gate

Reject completion when any of the following is true:

- added or modified Unit-owned production logic is below 90%;
- a touched Unit-tested package is below 90% without the complete recorded
  legacy exception;
- any BDD, Integration-boundary, frontend-behavior, stable-error, or Critical
  E2E inventory is below 100%;
- a required proof is stale, skipped, unmapped, in the wrong layer, or absent
  from a passing native report;
- an ecosystem lacks the proof adapter required to verify its declarations and
  native report;
- a required pull-request gate is nightly-only, retried into success,
  quarantined, weakened, suppressed, or empty;
- an inventory is not derived from authoritative production artifacts or its
  provenance is not mechanically enforced;
- an exception is incomplete, stale, manually added where forbidden, or used
  to waive added or modified behavior;
- a configured formatter, compiler, type checker, static analyzer, test,
  coverage, contract, generation, architecture, or build gate was skipped,
  weakened, or suppressed.
