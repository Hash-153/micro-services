import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v13():
    print("Generating comprehensive Production V13 Modules...")

    # 1. Payment Dispute & Chargeback Defense Manager
    write_file("services/payment-service/src/domain/dispute-manager.ts", """import { PaymentTransactionEntity, Currency } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export interface DisputeRecord {
  disputeId: string;
  transactionReference: string;
  amountCents: number;
  currency: Currency;
  reasonCode: string;
  evidenceDueBy: Date;
  status: 'NEEDS_RESPONSE' | 'UNDER_REVIEW' | 'WON' | 'LOST';
  submittedEvidenceUrls: string[];
  createdAt: Date;
}

export class DisputeManager {
  private logger: Logger;
  private disputes: Map<string, DisputeRecord> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public registerDispute(
    transactionRef: string,
    amountCents: number,
    currency: Currency,
    reasonCode: string,
    evidenceDueDays: number = 7
  ): DisputeRecord {
    const disputeId = `dp_${Date.now().toString(36)}`;
    const evidenceDueBy = new Date(Date.now() + evidenceDueDays * 86400000);

    const dispute: DisputeRecord = {
      disputeId,
      transactionReference: transactionRef,
      amountCents,
      currency,
      reasonCode,
      evidenceDueBy,
      status: 'NEEDS_RESPONSE',
      submittedEvidenceUrls: [],
      createdAt: new Date()
    };

    this.disputes.set(disputeId, dispute);
    this.logger.warn(`Payment dispute received: ${disputeId} for txn ${transactionRef} ($${(amountCents / 100).toFixed(2)})`);
    return dispute;
  }

  public submitEvidence(disputeId: string, evidenceUrls: string[]): DisputeRecord {
    const dispute = this.disputes.get(disputeId);
    if (!dispute) throw new Error(`Dispute ${disputeId} not found`);

    dispute.submittedEvidenceUrls.push(...evidenceUrls);
    dispute.status = 'UNDER_REVIEW';

    this.logger.info(`Evidence submitted for dispute ${disputeId} (${evidenceUrls.length} documents)`);
    return dispute;
  }
}
""")

    # 2. Inventory Dead Stock & Liquidation Analyzer
    write_file("services/inventory-service/src/domain/dead-stock-analyzer.ts", """import { InventoryStockEntity } from '@novacommerce/core-types';

export interface DeadStockAssessment {
  sku: string;
  warehouseId: string;
  onHandQuantity: number;
  daysSinceLastSold: number;
  isDeadStock: boolean;
  recommendedAction: 'HOLD' | 'PROMOTIONAL_DISCOUNT' | 'BUNDLE_CLEARANCE' | 'LIQUIDATE_VENDOR';
  discountSuggestedPercentage: number;
}

export class DeadStockAnalyzer {
  public static evaluateStockVelocity(
    stock: InventoryStockEntity,
    daysSinceLastSold: number,
    deadStockThresholdDays: number = 90
  ): DeadStockAssessment {
    const isDead = daysSinceLastSold >= deadStockThresholdDays && stock.onHandQuantity > 0;

    let action: DeadStockAssessment['recommendedAction'] = 'HOLD';
    let discountPct = 0;

    if (daysSinceLastSold >= 180) {
      action = 'LIQUIDATE_VENDOR';
      discountPct = 60;
    } else if (daysSinceLastSold >= 120) {
      action = 'BUNDLE_CLEARANCE';
      discountPct = 40;
    } else if (daysSinceLastSold >= 90) {
      action = 'PROMOTIONAL_DISCOUNT';
      discountPct = 20;
    }

    return {
      sku: stock.sku,
      warehouseId: stock.warehouseId,
      onHandQuantity: stock.onHandQuantity,
      daysSinceLastSold,
      isDeadStock: isDead,
      recommendedAction: action,
      discountSuggestedPercentage: discountPct
    };
  }
}
""")

    print("Production V13 modules generated.")

if __name__ == "__main__":
    generate_prod_v13()
