import { OrderStatus, AppError, ErrorCode } from '@novacommerce/core-types';

const ALLOWED_TRANSITIONS: Record<OrderStatus, OrderStatus[]> = {
  [OrderStatus.DRAFT]: [OrderStatus.PENDING_PAYMENT, OrderStatus.CANCELLED],
  [OrderStatus.PENDING_PAYMENT]: [OrderStatus.PAYMENT_AUTHORIZED, OrderStatus.PAYMENT_FAILED, OrderStatus.CANCELLED, OrderStatus.EXPIRED],
  [OrderStatus.PAYMENT_AUTHORIZED]: [OrderStatus.PROCESSING, OrderStatus.INVENTORY_RESERVED, OrderStatus.CANCELLED],
  [OrderStatus.INVENTORY_RESERVED]: [OrderStatus.PROCESSING, OrderStatus.PACKED, OrderStatus.CANCELLED],
  [OrderStatus.INVENTORY_ALLOCATION_FAILED]: [OrderStatus.CANCELLED],
  [OrderStatus.PAYMENT_FAILED]: [OrderStatus.PENDING_PAYMENT, OrderStatus.CANCELLED],
  [OrderStatus.PROCESSING]: [OrderStatus.PACKED, OrderStatus.CANCELLED],
  [OrderStatus.PACKED]: [OrderStatus.DISPATCHED, OrderStatus.CANCELLED],
  [OrderStatus.DISPATCHED]: [OrderStatus.IN_TRANSIT, OrderStatus.DELIVERED],
  [OrderStatus.IN_TRANSIT]: [OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED],
  [OrderStatus.OUT_FOR_DELIVERY]: [OrderStatus.DELIVERED],
  [OrderStatus.DELIVERED]: [OrderStatus.REFUND_REQUESTED, OrderStatus.REFUNDED],
  [OrderStatus.CANCELLED]: [],
  [OrderStatus.REFUND_REQUESTED]: [OrderStatus.REFUNDED, OrderStatus.PARTIALLY_REFUNDED],
  [OrderStatus.REFUNDED]: [],
  [OrderStatus.PARTIALLY_REFUNDED]: [OrderStatus.REFUNDED],
  [OrderStatus.EXPIRED]: []
};

export class OrderStateMachine {
  public static canTransition(current: OrderStatus, target: OrderStatus): boolean {
    const allowed = ALLOWED_TRANSITIONS[current] || [];
    return allowed.includes(target);
  }

  public static transition(current: OrderStatus, target: OrderStatus): OrderStatus {
    if (!this.canTransition(current, target)) {
      throw new AppError(
        `Invalid order status transition from ${current} to ${target}`,
        400,
        ErrorCode.ORDER_INVALID_STATE_TRANSITION
      );
    }
    return target;
  }
}
