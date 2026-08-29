# ADR-014: Optimistic Locking Strategy for Inventory Stock Allocation

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
During high-traffic flash sales, hundreds of concurrent checkout requests may attempt to reserve stock for the same SKU simultaneously. Pessimistic row locking (`SELECT FOR UPDATE`) causes database connection pool starvation and severe throughput degradation.

## Decision
We adopt Optimistic Concurrency Control (OCC) using an incrementing `version` column for the `inventory_stocks` table.
1. When fetching stock: `SELECT on_hand_quantity, reserved_quantity, version FROM inventory_stocks WHERE sku = $1`.
2. When reserving stock: `UPDATE inventory_stocks SET reserved_quantity = reserved_quantity + $qty, version = version + 1 WHERE sku = $1 AND version = $v AND (on_hand_quantity - reserved_quantity) >= $qty`.
3. If zero rows are updated, the service retries up to 3 times with exponential jitter before returning `400 Insufficient Stock`.

## Consequences
### Positive
- High database throughput with zero long-held row locks.
- Complete protection against stock over-allocation.

### Negative / Trade-offs
- Requires retry logic in application layer on concurrent modification conflicts.
