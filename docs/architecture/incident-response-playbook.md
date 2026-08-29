# NovaCommerce Incident Response & Disaster Recovery Playbook

## 1. Severity Definitions
- **SEV-1 (Critical Outage)**: Checkout saga or payment processing down platform-wide. Response SLA: 5 minutes.
- **SEV-2 (Major Degradation)**: Single carrier integration offline or inventory reservation delays. Response SLA: 15 minutes.
- **SEV-3 (Minor Issue)**: Analytics rollup delay or non-critical notification latency. Response SLA: 2 hours.

## 2. Triage & Remediation Runbooks

### Runbook 1: Payment Gateway Outage
1. Inspect gateway latency in Prometheus: `rate(payment_gateway_duration_seconds_bucket[5m])`.
2. Trigger automated fallback to secondary processor in `PaymentGatewayRouter`.
3. Post notification to customer status page.

### Runbook 2: Saga Rollback Spike
1. Query order failure causes: `SELECT cancellation_reason, COUNT(*) FROM orders WHERE created_at > NOW() - INTERVAL '15 minutes' GROUP BY 1`.
2. If `INVENTORY_OUT_OF_STOCK` exceeds 10%, verify warehouse reservation sync locks.
