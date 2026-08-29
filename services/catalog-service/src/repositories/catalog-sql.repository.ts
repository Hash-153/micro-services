import { ProductEntity, PaginationParams, PaginatedResult } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class CatalogSqlRepository {
  private logger: Logger;
  private products: Map<string, ProductEntity> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async findById(id: string): Promise<ProductEntity | null> {
    return this.products.get(id) || null;
  }

  public async findBySku(sku: string): Promise<ProductEntity | null> {
    for (const p of this.products.values()) {
      if (p.sku === sku) return p;
    }
    return null;
  }

  public async create(product: ProductEntity): Promise<ProductEntity> {
    this.products.set(product.id, product);
    this.logger.info(`Product persisted in SQL repo: SKU ${product.sku} (ID: ${product.id})`);
    return product;
  }

  public async update(id: string, partial: Partial<ProductEntity>): Promise<ProductEntity> {
    const p = this.products.get(id);
    if (!p) throw new Error(`Product ${id} not found in SQL repo`);
    const updated = { ...p, ...partial, updatedAt: new Date() };
    this.products.set(id, updated);
    return updated;
  }
}
