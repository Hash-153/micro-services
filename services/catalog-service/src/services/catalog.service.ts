import { InMemoryProductRepository, InMemoryCategoryRepository } from '../repositories/product.repository.js';
import { ProductEntity, CategoryEntity, CreateProductDTO, NotFoundError, ConflictError } from '@novacommerce/core-types';
import { IEventBus, DomainEventFactory } from '@novacommerce/core-events';
import { EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class CatalogService {
  private readonly productRepo: InMemoryProductRepository;
  private readonly categoryRepo: InMemoryCategoryRepository;
  private readonly eventBus?: IEventBus;

  constructor(productRepo: InMemoryProductRepository, categoryRepo: InMemoryCategoryRepository, eventBus?: IEventBus) {
    this.productRepo = productRepo;
    this.categoryRepo = categoryRepo;
    this.eventBus = eventBus;
  }

  public async createProduct(dto: CreateProductDTO, correlationId?: string): Promise<ProductEntity> {
    const existing = await this.productRepo.findBySku(dto.sku);
    if (existing) {
      throw new ConflictError(`Product with SKU '${dto.sku}' already exists.`);
    }

    const product: ProductEntity = {
      id: randomUUID(),
      sku: dto.sku,
      name: dto.name,
      slug: dto.slug,
      description: dto.description,
      categoryId: dto.categoryId,
      basePrice: dto.basePrice,
      isActive: dto.isActive,
      tags: dto.tags,
      attributes: dto.attributes,
      images: [],
      createdAt: new Date(),
      updatedAt: new Date()
    };

    const saved = await this.productRepo.create(product);

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.CATALOG_PRODUCT_CREATED,
        saved.id,
        'Product',
        saved,
        'catalog-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return saved;
  }

  public async getProductById(id: string): Promise<ProductEntity> {
    const product = await this.productRepo.findById(id);
    if (!product || product.deletedAt) {
      throw new NotFoundError('Product', id);
    }
    return product;
  }

  public async listProducts(limit: number = 20, offset: number = 0): Promise<{ items: ProductEntity[]; total: number }> {
    const items = await this.productRepo.findAll({ isActive: true } as any, limit, offset);
    const total = await this.productRepo.count({ isActive: true } as any);
    return { items, total };
  }
}
