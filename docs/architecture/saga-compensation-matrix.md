# Saga Orchestration: Comprehensive Failure Modes & Compensating Actions

| Step Number | Executing Service | Forward Transaction | Failure Scenario | Triggered Compensating Actions | Resulting Order State |
|:---|:---|:---|:---|:---|:---|
| **1** | `Inventory Service` | `ReserveStock(SKU, Qty)` | Stock insufficient / locked | Cancel Order | `CANCELLED (Reason: OUT_OF_STOCK)` |
| **2** | `Payment Service` | `AuthorizePayment(Amount)` | Card declined / 3DS fail | 1. Release Inventory Reservation<br>2. Cancel Order | `CANCELLED (Reason: PAYMENT_DECLINED)` |
| **3** | `Fulfillment Svc` | `CreateShipment(Address)` | Invalid destination address | 1. Void Payment Authorization<br>2. Release Inventory Reservation<br>3. Cancel Order | `CANCELLED (Reason: CARRIER_RESTRICTION)` |
| **4** | `Notification Svc` | `SendConfirmation(Email)` | SMTP timeout / Bounce | None (Notification retries in background without blocking saga) | `COMPLETED` |
