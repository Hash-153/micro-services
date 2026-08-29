import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def build_inventory_and_catalog_advanced():
    print("Generating Inventory and Catalog Advanced...")

    # 1. Inventory Aisle Optimizer
    write_file("services/inventory-service/src/domain/aisle-graph-optimizer.ts", """export interface WarehouseBinLocation {
  binId: string;
  zone: string;
  aisle: number;
  shelf: number;
  position: number;
}

export interface PickItem {
  sku: string;
  quantity: number;
  binLocation: WarehouseBinLocation;
}

export class AisleGraphOptimizer {
  public static calculateOptimalPickPath(items: PickItem[]): PickItem[] {
    // Sorts by S-shape picking trajectory across warehouse aisles
    return [...items].sort((a, b) => {
      // 1. Zone sorting
      if (a.binLocation.zone !== b.binLocation.zone) {
        return a.binLocation.zone.localeCompare(b.binLocation.zone);
      }

      // 2. Aisle sorting
      if (a.binLocation.aisle !== b.binLocation.aisle) {
        return a.binLocation.aisle - b.binLocation.aisle;
      }

      // 3. S-shape serpentine direction: even aisles go forward, odd aisles go backwards
      const isEvenAisle = a.binLocation.aisle % 2 === 0;
      if (isEvenAisle) {
        if (a.binLocation.shelf !== b.binLocation.shelf) {
          return a.binLocation.shelf - b.binLocation.shelf;
        }
        return a.binLocation.position - b.binLocation.position;
      } else {
        if (a.binLocation.shelf !== b.binLocation.shelf) {
          return b.binLocation.shelf - a.binLocation.shelf;
        }
        return b.binLocation.position - a.binLocation.position;
      }
    });
  }
}
""")

    # 2. Inventory Supplier PO Service
    write_file("services/inventory-service/src/services/supplier-po.service.ts", """import { Logger } from '@novacommerce/core-logger';

export interface SupplierPurchaseOrder {
  poNumber: string;
  supplierId: string;
  supplierName: string;
  targetWarehouseId: string;
  items: { sku: string; quantity: number; unitCostCents: number }[];
  totalCostCents: number;
  status: 'DRAFT' | 'ISSUED' | 'CONFIRMED' | 'IN_TRANSIT' | 'RECEIVED' | 'CANCELLED';
  expectedDeliveryDate: Date;
  createdAt: Date;
}

export class SupplierPoService {
  private logger: Logger;
  private purchaseOrders: Map<string, SupplierPurchaseOrder> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async createPurchaseOrder(
    supplierId: string,
    supplierName: string,
    targetWarehouseId: string,
    items: { sku: string; quantity: number; unitCostCents: number }[],
    leadTimeDays: number = 7
  ): Promise<SupplierPurchaseOrder> {
    const poNumber = `PO-${Date.now().toString(36).toUpperCase()}`;
    const totalCostCents = items.reduce((acc, it) => acc + it.quantity * it.unitCostCents, 0);
    const expectedDeliveryDate = new Date(Date.now() + leadTimeDays * 24 * 60 * 60 * 1000);

    const po: SupplierPurchaseOrder = {
      poNumber,
      supplierId,
      supplierName,
      targetWarehouseId,
      items,
      totalCostCents,
      status: 'ISSUED',
      expectedDeliveryDate,
      createdAt: new Date()
    };

    this.purchaseOrders.set(poNumber, po);
    this.logger.info(`Supplier purchase order created: ${poNumber} ($${(totalCostCents / 100).toFixed(2)}) for warehouse ${targetWarehouseId}`);
    return po;
  }

  public async getPurchaseOrder(poNumber: string): Promise<SupplierPurchaseOrder | null> {
    return this.purchaseOrders.get(poNumber) || null;
  }
}
""")

    # 3. Catalog Product SEO Optimizer
    write_file("services/catalog-service/src/domain/product-seo-optimizer.ts", """import { ProductEntity } from '@novacommerce/core-types';

export interface ProductSeoMetadata {
  title: string;
  description: string;
  canonicalUrl: string;
  openGraph: {
    title: string;
    description: string;
    type: 'product';
    url: string;
    imageUrl?: string;
    priceAmount: string;
    priceCurrency: string;
  };
  jsonLdSchema: Record<string, any>;
}

export class ProductSeoOptimizer {
  public static generateSeoMetadata(product: ProductEntity, baseUrl: string = 'https://storefront.novacommerce.io'): ProductSeoMetadata {
    const canonicalUrl = `${baseUrl}/products/${product.slug}`;
    const primaryImage = product.images.find(img => img.isPrimary)?.url || product.images[0]?.url;
    const formattedPrice = (product.basePrice.amount / 100).toFixed(2);

    const jsonLdSchema = {
      '@context': 'https://schema.org',
      '@type': 'Product',
      name: product.name,
      image: primaryImage,
      description: product.description,
      sku: product.sku,
      offers: {
        '@type': 'Offer',
        url: canonicalUrl,
        priceCurrency: product.basePrice.currency,
        price: formattedPrice,
        availability: product.isActive ? 'https://schema.org/InStock' : 'https://schema.org/OutOfStock'
      }
    };

    return {
      title: `${product.name} | NovaCommerce Enterprise`,
      description: product.description.substring(0, 160),
      canonicalUrl,
      openGraph: {
        title: product.name,
        description: product.description.substring(0, 200),
        type: 'product',
        url: canonicalUrl,
        imageUrl: primaryImage,
        priceAmount: formattedPrice,
        priceCurrency: product.basePrice.currency
      },
      jsonLdSchema
    };
  }
}
""")

    # 4. Catalog Recommendation Service
    write_file("services/catalog-service/src/services/recommendation.service.ts", """import { ProductEntity } from '@novacommerce/core-types';
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
""")

    print("Inventory and Catalog advanced complete.")

if __name__ == "__main__":
    build_inventory_and_catalog_advanced()
