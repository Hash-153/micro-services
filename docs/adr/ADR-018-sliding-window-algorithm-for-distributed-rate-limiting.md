# ADR-018: Sliding Window Algorithm for Distributed Rate Limiting

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Fixed-window rate limiters suffer from traffic burst anomalies at window boundaries (e.g. allowing 2x traffic if requests arrive at the end of window 1 and start of window 2).

## Decision
We implement a Sliding Window Log rate limiter using Redis sorted sets (ZSET).
1. Each request adds a timestamp entry with `ZADD key now requestId`.
2. Expired timestamps are purged with `ZREMRANGEBYSCORE key -inf (now - windowMs)`.
3. The remaining count is inspected with `ZCARD key`. If count > limit, the request is rejected with `429 Too Many Requests`.

## Consequences
### Positive
- Completely smooth rate limiting with zero boundary burst vulnerabilities.
- Distributed synchronization across all API Gateway replica pods.

### Negative / Trade-offs
- Redis memory footprint proportional to request volume within the active window (optimized by short TTLs).
