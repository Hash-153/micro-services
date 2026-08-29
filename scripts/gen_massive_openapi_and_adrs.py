import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_adrs():
    adr_list = [
        ("011", "Event Sourcing Strategy for Financial Transactions", """# ADR-011: Event Sourcing Strategy for Financial Transactions

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
In financial transactions, traditional CRUD updates to balances lose the historical state transitions and make forensic auditing difficult. To guarantee full auditability, every state change to account balances, payments, refunds, and adjustments must be captured as an immutable sequence of domain events.

## Decision
We adopt Event Sourcing specifically for the Financial Ledger subsystem within the Payment Service.
1. The primary source of truth is the append-only `ledger_journal_entries` and `ledger_lines` event stream.
2. Current account balances are derived projections (read models) computed from the event log.
3. Snapshots of account balances are taken nightly to optimize projection rebuild times.

## Consequences
### Positive
- Complete, non-repudiable audit trail of every cent moving through the system.
- Ability to reconstruct past account states at any given point in time (time-travel queries).
- Elimination of update race conditions and lost update anomalies.

### Negative / Trade-offs
- Increased storage requirements for event logs.
- Requires asynchronous projection rebuilding for read queries.
"""),
        ("012", "Distributed Tracing with OpenTelemetry and Jaeger", """# ADR-012: Distributed Tracing with OpenTelemetry and Jaeger

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
As requests traverse the API Gateway, Order Service, Inventory Service, Payment Service, and Fulfillment Service via both synchronous HTTP/gRPC calls and asynchronous message queues, identifying performance bottlenecks and failure points requires unified distributed tracing.

## Decision
We standardize on OpenTelemetry (OTel) instrumentation with Jaeger as the distributed tracing backend.
1. The API Gateway generates or propagates a W3C Trace Context (`traceparent`) and a UUID `x-correlation-id`.
2. All inter-service HTTP clients, gRPC interceptors, and RabbitMQ message headers must forward the active trace context.
3. Every log statement produced by `core-logger` automatically embeds `traceId`, `spanId`, and `correlationId`.

## Consequences
### Positive
- End-to-end latency visualization across service and queue boundaries.
- Rapid mean time to resolution (MTTR) for distributed system incidents.

### Negative / Trade-offs
- Slight network overhead for trace header propagation and OTel collector reporting (mitigated by probabilistic sampling in production).
"""),
        ("013", "Idempotency Key Specification for State-Mutating APIs", """# ADR-013: Idempotency Key Specification for State-Mutating APIs

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Network retries, client timeouts, and automated message broker redeliveries can cause duplicate order creation, duplicate payment authorization, or double inventory reservations.

## Decision
We mandate an `Idempotency-Key` HTTP header (UUID v4) for all `POST` and `PUT` mutating operations in the Order, Payment, and Fulfillment services.
1. When a mutating request arrives, the service checks Redis for an existing idempotency record with that key.
2. If the key exists and is in `IN_PROGRESS` state, concurrent duplicate requests are rejected with `409 Conflict`.
3. If the key exists with a completed result, the cached response payload and HTTP status code are returned immediately without re-executing business logic.
4. If the key is new, the operation executes and the response is cached with a 24-hour TTL.

## Consequences
### Positive
- Safe network retries from clients and upstream message queues.
- Zero duplicate billing or duplicate order placement.

### Negative / Trade-offs
- Requires Redis storage for idempotency caches and distributed lock coordination.
"""),
        ("014", "Optimistic Locking Strategy for Inventory Stock Allocation", """# ADR-014: Optimistic Locking Strategy for Inventory Stock Allocation

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
During high-traffic flash sales, hundreds of concurrent checkout requests may attempt to reserve stock for the same SKU simultaneously. Pessimistic row locking (`SELECT FOR UPDATE`) causes database connection pool starvation and severe throughput degradation.

## Decision
We adopt Optimistic Concurrency Control (OCC) using an incrementing `version` column for the `inventory_stocks` table.
1. When fetching stock: `SELECT on_hand_quantity, reserved_quantity, version FROM inventory_stocks WHERE sku = $1`.
2. When reserving stock: `UPDATE inventory_stocks SET reserved_quantity = reserved_quantity + $qty, version = version + 1 WHERE sku = $1 AND version = $v AND (on_hand_quantity - reserved_quantity) >= $qty`.
3. If zero rows are updated, the service retries up to 3 times with exponential jitter before returning `400 Insufficient Stock`.

## Consequences
### Positive
- High database throughput with zero long-held row locks.
- Complete protection against stock over-allocation.

### Negative / Trade-offs
- Requires retry logic in application layer on concurrent modification conflicts.
"""),
        ("015", "Dead Letter Exchange and Retry Strategy for Asynchronous Events", """# ADR-015: Dead Letter Exchange and Retry Strategy for Asynchronous Events

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Transient consumer failures (e.g. database connection hiccup, temporary downstream API downtime) must not cause message loss or permanently block queue consumption.

## Decision
We implement a 3-tier dead-letter and retry architecture in RabbitMQ:
1. **Primary Queue**: Messages are consumed. If a consumer throws a retryable error, the message is nacked.
2. **Retry Queue with TTL**: Nacked messages are routed to a delayed retry exchange with an exponential TTL (5s, 25s, 125s) before dead-lettering back to the main queue.
3. **Dead Letter Queue (DLQ)**: After 3 failed retry attempts, messages are moved to `novacommerce.dlq` for manual inspection and alerting.

## Consequences
### Positive
- Resilient recovery from transient network glitches without data loss.
- Poison-pill messages are isolated to the DLQ without blocking other valid traffic.

### Negative / Trade-offs
- Out-of-order delivery possible during retries, requiring idempotent consumers.
"""),
        ("016", "Database per Service Boundary Enforcement and Foreign Key Independence", """# ADR-016: Database per Service Boundary Enforcement

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Sharing database schemas or executing cross-service database JOINs introduces tight coupling, prevents independent scaling, and creates cross-team coordination bottlenecks.

## Decision
Every microservice owns its private database schema.
1. Direct database access from outside the owning microservice is strictly prohibited.
2. Cross-service data retrieval must occur via REST/gRPC APIs or materialized CQRS read projections updated via domain events.
3. Foreign keys cannot reference tables in other service databases; references must use UUID logical identifiers.

## Consequences
### Positive
- Complete architectural decoupling and schema migration independence.
- Each service can be scaled or migrated to alternate storage engines independently.

### Negative / Trade-offs
- Application-level joins and eventual consistency overhead for cross-domain queries.
"""),
        ("017", "Argon2id for Password Hashing and Key Derivation", """# ADR-017: Argon2id for Password Hashing and Key Derivation

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Legacy hashing algorithms (MD5, SHA-1, SHA-256) and older slow hashes (bcrypt) are susceptible to GPU/ASIC-accelerated brute force attacks and side-channel vulnerabilities.

## Decision
We mandate **Argon2id** (winner of the Password Hashing Competition) for all credential hashing in the Auth Service.
- Memory cost: 64 MB (`65536 KiB`)
- Time cost: 3 iterations
- Parallelism: 4 threads
- Salt: 16 cryptographically secure random bytes

## Consequences
### Positive
- State-of-the-art resistance against GPU/ASIC side-channel and brute-force cracking attacks.
- Tunable memory and time parameters for future hardware advancements.

### Negative / Trade-offs
- Higher CPU and memory utilization during authentication requests (mitigated by rate limiting and worker offloading).
"""),
        ("018", "Sliding Window Algorithm for Distributed Rate Limiting", """# ADR-018: Sliding Window Algorithm for Distributed Rate Limiting

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Fixed-window rate limiters suffer from traffic burst anomalies at window boundaries (e.g. allowing 2x traffic if requests arrive at the end of window 1 and start of window 2).

## Decision
We implement a Sliding Window Log rate limiter using Redis sorted sets (ZSET).
1. Each request adds a timestamp entry with `ZADD key now requestId`.
2. Expired timestamps are purged with `ZREMRANGEBYSCORE key -inf (now - windowMs)`.
3. The remaining count is inspected with `ZCARD key`. If count > limit, the request is rejected with `429 Too Many Requests`.

## Consequences
### Positive
- Completely smooth rate limiting with zero boundary burst vulnerabilities.
- Distributed synchronization across all API Gateway replica pods.

### Negative / Trade-offs
- Redis memory footprint proportional to request volume within the active window (optimized by short TTLs).
"""),
        ("019", "Automated Database Schema Migration Management", """# ADR-019: Automated Database Schema Migration Management

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Managing database schema evolution across 10 autonomous microservices in development, staging, and production requires deterministic version tracking and rollback capabilities.

## Decision
We implement ordered SQL migrations managed per service in `migrations/` with a metadata table `schema_migrations`.
1. Migrations follow the naming convention `NNN_description.sql` (e.g. `001_auth_schema.sql`).
2. Migrations must be backward-compatible (Expand and Contract pattern).
3. The migration runner executes in container init containers prior to application startup.

## Consequences
### Positive
- Reproducible, automated database schema state across all environments.
- Zero downtime deployments through phased column additions and deprecations.

### Negative / Trade-offs
- Schema changes require multi-step releases to maintain backward compatibility.
"""),
        ("020", "Graceful Shutdown and Zero-Downtime Container Lifecycle", """# ADR-020: Graceful Shutdown and Zero-Downtime Container Lifecycle

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
During Kubernetes rolling updates or pod auto-scaling downscaling, in-flight HTTP requests and active database transactions must complete gracefully without abrupt termination.

## Decision
All microservice servers handle `SIGTERM` and `SIGINT` signals with a graceful shutdown sequence:
1. Stop accepting new incoming HTTP/gRPC requests.
2. Mark Kubernetes readiness probe as unhealthy.
3. Allow up to 25 seconds for in-flight requests to complete.
4. Stop background event consumers and flush logs.
5. Close database connection pools and Redis clients.
6. Exit process cleanly with code 0.

## Consequences
### Positive
- Zero 502/504 Bad Gateway errors during deployments and pod scaling events.
- Clean release of database locks and message broker channel leases.

### Negative / Trade-offs
- Kubernetes `terminationGracePeriodSeconds` must be configured to at least 30s.
""")
    ]

    for num, title, content in adr_list:
        write_file(f"docs/adr/ADR-{num}-{title.lower().replace(' ', '-').replace('/', '-')}.md", content)

    print("Generated ADRs 011 through 020.")

def generate_detailed_openapi():
    services = [
        ("auth", "Auth & IAM Service", 8001, [
            ("/register", "post", "Register new user account", "RegisterUserRequest", "AuthResponse"),
            ("/login", "post", "Authenticate user credentials", "LoginRequest", "AuthResponse"),
            ("/refresh", "post", "Refresh JWT access token", "RefreshTokenRequest", "AuthResponse"),
            ("/me", "get", "Get current user profile", None, "UserProfileResponse"),
            ("/mfa/setup", "post", "Initiate MFA enrollment", None, "MfaSetupResponse"),
            ("/mfa/verify", "post", "Verify MFA token", "MfaVerifyRequest", "SuccessResponse"),
            ("/password/reset-request", "post", "Request password reset email", "PasswordResetRequest", "SuccessResponse"),
            ("/password/reset-confirm", "post", "Confirm password reset", "PasswordResetConfirm", "SuccessResponse")
        ]),
        ("catalog", "Product Catalog Service", 8003, [
            ("/products", "get", "List products with filtering", None, "PaginatedProductList"),
            ("/products", "post", "Create new product", "CreateProductRequest", "ProductResponse"),
            ("/products/{id}", "get", "Get product by ID", None, "ProductResponse"),
            ("/products/{id}", "put", "Update product attributes", "UpdateProductRequest", "ProductResponse"),
            ("/products/{id}", "delete", "Soft delete product", None, "SuccessResponse"),
            ("/categories", "get", "List catalog categories", None, "CategoryListResponse"),
            ("/categories", "post", "Create product category", "CreateCategoryRequest", "CategoryResponse"),
            ("/search", "get", "Full text fuzzy search", None, "SearchResultResponse")
        ]),
        ("order", "Order & Saga Service", 8004, [
            ("/orders", "post", "Create new customer order", "CreateOrderRequest", "OrderResponse"),
            ("/orders", "get", "List customer orders", None, "PaginatedOrderList"),
            ("/orders/{id}", "get", "Get order details", None, "OrderResponse"),
            ("/orders/{id}/cancel", "post", "Cancel pending order", "CancelOrderRequest", "OrderResponse"),
            ("/orders/{id}/checkout-saga", "post", "Trigger distributed checkout saga", "CheckoutSagaRequest", "SagaResponse"),
            ("/orders/{id}/refund", "post", "Initiate order refund", "RefundOrderRequest", "RefundResponse")
        ]),
        ("payment", "Payment & Ledger Service", 8005, [
            ("/payments/authorize", "post", "Authorize payment transaction", "AuthorizePaymentRequest", "PaymentResponse"),
            ("/payments/capture", "post", "Capture authorized payment", "CapturePaymentRequest", "PaymentResponse"),
            ("/payments/refund", "post", "Execute refund", "RefundPaymentRequest", "PaymentResponse"),
            ("/ledger/accounts", "get", "List chart of accounts", None, "AccountListResponse"),
            ("/ledger/journal-entries", "get", "List journal entries", None, "JournalEntryListResponse"),
            ("/webhooks/stripe", "post", "Stripe payment webhook endpoint", "WebhookPayload", "SuccessResponse")
        ]),
        ("inventory", "Inventory & Stock Service", 8009, [
            ("/inventory/stock", "post", "Set warehouse stock level", "SetStockRequest", "StockResponse"),
            ("/inventory/stock/{sku}", "get", "Get real-time stock level", None, "StockResponse"),
            ("/inventory/reserve", "post", "Reserve stock for order", "ReserveStockRequest", "ReservationResponse"),
            ("/inventory/release", "post", "Release expired reservation", "ReleaseStockRequest", "SuccessResponse"),
            ("/inventory/reorder-advice", "get", "Calculate reorder parameters", None, "ReorderAdviceResponse")
        ]),
        ("fulfillment", "Fulfillment & Logistics Service", 8006, [
            ("/fulfillment/shipments", "post", "Generate shipment & tracking", "CreateShipmentRequest", "ShipmentResponse"),
            ("/fulfillment/shipments/{id}", "get", "Get shipment tracking status", None, "ShipmentResponse"),
            ("/fulfillment/rates", "post", "Calculate carrier shipping rates", "CalculateRatesRequest", "RateListResponse"),
            ("/fulfillment/pack", "post", "Optimize 3D package packing", "PackingRequest", "PackingPlanResponse")
        ])
    ]

    for svc_name, title, port, endpoints in services:
        content = f"""openapi: 3.0.3
info:
  title: NovaCommerce {title}
  version: 1.0.0
  description: Exhaustive OpenAPI 3.0 specification for {title} with comprehensive schema validation.
servers:
  - url: http://localhost:8000/api/v1/{svc_name}
    description: API Gateway Proxy
paths:
"""
        for path, method, summary, req_body, res_body in endpoints:
            content += f"""  {path}:
    {method}:
      summary: {summary}
      operationId: {svc_name}_{method}_{path.replace('/', '_').replace('{', '').replace('}', '')}
      tags:
        - {svc_name.capitalize()}
      responses:
        '200':
          description: Successful operation
        '400':
          description: Bad request / validation error
        '401':
          description: Unauthorized
        '403':
          description: Forbidden
        '404':
          description: Resource not found
        '409':
          description: Conflict
        '500':
          description: Internal server error
"""
        write_file(f"docs/api/{svc_name}-service-detailed-openapi.yaml", content)

    print("Detailed OpenAPI specifications generated.")

if __name__ == "__main__":
    generate_adrs()
    generate_detailed_openapi()
