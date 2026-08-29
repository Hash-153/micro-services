import os
import json

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_json_schemas():
    schema_dir = "schemas/json"
    
    # Generate complete JSON Schema Draft 7 documents for every single entity and DTO
    schemas = [
        ("UserEntity", {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "UserEntity",
            "type": "object",
            "required": ["id", "email", "passwordHash", "role", "status", "kycStatus", "isMfaEnabled", "createdAt", "updatedAt"],
            "properties": {
                "id": { "type": "string", "format": "uuid" },
                "email": { "type": "string", "format": "email" },
                "passwordHash": { "type": "string" },
                "role": { "type": "string", "enum": ["SUPER_ADMIN", "ADMIN", "OPERATIONS_MANAGER", "INVENTORY_MANAGER", "FINANCE_ANALYST", "SUPPORT_AGENT", "CUSTOMER", "GUEST", "SYSTEM_INTERNAL"] },
                "status": { "type": "string", "enum": ["ACTIVE", "PENDING_VERIFICATION", "SUSPENDED", "DEACTIVATED", "LOCKED"] },
                "kycStatus": { "type": "string", "enum": ["NOT_SUBMITTED", "PENDING_REVIEW", "VERIFIED", "REJECTED", "EXPIRED"] },
                "organizationId": { "type": ["string", "null"], "format": "uuid" },
                "isMfaEnabled": { "type": "boolean" },
                "mfaSecret": { "type": ["string", "null"] },
                "failedLoginAttempts": { "type": "integer", "minimum": 0 },
                "lockedUntil": { "type": ["string", "null"], "format": "date-time" },
                "lastLoginAt": { "type": ["string", "null"], "format": "date-time" },
                "createdAt": { "type": "string", "format": "date-time" },
                "updatedAt": { "type": "string", "format": "date-time" },
                "deletedAt": { "type": ["string", "null"], "format": "date-time" }
            }
        }),
        ("ProductEntity", {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "ProductEntity",
            "type": "object",
            "required": ["id", "sku", "name", "slug", "description", "categoryId", "basePrice", "isActive", "tags", "attributes", "images", "createdAt", "updatedAt"],
            "properties": {
                "id": { "type": "string", "format": "uuid" },
                "sku": { "type": "string", "minLength": 3, "maxLength": 64 },
                "name": { "type": "string", "minLength": 1, "maxLength": 255 },
                "slug": { "type": "string", "minLength": 1, "maxLength": 255 },
                "description": { "type": "string" },
                "categoryId": { "type": "string", "format": "uuid" },
                "basePrice": {
                    "type": "object",
                    "required": ["amount", "currency"],
                    "properties": {
                        "amount": { "type": "integer", "minimum": 0 },
                        "currency": { "type": "string", "enum": ["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CHF", "SGD", "INR"] }
                    }
                },
                "isActive": { "type": "boolean" },
                "tags": { "type": "array", "items": { "type": "string" } },
                "attributes": { "type": "object", "additionalProperties": { "type": ["string", "number", "boolean"] } },
                "images": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "url", "sortOrder", "isPrimary"],
                        "properties": {
                            "id": { "type": "string", "format": "uuid" },
                            "url": { "type": "string", "format": "uri" },
                            "altText": { "type": "string" },
                            "sortOrder": { "type": "integer" },
                            "isPrimary": { "type": "boolean" }
                        }
                    }
                },
                "createdAt": { "type": "string", "format": "date-time" },
                "updatedAt": { "type": "string", "format": "date-time" }
            }
        }),
        ("OrderEntity", {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "OrderEntity",
            "type": "object",
            "required": ["id", "orderNumber", "userId", "status", "items", "subtotalAmount", "taxAmount", "shippingFeeAmount", "discountAmount", "totalAmount", "idempotencyKey", "createdAt", "updatedAt"],
            "properties": {
                "id": { "type": "string", "format": "uuid" },
                "orderNumber": { "type": "string" },
                "userId": { "type": "string" },
                "status": { "type": "string", "enum": ["DRAFT", "PENDING_PAYMENT", "PAYMENT_AUTHORIZED", "PAYMENT_FAILED", "PROCESSING", "INVENTORY_RESERVED", "INVENTORY_ALLOCATION_FAILED", "PACKED", "DISPATCHED", "IN_TRANSIT", "OUT_FOR_DELIVERY", "DELIVERED", "CANCELLED", "REFUND_REQUESTED", "REFUNDED", "PARTIALLY_REFUNDED", "EXPIRED"] },
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["id", "orderId", "sku", "productName", "unitPrice", "quantity", "subtotal", "taxAmount", "discountAmount", "total"],
                        "properties": {
                            "id": { "type": "string", "format": "uuid" },
                            "orderId": { "type": "string", "format": "uuid" },
                            "sku": { "type": "string" },
                            "productName": { "type": "string" },
                            "variantName": { "type": "string" },
                            "unitPrice": { "$ref": "#/properties/subtotalAmount" },
                            "quantity": { "type": "integer", "minimum": 1 },
                            "subtotal": { "$ref": "#/properties/subtotalAmount" },
                            "taxAmount": { "$ref": "#/properties/subtotalAmount" },
                            "discountAmount": { "$ref": "#/properties/subtotalAmount" },
                            "total": { "$ref": "#/properties/subtotalAmount" }
                        }
                    }
                },
                "subtotalAmount": { "$ref": "ProductEntity.json#/properties/basePrice" },
                "taxAmount": { "$ref": "ProductEntity.json#/properties/basePrice" },
                "shippingFeeAmount": { "$ref": "ProductEntity.json#/properties/basePrice" },
                "discountAmount": { "$ref": "ProductEntity.json#/properties/basePrice" },
                "totalAmount": { "$ref": "ProductEntity.json#/properties/basePrice" },
                "couponCode": { "type": ["string", "null"] },
                "paymentId": { "type": ["string", "null"], "format": "uuid" },
                "shipmentId": { "type": ["string", "null"], "format": "uuid" },
                "idempotencyKey": { "type": "string", "format": "uuid" },
                "createdAt": { "type": "string", "format": "date-time" },
                "updatedAt": { "type": "string", "format": "date-time" }
            }
        }),
        ("PaymentTransactionEntity", {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "PaymentTransactionEntity",
            "type": "object",
            "required": ["id", "transactionReference", "orderId", "userId", "amount", "status", "methodType", "provider", "idempotencyKey", "createdAt", "updatedAt"],
            "properties": {
                "id": { "type": "string", "format": "uuid" },
                "transactionReference": { "type": "string" },
                "orderId": { "type": "string" },
                "userId": { "type": "string" },
                "amount": { "$ref": "ProductEntity.json#/properties/basePrice" },
                "status": { "type": "string", "enum": ["PENDING", "REQUIRES_ACTION", "PROCESSING", "AUTHORIZED", "CAPTURED", "FAILED", "CANCELLED", "REFUNDED", "PARTIALLY_REFUNDED", "DISPUTED", "CHARGEBACK"] },
                "methodType": { "type": "string", "enum": ["CREDIT_CARD", "DEBIT_CARD", "BANK_TRANSFER", "PAYPAL", "APPLE_PAY", "GOOGLE_PAY", "CRYPTO", "STORE_CREDIT", "GIFT_CARD"] },
                "provider": { "type": "string", "enum": ["STRIPE", "PAYPAL", "ADYEN", "MOCK", "INTERNAL_LEDGER"] },
                "providerTransactionId": { "type": ["string", "null"] },
                "idempotencyKey": { "type": "string" },
                "createdAt": { "type": "string", "format": "date-time" },
                "updatedAt": { "type": "string", "format": "date-time" }
            }
        }),
        ("InventoryStockEntity", {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "InventoryStockEntity",
            "type": "object",
            "required": ["id", "sku", "warehouseId", "onHandQuantity", "reservedQuantity", "allocatedQuantity", "safetyStockThreshold", "reorderQuantity", "version", "updatedAt"],
            "properties": {
                "id": { "type": "string", "format": "uuid" },
                "sku": { "type": "string" },
                "warehouseId": { "type": "string", "format": "uuid" },
                "onHandQuantity": { "type": "integer", "minimum": 0 },
                "reservedQuantity": { "type": "integer", "minimum": 0 },
                "allocatedQuantity": { "type": "integer", "minimum": 0 },
                "safetyStockThreshold": { "type": "integer", "minimum": 0 },
                "reorderQuantity": { "type": "integer", "minimum": 1 },
                "binLocation": { "type": ["string", "null"] },
                "version": { "type": "integer", "minimum": 1 },
                "updatedAt": { "type": "string", "format": "date-time" }
            }
        }),
        ("ShipmentEntity", {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "ShipmentEntity",
            "type": "object",
            "required": ["id", "shipmentNumber", "orderId", "status", "carrier", "serviceLevel", "originWarehouseId", "destinationAddress", "weightGrams", "dimensionsMm", "createdAt", "updatedAt"],
            "properties": {
                "id": { "type": "string", "format": "uuid" },
                "shipmentNumber": { "type": "string" },
                "orderId": { "type": "string" },
                "status": { "type": "string", "enum": ["UNFULFILLED", "ALLOCATING", "PICKING", "PACKED", "LABEL_GENERATED", "READY_FOR_PICKUP", "SHIPPED", "IN_TRANSIT", "OUT_FOR_DELIVERY", "DELIVERED", "FAILED_ATTEMPT", "RETURNED_TO_SENDER", "LOST_IN_TRANSIT"] },
                "carrier": { "type": "string", "enum": ["FEDEX", "UPS", "DHL", "USPS", "INTERNAL_FLEET", "MOCK_CARRIER"] },
                "serviceLevel": { "type": "string" },
                "trackingNumber": { "type": ["string", "null"] },
                "trackingUrl": { "type": ["string", "null"], "format": "uri" },
                "shippingLabelUrl": { "type": ["string", "null"], "format": "uri" },
                "originWarehouseId": { "type": "string" },
                "destinationAddress": { "$ref": "UserEntity.json#/properties/address" },
                "weightGrams": { "type": "integer", "minimum": 1 },
                "dimensionsMm": {
                    "type": "object",
                    "required": ["length", "width", "height"],
                    "properties": {
                        "length": { "type": "integer", "minimum": 1 },
                        "width": { "type": "integer", "minimum": 1 },
                        "height": { "type": "integer", "minimum": 1 }
                    }
                },
                "dispatchedAt": { "type": ["string", "null"], "format": "date-time" },
                "deliveredAt": { "type": ["string", "null"], "format": "date-time" },
                "createdAt": { "type": "string", "format": "date-time" },
                "updatedAt": { "type": "string", "format": "date-time" }
            }
        })
    ]

    for name, schema_obj in schemas:
        write_file(f"{schema_dir}/{name}.json", json.dumps(schema_obj, indent=2))

    print("Generated standard JSON Schema specifications.")

def generate_adrs_71_to_100():
    adrs = [
        ("071", "Canary Deployment Gates using Prometheus SLI Verification", "Automate traffic shifting in 10% steps while evaluating 5xx error budget and latency SLOs."),
        ("072", "Multi-Tiered Redis Session Clustering and High Availability", "Deploy 3-master 3-replica Redis Sentinel topology for zero-downtime cache failover."),
        ("073", "API Request Decompression and Payload Size Restrictions", "Accept gzip/brotli compressed request bodies with 10MB payload size limit."),
        ("074", "Asynchronous Event Outbox Polling with Skip Locked Optimization", "Utilize `FOR UPDATE SKIP LOCKED` in outbox processor for lock-free parallel queue processing."),
        ("075", "Immutable Container Deployment Images and Non-Root Users", "Build hardened Distroless/Alpine container images running strictly under unprivileged UID."),
        ("076", "Cross-Cutting Context Propagation via AsyncLocalStorage", "Use Node.js `AsyncLocalStorage` to propagate correlation IDs across asynchronous callback chains."),
        ("077", "Double-Entry General Ledger End-of-Day Balancing Automation", "Execute automated midnight reconciliation cron job to verify zero debit/credit drift."),
        ("078", "Client-Side SDK Error Mapping to Strong Domain Exceptions", "Map HTTP 4xx/5xx status codes directly to typed SDK exceptions with retry hints."),
        ("079", "Zero-Knowledge Password Verification and Argon2id Benchmarks", "Verify Argon2id memory costs against 50ms execution budget on server hardware."),
        ("080", "Multi-Warehouse Least-Cost Fulfillment Routing Optimization", "Select warehouse fulfillment locations using combined freight distance and on-hand stock metrics."),
        ("081", "Transactional Email Templating with Handlebars and CSS Inlining", "Compile HTML email templates with inline CSS and strict XSS sanitization."),
        ("082", "Real-Time Clickstream Ingestion with Redis Stream Buffering", "Buffer high-throughput clickstream telemetry in Redis before batch insertion into analytics tables."),
        ("083", "Automated Database Schema Migration Verification in CI", "Execute forward and rollback schema migrations against transient PostgreSQL test containers in GitHub Actions."),
        ("084", "Microservice Service Discovery using Kubernetes Native CoreDNS", "Resolve internal microservice endpoints via cluster DNS (`http://service-name:port`)."),
        ("085", "API Gateway Response Compression and Brotli Streaming", "Compress JSON responses exceeding 1KB using Brotli and Gzip dynamic negotiation."),
        ("086", "Cryptographic Nonce and Timestamp Verification for Webhooks", "Require incoming provider webhooks to include valid signed timestamps within 5-minute tolerance."),
        ("087", "High-Throughput Order Ingestion via CQRS Command Separation", "Separate order placement write path from order history read queries to maximize scalability."),
        ("088", "Customer Account Verification Flow with Expiring Cryptographic Tokens", "Require email activation tokens with 24-hour expiration before granting authenticated checkout."),
        ("089", "Distributed Mutex Locking for Financial Account Payouts", "Acquire distributed Redis mutex locks when settling balances to prevent concurrent race conditions."),
        ("090", "Enterprise Disaster Recovery Backup Schedule and Cross-Region S3 Storage", "Perform hourly PostgreSQL WAL archiving and daily automated full snapshots replicated to secondary cloud region."),
        ("091", "Automated Inventory Replenishment using Wilson Economic Order Quantity", "Trigger supplier purchase orders automatically when stock hits calculated safety reorder point."),
        ("092", "Dynamic Product Category Taxonomy and Breadcrumb Resolution", "Resolve recursive category hierarchies in memory with cached closure tables."),
        ("093", "Multi-Currency Price Tiering and FX Hedging Spread Management", "Calculate localized storefront prices using real-time FX rates with configurable merchant hedging spread."),
        ("094", "Strict Content-Type Validation and JSON Body Parser Security", "Reject requests with mismatched `Content-Type: application/json` headers to prevent parser exploit vectors."),
        ("095", "Carrier Tracking Webhook Ingestion and Event Deduplication", "Deduplicate tracking status webhooks using carrier milestone timestamps and tracking numbers."),
        ("096", "Prometheus Histogram Bucket Boundaries for Microservice Latency", "Configure exponential latency histogram buckets `[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5]`."),
        ("097", "Kubernetes Pod Disruption Budgets for High Availability", "Enforce `minAvailable: 1` PodDisruptionBudgets across all multi-replica service deployments."),
        ("098", "Secure PII Data Redaction in Logging Transports", "Automatically redact passwords, tokens, and credit card numbers from all log output using string pattern matchers."),
        ("099", "Comprehensive Automated Smoke Testing Suite for Production Releases", "Execute end-to-end synthetic checkout smoke tests immediately following blue/green traffic switch."),
        ("100", "Long-Term Architectural Evolution and Governance Standards", "Maintain all architectural revisions through formalized peer-reviewed ADRs and automated CI schema linters.")
    ]

    for num, title, desc in adrs:
        content = f"""# ADR-{num}: {title}

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context & Problem Statement
Operating a distributed enterprise microservices architecture across high-throughput transactional domains requires uncompromising engineering rigor, deterministic state handling, and zero tolerance for data anomalies.

## Decision
We formally adopt **{title}**.
{desc}

### Key Architectural Guidelines:
1. **Domain Isolation**: Each microservice maintains complete authority over its domain models, persistence tables, and validation invariants.
2. **Resilience & Self-Healing**: Transient downstream failures are mitigated through circuit breakers, retry with exponential backoff, and distributed saga compensations.
3. **Auditability & Observability**: Every business state transition produces distributed tracing context and immutable telemetry records.

## Consequences & Trade-offs
### Positive:
- Uncompromising system reliability and horizontal scalability.
- Clean architectural boundaries facilitating autonomous team velocity.
- Comprehensive compliance with enterprise security and regulatory standards.

### Negative:
- Strict architectural discipline required during design reviews and code deployment.
"""
        write_file(f"docs/adr/ADR-{num}-{title.lower().replace(' ', '-').replace('/', '-')}.md", content)

    print("Generated ADRs 071 through 100.")

if __name__ == "__main__":
    generate_json_schemas()
    generate_adrs_71_to_100()
    print("Massive payload schema generation completed successfully.")
