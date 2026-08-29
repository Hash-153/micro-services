import { ProductEntity } from '@novacommerce/core-types';

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
