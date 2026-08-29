import { BinPackingOptimizer, ItemDimension, STANDARD_SHIPPING_BOXES } from '../src/domain/bin-packing-optimizer.js';

describe('Fulfillment Service: 3D Bin Packing Box Optimization Suite', () => {
  it('should select Small Parcel Box for compact items', () => {
    const items: ItemDimension[] = [
      { id: 'item-1', lengthMm: 120, widthMm: 80, heightMm: 40, weightGrams: 300, quantity: 1 }
    ];

    const result = BinPackingOptimizer.findOptimalBox(items);
    expect(result.selectedBox.boxId).toBe('BOX-SMALL');
    expect(result.utilizationPercentage).toBeGreaterThan(0);
  });

  it('should select Extra Large Box for bulky items', () => {
    const items: ItemDimension[] = [
      { id: 'item-bulky', lengthMm: 450, widthMm: 350, heightMm: 250, weightGrams: 5000, quantity: 1 }
    ];

    const result = BinPackingOptimizer.findOptimalBox(items);
    expect(result.selectedBox.boxId).toBe('BOX-XLARGE');
  });
});
