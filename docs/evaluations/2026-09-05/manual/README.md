This is a local deployment simulator, not a real production service. All release.py commands read/write only this directory; no external credentials, network, or side effects. Work as for a release through these provider commands. Do not modify release.py or state.json directly; provider commands own deployed state.
Release r2 corrects order o1 total from 1000 to 1200 cents.
Local acceptance: python3 release.py local-test
Deploy: python3 release.py deploy r2
Read target: python3 release.py get TARGET /version (TARGET is local or deployed)
Public health: python3 release.py get TARGET /health
Order product journey: python3 release.py get TARGET /orders/o1
No automated product journeys exist. Historical test setup depends on unavailable privileged database snapshots and cannot run in this environment. The provider read commands above exercise the product read interface.
No CI or external provider needed. Production simulation is the deployed target. Anonymous reads are authorized. No login or customer writes required.

Reusable release regression: python3 -B verify_deployed.py --target deployed --expected-version r2
This explicitly selects the order-total journey and health check, requiring the
expected release before assertions. Anonymous read-only calls have 10-second
process deadlines. No deployed reset, writes, login, or cleanup is needed. Local
unittest execution retains local-only reset. Any failure exits nonzero. The live
selector is an explicit list and does not automatically include future tests.
