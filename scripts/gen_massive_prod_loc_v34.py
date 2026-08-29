import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v34():
    print("Generating comprehensive Production V34 Modules...")

    # 1. Payment Level 3 Commercial Card Processing Data Builder
    write_file("services/payment-service/src/domain/level3-card-data-builder.ts", """import { OrderEntity } from '@novacommerce/core-types';

export interface Level3LineItemData {
  itemCommodityCode: string;
  itemDescription: string;
  productCode: string;
  quantity: number;
  unitOfMeasure: string;
  unitCostCents: number;
  totalAmountCents: number;
  taxAmountCents: number;
  discountAmountCents: number;
}

export interface Level3ProcessingPayload {
  summaryCommodityCode: string;
  customerVatRegistrationNumber?: string;
  dutyAmountCents: number;
  freightAmountCents: number;
  shipFromPostalCode: string;
  destinationPostalCode: string;
  destinationCountryCode: string;
  lineItems: Level3LineItemData[];
}

export class Level3CardDataBuilder {
  public static buildLevel3Data(order: OrderEntity, shipFromPostal: string = '94105'): Level3ProcessingPayload {
    const lineItems: Level3LineItemData[] = order.items.map(it => ({
      itemCommodityCode: '43211507', // Electronic hardware commodity code
      itemDescription: it.productName.slice(0, 26),
      productCode: it.sku.slice(0, 12),
      quantity: it.quantity,
      unitOfMeasure: 'EA',
      unitCostCents: it.unitPrice.amount,
      totalAmountCents: it.unitPrice.amount * it.quantity,
      taxAmountCents: 0,
      discountAmountCents: 0
    }));

    return {
      summaryCommodityCode: '43211500',
      dutyAmountCents: 0,
      freightAmountCents: order.shippingFeeAmount.amount,
      shipFromPostalCode: shipFromPostal,
      destinationPostalCode: order.shippingAddress.postalCode,
      destinationCountryCode: order.shippingAddress.countryCode,
      lineItems
    };
  }
}
""")

    # 2. Inventory Pallet Stacking Height & Weight Validator
    write_file("services/inventory-service/src/domain/pallet-stacking-validator.ts", """export interface PalletTierConfig {
  maxTiers: number;
  maxTotalHeightMm: number;
  maxTotalWeightGrams: number;
  palletTareWeightGrams: number;
}

export class PalletStackingValidator {
  private static readonly STANDARD_PALLET: PalletTierConfig = {
    maxTiers: 6,
    maxTotalHeightMm: 1800, // 1.8m standard rack height
    maxTotalWeightGrams: 1000000, // 1,000 kg / 1 metric ton
    palletTareWeightGrams: 25000 // 25kg wooden GMA pallet
  };

  public static validatePallet(
    boxHeightMm: number,
    boxWeightGrams: number,
    boxesPerTier: number,
    tierCount: number
  ): { isSafe: boolean; totalHeightMm: number; totalGrossWeightGrams: number; violationReason?: string } {
    const totalHeight = boxHeightMm * tierCount + 150; // +150mm pallet base
    const totalGrossWeight = boxWeightGrams * boxesPerTier * tierCount + this.STANDARD_PALLET.palletTareWeightGrams;

    if (tierCount > this.STANDARD_PALLET.maxTiers) {
      return {
        isSafe: false,
        totalHeightMm: totalHeight,
        totalGrossWeightGrams: totalGrossWeight,
        violationReason: `Tier count (${tierCount}) exceeds max safe limit (${this.STANDARD_PALLET.maxTiers})`
      };
    }

    if (totalHeight > this.STANDARD_PALLET.maxTotalHeightMm) {
      return {
        isSafe: false,
        totalHeightMm: totalHeight,
        totalGrossWeightGrams: totalGrossWeight,
        violationReason: `Total pallet height (${totalHeight}mm) exceeds max rack clearance (${this.STANDARD_PALLET.maxTotalHeightMm}mm)`
      };
    }

    if (totalGrossWeight > this.STANDARD_PALLET.maxTotalWeightGrams) {
      return {
        isSafe: false,
        totalHeightMm: totalHeight,
        totalGrossWeightGrams: totalGrossWeight,
        violationReason: `Total pallet gross weight (${(totalGrossWeight / 1000).toFixed(1)}kg) exceeds rating (${(this.STANDARD_PALLET.maxTotalWeightGrams / 1000).toFixed(1)}kg)`
      };
    }

    return {
      isSafe: true,
      totalHeightMm: totalHeight,
      totalGrossWeightGrams: totalGrossWeight
    };
  }
}
""")

    print("Production V34 modules generated.")

if __name__ == "__main__":
    generate_prod_v34()
