import { NotificationService } from '../../services/notification-service/src/services/notification.service.js';
import { Logger } from '@novacommerce/core-logger';

describe('E2E Scenario: Omni-Channel Notification Dispatch (Email, SMS, Push)', () => {
  const logger = Logger.create('test-notification-e2e');
  const service = new NotificationService(logger);

  it('should dispatch email and SMS notifications successfully', async () => {
    const emailResult = await service.send({
      recipient: 'shopper@example.com',
      channel: 'EMAIL',
      template: 'order_confirmation',
      data: { orderNumber: 'ORD-2026-999', totalAmount: 4999 }
    });

    expect(emailResult.id).toBeDefined();
    expect(emailResult.status).toBe('DELIVERED');

    const smsResult = await service.send({
      recipient: '+15551234567',
      channel: 'SMS',
      template: 'shipping_dispatched',
      data: { orderNumber: 'ORD-2026-999', trackingNumber: 'TRK-12345678' }
    });

    expect(smsResult.id).toBeDefined();
    expect(smsResult.status).toBe('DELIVERED');
  });
});
