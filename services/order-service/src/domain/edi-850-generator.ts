import { OrderEntity } from '@novacommerce/core-types';

export class Edi850Generator {
  public static generateEdi850(order: OrderEntity, senderId: string = 'NOVACOMMERCE', receiverId: string = 'SUPPLIER_EDI'): string {
    const dateStr = new Date(order.createdAt).toISOString().slice(2, 10).replace(/-/g, '');
    const timeStr = new Date(order.createdAt).toTimeString().slice(0, 5).replace(/:/g, '');

    const segments: string[] = [
      `ISA*00*          *00*          *ZZ*${senderId.padEnd(15, ' ')}*ZZ*${receiverId.padEnd(15, ' ')}*${dateStr}*${timeStr}*U*00401*000000001*0*P*>~`,
      `GS*PO*${senderId}*${receiverId}*${dateStr}*${timeStr}*1*X*004010~`,
      `ST*850*0001~`,
      `BEG*00*SA*${order.orderNumber}**${dateStr}~`,
      `REF*IA*${order.userId}~`,
      `DTM*002*${dateStr}~`,
      `N1*ST*${order.shippingAddress.recipientName}*92*${order.shippingAddress.id || 'LOC1'}~`,
      `N3*${order.shippingAddress.streetLine1}~`,
      `N4*${order.shippingAddress.city}*${order.shippingAddress.stateOrProvince}*${order.shippingAddress.postalCode}*${order.shippingAddress.countryCode}~`
    ];

    let lineIndex = 1;
    for (const item of order.items) {
      segments.push(`PO1*${lineIndex}*${item.quantity}*EA*${(item.unitPrice.amount / 100).toFixed(2)}*PE*VP*${item.sku}~`);
      segments.push(`PID*F****${item.productName}~`);
      lineIndex++;
    }

    const totalQty = order.items.reduce((acc, it) => acc + it.quantity, 0);
    segments.push(`CTT*${order.items.length}*${totalQty}~`);
    segments.push(`SE*${segments.length - 2}*0001~`);
    segments.push(`GE*1*1~`);
    segments.push(`IEA*1*000000001~`);

    return segments.join('\n');
  }
}
