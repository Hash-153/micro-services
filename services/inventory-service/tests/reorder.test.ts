import { ReorderCalculator } from '../src/domain/reorder-calculator.js';

describe('Inventory Safety Stock & Reorder Formula Suite', () => {
  it('should recommend ordering when stock is at or below reorder point', () => {
    const advice = ReorderCalculator.calculateReorderParameters(
      {
        sku: 'SKU-001',
        averageDailySales: 10,
        leadTimeDays: 7,
        supplierReliabilityPercent: 95,
        serviceLevelZScore: 1.65,
        demandStandardDeviation: 2.5
      },
      75, // on hand
      10  // reserved -> 65 available <= reorder point (70 + safety)
    );

    expect(advice.safetyStockUnits).toBeGreaterThan(0);
    expect(advice.reorderPointUnits).toBeGreaterThan(70);
    expect(advice.economicOrderQuantity).toBeGreaterThan(0);
    expect(advice.suggestedAction).toBe('ORDER_NOW');
  });
});
