import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v27():
    print("Generating comprehensive Production V27 Modules...")

    # 1. Fulfillment International Customs Commercial Invoice Builder
    write_file("services/fulfillment-service/src/domain/customs-invoice-builder.ts", """import { OrderEntity, Currency } from '@novacommerce/core-types';

export interface CustomsLineItem {
  hsTariffCode: string;
  description: string;
  countryOfOrigin: string;
  quantity: number;
  unitValueCents: number;
  totalValueCents: number;
}

export interface CommercialCustomsInvoice {
  invoiceNumber: string;
  incoterm: 'DAP' | 'DDP' | 'FOB' | 'CIF';
  shipperTaxId: string;
  recipientTaxId?: string;
  items: CustomsLineItem[];
  declaredTotalCents: number;
  currency: Currency;
  exportReason: 'COMMERCIAL_SALE' | 'SAMPLE' | 'RETURN';
  declarationSignature: string;
}

export class CustomsInvoiceBuilder {
  public static buildInvoice(
    order: OrderEntity,
    shipperTaxId: string = 'US-EIN-9921004',
    incoterm: CommercialCustomsInvoice['incoterm'] = 'DDP'
  ): CommercialCustomsInvoice {
    const items: CustomsLineItem[] = order.items.map(it => ({
      hsTariffCode: '8471.30.01', // Data processing machines / computers
      description: it.productName,
      countryOfOrigin: 'US',
      quantity: it.quantity,
      unitValueCents: it.unitPrice.amount,
      totalValueCents: it.unitPrice.amount * it.quantity
    }));

    const declaredTotal = items.reduce((acc, it) => acc + it.totalValueCents, 0);

    return {
      invoiceNumber: `CI-${order.orderNumber}`,
      incoterm,
      shipperTaxId,
      items,
      declaredTotalCents: declaredTotal,
      currency: order.totalAmount.currency,
      exportReason: 'COMMERCIAL_SALE',
      declarationSignature: 'NovaCommerce Global Trade Compliance Officer'
    };
  }
}
""")

    # 2. Analytics Product Performance Affinity Matrix
    write_file("services/analytics-service/src/domain/product-affinity-matrix.ts", """export interface ProductAffinityPair {
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
""")

    print("Production V27 modules generated.")

if __name__ == "__main__":
    generate_prod_v27()
