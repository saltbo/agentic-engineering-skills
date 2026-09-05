# Live Verification Execution

## Protect Identity And Secrets

For authenticated checks, use a dedicated least-privilege test identity through
the environment's approved agent/delegation mechanism. Follow existing identity
policy and reuse already granted authority; never silently switch to user credentials.
Anonymous checks require no test account or credential.

Provision and verify the account
outside the ordinary PVT run unless safe account creation is itself the approved
behavior under test. Assert that authenticated responses identify the expected
account so a stale or borrowed session cannot produce a false pass.

Resolve any required credentials through the approved identity flow. Use a secret
manager or ignored local environment file only when that credential source is
authorized. If authority is missing, pause authenticated checks while continuing
independent public checks; do not claim the authenticated subset passed.
Never place secrets in source,
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
provider-specific noise. Include successful wiring and meaningful access-boundary
checks when the affected capability has an access boundary. For authenticated
systems, verify session creation,
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

Treat production evidence as sensitive. Prefer a concise native report for
automation, or expected/observed results and safe evidence for manual checks. Disable
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
