# Browser Security And Storage

Use these preferences for new work. Preserve existing architecture and supported behavior unless the task includes changing them. Apply checks to the affected capability; formal project-wide CI governance is a separate task.

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
