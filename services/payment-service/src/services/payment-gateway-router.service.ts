import { PaymentGatewayProvider, Currency } from '@novacommerce/core-types';

export class PaymentGatewayRouter {
  public static selectOptimalGateway(currency: Currency, countryCode: string = 'US', amountCents: number = 0): PaymentGatewayProvider {
    if (currency === Currency.EUR || countryCode === 'DE' || countryCode === 'FR' || countryCode === 'NL') {
      return PaymentGatewayProvider.ADYEN;
    }
    if (currency === Currency.USD || countryCode === 'US' || countryCode === 'CA') {
      return PaymentGatewayProvider.STRIPE;
    }
    return PaymentGatewayProvider.MOCK;
  }
}
