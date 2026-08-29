import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_complete_infinity_modules():
    print("Generating comprehensive Complete Infinity Modules...")

    # 1. Payment Merchant Interchange Plus Pricing Engine
    write_file("services/payment-service/src/domain/interchange-plus-calculator.ts", """export interface InterchangeRateFee {
  cardScheme: 'VISA' | 'MASTERCARD' | 'AMEX' | 'DISCOVER';
  cardCategory: 'CONSUMER_CREDIT' | 'CONSUMER_DEBIT' | 'COMMERCIAL_CORPORATE' | 'INTERNATIONAL';
  interchangeRatePercent: number;
  perTransactionFeeCents: number;
  schemeAssessmentBps: number;
}

export const INTERCHANGE_RATE_TABLE: InterchangeRateFee[] = [
  { cardScheme: 'VISA', cardCategory: 'CONSUMER_DEBIT', interchangeRatePercent: 0.05, perTransactionFeeCents: 21, schemeAssessmentBps: 13 }, // Durbin regulated debit
  { cardScheme: 'VISA', cardCategory: 'CONSUMER_CREDIT', interchangeRatePercent: 1.51, perTransactionFeeCents: 10, schemeAssessmentBps: 14 },
  { cardScheme: 'VISA', cardCategory: 'COMMERCIAL_CORPORATE', interchangeRatePercent: 2.20, perTransactionFeeCents: 10, schemeAssessmentBps: 14 },
  { cardScheme: 'VISA', cardCategory: 'INTERNATIONAL', interchangeRatePercent: 1.95, perTransactionFeeCents: 10, schemeAssessmentBps: 55 },
  { cardScheme: 'MASTERCARD', cardCategory: 'CONSUMER_DEBIT', interchangeRatePercent: 0.05, perTransactionFeeCents: 21, schemeAssessmentBps: 13 },
  { cardScheme: 'MASTERCARD', cardCategory: 'CONSUMER_CREDIT', interchangeRatePercent: 1.58, perTransactionFeeCents: 10, schemeAssessmentBps: 14 },
  { cardScheme: 'MASTERCARD', cardCategory: 'COMMERCIAL_CORPORATE', interchangeRatePercent: 2.25, perTransactionFeeCents: 10, schemeAssessmentBps: 14 },
  { cardScheme: 'AMEX', cardCategory: 'CONSUMER_CREDIT', interchangeRatePercent: 2.30, perTransactionFeeCents: 10, schemeAssessmentBps: 16 }
];

export class InterchangePlusCalculator {
  public static calculateProcessingCosts(
    amountCents: number,
    cardScheme: 'VISA' | 'MASTERCARD' | 'AMEX' | 'DISCOVER',
    cardCategory: InterchangeRateFee['cardCategory'],
    acquirerMarkupBps: number = 20, // 0.20% processor markup
    acquirerPerTxnFeeCents: number = 10
  ): { totalFeeCents: number; interchangeCents: number; assessmentCents: number; acquirerMarkupCents: number } {
    const rate = INTERCHANGE_RATE_TABLE.find(r => r.cardScheme === cardScheme && r.cardCategory === cardCategory) || INTERCHANGE_RATE_TABLE[1];

    const interchangeCents = Math.round((amountCents * rate.interchangeRatePercent) / 100) + rate.perTransactionFeeCents;
    const assessmentCents = Math.round((amountCents * rate.schemeAssessmentBps) / 10000);
    const acquirerMarkupCents = Math.round((amountCents * acquirerMarkupBps) / 10000) + acquirerPerTxnFeeCents;

    const totalFee = interchangeCents + assessmentCents + acquirerMarkupCents;

    return {
      totalFeeCents: totalFee,
      interchangeCents,
      assessmentCents,
      acquirerMarkupCents
    };
  }
}
""")

    # 2. Inventory Automated Replenishment Reorder Point Solver
    write_file("services/inventory-service/src/domain/reorder-point-solver.ts", """export interface SkuVelocityProfile {
  sku: string;
  leadTimeDays: number;
  averageDailySales: number;
  maxDailySales: number;
  maxLeadTimeDays: number;
}

export class ReorderPointSolver {
  public static computeReorderPoint(profile: SkuVelocityProfile): { reorderPoint: number; safetyStock: number; leadTimeDemand: number } {
    const maxUsage = profile.maxDailySales * profile.maxLeadTimeDays;
    const avgUsage = profile.averageDailySales * profile.leadTimeDays;
    const safetyStock = Math.max(0, maxUsage - avgUsage);
    const leadTimeDemand = Math.round(avgUsage);
    const reorderPoint = leadTimeDemand + Math.round(safetyStock);

    return {
      reorderPoint,
      safetyStock: Math.round(safetyStock),
      leadTimeDemand
    };
  }
}
""")

    print("Complete infinity modules generated.")

if __name__ == "__main__":
    generate_complete_infinity_modules()
