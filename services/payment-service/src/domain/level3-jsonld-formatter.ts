import { Level3ProcessingPayload } from './level3-card-data-builder.js';

export class Level3JsonLdFormatter {
  public static formatJsonLd(payload: Level3ProcessingPayload): Record<string, any> {
    return {
      '@context': 'https://schema.org',
      '@type': 'Invoice',
      category: payload.summaryCommodityCode,
      broker: {
        '@type': 'Organization',
        name: 'NovaCommerce Global Inc',
        postalCode: payload.shipFromPostalCode
      },
      customer: {
        '@type': 'Organization',
        postalCode: payload.destinationPostalCode,
        addressCountry: payload.destinationCountryCode
      },
      totalPaymentDue: {
        '@type': 'PriceSpecification',
        price: payload.lineItems.reduce((acc, it) => acc + it.totalAmountCents, 0) / 100,
        priceCurrency: 'USD'
      }
    };
  }
}
