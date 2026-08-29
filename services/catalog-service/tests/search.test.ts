import { SearchIndexingService } from '../src/services/search-indexing.service.js';
import { Currency } from '@novacommerce/core-types';

describe('Search Indexing Suite', () => {
  const searchIndex = new SearchIndexingService();

  beforeAll(() => {
    searchIndex.indexProduct({
      id: 'p1',
      sku: 'NOVA-HEADPHONE-01',
      name: 'Wireless Noise Canceling Headphones Pro',
      slug: 'wireless-nc-headphones',
      description: 'Superior sound quality with active noise cancellation and 40h battery.',
      categoryId: 'cat_audio',
      basePrice: { amount: 29900, currency: Currency.USD },
      isActive: true,
      tags: ['audio', 'wireless', 'bluetooth'],
      attributes: {},
      images: [],
      createdAt: new Date(),
      updatedAt: new Date()
    });
  });

  it('should find indexed product by token match', () => {
    const results = searchIndex.search('Noise Canceling');
    expect(results.length).toBe(1);
    expect(results[0].product.sku).toBe('NOVA-HEADPHONE-01');
  });

  it('should filter search results by price range', () => {
    const results = searchIndex.search('Headphones', { minPriceCents: 50000 });
    expect(results.length).toBe(0);
  });
});
