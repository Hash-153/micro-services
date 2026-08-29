# ADR-013: Idempotency Key Specification for State-Mutating APIs

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Network retries, client timeouts, and automated message broker redeliveries can cause duplicate order creation, duplicate payment authorization, or double inventory reservations.

## Decision
We mandate an `Idempotency-Key` HTTP header (UUID v4) for all `POST` and `PUT` mutating operations in the Order, Payment, and Fulfillment services.
1. When a mutating request arrives, the service checks Redis for an existing idempotency record with that key.
2. If the key exists and is in `IN_PROGRESS` state, concurrent duplicate requests are rejected with `409 Conflict`.
3. If the key exists with a completed result, the cached response payload and HTTP status code are returned immediately without re-executing business logic.
4. If the key is new, the operation executes and the response is cached with a 24-hour TTL.

## Consequences
### Positive
- Safe network retries from clients and upstream message queues.
- Zero duplicate billing or duplicate order placement.

### Negative / Trade-offs
- Requires Redis storage for idempotency caches and distributed lock coordination.
