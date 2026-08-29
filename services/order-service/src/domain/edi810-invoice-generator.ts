import { OrderEntity } from '@novacommerce/core-types';

export class Edi810InvoiceGenerator {
  public static generateEdi810(order: OrderEntity, invoiceNumber: string, senderId: string = 'NOVACOMMERCE', receiverId: string = 'ENTERPRISEBUYER'): string {
    const now = new Date();
    const dateStr = now.toISOString().slice(2, 10).replace(/-/g, '');
    const timeStr = now.toTimeString().slice(0, 5).replace(/:/g, '');
    const controlNumber = Math.floor(100000 + Math.random() * 900000).toString();

    const segments: string[] = [
      `ISA*00*          *00*          *ZZ*${senderId.padEnd(15, ' ')}*ZZ*${receiverId.padEnd(15, ' ')}*${dateStr}*${timeStr}*U*00401*${controlNumber}*0*P*>~`,
      `GS*IN*${senderId}*${receiverId}*${dateStr}*${timeStr}*1*X*004010~`,
      `ST*810*0001~`,
      `BIG*${dateStr}*${invoiceNumber}*${dateStr}*${order.orderNumber}~`,
      `CUR*SE*${order.totalAmount.currency}~`,
      `N1*BT*${order.shippingAddress.recipientName}~`,
      `N3*${order.shippingAddress.streetLine1}~`,
      `N4*${order.shippingAddress.city}*${order.shippingAddress.stateOrProvince}*${order.shippingAddress.postalCode}*${order.shippingAddress.countryCode}~`,
      `ITD*01*3*1.0**10*30~` // Terms: 1% 10 Net 30
    ];

    let lineIndex = 1;
    for (const item of order.items) {
      const unitCost = (item.unitPrice.amount / 100).toFixed(2);
      segments.push(`IT1*${lineIndex}*${item.quantity}*EA*${unitCost}**VP*${item.sku}*IN*${item.productId}~`);
      segments.push(`PID*F****${item.productName.slice(0, 80)}~`);
      lineIndex++;
    }

    const totalCost = (order.totalAmount.amount / 100).toFixed(2);
    segments.push(`TDS*${(order.totalAmount.amount).toString()}~`);
    segments.push(`CAD*T***${order.shippingAddress.countryCode}~`);
    segments.push(`CTT*${order.items.length}~`);
    segments.push(`SE*${segments.length - 2}*0001~`);
    segments.push(`GE*1*1~`);
    segments.push(`IEA*1*${controlNumber}~`);

    return segments.join('\n');
  }
}
