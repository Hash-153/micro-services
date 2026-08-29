import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { OrderEntity } from '@novacommerce/core-types';

export class InMemoryOrderRepository extends InMemoryBaseRepository<OrderEntity> {
  public async findByOrderNumber(orderNumber: string): Promise<OrderEntity | null> {
    for (const ord of this.items.values()) {
      if (ord.orderNumber === orderNumber) return JSON.parse(JSON.stringify(ord));
    }
    return null;
  }

  public async findByUserId(userId: string): Promise<OrderEntity[]> {
    return Array.from(this.items.values()).filter(o => o.userId === userId);
  }
}
