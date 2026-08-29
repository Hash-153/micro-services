import { Level3ProcessingPayload } from './level3-card-data-builder.js';

export class Level3IntegrityValidator {
  public static validateTotals(payload: Level3ProcessingPayload, orderTotalCents: number): { isValid: boolean; calculatedSumCents: number; differenceCents: number } {
    const itemsSum = payload.lineItems.reduce((acc, it) => acc + it.totalAmountCents, 0);
    const calculatedSum = itemsSum + payload.freightAmountCents + payload.dutyAmountCents;
    const diff = calculatedSum - orderTotalCents;

    return {
      isValid: Math.abs(diff) === 0,
      calculatedSumCents: calculatedSum,
      differenceCents: diff
    };
  }
}
