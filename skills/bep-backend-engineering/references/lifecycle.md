# Service Lifecycle

Apply BEP preferences to new architecture. In an existing project, improve the affected boundary within its conventions; do not require unrelated restructuring.

## Own The Complete Service Lifecycle

At startup:

- read, parse, and validate configuration once;
- construct the dependency graph in the Composition Root;
- validate every critical dependency required for readiness;
- register background workers, connection pools, servers, and cleanup owners;
- fail startup when required configuration or invariants are invalid.

Define liveness as whether the process can make progress. Define readiness as
whether the instance may receive its intended traffic or work. Do not make
liveness depend on every transient external dependency and create restart
storms.

At shutdown:

1. mark the instance unready and stop accepting new requests or tasks;
2. cancel or drain in-flight work within an explicit deadline;
3. flush owned telemetry and durable work according to their guarantees;
4. close workers, pools, servers, and other resources in a defined order;
5. terminate with failure when safe shutdown cannot preserve required
   invariants.

For an optional dependency, define at design time whether its absence prevents
readiness, fails only the affected operation, or enables an explicit degraded
product mode. Do not discover that policy through an accidental catch block.
