# ADR-022: Zero-Trust Service-to-Service mTLS and JWT Forwarding

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
As NovaCommerce expands horizontally to support millions of monthly active shoppers, clear architectural standardization across all engineering squads is essential to ensure operational stability, security, and developer velocity.

## Summary & Decision
All internal microservice RPC calls must validate mutual TLS and forward user identity context.

### Key Principles:
1. **Consistency**: All microservices follow identical design patterns and coding conventions.
2. **Measurability**: Every architectural decision is monitored through real-time Prometheus SLIs.
3. **Resilience**: Failures are isolated to bounded contexts without cascading service degradation.

## Consequences
- **Positive**: High predictability in production operations and rapid onboarding.
- **Negative**: Strict architectural review requirements for cross-cutting modifications.
