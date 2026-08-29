# NovaCommerce Production Operations Runbook

## 1. Incident Response Matrix
- **P1: Database Unavailability**: Failover to replica, notify on-call SRE.
- **P2: Message Broker Queue Spike**: Scale consumer pods horizontally via HPA.
- **P3: Payment Gateway Degraded**: Switch to secondary mock fallback adapter.

## 2. Disaster Recovery Procedures
1. Restore PostgreSQL schema backups per service.
2. Replay uncommitted outbox events from RabbitMQ dead-letter queues.
3. Validate financial ledger balance invariant via `npm run test:ledger`.
