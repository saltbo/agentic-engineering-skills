# E2E Across Local And Deployed Environments

When designing or changing E2E infrastructure, consider post-deployment regression
from the start. Keep environment-independent assertions in one suite. Inject the
target origin, expected build, authorized identity, setup, selection, and cleanup
through runner projects or fixtures, not divergent copies of test bodies.

The local default starts isolated dependencies, uses disposable state, and never
contacts production. A separate explicit live command selects only tests whose
setup, assertions, and cleanup are suitable for the deployed environment. Selection
must not silently expand when a new ordinary E2E test is added.

Reuse critical read journeys and reversible writes in a runner-owned scope.
Keep database resets, direct production seeding, destructive customer operations,
and billed or user-visible external side effects out of the default live subset.
Authenticate through the approved identity mechanism. Test identities must not
bypass the product boundary a journey claims to prove.

For an existing suite, inspect its suitability before reuse. If a small adapter,
fixture separation, or explicit selector enables safe live execution within the
deployment task, implement and validate it locally. Do not run a local bootstrap
against production. If conversion needs substantial architecture work or unavailable
authority, use bounded manual regression for the current release and report the
specific automation gap. Do not skip regression merely because automation is absent.

Use `$bep-production-verification` when actually preparing or executing the live
regression. A live run supplements the same journey's local proof by checking the
deployment; it is not a new proof layer or a reason to duplicate the test pyramid.
Deployment completion requires affected behavior and relevant critical journeys,
not necessarily every feature in the product.
