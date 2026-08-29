import { OrderEntity } from '@novacommerce/core-types';

export class InvoiceGenerator {
  public static generateHtmlInvoice(order: OrderEntity, companyName: string = 'NovaCommerce Inc.'): string {
    const itemRows = order.items
      .map(
        item => `<tr>
        <td>${item.sku}</td>
        <td>${item.productName}</td>
        <td>${item.quantity}</td>
        <td>$${(item.unitPrice.amount / 100).toFixed(2)}</td>
        <td>$${(item.total.amount / 100).toFixed(2)}</td>
      </tr>`
      )
      .join('\n');

    return `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Invoice #${order.orderNumber}</title>
  <style>
    body { font-family: Arial, sans-serif; padding: 40px; color: #333; }
    .header { border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }
    .invoice-title { font-size: 28px; font-weight: bold; color: #1a365d; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
    th { background: #f7fafc; }
    .totals { margin-top: 30px; text-align: right; font-size: 16px; }
    .total-due { font-size: 22px; font-weight: bold; color: #2b6cb0; }
  </style>
</head>
<body>
  <div class="header">
    <div class="invoice-title">COMMERCIAL INVOICE</div>
    <p><strong>${companyName}</strong><br>100 Enterprise Way, Suite 400, Wilmington, DE 19801</p>
    <p><strong>Invoice Number:</strong> INV-${order.orderNumber}<br>
       <strong>Order Date:</strong> ${order.createdAt.toISOString()}<br>
       <strong>Customer ID:</strong> ${order.userId}</p>
  </div>

  <table>
    <thead>
      <tr>
        <th>SKU</th>
        <th>Description</th>
        <th>Qty</th>
        <th>Unit Price</th>
        <th>Total Amount</th>
      </tr>
    </thead>
    <tbody>
      ${itemRows}
    </tbody>
  </table>

  <div class="totals">
    <p>Subtotal: $${(order.subtotalAmount.amount / 100).toFixed(2)}</p>
    <p>Tax: $${(order.taxAmount.amount / 100).toFixed(2)}</p>
    <p>Shipping & Handling: $${(order.shippingFeeAmount.amount / 100).toFixed(2)}</p>
    <p class="total-due">Total Amount Paid: $${(order.totalAmount.amount / 100).toFixed(2)} ${order.totalAmount.currency}</p>
  </div>
</body>
</html>`;
  }
}
