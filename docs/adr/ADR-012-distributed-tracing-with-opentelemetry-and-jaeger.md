# ADR-012: Distributed Tracing with OpenTelemetry and Jaeger

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
As requests traverse the API Gateway, Order Service, Inventory Service, Payment Service, and Fulfillment Service via both synchronous HTTP/gRPC calls and asynchronous message queues, identifying performance bottlenecks and failure points requires unified distributed tracing.

## Decision
We standardize on OpenTelemetry (OTel) instrumentation with Jaeger as the distributed tracing backend.
1. The API Gateway generates or propagates a W3C Trace Context (`traceparent`) and a UUID `x-correlation-id`.
2. All inter-service HTTP clients, gRPC interceptors, and RabbitMQ message headers must forward the active trace context.
3. Every log statement produced by `core-logger` automatically embeds `traceId`, `spanId`, and `correlationId`.

## Consequences
### Positive
- End-to-end latency visualization across service and queue boundaries.
- Rapid mean time to resolution (MTTR) for distributed system incidents.

### Negative / Trade-offs
- Slight network overhead for trace header propagation and OTel collector reporting (mitigated by probabilistic sampling in production).
