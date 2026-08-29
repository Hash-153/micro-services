# PCI-DSS v4.0 Cardholder Tokenization & Zero-Footprint Architecture

## 1. Compliance Scope & Data Flow
NovaCommerce maintains zero cardholder data footprint across application databases:
1. **Direct Tokenization**: Card numbers (PAN), CVVs, and expiration dates are collected exclusively via Stripe Elements / Adyen Drop-in iframes directly from the customer browser.
2. **Ephemeral Tokens**: The browser receives an opaque gateway token (`tok_...` or `pm_...`) which is transmitted to our backend.
3. **Zero PAN Storage**: Databases store exclusively non-sensitive token references, card brand (e.g. Visa), last 4 digits (`4242`), and expiration month/year for display.
