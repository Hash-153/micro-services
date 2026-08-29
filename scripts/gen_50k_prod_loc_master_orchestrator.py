import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_master_orchestrator_modules():
    print("Generating comprehensive Master Orchestrator Modules...")

    # -------------------------------------------------------------------------
    # 1. AUTH SERVICE OAUTH2 & SAML IDENTITY PROVIDER MAPPINGS
    # -------------------------------------------------------------------------
    write_file("services/auth-service/src/domain/oauth2-saml-federation.ts", """export interface SamlIdentityProviderConfig {
  idpEntityId: string;
  ssoLoginUrl: string;
  ssoLogoutUrl?: string;
  x509CertificatePem: string;
  allowIdpInitiatedSso: boolean;
  nameIdFormat: 'urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress' | 'urn:oasis:names:tc:SAML:2.0:nameid-format:persistent';
}

export interface OAuth2ProviderConfig {
  providerName: 'GOOGLE' | 'GITHUB' | 'MICROSOFT_AZURE_AD' | 'OKTA' | 'PING_IDENTITY';
  clientId: string;
  clientSecret: string;
  authorizationUrl: string;
  tokenUrl: string;
  userInfoUrl: string;
  scopes: string[];
}

export class IdentityFederationRegistry {
  private static readonly OAUTH2_PROVIDERS: Map<string, OAuth2ProviderConfig> = new Map([
    [
      'GOOGLE',
      {
        providerName: 'GOOGLE',
        clientId: 'google-oauth2-client-id.apps.googleusercontent.com',
        clientSecret: 'sec_google_client_secret_placeholder',
        authorizationUrl: 'https://accounts.google.com/o/oauth2/v2/auth',
        tokenUrl: 'https://oauth2.googleapis.com/token',
        userInfoUrl: 'https://openidconnect.googleapis.com/v1/userinfo',
        scopes: ['openid', 'email', 'profile']
      }
    ],
    [
      'MICROSOFT_AZURE_AD',
      {
        providerName: 'MICROSOFT_AZURE_AD',
        clientId: 'azure-ad-application-client-id',
        clientSecret: 'sec_azure_ad_secret_placeholder',
        authorizationUrl: 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
        tokenUrl: 'https://login.microsoftonline.com/common/oauth2/v2.0/token',
        userInfoUrl: 'https://graph.microsoft.com/v1.0/me',
        scopes: ['openid', 'email', 'profile', 'User.Read']
      }
    ],
    [
      'OKTA',
      {
        providerName: 'OKTA',
        clientId: 'okta-enterprise-client-id',
        clientSecret: 'sec_okta_client_secret_placeholder',
        authorizationUrl: 'https://novacommerce.okta.com/oauth2/v1/authorize',
        tokenUrl: 'https://novacommerce.okta.com/oauth2/v1/token',
        userInfoUrl: 'https://novacommerce.okta.com/oauth2/v1/userinfo',
        scopes: ['openid', 'email', 'profile', 'groups']
      }
    ]
  ]);

  public static getOAuth2Config(providerName: string): OAuth2ProviderConfig | undefined {
    return this.OAUTH2_PROVIDERS.get(providerName.toUpperCase());
  }
}
""")

    # -------------------------------------------------------------------------
    # 2. PAYMENT SERVICE CURRENCY ROUNDING & PRECISION RULES
    # -------------------------------------------------------------------------
    write_file("services/payment-service/src/domain/currency-precision-rules.ts", """import { Currency } from '@novacommerce/core-types';

export interface CurrencyFormattingSpec {
  currency: Currency;
  minorUnitDecimalPlaces: number;
  symbol: string;
  symbolPlacement: 'BEFORE' | 'AFTER';
  thousandsSeparator: string;
  decimalSeparator: string;
}

export const CURRENCY_FORMATTING_SPECS: Record<Currency, CurrencyFormattingSpec> = {
  [Currency.USD]: { currency: Currency.USD, minorUnitDecimalPlaces: 2, symbol: '$', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.EUR]: { currency: Currency.EUR, minorUnitDecimalPlaces: 2, symbol: '€', symbolPlacement: 'AFTER', thousandsSeparator: '.', decimalSeparator: ',' },
  [Currency.GBP]: { currency: Currency.GBP, minorUnitDecimalPlaces: 2, symbol: '£', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.CAD]: { currency: Currency.CAD, minorUnitDecimalPlaces: 2, symbol: 'CA$', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.AUD]: { currency: Currency.AUD, minorUnitDecimalPlaces: 2, symbol: 'AU$', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.JPY]: { currency: Currency.JPY, minorUnitDecimalPlaces: 0, symbol: '¥', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.CHF]: { currency: Currency.CHF, minorUnitDecimalPlaces: 2, symbol: 'CHF ', symbolPlacement: 'BEFORE', thousandsSeparator: "'", decimalSeparator: '.' },
  [Currency.SGD]: { currency: Currency.SGD, minorUnitDecimalPlaces: 2, symbol: 'SG$', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' },
  [Currency.INR]: { currency: Currency.INR, minorUnitDecimalPlaces: 2, symbol: '₹', symbolPlacement: 'BEFORE', thousandsSeparator: ',', decimalSeparator: '.' }
};

export class CurrencyFormatter {
  public static format(amountCents: number, currency: Currency): string {
    const spec = CURRENCY_FORMATTING_SPECS[currency] || CURRENCY_FORMATTING_SPECS[Currency.USD];

    let formattedValue: string;
    if (spec.minorUnitDecimalPlaces === 0) {
      formattedValue = Math.round(amountCents / 100).toLocaleString('en-US');
    } else {
      const mainUnits = (amountCents / 100).toFixed(spec.minorUnitDecimalPlaces);
      const [whole, dec] = mainUnits.split('.');
      const wholeFormatted = whole.replace(/\\B(?=(\\d{3})+(?!\\d))/g, spec.thousandsSeparator);
      formattedValue = `${wholeFormatted}${spec.decimalSeparator}${dec}`;
    }

    return spec.symbolPlacement === 'BEFORE'
      ? `${spec.symbol}${formattedValue}`
      : `${formattedValue} ${spec.symbol}`;
  }
}
""")

    print("Master orchestrator modules generated.")

if __name__ == "__main__":
    generate_master_orchestrator_modules()
