# Critical E2E Journeys

When designing runner or fixtures, read [live-e2e.md](live-e2e.md) so a selected
subset can also verify deployments. Keep the local default isolated.

## Prove Critical Journeys With E2E

An E2E test exercises the real shipped entry point and application stack for
one user-observable journey. For a web app this includes frontend, backend,
router, applicable authorization, and storage; for a CLI or API product use its
actual user entry point rather than inventing a browser frontend. Reserve E2E for
journeys involving at least one of these risks:

- authentication, session continuity, permissions, or tenant isolation;
- onboarding, initialization, or first successful product use;
- the product's core create, submit, or completion flow;
- money, irreversible action, sensitive data, or realistic data-loss risk;
- a serious historical cross-stack regression.

Mark each required journey with a stable `critical` classification. Adding,
removing, or weakening that classification changes the verification
specification and requires deliberate review.

Exercise the behavior the journey exists to prove. Frontend mocks or direct
backend setup cannot replace authentication, permission, persistence, or
cross-stack behavior inside that journey.

Fix E2E races, readiness signals, selectors, and environment isolation. Required
journeys may not rely on runner retries, quarantine, fixed sleeps, or skips.
Full execution may remain primarily in CI when slow, but the same bootstrap and
command must be available locally.

## Keep Tests Deterministic And Isolated

Hermetic test suites must not depend on execution order, wall-clock time,
uncontrolled random values, public network access, fixed sleeps, default
development ports, or residue from another test. A separately selected PVT may
depend on its explicit live target under the production-verification rules.
Inject clocks, random generators, and identifiers. Seed randomized tests and
print the seed on failure. Wait on observable readiness or state.

Reset or uniquely isolate databases, queues, caches, files, accounts, browser
state, and namespaces. Parallelize by isolation. Run a suite serially only when
a real global resource cannot be isolated, and record the resource and reason
beside the runner configuration.

Every hermetic local or CI E2E run must:

- dynamically allocate ports;
- create unique temporary configuration and state locations;
- migrate and initialize from a clean starting point through the CI bootstrap;
- register cleanup for success and failure after diagnostic evidence is saved.

Never share ordinary local-development configuration or persistent state with
E2E.

## Capture E2E Failure Evidence

Before cleanup, preserve:

- browser trace, screenshots, console output, and network failure summary;
- structured server and worker boundary logs;
- request, correlation, and Trace identities;
- native test report, random seed, and isolated-environment identifiers.

Publish the evidence as CI artifacts with an explicit retention policy. Redact
credentials, tokens, sensitive bodies, and personal data. Do not upload a full
database snapshot by default.
