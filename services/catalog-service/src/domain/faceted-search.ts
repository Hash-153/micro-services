import { ProductEntity, ProductSearchFilter } from '@novacommerce/core-types';

export interface FacetResult {
  field: string;
  buckets: { key: string; count: number }[];
}

export interface SearchResponsePayload {
  items: ProductEntity[];
  total: number;
  facets: FacetResult[];
  page: number;
  limit: number;
  totalPages: number;
}

export class FacetedSearchEngine {
  public static executeSearch(products: ProductEntity[], filter: ProductSearchFilter): SearchResponsePayload {
    let matches = products.filter(p => p.isActive);

    if (filter.query) {
      const q = filter.query.toLowerCase().trim();
      matches = matches.filter(p =>
        p.name.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q) ||
        p.sku.toLowerCase().includes(q) ||
        p.tags.some(t => t.toLowerCase().includes(q))
      );
    }

    if (filter.categoryId) {
      matches = matches.filter(p => p.categoryId === filter.categoryId);
    }

    if (filter.minPriceCents !== undefined) {
      matches = matches.filter(p => p.basePrice.amount >= filter.minPriceCents!);
    }

    if (filter.maxPriceCents !== undefined) {
      matches = matches.filter(p => p.basePrice.amount <= filter.maxPriceCents!);
    }

    if (filter.tags && filter.tags.length > 0) {
      matches = matches.filter(p => filter.tags!.some(t => p.tags.includes(t)));
    }

    // Build Facet Buckets
    const categoryCounts: Record<string, number> = {};
    const tagCounts: Record<string, number> = {};

    matches.forEach(p => {
      categoryCounts[p.categoryId] = (categoryCounts[p.categoryId] || 0) + 1;
      p.tags.forEach(t => {
        tagCounts[t] = (tagCounts[t] || 0) + 1;
      });
    });

    const facets: FacetResult[] = [
      {
        field: 'categoryId',
        buckets: Object.entries(categoryCounts).map(([key, count]) => ({ key, count }))
      },
      {
        field: 'tags',
        buckets: Object.entries(tagCounts).map(([key, count]) => ({ key, count }))
      }
    ];

    const page = filter.page || 1;
    const limit = filter.limit || 20;
    const offset = (page - 1) * limit;
    const paginatedItems = matches.slice(offset, offset + limit);

    return {
      items: paginatedItems,
      total: matches.length,
      facets,
      page,
      limit,
      totalPages: Math.ceil(matches.length / limit)
    };
  }
}
