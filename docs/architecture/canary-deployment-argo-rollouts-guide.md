# Zero-Downtime Canary Deployments with Argo Rollouts

## 1. Traffic Shifting Schedule
- **Step 1**: Route 10% traffic to Canary pods. Observe Prometheus 5xx error rate for 5 minutes.
- **Step 2**: Route 25% traffic to Canary pods. Evaluate P99 latency SLO (< 100ms) for 5 minutes.
- **Step 3**: Route 50% traffic to Canary pods. Evaluate conversion funnel completion rate.
- **Step 4**: Promote Canary to 100% stable production release.

## 2. Automated Rollback Criteria
If any of the following conditions trigger during canary verification, Argo Rollouts immediately halts and restores 100% traffic to stable version:
1. `rate(http_requests_total{status=~"5.."}[2m]) > 0.01` (Error rate > 1%).
2. `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[2m])) > 0.500` (P99 Latency > 500ms).
