# Frontend Verification Profile

Apply this profile when production or review affects browser routes, typed
transports, feature operations, forms, navigation, browser state, accessibility,
security, compatibility, performance, responsive behavior, or visual quality.
Apply the common testing and quality-gate references first.

## Contents

- [Generate The Frontend Behavior Inventory](#generate-the-frontend-behavior-inventory)
- [Derive Required Profiles](#derive-required-profiles)
- [Prove Behavior At The Canonical Unit Layer](#prove-behavior-at-the-canonical-unit-layer)
- [Prove Browser Behavior](#prove-browser-behavior)
- [Block On Browser Quality](#block-on-browser-quality)
- [Enforce Frontend Architecture Mechanically](#enforce-frontend-architecture-mechanically)
- [Apply The Frontend Verification Gate](#apply-the-frontend-verification-gate)

## Generate The Frontend Behavior Inventory

Generate four kinds from production declarations:

- `frontend-route` for every navigable product surface;
- `frontend-transport` for each typed remote boundary that normalizes status,
  credentials, correlation, and runtime decoding;
- `frontend-operation` for every user-visible feature query or command;
- `frontend-operation-entry` for every concrete route-to-operation binding.

The declarations must construct or be consumed by the real router, feature
operation wrappers, and runtime bindings. Reconcile route `(id, path)` pairs
with the flattened production router, route-operation pairs with runtime
bindings, sources with architecture-owned files, and transport operations with
the authoritative server operation registry.

A test-only checklist or directory scan is not authoritative. Frontend
inventory permits no manual item or profile exception. Correct the production
declaration. Require an explicit disabled declaration with a reason when the
governed project has no browser frontend.

## Derive Required Profiles

Every transport requires `success`, `protocol-failure`, and `invalid-payload`.
Derive `credentials` and `correlation` from its production capabilities. A
compile-time typed but runtime-undecoded response fails `invalid-payload`.

Every route requires `render`, `unexpected-failure`, and `accessibility`.
Derive:

- `url-state` from a non-empty URL-state key list;
- `authentication` and `authorization` from access metadata;
- `dialog-lifecycle` for modal or drawer surfaces.

One `dialog-lifecycle` proof covers open, close, cancellation, and focus
restoration.

Classify each operation as `query` or `command`, with route, user, or background
trigger and explicit input kind. Every operation requires `success` and
`unexpected-failure`; a user trigger adds `interaction`.

A query requires `loading` and derives `empty`, `stale`, `partial`, and `offline`
from declared capabilities. A command requires `pending` and
`duplicate-submit`. Derive:

- `validation` from non-empty input;
- `authentication`, `authorization`, and `conflict` from the linked server
  operation;
- `recoverable-failure` for transport work;
- `uncertain-result` for a transport command;
- `destructive-safety`, `undo`, `optimistic-rollback`, and
  `offline-reconcile` from explicit production capabilities.

A form declares whether it creates, edits, configures, searches, filters, or
performs another operation. Create, edit, and configuration forms bind only to
a modal, drawer, or secondary page. Record the rendered surface on the
production route-operation binding so a dialog opened from a primary route is
not misclassified as an inline form.

Reject query/command contradictions, undo without destructive work, optimistic
destructive work, or a read/write mode that disagrees with the linked server
operation. Every operation must be bound, and every entry requires `wired`.

## Prove Behavior At The Canonical Unit Layer

Prove every frontend inventory pair in the canonical Unit layer with semantic
feature interactions and a protocol-level API Fake. A `web`, component, jsdom,
or real-browser component project remains a Unit runtime subdivision while it
does not cross the real application boundary.

Mock only real browser or protocol boundaries, never internal hooks, child
components, query definitions, private state, or the typed client. Keep Unit and
component tests beside feature source. Keep cross-boundary Integration, visual,
and E2E suites in explicit suite directories.

Test through accessible roles, names, content, navigation, and user events.
Critical authentication continuity, focus, navigation, layout, and cross-stack
risks require additional real-browser or E2E proof. Those tests complement and
never replace the complete canonical Unit behavior matrix.

## Prove Browser Behavior

Use a real supported browser to prove behavior that DOM simulation cannot:

- keyboard traversal, focus order, focus trapping, and focus restoration;
- route history, navigation, reload, and URL-owned state;
- browser authentication continuity and cookie behavior;
- layout, zoom, reflow, viewport, font-size, and reduced-motion behavior;
- CSP, Trusted Types, sanitization, origin, redirect, and injection enforcement;
- browser storage migration and multi-tab coordination;
- supported-browser compatibility and production-preview integration.

Use deterministic data, time, fonts, animation settings, browser versions, and
viewports. Manual inspection remains required where automation cannot establish
screen-reader usability, responsive coherence, or interaction quality. Record
the inspected matrix and result.

## Block On Browser Quality

Make these independent gates block every pull request when the production
capability metadata derives their profile:

- semantic lint and automated accessibility checks;
- real-browser keyboard and focus proof for critical interactions;
- browser-support smoke tests from the versioned support matrix;
- production-preview CSP and injection probes rather than source grep;
- critical-journey performance budgets under deterministic lab conditions;
- visual regression for stable critical states with reviewed baseline changes;
- recorded responsive and manual accessibility inspection for changed high-risk
  UI.

Treat production field performance as an SLO and release signal. Noisy field
samples do not directly decide one pull request. Visual evidence complements
behavior and accessibility proof; it never replaces either.

## Enforce Frontend Architecture Mechanically

Put every reliably detectable frontend architecture constraint into blocking
CI. Cover:

- feature public-entry imports and dependency direction;
- direct component network, configuration, or durable-storage access;
- duplicate server state and forbidden synchronization Effects;
- ad-hoc console or telemetry calls;
- dangerous HTML, dynamic execution, and unreviewed script boundaries;
- focused or skipped tests and inventory completeness;
- accessibility, supported-browser, performance, and visual-baseline gates.

Use the repository's type-aware linter, import graph, build tooling, browser
probes, and security analysis. Maintain positive and bypass-oriented negative
fixtures. A name-based syntax scan cannot claim to prove aliases, computed
access, framework construction, or data flow.

## Apply The Frontend Verification Gate

Reject completion when any of the following is true:

- a production frontend item or required profile is missing, stale, skipped,
  manually entered, excepted, or uncovered;
- a transport trusts an undecoded runtime value or lacks stable protocol
  failure normalization;
- a route, operation, or concrete binding lacks canonical Unit proof;
- a create, edit, or configuration form binds directly to a primary browsing
  surface;
- authentication, focus, navigation, layout, security, or compatibility risk
  lacks its required real-browser proof;
- accessibility, browser support, performance, responsive layout, or visual
  behavior lacks its blocking evidence;
- a frontend architecture rule exists only in prose when a reliable detector
  can enforce it;
- the common testing or quality-gate reference remains unmet.
