export interface DailyRevenueMetric {
  date: string;
  grossMerchandiseVolumeCents: number;
  totalOrders: number;
  averageOrderValueCents: number;
  refundedAmountCents: number;
  netRevenueCents: number;
}

export class RevenueRollupService {
  private readonly dailyMetrics: Map<string, DailyRevenueMetric> = new Map();

  public recordTransaction(dateStr: string, amountCents: number, isRefund: boolean = false): void {
    let metric = this.dailyMetrics.get(dateStr);
    if (!metric) {
      metric = {
        date: dateStr,
        grossMerchandiseVolumeCents: 0,
        totalOrders: 0,
        averageOrderValueCents: 0,
        refundedAmountCents: 0,
        netRevenueCents: 0
      };
    }

    if (isRefund) {
      metric.refundedAmountCents += amountCents;
    } else {
      metric.grossMerchandiseVolumeCents += amountCents;
      metric.totalOrders += 1;
    }

    metric.netRevenueCents = metric.grossMerchandiseVolumeCents - metric.refundedAmountCents;
    metric.averageOrderValueCents = metric.totalOrders > 0 ? Math.round(metric.grossMerchandiseVolumeCents / metric.totalOrders) : 0;

    this.dailyMetrics.set(dateStr, metric);
  }

  public getMetricsForPeriod(startDate: string, endDate: string): DailyRevenueMetric[] {
    return Array.from(this.dailyMetrics.values())
      .filter(m => m.date >= startDate && m.date <= endDate)
      .sort((a, b) => a.date.localeCompare(b.date));
  }
}
