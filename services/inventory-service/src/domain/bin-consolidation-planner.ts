export interface FragmentedBinStock {
  binId: string;
  sku: string;
  quantity: number;
  maxBinCapacity: number;
}

export class BinConsolidationPlanner {
  public static planConsolidation(bins: FragmentedBinStock[]): { sourceBinId: string; targetBinId: string; quantityToMove: number }[] {
    const moves: { sourceBinId: string; targetBinId: string; quantityToMove: number }[] = [];
    const groupedBySku = new Map<string, FragmentedBinStock[]>();

    for (const b of bins) {
      if (!groupedBySku.has(b.sku)) {
        groupedBySku.set(b.sku, []);
      }
      groupedBySku.get(b.sku)!.push({ ...b });
    }

    for (const [sku, skuBins] of groupedBySku.entries()) {
      if (skuBins.length <= 1) continue;

      // Sort bins ascending by current quantity (drain lowest bins first)
      skuBins.sort((a, b) => a.quantity - b.quantity);

      let targetIdx = skuBins.length - 1;
      let sourceIdx = 0;

      while (sourceIdx < targetIdx) {
        const source = skuBins[sourceIdx];
        const target = skuBins[targetIdx];

        const spaceInTarget = target.maxBinCapacity - target.quantity;
        if (spaceInTarget <= 0) {
          targetIdx--;
          continue;
        }

        const moveQty = Math.min(source.quantity, spaceInTarget);
        if (moveQty > 0) {
          moves.push({
            sourceBinId: source.binId,
            targetBinId: target.binId,
            quantityToMove: moveQty
          });
          source.quantity -= moveQty;
          target.quantity += moveQty;
        }

        if (source.quantity === 0) {
          sourceIdx++;
        }
        if (target.quantity >= target.maxBinCapacity) {
          targetIdx--;
        }
      }
    }

    return moves;
  }
}
