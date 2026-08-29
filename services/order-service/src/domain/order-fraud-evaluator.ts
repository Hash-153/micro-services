import { OrderEntity } from '@novacommerce/core-types';

export class OrderFraudEvaluator {
  public static evaluateRisk(order: OrderEntity): { riskScore: number; isFlagged: boolean; reasons: string[] } {
    const reasons: string[] = [];
    let score = 0;

    // High order value
    if (order.totalAmount.amount >= 200000) {
      score += 30;
      reasons.push('High value order (>$2,000)');
    }

    // Multiple high-quantity items
    const highQtyItems = order.items.filter(i => i.quantity > 5);
    if (highQtyItems.length > 0) {
      score += 20;
      reasons.push('Bulk unit quantities requested');
    }

    // Shipping and Billing country mismatch
    if (order.shippingAddress.countryCode !== order.billingAddress.countryCode) {
      score += 25;
      reasons.push('Cross-border shipping/billing country mismatch');
    }

    return {
      riskScore: score,
      isFlagged: score >= 50,
      reasons
    };
  }
}
