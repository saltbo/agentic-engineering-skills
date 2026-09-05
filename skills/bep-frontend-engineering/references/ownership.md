# Frontend Ownership And State

Use these preferences for new work. Preserve existing architecture and supported behavior unless the task includes changing them. Apply checks to the affected capability; formal project-wide CI governance is a separate task.

## Organize By Business Capability

Use business features or domains as the primary frontend module boundary. A
growing application should normally make these ownership roles visible:

```text
src/
  app/                 composition, providers, router, shell
  routes/              thin route entry adapters
  features/<feature>/  UI, model, query/mutation definitions, tests, public API
  shared/
    api/                typed transport and generated contract boundary
    config/             validated public runtime configuration
    observability/      browser telemetry boundary
    persistence/        versioned browser-storage adapters
    ui/                 design-system primitives and semantic components
    lib/                genuinely stable cross-feature utilities
```

Adapt names to the framework and repository, but preserve the ownership:

- `app` owns composition and may depend on routes, features, and shared modules;
- a route parses navigation state and composes feature public APIs; it does not
  own business rules or reusable feature behavior;
- a feature owns one coherent business capability, including its UI, client
  workflow state, remote-operation definitions, and colocated Unit tests;
- `shared` owns only stable cross-feature infrastructure or semantics and never
  imports app, routes, or features.

Do not create global `components`, `hooks`, `services`, or `stores` directories
that mix unrelated capabilities. A technical subdirectory inside one feature
is acceptable when it clarifies that feature. Keep code in its owning feature
until the cross-feature semantics are real and stable; do not promote code to
`shared` merely because two implementations look similar.

## Keep Feature Dependencies Public

Give every feature a small explicit public entry point. Another feature may
depend only on that entry point, never on internal components, hooks, query
keys, stores, or generated files. Export named capabilities deliberately; do
not use recursive wildcard barrels that conceal ownership or pull unnecessary
runtime code into a bundle.

Reject circular feature dependencies. Resolve them by:

1. moving composition to `app` or a route;
2. extracting a genuinely shared stable concept; or
3. correcting a feature boundary that combines the wrong responsibilities.

Do not solve a cycle by deep-importing internals or moving feature-specific code
into a generic shared directory. Routes may compose feature public APIs; shared
modules and low-level visual components must not import features. Features must
not import app or routes.

For new architecture, make these ownership directions explicit. In an existing
project, use its equivalent boundaries rather than imposing this directory model.
When architecture enforcement is in scope, use import-graph or AST linting;
ordinary feature work does not require building a new blocking CI system.

## Give Every State One Owner

Classify state by ownership before choosing a library:

- put shareable navigation state such as route, search, filter, sort, page, tab,
  and selected resource identity in the URL when practical;
- treat fetched data as server state and let the established query cache or
  framework loader own freshness, deduplication, cancellation, and invalidation;
- keep transient interaction state local to the smallest component subtree that
  owns it;
- use a feature-scoped reducer or explicit state machine when asynchronous or
  multi-step behavior can otherwise enter impossible boolean combinations;
- introduce a global client-state store only for stable state whose ownership
  genuinely crosses feature boundaries and cannot remain in URL, server cache,
  composition context, or a smaller subtree.

Never copy a query response into an unrelated Store, synchronize duplicate
representations with Effects, or keep server-owned permissions and workflow
truth as authoritative browser state. Derive values during rendering. Preserve
back, forward, reload, and deep-link behavior for URL-owned state.
Never put credentials, sensitive personal data, or other confidential state in
the URL merely to make it shareable.

## Keep The Server Authoritative

The server is the final authority for business invariants, authorization,
money, inventory, durable workflow transitions, and conflicts. Frontend checks
may improve responsiveness but do not replace server enforcement.

Reuse one contract schema or generated representation when client and server
perform the same input validation. Keep client-only interaction rules, display
formatting, and workflow presentation in the feature. Do not maintain an
independent authoritative copy of server business rules or treat hidden and
disabled controls as authorization.

Share a complete domain implementation between client and server only when the
same deterministic domain truly executes in both runtimes and the resulting
release coupling is intentional. Do not introduce a shared domain package just
to avoid a few validation lines.

## Keep Effects At External Boundaries

Treat an Effect as synchronization with an external system, not as a general
control-flow mechanism. Valid owners include a browser subscription, media API,
imperative third-party widget, or another resource whose lifetime follows the
component.

- derive render values during rendering rather than setting derived state in an
  Effect;
- perform user-triggered work in the event handler or feature operation;
- let the router or query layer own remote-data lifecycles;
- cancel or ignore obsolete external work through the boundary's explicit
  cancellation contract;
- make setup and cleanup symmetrical and safe under development remounting.

Moving a convoluted Effect into a custom hook does not correct its ownership.
Fix the data model or event boundary. Do not suppress exhaustive-dependency or
equivalent lifecycle lint without a documented external-system reason.
