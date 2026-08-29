# ADR-146: Multi-Tenant Database Row-Level Security Policies in PostgreSQL

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context & Problem Statement
Operating an enterprise-scale distributed commerce platform requires formalizing architectural standards across domain boundaries to guarantee operational stability, security, and developer velocity.

## Decision
We formally adopt **Multi-Tenant Database Row-Level Security Policies in PostgreSQL**.
Enforce `CREATE POLICY tenant_isolation_policy ON organizations USING (id = current_setting('app.current_org_id')::UUID)`.

### Key Architectural Guidelines:
1. **Domain Isolation**: Each microservice maintains complete encapsulation over its private domain models and databases.
2. **Resilience & Fault Isolation**: Service failures are isolated through circuit breakers, retry with backoff, and compensating saga workflows.
3. **Auditability**: Every transaction and mutation is recorded with immutable timestamps and correlation context.

## Consequences & Trade-offs
### Positive:
- High horizontal scalability, zero data loss, and predictable system performance.
- Full compliance with enterprise security, PCI-DSS Level 1, and SOX frameworks.

### Negative:
- Continuous review and adherence required in code reviews and CI/CD pipelines.
