import { Money, Currency } from '@novacommerce/core-types';

export interface EscrowHoldRecord {
  escrowId: string;
  orderId: string;
  sellerId: string;
  buyerId: string;
  holdAmountCents: number;
  currency: Currency;
  status: 'HELD' | 'RELEASED_TO_SELLER' | 'REFUNDED_TO_BUYER' | 'SPLIT_DISPUTE';
  autoReleaseDate: Date;
  deliveryConfirmedDate?: Date;
}

export class EscrowReleaseEngine {
  public static canReleaseToSeller(escrow: EscrowHoldRecord, currentDate: Date = new Date()): boolean {
    if (escrow.status !== 'HELD') return false;

    // Release if delivery confirmed + 48 hours cooling off
    if (escrow.deliveryConfirmedDate) {
      const coolingOffEnd = new Date(escrow.deliveryConfirmedDate.getTime() + 48 * 3600000);
      if (currentDate >= coolingOffEnd) return true;
    }

    // Release if autoReleaseDate reached without active dispute
    return currentDate >= escrow.autoReleaseDate;
  }
}
