# Event-Driven Messaging Taxonomy & Exchange Topology

## 1. Exchange and Queue Architecture
All domain events are published to the main topic exchange `novacommerce.events` using structured routing keys following the pattern `<domain>.<entity>.<action>`.

```
                  +--------------------------------+
                  |  Topic Exchange:               |
                  |  novacommerce.events           |
                  +---------------+----------------+
                                  |
            +---------------------+---------------------+
            | (Routing: order.*)  | (Routing: payment.*)| (Routing: inventory.*)
            v                     v                     v
    +---------------+     +---------------+     +---------------+
    | Order Queue   |     | Payment Queue |     | Inventory Q   |
    +---------------+     +---------------+     +---------------+
            |                     |                     |
            +---------------------+---------------------+
                                  | (On 3x Failure)
                                  v
                  +--------------------------------+
                  |  Direct Exchange:              |
                  |  novacommerce.dlx              |
                  +---------------+----------------+
                                  |
                                  v
                  +--------------------------------+
                  |  Dead Letter Queue (DLQ):      |
                  |  novacommerce.dlq              |
                  +--------------------------------+
```

## 2. Complete Routing Key Directory
- `auth.user.registered`
- `auth.user.logged_in`
- `auth.password.reset_requested`
- `user.profile.updated`
- `user.address.added`
- `catalog.product.created`
- `catalog.product.updated`
- `catalog.price.changed`
- `inventory.stock.updated`
- `inventory.reservation.created`
- `inventory.reservation.released`
- `inventory.stock.low_alert`
- `order.created`
- `order.payment_pending`
- `order.paid`
- `order.dispatched`
- `order.delivered`
- `order.cancelled`
- `payment.authorized`
- `payment.captured`
- `payment.refunded`
- `payment.ledger.recorded`
- `fulfillment.label_generated`
- `notification.sent`
- `analytics.event.ingested`
