import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_expansion_part1():
    print("Generating Production Expansion Part 1...")

    # -------------------------------------------------------------
    # 1. ORDER DOMAIN EXPANSIONS
    # -------------------------------------------------------------
    write_file("services/order-service/src/domain/order-validator.ts", """import { OrderEntity, OrderItemEntity, AddressEntity } from '@novacommerce/core-types';

export interface ValidationIssue {
  field: string;
  code: string;
  message: string;
}

export class OrderValidator {
  public static validate(order: Partial<OrderEntity>): { isValid: boolean; issues: ValidationIssue[] } {
    const issues: ValidationIssue[] = [];

    if (!order.userId || order.userId.trim().length === 0) {
      issues.push({ field: 'userId', code: 'REQUIRED', message: 'User ID is mandatory for order placement.' });
    }

    if (!order.items || order.items.length === 0) {
      issues.push({ field: 'items', code: 'EMPTY_CART', message: 'Order must contain at least one line item.' });
    } else {
      order.items.forEach((item, idx) => {
        if (!item.sku || item.sku.trim().length === 0) {
          issues.push({ field: `items[${idx}].sku`, code: 'INVALID_SKU', message: 'Item SKU cannot be empty.' });
        }
        if (item.quantity <= 0) {
          issues.push({ field: `items[${idx}].quantity`, code: 'INVALID_QTY', message: 'Quantity must be at least 1 unit.' });
        }
        if (item.unitPrice.amount < 0) {
          issues.push({ field: `items[${idx}].unitPrice`, code: 'INVALID_PRICE', message: 'Unit price cannot be negative.' });
        }
      });
    }

    if (!order.shippingAddress) {
      issues.push({ field: 'shippingAddress', code: 'REQUIRED', message: 'Shipping address is required.' });
    } else {
      this.validateAddress(order.shippingAddress, 'shippingAddress', issues);
    }

    if (!order.billingAddress) {
      issues.push({ field: 'billingAddress', code: 'REQUIRED', message: 'Billing address is required.' });
    } else {
      this.validateAddress(order.billingAddress, 'billingAddress', issues);
    }

    if (order.totalAmount && order.totalAmount.amount < 0) {
      issues.push({ field: 'totalAmount', code: 'INVALID_TOTAL', message: 'Total order amount cannot be negative.' });
    }

    return {
      isValid: issues.length === 0,
      issues
    };
  }

  private static validateAddress(address: AddressEntity, prefix: string, issues: ValidationIssue[]): void {
    if (!address.recipientName || address.recipientName.trim().length === 0) {
      issues.push({ field: `${prefix}.recipientName`, code: 'REQUIRED', message: 'Recipient name is required.' });
    }
    if (!address.streetLine1 || address.streetLine1.trim().length === 0) {
      issues.push({ field: `${prefix}.streetLine1`, code: 'REQUIRED', message: 'Street address line 1 is required.' });
    }
    if (!address.city || address.city.trim().length === 0) {
      issues.push({ field: `${prefix}.city`, code: 'REQUIRED', message: 'City is required.' });
    }
    if (!address.stateOrProvince || address.stateOrProvince.trim().length === 0) {
      issues.push({ field: `${prefix}.stateOrProvince`, code: 'REQUIRED', message: 'State or province is required.' });
    }
    if (!address.postalCode || address.postalCode.trim().length === 0) {
      issues.push({ field: `${prefix}.postalCode`, code: 'REQUIRED', message: 'Postal code is required.' });
    }
    if (!address.countryCode || address.countryCode.length !== 2) {
      issues.push({ field: `${prefix}.countryCode`, code: 'INVALID_FORMAT', message: 'Country code must be 2-letter ISO code.' });
    }
  }
}
""")

    write_file("services/order-service/src/domain/tax-nexus-rules.ts", """export interface TaxNexusRule {
  stateCode: string;
  stateName: string;
  hasEconomicNexus: boolean;
  annualSalesThresholdCents: number;
  annualTransactionThreshold: number;
  collectsFreightTax: boolean;
  standardVatPercent?: number;
}

export class TaxNexusEngine {
  private static readonly NEXUS_RULES: Record<string, TaxNexusRule> = {
    CA: { stateCode: 'CA', stateName: 'California', hasEconomicNexus: true, annualSalesThresholdCents: 50000000, annualTransactionThreshold: 200, collectsFreightTax: false },
    NY: { stateCode: 'NY', stateName: 'New York', hasEconomicNexus: true, annualSalesThresholdCents: 50000000, annualTransactionThreshold: 100, collectsFreightTax: true },
    TX: { stateCode: 'TX', stateName: 'Texas', hasEconomicNexus: true, annualSalesThresholdCents: 50000000, annualTransactionThreshold: 0, collectsFreightTax: true },
    FL: { stateCode: 'FL', stateName: 'Florida', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 0, collectsFreightTax: false },
    IL: { stateCode: 'IL', stateName: 'Illinois', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    PA: { stateCode: 'PA', stateName: 'Pennsylvania', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 0, collectsFreightTax: false },
    OH: { stateCode: 'OH', stateName: 'Ohio', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    GA: { stateCode: 'GA', stateName: 'Georgia', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    NC: { stateCode: 'NC', stateName: 'North Carolina', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    MI: { stateCode: 'MI', stateName: 'Michigan', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    NJ: { stateCode: 'NJ', stateName: 'New Jersey', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: true },
    VA: { stateCode: 'VA', stateName: 'Virginia', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 200, collectsFreightTax: false },
    WA: { stateCode: 'WA', stateName: 'Washington', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 0, collectsFreightTax: true },
    AZ: { stateCode: 'AZ', stateName: 'Arizona', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 0, collectsFreightTax: false },
    MA: { stateCode: 'MA', stateName: 'Massachusetts', hasEconomicNexus: true, annualSalesThresholdCents: 10000000, annualTransactionThreshold: 0, collectsFreightTax: false }
  };

  public static hasNexus(stateCode: string, currentAnnualSalesCents: number, currentAnnualTransactions: number): boolean {
    const rule = this.NEXUS_RULES[stateCode.toUpperCase()];
    if (!rule || !rule.hasEconomicNexus) return false;
    return (
      currentAnnualSalesCents >= rule.annualSalesThresholdCents ||
      (rule.annualTransactionThreshold > 0 && currentAnnualTransactions >= rule.annualTransactionThreshold)
    );
  }

  public static isFreightTaxable(stateCode: string): boolean {
    const rule = this.NEXUS_RULES[stateCode.toUpperCase()];
    return rule ? rule.collectsFreightTax : false;
  }
}
""")

    write_file("services/order-service/src/domain/rma-inspection-rules.ts", """export type ItemReturnCondition = 'UNOPENED' | 'OPENED_UNUSED' | 'LIGHTLY_USED' | 'DAMAGED_BY_CUSTOMER' | 'DEFECTIVE_ON_ARRIVAL';

export interface RmaInspectionAssessment {
  condition: ItemReturnCondition;
  isEligibleForRefund: boolean;
  restockingFeePercent: number;
  restockingFeeCents: number;
  netRefundCents: number;
  disposition: 'RETURN_TO_INVENTORY' | 'REFURBISH' | 'LIQUIDATE' | 'SCRAP';
  reason: string;
}

export class RmaInspectionEngine {
  public static assessReturnItem(unitPriceCents: number, condition: ItemReturnCondition): RmaInspectionAssessment {
    switch (condition) {
      case 'UNOPENED':
        return {
          condition,
          isEligibleForRefund: true,
          restockingFeePercent: 0,
          restockingFeeCents: 0,
          netRefundCents: unitPriceCents,
          disposition: 'RETURN_TO_INVENTORY',
          reason: 'Item in original factory sealed condition. Full refund.'
        };
      case 'OPENED_UNUSED':
        return {
          condition,
          isEligibleForRefund: true,
          restockingFeePercent: 10,
          restockingFeeCents: Math.round(unitPriceCents * 0.10),
          netRefundCents: Math.round(unitPriceCents * 0.90),
          disposition: 'RETURN_TO_INVENTORY',
          reason: 'Packaging opened but item unused. 10% repackaging fee applies.'
        };
      case 'LIGHTLY_USED':
        return {
          condition,
          isEligibleForRefund: true,
          restockingFeePercent: 20,
          restockingFeeCents: Math.round(unitPriceCents * 0.20),
          netRefundCents: Math.round(unitPriceCents * 0.80),
          disposition: 'REFURBISH',
          reason: 'Item lightly used with all accessories. 20% restocking fee applies.'
        };
      case 'DEFECTIVE_ON_ARRIVAL':
        return {
          condition,
          isEligibleForRefund: true,
          restockingFeePercent: 0,
          restockingFeeCents: 0,
          netRefundCents: unitPriceCents,
          disposition: 'SCRAP',
          reason: 'Factory defect verified. 100% full refund with zero restocking fee.'
        };
      case 'DAMAGED_BY_CUSTOMER':
        return {
          condition,
          isEligibleForRefund: false,
          restockingFeePercent: 100,
          restockingFeeCents: unitPriceCents,
          netRefundCents: 0,
          disposition: 'SCRAP',
          reason: 'Item damaged by customer misuse. Ineligible for return refund.'
        };
    }
  }
}
""")

    print("Order expansions complete.")

if __name__ == "__main__":
    generate_prod_expansion_part1()
