# Frontend Remote Data

Use these preferences for new work. Preserve existing architecture and supported behavior unless the task includes changing them. Apply checks to the affected capability; formal project-wide CI governance is a separate task.

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
