import { RevenueRollupService } from '../src/services/revenue-rollup.service.js';

describe('Revenue Rollup Analytics Suite', () => {
  const service = new RevenueRollupService();

  it('should compute daily GMV and net revenue with refunds', () => {
    service.recordTransaction('2026-08-29', 10000);
    service.recordTransaction('2026-08-29', 15000);
    service.recordTransaction('2026-08-29', 5000, true); // refund

    const metrics = service.getMetricsForPeriod('2026-08-01', '2026-08-31');
    expect(metrics.length).toBe(1);
    expect(metrics[0].grossMerchandiseVolumeCents).toBe(25000);
    expect(metrics[0].refundedAmountCents).toBe(5000);
    expect(metrics[0].netRevenueCents).toBe(20000);
    expect(metrics[0].totalOrders).toBe(2);
    expect(metrics[0].averageOrderValueCents).toBe(12500);
  });
});
