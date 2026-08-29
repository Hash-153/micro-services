import { AnalyticsService } from '../../services/analytics-service/src/services/analytics.service.js';
import { Logger } from '@novacommerce/core-logger';

describe('E2E Scenario: Real-Time Clickstream Ingestion & Conversion Funnel Analytics', () => {
  const logger = Logger.create('test-analytics-e2e');
  const analytics = new AnalyticsService(logger);

  it('should ingest telemetry events and aggregate summary counts', async () => {
    await analytics.trackEvent({ eventName: 'product_viewed', properties: { sku: 'SKU-001' } });
    await analytics.trackEvent({ eventName: 'cart_item_added', properties: { sku: 'SKU-001', qty: 1 } });
    await analytics.trackEvent({ eventName: 'checkout_started', properties: { cartTotal: 2999 } });
    await analytics.trackEvent({ eventName: 'order_completed', properties: { orderId: 'ord-100' } });

    const summary = analytics.getSummary();
    expect(summary.totalEvents).toBe(4);
    expect(summary.countsByEvent['product_viewed']).toBe(1);
    expect(summary.countsByEvent['order_completed']).toBe(1);
  });
});
