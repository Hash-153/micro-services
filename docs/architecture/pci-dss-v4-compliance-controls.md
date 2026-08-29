# PCI-DSS v4.0 Technical Controls & Security Verification

## 1. Compliance Architecture Overview
NovaCommerce is engineered to strictly satisfy PCI-DSS v4.0 Level 1 requirements under SAQ A-EP scope.

```
+---------------------------------------------------------------------------------------+
|                                  Customer Browser (Client)                            |
|  1. Customer inputs card details into iframe hosted directly by Stripe / Adyen        |
|  2. Stripe / Adyen returns cryptographic token: "tok_visa_4242_sample"                |
+-------------------------------------------+-------------------------------------------+
                                            |
                         3. Opaque Token Transmitted
                                            v
+---------------------------------------------------------------------------------------+
|                       NovaCommerce API Gateway & Payment Service                      |
|  4. Validates JWT, sets idempotency lock, initiates Charge with Token                 |
|  5. Records Double-Entry Ledger Entry (Debit Cash, Credit Revenue)                    |
|  6. ZERO Primary Account Number (PAN), CVV, or Magnetic Stripe Data stored in DB!     |
+---------------------------------------------------------------------------------------+
```

## 2. Technical Control Matrix
- **Control 3.4**: Zero storage of sensitive authentication data (SAD) after authorization.
- **Control 4.1**: Strong cryptography (TLS 1.3) required for all transmission of cardholder data across open public networks.
- **Control 8.3**: Multi-factor authentication (MFA) mandatory for all administrative console and database access.
- **Control 10.2**: Automated audit trail logging for all administrative actions and security events.
