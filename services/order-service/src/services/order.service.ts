import { InMemoryOrderRepository } from '../repositories/order.repository.js';
import { OrderEntity, OrderStatus, Currency, NotFoundError, CreateOrderDTO } from '@novacommerce/core-types';
import { TaxCalculator } from '../domain/tax-calculator.js';
import { OrderStateMachine } from '../domain/order-state-machine.js';
import { IEventBus, DomainEventFactory } from '@novacommerce/core-events';
import { EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class OrderService {
  private readonly repo: InMemoryOrderRepository;
  private readonly eventBus?: IEventBus;

  constructor(repo: InMemoryOrderRepository, eventBus?: IEventBus) {
    this.repo = repo;
    this.eventBus = eventBus;
  }

  public async createOrder(dto: CreateOrderDTO, userId: string = 'user-anon', correlationId?: string): Promise<OrderEntity> {
    const orderNumber = `ORD-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
    
    let subtotalCents = 0;
    const items = dto.items.map(i => {
      const unitCents = 2999; // mock unit price
      const totalItem = unitCents * i.quantity;
      subtotalCents += totalItem;
      return {
        id: randomUUID(),
        orderId: '',
        sku: i.sku,
        productName: `Item ${i.sku}`,
        unitPrice: { amount: unitCents, currency: dto.currency || Currency.USD },
        quantity: i.quantity,
        subtotal: { amount: totalItem, currency: dto.currency || Currency.USD },
        taxAmount: { amount: 0, currency: dto.currency || Currency.USD },
        discountAmount: { amount: 0, currency: dto.currency || Currency.USD },
        total: { amount: totalItem, currency: dto.currency || Currency.USD }
      };
    });

    const subtotalMoney = { amount: subtotalCents, currency: dto.currency || Currency.USD };
    const taxMoney = TaxCalculator.calculateTax(subtotalMoney, 'US');
    const shippingMoney = { amount: 500, currency: dto.currency || Currency.USD };
    const totalMoney = { amount: subtotalMoney.amount + taxMoney.amount + shippingMoney.amount, currency: dto.currency || Currency.USD };

    const orderId = randomUUID();
    items.forEach(i => (i.orderId = orderId));

    const order: OrderEntity = {
      id: orderId,
      orderNumber,
      userId,
      status: OrderStatus.PENDING_PAYMENT,
      shippingAddress: {} as any,
      billingAddress: {} as any,
      items,
      subtotalAmount: subtotalMoney,
      taxAmount: taxMoney,
      shippingFeeAmount: shippingMoney,
      discountAmount: { amount: 0, currency: dto.currency || Currency.USD },
      totalAmount: totalMoney,
      idempotencyKey: dto.idempotencyKey,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    const saved = await this.repo.create(order);

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.ORDER_CREATED,
        saved.id,
        'Order',
        saved,
        'order-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return saved;
  }

  public async updateOrderStatus(id: string, newStatus: OrderStatus, correlationId?: string): Promise<OrderEntity> {
    const order = await this.repo.findById(id);
    if (!order) throw new NotFoundError('Order', id);

    const validStatus = OrderStateMachine.transition(order.status, newStatus);
    const updated = await this.repo.update(id, { status: validStatus });

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.ORDER_UPDATED,
        id,
        'Order',
        { orderId: id, status: validStatus },
        'order-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return updated!;
  }

  public async getOrderById(id: string): Promise<OrderEntity> {
    const order = await this.repo.findById(id);
    if (!order) throw new NotFoundError('Order', id);
    return order;
  }
}
