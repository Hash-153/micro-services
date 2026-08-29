# ADR-020: Graceful Shutdown and Zero-Downtime Container Lifecycle

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
During Kubernetes rolling updates or pod auto-scaling downscaling, in-flight HTTP requests and active database transactions must complete gracefully without abrupt termination.

## Decision
All microservice servers handle `SIGTERM` and `SIGINT` signals with a graceful shutdown sequence:
1. Stop accepting new incoming HTTP/gRPC requests.
2. Mark Kubernetes readiness probe as unhealthy.
3. Allow up to 25 seconds for in-flight requests to complete.
4. Stop background event consumers and flush logs.
5. Close database connection pools and Redis clients.
6. Exit process cleanly with code 0.

## Consequences
### Positive
- Zero 502/504 Bad Gateway errors during deployments and pod scaling events.
- Clean release of database locks and message broker channel leases.

### Negative / Trade-offs
- Kubernetes `terminationGracePeriodSeconds` must be configured to at least 30s.
