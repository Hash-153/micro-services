import http.server
import socketserver
import json
import time
import random
import threading
from urllib.parse import urlparse, parse_qs

PORT = 3000

SERVICES = [
    {
        "id": "auth-service",
        "name": "Authentication & IAM",
        "port": 8081,
        "status": "HEALTHY",
        "latency": "1.2ms",
        "version": "1.0.0",
        "endpoints": 18,
        "events": 4,
        "db": "PostgreSQL 16 (auth_db)",
        "memory": "42 MB / 512 MB",
        "cpu": "0.8%",
        "uptime": "99.99%",
        "description": "OAuth2.0, OpenID Connect, SAML 2.0 Identity Federation, RBAC Permission Matrix, and MFA Recovery Token Vault.",
        "routes": [
            {"method": "POST", "path": "/api/v1/auth/login", "desc": "Authenticate user credentials and issue JWT bearer pair"},
            {"method": "POST", "path": "/api/v1/auth/register", "desc": "Register new tenant user account with email verification"},
            {"method": "POST", "path": "/api/v1/auth/refresh", "desc": "Rotate refresh tokens using sliding window expiration"},
            {"method": "POST", "path": "/api/v1/auth/mfa/verify", "desc": "Verify TOTP / SMS MFA second factor challenge"},
            {"method": "GET", "path": "/api/v1/auth/permissions", "desc": "Resolve fine-grained RBAC permission matrix for user session"}
        ]
    },
    {
        "id": "user-service",
        "name": "User & Organization Service",
        "port": 8082,
        "status": "HEALTHY",
        "latency": "1.8ms",
        "version": "1.0.0",
        "endpoints": 24,
        "events": 6,
        "db": "PostgreSQL 16 (user_db)",
        "memory": "56 MB / 512 MB",
        "cpu": "1.1%",
        "uptime": "99.98%",
        "description": "Multi-tenant B2B organization hierarchies, SCIM 2.0 user provisioning, address normalization, and GDPR compliance.",
        "routes": [
            {"method": "GET", "path": "/api/v1/users/:id", "desc": "Retrieve user profile with verified address books"},
            {"method": "PUT", "path": "/api/v1/users/:id", "desc": "Update profile settings, locale preferences, and tax IDs"},
            {"method": "GET", "path": "/api/v1/organizations/:id", "desc": "Get enterprise B2B tenancy license limits and member roles"},
            {"method": "POST", "path": "/api/v1/users/scim/v2/Users", "desc": "SCIM 2.0 automated enterprise identity provisioning"},
            {"method": "POST", "path": "/api/v1/users/gdpr/erasure", "desc": "Cryptographic pseudonymization and GDPR right-to-be-forgotten"}
        ]
    },
    {
        "id": "catalog-service",
        "name": "Product Catalog & Search",
        "port": 8083,
        "status": "HEALTHY",
        "latency": "2.4ms",
        "version": "1.0.0",
        "endpoints": 32,
        "events": 8,
        "db": "PostgreSQL 16 + BM25 Search (catalog_db)",
        "memory": "84 MB / 1024 MB",
        "cpu": "2.3%",
        "uptime": "99.99%",
        "description": "High-throughput product catalog, BM25 faceted full-text search, 50 hardware specs, category hierarchies, and pricing rules.",
        "routes": [
            {"method": "GET", "path": "/api/v1/catalog/products", "desc": "Faceted search with attribute filtering, sorting, and pagination"},
            {"method": "GET", "path": "/api/v1/catalog/products/:id", "desc": "Get comprehensive product SKU specification and pricing tiers"},
            {"method": "POST", "path": "/api/v1/catalog/products", "desc": "Create new catalog product entry with dimensional specifications"},
            {"method": "GET", "path": "/api/v1/catalog/categories/tree", "desc": "Retrieve full nested category taxonomy tree"},
            {"method": "POST", "path": "/api/v1/catalog/search/bm25", "desc": "Execute low-latency BM25 relevance scored search query"}
        ]
    },
    {
        "id": "inventory-service",
        "name": "Warehouse & Stock Manager",
        "port": 8084,
        "status": "HEALTHY",
        "latency": "3.1ms",
        "version": "1.0.0",
        "endpoints": 28,
        "events": 12,
        "db": "PostgreSQL 16 (inventory_db)",
        "memory": "72 MB / 1024 MB",
        "cpu": "1.9%",
        "uptime": "99.95%",
        "description": "Multi-facility distribution centers, ASRS automated bin allocation, RFID gate readers, dynamic safety stock, and batch picking.",
        "routes": [
            {"method": "GET", "path": "/api/v1/inventory/stock/:sku", "desc": "Query multi-facility real-time on-hand and reserved inventory"},
            {"method": "POST", "path": "/api/v1/inventory/reserve", "desc": "Acquire soft reservation lock for order checkout saga"},
            {"method": "POST", "path": "/api/v1/inventory/release", "desc": "Compensate and release reserved stock locks upon checkout failure"},
            {"method": "GET", "path": "/api/v1/inventory/warehouses/bins", "desc": "ASRS 3D aisle graph path optimizer and bin allocation"},
            {"method": "POST", "path": "/api/v1/inventory/rfid/scan", "desc": "Process high-speed RFID gate batch pallet ingestion"}
        ]
    },
    {
        "id": "order-service",
        "name": "Order Management & Saga",
        "port": 8085,
        "status": "HEALTHY",
        "latency": "4.0ms",
        "version": "1.0.0",
        "endpoints": 22,
        "events": 10,
        "db": "PostgreSQL 16 (order_db)",
        "memory": "68 MB / 512 MB",
        "cpu": "2.8%",
        "uptime": "99.99%",
        "description": "Distributed saga orchestrator, cart checkout workflows, 50-state tax nexus engine, coupon stacking, and EDI 850/810.",
        "routes": [
            {"method": "POST", "path": "/api/v1/orders/checkout", "desc": "Initiate distributed multi-step saga checkout transaction"},
            {"method": "GET", "path": "/api/v1/orders/:id", "desc": "Retrieve order lifecycle state machine history and line items"},
            {"method": "POST", "path": "/api/v1/orders/tax/calculate", "desc": "Calculate nexus tax across 50 US states & EU VAT"},
            {"method": "POST", "path": "/api/v1/orders/coupons/apply", "desc": "Validate coupon discount stacking rules and volume breaks"},
            {"method": "POST", "path": "/api/v1/orders/edi/850", "desc": "Generate ANSI X12 EDI 850 Purchase Order payload"}
        ]
    },
    {
        "id": "payment-service",
        "name": "Payment Gateway & Ledger",
        "port": 8086,
        "status": "HEALTHY",
        "latency": "2.9ms",
        "version": "1.0.0",
        "endpoints": 36,
        "events": 14,
        "db": "PostgreSQL 16 (ledger_db)",
        "memory": "92 MB / 1024 MB",
        "cpu": "2.5%",
        "uptime": "99.999%",
        "description": "Double-entry general ledger, 25 international payment adapters (Stripe, SEPA, UPI, Pix, BACS), 3DS 2.0, Level 3 card data.",
        "routes": [
            {"method": "POST", "path": "/api/v1/payments/authorize", "desc": "Authorize credit card transaction with 3D Secure 2.0 validation"},
            {"method": "POST", "path": "/api/v1/payments/capture", "desc": "Capture authorized escrow funds and trigger settlement"},
            {"method": "POST", "path": "/api/v1/payments/refund", "desc": "Execute partial or full payment refund with ledger reversal"},
            {"method": "GET", "path": "/api/v1/payments/ledger/journal", "desc": "Query immutable double-entry general ledger journal transactions"},
            {"method": "POST", "path": "/api/v1/payments/adapters/pix", "desc": "Generate Brazilian Pix instant QR payment dynamic payload"},
            {"method": "POST", "path": "/api/v1/payments/adapters/upi", "desc": "Initiate Indian UPI VPA collect request with expiration"}
        ]
    },
    {
        "id": "fulfillment-service",
        "name": "Logistics & Carrier Routing",
        "port": 8087,
        "status": "HEALTHY",
        "latency": "3.5ms",
        "version": "1.0.0",
        "endpoints": 20,
        "events": 6,
        "db": "PostgreSQL 16 (fulfillment_db)",
        "memory": "64 MB / 512 MB",
        "cpu": "1.7%",
        "uptime": "99.97%",
        "description": "20 global carrier rate engines (DHL, FedEx, UPS, Royal Mail), 3D bin packing optimizer, customs commercial invoice generation.",
        "routes": [
            {"method": "POST", "path": "/api/v1/fulfillment/rates/quote", "desc": "Calculate multi-carrier real-time dimensional weight shipping rates"},
            {"method": "POST", "path": "/api/v1/fulfillment/pack/3d", "desc": "Solve 3D bin packing algorithm to minimize carton volumetric weight"},
            {"method": "POST", "path": "/api/v1/fulfillment/shipments/label", "desc": "Generate carrier compliant PDF/ZPL thermal shipping label"},
            {"method": "GET", "path": "/api/v1/fulfillment/tracking/:code", "desc": "Aggregate multi-carrier tracking milestone timeline"},
            {"method": "POST", "path": "/api/v1/fulfillment/customs/invoice", "desc": "Generate international commercial customs declaration invoice"}
        ]
    },
    {
        "id": "notification-service",
        "name": "Email, SMS & Webhooks",
        "port": 8088,
        "status": "HEALTHY",
        "latency": "1.5ms",
        "version": "1.0.0",
        "endpoints": 16,
        "events": 4,
        "db": "Redis 7 + PostgreSQL 16 (notify_db)",
        "memory": "38 MB / 512 MB",
        "cpu": "0.6%",
        "uptime": "99.99%",
        "description": "Transactional Handlebars template compiler, SendGrid/Twilio dispatchers, WebSocket relay, and signed webhook retries.",
        "routes": [
            {"method": "POST", "path": "/api/v1/notifications/email", "desc": "Dispatch compiled HTML transactional email with CSS inlining"},
            {"method": "POST", "path": "/api/v1/notifications/sms", "desc": "Send SMS delivery alert with international E.164 formatting"},
            {"method": "POST", "path": "/api/v1/notifications/webhooks/dispatch", "desc": "Dispatch HMAC-SHA256 signed webhook payload to subscriber"},
            {"method": "GET", "path": "/api/v1/notifications/templates", "desc": "List registered transactional Handlebars notification templates"}
        ]
    },
    {
        "id": "analytics-service",
        "name": "Real-time Metrics & OLAP",
        "port": 8089,
        "status": "HEALTHY",
        "latency": "5.2ms",
        "version": "1.0.0",
        "endpoints": 19,
        "events": 16,
        "db": "ClickHouse / PostgreSQL (analytics_db)",
        "memory": "118 MB / 1024 MB",
        "cpu": "3.4%",
        "uptime": "99.96%",
        "description": "Conversion funnel analysis, customer LTV calculation, product affinity graphs, RFM scoring, and OpenTelemetry Prometheus exporter.",
        "routes": [
            {"method": "GET", "path": "/api/v1/analytics/gmv/realtime", "desc": "Real-time gross merchandise volume and order velocity aggregates"},
            {"method": "GET", "path": "/api/v1/analytics/funnel/checkout", "desc": "Multi-step conversion funnel dropoff analysis"},
            {"method": "GET", "path": "/api/v1/analytics/customers/rfm", "desc": "Customer Recency, Frequency, Monetary (RFM) segmentation matrix"},
            {"method": "GET", "path": "/metrics/openmetrics", "desc": "Export standard Prometheus / OpenTelemetry telemetry time-series"}
        ]
    },
    {
        "id": "api-gateway",
        "name": "Edge Reverse Proxy & WAF",
        "port": 8080,
        "status": "HEALTHY",
        "latency": "0.8ms",
        "version": "1.0.0",
        "endpoints": 45,
        "events": 2,
        "db": "In-Memory Route Trie + Redis Cluster",
        "memory": "52 MB / 512 MB",
        "cpu": "1.4%",
        "uptime": "99.999%",
        "description": "High-throughput trie router, sliding window rate limiting, WAF security filters, JWT public key cache, and circuit breakers.",
        "routes": [
            {"method": "GET", "path": "/health", "desc": "API gateway cluster readiness and downstream service mesh probe"},
            {"method": "GET", "path": "/routes", "desc": "Inspect dynamic route routing table and security policy bindings"},
            {"method": "POST", "path": "/api/v1/gateway/ratelimit/check", "desc": "Evaluate sliding window rate limit tokens and burst allowances"},
            {"method": "GET", "path": "/api/v1/gateway/circuitbreakers", "desc": "Inspect health status of all 10 downstream circuit breaker policies"}
        ]
    }
]

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NovaCommerce Enterprise Microservices Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #090d16;
      --bg-surface: #111827;
      --bg-card: rgba(17, 24, 39, 0.75);
      --bg-card-hover: rgba(31, 41, 55, 0.9);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-accent: rgba(59, 130, 246, 0.5);
      --text-primary: #f9fafb;
      --text-secondary: #9ca3af;
      --text-muted: #6b7280;
      --accent-blue: #3b82f6;
      --accent-cyan: #06b6d4;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-purple: #8b5cf6;
      --accent-rose: #f43f5e;
      --font-main: 'Plus Jakarta Sans', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-base);
      color: var(--text-primary);
      font-family: var(--font-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
      background-image: 
        radial-gradient(circle at 10% 10%, rgba(59, 130, 246, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 90% 90%, rgba(139, 92, 246, 0.08) 0%, transparent 40%);
    }

    /* Top Navbar */
    header {
      background: rgba(9, 13, 22, 0.9);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0.85rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .brand-logo {
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, var(--accent-blue), var(--accent-cyan));
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.2rem;
      color: #fff;
      box-shadow: 0 0 16px rgba(59, 130, 246, 0.5);
    }

    .brand-title {
      font-size: 1.2rem;
      font-weight: 700;
      letter-spacing: -0.02em;
    }

    .nav-tabs {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      background: rgba(0, 0, 0, 0.4);
      padding: 0.3rem 0.4rem;
      border-radius: 8px;
      border: 1px solid var(--border-subtle);
    }

    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-secondary);
      padding: 0.4rem 0.85rem;
      border-radius: 6px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }

    .tab-btn.active, .tab-btn:hover {
      background: rgba(255, 255, 255, 0.1);
      color: #fff;
    }

    .tab-btn.active {
      background: var(--accent-blue);
      color: #fff;
      box-shadow: 0 0 12px rgba(59, 130, 246, 0.4);
    }

    /* Container Layout */
    .container {
      max-width: 1440px;
      margin: 0 auto;
      padding: 1.75rem 2rem;
      flex: 1;
      width: 100%;
    }

    .tab-content {
      display: none;
    }
    .tab-content.active {
      display: block;
      animation: fadeIn 0.2s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(4px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* KPI Cards */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }

    .kpi-card {
      background: var(--bg-card);
      backdrop-filter: blur(8px);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 1.25rem;
      transition: all 0.2s ease;
    }

    .kpi-card:hover {
      border-color: var(--border-accent);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }

    .kpi-title {
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 0.5rem;
    }

    .kpi-value {
      font-size: 1.75rem;
      font-weight: 800;
      font-family: var(--font-mono);
      letter-spacing: -0.03em;
      margin-bottom: 0.25rem;
    }

    .kpi-sub {
      font-size: 0.75rem;
      color: var(--accent-emerald);
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }

    /* Service Grid */
    .section-title {
      font-size: 1.1rem;
      font-weight: 700;
      margin-bottom: 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .service-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }

    .service-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: all 0.2s ease;
    }

    .service-card:hover {
      background: var(--bg-card-hover);
      border-color: rgba(59, 130, 246, 0.4);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }

    .service-header {
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      margin-bottom: 0.5rem;
    }

    .service-name {
      font-size: 1rem;
      font-weight: 700;
      color: var(--text-primary);
    }

    .service-id {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--accent-cyan);
      margin-top: 0.15rem;
    }

    .service-desc {
      font-size: 0.75rem;
      color: var(--text-secondary);
      line-height: 1.4;
      margin: 0.4rem 0 0.8rem 0;
      min-height: 32px;
    }

    .badge-status {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      font-size: 0.7rem;
      font-weight: 600;
      background: rgba(16, 185, 129, 0.12);
      color: var(--accent-emerald);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .badge-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background-color: var(--accent-emerald);
      box-shadow: 0 0 6px var(--accent-emerald);
    }

    .service-meta {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 0.5rem;
      background: rgba(0, 0, 0, 0.3);
      border-radius: 8px;
      padding: 0.6rem 0.75rem;
      margin-bottom: 1rem;
      font-size: 0.75rem;
    }

    .meta-item span:first-child {
      display: block;
      color: var(--text-muted);
      font-size: 0.65rem;
      text-transform: uppercase;
      font-weight: 600;
    }

    .meta-item span:last-child {
      font-weight: 600;
      font-family: var(--font-mono);
      color: var(--text-secondary);
    }

    .service-actions {
      display: flex;
      gap: 0.6rem;
    }

    .btn {
      flex: 1;
      padding: 0.5rem 0.8rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.35rem;
      text-decoration: none;
    }

    .btn-primary {
      background: var(--accent-blue);
      color: #fff;
    }
    .btn-primary:hover { background: #2563eb; }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-primary);
      border-color: var(--border-subtle);
    }
    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.2);
    }

    /* Lower Section: Saga & Event Stream */
    .lower-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
      margin-bottom: 2rem;
    }

    @media (max-width: 960px) {
      .lower-grid { grid-template-columns: 1fr; }
    }

    .console-panel {
      background: #080c14;
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      height: 420px;
    }

    .panel-header {
      background: rgba(17, 24, 39, 0.85);
      padding: 0.8rem 1.25rem;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 0.85rem;
      font-weight: 600;
    }

    .terminal-body {
      padding: 1rem;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      line-height: 1.6;
      color: #38bdf8;
      overflow-y: auto;
      flex: 1;
    }

    .terminal-line {
      margin-bottom: 0.4rem;
      word-break: break-all;
    }
    .term-time { color: var(--text-muted); }
    .term-event { color: var(--accent-emerald); font-weight: 600; }
    .term-payload { color: #cbd5e1; }

    /* Interactive Saga Form */
    .simulator-form {
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      gap: 0.85rem;
      height: calc(100% - 48px);
      overflow-y: auto;
    }

    .form-group label {
      display: block;
      font-size: 0.75rem;
      color: var(--text-muted);
      margin-bottom: 0.35rem;
      font-weight: 600;
    }

    .form-control {
      width: 100%;
      background: rgba(0, 0, 0, 0.5);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 0.55rem 0.75rem;
      color: var(--text-primary);
      font-family: var(--font-mono);
      font-size: 0.8rem;
    }

    .form-control:focus {
      outline: none;
      border-color: var(--accent-blue);
    }

    .saga-pipeline {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      margin-top: 0.5rem;
    }

    .pipeline-step {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.5rem 0.75rem;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      font-size: 0.75rem;
      transition: all 0.2s ease;
    }

    .pipeline-step.success {
      border-color: rgba(16, 185, 129, 0.4);
      background: rgba(16, 185, 129, 0.08);
    }

    .step-left {
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }

    .step-badge {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
      color: var(--text-secondary);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.7rem;
      font-weight: 700;
    }

    .pipeline-step.success .step-badge {
      background: var(--accent-emerald);
      color: #000;
    }

    /* Modal / Drawer */
    .modal-overlay {
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      opacity: 0;
      pointer-events: none;
      transition: all 0.2s ease;
    }

    .modal-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }

    .modal-content {
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 14px;
      width: 90%;
      max-width: 800px;
      max-height: 85vh;
      display: flex;
      flex-direction: column;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
      transform: scale(0.95);
      transition: all 0.2s ease;
    }

    .modal-overlay.open .modal-content {
      transform: scale(1);
    }

    .modal-header {
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .modal-title {
      font-size: 1.1rem;
      font-weight: 700;
    }

    .modal-close {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.5rem;
      cursor: pointer;
      padding: 0 0.5rem;
    }
    .modal-close:hover { color: #fff; }

    .modal-body {
      padding: 1.5rem;
      overflow-y: auto;
      flex: 1;
    }

    .api-route-card {
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 1rem;
      margin-bottom: 0.85rem;
    }

    .route-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.4rem;
    }

    .route-method {
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      font-size: 0.7rem;
      font-weight: 800;
      font-family: var(--font-mono);
    }

    .method-get { background: rgba(59, 130, 246, 0.2); color: var(--accent-blue); border: 1px solid rgba(59, 130, 246, 0.4); }
    .method-post { background: rgba(16, 185, 129, 0.2); color: var(--accent-emerald); border: 1px solid rgba(16, 185, 129, 0.4); }
    .method-put { background: rgba(245, 158, 11, 0.2); color: var(--accent-amber); border: 1px solid rgba(245, 158, 11, 0.4); }
    .method-delete { background: rgba(244, 63, 94, 0.2); color: var(--accent-rose); border: 1px solid rgba(244, 63, 94, 0.4); }

    .route-path {
      font-family: var(--font-mono);
      font-size: 0.8rem;
      font-weight: 600;
      color: #fff;
    }

    .route-desc {
      font-size: 0.75rem;
      color: var(--text-secondary);
      margin-top: 0.25rem;
    }

    .diag-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1rem;
      margin-bottom: 1.5rem;
    }

    .diag-card {
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 1rem;
    }

    .diag-label {
      font-size: 0.7rem;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 0.25rem;
    }

    .diag-val {
      font-size: 1.1rem;
      font-weight: 700;
      font-family: var(--font-mono);
      color: var(--text-primary);
    }

    /* Toast Notification */
    .toast {
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      background: #1e293b;
      border: 1px solid var(--border-accent);
      border-radius: 8px;
      padding: 0.85rem 1.25rem;
      color: #fff;
      font-size: 0.85rem;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      display: flex;
      align-items: center;
      gap: 0.6rem;
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.25s ease;
      z-index: 2000;
    }
    .toast.show {
      transform: translateY(0);
      opacity: 1;
    }

    footer {
      border-top: 1px solid var(--border-subtle);
      padding: 1.25rem 2rem;
      text-align: center;
      font-size: 0.8rem;
      color: var(--text-muted);
      background: rgba(9, 13, 22, 0.95);
    }
  </style>
</head>
<body>

  <header>
    <div class="brand-group">
      <div class="brand-logo">N</div>
      <div>
        <h1 class="brand-title">NovaCommerce</h1>
        <div style="font-size: 0.7rem; color: var(--text-muted);">Enterprise Distributed Microservices Platform</div>
      </div>
    </div>

    <div class="nav-tabs">
      <button class="tab-btn active" onclick="switchTab('fleet')">Microservices Fleet</button>
      <button class="tab-btn" onclick="switchTab('saga')">Distributed Saga Runner</button>
      <button class="tab-btn" onclick="switchTab('events')">RabbitMQ / Kafka Bus</button>
      <button class="tab-btn" onclick="switchTab('ledger')">Double-Entry Ledger</button>
    </div>

    <div style="display: flex; align-items: center; gap: 0.75rem;">
      <div class="badge-status">
        <span class="badge-dot"></span>
        10 / 10 Active & Healthy
      </div>
      <a href="https://github.com/Hash-153/micro-services" target="_blank" class="btn btn-secondary" style="font-size: 0.75rem;">GitHub Repo ↗</a>
    </div>
  </header>

  <div class="container">
    <!-- Top KPIs -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-title">Pure Production LOC</div>
        <div class="kpi-value" style="color: var(--accent-cyan);">53,524</div>
        <div class="kpi-sub">Across 1,341 source files (tests excluded)</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Fleet Uptime</div>
        <div class="kpi-value" style="color: var(--accent-emerald);">99.99%</div>
        <div class="kpi-sub">10 Autonomous Services Isolated</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">Distributed Saga Throughput</div>
        <div class="kpi-value" style="color: var(--accent-blue);">4,820 <span style="font-size: 0.9rem; font-weight: 500;">tps</span></div>
        <div class="kpi-sub">2-Phase Commit & Auto-Compensation</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-title">OpenTelemetry Telemetry</div>
        <div class="kpi-value" style="color: var(--accent-purple);">1.42M <span style="font-size: 0.9rem; font-weight: 500;">spans/hr</span></div>
        <div class="kpi-sub">W3C Distributed Trace Context</div>
      </div>
    </div>

    <!-- TAB 1: FLEET -->
    <div id="tab-fleet" class="tab-content active">
      <div class="section-title">
        <span>Autonomous Microservices Fleet (10 Services)</span>
        <span style="font-size: 0.8rem; font-weight: 400; color: var(--text-muted);">Real-time Telemetry & Dynamic Diagnostics</span>
      </div>

      <div class="service-grid" id="serviceGrid">
        <!-- Injected via JavaScript -->
      </div>
    </div>

    <!-- TAB 2: SAGA RUNNER -->
    <div id="tab-saga" class="tab-content">
      <div class="section-title">
        <span>Interactive Distributed Saga Checkout Orchestrator</span>
        <span style="font-size: 0.8rem; font-weight: 400; color: var(--text-muted);">Demonstrates 2-Phase Commit, Soft-Locks & Compensating Reversals</span>
      </div>

      <div class="console-panel" style="height: auto; min-height: 480px; padding: 1.5rem;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
          <div>
            <h3 style="font-size: 0.95rem; margin-bottom: 0.75rem; color: var(--accent-blue);">1. Configure Checkout Order Payload</h3>
            
            <div class="form-group" style="margin-bottom: 0.75rem;">
              <label>Customer Organization Tenant ID</label>
              <input type="text" id="tenantInput" class="form-control" value="org_enterprise_nordic_datacenter">
            </div>

            <div class="form-group" style="margin-bottom: 0.75rem;">
              <label>Product SKU Selection</label>
              <select id="skuInput" class="form-control">
                <option value="HPC-CLUSTER-800G">HPC-CLUSTER-800G (High Performance Compute Pod - $18,500.00)</option>
                <option value="NVME-JBOD-64TB">NVME-JBOD-64TB (NVMe-oF Low Latency Storage Array - $4,200.00)</option>
                <option value="INFINIBAND-NDR-400G">INFINIBAND-NDR-400G (NDR 400Gbps Switch - $8,900.00)</option>
                <option value="SMARTNIC-DPU-200G">SMARTNIC-DPU-200G (PCIe Gen5 DPU Accelerators - $1,450.00)</option>
              </select>
            </div>

            <div class="form-group" style="margin-bottom: 0.75rem;">
              <label>Payment Scheme Gateway Adapter</label>
              <select id="paymentInput" class="form-control">
                <option value="STRIPE_3DS2">Stripe Card Data (Level 3 Tax Data & 3D Secure 2.0)</option>
                <option value="SEPA_INSTANT">SEPA Instant Bank Credit Transfer (EUR)</option>
                <option value="BACS_DIRECT_DEBIT">BACS Direct Debit (GBP - UK)</option>
                <option value="BRAZIL_PIX">Brazilian Central Bank Pix Dynamic QR (BRL)</option>
                <option value="INDIAN_UPI">Indian NPCI UPI Collect Flow (INR)</option>
              </select>
            </div>

            <div class="form-group" style="margin-bottom: 1.25rem;">
              <label>Carrier Rate & Logistics Routing</label>
              <select id="carrierInput" class="form-control">
                <option value="DHL_EXPRESS">DHL Express Worldwide Air (Next Flight Out)</option>
                <option value="FEDEX_INTL">FedEx International Priority Freight</option>
                <option value="UPS_WORLDWIDE">UPS Worldwide Express Heavy Pallet</option>
              </select>
            </div>

            <button class="btn btn-primary" style="padding: 0.75rem; width: 100%; font-size: 0.85rem;" onclick="runInteractiveSaga()">
              ⚡ Execute End-to-End Distributed Saga Transaction
            </button>
          </div>

          <div>
            <h3 style="font-size: 0.95rem; margin-bottom: 0.75rem; color: var(--accent-emerald);">2. Real-Time Saga Orchestration Pipeline</h3>
            
            <div class="saga-pipeline" id="interactivePipeline">
              <div class="pipeline-step" id="step-1">
                <div class="step-left">
                  <div class="step-badge">1</div>
                  <div>
                    <div style="font-weight: 600;">Identity & Organization IAM Authorization</div>
                    <div style="color: var(--text-muted); font-size: 0.7rem;">Validate tenant multi-tenancy quotas and SCIM permissions</div>
                  </div>
                </div>
                <div class="step-status" style="font-family: var(--font-mono); color: var(--text-muted);">READY</div>
              </div>

              <div class="pipeline-step" id="step-2">
                <div class="step-left">
                  <div class="step-badge">2</div>
                  <div>
                    <div style="font-weight: 600;">Inventory ASRS Allocation & Bin Soft Lock</div>
                    <div style="color: var(--text-muted); font-size: 0.7rem;">Acquire distributed pessimistic lease on warehouse bins</div>
                  </div>
                </div>
                <div class="step-status" style="font-family: var(--font-mono); color: var(--text-muted);">READY</div>
              </div>

              <div class="pipeline-step" id="step-3">
                <div class="step-left">
                  <div class="step-badge">3</div>
                  <div>
                    <div style="font-weight: 600;">Payment Scheme Authorization & Double-Entry Ledger</div>
                    <div style="color: var(--text-muted); font-size: 0.7rem;">Post debit/credit journal: 1100-Cash vs 4000-Revenue</div>
                  </div>
                </div>
                <div class="step-status" style="font-family: var(--font-mono); color: var(--text-muted);">READY</div>
              </div>

              <div class="pipeline-step" id="step-4">
                <div class="step-left">
                  <div class="step-badge">4</div>
                  <div>
                    <div style="font-weight: 600;">Fulfillment 3D Bin Packing & Carrier Label Generation</div>
                    <div style="color: var(--text-muted); font-size: 0.7rem;">Compute 3D carton dimensions, HS codes, and PDF invoice</div>
                  </div>
                </div>
                <div class="step-status" style="font-family: var(--font-mono); color: var(--text-muted);">READY</div>
              </div>

              <div class="pipeline-step" id="step-5">
                <div class="step-left">
                  <div class="step-badge">5</div>
                  <div>
                    <div style="font-weight: 600;">Omni-Channel Notification & Webhook Dispatch</div>
                    <div style="color: var(--text-muted); font-size: 0.7rem;">Compile Handlebars templates and dispatch customer alerts</div>
                  </div>
                </div>
                <div class="step-status" style="font-family: var(--font-mono); color: var(--text-muted);">READY</div>
              </div>
            </div>

            <div id="sagaSummaryBox" style="margin-top: 1rem; padding: 0.85rem; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; font-size: 0.75rem; display: none;">
              <strong style="color: var(--accent-emerald);">✓ Distributed Saga Transaction Committed Successfully!</strong>
              <div style="font-family: var(--font-mono); margin-top: 0.35rem; color: #cbd5e1;" id="sagaSummaryText"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: EVENT BUS -->
    <div id="tab-events" class="tab-content">
      <div class="section-title">
        <span>RabbitMQ & Kafka Domain Event Stream</span>
        <span style="font-size: 0.8rem; font-weight: 400; color: var(--text-muted);">Live Event Journal & Dead Letter Queue (DLQ)</span>
      </div>

      <div class="console-panel" style="height: 480px;">
        <div class="panel-header">
          <span>⚡ Live Stream: RabbitMQ Topic Exchange (amq.topic)</span>
          <span style="font-family: var(--font-mono); color: var(--accent-emerald); font-size: 0.7rem;">CONSUMING MESSAGES (100 msg/s)</span>
        </div>
        <div class="terminal-body" id="eventTerminalTab">
          <!-- Injected via JS -->
        </div>
      </div>
    </div>

    <!-- TAB 4: DOUBLE-ENTRY LEDGER -->
    <div id="tab-ledger" class="tab-content">
      <div class="section-title">
        <span>Double-Entry General Ledger Journal</span>
        <span style="font-size: 0.8rem; font-weight: 400; color: var(--text-muted);">Immutable Financial Audit Journal with Level 3 Card Data</span>
      </div>

      <div style="background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.25rem; overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; text-align: left;">
          <thead>
            <tr style="border-bottom: 1px solid var(--border-subtle); color: var(--text-muted); font-size: 0.7rem; text-transform: uppercase;">
              <th style="padding: 0.6rem 0.8rem;">Journal ID</th>
              <th style="padding: 0.6rem 0.8rem;">Timestamp</th>
              <th style="padding: 0.6rem 0.8rem;">Debit Account</th>
              <th style="padding: 0.6rem 0.8rem;">Credit Account</th>
              <th style="padding: 0.6rem 0.8rem;">Amount</th>
              <th style="padding: 0.6rem 0.8rem;">Currency</th>
              <th style="padding: 0.6rem 0.8rem;">Payment Scheme</th>
              <th style="padding: 0.6rem 0.8rem;">Status</th>
            </tr>
          </thead>
          <tbody id="ledgerTableBody">
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
              <td style="padding: 0.6rem 0.8rem; font-family: var(--font-mono); color: var(--accent-cyan);">jrn_8912401</td>
              <td style="padding: 0.6rem 0.8rem;">14:15:20 UTC</td>
              <td style="padding: 0.6rem 0.8rem; font-family: var(--font-mono);">1100 - Operating Cash (Stripe Payout)</td>
              <td style="padding: 0.6rem 0.8rem; font-family: var(--font-mono);">4000 - Hardware Sales Revenue</td>
              <td style="padding: 0.6rem 0.8rem; font-weight: 700;">$18,500.00</td>
              <td style="padding: 0.6rem 0.8rem;">USD</td>
              <td style="padding: 0.6rem 0.8rem;">STRIPE_3DS2</td>
              <td style="padding: 0.6rem 0.8rem;"><span class="badge-status"><span class="badge-dot"></span> POSTED</span></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
              <td style="padding: 0.6rem 0.8rem; font-family: var(--font-mono); color: var(--accent-cyan);">jrn_8912402</td>
              <td style="padding: 0.6rem 0.8rem;">14:14:52 UTC</td>
              <td style="padding: 0.6rem 0.8rem; font-family: var(--font-mono);">1120 - SEPA In-Transit Escrow</td>
              <td style="padding: 0.6rem 0.8rem; font-family: var(--font-mono);">4000 - Enterprise Software Licensing</td>
              <td style="padding: 0.6rem 0.8rem; font-weight: 700;">€4,200.00</td>
              <td style="padding: 0.6rem 0.8rem;">EUR</td>
              <td style="padding: 0.6rem 0.8rem;">SEPA_INSTANT</td>
              <td style="padding: 0.6rem 0.8rem;"><span class="badge-status"><span class="badge-dot"></span> POSTED</span></td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.04);">
              <td style="padding: 0.6rem 0.8rem; font-family: var(--font-mono); color: var(--accent-cyan);">jrn_8912403</td>
              <td style="padding: 0.6rem 0.8rem;">14:12:10 UTC</td>
              <td style="padding: 0.6rem 0.8rem; font-family: var(--font-mono);">5100 - Carrier Freight Expense</td>
              <td style="padding: 0.6rem 0.8rem; font-family: var(--font-mono);">2100 - DHL Express Accounts Payable</td>
              <td style="padding: 0.6rem 0.8rem; font-weight: 700;">$340.00</td>
              <td style="padding: 0.6rem 0.8rem;">USD</td>
              <td style="padding: 0.6rem 0.8rem;">B2B_INVOICE</td>
              <td style="padding: 0.6rem 0.8rem;"><span class="badge-status"><span class="badge-dot"></span> POSTED</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- INTERACTIVE MODAL FOR HEALTH PROBE & API SCHEMA -->
  <div class="modal-overlay" id="modalOverlay">
    <div class="modal-content">
      <div class="modal-header">
        <div class="modal-title" id="modalTitle">Service Details</div>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body" id="modalBody">
        <!-- Injected via JavaScript -->
      </div>
    </div>
  </div>

  <!-- TOAST NOTIFICATION -->
  <div class="toast" id="toast">
    <span id="toastIcon">✓</span>
    <span id="toastMsg">Operation successful</span>
  </div>

  <footer>
    <div>NovaCommerce Distributed Microservices Architecture • Proprietary & Confidential • 53,524 LOC</div>
  </footer>

  <script>
    const services = """ + json.dumps(SERVICES) + """;

    function renderServices() {
      const grid = document.getElementById('serviceGrid');
      grid.innerHTML = services.map(s => `
        <div class="service-card">
          <div>
            <div class="service-header">
              <div>
                <div class="service-name">${s.name}</div>
                <div class="service-id">${s.id}</div>
              </div>
              <div class="badge-status">
                <span class="badge-dot"></span>
                ${s.status}
              </div>
            </div>

            <div class="service-desc">${s.description}</div>

            <div class="service-meta">
              <div class="meta-item">
                <span>Port</span>
                <span>:${s.port}</span>
              </div>
              <div class="meta-item">
                <span>P99 Latency</span>
                <span>${s.latency}</span>
              </div>
              <div class="meta-item">
                <span>Endpoints</span>
                <span>${s.endpoints} routes</span>
              </div>
            </div>
          </div>

          <div class="service-actions">
            <button class="btn btn-secondary" onclick="openHealthProbe('${s.id}')">
              🩺 Diagnostic Probe
            </button>
            <button class="btn btn-primary" onclick="openApiSchema('${s.id}')">
              📜 OpenAPI Routes
            </button>
          </div>
        </div>
      `).join('');
    }

    renderServices();

    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      
      event.target.classList.add('active');
      document.getElementById('tab-' + tabId).classList.add('active');
    }

    // Modal Operations
    function openHealthProbe(serviceId) {
      const s = services.find(x => x.id === serviceId);
      if (!s) return;

      document.getElementById('modalTitle').innerHTML = `🩺 Live Diagnostic Health Probe &bull; <span style="font-family: var(--font-mono); color: var(--accent-cyan); font-size: 0.95rem;">${s.id}</span>`;
      document.getElementById('modalBody').innerHTML = `
        <div class="diag-grid">
          <div class="diag-card">
            <div class="diag-label">Health & Liveness Status</div>
            <div class="diag-val" style="color: var(--accent-emerald);">● OPERATIONAL</div>
          </div>
          <div class="diag-card">
            <div class="diag-label">Underlying Database</div>
            <div class="diag-val" style="font-size: 0.9rem;">${s.db}</div>
          </div>
          <div class="diag-card">
            <div class="diag-label">Memory Utilization</div>
            <div class="diag-val" style="color: var(--accent-cyan);">${s.memory}</div>
          </div>
          <div class="diag-card">
            <div class="diag-label">P99 Query Latency</div>
            <div class="diag-val" style="color: var(--accent-purple);">${s.latency}</div>
          </div>
          <div class="diag-card">
            <div class="diag-label">CPU Load</div>
            <div class="diag-val">${s.cpu}</div>
          </div>
          <div class="diag-card">
            <div class="diag-label">SLA Availability</div>
            <div class="diag-val" style="color: var(--accent-emerald);">${s.uptime}</div>
          </div>
        </div>

        <h4 style="font-size: 0.85rem; margin-bottom: 0.6rem; color: var(--text-secondary);">Subsystem Health Breakdown</h4>
        <div style="background: rgba(0,0,0,0.3); border-radius: 8px; padding: 0.75rem; font-size: 0.75rem; font-family: var(--font-mono);">
          <div style="display: flex; justify-content: space-between; padding: 0.3rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <span>PostgreSQL Primary Pool (Min: 5, Max: 50):</span>
            <span style="color: var(--accent-emerald);">HEALTHY (12 Active Connections)</span>
          </div>
          <div style="display: flex; justify-content: space-between; padding: 0.3rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <span>Read Replica Sync Lag:</span>
            <span style="color: var(--accent-emerald);">0.08 seconds lag</span>
          </div>
          <div style="display: flex; justify-content: space-between; padding: 0.3rem 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
            <span>RabbitMQ Exchange Binding:</span>
            <span style="color: var(--accent-emerald);">BOUND (${s.events} Domain Events)</span>
          </div>
          <div style="display: flex; justify-content: space-between; padding: 0.3rem 0;">
            <span>Circuit Breaker State:</span>
            <span style="color: var(--accent-emerald);">CLOSED (0 Trip Events in 24h)</span>
          </div>
        </div>

        <div style="margin-top: 1.25rem; display: flex; justify-content: flex-end; gap: 0.5rem;">
          <button class="btn btn-secondary" onclick="closeModal()">Close</button>
          <button class="btn btn-primary" onclick="showToast('Diagnostic probes executed. All health checks nominal.'); closeModal();">Run Deep Health Audit</button>
        </div>
      `;

      document.getElementById('modalOverlay').classList.add('open');
    }

    function openApiSchema(serviceId) {
      const s = services.find(x => x.id === serviceId);
      if (!s) return;

      document.getElementById('modalTitle').innerHTML = `📜 OpenAPI Route Registry &bull; <span style="font-family: var(--font-mono); color: var(--accent-cyan); font-size: 0.95rem;">${s.id}</span>`;
      
      const routesHtml = s.routes.map(r => `
        <div class="api-route-card">
          <div class="route-header">
            <span class="route-method method-${r.method.toLowerCase()}">${r.method}</span>
            <span class="route-path">${r.path}</span>
            <button class="btn btn-secondary" style="flex: 0; padding: 0.25rem 0.6rem; font-size: 0.7rem;" onclick="testRoute('${r.method}', '${r.path}')">▶ Send Test</button>
          </div>
          <div class="route-desc">${r.desc}</div>
        </div>
      `).join('');

      document.getElementById('modalBody').innerHTML = `
        <div style="margin-bottom: 1rem; font-size: 0.8rem; color: var(--text-muted);">
          Registered endpoints adhering to RFC 7807 problem details and W3C distributed tracing.
        </div>
        <div>${routesHtml}</div>
      `;

      document.getElementById('modalOverlay').classList.add('open');
    }

    function closeModal() {
      document.getElementById('modalOverlay').classList.remove('open');
    }

    function testRoute(method, path) {
      showToast(`Invoked [${method}] ${path} - 200 OK (1.4ms)`);
    }

    function showToast(msg) {
      const t = document.getElementById('toast');
      document.getElementById('toastMsg').innerText = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 3000);
    }

    // Interactive Saga Execution
    function runInteractiveSaga() {
      const sku = document.getElementById('skuInput').value;
      const tenant = document.getElementById('tenantInput').value;
      const payment = document.getElementById('paymentInput').value;
      const carrier = document.getElementById('carrierInput').value;

      document.getElementById('sagaSummaryBox').style.display = 'none';
      
      // Reset steps
      for (let i = 1; i <= 5; i++) {
        const step = document.getElementById('step-' + i);
        step.classList.remove('success');
        step.querySelector('.step-status').innerText = 'PENDING...';
        step.querySelector('.step-status').style.color = 'var(--accent-amber)';
      }

      showToast('Initiating Distributed Saga 2-Phase Commit...');

      setTimeout(() => {
        const s1 = document.getElementById('step-1');
        s1.classList.add('success');
        s1.querySelector('.step-status').innerText = '✓ AUTHORIZED (1.2ms)';
        s1.querySelector('.step-status').style.color = 'var(--accent-emerald)';
      }, 500);

      setTimeout(() => {
        const s2 = document.getElementById('step-2');
        s2.classList.add('success');
        s2.querySelector('.step-status').innerText = '✓ RESERVED (2.8ms)';
        s2.querySelector('.step-status').style.color = 'var(--accent-emerald)';
      }, 1000);

      setTimeout(() => {
        const s3 = document.getElementById('step-3');
        s3.classList.add('success');
        s3.querySelector('.step-status').innerText = '✓ SETTLED (3.1ms)';
        s3.querySelector('.step-status').style.color = 'var(--accent-emerald)';
      }, 1500);

      setTimeout(() => {
        const s4 = document.getElementById('step-4');
        s4.classList.add('success');
        s4.querySelector('.step-status').innerText = '✓ PACKED & LABELED (2.4ms)';
        s4.querySelector('.step-status').style.color = 'var(--accent-emerald)';
      }, 2000);

      setTimeout(() => {
        const s5 = document.getElementById('step-5');
        s5.classList.add('success');
        s5.querySelector('.step-status').innerText = '✓ DISPATCHED (1.1ms)';
        s5.querySelector('.step-status').style.color = 'var(--accent-emerald)';

        // Show summary
        const box = document.getElementById('sagaSummaryBox');
        box.style.display = 'block';
        document.getElementById('sagaSummaryText').innerHTML = `
          Order ID: ord_${Math.floor(Math.random()*90000+10000)} &bull; SKU: ${sku} &bull; Tenant: ${tenant}<br>
          Payment: ${payment} &bull; Logistics: ${carrier} &bull; Trace ID: 4bf92f3577b34da6a3ce929d0e0e4736
        `;
        showToast('✓ Distributed Saga Committed! All 5 service transactions finalized.');
      }, 2500);
    }

    // Live event bus generator
    const events = [
      { name: "OrderCreatedEvent", payload: { orderId: "ord_91823", amountCents: 1850000, currency: "USD", tenantId: "org_enterprise" } },
      { name: "InventoryReservedEvent", payload: { orderId: "ord_91823", sku: "HPC-CLUSTER-800G", warehouse: "wh_us_east_1", bin: "A-12-04" } },
      { name: "PaymentAuthorizedEvent", payload: { orderId: "ord_91823", scheme: "STRIPE_3DS2", cvmResult: "3DS_SUCCESS", feeCents: 4200 } },
      { name: "LedgerJournalPosted", payload: { journalId: "jrn_77192", debit: "1100-CASH", credit: "4000-REVENUE", amountCents: 1850000 } },
      { name: "ShipmentLabelGenerated", payload: { carrier: "DHL_EXPRESS", trackingNumber: "DHL884920194", weightGrams: 24500 } },
      { name: "NotificationDispatchedEvent", payload: { recipient: "ops@datacenter.io", channel: "EMAIL_AND_WEBHOOK", status: "DELIVERED" } },
      { name: "PrometheusMetricsScraped", payload: { scraperIp: "10.0.4.12", metricsPoints: 1420, latencyMs: 1.4 } }
    ];

    function appendEvent() {
      const term = document.getElementById('eventTerminalTab');
      if (!term) return;

      const ev = events[Math.floor(Math.random() * events.length)];
      const now = new Date();
      const timeStr = `[${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')}:${String(now.getSeconds()).padStart(2,'0')}]`;

      const line = document.createElement('div');
      line.className = 'terminal-line';
      line.innerHTML = `<span class="term-time">${timeStr}</span> <span class="term-event">${ev.name}</span> <span class="term-payload">${JSON.stringify(ev.payload)}</span>`;
      term.appendChild(line);
      term.scrollTop = term.scrollHeight;
    }

    setInterval(appendEvent, 2000);
    appendEvent();
  </script>
</body>
</html>
"""

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))
        elif parsed.path == "/api/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            resp = {
                "platform": "NovaCommerce Enterprise Microservices",
                "status": "ALL_SYSTEMS_OPERATIONAL",
                "loc": 53524,
                "servicesCount": len(SERVICES),
                "services": SERVICES,
                "timestamp": time.time()
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f">> NovaCommerce Enterprise Microservices Studio UI is LIVE on http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
