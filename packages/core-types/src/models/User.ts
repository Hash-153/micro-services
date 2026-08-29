import { UserRole, AccountStatus, KycStatus } from '../enums/UserRole.js';

export interface UserEntity {
  id: string;
  email: string;
  passwordHash: string;
  role: UserRole;
  status: AccountStatus;
  kycStatus: KycStatus;
  organizationId?: string;
  isMfaEnabled: boolean;
  mfaSecret?: string;
  failedLoginAttempts: number;
  lockedUntil?: Date;
  lastLoginAt?: Date;
  createdAt: Date;
  updatedAt: Date;
  deletedAt?: Date;
}

export interface UserProfileEntity {
  id: string;
  userId: string;
  firstName: string;
  lastName: string;
  phoneNumber?: string;
  avatarUrl?: string;
  timeZone: string;
  locale: string;
  metadata: Record<string, unknown>;
  createdAt: Date;
  updatedAt: Date;
}

export interface AddressEntity {
  id: string;
  userId: string;
  recipientName: string;
  streetLine1: string;
  streetLine2?: string;
  city: string;
  stateOrProvince: string;
  postalCode: string;
  countryCode: string; // ISO 3166-1 alpha-2 (e.g. US, DE, GB)
  isDefaultShipping: boolean;
  isDefaultBilling: boolean;
  phone?: string;
  createdAt: Date;
  updatedAt: Date;
}
