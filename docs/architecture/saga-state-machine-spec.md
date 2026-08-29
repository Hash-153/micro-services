# Distributed Checkout Saga: Orchestration & Compensation Protocol

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
