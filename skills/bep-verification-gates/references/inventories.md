# Production Proof Inventories

Apply this protocol only to the governed scope. For new governance use BEP defaults; for an existing project preserve its declared policy unless this task authorizes a transition.

## Derive Inventories From Production

Generate inventories from authoritative production artifacts, never a parallel
testing checklist:

- API operations from authoritative protocol operation identities;
- routes from the real runtime router and production route metadata;
- Repositories, external Adapters, Consumers, and observability boundaries from
  production registries or architecture-enforced directories;
- concrete request, Consumer, scheduled, and CLI wiring from production
  composition registries;
- stable Port errors from the Port's enumerable error taxonomy;
- migrations from migration history and supported-version policy;
- frontend routes, transports, operations, and bindings from production router,
  contract, and feature-operation declarations;
- BDD scenarios and critical journeys from feature IDs and tags.

Make the generator consume declarations also used by production composition.
Compare declared routes with the runtime router, registered adapters with
architecture-owned files, and migration declarations with history on disk.
Emit deterministic per-kind counts and a content digest, and have the linter
recompute both.

A generic collector cannot prove its own provenance. Add a stack-specific
source or import-graph gate that proves the collector reaches the actual router,
composition registries, and feature wrappers. Keep the collector gate unmet
until that provenance is mechanically established.

Use a manual inventory entry only when production derivation is impossible.
Every manual entry records its reason, owner, and expiry or removal condition.
Frontend verification permits no manual item or profile exception.

## Define Applicability Mechanically

Derive required profiles from production-owned capability metadata. An omitted
default profile is allowed only when semantically impossible, never merely
inconvenient. When metadata cannot express the semantic fact, record this exact
exception shape beside the production declaration:

```json
{
  "profileExceptions": [
    {
      "profile": "authentication",
      "reason": "The operation is reachable only through an authenticated private service binding",
      "owner": "orders",
      "removalCondition": "Remove when the operation becomes directly network-addressable"
    }
  ]
}
```

Lint the exception like a production declaration. Reject an unknown profile,
missing owner, vague reason, stale condition, or exception that metadata can
express directly. Do not except an observability boundary's derived contract,
a concrete entry's production wiring, or any frontend inventory profile.
