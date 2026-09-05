# Components And Accessibility

Use these preferences for new work. Preserve existing architecture and supported behavior unless the task includes changing them. Apply checks to the affected capability; formal project-wide CI governance is a separate task.

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
