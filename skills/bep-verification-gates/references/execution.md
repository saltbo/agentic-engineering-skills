# Native Execution Evidence

Apply this protocol only to the governed scope. For new governance use BEP defaults; for an existing project preserve its declared policy unless this task authorizes a transition.

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
