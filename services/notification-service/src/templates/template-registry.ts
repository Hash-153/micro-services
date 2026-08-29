export interface EmailTemplateDefinition {
  subject: string;
  htmlBody: string;
  textBody: string;
}

export const TRANSACTIONAL_TEMPLATES: Record<string, (data: any) => EmailTemplateDefinition> = {
  'order_confirmation': (d) => ({
    subject: `Order Confirmation #${d.orderNumber} - NovaCommerce`,
    htmlBody: `<h1>Thank you for your order!</h1><p>Your order <strong>#${d.orderNumber}</strong> totaling <strong>$${(d.totalAmount / 100).toFixed(2)}</strong> has been confirmed and is being processed.</p>`,
    textBody: `Thank you for your order #${d.orderNumber} totaling $${(d.totalAmount / 100).toFixed(2)}.`
  }),
  'shipping_dispatched': (d) => ({
    subject: `Your order #${d.orderNumber} has shipped!`,
    htmlBody: `<h1>Your shipment is on the way!</h1><p>Tracking number: <a href="${d.trackingUrl}">${d.trackingNumber}</a> via ${d.carrier}.</p>`,
    textBody: `Your order #${d.orderNumber} has shipped. Tracking: ${d.trackingNumber} via ${d.carrier}.`
  }),
  'payment_receipt': (d) => ({
    subject: `Receipt for Payment #${d.transactionReference}`,
    htmlBody: `<h1>Payment Received</h1><p>We received your payment of <strong>$${(d.amount / 100).toFixed(2)}</strong> via ${d.methodType}.</p>`,
    textBody: `Payment of $${(d.amount / 100).toFixed(2)} received for transaction ${d.transactionReference}.`
  }),
  'password_reset': (d) => ({
    subject: 'Reset Your NovaCommerce Password',
    htmlBody: `<h1>Password Reset</h1><p>Click <a href="${d.resetUrl}">here</a> to reset your password. Link expires in 15 minutes.</p>`,
    textBody: `Reset your password by opening: ${d.resetUrl}`
  }),
  'mfa_alert': (d) => ({
    subject: 'Security Alert: Two-Factor Authentication Updated',
    htmlBody: `<h1>Security Notice</h1><p>MFA was modified on your account at ${new Date().toISOString()} from IP ${d.ipAddress}.</p>`,
    textBody: `MFA was modified on your account from IP ${d.ipAddress}.`
  })
};
