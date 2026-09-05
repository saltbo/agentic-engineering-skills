# Rendering And Performance

Use these preferences for new work. Preserve existing architecture and supported behavior unless the task includes changing them. Apply checks to the affected capability; formal project-wide CI governance is a separate task.

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
