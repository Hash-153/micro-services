# SRE Observability, Service Level Indicators (SLIs), and SLOs

## 1. Service Level Objectives (SLOs)

| Microservice | Target Availability (SLO) | Latency P95 Target | Latency P99 Target | Error Budget (Monthly) |
|:---|:---|:---|:---|:---|
| **API Gateway** | 99.99% | < 15ms | < 45ms | 4.38 minutes downtime |
| **Auth Service** | 99.95% | < 40ms | < 120ms | 21.92 minutes downtime |
| **Catalog Service** | 99.95% | < 25ms | < 80ms | 21.92 minutes downtime |
| **Order Service** | 99.90% | < 80ms | < 250ms | 43.83 minutes downtime |
| **Payment Service** | 99.95% | < 150ms | < 500ms | 21.92 minutes downtime |
| **Inventory Service**| 99.95% | < 30ms | < 90ms | 21.92 minutes downtime |
