# Blocking CI

Apply this protocol only to the governed scope. For new governance use BEP defaults; for an existing project preserve its declared policy unless this task authorizes a transition.

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
