# HTTP Trust Boundaries

## Separate Identity From Permission

Authenticate at the HTTP execution boundary and produce a normalized immutable
principal. Authorize separately against the addressed resource, operation,
ownership, tenant, state, and requested fields. A valid identity is input to a
permission decision, never proof of permission.

Keep raw tokens and provider claims out of business code. Expose stable
authentication and authorization failure categories without leaking credential
details or turning denial into resource success.

## Secure Every HTTP Trust Transition

Keep credentials and privileged data out of URLs, redirects, ordinary logs,
error bodies, caches, and browser-readable configuration. Apply established
platform controls for cookie scope, transport security, CSRF, CORS or origin
policy, redirects, uploads, and content handling.

Authorize the addressed resource and fields, not only the route or coarse role.
Apply upload size, decoded-size, content, rate, and cost limits where untrusted
input can consume material resources. Use mature protocol and cryptography
implementations; never invent an authentication or token format.
