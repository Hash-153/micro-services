# NovaCommerce Distributed Microservices Platform

[![CI/CD Pipeline](https://github.com/Hash-153/micro-services/actions/workflows/ci-cd.yaml/badge.svg)](https://github.com/Hash-153/micro-services/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4-blue.svg)](https://www.typescriptlang.org/)
[![Node.js](https://img.shields.io/badge/Node.js-22.x-green.svg)](https://nodejs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-3.13-orange.svg)](https://www.rabbitmq.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.29-blue.svg)](https://kubernetes.io/)

NovaCommerce is an enterprise-grade, distributed microservices platform engineered for high-throughput digital commerce, real-time inventory management, distributed multi-step saga checkout workflows, double-entry financial ledger settlement, and omni-channel logistics fulfillment.

---

## Architecture Overview

NovaCommerce employs a **Domain-Driven Design (DDD)** and **Event-Driven Architecture (EDA)** pattern with complete database isolation per microservice.

```
                                  +-----------------------+
                                  |   API Gateway (REST)  |
                                  |   (Port 8000)         |
                                  +-----------+-----------+
                                              |
                     +------------------------+------------------------+
                     |                        |                        |
             +-------v-------+        +-------v-------+        +-------v-------+
             | Auth & IAM    |        | User Profile  |        | Product &     |
             | Service       |        | Service       |        | Catalog Svc   |
             | (Port 8001)   |        | (Port 8002)   |        | (Port 8003)   |
             +-------+-------+        +-------+-------+        +-------+-------+
                     |                        |                        |
             +-------v-------+        +-------v-------+        +-------v-------+
             | Order & Saga  |        | Payment &     |        | Fulfillment   |
             | Service       |        | Ledger Svc    |        | & Logistics   |
             | (Port 8004)   |        | (Port 8005)   |        | (Port 8006)   |
             +-------+-------+        +-------+-------+        +-------+-------+
                     |                        |                        |
             +-------v-------+        +-------v-------+        +-------v-------+
             | Notification  |        | Analytics &   |        | Inventory     |
             | Service       |        | Audit Svc     |        | Service       |
             | (Port 8007)   |        | (Port 8008)   |        | (Port 8009)   |
             +-------+-------+        +-------+-------+        +-------+-------+
                     |                        |                        |
                     +------------------------+------------------------+
                                              |
                               +--------------v--------------+
                               | Event Broker (RabbitMQ)     |
                               | Shared Outbox & DLQ Bus     |
                               +-----------------------------+
```

---

## Key Microservices

| Service | Port (HTTP/gRPC) | Core Domain Responsibility | Data Storage |
|:---|:---|:---|:---|
| **API Gateway** | `8000` | Rate limiting, JWT validation, intelligent proxy routing, request aggregation | Redis (Rate Limiting) |
| **Auth & IAM** | `8001` / `50051` | Argon2id hashing, JWT access/refresh tokens, RBAC, OAuth2/OIDC, MFA | PostgreSQL (`novacommerce_auth`) |
| **User Service** | `8002` / `50052` | User profiles, organizations, address books, preferences, KYC verification | PostgreSQL (`novacommerce_user_db`) |
| **Catalog Service** | `8003` / `50053` | Products, variants, categories, dynamic attributes, pricing tiers, search | PostgreSQL (`novacommerce_catalog`) |
| **Inventory Service** | `8009` / `50059` | Stock allocation, warehouse bin tracking, reservation locking, reorder levels | PostgreSQL (`novacommerce_inventory`) |
| **Order Service** | `8004` / `50054` | Order lifecycle, Checkout Saga Orchestrator, State machine, Tax & discount engine | PostgreSQL (`novacommerce_orders`) |
| **Payment Service** | `8005` / `50055` | Payment gateway adapters, double-entry financial ledger, idempotent refunds | PostgreSQL (`novacommerce_payments`) |
| **Fulfillment Service**| `8006` / `50056` | Carrier rate calculation, dispatch schedules, package dimensioning, tracking | PostgreSQL (`novacommerce_fulfillment`) |
| **Notification Svc** | `8007` / `50057` | Multi-channel dispatch (Email, SMS, Webhook), template rendering, batching | PostgreSQL (`novacommerce_notifications`) |
| **Analytics Service** | `8008` / `50058` | Clickstream ingestion, audit compliance logs, rollups, business intelligence | PostgreSQL (`novacommerce_analytics`) |

---

## Architectural Highlights

### 1. Distributed Saga Orchestration
Checkout transactions span multiple autonomous services (`Order` -> `Inventory` -> `Payment` -> `Fulfillment`). The **Order Saga Orchestrator** manages the forward workflow and reliably triggers compensating transactions (release inventory reservation, refund authorized payment, void shipment) in the event of partial system failure or card decline.

### 2. Transactional Outbox Pattern
Guarantees **at-least-once delivery** of domain events by writing events to a persistent `outbox_events` table inside the same local database transaction as business entities, preventing dual-write inconsistencies.

### 3. Financial Double-Entry Ledger
All monetary operations in the Payment service are backed by immutable double-entry journal entries (debits and credits) ensuring that total debits always equal total credits for zero-loss financial auditing.

### 4. Zero-Trust Security & RBAC
Every microservice independently validates incoming JWT tokens, evaluates contextual RBAC permissions (`admin`, `manager`, `customer`, `system_service`), and rejects unauthenticated inter-service traffic.

---

## Repository Structure

```
├── .github/workflows/         # CI/CD GitHub Actions pipelines
├── docker/                    # Docker Compose mesh, Prometheus, Grafana, RabbitMQ configs
├── k8s/                       # Kubernetes manifests (Deployments, Services, Ingress, HPA)
│   ├── base/
│   ├── services/
│   └── helm/
├── proto/                     # Protobuf v3 contracts for high-performance gRPC
├── packages/                  # Reusable Core Enterprise Libraries
│   ├── core-types/            # Canonical domain models, DTOs, Enums, Error definitions
│   ├── core-logger/           # Structured JSON logger with distributed correlation IDs
│   ├── core-events/           # RabbitMQ broker, Outbox processor, Dead Letter Queues (DLQ)
│   ├── core-middleware/       # Auth guards, Rate limiters, Joi/Zod validators, Error handling
│   ├── core-database/         # PostgreSQL connection pool, Base repositories, Unit of Work
│   └── core-grpc/             # Interceptors, client connection pooling, metadata propagation
├── services/                  # Autonomous Business Microservices (9 distinct services + Gateway)
├── migrations/                # Schema DDL SQL migrations per service
├── sdks/                      # Developer Client SDKs
│   ├── typescript/            # Typed TypeScript SDK with exponential backoff & retry
│   └── python/                # Async Python Client SDK with Pydantic models
├── docs/                      # Technical Documentation
│   ├── adr/                   # Architecture Decision Records (ADR 001 - ADR 010)
│   ├── api/                   # OpenAPI 3.0 specs for each service
│   └── architecture/          # Deep-dive design guides, sequence diagrams, runbooks
└── scripts/                   # Database seeders, benchmark runners, LOC counters
```

---

## Getting Started

### Prerequisites
- **Node.js**: v20.x or v22.x+
- **Docker & Docker Compose**: v2.20+
- **Python**: v3.10+ (for Python SDK & verification scripts)

### 1. Clone & Configure Environment
```bash
git clone https://github.com/Hash-153/micro-services.git
cd micro-services
cp .env.example .env
```

### 2. Install Dependencies & Build Packages
```bash
npm install
npm run build
```

### 3. Launch Local Infrastructure (Docker Compose)
```bash
npm run docker:up
```
This spins up:
- 10 Isolated PostgreSQL Database Instances (or multi-tenant schemas)
- RabbitMQ Message Broker with Management UI on port `15672`
- Redis Cache on port `6379`
- Prometheus Metrics Server on port `9090`
- Grafana Dashboards on port `3001`
- MailHog Sandbox SMTP Server on port `8025`

### 4. Run Test Suites
```bash
npm run test
```

### 5. Seed Test Data
```bash
npm run seed
```

---

## CI/CD & Production Deployment

All services include production-ready Dockerfiles, Kubernetes manifests, and Helm charts.
CI/CD workflows automatically execute:
1. Static code analysis & Typechecking
2. Unit and Integration test matrices
3. Security vulnerability auditing & dependency scanning
4. Docker image builds & Helm chart validation

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
