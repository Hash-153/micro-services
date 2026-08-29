# NovaCommerce Disaster Recovery: Comprehensive Step-by-Step Operations Runbook

## 1. Incident Classification & Activation Protocol
- **RTO (Recovery Time Objective)**: 15 minutes maximum service restoration.
- **RPO (Recovery Point Objective)**: Zero data loss for settled financial ledger records and orders.

## 2. Emergency Failover Procedure (Primary Leader Outage)
1. **Detect Outage**: PagerDuty triggers SEV-1 incident upon 3 failed Prometheus health probes.
2. **Promote Standby Database**:
   ```bash
   patronictl -c /etc/patroni/config.yml failover novacommerce-cluster --candidate us-east-1b-replica
   ```
3. **Update API Gateway Connection Pools**:
   API Gateway dynamically discovers new leader endpoint via Kubernetes CoreDNS within 5 seconds.
4. **Replay Unprocessed Outbox Events**:
   Execute outbox recovery worker to publish pending events from `outbox_events` table.
5. **Verify Financial Balance**:
   Run `npm run test:ledger` to verify that all double-entry ledger accounts maintain zero drift.
