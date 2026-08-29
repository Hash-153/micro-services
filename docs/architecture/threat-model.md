# NovaCommerce Security Threat Model (STRIDE Methodology)

| Threat Category | Potential Attack Vector | Platform Countermeasure & Defense |
|:---|:---|:---|
| **Spoofing** | Forged JWT tokens or identity impersonation | Cryptographically signed RS256/HS256 tokens, strict issuer & expiry checks |
| **Tampering** | Parameter tampering or unverified price injection | Server-side price resolution, Zod schema validation, HMAC webhooks |
| **Repudiation** | Denying payment or order actions | Immutable audit logs, double-entry ledger journals, signed event streams |
| **Information Disclosure** | Secret leakage or PII exposure in logs | Automated PII redactor in logger, zero credentials in code or git |
| **Denial of Service** | DDoS or endpoint flooding | Sliding-window IP rate limiters, Kubernetes HPA, connection pooling |
| **Elevation of Privilege**| Unauthorized role escalation | Strict RBAC middleware checking token claims on every route |
