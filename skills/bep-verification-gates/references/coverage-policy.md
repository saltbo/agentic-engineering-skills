# BEP Coverage Policy

Apply this protocol only to the governed scope. For new governance use BEP defaults; for an existing project preserve its declared policy unless this task authorizes a transition.

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
