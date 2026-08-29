import { PaymentTransactionEntity, OrderEntity, UserProfileEntity } from '@novacommerce/core-types';

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
