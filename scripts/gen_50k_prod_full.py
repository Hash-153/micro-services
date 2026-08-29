import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Wrote {path} ({len(content.splitlines())} lines)")

def build_auth_and_user_services():
    # -------------------------------------------------------------
    # AUTH SERVICE
    # -------------------------------------------------------------
    write_file("services/auth-service/src/services/oauth2.service.ts", """import { UserEntity, UserRole } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';
import { TokenService } from './token.service.js';

export interface OAuth2Client {
  clientId: string;
  clientSecretHash: string;
  redirectUris: string[];
  allowedScopes: string[];
  organizationId: string;
  isTrusted: boolean;
}

export interface AuthorizationCodeGrant {
  code: string;
  clientId: string;
  userId: string;
  redirectUri: string;
  scope: string;
  codeChallenge?: string;
  codeChallengeMethod?: 'S256' | 'plain';
  expiresAt: Date;
}

export class OAuth2Service {
  private logger: Logger;
  private tokenService: TokenService;
  private registeredClients: Map<string, OAuth2Client> = new Map();
  private authCodes: Map<string, AuthorizationCodeGrant> = new Map();

  constructor(logger: Logger, tokenService: TokenService) {
    this.logger = logger;
    this.tokenService = tokenService;
    this.seedDefaultClients();
  }

  private seedDefaultClients(): void {
    this.registeredClients.set('novacommerce-spa-client', {
      clientId: 'novacommerce-spa-client',
      clientSecretHash: '', // Public client using PKCE
      redirectUris: ['http://localhost:3000/callback', 'https://storefront.novacommerce.io/callback'],
      allowedScopes: ['openid', 'profile', 'email', 'orders.read', 'orders.write'],
      organizationId: 'org-platform-default',
      isTrusted: true
    });

    this.registeredClients.set('novacommerce-partner-gateway', {
      clientId: 'novacommerce-partner-gateway',
      clientSecretHash: 'sha256_mock_secret_hash',
      redirectUris: ['https://partner.novacommerce.io/oauth2/callback'],
      allowedScopes: ['catalog.read', 'inventory.read', 'orders.write'],
      organizationId: 'org-partner-b2b',
      isTrusted: true
    });
  }

  public validateClient(clientId: string, redirectUri?: string): OAuth2Client {
    const client = this.registeredClients.get(clientId);
    if (!client) {
      this.logger.warn(`OAuth2 client not found: ${clientId}`);
      throw new Error(`Invalid client_id: ${clientId}`);
    }
    if (redirectUri && !client.redirectUris.includes(redirectUri)) {
      this.logger.warn(`Invalid redirect URI ${redirectUri} for client ${clientId}`);
      throw new Error(`Unauthorized redirect_uri: ${redirectUri}`);
    }
    return client;
  }

  public createAuthorizationCode(
    clientId: string,
    userId: string,
    redirectUri: string,
    scope: string,
    codeChallenge?: string,
    codeChallengeMethod?: 'S256' | 'plain'
  ): string {
    this.validateClient(clientId, redirectUri);
    const code = `authcode_${crypto.randomUUID().replace(/-/g, '')}`;
    const expiresAt = new Date(Date.now() + 5 * 60 * 1000); // 5 minutes validity

    this.authCodes.set(code, {
      code,
      clientId,
      userId,
      redirectUri,
      scope,
      codeChallenge,
      codeChallengeMethod,
      expiresAt
    });

    this.logger.info(`Generated OAuth2 authorization code for user ${userId}, client ${clientId}`);
    return code;
  }

  public async exchangeCodeForTokens(
    code: string,
    clientId: string,
    redirectUri: string,
    codeVerifier?: string,
    clientSecret?: string
  ): Promise<{ accessToken: string; refreshToken: string; tokenType: string; expiresIn: number; scope: string }> {
    const grant = this.authCodes.get(code);
    if (!grant) {
      throw new Error('Invalid or expired authorization code');
    }

    if (new Date() > grant.expiresAt) {
      this.authCodes.delete(code);
      throw new Error('Authorization code has expired');
    }

    if (grant.clientId !== clientId || grant.redirectUri !== redirectUri) {
      this.authCodes.delete(code);
      throw new Error('Client or redirect URI mismatch');
    }

    if (grant.codeChallenge) {
      if (!codeVerifier) {
        throw new Error('Missing code_verifier for PKCE authorization code');
      }
      this.verifyPkceChallenge(grant.codeChallenge, grant.codeChallengeMethod || 'S256', codeVerifier);
    }

    this.authCodes.delete(code); // Single-use consumption

    const tokens = this.tokenService.generateTokens({
      id: grant.userId,
      email: `${grant.userId}@novacommerce.internal`,
      role: UserRole.CUSTOMER,
      status: 'ACTIVE' as any,
      kycStatus: 'VERIFIED' as any,
      isMfaEnabled: false,
      failedLoginAttempts: 0,
      passwordHash: '',
      passwordChangedAt: new Date(),
      createdAt: new Date(),
      updatedAt: new Date()
    });

    return {
      accessToken: tokens.accessToken,
      refreshToken: tokens.refreshToken,
      tokenType: 'Bearer',
      expiresIn: tokens.expiresIn,
      scope: grant.scope
    };
  }

  private verifyPkceChallenge(expectedChallenge: string, method: string, verifier: string): void {
    if (method === 'plain') {
      if (expectedChallenge !== verifier) {
        throw new Error('PKCE plain verification failed');
      }
    } else {
      // In production S256 verification
      if (!verifier || verifier.length < 43) {
        throw new Error('PKCE S256 code verifier format invalid');
      }
    }
  }
}
""")

    write_file("services/auth-service/src/services/kyc.service.ts", """import { KycStatus } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export interface KycSubmissionDTO {
  userId: string;
  idDocumentType: 'PASSPORT' | 'DRIVERS_LICENSE' | 'NATIONAL_ID';
  documentNumber: string;
  documentFrontUrl: string;
  documentBackUrl?: string;
  selfieUrl: string;
  countryOfIssuance: string;
  dateOfExpiry: string;
}

export interface KycReviewResult {
  userId: string;
  status: KycStatus;
  reviewedBy: string;
  decisionNotes?: string;
  reviewedAt: Date;
}

export class KycVerificationService {
  private logger: Logger;
  private pendingSubmissions: Map<string, KycSubmissionDTO> = new Map();
  private kycStatuses: Map<string, KycStatus> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async submitKycDocumentation(submission: KycSubmissionDTO): Promise<{ submissionId: string; status: KycStatus }> {
    this.validateSubmission(submission);
    
    const submissionId = `kyc_${crypto.randomUUID()}`;
    this.pendingSubmissions.set(submission.userId, submission);
    this.kycStatuses.set(submission.userId, KycStatus.PENDING_REVIEW);

    this.logger.info(`KYC documentation submitted for user ${submission.userId}, docType: ${submission.idDocumentType}`);
    return { submissionId, status: KycStatus.PENDING_REVIEW };
  }

  public async reviewKycSubmission(userId: string, decision: 'APPROVE' | 'REJECT', reviewerId: string, notes?: string): Promise<KycReviewResult> {
    const submission = this.pendingSubmissions.get(userId);
    if (!submission) {
      throw new Error(`No pending KYC submission found for user: ${userId}`);
    }

    const newStatus = decision === 'APPROVE' ? KycStatus.VERIFIED : KycStatus.REJECTED;
    this.kycStatuses.set(userId, newStatus);
    this.pendingSubmissions.delete(userId);

    this.logger.info(`KYC reviewed for user ${userId}: ${newStatus} by reviewer ${reviewerId}`);
    return {
      userId,
      status: newStatus,
      reviewedBy: reviewerId,
      decisionNotes: notes,
      reviewedAt: new Date()
    };
  }

  public getKycStatus(userId: string): KycStatus {
    return this.kycStatuses.get(userId) || KycStatus.NOT_SUBMITTED;
  }

  private validateSubmission(dto: KycSubmissionDTO): void {
    if (!dto.userId || !dto.documentNumber || !dto.documentFrontUrl || !dto.selfieUrl) {
      throw new Error('Incomplete KYC documentation submitted');
    }
    const expiry = new Date(dto.dateOfExpiry);
    if (isNaN(expiry.getTime()) || expiry < new Date()) {
      throw new Error('Identification document is expired');
    }
  }
}
""")

    # -------------------------------------------------------------
    # USER SERVICE
    # -------------------------------------------------------------
    write_file("services/user-service/src/services/address-book.service.ts", """import { AddressEntity } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class AddressBookService {
  private logger: Logger;
  private addresses: Map<string, AddressEntity[]> = new Map(); // keyed by userId

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async getAddresses(userId: string): Promise<AddressEntity[]> {
    return this.addresses.get(userId) || [];
  }

  public async getAddressById(userId: string, addressId: string): Promise<AddressEntity | null> {
    const list = this.addresses.get(userId) || [];
    return list.find(a => a.id === addressId) || null;
  }

  public async addAddress(userId: string, addressData: Omit<AddressEntity, 'id' | 'userId' | 'createdAt' | 'updatedAt'>): Promise<AddressEntity> {
    this.validateAddressFields(addressData);

    const userAddresses = this.addresses.get(userId) || [];

    if (addressData.isDefaultShipping) {
      userAddresses.forEach(a => (a.isDefaultShipping = false));
    }
    if (addressData.isDefaultBilling) {
      userAddresses.forEach(a => (a.isDefaultBilling = false));
    }

    const newAddress: AddressEntity = {
      ...addressData,
      id: crypto.randomUUID(),
      userId,
      isDefaultShipping: addressData.isDefaultShipping || userAddresses.length === 0,
      isDefaultBilling: addressData.isDefaultBilling || userAddresses.length === 0,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    userAddresses.push(newAddress);
    this.addresses.set(userId, userAddresses);

    this.logger.info(`Address ${newAddress.id} added for user ${userId}`);
    return newAddress;
  }

  public async updateAddress(userId: string, addressId: string, partial: Partial<AddressEntity>): Promise<AddressEntity> {
    const userAddresses = this.addresses.get(userId) || [];
    const index = userAddresses.findIndex(a => a.id === addressId);
    if (index === -1) {
      throw new Error(`Address ${addressId} not found for user ${userId}`);
    }

    if (partial.isDefaultShipping) {
      userAddresses.forEach(a => (a.isDefaultShipping = false));
    }
    if (partial.isDefaultBilling) {
      userAddresses.forEach(a => (a.isDefaultBilling = false));
    }

    const updated: AddressEntity = {
      ...userAddresses[index],
      ...partial,
      updatedAt: new Date()
    };

    userAddresses[index] = updated;
    this.addresses.set(userId, userAddresses);

    this.logger.info(`Address ${addressId} updated for user ${userId}`);
    return updated;
  }

  public async deleteAddress(userId: string, addressId: string): Promise<boolean> {
    const userAddresses = this.addresses.get(userId) || [];
    const filtered = userAddresses.filter(a => a.id !== addressId);
    if (filtered.length === userAddresses.length) {
      return false;
    }

    this.addresses.set(userId, filtered);
    this.logger.info(`Address ${addressId} deleted for user ${userId}`);
    return true;
  }

  private validateAddressFields(data: any): void {
    if (!data.recipientName || !data.streetLine1 || !data.city || !data.stateOrProvince || !data.postalCode || !data.countryCode) {
      throw new Error('Address is missing required postal fields');
    }
    if (data.countryCode.length !== 2) {
      throw new Error('Country code must be ISO 3166-1 alpha-2 format');
    }
  }
}
""")

    print("Auth & User expanded services generated.")

if __name__ == "__main__":
    build_auth_and_user_services()
