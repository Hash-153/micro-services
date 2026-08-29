# Event Streaming Performance Benchmarks: RabbitMQ vs Apache Kafka

## 1. Benchmark Methodology
We evaluated message publishing and consumption throughput under heavy simulated load (1,000,000 domain events):

| Metric | RabbitMQ (Topic Exchanges) | Apache Kafka (Partitioned Topics) | Recommendation |
|:---|:---|:---|:---|
| **P95 Publish Latency** | 1.8ms | 2.1ms | RabbitMQ for low-latency point-to-point sagas |
| **P99 Publish Latency** | 4.2ms | 5.8ms | RabbitMQ for distributed transaction workflows |
| **Consumer Throughput** | 45,000 msg/sec | 120,000 msg/sec | Kafka for massive clickstream telemetry ingestion |
| **Dead Letter Handling**| Native DLX routing | Requires custom DLQ topics | RabbitMQ for complex transactional retry policies |
