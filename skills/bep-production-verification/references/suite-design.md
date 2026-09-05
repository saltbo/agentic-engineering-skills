# Production Regression Suite Design

## Classify The Test Correctly

PVT describes where and when a test runs, not what proof layer it belongs to.
Keep every selected test classified by the real behavior and boundary it proves:

- an HTTP schema or discovery assertion remains Contract or Integration proof;
- an authenticated browser journey through the deployed stack remains E2E;
- a liveness request may be a smoke check without becoming E2E.

Do not create a `pvt` proof layer, duplicate BDD mappings, or count the same
behavior twice merely because it also runs against production. Distinguish PVT
from synthetic monitoring: PVT is normally a bounded release or operator-
triggered verification run, while synthetic monitoring is a recurring
operational signal with alerting and service-level ownership.

## Reuse One Behavioral Suite

Start by auditing the existing Contract, Integration, and E2E tests. Reuse the
same test bodies when their assertions describe environment-independent product
behavior. Isolate environment differences in runner configuration and fixtures:

- target origin and expected deployed version;
- authentication bootstrap and account selection;
- local service, database, or dependency startup;
- test selection, concurrency, timeouts, artifacts, and cleanup.

Give production-safe tests one explicit native tag, project, annotation, or
equivalent selector. Provide a separate, clearly named command that selects
that subset against an explicit deployment. Do not branch assertions on the
environment when the product contract should be identical. Allow an
environment-specific branch only for a real deployment property, such as HTTPS
cookie requirements or an artifact that exists only in a production build.

Do not force reuse when a local test's purpose requires database resets, direct
seeding, mocked dependencies, privileged setup, or destructive state changes.
Keep that test local and prove the corresponding live risk through a narrower
read-only or reversible production-safe behavior.

## Select Production-Safe Coverage

Keep the live subset small, deterministic, and valuable. Prefer behavior that
is read-only, idempotent, or completely reversible within a runner-owned scope.
Typical candidates include:

- liveness and readiness;
- deployed build or API-contract version;
- public configuration, discovery documents, and signing keys;
- anonymous authentication and authorization boundaries;
- sign-in, current-identity, session-cookie, and sign-out behavior;
- one or two critical read-only product journeys.

Exclude ordinary creation or mutation of customer, tenant, billing,
configuration, messaging, or other business resources. Include a write only
when the production check genuinely requires it, the user or release policy
authorizes it, the resource has a unique runner-owned namespace, cleanup is
reliable and verified, and abandoned state has an operational recovery path.

Do not put third-party identity providers, email or SMS delivery, payments, or
other externally billed or user-visible side effects in the default PVT subset.
Test owned protocol wiring without invoking the external side effect, or use a
separately authorized operational exercise.
