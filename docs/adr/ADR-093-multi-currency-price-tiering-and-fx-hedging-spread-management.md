# ADR-093: Multi-Currency Price Tiering and FX Hedging Spread Management

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context & Problem Statement
Operating a distributed enterprise microservices architecture across high-throughput transactional domains requires uncompromising engineering rigor, deterministic state handling, and zero tolerance for data anomalies.

## Decision
We formally adopt **Multi-Currency Price Tiering and FX Hedging Spread Management**.
Calculate localized storefront prices using real-time FX rates with configurable merchant hedging spread.

### Key Architectural Guidelines:
1. **Domain Isolation**: Each microservice maintains complete authority over its domain models, persistence tables, and validation invariants.
2. **Resilience & Self-Healing**: Transient downstream failures are mitigated through circuit breakers, retry with exponential backoff, and distributed saga compensations.
3. **Auditability & Observability**: Every business state transition produces distributed tracing context and immutable telemetry records.

## Consequences & Trade-offs
### Positive:
- Uncompromising system reliability and horizontal scalability.
- Clean architectural boundaries facilitating autonomous team velocity.
- Comprehensive compliance with enterprise security and regulatory standards.

### Negative:
- Strict architectural discipline required during design reviews and code deployment.
