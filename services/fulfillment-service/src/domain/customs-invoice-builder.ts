import { OrderEntity, Currency } from '@novacommerce/core-types';

export interface CustomsLineItem {
  hsTariffCode: string;
  description: string;
  countryOfOrigin: string;
  quantity: number;
  unitValueCents: number;
  totalValueCents: number;
}

export interface CommercialCustomsInvoice {
  invoiceNumber: string;
  incoterm: 'DAP' | 'DDP' | 'FOB' | 'CIF';
  shipperTaxId: string;
  recipientTaxId?: string;
  items: CustomsLineItem[];
  declaredTotalCents: number;
  currency: Currency;
  exportReason: 'COMMERCIAL_SALE' | 'SAMPLE' | 'RETURN';
  declarationSignature: string;
}

export class CustomsInvoiceBuilder {
  public static buildInvoice(
    order: OrderEntity,
    shipperTaxId: string = 'US-EIN-9921004',
    incoterm: CommercialCustomsInvoice['incoterm'] = 'DDP'
  ): CommercialCustomsInvoice {
    const items: CustomsLineItem[] = order.items.map(it => ({
      hsTariffCode: '8471.30.01', // Data processing machines / computers
      description: it.productName,
      countryOfOrigin: 'US',
      quantity: it.quantity,
      unitValueCents: it.unitPrice.amount,
      totalValueCents: it.unitPrice.amount * it.quantity
    }));

    const declaredTotal = items.reduce((acc, it) => acc + it.totalValueCents, 0);

    return {
      invoiceNumber: `CI-${order.orderNumber}`,
      incoterm,
      shipperTaxId,
      items,
      declaredTotalCents: declaredTotal,
      currency: order.totalAmount.currency,
      exportReason: 'COMMERCIAL_SALE',
      declarationSignature: 'NovaCommerce Global Trade Compliance Officer'
    };
  }
}
