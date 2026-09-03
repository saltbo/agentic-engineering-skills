# Frontend Engineering Constraints

Apply this reference to browser UI, client state, frontend routing, rendering,
styling, accessibility, browser security, frontend observability, or client
performance. This reference defines frontend runtime ownership without copying
backend Clean Architecture. Use the verification profile in this skill only
when formal runtime proof is in scope.

## Contents

- [Organize By Business Capability](#organize-by-business-capability)
- [Keep Feature Dependencies Public](#keep-feature-dependencies-public)
- [Give Every State One Owner](#give-every-state-one-owner)
- [Keep The Server Authoritative](#keep-the-server-authoritative)
- [Put Remote Access At A Feature Boundary](#put-remote-access-at-a-feature-boundary)
- [Validate Every Runtime Boundary](#validate-every-runtime-boundary)
- [Model Rendering And Failure Deliberately](#model-rendering-and-failure-deliberately)
- [Keep Effects At External Boundaries](#keep-effects-at-external-boundaries)
- [Build Coherent Components And Forms](#build-coherent-components-and-forms)
- [Make Accessibility A Release Gate](#make-accessibility-a-release-gate)
- [Secure Browser Identity And Script Execution](#secure-browser-identity-and-script-execution)
- [Version Durable Browser Data](#version-durable-browser-data)
- [Treat Offline Behavior As A Product Capability](#treat-offline-behavior-as-a-product-capability)
- [Observe The Browser At Boundaries](#observe-the-browser-at-boundaries)
- [Choose Rendering And Compatibility Deliberately](#choose-rendering-and-compatibility-deliberately)
- [Enforce Performance And Visual Quality](#enforce-performance-and-visual-quality)
- [Apply The Frontend Completion Gate](#apply-the-frontend-completion-gate)

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

Enforce these directions and public-entry rules with import-graph or AST linting
in blocking CI. Repository convention may rename directories but may not remove
the dependency constraints.

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

## Put Remote Access At A Feature Boundary

Use one authoritative protocol source such as OpenAPI, an RPC schema, or another
versioned contract to produce the typed client, wire types, and runtime schemas
that the protocol can provide. Keep generated files isolated and never edit
them. Do not hand-copy paths, DTOs, status codes, or error categories into
features.

Keep a small environment-specific transport boundary in `shared/api` or its
repository equivalent. It owns base URL, correlation, credentials, decoding,
and protocol-level error normalization. A feature owns its query and mutation
definitions, cache keys, freshness policy, invalidation, stable error mapping,
and user-visible reconciliation. A route or page composes those definitions.
Presentational components receive data and emit semantic events; they do not
call `fetch`, an RPC client, or a query cache directly.

Do not mechanically reproduce backend Repository, Use Case, Port, and Adapter
layers for ordinary frontend CRUD. Introduce a dependency-free client domain or
application module only for substantial browser-owned behavior such as an
editor, local workflow, offline engine, or complex deterministic state machine.

Every query declares its freshness and invalidation semantics. Every mutation
declares duplicate-submission, conflict, cancellation, and uncertain-result
behavior. Default to server-confirmed updates. Use optimistic updates only for
low-risk reversible operations with explicit rollback and authoritative
resynchronization. Never display an uncertain write as confirmed success.

## Validate Every Runtime Boundary

TypeScript proves compile-time relationships, not runtime data. Decode and
validate untrusted values before they enter a feature:

- API and streaming responses;
- URL path, query, fragment, and navigation state;
- local storage, session storage, IndexedDB, cache, and imported files;
- `postMessage`, BroadcastChannel, Service Worker, extension, and third-party
  script events;
- public runtime configuration and server-rendered bootstrap data.

Prefer a schema derived from the protocol's authoritative contract. Treat the
decoded value as a new trusted value; do not spread `unknown` data into a typed
object. Reject `as`, non-null assertions, silent defaults, or fallback parsing
used only to bypass a failed boundary check. A schema mismatch is an explicit
contract failure and enters the unexpected-failure observability path.

## Model Rendering And Failure Deliberately

Design applicable success, initial loading, background refresh, empty, stale,
partial, validation, authentication, authorization, conflict, offline,
uncertain-result, and unexpected-failure states with the feature. Do not add
them as generic spinners and error pages after implementation.

- keep usable content visible during background refresh when its age and stale
  state are explicit and safe;
- place field validation next to the field and actionable operation failure next
  to the operation;
- use a route or content-region failure state for failed loading while keeping
  unaffected content usable;
- preserve input after recoverable failure and move focus to useful feedback;
- prevent duplicate submission while allowing a deliberate retry after the
  previous outcome is known;
- size confirmation and undo behavior to the consequence of destructive work.

Use Toast only for a result with no natural persistent location, such as a
background action completed after its initiating surface disappeared. Do not
make Toast the default error channel. Use Error Boundaries for unexpected render
failures at a scope that can fail independently; do not route expected query or
mutation errors through them and do not wrap every component defensively.

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

## Build Coherent Components And Forms

Use semantic HTML and mature accessible UI primitives. Let `shared/ui` own
stable design-system behavior, semantic tokens, focus rules, and visual
contracts. Let feature components own domain meaning. Create a shared wrapper
only when it enforces real product semantics, accessibility, or repeated
interaction behavior; do not make one-to-one wrappers that merely rename a
native element or library primitive.

Keep component interfaces semantic and small. Prefer composition over a matrix
of styling and behavior booleans. Split a component when it owns unrelated
state, orchestration, or interaction responsibilities, not to satisfy a line
count. Keep feature data orchestration out of low-level visual components.

Use primary pages for browsing, scanning, and operating existing content. Put
create, edit, and configuration forms in a modal, drawer or sheet, or a
dedicated secondary page. Use a modal or drawer for a short contextual task and
a secondary page for a long, multi-step, linkable, or recoverable task.

Use platform form behavior and direct state for a simple form. Use a mature form
library for dynamic fields, conditional sections, complex validation, or
multi-step recovery. Do not force every form through a universal abstraction.
Use the authoritative schema when its semantics match, map stable server errors
back to the relevant field or form, preserve input, and make pending and
duplicate-submission behavior explicit.

Choose the repository's styling technology, but keep stable visual decisions in
semantic design tokens. Scope feature styles locally. Do not introduce global
selectors that affect unknown surfaces or copy hard-coded values when an
appropriate token exists.

## Make Accessibility A Release Gate

Accessibility is part of the interface contract and blocks release. Use
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) AA as the default conformance target
unless the product or regulation sets a stricter one. Require:

- semantic elements and native controls before custom widgets;
- programmatic labels, meaningful headings, visible focus, complete keyboard
  operation, and correct accessible names and states;
- deliberate focus restoration or movement after dialogs, route transitions,
  validation failure, and inserted content;
- appropriate announcements for dynamic content without noisy repetition;
- meaning that does not depend on color alone, sufficient contrast, usable
  target sizes, reduced-motion support, and user font-size resilience.

Run semantic lint, automated accessibility checks, and interaction tests through
roles, names, and keyboard behavior. Exercise focus, navigation, and critical
flows in a real browser. Manually inspect changed high-risk UI because automated
scans do not prove usability. Do not waive a failure because a third-party
component caused it; the product owns the delivered interface.

## Secure Browser Identity And Script Execution

Select the OAuth/OIDC browser architecture from a threat model; do not conflate
an API's stateless token validation with browser token storage.

Classify the risk explicitly. Financial or irreversible work, administrative
privilege, regulated or sensitive data, high-value scopes, long-lived access,
or browser-held Refresh Tokens require a BFF that keeps OAuth Tokens outside
browser JavaScript. A direct browser client for other material business or
personal data requires an ADR naming the security owner, scopes, audiences,
Token lifetimes, XSS consequences, storage choice, revocation, and review or
removal condition. A lower-impact application may use a direct browser client
without manufacturing a server Session.

For a direct browser OAuth client:

- use Authorization Code with PKCE through a mature implementation; never use
  the Implicit flow or invent a login protocol;
- use the Access Token, not the ID Token, as the API credential;
- keep short-lived Access Tokens in memory by default;
- issue a Refresh Token to a public client only with rotation or sender
  constraint, and follow the provider's revocation behavior;
- make persistent browser Token storage an explicit security decision because
  same-origin malicious JavaScript can read and exfiltrate it;
- make the Resource Server verify signature and allowed algorithm, issuer,
  audience, time validity, and authorization scopes or claims against the
  provider's rotating keys.

Use a Backend for Frontend with Secure, HttpOnly, appropriately scoped cookies
and explicit CSRF protection when the sensitivity or threat model requires
Tokens to stay outside browser JavaScript. Rotate the Session after login and
privilege change, and proxy only declared downstream origins, paths, and methods.
The BFF must not expose OAuth Tokens to browser responses. It reduces Token
exfiltration but does not replace server authorization or XSS prevention. The
BFF is the OAuth client; it is not required for every application merely because
the API otherwise validates JWTs through JWKS.

[RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html) defines OAuth security
requirements. [RFC 10017](https://www.rfc-editor.org/rfc/rfc10017.html) is the
Browser-Based Applications Best Current Practice and describes the BFF,
token-mediating backend, direct browser client, and storage trade-offs. Recheck
the current BCPs and the chosen provider before changing an authentication
architecture.

Keep secrets and privileged credentials out of browser code, build arguments,
source maps, URLs, telemetry, and public configuration. Framework escaping does
not authorize arbitrary HTML. Default-deny raw HTML insertion, dynamic code
execution, and unreviewed third-party scripts. When sanitized rich text is a
product requirement, route it through one reviewed boundary using a mature
sanitizer and test malicious inputs. Enforce a restrictive Content Security
Policy through production HTTP response headers; Report-Only is a migration
tool, not completion. Validate the effective policy against the production
preview rather than grepping directive text. Use Trusted Types when injection
sinks exist and the supported-browser matrix permits enforcement; keep policy
creation in one reviewed module.

## Version Durable Browser Data

Treat browser-persisted data as a released data contract. Give durable keys a
namespace, owner, schema version, runtime decoder, and explicit migration path.
Test upgrades from every supported version when the data matters to the user.

Do not silently replace corrupt or incompatible durable data with defaults. Fail
with a recoverable user-visible path, preserve diagnosable metadata without
recording sensitive content, and delete data only when product policy explicitly
permits loss. Do not persist server-query cache, sensitive credentials, or
derivable interaction state merely to survive a reload.

## Treat Offline Behavior As A Product Capability

Do not add automatic cache fallback or delayed writes merely to keep the UI
appearing successful. Without an explicit offline contract, show the network
failure and safe retry state.

When offline behavior is a product capability, define and test:

- cache ownership, freshness, expiry, and visible stale state;
- durable queue schema and migration;
- idempotency, ordering, retry, cancellation, and duplicate delivery;
- server reconciliation and conflict resolution;
- user-visible pending, failed, blocked, and recovered states;
- storage quotas, sign-out cleanup, and multi-tab coordination.

An offline engine is substantial client-owned domain behavior and deserves a
pure tested module and explicit boundary interfaces.

## Observe The Browser At Boundaries

Centralize browser telemetry in route/navigation instrumentation, the typed
transport, scoped Error Boundaries, global unhandled-error handlers, and the
performance collector. Do not scatter `console.*`, logging calls, or duplicate
error reporting through components and hooks.

Expected failures are rendered at their owning surface and counted through
Metrics when operationally useful; they are not repeatedly reported as
exceptions. Unexpected failures capture release version, route identity,
correlation or Trace context, stable error category, browser-support class, and
sanitized diagnostic context. Propagate Trace context through the transport so
browser, API, downstream calls, and asynchronous work can be correlated.

Give the exporter explicit sampling, batching, resource limits, and privacy or
consent behavior. Treat telemetry delivery failure as a declared degraded mode
only when its drop or bounded-buffer semantics, tests, boundary self-diagnostic,
and recovery condition are explicit. The boundary surfaces that failure through
its own health signal without changing an already completed product result;
business code must neither swallow it nor misreport telemetry delivery as
successful.

Do not record request or response bodies, form values, Tokens, URLs containing
sensitive parameters, or uncontrolled user content. Analytics is not an audit
source of truth: durable audit events come from the authoritative server-side
resource boundary.

## Choose Rendering And Compatibility Deliberately

Choose CSR, SSR, SSG, streaming, or selective hydration per route from its SEO,
first-render, personalization, freshness, caching, and interaction needs. Keep
server-only and client-only modules explicit. Send JavaScript only for behavior
that requires it. Do not adopt one rendering mode as a project-wide belief.

Define an explicit supported matrix of browsers, devices, input methods, and
representative viewports from product commitments and real users. Drive build
targets, transforms, Polyfills, automated browsers, and manual checks from that
matrix. Do not add compatibility branches for uncommitted environments. Change
published support through the repository's versioning and migration rules, or
use `$bep-delivery-engineering` when that policy must be designed.

## Enforce Performance And Visual Quality

Measure before optimizing. Give each material route or critical journey an
owned performance budget covering applicable user-centric latency, JavaScript
and resource cost, request count, rendering work, and layout stability. Block a
material regression in CI; calibrate budgets with production percentiles when
real telemetry exists. Keep an explicit owner and expiry for a temporary budget
exception.

Avoid unnecessary JavaScript, renders, requests, and broad dependency imports.
Reserve layout space for delayed content, size media for its rendered use, and
prioritize only initial-journey resources. Do not trade correctness or
accessibility for an unmeasured micro-optimization.

Use visual regression for stable high-value design-system states and critical
pages across the declared themes and representative viewports. Review every
snapshot change; never bulk-accept it to make CI pass. Manually inspect new or
changed responsive UI in real browsers at representative narrow and wide
viewports. Visual proof complements behavior and accessibility tests; it does
not replace them.

## Apply The Frontend Completion Gate

Reject completion when any applicable condition is true:

- a feature is organized by technical dumping ground or another feature imports
  its internals;
- shared, route, app, feature, generated, or transport ownership is reversed or
  cyclic;
- server state is copied into a Store or duplicate state is synchronized by an
  Effect;
- a component performs direct network access or trusts unvalidated external
  data;
- client-side checks are treated as authorization or authoritative business
  enforcement;
- expected failures become generic Toasts, unexpected failures are swallowed,
  or browser telemetry is scattered and duplicated;
- an optimistic, offline, stale, or compatibility path exists without explicit
  product semantics and tests;
- raw HTML, dynamic execution, persistent Tokens, durable browser data, or a
  third-party script bypasses its trust and version boundary;
- an applicable frontend verification or common quality gate remains unmet.
