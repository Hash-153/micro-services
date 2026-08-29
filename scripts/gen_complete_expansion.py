import os
import json

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_additional_architecture_guides():
    # 1. API Gateway Routing Matrix
    write_file("docs/architecture/api-gateway-routing-matrix.md", """# NovaCommerce API Gateway: Comprehensive Routing & Security Matrix

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
""")

    # 2. Event-Driven Messaging Taxonomy
    write_file("docs/architecture/event-driven-messaging-taxonomy.md", """# Event-Driven Messaging Taxonomy & Exchange Topology

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
""")

    # 3. PCI-DSS Compliance and Tokenization
    write_file("docs/architecture/pci-dss-compliance-and-tokenization.md", """# PCI-DSS Level 1 Compliance & Cardholder Data Tokenization Architecture

## 1. Out-of-Scope Architecture (SAQ A-EP)
NovaCommerce achieves zero cardholder data footprint across application databases:
1. **Direct Tokenization**: Card numbers (PAN), CVVs, and expiration dates are collected exclusively via Stripe Elements / Adyen Drop-in iframes directly from the customer browser.
2. **Ephemeral Tokens**: The browser receives an opaque gateway token (`tok_...` or `pm_...`) which is transmitted to our backend.
3. **Zero PAN Storage**: Databases store exclusively non-sensitive token references, card brand (e.g. Visa), last 4 digits (`4242`), and expiration month/year for display.
""")

    # 4. Incident Response Playbook
    write_file("docs/architecture/incident-response-playbook.md", """# NovaCommerce Incident Response & Disaster Recovery Playbook

## 1. Severity Definitions
- **SEV-1 (Critical Outage)**: Checkout saga or payment processing down platform-wide. Response SLA: 5 minutes.
- **SEV-2 (Major Degradation)**: Single carrier integration offline or inventory reservation delays. Response SLA: 15 minutes.
- **SEV-3 (Minor Issue)**: Analytics rollup delay or non-critical notification latency. Response SLA: 2 hours.

## 2. Triage & Remediation Runbooks

### Runbook 1: Payment Gateway Outage
1. Inspect gateway latency in Prometheus: `rate(payment_gateway_duration_seconds_bucket[5m])`.
2. Trigger automated fallback to secondary processor in `PaymentGatewayRouter`.
3. Post notification to customer status page.

### Runbook 2: Saga Rollback Spike
1. Query order failure causes: `SELECT cancellation_reason, COUNT(*) FROM orders WHERE created_at > NOW() - INTERVAL '15 minutes' GROUP BY 1`.
2. If `INVENTORY_OUT_OF_STOCK` exceeds 10%, verify warehouse reservation sync locks.
""")

    print("Generated Architecture Guides.")

def generate_fixtures_suite():
    # Categories Fixture (50 categories)
    cats = []
    parents = ["Electronics", "Computers", "Home & Kitchen", "Fashion", "Sports & Outdoors", "Automotive", "Books & Media", "Health & Wellness", "Tools & Industrial", "Office Supplies"]
    for idx, p in enumerate(parents):
        parent_id = f"cat-parent-{idx+1:03d}"
        cats.append({
            "id": parent_id,
            "name": p,
            "slug": p.lower().replace(" & ", "-").replace(" ", "-"),
            "parentId": None,
            "displayOrder": idx + 1,
            "isActive": True
        })
        for sub in range(1, 5):
            sub_id = f"cat-sub-{idx+1:02d}-{sub:02d}"
            cats.append({
                "id": sub_id,
                "name": f"{p} Subcategory {sub}",
                "slug": f"{p.lower().replace(' & ', '-').replace(' ', '-')}-sub-{sub}",
                "parentId": parent_id,
                "displayOrder": sub,
                "isActive": True
            })
    write_file("scripts/fixtures/categories_fixture.json", json.dumps(cats, indent=2))

    # Chart of Accounts Fixture
    accounts = [
        {"accountNumber": "1010", "name": "Operating Cash & Bank Account", "type": "ASSET", "currency": "USD"},
        {"accountNumber": "1020", "name": "Stripe Processor Clearing Account", "type": "ASSET", "currency": "USD"},
        {"accountNumber": "1030", "name": "PayPal Processor Clearing Account", "type": "ASSET", "currency": "USD"},
        {"accountNumber": "1040", "name": "Accounts Receivable", "type": "ASSET", "currency": "USD"},
        {"accountNumber": "1050", "name": "Inventory Asset - On-Hand Stock", "type": "ASSET", "currency": "USD"},
        {"accountNumber": "2010", "name": "Accounts Payable - Suppliers", "type": "LIABILITY", "currency": "USD"},
        {"accountNumber": "2020", "name": "Sales Tax Payable - State Jurisdictions", "type": "LIABILITY", "currency": "USD"},
        {"accountNumber": "2030", "name": "Unearned Revenue / Gift Card Liability", "type": "LIABILITY", "currency": "USD"},
        {"accountNumber": "3010", "name": "Common Stock Paid-in Capital", "type": "EQUITY", "currency": "USD"},
        {"accountNumber": "3020", "name": "Retained Earnings", "type": "EQUITY", "currency": "USD"},
        {"accountNumber": "4010", "name": "Product Sales Gross Revenue", "type": "REVENUE", "currency": "USD"},
        {"accountNumber": "4020", "name": "Shipping & Freight Income", "type": "REVENUE", "currency": "USD"},
        {"accountNumber": "4090", "name": "Sales Discounts & Promotions (Contra-Revenue)", "type": "REVENUE", "currency": "USD"},
        {"accountNumber": "5010", "name": "Cost of Goods Sold (COGS)", "type": "EXPENSE", "currency": "USD"},
        {"accountNumber": "5020", "name": "Carrier Freight & Delivery Expense", "type": "EXPENSE", "currency": "USD"},
        {"accountNumber": "5030", "name": "Payment Gateway Processing Interchange Fees", "type": "EXPENSE", "currency": "USD"}
    ]
    write_file("scripts/fixtures/chart_of_accounts_fixture.json", json.dumps(accounts, indent=2))

    # Shipping Rates Fixture
    rates = [
        {"carrier": "FEDEX", "service": "GROUND", "baseRateCents": 850, "perKgRateCents": 150, "estimatedDays": 3},
        {"carrier": "FEDEX", "service": "EXPRESS_2DAY", "baseRateCents": 1850, "perKgRateCents": 300, "estimatedDays": 2},
        {"carrier": "FEDEX", "service": "OVERNIGHT", "baseRateCents": 3450, "perKgRateCents": 550, "estimatedDays": 1},
        {"carrier": "UPS", "service": "GROUND", "baseRateCents": 820, "perKgRateCents": 140, "estimatedDays": 3},
        {"carrier": "UPS", "service": "NEXT_DAY_AIR", "baseRateCents": 3500, "perKgRateCents": 520, "estimatedDays": 1},
        {"carrier": "DHL", "service": "EXPRESS_WORLDWIDE", "baseRateCents": 4200, "perKgRateCents": 750, "estimatedDays": 2}
    ]
    write_file("scripts/fixtures/shipping_rates_fixture.json", json.dumps(rates, indent=2))

    print("Generated seed fixtures.")

def generate_test_suites():
    # Order Service Returns Test
    write_file("services/order-service/tests/returns.test.ts", """import { ReturnStateMachine, ReturnRequestStatus } from '../src/domain/refund-state-machine.js';

describe('Order Return & RMA State Machine Suite', () => {
  it('should allow valid return progression', () => {
    expect(ReturnStateMachine.canTransition(ReturnRequestStatus.SUBMITTED, ReturnRequestStatus.APPROVED)).toBe(true);
    expect(ReturnStateMachine.canTransition(ReturnRequestStatus.APPROVED, ReturnRequestStatus.RETURN_LABEL_SENT)).toBe(true);
    expect(ReturnStateMachine.canTransition(ReturnRequestStatus.RETURN_LABEL_SENT, ReturnRequestStatus.PACKAGE_RECEIVED)).toBe(true);
    expect(ReturnStateMachine.canTransition(ReturnRequestStatus.PACKAGE_RECEIVED, ReturnRequestStatus.INSPECTION_PASSED)).toBe(true);
    expect(ReturnStateMachine.canTransition(ReturnRequestStatus.INSPECTION_PASSED, ReturnRequestStatus.REFUND_ISSUED)).toBe(true);
  });

  it('should reject illegal return state jump', () => {
    expect(() => {
      ReturnStateMachine.transition(ReturnRequestStatus.SUBMITTED, ReturnRequestStatus.REFUND_ISSUED);
    }).toThrow();
  });
});
""")

    # Payment Service Currency Test
    write_file("services/payment-service/tests/exchange-rate.test.ts", """import { CurrencyConverter } from '../src/domain/currency-exchange-rate.js';
import { Currency } from '@novacommerce/core-types';

describe('Multi-Currency FX Exchange Engine Suite', () => {
  it('should return identical money object for same currency conversion', () => {
    const money = { amount: 5000, currency: Currency.USD };
    const res = CurrencyConverter.convert(money, Currency.USD);
    expect(res.amount).toBe(5000);
    expect(res.currency).toBe(Currency.USD);
  });

  it('should convert USD to EUR with spread correctly', () => {
    const money = { amount: 10000, currency: Currency.USD }; // $100.00
    const res = CurrencyConverter.convert(money, Currency.EUR, 0.5);
    expect(res.currency).toBe(Currency.EUR);
    expect(res.amount).toBeGreaterThan(9000);
    expect(res.amount).toBeLessThan(10000);
  });
});
""")

    # Inventory Service Reorder Test
    write_file("services/inventory-service/tests/reorder.test.ts", """import { ReorderCalculator } from '../src/domain/reorder-calculator.js';

describe('Inventory Safety Stock & Reorder Formula Suite', () => {
  it('should recommend ordering when stock is at or below reorder point', () => {
    const advice = ReorderCalculator.calculateReorderParameters(
      {
        sku: 'SKU-001',
        averageDailySales: 10,
        leadTimeDays: 7,
        supplierReliabilityPercent: 95,
        serviceLevelZScore: 1.65,
        demandStandardDeviation: 2.5
      },
      75, // on hand
      10  // reserved -> 65 available <= reorder point (70 + safety)
    );

    expect(advice.safetyStockUnits).toBeGreaterThan(0);
    expect(advice.reorderPointUnits).toBeGreaterThan(70);
    expect(advice.economicOrderQuantity).toBeGreaterThan(0);
    expect(advice.suggestedAction).toBe('ORDER_NOW');
  });
});
""")

    # Catalog Service Attribute Validator Test
    write_file("services/catalog-service/tests/attributes.test.ts", """import { ProductAttributeValidator, AttributeSchemaField } from '../src/domain/attribute-validator.js';

describe('Product Dynamic Attribute Validation Suite', () => {
  const schema: AttributeSchemaField[] = [
    { name: 'screenSizeInches', label: 'Screen Size', type: 'NUMBER', required: true, minValue: 5, maxValue: 100 },
    { name: 'color', label: 'Color', type: 'ENUM', required: true, allowedValues: ['Black', 'Silver', 'Space Gray'] },
    { name: 'hasTouchScreen', label: 'Touch Screen', type: 'BOOLEAN', required: false }
  ];

  it('should validate valid attributes', () => {
    const res = ProductAttributeValidator.validate(schema, {
      screenSizeInches: 15.6,
      color: 'Space Gray',
      hasTouchScreen: true
    });
    expect(res.isValid).toBe(true);
    expect(res.errors.length).toBe(0);
  });

  it('should report errors on missing required attribute or illegal enum value', () => {
    const res = ProductAttributeValidator.validate(schema, {
      screenSizeInches: 15.6,
      color: 'Hot Pink' // not in enum
    });
    expect(res.isValid).toBe(false);
    expect(res.errors.some(e => e.includes('Hot Pink'))).toBe(true);
  });
});
""")

    print("Generated comprehensive test suites.")

if __name__ == "__main__":
    generate_additional_architecture_guides()
    generate_fixtures_suite()
    generate_test_suites()
    print("Complete expansion finished successfully.")
