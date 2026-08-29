import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_typescript_sdk_clients():
    pkg_dir = "sdks/typescript/src/api"
    
    # Auth API Client
    write_file(f"{pkg_dir}/AuthApiClient.ts", """import { RegisterUserDTO, LoginUserDTO, AuthTokensResponseDTO, ApiResponse } from '@novacommerce/core-types';

export class AuthApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async register(dto: RegisterUserDTO): Promise<AuthTokensResponseDTO> {
    const res = await fetch(`${this.baseUrl}/api/v1/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dto)
    });
    if (!res.ok) throw new Error(`Registration failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<AuthTokensResponseDTO>;
    return json.data;
  }

  public async login(dto: LoginUserDTO): Promise<AuthTokensResponseDTO> {
    const res = await fetch(`${this.baseUrl}/api/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dto)
    });
    if (!res.ok) throw new Error(`Login failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<AuthTokensResponseDTO>;
    return json.data;
  }

  public async getProfile(): Promise<any> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/auth/me`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) throw new Error(`Fetch profile failed: ${res.statusText}`);
    const json = await res.json();
    return json.data;
  }
}
""")

    # Catalog API Client
    write_file(f"{pkg_dir}/CatalogApiClient.ts", """import { ProductEntity, CreateProductDTO, ApiResponse } from '@novacommerce/core-types';

export class CatalogApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async listProducts(page: number = 1, limit: number = 20): Promise<{ items: ProductEntity[]; total: number }> {
    const res = await fetch(`${this.baseUrl}/api/v1/catalog/products?page=${page}&limit=${limit}`);
    if (!res.ok) throw new Error(`List products failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<ProductEntity[]>;
    return { items: json.data, total: json.meta?.totalItems || json.data.length };
  }

  public async getProductById(id: string): Promise<ProductEntity> {
    const res = await fetch(`${this.baseUrl}/api/v1/catalog/products/${id}`);
    if (!res.ok) throw new Error(`Get product failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<ProductEntity>;
    return json.data;
  }

  public async createProduct(dto: CreateProductDTO): Promise<ProductEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/catalog/products`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(dto)
    });
    if (!res.ok) throw new Error(`Create product failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<ProductEntity>;
    return json.data;
  }
}
""")

    # Order API Client
    write_file(f"{pkg_dir}/OrderApiClient.ts", """import { OrderEntity, CreateOrderDTO, ApiResponse } from '@novacommerce/core-types';

export class OrderApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async createOrder(dto: CreateOrderDTO): Promise<OrderEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(dto)
    });
    if (!res.ok) throw new Error(`Create order failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<OrderEntity>;
    return json.data;
  }

  public async getOrderById(id: string): Promise<OrderEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/orders/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (!res.ok) throw new Error(`Get order failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<OrderEntity>;
    return json.data;
  }
}
""")

    # Inventory API Client
    write_file(f"{pkg_dir}/InventoryApiClient.ts", """import { InventoryStockEntity, InventoryReservationEntity, ApiResponse } from '@novacommerce/core-types';

export class InventoryApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async setStock(sku: string, warehouseId: string, quantity: number): Promise<InventoryStockEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/inventory/stock`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ sku, warehouseId, quantity })
    });
    if (!res.ok) throw new Error(`Set stock failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<InventoryStockEntity>;
    return json.data;
  }

  public async reserveStock(orderId: string, sku: string, quantity: number): Promise<InventoryReservationEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/inventory/reserve`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ orderId, sku, quantity })
    });
    if (!res.ok) throw new Error(`Reserve stock failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<InventoryReservationEntity>;
    return json.data;
  }
}
""")

    # Payment API Client
    write_file(f"{pkg_dir}/PaymentApiClient.ts", """import { PaymentTransactionEntity, Currency, ApiResponse } from '@novacommerce/core-types';

export class PaymentApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async authorizePayment(orderId: string, amountCents: number, currency: Currency = Currency.USD): Promise<PaymentTransactionEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/payments/authorize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ orderId, amountCents, currency })
    });
    if (!res.ok) throw new Error(`Payment authorization failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<PaymentTransactionEntity>;
    return json.data;
  }
}
""")

    # Fulfillment API Client
    write_file(f"{pkg_dir}/FulfillmentApiClient.ts", """import { ShipmentEntity, ApiResponse } from '@novacommerce/core-types';

export class FulfillmentApiClient {
  private readonly baseUrl: string;
  private tokenProvider: () => string | undefined;

  constructor(baseUrl: string, tokenProvider: () => string | undefined) {
    this.baseUrl = baseUrl;
    this.tokenProvider = tokenProvider;
  }

  public async createShipment(orderId: string, destinationAddress: any, carrier: string = 'FEDEX'): Promise<ShipmentEntity> {
    const token = this.tokenProvider();
    const res = await fetch(`${this.baseUrl}/api/v1/fulfillment/shipments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ orderId, destinationAddress, carrier })
    });
    if (!res.ok) throw new Error(`Create shipment failed: ${res.statusText}`);
    const json = (await res.json()) as ApiResponse<ShipmentEntity>;
    return json.data;
  }
}
""")

    print("Generated TypeScript SDK API Clients.")

def generate_python_sdk_clients():
    pkg_dir = "sdks/python/novacommerce/api"
    
    write_file(f"{pkg_dir}/__init__.py", """from .auth import AuthApi
from .catalog import CatalogApi
from .orders import OrdersApi
from .inventory import InventoryApi
from .payments import PaymentsApi
from .fulfillment import FulfillmentApi

__all__ = ["AuthApi", "CatalogApi", "OrdersApi", "InventoryApi", "PaymentsApi", "FulfillmentApi"]
""")

    write_file(f"{pkg_dir}/auth.py", """import httpx
from typing import Dict, Any

class AuthApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def register(self, email: str, password: str, first_name: str, last_name: str) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/auth/register", json={
            "email": email,
            "password": password,
            "firstName": first_name,
            "lastName": last_name
        })
        resp.raise_for_status()
        return resp.json()["data"]

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/auth/login", json={
            "email": email,
            "password": password
        })
        resp.raise_for_status()
        return resp.json()["data"]
""")

    write_file(f"{pkg_dir}/catalog.py", """import httpx
from typing import Dict, Any, List

class CatalogApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def list_products(self, page: int = 1, limit: int = 20) -> List[Dict[str, Any]]:
        resp = await self._client.get(f"/api/v1/catalog/products?page={page}&limit={limit}")
        resp.raise_for_status()
        return resp.json()["data"]

    async def get_product(self, product_id: str) -> Dict[str, Any]:
        resp = await self._client.get(f"/api/v1/catalog/products/{product_id}")
        resp.raise_for_status()
        return resp.json()["data"]
""")

    write_file(f"{pkg_dir}/orders.py", """import httpx
from typing import Dict, Any

class OrdersApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/orders", json=order_data)
        resp.raise_for_status()
        return resp.json()["data"]

    async def get_order(self, order_id: str) -> Dict[str, Any]:
        resp = await self._client.get(f"/api/v1/orders/{order_id}")
        resp.raise_for_status()
        return resp.json()["data"]
""")

    write_file(f"{pkg_dir}/inventory.py", """import httpx
from typing import Dict, Any

class InventoryApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def set_stock(self, sku: str, warehouse_id: str, quantity: int) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/inventory/stock", json={
            "sku": sku,
            "warehouseId": warehouse_id,
            "quantity": quantity
        })
        resp.raise_for_status()
        return resp.json()["data"]

    async def reserve_stock(self, order_id: str, sku: str, quantity: int) -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/inventory/reserve", json={
            "orderId": order_id,
            "sku": sku,
            "quantity": quantity
        })
        resp.raise_for_status()
        return resp.json()["data"]
""")

    write_file(f"{pkg_dir}/payments.py", """import httpx
from typing import Dict, Any

class PaymentsApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def authorize(self, order_id: str, amount_cents: int, currency: str = "USD") -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/payments/authorize", json={
            "orderId": order_id,
            "amountCents": amount_cents,
            "currency": currency
        })
        resp.raise_for_status()
        return resp.json()["data"]
""")

    write_file(f"{pkg_dir}/fulfillment.py", """import httpx
from typing import Dict, Any

class FulfillmentApi:
    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def create_shipment(self, order_id: str, destination_address: Dict[str, Any], carrier: str = "FEDEX") -> Dict[str, Any]:
        resp = await self._client.post("/api/v1/fulfillment/shipments", json={
            "orderId": order_id,
            "destinationAddress": destination_address,
            "carrier": carrier
        })
        resp.raise_for_status()
        return resp.json()["data"]
""")

    print("Generated Python SDK API Clients.")

def generate_deep_architecture_docs():
    # 1. Bounded Contexts
    write_file("docs/architecture/domain-driven-design-bounded-contexts.md", """# Domain-Driven Design (DDD) Bounded Contexts & Ubiquitous Language

## 1. Overview
The NovaCommerce platform is divided into nine autonomous Bounded Contexts aligned strictly with strategic business capabilities. Each context encapsulates its private domain models, persistence tables, and invariants.

```
+------------------------------------------------------------------------------------+
|                               NovaCommerce Ecosystem                               |
+------------------------------------------------------------------------------------+
|  [ Identity & Access Management ]  -->  [ User Profile & Organization Context ]    |
|              |                                            |                        |
|              v                                            v                        |
|  [ Product Catalog Context ]       -->  [ Real-Time Inventory & Warehouse Context ]|
|              |                                            |                        |
|              v                                            v                        |
|  [ Order & Saga Context ]          -->  [ Payment & Double-Entry Ledger Context ]  |
|              |                                            |                        |
|              v                                            v                        |
|  [ Fulfillment & Courier Context ] -->  [ Omni-Channel Notification Context ]       |
|              |                                            |                        |
|              +--------------------+-----------------------+                        |
|                                   |                                                |
|                                   v                                                |
|                   [ Analytics & Audit Context ]                                    |
+------------------------------------------------------------------------------------+
```

## 2. Context Definitions & Aggregate Roots

### A. Identity & Access Management (IAM)
- **Aggregate Root**: `User`
- **Entities**: `UserSession`, `PasswordResetToken`, `MfaCredential`
- **Value Objects**: `EmailAddress`, `HashedPassword`, `UserRole`, `Permission`
- **Domain Invariants**:
  - Email addresses must be globally unique and validated according to RFC 5322.
  - Passwords must be hashed using Argon2id with 64MB memory cost and minimum 3 iterations.
  - Accounts are locked after 5 consecutive failed login attempts within a 15-minute sliding window.

### B. Product Catalog Context
- **Aggregate Root**: `Product`
- **Entities**: `ProductVariant`, `ProductImage`, `Category`
- **Value Objects**: `SKU`, `Slug`, `Money`, `DynamicAttributeSet`
- **Domain Invariants**:
  - SKU must be unique across all active and draft products.
  - Base price amount cannot be negative.
  - Categories cannot form cyclic parent-child hierarchies.

### C. Real-Time Inventory Context
- **Aggregate Root**: `InventoryStock`
- **Entities**: `Warehouse`, `InventoryReservation`, `ReplenishmentOrder`
- **Value Objects**: `BinLocation`, `SafetyStockThreshold`, `ReorderQuantity`
- **Domain Invariants**:
  - `reservedQuantity + allocatedQuantity` must never exceed `onHandQuantity`.
  - Concurrent stock mutations must match the expected entity `version` (Optimistic Concurrency Control).
  - Uncommitted stock reservations automatically expire after 30 minutes.

### D. Order & Saga Orchestration Context
- **Aggregate Root**: `Order`
- **Entities**: `OrderItem`, `ReturnRequest`, `SagaExecutionRecord`
- **Value Objects**: `OrderNumber`, `OrderStatus`, `TaxBreakdown`, `ShippingFee`
- **Domain Invariants**:
  - Orders cannot transition backwards in the lifecycle state machine.
  - Order total amount must equal `subtotal + tax + shippingFee - discountAmount`.
  - Mutating operations require a verified `Idempotency-Key`.

### E. Payment & Financial Ledger Context
- **Aggregate Root**: `PaymentTransaction`
- **Entities**: `LedgerAccount`, `LedgerJournalEntry`, `LedgerLine`
- **Value Objects**: `TransactionReference`, `Currency`, `DebitCreditEntry`
- **Domain Invariants**:
  - In every journal entry, `SUM(debit amounts) == SUM(credit amounts)` (Double-Entry Invariant).
  - Posted journal entries and lines are strictly immutable (append-only ledger).
  - Refund amounts cannot exceed the original captured payment transaction.

### F. Fulfillment & Logistics Context
- **Aggregate Root**: `Shipment`
- **Entities**: `Carrier`, `PackingPlan`, `CarrierTrackingEvent`
- **Value Objects**: `TrackingNumber`, `Dimensions3D`, `ServiceLevel`
- **Domain Invariants**:
  - Shipment billable weight is the maximum of gross scale weight and dimensional volumetric weight.
  - Tracking numbers must match carrier format patterns (e.g. 12 digits for FedEx Express, 1Z... for UPS).
""")

    # 2. Saga Specification
    write_file("docs/architecture/saga-state-machine-spec.md", """# Distributed Checkout Saga: Orchestration & Compensation Protocol

## 1. Saga Execution Topology

The Checkout Saga orchestrates a 4-step distributed transaction across autonomous microservices using a centralized orchestrator with forward recovery and backwards compensation.

```
       [Order Service] (Orchestrator)
              |
       1. Reserve Stock
              v
     [Inventory Service]  ---(Success)---+
              |                           |
              | (Fail: Out of Stock)      |
              v                           v
     [Cancel Order]              2. Authorize Payment
                                          v
                                 [Payment Service] ---(Success)---+
                                          |                       |
                                          | (Fail: Card Declined) |
                                          v                       v
                                 [Release Inventory]     3. Create Shipment
                                 [Cancel Order]                   v
                                                        [Fulfillment Service] --(Success)--+
                                                                  |                        |
                                                                  | (Fail: Bad Address)    |
                                                                  v                        v
                                                         [Void Payment]           4. Send Notification
                                                         [Release Inventory]               v
                                                         [Cancel Order]           [Notification Svc]
                                                                                           v
                                                                                  [Order Complete]
```

## 2. Step Specifications & Compensation Logic

| Step Order | Microservice | Action Name | Forward Payload | Compensating Rollback Action |
|:---|:---|:---|:---|:---|
| **1** | `Inventory Service` | `ReserveStock` | `{ orderId, sku, qty }` | `ReleaseReservation({ orderId })` |
| **2** | `Payment Service` | `AuthorizePayment` | `{ orderId, userId, amountCents }` | `VoidOrRefundPayment({ transactionId })` |
| **3** | `Fulfillment Service` | `CreateShipment` | `{ orderId, address, carrier }` | `CancelShipmentLabel({ shipmentId })` |
| **4** | `Notification Service`| `SendConfirmation`| `{ orderId, template: 'order_conf' }`| None (Idempotent notification) |
""")

    # 3. Double-Entry Ledger Invariants
    write_file("docs/architecture/double-entry-ledger-invariants.md", """# Double-Entry General Ledger: Formal Mathematical Proofs & Invariants

## 1. Fundamental Accounting Equation
$$\\text{Assets} = \\text{Liabilities} + \\text{Equity} + (\\text{Revenues} - \\text{Expenses})$$

## 2. Invariant Proofs
For every Journal Entry $J = \\{ L_1, L_2, \\dots, L_n \\}$:

$$\\sum_{i=1}^{n} \\text{Debit}(L_i) - \\sum_{i=1}^{n} \\text{Credit}(L_i) = 0$$

If any journal entry attempts to persist where $\\Delta \\neq 0$, the database transaction is immediately aborted with `ERR_PAYMENT_LEDGER_UNBALANCED`.
""")

    # 4. Zero-Trust Network Policies
    write_file("docs/architecture/zero-trust-network-policies.md", """# Zero-Trust Microservice Network Security & mTLS Policy

## 1. Network Topology
All microservice-to-microservice traffic is governed by Kubernetes NetworkPolicies enforcing default-deny ingress and egress rules.

1. **Ingress Controller**: Only component exposed to external public traffic on ports 80/443.
2. **API Gateway**: Sole entity authorized to send HTTP requests to internal microservice REST ports.
3. **Internal Microservices**: Isolated within Kubernetes cluster namespace with mutual TLS (mTLS) cryptographic encryption.
""")

    # 5. SRE Observability & SLO/SLI
    write_file("docs/architecture/sre-observability-slo-sli.md", """# SRE Observability, Service Level Indicators (SLIs), and SLOs

## 1. Service Level Objectives (SLOs)

| Microservice | Target Availability (SLO) | Latency P95 Target | Latency P99 Target | Error Budget (Monthly) |
|:---|:---|:---|:---|:---|
| **API Gateway** | 99.99% | < 15ms | < 45ms | 4.38 minutes downtime |
| **Auth Service** | 99.95% | < 40ms | < 120ms | 21.92 minutes downtime |
| **Catalog Service** | 99.95% | < 25ms | < 80ms | 21.92 minutes downtime |
| **Order Service** | 99.90% | < 80ms | < 250ms | 43.83 minutes downtime |
| **Payment Service** | 99.95% | < 150ms | < 500ms | 21.92 minutes downtime |
| **Inventory Service**| 99.95% | < 30ms | < 90ms | 21.92 minutes downtime |
""")

    print("Generated deep architecture documents.")

if __name__ == "__main__":
    generate_typescript_sdk_clients()
    generate_python_sdk_clients()
    generate_deep_architecture_docs()
    print("SDK and Architecture expansion complete.")
