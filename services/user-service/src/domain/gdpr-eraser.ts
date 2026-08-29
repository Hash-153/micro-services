import { UserProfileEntity, AddressEntity } from '@novacommerce/core-types';

export class GdprErasureEngine {
  public static anonymizeProfile(profile: UserProfileEntity): UserProfileEntity {
    const anonymousId = `anon_${Date.now().toString(36)}`;

    return {
      ...profile,
      firstName: 'ANONYMIZED',
      lastName: 'ANONYMIZED',
      avatarUrl: undefined,
      timezone: 'UTC',
      updatedAt: new Date()
    };
  }

  public static anonymizeAddress(address: AddressEntity): AddressEntity {
    return {
      ...address,
      recipientName: 'REDACTED GDPR',
      streetLine1: 'REDACTED GDPR',
      streetLine2: undefined,
      phone: undefined,
      updatedAt: new Date()
    };
  }
}
