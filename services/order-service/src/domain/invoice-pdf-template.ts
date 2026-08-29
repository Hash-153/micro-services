import { OrderEntity } from '@novacommerce/core-types';

export class InvoicePdfTemplate {
  public static render(order: OrderEntity): string {
    const formattedDate = new Date(order.createdAt).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    const itemRows = order.items
      .map(
        (it, idx) => `
      <tr>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0;">${idx + 1}</td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0;">
          <strong>${it.productName}</strong><br/>
          <span style="font-size: 12px; color: #64748b;">SKU: ${it.sku}</span>
        </td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: center;">${it.quantity}</td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: right;">$${(it.unitPrice.amount / 100).toFixed(2)}</td>
        <td style="padding: 12px; border-bottom: 1px solid #e2e8f0; text-align: right; font-weight: bold;">$${((it.unitPrice.amount * it.quantity) / 100).toFixed(2)}</td>
      </tr>`
      )
      .join('');

    return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Invoice #${order.orderNumber}</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; margin: 0; padding: 40px; }
    .invoice-box { max-width: 800px; margin: auto; border: 1px solid #e2e8f0; border-radius: 8px; padding: 32px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .header { display: flex; justify-content: space-between; border-bottom: 2px solid #3b82f6; padding-bottom: 20px; margin-bottom: 24px; }
    .brand { font-size: 24px; font-weight: 800; color: #1e40af; }
    .invoice-title { font-size: 28px; font-weight: 700; color: #0f172a; text-align: right; }
    .addresses { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 32px; }
    .address-card { background: #f8fafc; padding: 16px; border-radius: 6px; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 32px; }
    th { background: #f1f5f9; padding: 12px; text-align: left; font-size: 13px; text-transform: uppercase; color: #475569; }
    .totals { width: 300px; margin-left: auto; }
    .total-row { display: flex; justify-content: space-between; padding: 6px 0; }
    .grand-total { border-top: 2px solid #0f172a; padding-top: 8px; font-size: 18px; font-weight: 800; color: #0f172a; }
  </style>
</head>
<body>
  <div class="invoice-box">
    <div class="header">
      <div>
        <div class="brand">NovaCommerce Enterprise</div>
        <div style="color: #64748b; font-size: 13px; margin-top: 4px;">Cloud Distributed Commerce Engine</div>
      </div>
      <div>
        <div class="invoice-title">INVOICE</div>
        <div style="color: #64748b; font-size: 14px;">Invoice #: ${order.orderNumber}</div>
        <div style="color: #64748b; font-size: 14px;">Date: ${formattedDate}</div>
      </div>
    </div>

    <div class="addresses">
      <div class="address-card">
        <strong style="color: #334155; font-size: 14px;">Billed To:</strong><br/>
        <strong>${order.billingAddress.recipientName}</strong><br/>
        ${order.billingAddress.streetLine1}<br/>
        ${order.billingAddress.city}, ${order.billingAddress.stateOrProvince} ${order.billingAddress.postalCode}<br/>
        ${order.billingAddress.countryCode}
      </div>
      <div class="address-card">
        <strong style="color: #334155; font-size: 14px;">Shipped To:</strong><br/>
        <strong>${order.shippingAddress.recipientName}</strong><br/>
        ${order.shippingAddress.streetLine1}<br/>
        ${order.shippingAddress.city}, ${order.shippingAddress.stateOrProvince} ${order.shippingAddress.postalCode}<br/>
        ${order.shippingAddress.countryCode}
      </div>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width: 40px;">#</th>
          <th>Description</th>
          <th style="text-align: center; width: 60px;">Qty</th>
          <th style="text-align: right; width: 100px;">Unit Price</th>
          <th style="text-align: right; width: 100px;">Total</th>
        </tr>
      </thead>
      <tbody>
        ${itemRows}
      </tbody>
    </table>

    <div class="totals">
      <div class="total-row"><span>Subtotal:</span><span>$${(order.subtotalAmount.amount / 100).toFixed(2)}</span></div>
      <div class="total-row"><span>Estimated Tax:</span><span>$${(order.taxAmount.amount / 100).toFixed(2)}</span></div>
      <div class="total-row"><span>Shipping & Handling:</span><span>$${(order.shippingFeeAmount.amount / 100).toFixed(2)}</span></div>
      ${order.discountAmount.amount > 0 ? `<div class="total-row" style="color: #16a34a;"><span>Discounts Applied:</span><span>-$${(order.discountAmount.amount / 100).toFixed(2)}</span></div>` : ''}
      <div class="total-row grand-total"><span>Total Due:</span><span>$${(order.totalAmount.amount / 100).toFixed(2)} ${order.totalAmount.currency}</span></div>
    </div>
  </div>
</body>
</html>`;
  }
}
