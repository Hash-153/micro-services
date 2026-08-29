import { ProductEntity } from '@novacommerce/core-types';

export interface DocumentPosting {
  documentId: string;
  termFrequency: number;
  field: 'name' | 'description' | 'tags' | 'sku';
}

export class SearchBm25Indexer {
  private documents: Map<string, ProductEntity> = new Map();
  private invertedIndex: Map<string, DocumentPosting[]> = new Map();
  private docLengths: Map<string, number> = new Map();
  private avgDocLength: number = 0;
  private readonly k1: number = 1.2;
  private readonly b: number = 0.75;

  public indexProduct(product: ProductEntity): void {
    this.documents.set(product.id, product);
    const tokens = this.tokenize(`${product.name} ${product.description} ${product.tags.join(' ')} ${product.sku}`);
    this.docLengths.set(product.id, tokens.length);
    this.updateAvgDocLength();

    // Term frequencies
    const tfMap: Map<string, number> = new Map();
    tokens.forEach(t => tfMap.set(t, (tfMap.get(t) || 0) + 1));

    for (const [term, freq] of tfMap.entries()) {
      if (!this.invertedIndex.has(term)) {
        this.invertedIndex.set(term, []);
      }
      const postings = this.invertedIndex.get(term)!;
      const existing = postings.find(p => p.documentId === product.id);
      if (existing) {
        existing.termFrequency = freq;
      } else {
        postings.push({ documentId: product.id, termFrequency: freq, field: 'name' });
      }
    }
  }

  public search(query: string, limit: number = 20): { product: ProductEntity; score: number }[] {
    const queryTokens = this.tokenize(query);
    const scores: Map<string, number> = new Map();
    const totalDocs = this.documents.size;

    for (const term of queryTokens) {
      const postings = this.invertedIndex.get(term) || [];
      const df = postings.length;
      if (df === 0) continue;

      // IDF calculation (BM25 formula)
      const idf = Math.log((totalDocs - df + 0.5) / (df + 0.5) + 1);

      for (const posting of postings) {
        const docLen = this.docLengths.get(posting.documentId) || this.avgDocLength;
        const tf = posting.termFrequency;
        const numerator = tf * (this.k1 + 1);
        const denominator = tf + this.k1 * (1 - this.b + this.b * (docLen / this.avgDocLength));
        const termScore = idf * (numerator / denominator);

        scores.set(posting.documentId, (scores.get(posting.documentId) || 0) + termScore);
      }
    }

    return Array.from(scores.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, limit)
      .map(([docId, score]) => ({
        product: this.documents.get(docId)!,
        score: Math.round(score * 100) / 100
      }));
  }

  private tokenize(text: string): string[] {
    return text
      .toLowerCase()
      .replace(/[^a-z0-9\s]/g, '')
      .split(/\s+/)
      .filter(t => t.length > 1);
  }

  private updateAvgDocLength(): void {
    if (this.docLengths.size === 0) {
      this.avgDocLength = 0;
      return;
    }
    const sum = Array.from(this.docLengths.values()).reduce((a, b) => a + b, 0);
    this.avgDocLength = sum / this.docLengths.size;
  }
}
