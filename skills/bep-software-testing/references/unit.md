# Unit Testing

## Write Behavioral Unit Tests

Test a public module through its public contract. For a substitutable capability,
use in-memory Fakes and simple Stubs supplied with the Port or contract. Test
pure functions, immutable values, and UI components directly.

Assert returned values, state transitions, emitted domain facts, stable failure
categories, and observable UI behavior. Use interaction assertions only when
the interaction is itself the contract, such as charging exactly once,
publishing one event, or avoiding a forbidden write.

Keep private methods, implementation structure, pure internal collaborators,
and incidental call order out of assertions. Derive expected results from the
specification, worked examples, or another independent source rather than
reproducing the production algorithm in the test.

Inject time, random values, identifiers, and nondeterministic boundaries. Cover
normal behavior, meaningful error handling, and critical invariants.

Apply mutation testing periodically to critical pure business modules such as
money calculations, authorization rules, and state machines, or when those
modules change materially. Track mutation score separately from statement
coverage. Mutation testing is not a universal per-PR gate.
