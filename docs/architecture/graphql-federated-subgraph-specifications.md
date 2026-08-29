# GraphQL Federation & Unified Distributed Schema Specification

## 1. Gateway Federation Architecture
The NovaCommerce GraphQL Gateway federates multiple autonomous subgraphs into a unified distributed schema using Apollo Federation v2.

```
                  +----------------------------------+
                  |    GraphQL Federated Gateway     |
                  |    (Port 4000: Schema Router)    |
                  +-----------------+----------------+
                                    |
            +-----------------------+-----------------------+
            |                       |                       |
    +-------v-------+       +-------v-------+       +-------v-------+
    | User Subgraph |       |Catalog Subgraph|      | Order Subgraph|
    | (Port 8002)   |       | (Port 8003)   |       | (Port 8004)   |
    +---------------+       +---------------+       +---------------+
```

## 2. Key Entity Extensions
```graphql
type Product @key(fields: "id") {
  id: ID!
  sku: String!
  name: String!
  basePrice: Money!
  inStock: Boolean! @requires(fields: "sku")
}

type Order @key(fields: "id") {
  id: ID!
  orderNumber: String!
  customer: User! @provides(fields: "email")
  items: [OrderItem!]!
  totalAmount: Money!
}
```
