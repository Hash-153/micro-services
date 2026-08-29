# Domain-Driven Design (DDD) Bounded Contexts & Ubiquitous Language

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
