# Behavior Specifications

For a new product, BEP favors lightweight `specs/**/*.feature` scenarios for
observable domain behavior. Pure libraries do not need product BDD. Keep specs
proportionate to real behavior; use them while defining product requirements,
not as paperwork for a mechanical edit.

For an existing project, preserve its specification format and test framework.
Do not introduce Gherkin, a BDD runner, or formal proof IDs merely to add a test.
When the project uses `.feature` files, update affected scenarios for changed
behavior and make their automated proof discoverable at the cheapest sufficient
layer. A scenario may be proven by ordinary native tests; no separate BDD runner
is required. Keep implementation details out of domain scenarios.

A behavior-preserving refactor does not need new scenarios. For a bug, add a
scenario only when product behavior was missing or ambiguous; otherwise link
the regression test to the existing behavior. Formal stable IDs, coverage
thresholds, and traceability lint belong to explicitly scoped verification
governance, not every specification change.
