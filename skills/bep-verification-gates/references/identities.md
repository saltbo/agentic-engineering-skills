# Proof Identities And BDD

Apply this protocol only to the governed scope. For new governance use BEP defaults; for an existing project preserve its declared policy unless this task authorizes a transition.

## Use Stable Proof Identities

Give every governed production item and proof a stable machine-readable identity.
Generate one normalized inventory record for every testable item:

```text
kind | stable id | production source | required profiles
```

Represent coverage as `(inventory item, required profile)` pairs. A pair is
covered only when it maps to an executable test in the required proof layer and
the native runner reports that test executed and passed.

Give every BDD scenario, critical journey, public operation, Repository,
external Adapter, Consumer, migration path, observability boundary, frontend
route, frontend transport, and frontend feature operation its profile-defined
stable identity. Give every stable Port failure category both a production and
handling proof identity.

Keep governance identities as literal, statically discoverable metadata in the
ecosystem's canonical test declaration. Parameterized execution may implement
the matrix underneath, but every required proof identity remains independently
discoverable and attributable to one proof layer.

## Trace Product Behavior Through BDD

Use lightweight `.feature` files as the source of truth for user-visible product
behavior. Write scenarios in domain language and observable outcomes, without
database tables, HTTP paths, CSS selectors, classes, mocks, or other
implementation details.

Every scenario has one unique stable ID and declares its cheapest canonical
proof layer, for example `@id:ORD-001 @proof:unit`. The proving test carries the
same stable ID through the ecosystem proof adapter. The BDD lint gate proves:

- every scenario ID is unique and maps to at least one executable test;
- every mapped test exists in the declared proof layer;
- no required scenario or proving test is skipped;
- deleted or renamed scenarios leave no orphaned proof identity.

Map each scenario to the Unit, Integration, or E2E tests that prove it.

Update or add the scenario before implementing new or changed user-visible
behavior. A behavior-preserving refactor, dependency update, performance-only
change, or behavior-preserving migration does not change the scenario. For a
bug, add a scenario only when the product specification was missing or
ambiguous; otherwise link the regression test to the existing scenario.
