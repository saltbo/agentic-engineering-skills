# HTTP Correlation

## Correlate The Complete Interaction

Propagate stable request and Trace context from the caller through the HTTP
boundary, downstream dependencies, and asynchronous work. Extract incoming
Trace context according to the supported standard, start a new root only when
no valid parent exists or scheduled semantics require it, and inject context
into traced downstream calls.

Let the server request boundary own the one structured diagnostic completion
event. Use Metrics for aggregation and Traces for causal flow. Browser-visible
failure, server execution, dependency calls, and asynchronous continuation must
be correlatable without logging request or response bodies.
