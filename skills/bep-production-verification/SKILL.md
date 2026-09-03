---
name: bep-production-verification
description: Design, implement, run, or review production verification tests, post-deployment checks, production smoke tests, or another bounded verification profile against an already deployed environment. Do not use for hermetic local or CI testing.
---

# Production Verification

Apply these constraints when designing, implementing, running, or reviewing a
production verification test (PVT), post-deployment verification, production
smoke test, or another test profile aimed at an already deployed environment.

## Contents

- [Classify The Test Correctly](#classify-the-test-correctly)
- [Reuse One Behavioral Suite](#reuse-one-behavioral-suite)
- [Select Production-Safe Coverage](#select-production-safe-coverage)
- [Protect Identity And Secrets](#protect-identity-and-secrets)
- [Verify The Deployment](#verify-the-deployment)
- [Own Setup Cleanup And Evidence](#own-setup-cleanup-and-evidence)
- [Choose The Trigger Deliberately](#choose-the-trigger-deliberately)
- [Apply The PVT Completion Gate](#apply-the-pvt-completion-gate)

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

## Protect Identity And Secrets

Use a dedicated least-privilege test identity. Provision and verify the account
outside the ordinary PVT run unless safe account creation is itself the approved
behavior under test. Assert that authenticated responses identify the expected
account so a stale or borrowed session cannot produce a false pass.

Load credentials from a secret manager or a repository-ignored local
environment file. Require them explicitly and fail before opening a browser or
calling production when they are absent. Never place secrets in source,
committed fixtures, command-line arguments, URLs, logs, screenshots, traces, or
ordinary failure messages.

When production bot protection requires a human challenge, let the operator
complete it in a real, visibly controlled browser. Do not bypass, solve, or
weaken CAPTCHA or bot protection. Reuse only the short-lived session created for
the current run and keep its browser profile or storage state in a runner-owned
temporary location.

## Verify The Deployment

Require an explicit remote target and reject ambiguous, local, or insecure
origins unless the deployment policy intentionally permits them. Require the
expected release or contract version independently from the deployed response;
checking only that a version field exists cannot detect an old deployment.

Derive assertions from supported product and protocol contracts. Verify stable
fields and invariants rather than timestamps, generated prose, request IDs, or
provider-specific noise. Include both successful wiring and at least one
meaningful access boundary. For authenticated systems, verify session creation,
the expected identity, required cookie or token protections, and session
invalidation after sign-out when those risks apply.

Use no retries, fixed sleeps, or broad catch-and-continue behavior to manufacture
a pass. Give live calls and operator interaction explicit deadlines that reflect
their different failure modes. Report the failing operation and safe response
metadata without exposing credentials or response bodies by default.

## Own Setup Cleanup And Evidence

The runner owns every session, temporary file, browser profile, token, and live
resource it creates. Register cleanup for success and failure, revoke temporary
sessions or tokens, remove local authentication state, and verify important
revocations by attempting the previously authorized operation again.

Treat production evidence as sensitive. Prefer a concise native report. Disable
screenshots, traces, videos, and verbose HTTP bodies when they can capture
credentials or private production data; otherwise redact them before
persistence and apply a short explicit retention period. This production rule
takes precedence over ordinary E2E failure-artifact collection.

Return a nonzero result for any failed assertion, incomplete setup, failed
cleanup invariant, or missing expected test. Never convert a partial run into a
successful production verification.

## Choose The Trigger Deliberately

Provide a manual command when operator-controlled execution is sufficient. Do
not require CI merely because the suite is automated. Keep the command usable
outside CI and document its required target, identity, expected version, human
interaction, side effects, cleanup, and result semantics.

When release policy makes PVT a promotion gate, run the same declared command
after deployment and block promotion or rollback decisions on its result. A
recurring request belongs to synthetic monitoring or an operational probe, not
an indefinitely running PVT command.

## Apply The PVT Completion Gate

Reject the PVT design or implementation when any of the following is true:

- it duplicates test bodies instead of isolating environment setup and selection;
- it reclassifies PVT as a proof layer or duplicates behavioral coverage counts;
- production-safe selection is implicit, broad, destructive, or unauditable;
- the target, expected version, identity, privileges, or side effects are ambiguous;
- secrets or private production data can enter source, arguments, logs, or artifacts;
- operator CAPTCHA is bypassed or an unrelated user browser session is borrowed;
- runner-created sessions, files, profiles, tokens, or resources lack verified cleanup;
- a failed, partial, skipped, retried, or cleanup-incomplete run can report success;
- the chosen manual, release-gated, or recurring trigger does not match the stated operational purpose.
