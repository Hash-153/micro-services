import { OrderEntity } from '@novacommerce/core-types';

export class InvoiceBuilder {
  public static generateHtmlInvoice(order: OrderEntity): string {
    const formattedDate = new Date(order.createdAt).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    const itemsHtml = order.items.map(item => `
      <tr>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; font-family: monospace;">${item.sku}</td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0;">${item.productName}</td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: center;">${item.quantity}</td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: right;">$${(item.unitPrice.amount / 100).toFixed(2)}</td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: right;">$${(item.total.amount / 100).toFixed(2)}</td>
      </tr>
    `).join('');

    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Commercial Invoice #${order.orderNumber}</title>
  <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1a202c; padding: 40px; }
    .header { display: flex; justify-content: space-between; border-bottom: 2px solid #2b6cb0; padding-bottom: 20px; }
    .company { font-size: 24px; font-weight: bold; color: #2b6cb0; }
    .invoice-details { text-align: right; }
    .addresses { display: flex; justify-content: space-between; margin-top: 30px; }
    .box { width: 45%; background: #f7fafc; padding: 15px; border-radius: 6px; }
    table { width: 100%; border-collapse: collapse; margin-top: 30px; }
    th { background: #edf2f7; padding: 12px; text-align: left; font-size: 12px; text-transform: uppercase; }
    .summary { margin-top: 30px; display: flex; justify-content: flex-end; }
    .summary-table { width: 300px; }
    .summary-table td { padding: 8px; }
    .total-row { font-size: 18px; font-weight: bold; color: #2b6cb0; border-top: 2px solid #2b6cb0; }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <div class="company">NovaCommerce Technologies</div>
      <div>Enterprise Logistics & Commerce Solutions</div>
      <div>100 Market St, San Francisco, CA 94105</div>
      <div>support@novacommerce.io</div>
    </div>
    <div class="invoice-details">
      <h2>COMMERCIAL INVOICE</h2>
      <div><strong>Invoice #:</strong> ${order.orderNumber}</div>
      <div><strong>Date:</strong> ${formattedDate}</div>
      <div><strong>Status:</strong> ${order.status}</div>
      <div><strong>Payment Ref:</strong> ${order.paymentId || 'N/A'}</div>
    </div>
  </div>

  <div class="addresses">
    <div class="box">
      <strong>Billed To:</strong><br>
      ${order.billingAddress.recipientName}<br>
      ${order.billingAddress.streetLine1}<br>
      ${order.billingAddress.city}, ${order.billingAddress.stateOrProvince} ${order.billingAddress.postalCode}<br>
      ${order.billingAddress.countryCode}
    </div>
    <div class="box">
      <strong>Shipped To:</strong><br>
      ${order.shippingAddress.recipientName}<br>
      ${order.shippingAddress.streetLine1}<br>
      ${order.shippingAddress.city}, ${order.shippingAddress.stateOrProvince} ${order.shippingAddress.postalCode}<br>
      ${order.shippingAddress.countryCode}
    </div>
  </div>

  <table>
    <thead>
      <tr>
        <th>SKU</th>
        <th>Product Description</th>
        <th style="text-align: center;">Qty</th>
        <th style="text-align: right;">Unit Price</th>
        <th style="text-align: right;">Total</th>
      </tr>
    </thead>
    <tbody>
      ${itemsHtml}
    </tbody>
  </table>

  <div class="summary">
    <table class="summary-table">
      <tr>
        <td>Subtotal:</td>
        <td style="text-align: right;">$${(order.subtotalAmount.amount / 100).toFixed(2)}</td>
      </tr>
      <tr>
        <td>Sales Tax:</td>
        <td style="text-align: right;">$${(order.taxAmount.amount / 100).toFixed(2)}</td>
      </tr>
      <tr>
        <td>Shipping & Freight:</td>
        <td style="text-align: right;">$${(order.shippingFeeAmount.amount / 100).toFixed(2)}</td>
      </tr>
      <tr>
        <td>Promotions & Discounts:</td>
        <td style="text-align: right; color: #e53e3e;">-$${(order.discountAmount.amount / 100).toFixed(2)}</td>
      </tr>
      <tr class="total-row">
        <td>Total Due:</td>
        <td style="text-align: right;">$${(order.totalAmount.amount / 100).toFixed(2)} ${order.totalAmount.currency}</td>
      </tr>
    </table>
  </div>
</body>
</html>`;
  }
}
