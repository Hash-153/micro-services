export interface EmailTemplateDefinition {
  templateKey: string;
  subject: string;
  htmlContent: string;
  textContent: string;
  requiredVariables: string[];
}

export const TRANSACTIONAL_EMAIL_TEMPLATES: Record<string, EmailTemplateDefinition> = {
  'ORDER_CONFIRMATION': {
    templateKey: 'ORDER_CONFIRMATION',
    subject: 'Order Confirmed - #{{orderNumber}}',
    htmlContent: `
      <div style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <h2 style="color: #1e40af;">Thank you for your order, {{customerName}}!</h2>
        <p>Your order <strong>#{{orderNumber}}</strong> has been received and is being processed by our automated fulfillment network.</p>
        <div style="background: #f8fafc; padding: 16px; border-radius: 6px; margin: 20px 0;">
          <p style="margin: 0;"><strong>Order Total:</strong> {{totalAmount}}</p>
          <p style="margin: 4px 0 0;"><strong>Estimated Delivery:</strong> {{estimatedDeliveryDate}}</p>
        </div>
        <p>You can track the live status of your shipment anytime at <a href="{{trackingUrl}}">{{trackingUrl}}</a>.</p>
      </div>`,
    textContent: 'Thank you for your order, {{customerName}}! Order #{{orderNumber}} is being processed. Total: {{totalAmount}}. Track at: {{trackingUrl}}',
    requiredVariables: ['customerName', 'orderNumber', 'totalAmount', 'estimatedDeliveryDate', 'trackingUrl']
  },
  'PAYMENT_RECEIPT': {
    templateKey: 'PAYMENT_RECEIPT',
    subject: 'Payment Receipt for Order #{{orderNumber}}',
    htmlContent: `
      <div style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <h2 style="color: #059669;">Payment Successful</h2>
        <p>We received your payment of <strong>{{amountPaid}}</strong> for Order #{{orderNumber}}.</p>
        <p><strong>Payment Method:</strong> {{paymentMethod}} (ending in {{lastFour}})</p>
        <p><strong>Transaction Reference:</strong> {{transactionReference}}</p>
      </div>`,
    textContent: 'Payment of {{amountPaid}} received for Order #{{orderNumber}}. Reference: {{transactionReference}}',
    requiredVariables: ['amountPaid', 'orderNumber', 'paymentMethod', 'lastFour', 'transactionReference']
  },
  'SHIPMENT_DISPATCHED': {
    templateKey: 'SHIPMENT_DISPATCHED',
    subject: 'Your order #{{orderNumber}} is on the way!',
    htmlContent: `
      <div style="font-family: sans-serif; max-width: 600px; margin: auto; padding: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
        <h2 style="color: #2563eb;">Package Dispatched</h2>
        <p>Carrier: <strong>{{carrierName}}</strong></p>
        <p>Tracking Number: <strong>{{trackingNumber}}</strong></p>
        <a href="{{trackingUrl}}" style="display: inline-block; background: #2563eb; color: #fff; padding: 12px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-top: 12px;">Track Package</a>
      </div>`,
    textContent: 'Your order #{{orderNumber}} has been shipped via {{carrierName}}. Tracking: {{trackingNumber}}',
    requiredVariables: ['orderNumber', 'carrierName', 'trackingNumber', 'trackingUrl']
  }
};

export class EmailTemplateRegistry {
  public static getTemplate(key: string): EmailTemplateDefinition | undefined {
    return TRANSACTIONAL_EMAIL_TEMPLATES[key];
  }
}
