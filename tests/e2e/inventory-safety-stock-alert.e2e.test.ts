import { ReorderCalculator } from '../../services/inventory-service/src/domain/reorder-calculator.js';

describe('E2E Scenario: Automated Safety Stock Alert & Inventory Replenishment Calculation', () => {
  it('should trigger emergency stockout warning when stock is below safety threshold', () => {
    const advice = ReorderCalculator.calculateReorderParameters(
      {
        sku: 'SKU-LOW-STOCK-ALERT',
        averageDailySales: 15,
        leadTimeDays: 5,
        supplierReliabilityPercent: 95,
        serviceLevelZScore: 1.65,
        demandStandardDeviation: 3.0
      },
      8, // 8 on hand
      2  // 2 reserved -> 6 available < 12 safety stock
    );

    expect(advice.suggestedAction).toBe('ORDER_NOW');
    expect(advice.safetyStockUnits).toBeGreaterThan(0);
    expect(advice.reorderPointUnits).toBeGreaterThan(75);
  });
});
