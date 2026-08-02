# Authentication And Authorization

Use this reference for every protected operation and every API that creates or
manages identities, credentials, sessions, roles, groups, grants, scopes, or
policies. Keep authentication and authorization separate in the external
contract, framework pipeline, domain model, tests, and failure responses.

## Contents

- [Keep The Boundary Explicit](#keep-the-boundary-explicit)
- [Define Authentication](#define-authentication)
- [Produce A Normalized Principal](#produce-a-normalized-principal)
- [Define Authorization](#define-authorization)
- [Publish The OpenAPI Contract](#publish-the-openapi-contract)
- [Use Correct Failures](#use-correct-failures)
- [Separate Framework Responsibilities](#separate-framework-responsibilities)
- [Review Gate](#review-gate)
- [Standards](#standards)

## Keep The Boundary Explicit

Authentication answers:

- Which credential or authentication method was presented?
- Is it valid for this API, issuer, audience, time, and trust boundary?
- Which human, service, client, device, or other principal does it identify?

Authorization answers:

- May this authenticated principal perform this resource operation?
- May it access this particular resource, relationship, field, or collection
  member in the resource's current state?

Successful authentication never grants permission by itself. Roles, groups,
scopes, tenant identifiers, and other validated claims are authorization inputs,
not authorization decisions.

## Define Authentication

- Select established schemes such as OAuth 2.0/OpenID Connect bearer tokens,
  mutual TLS, signed API credentials, or secure sessions according to the trust
  boundary. Do not invent a custom credential protocol when a standard fits.
- Validate credentials at the framework boundary before domain handlers run.
- Validate every scheme-specific requirement, including issuer, audience,
  signature or proof, expiry, revocation behavior, and credential location.
- Never accept identity, role, group, scope, or tenant authority from ordinary
  query parameters or request-body properties.
- Treat principals as more general than users; machine and delegated clients
  must have explicit identity semantics.
- Model sessions, credentials, grants, memberships, and policies as resources
  when the API manages their lifecycle. Prefer standardized OAuth or OpenID
  Connect endpoints when implementing those protocols; their standards take
  precedence over this skill's general URI house rules.

## Produce A Normalized Principal

Authentication produces one immutable request-scoped principal for downstream
authorization. Normalize framework- or issuer-specific claims into explicit
fields such as:

- stable subject and issuer;
- authentication method and assurance data when relevant;
- calling client identity and delegation context;
- tenant context when it is part of the trusted identity boundary;
- validated roles, groups, scopes, or other policy attributes.

Preserve the distinction between a claim supplied by an issuer and an attribute
loaded from an authoritative internal source. Do not pass raw tokens, session
objects, or unvalidated claim maps into domain handlers.

## Define Authorization

Evaluate authorization from the normalized principal plus:

- the resource operation such as list, get, create, replace, update, or delete;
- the addressed resource or parent collection;
- authoritative resource ownership, tenant, relationships, and current state;
- requested fields, `view`, `include`, filter, and mutation;
- applicable policy and environmental context.

Use scopes and roles as coarse capabilities where appropriate, then enforce
resource-level policy. A matching scope or role alone must not bypass ownership,
tenant, relationship, state, or field-level constraints.

Authorize collection membership before pagination and total calculation so
counts, ordering, links, and page boundaries do not leak inaccessible resources.
Authorize every embedded relationship and returned link. Authorize create
requests against the target collection, parent, and referenced resources.

Keep roles, groups, and client types out of resource paths. Do not create
`/admin/users`, `/manager-orders`, or separate canonical URIs for different
principals. Express authority through policy over the same resource URI.

## Publish The OpenAPI Contract

- Define authentication mechanisms under `components.securitySchemes`.
- Apply explicit operation-level `security` requirements. Use OAuth/OpenID
  Connect scopes where they are part of the public protocol.
- Treat an OpenAPI Security Requirement as a declared credential and coarse
  scope requirement, not a complete resource-level authorization policy.
- Document resource-level authorization behavior that affects callers,
  including field visibility, collection filtering, tenant boundaries, and
  resource-concealment policy.
- Define reusable `401`, `403`, and, when selected, concealment `404` Problem
  Details responses. Declare `WWW-Authenticate` where the authentication scheme
  requires it.
- Never document internal group or role names as a stable public contract unless
  the API intentionally exposes and versions them as public policy identifiers.

## Use Correct Failures

| Condition | Response |
| --- | --- |
| Required credentials are missing | `401 Unauthorized` with the applicable challenge |
| Credentials are malformed, expired, revoked, or otherwise invalid | `401 Unauthorized` with the applicable challenge |
| Principal is authenticated but lacks authority | `403 Forbidden` |
| Bearer token lacks a required scope | `403 Forbidden`; follow RFC 6750 challenge semantics |
| Existence must be concealed from unauthorized principals | Consistent policy-selected `404 Not Found` |

Do not return `403` for invalid credentials and do not return `401` merely
because an authenticated principal lacks permission. Choose resource concealment
by resource class and threat model, not endpoint-by-endpoint convenience.

## Separate Framework Responsibilities

Implement two distinct framework components:

1. **Authentication:** extract and validate credentials, resolve trusted
   identity attributes, and attach the normalized principal.
2. **Authorization:** evaluate policy for the resolved route, resource, and
   operation, then permit or deny access.

Handlers never parse tokens, inspect raw claims, translate authentication
exceptions, or implement scattered `isAdmin`/role/scope branches. Domain code
may supply authoritative resource facts to a policy decision, but credential
processing stays outside the domain.

Test the components independently:

- authentication tests cover missing, invalid, expired, wrong-issuer, and
  wrong-audience credentials plus normalized principal output;
- authorization tests start with a valid principal and cover allowed, denied,
  cross-tenant, ownership, state, field, collection, and concealment cases;
- contract tests verify `401`, `403`, `404`, challenges, Problem Details, and
  OpenAPI security requirements.

## Review Gate

Reject the design or implementation when:

- authentication success is treated as authorization success;
- credential validation and policy decisions share one handler or helper;
- handlers parse tokens or raw claims;
- roles, groups, or scopes are trusted from ordinary request data;
- scopes or roles replace resource-level authorization;
- collection totals or links reveal unauthorized resources;
- `401` and `403` are interchangeable;
- the same resource gets role-specific paths;
- OpenAPI declares a scheme but omits operation security or expected failures;
- authorization behavior is duplicated across handlers instead of enforced by
  one policy boundary.

## Standards

- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [RFC 6750: OAuth 2.0 Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750)
- [OpenAPI Security Scheme and Security Requirement Objects](https://spec.openapis.org/oas/latest.html)
