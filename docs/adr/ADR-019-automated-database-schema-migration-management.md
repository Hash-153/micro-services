# ADR-019: Automated Database Schema Migration Management

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Managing database schema evolution across 10 autonomous microservices in development, staging, and production requires deterministic version tracking and rollback capabilities.

## Decision
We implement ordered SQL migrations managed per service in `migrations/` with a metadata table `schema_migrations`.
1. Migrations follow the naming convention `NNN_description.sql` (e.g. `001_auth_schema.sql`).
2. Migrations must be backward-compatible (Expand and Contract pattern).
3. The migration runner executes in container init containers prior to application startup.

## Consequences
### Positive
- Reproducible, automated database schema state across all environments.
- Zero downtime deployments through phased column additions and deprecations.

### Negative / Trade-offs
- Schema changes require multi-step releases to maintain backward compatibility.
