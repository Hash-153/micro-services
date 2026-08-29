# ADR-062: Sliding-Window Rate Limiting Tiering for API Consumers

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context & Problem Statement
In an enterprise-scale distributed e-commerce and logistics platform supporting high-concurrency order throughput, formalizing architectural standards across domain boundaries guarantees system predictability and operational stability.

## Decision
We formally adopt **Sliding-Window Rate Limiting Tiering for API Consumers**.
Differentiate rate limiting tiers: Anonymous (60 rpm), Authenticated Customer (300 rpm), Partner API (1200 rpm).

### Key Architectural Tenets:
1. **Zero Data Loss**: Every financial transaction and inventory allocation is guaranteed by ACID transactions and distributed saga compensation.
2. **Deterministic Behavior**: State transitions follow validated mathematical state machines and cryptographic invariant checks.
3. **Observability**: Distributed traces, structured JSON telemetry, and Prometheus metrics provide real-time operational visibility.

## Consequences & Trade-offs
- **Positive**: High horizontal scalability, verifiable data consistency, and robust disaster recovery posture.
- **Negative**: Requires strict compliance checks in CI/CD automated linting and code review pipelines.
