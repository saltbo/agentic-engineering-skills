# Messaging And Durable Work

Apply BEP preferences to new architecture. In an existing project, improve the affected boundary within its conventions; do not require unrelated restructuring.

## Model Queues And Long-Running Work Explicitly

Treat queue publication as a Port and the queue consumer as a Transport. The
consumer establishes the execution boundary, validates and normalizes the
message, invokes application behavior, and lets boundary policy acknowledge,
retry, reject, or archive the result.

Every durable task message has:

- a stable message identifier and version;
- correlation or Trace identity;
- an idempotency or deduplication identity;
- explicit payload semantics independent from queue SDK types.

Assume at-least-once delivery unless stronger semantics are proved. Make every
consumer idempotent, bound retries with backoff and jitter, distinguish
retryable from permanent errors, and define poison-message or dead-letter
handling. Do not acknowledge failed work as success.

Use an outbox when a committed database change and message publication must not
diverge. For long-running work, persist an explicit lifecycle including queued,
running, succeeded, failed, cancelled, or timed-out states as applicable.
Define progress, deadlines, cancellation, retry limits, and failure archive or
repair behavior instead of hiding them in an in-memory task.

## Separate Domain Events From Integration Events

A Domain Event is an internal business fact. Keep it in Domain vocabulary and
free from broker names, serialization annotations, delivery metadata, and
external compatibility concerns.

An Integration Event is a versioned public message contract. Map Domain Events
to Integration Events at the application commit boundary, persist them through
the outbox when consistency requires it, and publish only committed facts.

Consumers must be idempotent and tolerate delivery repetition. Evolve
Integration Events through the supported protocol-version policy; do not force
Domain types to retain obsolete wire fields for compatibility.
