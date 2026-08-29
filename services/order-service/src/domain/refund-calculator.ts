import { OrderEntity, OrderItemEntity, Money, Currency } from '@novacommerce/core-types';

export interface RefundBreakdown {
  orderId: string;
  itemsRefundCents: number;
  taxRefundCents: number;
  shippingRefundCents: number;
  restockingFeeCents: number;
  totalRefundCents: number;
  currency: Currency;
}

export class RefundCalculator {
  public static computeRefund(
    order: OrderEntity,
    refundItems: { sku: string; quantity: number; conditionFeePercent?: number }[],
    refundShipping: boolean = false
  ): RefundBreakdown {
    let itemsRefundCents = 0;
    let restockingFeeCents = 0;

    for (const refItem of refundItems) {
      const orderItem = order.items.find(i => i.sku === refItem.sku);
      if (!orderItem) {
        throw new Error(`Item with SKU ${refItem.sku} was not found in order ${order.orderNumber}`);
      }

      if (refItem.quantity > orderItem.quantity) {
        throw new Error(`Cannot refund ${refItem.quantity} units of SKU ${refItem.sku} (purchased: ${orderItem.quantity})`);
      }

      const itemTotal = orderItem.unitPrice.amount * refItem.quantity;
      itemsRefundCents += itemTotal;

      if (refItem.conditionFeePercent && refItem.conditionFeePercent > 0) {
        restockingFeeCents += Math.round((itemTotal * refItem.conditionFeePercent) / 100);
      }
    }

    // Proportional sales tax refund calculation
    const taxRate = order.subtotalAmount.amount > 0 ? order.taxAmount.amount / order.subtotalAmount.amount : 0;
    const taxRefundCents = Math.round(itemsRefundCents * taxRate);

    const shippingRefundCents = refundShipping ? order.shippingFeeAmount.amount : 0;
    const totalRefundCents = Math.max(0, itemsRefundCents + taxRefundCents + shippingRefundCents - restockingFeeCents);

    return {
      orderId: order.id,
      itemsRefundCents,
      taxRefundCents,
      shippingRefundCents,
      restockingFeeCents,
      totalRefundCents,
      currency: order.totalAmount.currency
    };
  }
}
