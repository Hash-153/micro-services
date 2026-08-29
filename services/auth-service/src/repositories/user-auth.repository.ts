import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { UserEntity } from '@novacommerce/core-types';

export interface IUserAuthRepository {
  findById(id: string): Promise<UserEntity | null>;
  findByEmail(email: string): Promise<UserEntity | null>;
  create(user: UserEntity): Promise<UserEntity>;
  update(id: string, user: Partial<UserEntity>): Promise<UserEntity | null>;
}

export class InMemoryUserAuthRepository extends InMemoryBaseRepository<UserEntity> implements IUserAuthRepository {
  public async findByEmail(email: string): Promise<UserEntity | null> {
    const normalized = email.toLowerCase().trim();
    for (const item of this.items.values()) {
      if (item.email.toLowerCase().trim() === normalized && !item.deletedAt) {
        return JSON.parse(JSON.stringify(item));
      }
    }
    return null;
  }
}
