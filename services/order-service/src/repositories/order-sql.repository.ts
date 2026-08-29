import { OrderEntity, OrderStatus, PaginationParams, PaginatedResult } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class OrderSqlRepository {
  private logger: Logger;
  private orders: Map<string, OrderEntity> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async findById(id: string): Promise<OrderEntity | null> {
    return this.orders.get(id) || null;
  }

  public async findByOrderNumber(orderNumber: string): Promise<OrderEntity | null> {
    for (const order of this.orders.values()) {
      if (order.orderNumber === orderNumber) return order;
    }
    return null;
  }

  public async findByUserId(userId: string, params: PaginationParams): Promise<PaginatedResult<OrderEntity>> {
    const userOrders = Array.from(this.orders.values())
      .filter(o => o.userId === userId)
      .sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());

    const page = params.page || 1;
    const limit = params.limit || 20;
    const offset = (page - 1) * limit;
    const items = userOrders.slice(offset, offset + limit);

    return {
      items,
      total: userOrders.length,
      page,
      limit,
      totalPages: Math.ceil(userOrders.length / limit),
      hasNext: offset + limit < userOrders.length,
      hasPrevious: page > 1
    };
  }

  public async create(order: OrderEntity): Promise<OrderEntity> {
    this.orders.set(order.id, order);
    this.logger.info(`Order persisted to SQL repository: ${order.orderNumber} (ID: ${order.id})`);
    return order;
  }

  public async updateStatus(id: string, status: OrderStatus): Promise<OrderEntity> {
    const order = this.orders.get(id);
    if (!order) throw new Error(`Order ${id} not found in repository`);
    order.status = status;
    order.updatedAt = new Date();
    this.orders.set(id, order);
    return order;
  }
}
