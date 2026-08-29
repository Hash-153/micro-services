# ADR-011: Event Sourcing Strategy for Financial Transactions

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
In financial transactions, traditional CRUD updates to balances lose the historical state transitions and make forensic auditing difficult. To guarantee full auditability, every state change to account balances, payments, refunds, and adjustments must be captured as an immutable sequence of domain events.

## Decision
We adopt Event Sourcing specifically for the Financial Ledger subsystem within the Payment Service.
1. The primary source of truth is the append-only `ledger_journal_entries` and `ledger_lines` event stream.
2. Current account balances are derived projections (read models) computed from the event log.
3. Snapshots of account balances are taken nightly to optimize projection rebuild times.

## Consequences
### Positive
- Complete, non-repudiable audit trail of every cent moving through the system.
- Ability to reconstruct past account states at any given point in time (time-travel queries).
- Elimination of update race conditions and lost update anomalies.

### Negative / Trade-offs
- Increased storage requirements for event logs.
- Requires asynchronous projection rebuilding for read queries.
