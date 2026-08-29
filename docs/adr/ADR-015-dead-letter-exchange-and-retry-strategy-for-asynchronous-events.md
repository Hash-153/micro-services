# ADR-015: Dead Letter Exchange and Retry Strategy for Asynchronous Events

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Transient consumer failures (e.g. database connection hiccup, temporary downstream API downtime) must not cause message loss or permanently block queue consumption.

## Decision
We implement a 3-tier dead-letter and retry architecture in RabbitMQ:
1. **Primary Queue**: Messages are consumed. If a consumer throws a retryable error, the message is nacked.
2. **Retry Queue with TTL**: Nacked messages are routed to a delayed retry exchange with an exponential TTL (5s, 25s, 125s) before dead-lettering back to the main queue.
3. **Dead Letter Queue (DLQ)**: After 3 failed retry attempts, messages are moved to `novacommerce.dlq` for manual inspection and alerting.

## Consequences
### Positive
- Resilient recovery from transient network glitches without data loss.
- Poison-pill messages are isolated to the DLQ without blocking other valid traffic.

### Negative / Trade-offs
- Out-of-order delivery possible during retries, requiring idempotent consumers.
