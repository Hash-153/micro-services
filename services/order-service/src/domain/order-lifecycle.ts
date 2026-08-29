import { OrderStatus } from '@novacommerce/core-types';

export class OrderLifecycleStateMachine {
  private static readonly VALID_TRANSITIONS: Record<OrderStatus, OrderStatus[]> = {
    [OrderStatus.DRAFT]: [OrderStatus.PENDING_PAYMENT, OrderStatus.CANCELLED],
    [OrderStatus.PENDING_PAYMENT]: [OrderStatus.PAYMENT_AUTHORIZED, OrderStatus.PAYMENT_FAILED, OrderStatus.CANCELLED, OrderStatus.EXPIRED],
    [OrderStatus.PAYMENT_AUTHORIZED]: [OrderStatus.PROCESSING, OrderStatus.INVENTORY_RESERVED, OrderStatus.CANCELLED],
    [OrderStatus.PAYMENT_FAILED]: [OrderStatus.PENDING_PAYMENT, OrderStatus.CANCELLED, OrderStatus.EXPIRED],
    [OrderStatus.PROCESSING]: [OrderStatus.INVENTORY_RESERVED, OrderStatus.INVENTORY_ALLOCATION_FAILED, OrderStatus.CANCELLED],
    [OrderStatus.INVENTORY_RESERVED]: [OrderStatus.PACKED, OrderStatus.CANCELLED],
    [OrderStatus.INVENTORY_ALLOCATION_FAILED]: [OrderStatus.CANCELLED, OrderStatus.PROCESSING],
    [OrderStatus.PACKED]: [OrderStatus.DISPATCHED, OrderStatus.CANCELLED],
    [OrderStatus.DISPATCHED]: [OrderStatus.IN_TRANSIT, OrderStatus.DELIVERED, OrderStatus.RETURNED_TO_SENDER],
    [OrderStatus.IN_TRANSIT]: [OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED, OrderStatus.FAILED_ATTEMPT, OrderStatus.LOST_IN_TRANSIT],
    [OrderStatus.OUT_FOR_DELIVERY]: [OrderStatus.DELIVERED, OrderStatus.FAILED_ATTEMPT],
    [OrderStatus.DELIVERED]: [OrderStatus.REFUND_REQUESTED, OrderStatus.REFUNDED, OrderStatus.PARTIALLY_REFUNDED],
    [OrderStatus.CANCELLED]: [],
    [OrderStatus.REFUND_REQUESTED]: [OrderStatus.REFUNDED, OrderStatus.PARTIALLY_REFUNDED, OrderStatus.DELIVERED],
    [OrderStatus.REFUNDED]: [],
    [OrderStatus.PARTIALLY_REFUNDED]: [OrderStatus.REFUNDED],
    [OrderStatus.EXPIRED]: []
  };

  public static canTransition(current: OrderStatus, next: OrderStatus): boolean {
    const allowed = this.VALID_TRANSITIONS[current];
    return allowed ? allowed.includes(next) : false;
  }

  public static validateTransition(current: OrderStatus, next: OrderStatus): void {
    if (!this.canTransition(current, next)) {
      throw new Error(`Illegal order state transition from ${current} to ${next}`);
    }
  }

  public static isTerminal(status: OrderStatus): boolean {
    return [OrderStatus.CANCELLED, OrderStatus.REFUNDED, OrderStatus.EXPIRED].includes(status);
  }

  public static isCancellable(status: OrderStatus): boolean {
    return [
      OrderStatus.DRAFT,
      OrderStatus.PENDING_PAYMENT,
      OrderStatus.PAYMENT_AUTHORIZED,
      OrderStatus.PROCESSING,
      OrderStatus.INVENTORY_RESERVED,
      OrderStatus.PACKED
    ].includes(status);
  }
}
