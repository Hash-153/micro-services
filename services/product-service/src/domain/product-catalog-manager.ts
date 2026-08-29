import { ProductEntity, CategoryEntity, ProductVariantEntity } from '@novacommerce/core-types';

export interface CatalogSearchParams {
  query?: string;
  categoryIds?: string[];
  priceRange?: { min: number; max: number };
  inStock?: boolean;
  tags?: string[];
  sortBy?: 'name' | 'price' | 'created' | 'popularity';
  sortOrder?: 'asc' | 'desc';
}

export interface SearchResult {
  products: ProductEntity[];
  total: number;
  facets: {
    categories: { id: string; name: string; count: number }[];
    priceRanges: { range: string; count: number }[];
    tags: { tag: string; count: number }[];
  };
}

export class ProductCatalogManager {
  private products: Map<string, ProductEntity> = new Map();
  private categories: Map<string, CategoryEntity> = new Map();

  constructor() {
    this.initializeSampleCatalog();
  }

  private initializeSampleCatalog(): void {
    // Sample products for demonstration
    const electronicsCategory: CategoryEntity = {
      id: 'cat-001',
      name: 'Electronics',
      slug: 'electronics',
      description: 'Consumer electronics and gadgets',
      displayOrder: 1,
      isActive: true,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    const clothingCategory: CategoryEntity = {
      id: 'cat-002',
      name: 'Clothing',
      slug: 'clothing',
      description: 'Apparel and fashion items',
      displayOrder: 2,
      isActive: true,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.categories.set(electronicsCategory.id, electronicsCategory);
    this.categories.set(clothingCategory.id, clothingCategory);

    // Add sample products
    const laptop: ProductEntity = {
      id: 'prod-001',
      sku: 'LAPTOP-PRO-001',
      name: 'Professional Laptop 15"',
      slug: 'professional-laptop-15',
      description: 'High-performance laptop for professionals',
      categoryId: electronicsCategory.id,
      basePrice: { amount: 129999, currency: 'USD' },
      isActive: true,
      isFeatured: true,
      tags: ['electronics', 'laptop', 'professional'],
      attributes: {
        brand: 'TechCorp',
        processor: 'Intel i7',
        ram: '16GB',
        storage: '512GB SSD'
      },
      images: [
        {
          id: 'img-001',
          url: 'https://example.com/laptop-1.jpg',
          altText: 'Laptop front view',
          sortOrder: 0,
          isPrimary: true
        }
      ],
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.products.set(laptop.id, laptop);
  }

  public async search(params: CatalogSearchParams): Promise<SearchResult> {
    let results = Array.from(this.products.values());

    // Filter by category
    if (params.categoryIds && params.categoryIds.length > 0) {
      results = results.filter(p => params.categoryIds!.includes(p.categoryId));
    }

    // Filter by price range
    if (params.priceRange) {
      results = results.filter(p => 
        p.basePrice.amount >= params.priceRange!.min * 100 &&
        p.basePrice.amount <= params.priceRange!.max * 100
      );
    }

    // Filter by tags
    if (params.tags && params.tags.length > 0) {
      results = results.filter(p =>
        params.tags!.some(tag => p.tags.includes(tag))
      );
    }

    // Filter by stock status
    if (params.inStock !== undefined) {
      results = results.filter(p => p.isActive === params.inStock);
    }

    // Text search
    if (params.query) {
      const query = params.query.toLowerCase();
      results = results.filter(p =>
        p.name.toLowerCase().includes(query) ||
        p.description.toLowerCase().includes(query) ||
        p.sku.toLowerCase().includes(query)
      );
    }

    // Sort
    const sortField = params.sortBy || 'name';
    const sortDir = params.sortOrder === 'desc' ? -1 : 1;

    results.sort((a, b) => {
      let comparison = 0;
      if (sortField === 'name') {
        comparison = a.name.localeCompare(b.name);
      } else if (sortField === 'price') {
        comparison = a.basePrice.amount - b.basePrice.amount;
      } else if (sortField === 'created') {
        comparison = a.createdAt.getTime() - b.createdAt.getTime();
      }
      return comparison * sortDir;
    });

    // Generate facets
    const facets = {
      categories: this.generateCategoryFacets(results),
      priceRanges: this.generatePriceRangeFacets(results),
      tags: this.generateTagFacets(results)
    };

    return {
      products: results,
      total: results.length,
      facets
    };
  }

  private generateCategoryFacets(products: ProductEntity[]): { id: string; name: string; count: number }[] {
    const counts = new Map<string, number>();
    products.forEach(p => {
      counts.set(p.categoryId, (counts.get(p.categoryId) || 0) + 1);
    });

    return Array.from(counts.entries()).map(([id, count]) => {
      const category = this.categories.get(id);
      return {
        id,
        name: category?.name || 'Unknown',
        count
      };
    });
  }

  private generatePriceRangeFacets(products: ProductEntity[]): { range: string; count: number }[] {
    const ranges = [
      { min: 0, max: 50, label: 'Under $50' },
      { min: 50, max: 100, label: '$50 - $100' },
      { min: 100, max: 250, label: '$100 - $250' },
      { min: 250, max: 500, label: '$250 - $500' },
      { min: 500, max: 1000, label: '$500 - $1000' },
      { min: 1000, max: Infinity, label: '$1000+' }
    ];

    return ranges.map(range => ({
      range: range.label,
      count: products.filter(p =>
        p.basePrice.amount >= range.min * 100 &&
        p.basePrice.amount < range.max * 100
      ).length
    }));
  }

  private generateTagFacets(products: ProductEntity[]): { tag: string; count: number }[] {
    const counts = new Map<string, number>();
    products.forEach(p => {
      p.tags.forEach(tag => {
        counts.set(tag, (counts.get(tag) || 0) + 1);
      });
    });

    return Array.from(counts.entries())
      .map(([tag, count]) => ({ tag, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 10);
  }

  public async getProductById(id: string): Promise<ProductEntity | null> {
    return this.products.get(id) || null;
  }

  public async getProductBySku(sku: string): Promise<ProductEntity | null> {
    return Array.from(this.products.values()).find(p => p.sku === sku) || null;
  }

  public async getProductsByIds(ids: string[]): Promise<ProductEntity[]> {
    return ids.map(id => this.products.get(id)).filter((p): p is ProductEntity => p !== undefined);
  }

  public async createProduct(product: Omit<ProductEntity, 'id' | 'createdAt' | 'updatedAt'>): Promise<ProductEntity> {
    const newProduct: ProductEntity = {
      ...product,
      id: `prod-${Date.now()}`,
      createdAt: new Date(),
      updatedAt: new Date()
    };
    this.products.set(newProduct.id, newProduct);
    return newProduct;
  }

  public async updateProduct(id: string, updates: Partial<ProductEntity>): Promise<ProductEntity> {
    const existing = this.products.get(id);
    if (!existing) {
      throw new Error(`Product not found: ${id}`);
    }

    const updated: ProductEntity = {
      ...existing,
      ...updates,
      id,
      updatedAt: new Date()
    };

    this.products.set(id, updated);
    return updated;
  }

  public async deleteProduct(id: string): Promise<boolean> {
    return this.products.delete(id);
  }
}
