import { z } from 'zod';
import { Currency } from '../enums/Currency.js';

export const OrderItemInputSchema = z.object({
  sku: z.string().min(1),
  quantity: z.number().int().positive()
});

export const CreateOrderSchema = z.object({
  userId: z.string().uuid().optional(),
  shippingAddressId: z.string().uuid(),
  billingAddressId: z.string().uuid(),
  items: z.array(OrderItemInputSchema).min(1),
  currency: z.nativeEnum(Currency).default(Currency.USD),
  couponCode: z.string().optional(),
  notes: z.string().max(500).optional(),
  idempotencyKey: z.string().uuid()
});

export type CreateOrderDTO = z.infer<typeof CreateOrderSchema>;

export const CheckoutSagaRequestSchema = z.object({
  orderId: z.string().uuid(),
  paymentMethod: z.object({
    type: z.string(),
    token: z.string(),
    provider: z.string()
  }),
  carrierCode: z.string().default('MOCK_CARRIER'),
  idempotencyKey: z.string().uuid()
});

export type CheckoutSagaRequestDTO = z.infer<typeof CheckoutSagaRequestSchema>;
