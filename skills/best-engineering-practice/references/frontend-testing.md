# Frontend Testing And Quality Gates

Apply `core.md`, `testing.md`, `web.md`, and `frontend.md` first. This reference
adds the frontend-specific behavioral denominator and browser evidence without
calling every browser test E2E.

## Generate The Frontend Behavior Inventory

Generate four kinds from production declarations:

- `frontend-route` for every navigable product surface;
- `frontend-transport` for each typed remote boundary that normalizes status,
  credentials, correlation, and runtime decoding;
- `frontend-operation` for every feature query or command visible to a user;
- `frontend-operation-entry` for every concrete route-to-operation binding.

The declarations must construct or be consumed by the real router, feature
operation wrappers, and runtime bindings. Reconcile route `(id, path)` pairs with
the flattened production router, route-operation pairs with runtime bindings,
transport and operation sources with architecture-owned files, and every transport operation
with the server's authoritative API operation registry. A test-only checklist
or directory scan is not authoritative. Require transport proofs for success,
protocol-failure normalization, invalid payload rejection, and applicable credentials and
correlation; returning a compile-time typed but undecoded response fails the
invalid-payload profile.

Every route requires `render`, `unexpected-failure`, and `accessibility`. Derive
`url-state` from a non-empty URL-state key list, `authentication` and
`authorization` from access metadata, and `dialog-lifecycle` for modal or drawer
surfaces. One dialog-lifecycle proof covers open, close, cancellation, and focus
restoration.

Classify each operation as `query` or `command`, with a route, user, or background
trigger and explicit input kind. A form also declares whether its purpose is
create, edit, configure, search, filter, or another action. Create, edit, and
configuration forms may bind only to a modal, drawer, or secondary page, never
to a primary browsing surface. Record the rendered surface on the production
route-operation binding so a modal or drawer opened from a primary route is not
misclassified as an inline form. A modal or drawer entry also requires a
`dialog-lifecycle` proof. Every operation requires `success` and
`unexpected-failure`; a user trigger adds `interaction`. A query adds `loading`
and derives `empty`, `stale`, and `partial`. A command adds `pending` and
`duplicate-submit`. Derive:

- `validation` from non-empty input;
- `authentication`, `authorization`, and `conflict` from the linked server
  operation rather than repeating them in frontend metadata;
- `recoverable-failure` for transport work;
- `uncertain-result` for a transport command;
- `destructive-safety`, `undo`, `optimistic-rollback`, and
  query `offline`, or command `offline-reconcile` from explicit production
  capabilities.

Reject query/command capability contradictions, undo without destructive work,
optimistic destructive work, or a read/write mode that disagrees with the
linked server operation. Every operation must be bound, and every entry requires
`wired`. Do not permit manual frontend items or profile exceptions; correct the
production declaration. Require an explicit disabled declaration with a reason
when the governed project has no browser frontend.

## Prove Behavior At The Canonical Unit Layer

Prove every frontend inventory pair in the canonical Unit layer with semantic
feature interactions and a protocol-level API Fake. The existing `web` or real-
browser component project remains a Unit runtime subdivision. Mock only real
browser or protocol boundaries, never internal hooks, child components, query
definitions, or the typed client.

Keep Unit and component tests beside the feature source. Keep cross-boundary
Integration, visual, and E2E tests in explicit suite directories; do not repeat
the layer in a filename when its directory already classifies it.

Critical authentication continuity, focus, navigation, layout, and cross-stack
risks require additional real-browser or E2E proof. Those tests do not replace
the complete cheap behavior matrix. A passing inventory proves 100% of declared
applicable pairs, not complete WCAG conformance or every visual state.

## Block On Browser Quality

Make these independent gates block every pull request when applicable:

- semantic and automated accessibility checks plus real-browser keyboard and
  focus behavior for critical interactions;
- browser-support smoke tests derived from the versioned support matrix;
- production-preview CSP and injection probes rather than source grep;
- declared critical-journey performance budgets under deterministic lab
  conditions;
- visual regression for stable critical states with reviewed baseline changes.

Use fixed data, time, fonts, animation settings, browser versions, and viewports
for visual evidence. Treat production field performance as an SLO and release
signal; noisy field samples do not directly decide one pull request. Preserve
manual browser, keyboard, screen-reader, zoom, reflow, and responsive inspection
where automation cannot establish usability.

Require 100% frontend behavior inventory and at least 90% Unit production-code
coverage per module and changed code. Neither denominator substitutes for the
browser-quality gates above.
