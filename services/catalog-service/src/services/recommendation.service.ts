import { ProductEntity } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class RecommendationService {
  private logger: Logger;
  private coOccurrenceMatrix: Map<string, Map<string, number>> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public recordOrderCoOccurrence(skus: string[]): void {
    for (let i = 0; i < skus.length; i++) {
      for (let j = 0; j < skus.length; j++) {
        if (i !== j) {
          const skuA = skus[i];
          const skuB = skus[j];
          if (!this.coOccurrenceMatrix.has(skuA)) {
            this.coOccurrenceMatrix.set(skuA, new Map());
          }
          const row = this.coOccurrenceMatrix.get(skuA)!;
          row.set(skuB, (row.get(skuB) || 0) + 1);
        }
      }
    }
  }

  public getFrequentlyBoughtTogether(sku: string, limit: number = 4): string[] {
    const row = this.coOccurrenceMatrix.get(sku);
    if (!row) return [];

    return Array.from(row.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, limit)
      .map(entry => entry[0]);
  }
}
