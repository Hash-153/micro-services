import { OrderEntity } from '@novacommerce/core-types';

export interface EnterpriseKpiSummary {
  periodDate: string;
  grossMerchandiseValueCents: number;
  netRevenueCents: number;
  totalOrdersCount: number;
  averageOrderValueCents: number;
  unitsPerOrder: number;
  totalDiscountAmountCents: number;
  totalRefundAmountCents: number;
  refundRatePercent: number;
}

export class StandardKpiAggregator {
  public static aggregateDailyKpis(orders: OrderEntity[], periodDate: string = new Date().toISOString().slice(0, 10)): EnterpriseKpiSummary {
    const validOrders = orders.filter(o => o.status !== 'CANCELLED');
    const refundedOrders = orders.filter(o => o.status === 'REFUNDED' || o.status === 'PARTIALLY_REFUNDED');

    const gmv = orders.reduce((acc, o) => acc + o.totalAmount.amount, 0);
    const discounts = orders.reduce((acc, o) => acc + o.discountAmount.amount, 0);
    const refunds = refundedOrders.reduce((acc, o) => acc + o.totalAmount.amount, 0);
    const netRevenue = Math.max(0, gmv - discounts - refunds);

    const totalUnits = validOrders.reduce((acc, o) => acc + o.items.reduce((sum, it) => sum + it.quantity, 0), 0);
    const aov = validOrders.length > 0 ? Math.round(gmv / validOrders.length) : 0;
    const unitsPerOrder = validOrders.length > 0 ? Math.round((totalUnits / validOrders.length) * 10) / 10 : 0;
    const refundRate = gmv > 0 ? (refunds / gmv) * 100 : 0;

    return {
      periodDate,
      grossMerchandiseValueCents: gmv,
      netRevenueCents: netRevenue,
      totalOrdersCount: validOrders.length,
      averageOrderValueCents: aov,
      unitsPerOrder,
      totalDiscountAmountCents: discounts,
      totalRefundAmountCents: refunds,
      refundRatePercent: Math.round(refundRate * 10) / 10
    };
  }
}
