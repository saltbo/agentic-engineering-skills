---
name: bep-production-verification
description: Prepare or execute regression checks against a deployed environment after release or on request. Not for local acceptance.
---

# Production Verification

A deployment task includes post-deployment regression, not just a successful
provider command. Verify the intended release and affected behavior plus relevant
critical journeys. This profile also applies to separately requested live checks;
local implementation alone does not authorize deployment or live side effects.

## Choose Automated Or Manual Regression

Inspect existing E2E selection and fixtures before running them live.

- If a production-safe subset exists, run it against the explicit target with
  the expected build and approved identity.
- If a small scoped change can make existing journeys portable, separate target,
  setup, identity, and cleanup; add explicit live selection, validate locally, then
  run the same assertions against the deployment. Use
  [suite design](references/suite-design.md) for this work.
- If safe conversion requires substantial unrelated work, or no suitable E2E
  exists, perform bounded manual regression with the available browser/API tools.
  Record each affected flow and relevant critical journey, expected result,
  observed result, and safe evidence. A health response alone does not prove a
  changed product journey. Report the specific automation gap for future work.

Do not create a second copy of the suite or skip regression because automation
is missing. When external access is unavailable, complete independent checks
and report the blocked live verification; never claim deployment is verified.

Reuse passing suite results as release evidence. Add manual probes for uncovered
behavior, ambiguous evidence, or a changed target; do not repeat the same version,
health, and journey checks merely to populate the final report.

## Execute And Close The Loop

Read [execution](references/execution.md) before any live automated or manual run.
Use the authorized target and identity, bounded operations, runner-owned state,
and verified cleanup. Anonymous checks do not require credentials. Automation
and manual regression have the same side-effect and evidence boundaries.

Do not repeatedly ask for authority already granted for the target and scope.
Deployment authorization includes ordinary read-only regression, but does not
implicitly authorize destructive, billed, messaging, or customer-data changes.

If regression fails, preserve evidence, diagnose and fix change-caused problems
within scope, validate locally, and redeploy/reverify when release authority
covers that action. Follow the project's rollback or roll-forward policy; pause
only the action needing missing authority or a consequential product decision.
Use the release plan's attempt/time budget, or choose a bounded recovery budget
proportionate to its risk. Continue evidence-based repair within that budget;
stop repeated deployment when the same failure recurs without new evidence,
a required decision is missing, or the recovery budget is exhausted.

Report target, intended and observed version, automated/manual flows exercised,
results, cleanup, and unverified risks. A failed or partial run remains failed or
partial. Recurring monitoring is a separate operational workflow.
