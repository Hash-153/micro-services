import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_root_files():
    # .gitignore
    write_file(".gitignore", """
# Node & Dependencies
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# Build outputs & caches
dist/
build/
out/
.next/
.nuxt/
.turbo/
*.tsbuildinfo
.eslintcache

# Environment & Sensitive configurations
.env
.env.local
.env.development.local
.env.test.local
.env.production.local
*.pem
*.key
*.cert
*.crt
id_rsa
secrets/
credentials.json

# Test & Coverage
coverage/
.nyc_output/
*.lcov
test-results/

# Python artifacts
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.venv/
venv/
ENV/
env/
dist_py/
*.egg-info/

# IDE & OS
.idea/
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Docker & local data volumes
docker/data/
pgdata/
redisdata/
rabbitmqdata/
""")

    # .env.example
    write_file(".env.example", """
# ==============================================================================
# NovaCommerce Distributed Platform - Environment Configuration Template
# NOTE: Copy this file to .env for local development. Never commit real credentials.
# ==============================================================================

# Global Environment
NODE_ENV=development
LOG_LEVEL=debug
APP_NAME=novacommerce-platform
CLUSTER_REGION=us-east-1

# API Gateway Configuration
GATEWAY_PORT=8000
GATEWAY_HOST=0.0.0.0
GATEWAY_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
GATEWAY_RATE_LIMIT_WINDOW_MS=60000
GATEWAY_RATE_LIMIT_MAX_REQUESTS=1000

# Auth & IAM Service
AUTH_SERVICE_PORT=8001
AUTH_SERVICE_GRPC_PORT=50051
AUTH_DB_HOST=localhost
AUTH_DB_PORT=5432
AUTH_DB_NAME=novacommerce_auth
AUTH_DB_USER=novacommerce_user
AUTH_DB_PASSWORD=local_development_password_only
JWT_SECRET=super_secret_local_jwt_signing_key_min_32_characters_long
JWT_ACCESS_EXPIRATION=15m
JWT_REFRESH_EXPIRATION=7d
ARGON2_MEMORY_COST=65536
ARGON2_TIME_COST=3
ARGON2_PARALLELISM=4

# User Service
USER_SERVICE_PORT=8002
USER_SERVICE_GRPC_PORT=50052
USER_DB_HOST=localhost
USER_DB_PORT=5432
USER_DB_NAME=novacommerce_user_db
USER_DB_USER=novacommerce_user
USER_DB_PASSWORD=local_development_password_only

# Product & Catalog Service
CATALOG_SERVICE_PORT=8003
CATALOG_SERVICE_GRPC_PORT=50053
CATALOG_DB_HOST=localhost
CATALOG_DB_PORT=5432
CATALOG_DB_NAME=novacommerce_catalog
CATALOG_DB_USER=novacommerce_user
CATALOG_DB_PASSWORD=local_development_password_only

# Order Service & Saga Orchestrator
ORDER_SERVICE_PORT=8004
ORDER_SERVICE_GRPC_PORT=50054
ORDER_DB_HOST=localhost
ORDER_DB_PORT=5432
ORDER_DB_NAME=novacommerce_orders
ORDER_DB_USER=novacommerce_user
ORDER_DB_PASSWORD=local_development_password_only
SAGA_TIMEOUT_MS=30000
SAGA_MAX_RETRIES=3

# Payment & Ledger Service
PAYMENT_SERVICE_PORT=8005
PAYMENT_SERVICE_GRPC_PORT=50055
PAYMENT_DB_HOST=localhost
PAYMENT_DB_PORT=5432
PAYMENT_DB_NAME=novacommerce_payments
PAYMENT_DB_USER=novacommerce_user
PAYMENT_DB_PASSWORD=local_development_password_only
MOCK_STRIPE_SECRET_KEY=sk_test_mock_stripe_sandbox_key_for_dev_mode
MOCK_PAYPAL_CLIENT_ID=sandbox_paypal_client_id_dev

# Fulfillment & Logistics Service
FULFILLMENT_SERVICE_PORT=8006
FULFILLMENT_SERVICE_GRPC_PORT=50056
FULFILLMENT_DB_HOST=localhost
FULFILLMENT_DB_PORT=5432
FULFILLMENT_DB_NAME=novacommerce_fulfillment
FULFILLMENT_DB_USER=novacommerce_user
FULFILLMENT_DB_PASSWORD=local_development_password_only

# Notification Service
NOTIFICATION_SERVICE_PORT=8007
NOTIFICATION_SERVICE_GRPC_PORT=50057
NOTIFICATION_DB_HOST=localhost
NOTIFICATION_DB_PORT=5432
NOTIFICATION_DB_NAME=novacommerce_notifications
NOTIFICATION_DB_USER=novacommerce_user
NOTIFICATION_DB_PASSWORD=local_development_password_only
SMTP_HOST=localhost
SMTP_PORT=1025
SMTP_USER=mock_smtp_user
SMTP_PASS=mock_smtp_password
SMTP_FROM_EMAIL=noreply@novacommerce.io

# Analytics & Audit Service
ANALYTICS_SERVICE_PORT=8008
ANALYTICS_SERVICE_GRPC_PORT=50058
ANALYTICS_DB_HOST=localhost
ANALYTICS_DB_PORT=5432
ANALYTICS_DB_NAME=novacommerce_analytics
ANALYTICS_DB_USER=novacommerce_user
ANALYTICS_DB_PASSWORD=local_development_password_only

# Inventory Service
INVENTORY_SERVICE_PORT=8009
INVENTORY_SERVICE_GRPC_PORT=50059
INVENTORY_DB_HOST=localhost
INVENTORY_DB_PORT=5432
INVENTORY_DB_NAME=novacommerce_inventory
INVENTORY_DB_USER=novacommerce_user
INVENTORY_DB_PASSWORD=local_development_password_only

# Distributed Cache & Message Broker
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
RABBITMQ_URL=amqp://guest:guest@localhost:5672
RABBITMQ_MANAGEMENT_URL=http://localhost:15672

# Observability & Tracing
JAEGER_AGENT_HOST=localhost
JAEGER_AGENT_PORT=6831
PROMETHEUS_METRICS_ENABLED=true
PROMETHEUS_METRICS_PATH=/metrics
""")

    # package.json
    write_file("package.json", """{
  "name": "novacommerce-platform",
  "version": "1.0.0",
  "description": "Enterprise-Scale Distributed Microservices E-Commerce & Logistics Platform",
  "author": "NovaCommerce Core Platform Engineering",
  "private": true,
  "workspaces": [
    "packages/*",
    "services/*",
    "sdks/typescript"
  ],
  "scripts": {
    "build": "npm run build --workspaces --if-present",
    "test": "npm run test --workspaces --if-present",
    "test:coverage": "npm run test:coverage --workspaces --if-present",
    "lint": "npm run lint --workspaces --if-present",
    "typecheck": "npm run typecheck --workspaces --if-present",
    "clean": "npm run clean --workspaces --if-present",
    "seed": "ts-node scripts/seed.ts",
    "benchmark": "ts-node scripts/benchmark.ts",
    "docker:up": "docker compose -f docker/docker-compose.yml up -d",
    "docker:down": "docker compose -f docker/docker-compose.yml down",
    "docker:logs": "docker compose -f docker/docker-compose.yml logs -f",
    "count:loc": "python scripts/count_loc.py"
  },
  "devDependencies": {
    "@types/node": "^22.0.0",
    "typescript": "^5.4.0",
    "ts-node": "^10.9.2",
    "jest": "^29.7.0",
    "@types/jest": "^29.5.12",
    "ts-jest": "^29.1.2",
    "rimraf": "^5.0.5"
  },
  "engines": {
    "node": ">=20.0.0",
    "npm": ">=10.0.0"
  }
}""")

    # tsconfig.json
    write_file("tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "composite": true,
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "esModuleInterop": true,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "exclude": [
    "node_modules",
    "dist",
    "coverage",
    "sdks/python"
  ]
}""")

    # README.md
    write_file("README.md", """# NovaCommerce Distributed Microservices Platform

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
""")

    # LICENSE
    write_file("LICENSE", """MIT License

Copyright (c) 2026 NovaCommerce Engineering Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""")

    # .github/workflows/ci-cd.yaml
    write_file(".github/workflows/ci-cd.yaml", """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  lint-and-typecheck:
    name: Lint & Typecheck
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Setup Node.js Environment
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Run Workspace Typecheck
        run: npm run typecheck

  unit-tests:
    name: Unit & Integration Tests
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Setup Node.js Environment
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Build Shared Packages
        run: npm run build

      - name: Execute Test Matrix
        run: npm test

  security-scan:
    name: Security Vulnerability Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Audit NPM Dependencies
        run: npm audit --audit-level=high

  docker-build-verification:
    name: Docker Container Build Verification
    runs-on: ubuntu-latest
    needs: [lint-and-typecheck, unit-tests]
    strategy:
      matrix:
        service:
          - api-gateway
          - auth-service
          - user-service
          - catalog-service
          - order-service
          - payment-service
          - fulfillment-service
          - notification-service
          - analytics-service
          - inventory-service
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4

      - name: Build Docker Container
        run: |
          docker build -f services/${{ matrix.service }}/Dockerfile -t novacommerce/${{ matrix.service }}:latest .
""")

    # .github/workflows/lint-and-test.yaml
    write_file(".github/workflows/lint-and-test.yaml", """name: Code Quality & Security

on:
  pull_request:
    branches: [ main, develop ]

jobs:
  static-analysis:
    name: ESLint & TypeScript Checking
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck

  test-coverage:
    name: Jest Test Coverage Suite
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - run: npm run test:coverage
""")

    # .github/workflows/release.yaml
    write_file(".github/workflows/release.yaml", """name: Production Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  publish-packages:
    name: Build & Tag Container Artifacts
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npm run build
      - run: npm test
""")

if __name__ == "__main__":
    generate_root_files()
    print("Root files generated successfully.")
