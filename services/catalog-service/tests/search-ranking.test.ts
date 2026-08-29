import { SearchIndexingService } from '../src/services/search-indexing.service.js';
import { Currency } from '@novacommerce/core-types';

describe('Catalog Service: TF-IDF Search Ranking & Token Matching Suite', () => {
  const search = new SearchIndexingService();

  beforeAll(() => {
    search.indexProduct({
      id: 'p-1',
      sku: 'MACBOOK-PRO-16',
      name: 'Apple MacBook Pro 16-inch M3 Max',
      slug: 'macbook-pro-16-m3',
      description: 'Professional high performance laptop workstation with 36GB memory.',
      categoryId: 'cat-laptops',
      basePrice: { amount: 349900, currency: Currency.USD },
      isActive: true,
      tags: ['apple', 'macbook', 'laptop', 'workstation'],
      attributes: {},
      images: [],
      createdAt: new Date(),
      updatedAt: new Date()
    });

    search.indexProduct({
      id: 'p-2',
      sku: 'MACBOOK-AIR-13',
      name: 'Apple MacBook Air 13-inch M3',
      slug: 'macbook-air-13-m3',
      description: 'Ultra thin lightweight portable laptop with all day battery life.',
      categoryId: 'cat-laptops',
      basePrice: { amount: 109900, currency: Currency.USD },
      isActive: true,
      tags: ['apple', 'macbook', 'laptop', 'portable'],
      attributes: {},
      images: [],
      createdAt: new Date(),
      updatedAt: new Date()
    });
  });

  it('should rank MacBook Pro higher when querying for Max performance', () => {
    const results = search.search('MacBook Pro Workstation');
    expect(results.length).toBeGreaterThan(0);
    expect(results[0].product.sku).toBe('MACBOOK-PRO-16');
  });
});
