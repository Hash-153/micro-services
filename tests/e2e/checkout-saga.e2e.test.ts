import { InMemoryStockRepository, InMemoryReservationRepository } from '../../services/inventory-service/src/repositories/inventory.repository.js';
import { InventoryService } from '../../services/inventory-service/src/services/inventory.service.js';
import { InMemoryPaymentRepository, InMemoryLedgerRepository } from '../../services/payment-service/src/repositories/payment.repository.js';
import { PaymentService } from '../../services/payment-service/src/services/payment.service.js';
import { InMemoryShipmentRepository } from '../../services/fulfillment-service/src/repositories/shipment.repository.js';
import { FulfillmentService } from '../../services/fulfillment-service/src/services/fulfillment.service.js';
import { CheckoutSagaOrchestrator } from '../../services/order-service/src/saga/checkout-saga.orchestrator.js';
import { ISagaStep, SagaContext } from '../../services/order-service/src/saga/saga-step.interface.js';
import { Logger } from '@novacommerce/core-logger';
import { randomUUID } from 'crypto';

describe('Distributed Checkout Saga End-to-End Test Suite', () => {
  const logger = Logger.create('e2e-test');
  let inventoryService: InventoryService;
  let paymentService: PaymentService;
  let fulfillmentService: FulfillmentService;
  let saga: CheckoutSagaOrchestrator;

  beforeEach(async () => {
    const stockRepo = new InMemoryStockRepository();
    const resRepo = new InMemoryReservationRepository();
    inventoryService = new InventoryService(stockRepo, resRepo);

    // Initial warehouse stock setup
    await inventoryService.setStock('SKU-LAPTOP-PRO', 'WH-MAIN-01', 10);

    const paymentRepo = new InMemoryPaymentRepository();
    const ledgerRepo = new InMemoryLedgerRepository();
    paymentService = new PaymentService(paymentRepo, ledgerRepo);

    const shipmentRepo = new InMemoryShipmentRepository();
    fulfillmentService = new FulfillmentService(shipmentRepo);

    saga = new CheckoutSagaOrchestrator(logger);

    // Step 1: Inventory Reservation Step
    const inventoryStep: ISagaStep = {
      name: 'ReserveInventory',
      execute: async (ctx: SagaContext) => {
        for (const item of ctx.items) {
          const res = await inventoryService.reserveStock(ctx.orderId, item.sku, item.quantity, ctx.correlationId);
          ctx.reservationId = res.id;
        }
      },
      compensate: async (ctx: SagaContext) => {
        await inventoryService.releaseReservation(ctx.orderId, ctx.correlationId);
      }
    };

    // Step 2: Payment Authorization Step
    const paymentStep: ISagaStep = {
      name: 'AuthorizePayment',
      execute: async (ctx: SagaContext) => {
        if (ctx.paymentMethod.token === 'tok_force_decline') {
          throw new Error('Card declined: Insufficient funds');
        }
        const payment = await paymentService.authorizePayment(ctx.orderId, ctx.userId, ctx.totalAmount);
        ctx.paymentTransactionId = payment.id;
      },
      compensate: async (ctx: SagaContext) => {
        // Refund logic
      }
    };

    // Step 3: Fulfillment Creation Step
    const fulfillmentStep: ISagaStep = {
      name: 'CreateFulfillment',
      execute: async (ctx: SagaContext) => {
        const shipment = await fulfillmentService.createShipment(ctx.orderId, {});
        ctx.shipmentId = shipment.id;
      },
      compensate: async (ctx: SagaContext) => {
        // Void shipment
      }
    };

    saga.addStep(inventoryStep).addStep(paymentStep).addStep(fulfillmentStep);
  });

  it('should successfully execute forward saga when all services succeed', async () => {
    const context: SagaContext = {
      orderId: 'ord-1001',
      userId: 'usr-444',
      items: [{ sku: 'SKU-LAPTOP-PRO', quantity: 1 }],
      totalAmount: 189900,
      currency: 'USD',
      paymentMethod: { type: 'CREDIT_CARD', token: 'tok_valid_card', provider: 'STRIPE' },
      carrierCode: 'FEDEX',
      correlationId: randomUUID()
    };

    const result = await saga.execute(context);
    expect(result).toBe(true);
    expect(context.reservationId).toBeDefined();
    expect(context.paymentTransactionId).toBeDefined();
    expect(context.shipmentId).toBeDefined();
  });

  it('should rollback and release inventory reservation when payment declines', async () => {
    const context: SagaContext = {
      orderId: 'ord-1002',
      userId: 'usr-444',
      items: [{ sku: 'SKU-LAPTOP-PRO', quantity: 1 }],
      totalAmount: 189900,
      currency: 'USD',
      paymentMethod: { type: 'CREDIT_CARD', token: 'tok_force_decline', provider: 'STRIPE' },
      carrierCode: 'FEDEX',
      correlationId: randomUUID()
    };

    await expect(saga.execute(context)).rejects.toThrow();
  });
});
