# Resource Creation And Organization

Scope: apply BEP design preferences directly to new APIs. In an existing API,
preserve established supported conventions, including version placement, naming,
and representation shapes. Do not require migration or deprecation merely for
style conformity. The checks below apply to the changed contract and selected
profile; security, protocol correctness, and supported behavior remain required.

Use this reference before adding a field, value object, resource, path prefix,
OpenAPI tag, or API module. HTTP and REST do not define domain decomposition;
the rules below are this skill's mandatory resource-design policy.

## Contents

- [Choose Field, Value Object, Or Resource](#choose-field-value-object-or-resource)
- [Prove A New Resource](#prove-a-new-resource)
- [Choose The Owning Domain Group](#choose-the-owning-domain-group)
- [Represent Groups Without Corrupting URIs](#represent-groups-without-corrupting-uris)
- [Handle Cross-Group Relationships](#handle-cross-group-relationships)
- [Review Gate](#review-gate)

## Choose Field, Value Object, Or Resource

Keep a concept as a scalar field when all of these are true:

- it has no identity separate from the containing resource;
- it has no lifecycle outside the containing resource;
- it has the same owner, authorization, retention, and consistency boundary;
- it changes under the same concurrency control and representation version;
- clients do not need to address, link, list, query, or audit it independently;
- its cardinality is naturally bounded within one representation.

Use an embedded value object when those conditions still hold but several fields
form one meaningful, identityless value such as a postal address or money
amount. Replace or patch it only as part of its owning resource.

Create a resource when any strong independence signal exists:

- it has a stable identity or must be referenced from other resources;
- it has its own creation, transition, expiry, archival, or deletion lifecycle;
- it forms an independently growing collection;
- clients need a canonical URI, direct retrieval, filtering, ordering, or
  pagination;
- it has different authorization, visibility, tenancy, retention, audit, or
  regulatory rules;
- it needs independent `ETag`, cache, consistency, retry, or concurrency
  semantics;
- it represents asynchronous work, an attempt, request, approval, grant,
  reservation, publication, result, or other durable process evidence;
- embedding it would make the parent representation unbounded or unstable.

Do not create a resource only because the implementation has another table,
class, service, or module. Do not add a field only to avoid designing a real
resource. Storage joins and transaction boundaries are evidence, not decisive
API semantics.

## Prove A New Resource

Record this decision before adding a path:

| Question | Field or value object | New resource |
| --- | --- | --- |
| Identity | Only the parent's identity | Stable independent identity |
| Lifecycle | Created and removed with parent | Independent states or retention |
| Cardinality | Bounded part of one representation | Independent or growing collection |
| Addressability | Never addressed directly | Needs canonical URI or links |
| Access policy | Same as parent | Independent authorization or visibility |
| Consistency | Same validator and update boundary | Independent cache, ETag, or consistency |
| Query | Read only with parent | Independently listed, filtered, or sorted |
| Audit | Parent history is sufficient | Own history or durable evidence |

If the evidence remains mixed, prefer the simplest representation that preserves
the actual lifecycle and authorization boundary. Record which future condition
would justify extraction. Do not pre-create speculative resources.

## Choose The Owning Domain Group

A domain group is a stable area of business language and rules. It is not a UI
module, organizational team, repository directory, database schema, controller,
deployment unit, or temporary product initiative.

Assign each resource to exactly one primary group by answering in order:

1. Which domain defines the resource's identity and authoritative vocabulary?
2. Which domain owns its invariants and valid lifecycle transitions?
3. Which domain decides its authorization, retention, audit, and consistency
   policies?
4. Which domain remains responsible if teams, services, screens, and storage
   layouts change?

The group that owns those decisions owns the resource. Request volume, number of
references, and the team currently implementing it do not determine ownership.

Reject catch-all groups such as `common`, `shared`, `misc`, `management`,
`general`, or `utilities`. A concept used by many groups either still belongs to
one authoritative domain or is itself a coherent domain with explicit rules.

## Represent Groups Without Corrupting URIs

Represent grouping in this order:

1. OpenAPI tags and documentation navigation;
2. contract and implementation package boundaries when the repository supports
   them;
3. an optional URI namespace only when that namespace is itself a stable,
   externally meaningful part of the public API.

Give every operation exactly one primary domain-group tag. Keep resource
operation identifiers globally unique and independent of documentation order.
Use hierarchical OpenAPI tags only when the project's chosen OpenAPI version and
toolchain support them; otherwise use one stable flat tag per domain group.

Do not add a URI prefix merely to mirror the current codebase:

```text
Reject: /modules/billing/invoice-controller/invoices
Reject: /team-a/invoices
Reject: /billing-service/invoices

Default canonical resource: /invoices/{invoiceId}
Optional stable namespace:  /billing/invoices/{invoiceId}
```

Use the optional namespace form only when `billing` is a durable public domain
namespace, prevents real ambiguity in a composed API, and will survive internal
reorganization. Once published, it is part of the canonical URI and cannot be
moved without a compatibility migration.

Do not confuse grouping with ownership nesting. `/customers/{customerId}/cards`
means the customer owns and scopes those cards; it must not be used merely to
place cards in a customer-related documentation group.

## Handle Cross-Group Relationships

- Keep one canonical URI in the owning group.
- Reference the resource from other groups through its absolute relationship
  URL under `links`.
- Do not duplicate representations under multiple group prefixes.
- Do not create proxy resources unless the proxy has its own identity,
  lifecycle, representation, and policy.
- Keep cross-group writes at the resource that owns the changed invariant. If a
  workflow spans groups, compose resource transitions or create a durable
  domain-specific request or job resource in the group that owns the workflow.

## Review Gate

Reject the design when:

- a new resource lacks a strong independence signal;
- an existing resource gains fields with a different lifecycle, policy,
  cardinality, or concurrency boundary;
- a resource belongs to several primary groups;
- group ownership is justified by UI, team, service, code, or storage layout;
- a catch-all group hides unresolved domain ownership;
- URI nesting is used as documentation grouping;
- a group prefix is likely to change with an internal reorganization;
- the same resource receives multiple canonical URIs for different groups.

When ownership cannot be established, report the missing decision and pause only
work dependent on that decision before defining the path or OpenAPI operation.
