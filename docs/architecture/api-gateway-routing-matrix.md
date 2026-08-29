# NovaCommerce API Gateway: Comprehensive Routing & Security Matrix

## 1. Gateway Architecture
The API Gateway operates as the primary edge reverse proxy for all client traffic. It handles:
1. Transport Layer Security (TLS 1.3 termination).
2. Sliding-window log rate limiting with Redis.
3. Cryptographic JWT signature and expiration verification.
4. Downstream request routing and circuit breaking.
5. Distributed correlation ID (`x-correlation-id`) injection.

```
+-----------------------------------------------------------------------------------------------+
|                                      API Gateway Route Table                                  |
+-------------------+--------------------+---------------+-------------+------------------------+
| Path Prefix       | Target Service     | Port (HTTP)   | Auth Mode   | Rate Limit (Req/min)   |
+-------------------+--------------------+---------------+-------------+------------------------+
| /api/v1/auth      | auth-service       | 8001          | Public      | 100                    |
| /api/v1/users     | user-service       | 8002          | JWT Bearer  | 200                    |
| /api/v1/catalog   | catalog-service    | 8003          | Public/JWT  | 500                    |
| /api/v1/orders    | order-service      | 8004          | JWT Bearer  | 150                    |
| /api/v1/payments  | payment-service    | 8005          | JWT Bearer  | 100                    |
| /api/v1/fulfill   | fulfillment-service| 8006          | JWT Bearer  | 150                    |
| /api/v1/notify    | notification-svc   | 8007          | Internal    | 100                    |
| /api/v1/analytics | analytics-service  | 8008          | JWT Bearer  | 300                    |
| /api/v1/inventory | inventory-service  | 8009          | JWT Bearer  | 300                    |
+-------------------+--------------------+---------------+-------------+------------------------+
```

## 2. Circuit Breaker Parameters
- **Failure Threshold**: 5 consecutive 5xx responses or socket timeouts.
- **Open State Duration**: 30 seconds cooldown.
- **Half-Open Probe**: 3 successful health requests before closing circuit.
