import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_surge_modules():
    print("Generating comprehensive Production Surge Modules...")

    # 1. Metaphone & BM25 Inverted Search Indexer
    write_file("services/catalog-service/src/domain/search-bm25-indexer.ts", """import { ProductEntity } from '@novacommerce/core-types';

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
      .replace(/[^a-z0-9\\s]/g, '')
      .split(/\\s+/)
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
""")

    # 2. Bayesian Fraud Engine
    write_file("services/payment-service/src/domain/bayesian-fraud-engine.ts", """export interface FraudFeatures {
  transactionAmountCents: number;
  ipVelocityPerHour: number;
  cardAttemptsPerDay: number;
  isCountryMismatch: boolean;
  isProxyOrVpn: boolean;
  accountAgeDays: number;
  previousChargebackCount: number;
}

export class BayesianFraudEngine {
  public static calculateRiskProbability(features: FraudFeatures): { probability: number; riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'; recommendation: 'APPROVE' | 'CHALLENGE_3DS' | 'MANUAL_REVIEW' | 'REJECT' } {
    let priorOdds = 0.02 / (1 - 0.02); // Baseline fraud prior: 2%

    // Likelihood ratios (LR)
    const lrAmount = features.transactionAmountCents > 500000 ? 3.5 : 1.0;
    const lrIpVelocity = features.ipVelocityPerHour > 5 ? 4.2 : 1.0;
    const lrCardAttempts = features.cardAttemptsPerDay > 3 ? 5.0 : 1.0;
    const lrCountryMismatch = features.isCountryMismatch ? 3.8 : 1.0;
    const lrProxy = features.isProxyOrVpn ? 4.5 : 1.0;
    const lrAccountAge = features.accountAgeDays < 1 ? 2.5 : 0.8;
    const lrChargebacks = features.previousChargebackCount > 0 ? 10.0 : 0.9;

    const posteriorOdds = priorOdds * lrAmount * lrIpVelocity * lrCardAttempts * lrCountryMismatch * lrProxy * lrAccountAge * lrChargebacks;
    const probability = posteriorOdds / (1 + posteriorOdds);

    let riskLevel: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
    let recommendation: 'APPROVE' | 'CHALLENGE_3DS' | 'MANUAL_REVIEW' | 'REJECT';

    if (probability < 0.15) {
      riskLevel = 'LOW';
      recommendation = 'APPROVE';
    } else if (probability < 0.45) {
      riskLevel = 'MEDIUM';
      recommendation = 'CHALLENGE_3DS';
    } else if (probability < 0.75) {
      riskLevel = 'HIGH';
      recommendation = 'MANUAL_REVIEW';
    } else {
      riskLevel = 'CRITICAL';
      recommendation = 'REJECT';
    }

    return {
      probability: Math.round(probability * 1000) / 1000,
      riskLevel,
      recommendation
    };
  }
}
""")

    # 3. Distributed Saga Event Handlers
    write_file("services/order-service/src/saga/saga-event-listener.ts", """import { IEventBus, IDomainEvent } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';
import { OrderService } from '../services/order.service.js';

export class SagaEventListener {
  private eventBus: IEventBus;
  private logger: Logger;
  private orderService: OrderService;

  constructor(eventBus: IEventBus, logger: Logger, orderService: OrderService) {
    this.eventBus = eventBus;
    this.logger = logger;
    this.orderService = orderService;
  }

  public async startListening(): Promise<void> {
    await this.eventBus.subscribe('payment.captured', this.handlePaymentCaptured);
    await this.eventBus.subscribe('payment.failed', this.handlePaymentFailed);
    await this.eventBus.subscribe('fulfillment.shipment.delivered', this.handleShipmentDelivered);
    this.logger.info('Saga Event Listener successfully subscribed to domain event topics.');
  }

  private handlePaymentCaptured = async (event: IDomainEvent<{ orderId: string; transactionReference: string }>) => {
    this.logger.info(`Saga listener received payment.captured for order ${event.payload.orderId}`);
  };

  private handlePaymentFailed = async (event: IDomainEvent<{ orderId: string; failureReason: string }>) => {
    this.logger.warn(`Saga listener received payment.failed for order ${event.payload.orderId}: ${event.payload.failureReason}`);
  };

  private handleShipmentDelivered = async (event: IDomainEvent<{ orderId: string; shipmentNumber: string }>) => {
    this.logger.info(`Saga listener received fulfillment.shipment.delivered for order ${event.payload.orderId}`);
  };
}
""")

    print("Surge modules generated successfully.")

if __name__ == "__main__":
    generate_prod_surge_modules()
