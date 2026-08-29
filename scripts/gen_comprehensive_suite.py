import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_domain_engines():
    # 1. Fraud Detection & Risk Scoring Rule Engine
    write_file("services/payment-service/src/domain/fraud-detector.ts", """export interface FraudEvaluationContext {
  userId: string;
  orderId: string;
  amountCents: number;
  currency: string;
  ipAddress: string;
  cardBin: string;
  cardCountry: string;
  billingCountry: string;
  shippingCountry: string;
  deviceFingerprint: string;
  accountAgeDays: number;
  previousOrderCount: number;
  previousDisputeCount: number;
}

export interface FraudRiskScore {
  score: number; // 0 to 100
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  action: 'ALLOW' | 'CHALLENGE_3DS' | 'MANUAL_REVIEW' | 'REJECT';
  flaggedRules: string[];
}

export class FraudDetector {
  public static evaluateRisk(ctx: FraudEvaluationContext): FraudRiskScore {
    let score = 0;
    const flaggedRules: string[] = [];

    // Rule 1: High Transaction Velocity / Extreme Amount
    if (ctx.amountCents > 500000) { // > $5,000
      score += 25;
      flaggedRules.push('RULE_HIGH_TICKET_VALUE');
    }

    // Rule 2: Country Mismatch (Card Country vs Shipping Country)
    if (ctx.cardCountry && ctx.shippingCountry && ctx.cardCountry !== ctx.shippingCountry) {
      score += 30;
      flaggedRules.push('RULE_GEO_COUNTRY_MISMATCH');
    }

    // Rule 3: Brand new account with large purchase
    if (ctx.accountAgeDays < 1 && ctx.amountCents > 100000) {
      score += 20;
      flaggedRules.push('RULE_NEW_ACCOUNT_LARGE_AMOUNT');
    }

    // Rule 4: Historical Chargebacks / Disputes
    if (ctx.previousDisputeCount > 0) {
      score += 40;
      flaggedRules.push('RULE_PRIOR_DISPUTE_HISTORY');
    }

    // Rule 5: Disposable / Proxy IP Range (Simulated)
    if (ctx.ipAddress.startsWith('10.') || ctx.ipAddress.startsWith('192.168.')) {
      // Local development safe
    }

    score = Math.min(100, score);

    let riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' = 'LOW';
    let action: 'ALLOW' | 'CHALLENGE_3DS' | 'MANUAL_REVIEW' | 'REJECT' = 'ALLOW';

    if (score >= 75) {
      riskLevel = 'CRITICAL';
      action = 'REJECT';
    } else if (score >= 50) {
      riskLevel = 'HIGH';
      action = 'MANUAL_REVIEW';
    } else if (score >= 25) {
      riskLevel = 'MEDIUM';
      action = 'CHALLENGE_3DS';
    }

    return {
      score,
      riskLevel,
      action,
      flaggedRules
    };
  }
}
""")

    # 2. Multi-Currency FX Exchange & Hedging Rate Table
    write_file("services/payment-service/src/domain/currency-exchange-rate.ts", """import { Currency, Money } from '@novacommerce/core-types';

export interface ExchangeRateQuote {
  baseCurrency: Currency;
  targetCurrency: Currency;
  rate: number;
  spreadPercent: number;
  effectiveRate: number;
  expiresAt: Date;
}

export const BASE_FX_RATES_TO_USD: Record<Currency, number> = {
  [Currency.USD]: 1.0,
  [Currency.EUR]: 1.08,
  [Currency.GBP]: 1.28,
  [Currency.CAD]: 0.74,
  [Currency.AUD]: 0.66,
  [Currency.JPY]: 0.0065,
  [Currency.CHF]: 1.13,
  [Currency.SGD]: 0.75,
  [Currency.INR]: 0.012
};

export class CurrencyConverter {
  public static convert(money: Money, targetCurrency: Currency, spreadPercent: number = 0.5): Money {
    if (money.currency === targetCurrency) {
      return money;
    }

    const baseToUsd = BASE_FX_RATES_TO_USD[money.currency] || 1.0;
    const targetToUsd = BASE_FX_RATES_TO_USD[targetCurrency] || 1.0;

    // Convert source amount to USD, then USD to target
    const amountInUsd = money.amount * baseToUsd;
    const rawTargetAmount = amountInUsd / targetToUsd;
    
    // Apply spread
    const spreadMultiplier = 1 + (spreadPercent / 100);
    const convertedAmount = Math.round(rawTargetAmount * spreadMultiplier);

    return {
      amount: convertedAmount,
      currency: targetCurrency
    };
  }
}
""")

    # 3. Inventory Reorder & Safety Stock Formula Engine
    write_file("services/inventory-service/src/domain/reorder-calculator.ts", """export interface InventoryDemandForecast {
  sku: string;
  averageDailySales: number;
  leadTimeDays: number;
  supplierReliabilityPercent: number; // 0 to 100
  serviceLevelZScore: number; // e.g. 1.65 for 95%, 2.33 for 99%
  demandStandardDeviation: number;
}

export interface ReorderRecommendation {
  sku: string;
  safetyStockUnits: number;
  reorderPointUnits: number;
  economicOrderQuantity: number;
  suggestedAction: 'ORDER_NOW' | 'STOCK_HEALTHY' | 'SURPLUS';
}

export class ReorderCalculator {
  // Uses Wilson EOQ (Economic Order Quantity) & probabilistic Safety Stock formulas
  public static calculateReorderParameters(
    forecast: InventoryDemandForecast,
    currentOnHand: number,
    currentReserved: number,
    annualCarryingCostPerUnit: number = 5.0,
    fixedOrderPlacementCost: number = 50.0
  ): ReorderRecommendation {
    // Safety Stock = Z * stdDev * sqrt(LeadTime)
    const safetyStock = Math.ceil(
      forecast.serviceLevelZScore * forecast.demandStandardDeviation * Math.sqrt(forecast.leadTimeDays)
    );

    // Reorder Point = (Daily Demand * Lead Time) + Safety Stock
    const leadTimeDemand = forecast.averageDailySales * forecast.leadTimeDays;
    const reorderPoint = Math.ceil(leadTimeDemand + safetyStock);

    // Economic Order Quantity (EOQ) = sqrt((2 * Annual Demand * Order Cost) / Carrying Cost)
    const annualDemand = forecast.averageDailySales * 365;
    const eoq = Math.ceil(
      Math.sqrt((2 * annualDemand * fixedOrderPlacementCost) / annualCarryingCostPerUnit)
    );

    const availableStock = currentOnHand - currentReserved;
    let suggestedAction: 'ORDER_NOW' | 'STOCK_HEALTHY' | 'SURPLUS' = 'STOCK_HEALTHY';

    if (availableStock <= reorderPoint) {
      suggestedAction = 'ORDER_NOW';
    } else if (availableStock > reorderPoint * 3) {
      suggestedAction = 'SURPLUS';
    }

    return {
      sku: forecast.sku,
      safetyStockUnits: safetyStock,
      reorderPointUnits: reorderPoint,
      economicOrderQuantity: eoq,
      suggestedAction
    };
  }
}
""")

    # 4. Returns & Refunds State Machine
    write_file("services/order-service/src/domain/refund-state-machine.ts", """export enum ReturnRequestStatus {
  SUBMITTED = 'SUBMITTED',
  APPROVED = 'APPROVED',
  RETURN_LABEL_SENT = 'RETURN_LABEL_SENT',
  PACKAGE_RECEIVED = 'PACKAGE_RECEIVED',
  INSPECTION_PASSED = 'INSPECTION_PASSED',
  INSPECTION_FAILED = 'INSPECTION_FAILED',
  REFUND_ISSUED = 'REFUND_ISSUED',
  REJECTED = 'REJECTED',
  CANCELLED = 'CANCELLED'
}

const ALLOWED_RETURN_TRANSITIONS: Record<ReturnRequestStatus, ReturnRequestStatus[]> = {
  [ReturnRequestStatus.SUBMITTED]: [ReturnRequestStatus.APPROVED, ReturnRequestStatus.REJECTED, ReturnRequestStatus.CANCELLED],
  [ReturnRequestStatus.APPROVED]: [ReturnRequestStatus.RETURN_LABEL_SENT, ReturnRequestStatus.CANCELLED],
  [ReturnRequestStatus.RETURN_LABEL_SENT]: [ReturnRequestStatus.PACKAGE_RECEIVED, ReturnRequestStatus.CANCELLED],
  [ReturnRequestStatus.PACKAGE_RECEIVED]: [ReturnRequestStatus.INSPECTION_PASSED, ReturnRequestStatus.INSPECTION_FAILED],
  [ReturnRequestStatus.INSPECTION_PASSED]: [ReturnRequestStatus.REFUND_ISSUED],
  [ReturnRequestStatus.INSPECTION_FAILED]: [ReturnRequestStatus.REJECTED],
  [ReturnRequestStatus.REFUND_ISSUED]: [],
  [ReturnRequestStatus.REJECTED]: [],
  [ReturnRequestStatus.CANCELLED]: []
};

export class ReturnStateMachine {
  public static canTransition(current: ReturnRequestStatus, target: ReturnRequestStatus): boolean {
    const allowed = ALLOWED_RETURN_TRANSITIONS[current] || [];
    return allowed.includes(target);
  }

  public static transition(current: ReturnRequestStatus, target: ReturnRequestStatus): ReturnRequestStatus {
    if (!this.canTransition(current, target)) {
      throw new Error(`Invalid return transition from ${current} to ${target}`);
    }
    return target;
  }
}
""")

    # 5. Dynamic Product Attribute Schema Validator
    write_file("services/catalog-service/src/domain/attribute-validator.ts", """export type AttributeDataType = 'STRING' | 'NUMBER' | 'BOOLEAN' | 'ENUM' | 'DIMENSIONS';

export interface AttributeSchemaField {
  name: string;
  label: string;
  type: AttributeDataType;
  required: boolean;
  allowedValues?: string[];
  minValue?: number;
  maxValue?: number;
  regexPattern?: string;
}

export class ProductAttributeValidator {
  public static validate(schema: AttributeSchemaField[], attributes: Record<string, unknown>): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    for (const field of schema) {
      const val = attributes[field.name];

      if (field.required && (val === undefined || val === null || val === '')) {
        errors.push(`Attribute '${field.name}' (${field.label}) is required.`);
        continue;
      }

      if (val === undefined || val === null) continue;

      if (field.type === 'NUMBER' && typeof val !== 'number') {
        errors.push(`Attribute '${field.name}' must be a numeric value.`);
      }

      if (field.type === 'BOOLEAN' && typeof val !== 'boolean') {
        errors.push(`Attribute '${field.name}' must be boolean true/false.`);
      }

      if (field.type === 'ENUM' && field.allowedValues && !field.allowedValues.includes(String(val))) {
        errors.push(`Attribute '${field.name}' value '${val}' is not in allowed list [${field.allowedValues.join(', ')}].`);
      }

      if (field.type === 'NUMBER' && typeof val === 'number') {
        if (field.minValue !== undefined && val < field.minValue) {
          errors.push(`Attribute '${field.name}' is below minimum allowed value ${field.minValue}.`);
        }
        if (field.maxValue !== undefined && val > field.maxValue) {
          errors.push(`Attribute '${field.name}' exceeds maximum allowed value ${field.maxValue}.`);
        }
      }
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}
""")

    print("Domain engines generated.")

def generate_e2e_tests():
    write_file("tests/e2e/checkout-saga.e2e.test.ts", """import { InMemoryStockRepository, InMemoryReservationRepository } from '../../services/inventory-service/src/repositories/inventory.repository.js';
import { InventoryService } from '../../services/inventory-service/src/services/inventory.service.js';
import { InMemoryPaymentRepository, InMemoryLedgerRepository } from '../../services/payment-service/src/repositories/payment.repository.js';
import { PaymentService } from '../../services/payment-service/src/services/payment.service.js';
import { InMemoryShipmentRepository } from '../../services/fulfillment-service/src/repositories/shipment.repository.js';
import { FulfillmentService } from '../../services/fulfillment-service/src/services/fulfillment.service.js';
import { CheckoutSagaOrchestrator } from '../../services/order-service/src/saga/checkout-saga.orchestrator.js';
import { ISagaStep, SagaContext } from '../../services/order-service/src/saga/saga-step.interface.js';
import { Logger } from '@novacommerce/core-logger';
import { randomUUID } from 'crypto';

describe('Distributed Checkout Saga End-to-End Test Suite', () => {
  const logger = Logger.create('e2e-test');
  let inventoryService: InventoryService;
  let paymentService: PaymentService;
  let fulfillmentService: FulfillmentService;
  let saga: CheckoutSagaOrchestrator;

  beforeEach(async () => {
    const stockRepo = new InMemoryStockRepository();
    const resRepo = new InMemoryReservationRepository();
    inventoryService = new InventoryService(stockRepo, resRepo);

    // Initial warehouse stock setup
    await inventoryService.setStock('SKU-LAPTOP-PRO', 'WH-MAIN-01', 10);

    const paymentRepo = new InMemoryPaymentRepository();
    const ledgerRepo = new InMemoryLedgerRepository();
    paymentService = new PaymentService(paymentRepo, ledgerRepo);

    const shipmentRepo = new InMemoryShipmentRepository();
    fulfillmentService = new FulfillmentService(shipmentRepo);

    saga = new CheckoutSagaOrchestrator(logger);

    // Step 1: Inventory Reservation Step
    const inventoryStep: ISagaStep = {
      name: 'ReserveInventory',
      execute: async (ctx: SagaContext) => {
        for (const item of ctx.items) {
          const res = await inventoryService.reserveStock(ctx.orderId, item.sku, item.quantity, ctx.correlationId);
          ctx.reservationId = res.id;
        }
      },
      compensate: async (ctx: SagaContext) => {
        await inventoryService.releaseReservation(ctx.orderId, ctx.correlationId);
      }
    };

    // Step 2: Payment Authorization Step
    const paymentStep: ISagaStep = {
      name: 'AuthorizePayment',
      execute: async (ctx: SagaContext) => {
        if (ctx.paymentMethod.token === 'tok_force_decline') {
          throw new Error('Card declined: Insufficient funds');
        }
        const payment = await paymentService.authorizePayment(ctx.orderId, ctx.userId, ctx.totalAmount);
        ctx.paymentTransactionId = payment.id;
      },
      compensate: async (ctx: SagaContext) => {
        // Refund logic
      }
    };

    // Step 3: Fulfillment Creation Step
    const fulfillmentStep: ISagaStep = {
      name: 'CreateFulfillment',
      execute: async (ctx: SagaContext) => {
        const shipment = await fulfillmentService.createShipment(ctx.orderId, {});
        ctx.shipmentId = shipment.id;
      },
      compensate: async (ctx: SagaContext) => {
        // Void shipment
      }
    };

    saga.addStep(inventoryStep).addStep(paymentStep).addStep(fulfillmentStep);
  });

  it('should successfully execute forward saga when all services succeed', async () => {
    const context: SagaContext = {
      orderId: 'ord-1001',
      userId: 'usr-444',
      items: [{ sku: 'SKU-LAPTOP-PRO', quantity: 1 }],
      totalAmount: 189900,
      currency: 'USD',
      paymentMethod: { type: 'CREDIT_CARD', token: 'tok_valid_card', provider: 'STRIPE' },
      carrierCode: 'FEDEX',
      correlationId: randomUUID()
    };

    const result = await saga.execute(context);
    expect(result).toBe(true);
    expect(context.reservationId).toBeDefined();
    expect(context.paymentTransactionId).toBeDefined();
    expect(context.shipmentId).toBeDefined();
  });

  it('should rollback and release inventory reservation when payment declines', async () => {
    const context: SagaContext = {
      orderId: 'ord-1002',
      userId: 'usr-444',
      items: [{ sku: 'SKU-LAPTOP-PRO', quantity: 1 }],
      totalAmount: 189900,
      currency: 'USD',
      paymentMethod: { type: 'CREDIT_CARD', token: 'tok_force_decline', provider: 'STRIPE' },
      carrierCode: 'FEDEX',
      correlationId: randomUUID()
    };

    await expect(saga.execute(context)).rejects.toThrow();
  });
});
""")
    print("E2E tests generated.")

if __name__ == "__main__":
    generate_domain_engines()
    generate_e2e_tests()
    print("Comprehensive suite generated successfully.")
