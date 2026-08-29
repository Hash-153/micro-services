# ADR-036: GraphQL vs REST vs gRPC Protocol Matrix

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context & Problem Statement
In an enterprise distributed microservices architecture operating across multiple Kubernetes nodes and databases, clear design standards are mandatory to prevent subtle distributed system failures, concurrency deadlocks, and compliance breaches.

## Decision
We formally adopt **GraphQL vs REST vs gRPC Protocol Matrix**.
Adopt REST for public API Gateway clients, gRPC for internal low-latency RPC, and RabbitMQ for asynchronous event notifications.

### Key Implementation Principles:
1. **Fault Tolerance**: Services must degrade gracefully under network partition or transient downstream service downtime.
2. **Determinism**: System state transitions must be completely deterministic and reproducible.
3. **Observability**: All actions and state mutations must be auditable via distributed tracing and structured telemetry.

## Consequences & Trade-offs
### Positive:
- Highly resilient distributed operations.
- Verifiable compliance with enterprise regulatory standards (SOX, GDPR, PCI-DSS Level 1).
- Exceptional developer productivity through consistent architectural guidelines.

### Negative:
- Additional operational rigor required during peer review and pull request validation.
