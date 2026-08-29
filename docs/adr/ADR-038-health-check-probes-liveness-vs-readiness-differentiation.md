# ADR-038: Health Check Probes Liveness vs Readiness Differentiation

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context & Problem Statement
In an enterprise distributed microservices architecture operating across multiple Kubernetes nodes and databases, clear design standards are mandatory to prevent subtle distributed system failures, concurrency deadlocks, and compliance breaches.

## Decision
We formally adopt **Health Check Probes Liveness vs Readiness Differentiation**.
Liveness checks purely inspect process loop responsiveness; Readiness checks verify database and queue connectivity.

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
