# Multi-Region Database Replication & High Availability Architecture

## 1. Topography & Geographic Distribution
NovaCommerce implements an active-primary, multi-region read-replica database architecture across three primary availability zones:
- **US-East (Primary Leader)**: Handles all write transactions, saga orchestration, payment authorizations, and outbox event commitments.
- **US-West (Read Replica)**: Serves low-latency product catalog queries, customer profile lookups, and inventory availability checks.
- **EU-Central (Read Replica)**: Serves European storefront browsing and localized pricing queries with sub-20ms latency.

```
                    +-------------------------------------+
                    |       Primary Write Leader          |
                    |         (Region: us-east-1)         |
                    +------------------+------------------+
                                       |
                 +---------------------+---------------------+
                 | (Streaming WAL Sync)| (Streaming WAL Sync)|
                 v                     v                     v
       +-------------------+ +-------------------+ +-------------------+
       | Local Read Replica| | US-West Replica   | | EU-Central Replica|
       | (us-east-1b)      | | (us-west-2a)      | | (eu-central-1a)   |
       +-------------------+ +-------------------+ +-------------------+
```

## 2. Failover Protocol
1. Health checkers probe primary leader every 3 seconds.
2. If primary fails 3 consecutive health checks, Patroni / Kubernetes operator promotes the synchronized standby replica in `us-east-1b` to Primary Leader.
3. DNS and API Gateway connection pools fail over automatically within 8 seconds with zero data loss (RPO = 0).
