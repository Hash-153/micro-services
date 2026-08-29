export interface SagaContext {
  orderId: string;
  userId: string;
  items: Array<{ sku: string; quantity: number }>;
  totalAmount: number;
  currency: string;
  paymentMethod: { type: string; token: string; provider: string };
  carrierCode: string;
  reservationId?: string;
  paymentTransactionId?: string;
  shipmentId?: string;
  correlationId: string;
}

export interface ISagaStep {
  name: string;
  execute(context: SagaContext): Promise<void>;
  compensate(context: SagaContext): Promise<void>;
}
