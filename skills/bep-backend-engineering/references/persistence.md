# Persistence And Consistency

Apply BEP preferences to new architecture. In an existing project, improve the affected boundary within its conventions; do not require unrelated restructuring.

## Put Transactions Around Business Operations

The Use Case owns transaction semantics because it knows which complete
business operation must be atomic. The infrastructure layer provides a
transaction or Unit-of-Work mechanism without deciding the business boundary.

- Never open or coordinate a transaction in an HTTP handler, RPC handler, or
  queue consumer.
- Pass transaction-scoped repositories or an explicit transaction context only
  within the operation that owns it.
- Keep external network calls out of database transactions unless the chosen
  consistency design explicitly requires and proves the consequences.
- Prefer a single atomic repository operation when one datastore statement and
  constraint can guarantee the invariant.
- Use an outbox or another explicit consistency protocol when one operation
  changes durable state and publishes a message.

Do not disguise a read-then-write race as a transaction. Use constraints,
conditional updates, version checks, locks, or atomic datastore operations that
actually preserve the invariant under concurrency.

## Shape Repositories Around Domain Resources

Define a repository around a Domain aggregate or cohesive resource, never
automatically around each database table. Its methods express business-needed
persistence operations and return Domain values or stable Port results.

When a write decision depends on existing aggregate state, load that state and
apply the transition through Domain behavior before persisting it. When an
invariant can be expressed completely by one constraint or conditional write,
prefer the atomic repository operation and map a rejected or zero-row write to
its stable Domain or Port failure. Do not add a read-before-write race merely to
construct an aggregate. For complex read-only views, define a separate Query or
Read Port that may return a purpose-built DTO without constructing an aggregate
that will not enforce behavior.

A generic CRUD implementation may exist only as private infrastructure reuse.
Use it to remove mechanical adapter duplication while keeping all of these out
of the business contract:

- generic CRUD interfaces;
- ORM models and query builders;
- table-oriented filters, sort syntax, or pagination internals;
- datastore-specific options or transactions.

Every Use Case depends on its domain-specific narrow repository or Query Port.
Add non-generic adapter operations when the domain capability cannot be
expressed safely through the private CRUD mechanism.

Make cursor pagination use a stable total order. When the primary sort field is
not unique, add a unique tiebreaker such as the resource ID to the ordering,
cursor, and seek predicate. Keep cursor encoding opaque and Adapter-owned; a
cursor over only a non-unique timestamp can silently skip or repeat rows.

## Keep Caching Semantically Transparent

Implement a cache as an adapter or decorator when it preserves the Port's
observable semantics. The cache owns keys, encoding, expiration mechanics,
stampede control, and cache-provider errors without leaking them inward.

Stale reads, partial data, fail-open behavior, or degraded responses change
product semantics. Model them explicitly in the Use Case or product contract,
including their validity window, recovery condition, tests, and observability.
Never introduce them as an adapter's silent fallback.

Keep invalidation ownership aligned with the business write. Prove concurrent
miss, stale entry, write/invalidate ordering, and outage behavior when those
risks exist.
