# Writes And Retries

## Make Writes Safe Under Repetition And Concurrency

Define write behavior for refresh, double submission, timeout, client retry,
concurrent update, and an unknown response outcome. Use operation-appropriate
idempotency identity, conditional request semantics, version checks, or
datastore constraints.

Retry only a transient failure at the boundary that owns the complete operation
semantics. Require idempotency, finite attempts, backoff, jitter, and an overall
deadline. A client or intermediary may not infer that an uncertain write failed
and silently repeat a non-idempotent operation.
