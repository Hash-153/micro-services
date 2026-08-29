import { InMemoryUserProfileRepository, InMemoryAddressRepository } from '../repositories/user-profile.repository.js';
import { UserProfileEntity, AddressEntity, NotFoundError } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class UserProfileService {
  private readonly profileRepo: InMemoryUserProfileRepository;
  private readonly addressRepo: InMemoryAddressRepository;

  constructor(profileRepo: InMemoryUserProfileRepository, addressRepo: InMemoryAddressRepository) {
    this.profileRepo = profileRepo;
    this.addressRepo = addressRepo;
  }

  public async getProfile(userId: string): Promise<UserProfileEntity> {
    let profile = await this.profileRepo.findByUserId(userId);
    if (!profile) {
      profile = await this.profileRepo.create({
        id: randomUUID(),
        userId,
        firstName: '',
        lastName: '',
        timeZone: 'UTC',
        locale: 'en-US',
        metadata: {},
        createdAt: new Date(),
        updatedAt: new Date()
      });
    }
    return profile;
  }

  public async updateProfile(userId: string, partial: Partial<UserProfileEntity>): Promise<UserProfileEntity> {
    const profile = await this.getProfile(userId);
    const updated = await this.profileRepo.update(profile.id, partial);
    return updated!;
  }

  public async addAddress(userId: string, addressData: Omit<AddressEntity, 'id' | 'userId' | 'createdAt' | 'updatedAt'>): Promise<AddressEntity> {
    return this.addressRepo.create({
      id: randomUUID(),
      userId,
      ...addressData,
      createdAt: new Date(),
      updatedAt: new Date()
    });
  }

  public async getAddresses(userId: string): Promise<AddressEntity[]> {
    return this.addressRepo.findByUserId(userId);
  }
}
