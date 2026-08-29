# ADR-121: Dynamic Currency Symbol Formatting and Locale-Aware Pricing

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context & Problem Statement
NovaCommerce operates as a mission-critical enterprise commerce platform. Formalizing domain boundaries, resilience policies, and mathematical consistency guarantees operational excellence and high developer velocity.

## Decision
We formally adopt **Dynamic Currency Symbol Formatting and Locale-Aware Pricing**.
Format currency values according to customer browser locale (e.g. $1,234.56 vs 1.234,56 €).

### Key Principles:
1. **Zero Data Loss**: Every financial transaction and inventory allocation is guaranteed by ACID transactions and distributed saga compensation.
2. **Deterministic Behavior**: State transitions follow validated mathematical state machines and cryptographic invariant checks.
3. **Observability**: Distributed traces, structured JSON telemetry, and Prometheus metrics provide real-time operational visibility.

## Consequences & Trade-offs
### Positive:
- Uncompromising reliability and horizontal scalability across global regions.
- Clear architectural boundaries facilitating independent squad velocity.
- Full compliance with PCI-DSS Level 1, GDPR, and SOX enterprise regulatory frameworks.

### Negative:
- Strict architectural compliance required in pull requests and deployment gates.
