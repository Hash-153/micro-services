import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { ProductEntity, CategoryEntity } from '@novacommerce/core-types';

export class InMemoryProductRepository extends InMemoryBaseRepository<ProductEntity> {
  public async findBySku(sku: string): Promise<ProductEntity | null> {
    for (const p of this.items.values()) {
      if (p.sku === sku && !p.deletedAt) return JSON.parse(JSON.stringify(p));
    }
    return null;
  }
}

export class InMemoryCategoryRepository extends InMemoryBaseRepository<CategoryEntity> {}
