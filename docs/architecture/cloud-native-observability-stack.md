# Cloud-Native Observability Stack: Prometheus, Grafana, and Jaeger

## 1. Observability Pillars
1. **Metrics (Prometheus)**: Golden signals (Latency, Traffic, Errors, Saturation) scraped every 15s across all pods.
2. **Logs (Fluentbit & Elasticsearch)**: Structured JSON logging with `traceId`, `spanId`, and `correlationId`.
3. **Traces (OpenTelemetry & Jaeger)**: W3C distributed trace context propagated across HTTP, gRPC, and RabbitMQ message headers.
