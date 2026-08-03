# Technology-Independent Engineering Constraints

Enforce these constraints across languages and frameworks. Express them through
the target platform's native mechanisms; do not force one language's syntax or
error model onto another.

## Contents

- [Apply The Rules By Authority](#apply-the-rules-by-authority)
- [Start From Observable Behavior](#start-from-observable-behavior)
- [Handle Failure Explicitly](#handle-failure-explicitly)
- [Unify Observability At Execution Boundaries](#unify-observability-at-execution-boundaries)
- [Make Simplicity A Design Constraint](#make-simplicity-a-design-constraint)
- [Define Public Modules For Consumers](#define-public-modules-for-consumers)
- [Keep Dependencies And State Explicit](#keep-dependencies-and-state-explicit)
- [Require Executable Proof](#require-executable-proof)
- [Diagnose Before Fixing](#diagnose-before-fixing)
- [Version Compatibility Deliberately](#version-compatibility-deliberately)
- [Protect Security Data And Runtime Boundaries](#protect-security-data-and-runtime-boundaries)
- [Record And Review Decisions](#record-and-review-decisions)
- [Complete Repository-Wide Corrections](#complete-repository-wide-corrections)
- [Apply The Completion Gate](#apply-the-completion-gate)
- [Influence](#influence)

## Apply The Rules By Authority

Treat the explicit user outcome and scope plus supported public contracts as the
task authority. Invoking this skill makes the Core authoritative within that
scope. A requested mechanism, repository convention, or existing pattern does
not implicitly waive a Core rule.

A later user instruction may authorize a deviation only by naming the Core rule
and accepting the resulting unmet gate. The deviation never becomes compliant
completion. Secret exposure and falsified verification evidence are never
authorizable.

Treat the following as non-negotiable:

- surface every failure explicitly;
- never swallow, downgrade, or disguise an error as success;
- never invent an unrequested fallback or defensive path;
- keep diagnostic logging at execution boundaries;
- keep dependencies, state ownership, and concurrency lifecycles explicit;
- prove changed behavior and meet the coverage and configured quality gates;
- preserve the compatibility promise of supported releases;
- never leak credentials or secrets;
- do not copy an existing pattern that violates these rules.

When a repository already contains a violating pattern, correct the pattern
repository-wide. Do not preserve inconsistency merely to keep the current diff
small.

Solve the same problem through one project-wide pattern. Follow an existing
Core-compliant pattern. When introducing a better replacement, migrate every
instance instead of leaving multiple competing but individually valid patterns.

## Start From Observable Behavior

- Define success in terms a user, caller, operator, or downstream system can
  observe.
- Identify the command or evidence that proves completion before expanding the
  implementation.
- Read the originating requirement, existing behavior, contracts, and release
  baseline before changing code.
- Separate the required capability from a mechanism suggested in the request.
- Clarify and record decisions before changing a hard-to-reverse interface or
  data model. Keep documentation proportional for simple reversible work.
- Work in vertical slices: one behavior, its implementation, and its proof.
  Never build all types, then all handlers, then all tests as horizontal batches.

## Handle Failure Explicitly

Classify predictable failures as errors and unexpected failures as exceptions
or fatal invariant violations, using the platform's native model.

For errors:

- check every returned failure at the call site;
- return immediately when the current layer cannot resolve it;
- preserve the original cause while adding only useful operation context;
- expose a stable type, code, or error chain for programmatic decisions;
- never parse error text to choose control flow, protocol status, or retry;
- keep domain error meaning independent from HTTP or another transport;
- translate domain errors into protocol responses only at the transport boundary.

For retries:

- mark only transient failures as retryable;
- never retry validation, authorization, deterministic conflict, or programming
  failures;
- retry only at the boundary that owns the full operation semantics;
- require idempotency, a finite attempt limit, backoff, jitter, and an overall
  deadline;
- return classification from internal modules instead of retrying there.

For unexpected failures:

- recover only at a request, job, process, or declared UI execution boundary;
- in a browser, scope recovery to the application, navigation, independently
  recoverable render subtree, or event boundary that owns the failed work;
- capture the complete cause, stack, and trace context;
- fail the current execution instead of converting the exception into a normal
  internal error;
- terminate or rethrow when shared state, data consistency, or process
  invariants may be damaged.

Allow a fallback, failover, or degraded mode only when it is an explicit product
or architecture behavior with defined semantics, tests, observability, and a
recovery condition. Otherwise fail immediately.

Validate untrusted input at real system boundaries. Inside a trusted boundary,
rely on established invariants. Do not add redundant null checks, catch blocks,
defaults, recovery, or branches to make impossible state appear valid.

## Unify Observability At Execution Boundaries

Use structured logs with stable field names. Do not depend on prose messages for
querying, aggregation, or alerting.

For synchronous requests:

- record the access event once in framework-level request middleware;
- record method, route template, status, duration, sizes, principal context,
  authentication method, request or trace identifiers, and error classification
  when available;
- record useful allowlisted headers or derived attributes, never credentials;
- do not record request or response bodies by default;
- allow body logging at Debug level according to project policy.

For asynchronous work:

- keep all permanent logging in the task execution entry boundary;
- emit one structured completion event per attempt with result or failure and
  duration;
- emit a distinct start event only when long-running work needs an operational
  progress signal, and make that event an explicit tested part of the task's
  observability contract;
- propagate the originating Request ID or Trace ID when one exists;
- start a new root trace for scheduled work;
- allow sparse Debug diagnostics at meaningful internal positions, disabled by
  default;
- never scatter permanent INFO or ERROR statements through business modules.

Do not log an error at each layer. Return it to the execution boundary and log
it once with the full error chain and execution context.

Separate telemetry responsibilities:

- use low-cardinality Metrics for aggregation, trends, SLOs, and actionable
  alerts; never label Metrics with request, user, or resource identifiers;
- use Traces for causal flow across modules, dependencies, and asynchronous work;
- use Logs for structured execution context;
- alert on user-visible failure, SLO breach, or saturation rather than the mere
  existence of one error log.

Generate common audit events in centralized middleware from canonical resource
operations. Audit all resource writes and every successful or failed
security-sensitive operation. Audit ordinary reads only for sensitive resources
or compliance requirements. Record actor, resource identity, operation, result,
time, Trace ID, and changed field names without copying full bodies. Emit an
explicit business audit event only when middleware cannot derive it, and route
it through the same audit schema and sink.

## Make Simplicity A Design Constraint

- Choose the simplest design that satisfies the current requirement.
- Prefer readable control flow over clever expressions and compressed one-liners.
- Step back when logic becomes convoluted. Inspect the data structure, domain
  model, and responsibility split before adding another conditional or helper.
- Restructure an incorrect or outdated internal data model without hesitation
  when it removes root complexity. Preserve released behavior and migrate
  persisted data safely.
- Prefer a small public interface with a cohesive, deep implementation.
- Treat a responsibility as one complete, nameable reason to change, not one
  line or one call. Do not split functions or files to satisfy a size metric.
- Organize modules by domain or business capability. Keep technical details
  inside their owning domain module when practical.
- Reject vague `common`, `utils`, or `helpers` containers. Every shared module
  must own a stable, nameable capability.
- Permit short-lived surface duplication when similar code has different
  meaning. Centralize the rule when duplicated code represents one business
  concept that must change together.
- Name functions, variables, types, tests, logs, and documents with the same
  precise domain vocabulary. Rename aggressively when understanding improves.
- Use comments to preserve why a surprising choice exists, never to narrate
  obvious code.
- Delete dead code, obsolete branches, unused parameters, vestigial abstractions,
  and replaced implementations. Do not polish what should not exist.

## Define Public Modules For Consumers

For every substitutable cross-module capability consumed by business code,
provide together:

1. one cohesive canonical contract;
2. the production implementation;
3. a contract-owner-provided mock or fake capability.

The capability normally owns its public contract and test double. Dependency
inversion changes that ownership: an inner business module owns the outward
Port it needs and its test double, while an outer Adapter provides the
production implementation. Do not let an infrastructure provider dictate an
inner business contract.

Keep callers on the canonical contract. If callers repeatedly need only
unrelated subsets, split the owning module and its contract instead of creating
competing caller-local views. A deliberately narrow outward Port is not such a
duplicate; it is the inner caller's owned business requirement.

Keep internal implementation types concrete. Test exported pure functions,
immutable values, declarative UI components, and other directly executable
values without manufacturing an interface or fake. Introduce another interface
when the implementation is a substitutable cross-module capability or a real
external seam, not merely because it is exported.

Do not prescribe a fixed Controller-Service-Repository layer count. Enforce
clear ownership and dependency direction instead:

- keep protocol parsing and response mapping at the transport boundary;
- keep business rules in their owning domain module;
- keep persistence and external-system details in infrastructure implementations;
- keep domain rules independent from Web-framework and datastore details;
- delete layers whose only behavior is forwarding the same parameters and result.

## Keep Dependencies And State Explicit

- Pass databases, clients, clocks, configuration, and other dependencies through
  constructors or explicit parameters. Never hide them in mutable global state.
- Permit immutable constants and genuinely stateless shared objects.
- Prefer immutable values and explicit data flow. When mutation is necessary,
  assign one owner and keep its scope small and visible.
- Read and validate configuration once at process startup. Convert it to typed,
  immutable values and inject it. Fail startup for missing or invalid required
  configuration. Never scatter environment reads through business code.
- Prefer the standard library when it provides a reliable solution.
- Use mature community libraries for standards, protocols, cryptography,
  authentication, established algorithms, and pervasive language boilerplate.
  Do not reimplement OAuth, OIDC, cryptography, or similar standards.
- Keep simple stable domain logic local. Do not add a micro-dependency for a few
  trivial operations.
- Use a mature ecosystem utility library instead of growing an internal utility
  package that duplicates it.
- Evaluate maintenance, stability, license, security history, and transitive
  dependency risk before adding a library.

## Require Executable Proof

Map every changed observable behavior to executable proof at the cheapest layer
that proves it completely. Prove real transports, persistence, external
Adapters, Consumers, migrations, browser boundaries, and cross-stack journeys
through their actual semantics rather than line coverage or internal mocks.

Apply every verification reference selected by `SKILL.md`. Treat its inventory,
coverage, native-report, exception, architecture, browser, and CI requirements
as independent blocking gates. A mapping, source declaration, coverage estimate,
or prose review is never a substitute for an executable passing native report.

Run every configured formatter, compiler, type checker, static analyzer, test,
coverage gate, contract validator, generator check, architecture gate, and build.
Fix the code or an actually incorrect rule. Never skip a check, suppress a valid
finding, lower a threshold, or edit configuration merely to manufacture success.

## Diagnose Before Fixing

For a bug or regression:

1. Build one fast, deterministic, agent-runnable command that detects the user's
   exact symptom.
2. Minimize the scenario until every remaining element is load-bearing.
3. Generate three to five ranked, falsifiable hypotheses.
4. Change one variable or add one targeted probe for each hypothesis.
5. Convert the minimal reproduction into a failing test at the correct public
   seam.
6. Apply the smallest causal fix.
7. Rerun the regression test and the original unminimized reproduction.
8. Remove temporary instrumentation and record the actual cause.

Measure a performance baseline with profiles, traces, query plans, or metrics
before optimizing. Block structurally unbounded queries, concurrency, fan-out,
memory growth, collection size, and per-item dependency calls without waiting
for production damage.

## Version Compatibility Deliberately

Determine compatibility against every published version still covered by a
support promise, not an earlier state of the current unreleased branch.

For unreleased behavior:

- make breaking design improvements directly;
- update all current callers, tests, and documentation;
- migrate existing development data to the new canonical form;
- keep runtime code clean instead of retaining compatibility branches.

For published and supported behavior:

- apply Semantic Versioning to versioned software artifacts;
- permit an explicitly defined protocol version system for APIs, events, and
  other wire contracts;
- preserve compatibility inside one supported version;
- introduce a breaking contract only through the version system with consumer,
  migration, coexistence, and recovery analysis.

Give every compatibility path a supported version range, old and new behavior
tests, usage telemetry, deprecation notice, removal condition, and owner. Delete
it when the support window or breaking-version transition ends. Never leave a
permanent fallback.

For live data and rolling deployments, permit a temporary
expand-migrate/backfill-switch-contract sequence. Make each stage observable,
rerunnable where appropriate, and recoverable. Delete dual reads, dual writes,
old fields, and old branches when migration completes.

Use Conventional Commits for every commit. Mark breaking changes with `!` or a
`BREAKING CHANGE` footer. Make every commit one coherent logical change and make
its message explain why the change exists. Never mix unrelated behavior,
refactoring, formatting, or generated output. Keep generated artifacts with the
source change when they are part of that same logical change.

Lock dependency and critical tool versions. Make code generation and builds
deterministic from a clean environment through declared commands shared by
local development and CI. Derive versions, changelogs, and release notes from
the commit history when practical. Publish immutable tags and traceable build
artifacts.

Define a rollback or prepared roll-forward path before production release. Give
every temporary feature flag an owner, observation plan, and deletion condition.

## Protect Security Data And Runtime Boundaries

- Authenticate at the execution boundary and produce a normalized immutable
  principal. Authorize separately against the resource, operation, ownership,
  tenant, state, and requested fields. Never let business code parse raw tokens
  or claims.
- Never put credentials, tokens, passwords, private keys, or secrets in source,
  version control, URLs, ordinary logs, or error responses. Inject them through
  the approved secret boundary with least privilege and rotation support. Treat
  accidental exposure as a security incident.
- Propagate cancellation, deadline, and Trace context through the complete
  synchronous call chain. Never replace an active caller context with a detached
  background context.
- Move work that must outlive a request into an explicit asynchronous task with
  its own lifecycle while preserving the correlation or Trace relationship.
- Give every potentially blocking network, process, queue, or external call an
  explicit timeout or deadline. Derive the budget from the operation objective
  and remaining time, not an arbitrary infinite default.
- Give every thread, coroutine, goroutine, or asynchronous task an owner,
  cancellation path, error propagation, join or cleanup behavior, and concurrency
  bound. Prohibit fire-and-forget work. Apply the platform's race detection when
  shared state or concurrency changes.
- Enforce critical data invariants in one authoritative place. Use transactions,
  atomic operations, and datastore constraints for guarantees the datastore can
  provide. Treat application prechecks as user-experience improvements, never as
  substitutes for the final constraint.

## Record And Review Decisions

- Keep public contracts, operating procedures, and critical failure handling
  documented alongside the system they govern.
- Create an Architecture Decision Record only when the decision is hard to
  reverse, surprising without context, and the result of a real trade-off.
- Record context, the decision, alternatives, consequences, and status. Preserve
  history by superseding an ADR instead of rewriting the old decision.
- Avoid documentation that merely restates code or will immediately drift.

A change is mechanical only when it cannot alter compiled behavior, runtime
behavior, stored data, generated contracts, public output, dependency
resolution, or execution order. Everything else is non-mechanical.

Before completing a non-mechanical change, run two independent reviews in
distinct reviewer or Sub-agent contexts isolated from the implementation
reasoning and from each other's initial findings:

1. **Outcome review:** compare the diff with the requirement and supported
   contracts; find omissions, wrong behavior, and scope creep.
2. **Engineering review:** enforce this Core and project standards; inspect
   errors, observability, tests, coverage, ownership, dependencies,
   compatibility, security, performance, and operability.

Verify every finding against the code, fix valid findings, and rerun affected
checks. Permit a mechanical rename, formatting-only change, or deterministic
generation update to skip independent review when behavior cannot change.
When independent reviewer capability is unavailable, do not silently omit the
reviews or claim full compliance. Run the two review axes separately, report the
missing independence, and leave the independent-review gate explicitly unmet.

## Complete Repository-Wide Corrections

For an authorized change task, keep the main workstream focused on its requested
outcome, but do not preserve a known Core violation or competing project pattern
for the sake of a small diff. For a read-only plan, diagnosis, or review, report
the required repository-wide correction without mutating the repository.

When authorized change work encounters an existing violating or competing
pattern:

1. stop adding new instances;
2. define the one correct replacement pattern;
3. keep the main Agent on the requested feature;
4. delegate repository-wide migration when independent workers are available,
   otherwise complete it in the main context;
5. review all delegated changes and run affected repository gates;
6. complete with one consistent pattern.

Do not ask for authorization merely because this internal cleanup is broad,
slow, or requires a better internal data model. Do not silently alter supported
public behavior. Use the versioning and migration rules when correction crosses
a published contract or persisted-data boundary.

## Apply The Completion Gate

Reject completion when any of the following is true:

- the requested outcome lacks observable proof;
- an error is swallowed, downgraded, logged repeatedly, or disguised as success;
- an unrequested fallback or redundant internal defense exists;
- diagnostic logs are scattered outside execution boundaries;
- a substitutable cross-module capability lacks its canonical contract,
  production implementation, contract-owner-provided mock or fake, or
  behavioral tests;
- an applicable loaded verification or configured repository gate remains
  unmet, skipped, weakened, or suppressed;
- business rules or mutable state have multiple owners;
- a concurrency task lacks a lifecycle or an external call lacks a time budget;
- a supported contract breaks outside its version and migration policy;
- a temporary compatibility path, migration branch, or feature flag lacks an
  exit condition;
- secrets can enter source, logs, URLs, or ordinary errors;
- outcome or engineering review has unresolved valid findings;
- the repository contains both the corrected pattern and the known violating
  pattern after the task;
- the same problem remains implemented through competing project patterns.

## Influence

The feedback-loop, vertical-slice, deep-module, seam, behavior-testing,
diagnosis, and two-axis review ideas were adapted and reorganized from Matt
Pocock's MIT-licensed [`skills`](https://github.com/mattpocock/skills)
repository, copyright 2026 Matt Pocock. The enforcement model and combined
constraints here reflect the preferences established for this skill.
