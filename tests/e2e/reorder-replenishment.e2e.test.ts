import { ReorderCalculator } from '../../services/inventory-service/src/domain/reorder-calculator.js';

describe('E2E Scenario: Automated Warehouse Inventory Reorder & EOQ Calculation', () => {
  it('should generate emergency purchase order when stock reaches zero', () => {
    const advice = ReorderCalculator.calculateReorderParameters(
      {
        sku: 'SKU-CRITICAL-PART',
        averageDailySales: 25,
        leadTimeDays: 14,
        supplierReliabilityPercent: 90,
        serviceLevelZScore: 2.33, // 99% SLA
        demandStandardDeviation: 4.5
      },
      0, // 0 on hand
      0  // 0 reserved
    );

    expect(advice.suggestedAction).toBe('ORDER_NOW');
    expect(advice.safetyStockUnits).toBeGreaterThan(20);
    expect(advice.economicOrderQuantity).toBeGreaterThan(100);
  });
});
