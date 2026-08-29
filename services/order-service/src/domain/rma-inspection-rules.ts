export type ItemReturnCondition = 'UNOPENED' | 'OPENED_UNUSED' | 'LIGHTLY_USED' | 'DAMAGED_BY_CUSTOMER' | 'DEFECTIVE_ON_ARRIVAL';

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
