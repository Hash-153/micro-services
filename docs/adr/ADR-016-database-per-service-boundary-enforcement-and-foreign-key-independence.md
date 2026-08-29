# ADR-016: Database per Service Boundary Enforcement

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Sharing database schemas or executing cross-service database JOINs introduces tight coupling, prevents independent scaling, and creates cross-team coordination bottlenecks.

## Decision
Every microservice owns its private database schema.
1. Direct database access from outside the owning microservice is strictly prohibited.
2. Cross-service data retrieval must occur via REST/gRPC APIs or materialized CQRS read projections updated via domain events.
3. Foreign keys cannot reference tables in other service databases; references must use UUID logical identifiers.

## Consequences
### Positive
- Complete architectural decoupling and schema migration independence.
- Each service can be scaled or migrated to alternate storage engines independently.

### Negative / Trade-offs
- Application-level joins and eventual consistency overhead for cross-domain queries.
