import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { UserProfileEntity, AddressEntity } from '@novacommerce/core-types';

export class InMemoryUserProfileRepository extends InMemoryBaseRepository<UserProfileEntity> {
  public async findByUserId(userId: string): Promise<UserProfileEntity | null> {
    for (const item of this.items.values()) {
      if (item.userId === userId) return JSON.parse(JSON.stringify(item));
    }
    return null;
  }
}

export class InMemoryAddressRepository extends InMemoryBaseRepository<AddressEntity> {
  public async findByUserId(userId: string): Promise<AddressEntity[]> {
    return Array.from(this.items.values()).filter(a => a.userId === userId);
  }
}
