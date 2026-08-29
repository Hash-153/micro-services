import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_titan():
    print("Generating comprehensive Production Titan Modules...")

    # 1. Payment Fraud Machine Learning Feature Extractor
    write_file("services/payment-service/src/domain/fraud-feature-extractor.ts", """import { PaymentTransactionEntity, OrderEntity, UserProfileEntity } from '@novacommerce/core-types';

export interface ExtractedFraudFeatures {
  transactionAmountCents: number;
  isHighValueTransaction: boolean;
  cardBrand: string;
  isInternationalCard: boolean;
  daysSinceAccountCreated: number;
  orderItemCount: number;
  distinctCategoriesCount: number;
  isShippingBillingStateMismatch: boolean;
  billingPostalCodeNumeric: number;
}

export class FraudFeatureExtractor {
  public static extract(
    transaction: PaymentTransactionEntity,
    order: OrderEntity,
    userProfile?: UserProfileEntity
  ): ExtractedFraudFeatures {
    const isHighValue = transaction.amount.amount >= 100000; // $1,000+
    const shipState = order.shippingAddress.stateOrProvince.toUpperCase();
    const billState = order.billingAddress.stateOrProvince.toUpperCase();
    const isMismatch = shipState !== billState;

    const distinctCats = new Set(order.items.map(i => i.sku.split('-')[0])).size;
    const accountCreated = userProfile?.createdAt ? new Date(userProfile.createdAt) : new Date();
    const daysSinceCreated = Math.max(0, Math.floor((Date.now() - accountCreated.getTime()) / (1000 * 60 * 60 * 24)));

    const postalClean = parseInt(order.billingAddress.postalCode.replace(/[^0-9]/g, ''), 10) || 0;

    return {
      transactionAmountCents: transaction.amount.amount,
      isHighValueTransaction: isHighValue,
      cardBrand: transaction.methodType,
      isInternationalCard: order.billingAddress.countryCode !== 'US',
      daysSinceAccountCreated: daysSinceCreated,
      orderItemCount: order.items.reduce((acc, it) => acc + it.quantity, 0),
      distinctCategoriesCount: distinctCats,
      isShippingBillingStateMismatch: isMismatch,
      billingPostalCodeNumeric: postalClean
    };
  }
}
""")

    # 2. Inventory Shrinkage & Cycle Count Manager
    write_file("services/inventory-service/src/domain/cycle-count-manager.ts", """import { InventoryStockEntity } from '@novacommerce/core-types';

export interface CycleCountRecord {
  countId: string;
  warehouseId: string;
  sku: string;
  systemOnHandQuantity: number;
  physicalCountQuantity: number;
  discrepancyQuantity: number;
  discrepancyPercentage: number;
  unitCostCents: number;
  totalShrinkageCostCents: number;
  status: 'PENDING_APPROVAL' | 'APPROVED' | 'RECOUNT_REQUESTED';
  countedAt: Date;
}

export class CycleCountManager {
  public static processCount(
    stock: InventoryStockEntity,
    physicalCount: number,
    unitCostCents: number = 1500
  ): CycleCountRecord {
    const discrepancy = physicalCount - stock.onHandQuantity;
    const discrepancyPercent = stock.onHandQuantity > 0 ? (discrepancy / stock.onHandQuantity) * 100 : 0;
    const shrinkageCost = Math.abs(discrepancy) * unitCostCents;

    const needsRecount = Math.abs(discrepancyPercent) > 5.0 || shrinkageCost > 100000; // >5% or >$1000 discrepancy

    return {
      countId: `cnt_${Date.now().toString(36)}`,
      warehouseId: stock.warehouseId,
      sku: stock.sku,
      systemOnHandQuantity: stock.onHandQuantity,
      physicalCountQuantity: physicalCount,
      discrepancyQuantity: discrepancy,
      discrepancyPercentage: Math.round(discrepancyPercent * 100) / 100,
      unitCostCents,
      totalShrinkageCostCents: shrinkageCost,
      status: needsRecount ? 'RECOUNT_REQUESTED' : 'PENDING_APPROVAL',
      countedAt: new Date()
    };
  }
}
""")

    print("Production titan modules generated.")

if __name__ == "__main__":
    generate_prod_titan()
