import { OrderStatus, OrderCancellationReason } from '../enums/OrderStatus.js';
import { Money } from '../enums/Currency.js';
import { AddressEntity } from './User.js';

export interface OrderItemEntity {
  id: string;
  orderId: string;
  sku: string;
  productName: string;
  variantName?: string;
  unitPrice: Money;
  quantity: number;
  subtotal: Money;
  taxAmount: Money;
  discountAmount: Money;
  total: Money;
  metadata?: Record<string, unknown>;
}

export interface OrderEntity {
  id: string;
  orderNumber: string;
  userId: string;
  status: OrderStatus;
  shippingAddress: AddressEntity;
  billingAddress: AddressEntity;
  items: OrderItemEntity[];
  subtotalAmount: Money;
  taxAmount: Money;
  shippingFeeAmount: Money;
  discountAmount: Money;
  totalAmount: Money;
  couponCode?: string;
  paymentId?: string;
  shipmentId?: string;
  cancellationReason?: OrderCancellationReason;
  notes?: string;
  idempotencyKey?: string;
  createdAt: Date;
  updatedAt: Date;
}
