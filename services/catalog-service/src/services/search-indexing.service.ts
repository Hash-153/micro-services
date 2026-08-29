import { ProductEntity } from '@novacommerce/core-types';

export interface SearchFilter {
  categoryId?: string;
  minPriceCents?: number;
  maxPriceCents?: number;
  tags?: string[];
  inStockOnly?: boolean;
}

export interface SearchResult {
  product: ProductEntity;
  score: number;
}

export class SearchIndexingService {
  private readonly documents: Map<string, ProductEntity> = new Map();
  private readonly invertedIndex: Map<string, Set<string>> = new Map();

  public indexProduct(product: ProductEntity): void {
    this.documents.set(product.id, product);

    const tokens = this.tokenize(`${product.name} ${product.description} ${product.sku} ${product.tags.join(' ')}`);
    for (const token of tokens) {
      if (!this.invertedIndex.has(token)) {
        this.invertedIndex.set(token, new Set());
      }
      this.invertedIndex.get(token)!.add(product.id);
    }
  }

  public search(query: string, filter?: SearchFilter, limit: number = 20): SearchResult[] {
    const queryTokens = this.tokenize(query);
    const scoreMap: Map<string, number> = new Map();

    for (const token of queryTokens) {
      const matchingDocIds = this.invertedIndex.get(token);
      if (matchingDocIds) {
        for (const docId of matchingDocIds) {
          const currentScore = scoreMap.get(docId) || 0;
          scoreMap.set(docId, currentScore + 1);
        }
      }
    }

    const results: SearchResult[] = [];
    for (const [docId, score] of scoreMap.entries()) {
      const product = this.documents.get(docId);
      if (!product || !product.isActive) continue;

      if (filter?.categoryId && product.categoryId !== filter.categoryId) continue;
      if (filter?.minPriceCents && product.basePrice.amount < filter.minPriceCents) continue;
      if (filter?.maxPriceCents && product.basePrice.amount > filter.maxPriceCents) continue;
      if (filter?.tags && !filter.tags.every(t => product.tags.includes(t))) continue;

      results.push({ product, score });
    }

    results.sort((a, b) => b.score - a.score);
    return results.slice(0, limit);
  }

  private tokenize(text: string): string[] {
    return text
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .split(/\s+/)
      .filter(t => t.length > 1);
  }
}
