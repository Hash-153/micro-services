import { CheckoutSagaOrchestrator } from '../../services/order-service/src/domain/checkout-saga-orchestrator.js';
import { Logger } from '@novacommerce/core-logger';

describe('E2E Scenario: Full Distributed Saga Compensation & Order Rollback Workflow', () => {
  const logger = Logger.create('test-saga-rollback');

  it('should compensate previous steps in reverse order upon step failure', async () => {
    const executedSteps: string[] = [];
    const compensatedSteps: string[] = [];

    const mockSteps = [
      {
        name: 'Step 1: Reserve Inventory',
        execute: async (ctx: any) => {
          executedSteps.push('ReserveInventory');
          return { reservationId: 'res-001' };
        },
        compensate: async (ctx: any) => {
          compensatedSteps.push('ReleaseInventory');
        }
      },
      {
        name: 'Step 2: Authorize Payment',
        execute: async (ctx: any) => {
          executedSteps.push('AuthorizePayment');
          return { transactionId: 'txn-001' };
        },
        compensate: async (ctx: any) => {
          compensatedSteps.push('VoidPayment');
        }
      },
      {
        name: 'Step 3: Create Carrier Shipment Label',
        execute: async (ctx: any) => {
          executedSteps.push('CreateShipment');
          throw new Error('Carrier API timeout: Failed to create label');
        },
        compensate: async (ctx: any) => {
          compensatedSteps.push('CancelShipment');
        }
      }
    ];

    const orchestrator = new CheckoutSagaOrchestrator(logger, mockSteps);
    const result = await orchestrator.execute({
      orderId: 'ord-rollback-e2e',
      userId: 'usr-buyer-01',
      totalAmountCents: 15000,
      currency: 'USD',
      items: [{ sku: 'SKU-001', quantity: 2, unitPriceCents: 7500 }],
      shippingAddress: {
        recipientName: 'Bob Vance',
        streetLine1: '100 Refrigeration Way',
        city: 'Scranton',
        stateOrProvince: 'PA',
        postalCode: '18503',
        countryCode: 'US'
      }
    });

    expect(result.status).toBe('FAILED');
    expect(result.error).toContain('Carrier API timeout');
    expect(executedSteps).toEqual(['ReserveInventory', 'AuthorizePayment', 'CreateShipment']);
    expect(compensatedSteps).toEqual(['VoidPayment', 'ReleaseInventory']);
  });
});
