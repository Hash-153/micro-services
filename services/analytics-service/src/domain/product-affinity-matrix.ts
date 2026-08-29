export interface ProductAffinityPair {
  skuA: string;
  skuB: string;
  support: number;
  confidence: number;
  lift: number;
}

export class ProductAffinityMatrix {
  public static computeAffinities(
    transactions: string[][],
    minSupport: number = 0.01,
    minConfidence: number = 0.1
  ): ProductAffinityPair[] {
    const totalTransactions = transactions.length;
    if (totalTransactions === 0) return [];

    const itemCounts: Map<string, number> = new Map();
    const pairCounts: Map<string, number> = new Map();

    for (const txn of transactions) {
      const uniqueItems = Array.from(new Set(txn));
      for (let i = 0; i < uniqueItems.length; i++) {
        const itemA = uniqueItems[i];
        itemCounts.set(itemA, (itemCounts.get(itemA) || 0) + 1);

        for (let j = i + 1; j < uniqueItems.length; j++) {
          const itemB = uniqueItems[j];
          const key = itemA < itemB ? `${itemA}::${itemB}` : `${itemB}::${itemA}`;
          pairCounts.set(key, (pairCounts.get(key) || 0) + 1);
        }
      }
    }

    const pairs: ProductAffinityPair[] = [];

    for (const [pairKey, count] of pairCounts.entries()) {
      const [skuA, skuB] = pairKey.split('::');
      const support = count / totalTransactions;

      if (support >= minSupport) {
        const countA = itemCounts.get(skuA) || 0;
        const countB = itemCounts.get(skuB) || 0;

        const confAtoB = count / countA;
        const lift = confAtoB / (countB / totalTransactions);

        if (confAtoB >= minConfidence) {
          pairs.push({
            skuA,
            skuB,
            support: Math.round(support * 1000) / 1000,
            confidence: Math.round(confAtoB * 1000) / 1000,
            lift: Math.round(lift * 100) / 100
          });
        }
      }
    }

    return pairs.sort((a, b) => b.lift - a.lift);
  }
}
