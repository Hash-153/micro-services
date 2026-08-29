# High-Availability Database Failover Topology & Zero-Data-Loss Invariants

## 1. Topography & Geographic Distribution
NovaCommerce implements an active-primary, multi-region read-replica database architecture:
- **Primary Leader**: Handles all write transactions, saga orchestration, payment authorizations, and outbox event commitments.
- **Synchronized Standby**: Streamed write-ahead logs (WAL) ensure Recovery Point Objective (RPO) = 0.
- **Automated Failover**: Patroni promotes standby to leader within 8 seconds upon detecting primary failure.
