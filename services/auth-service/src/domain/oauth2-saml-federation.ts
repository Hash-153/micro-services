export interface SamlIdentityProviderConfig {
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
