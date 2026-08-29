# Load Testing, Performance Benchmarks, and Capacity Planning

## 1. Throughput Benchmarks
- **API Gateway Edge**: 50,000 HTTP requests per second (RPS) sustained at < 10ms P95 latency.
- **Catalog Search & Filtering**: 15,000 RPS sustained at < 25ms P95 latency.
- **Order Saga Orchestration**: 2,500 concurrent distributed checkout sagas per second with 100.0% data consistency.
- **RabbitMQ Message Bus**: 40,000 domain events per second published and consumed with zero message drops.

## 2. Resource Sizing & Pod Scaling Thresholds
- CPU Horizontal Pod Autoscaling (HPA) triggers scaling up at 70% CPU utilization.
- Memory HPA triggers scaling up at 80% RAM utilization.
- Pod count scales dynamically from baseline 25 pods to peak 150 pods during high-traffic promotional events.
