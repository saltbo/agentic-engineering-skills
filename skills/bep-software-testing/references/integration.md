# Integration And Contract Testing

## Exercise Real Integration Boundaries

The named boundary must be real. Dependencies outside it may use a
protocol-faithful Fake. Run the production codec, schema, middleware,
configuration, and assembly that define the boundary's semantics.

Choose cases from the boundary contract and changed risks. Use formal runtime
verification profiles only when the project has adopted that governance. Assert stable protocol results, classifications, state transitions, and
structured fields rather than incidental prose, timestamps, formatting, or
vendor messages.

An Integration test cannot claim a datastore, router, queue, browser, identity,
or external protocol that it replaced with an in-process imitation lacking the
same semantics.

## Test Deployment Contracts

Use Contract tests only at independent deployment boundaries. For an OpenAPI or
other owned protocol contract, validate the artifact, verify runtime responses
against it, and require provider and consumer to use compatible versions.

Add consumer-driven contracts only when independently released consumers need
to express requirements the provider contract cannot safely capture. Do not add
Contract tests between modules deployed as one process. Contract compatibility
does not replace provider Integration proof of middleware, authorization,
storage, or behavior.

For versioned events, test producer encoding and consumer decoding against the
same published schema, including supported-version compatibility and stable
failure handling.
