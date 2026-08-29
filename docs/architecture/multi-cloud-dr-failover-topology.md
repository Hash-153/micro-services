# Multi-Cloud Disaster Recovery & Cross-Region Active-Active Topology

## 1. Cross-Cloud Infrastructure Architecture
To ensure continuous availability in the event of major cloud provider regional outages, NovaCommerce maintains automated disaster recovery cross-region replication across AWS and Google Cloud Platform (GCP).

- **Primary Cloud Host (AWS us-east-1)**: Main Kubernetes cluster hosting 9 microservices, primary PostgreSQL instances, RabbitMQ cluster, and Redis sentinel.
- **Secondary Cloud Standby (GCP us-central1)**: Warm standby Kubernetes cluster with read-replica database streaming and Patroni failover controllers.
- **DNS Routing (Cloudflare Edge)**: Global Anycast DNS monitoring synthetic health probes with automatic 10-second DNS failover.
