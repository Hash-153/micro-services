import { OrderEntity } from '@novacommerce/core-types';

export interface Level3LineItemData {
  itemCommodityCode: string;
  itemDescription: string;
  productCode: string;
  quantity: number;
  unitOfMeasure: string;
  unitCostCents: number;
  totalAmountCents: number;
  taxAmountCents: number;
  discountAmountCents: number;
}

export interface Level3ProcessingPayload {
  summaryCommodityCode: string;
  customerVatRegistrationNumber?: string;
  dutyAmountCents: number;
  freightAmountCents: number;
  shipFromPostalCode: string;
  destinationPostalCode: string;
  destinationCountryCode: string;
  lineItems: Level3LineItemData[];
}

export class Level3CardDataBuilder {
  public static buildLevel3Data(order: OrderEntity, shipFromPostal: string = '94105'): Level3ProcessingPayload {
    const lineItems: Level3LineItemData[] = order.items.map(it => ({
      itemCommodityCode: '43211507', // Electronic hardware commodity code
      itemDescription: it.productName.slice(0, 26),
      productCode: it.sku.slice(0, 12),
      quantity: it.quantity,
      unitOfMeasure: 'EA',
      unitCostCents: it.unitPrice.amount,
      totalAmountCents: it.unitPrice.amount * it.quantity,
      taxAmountCents: 0,
      discountAmountCents: 0
    }));

    return {
      summaryCommodityCode: '43211500',
      dutyAmountCents: 0,
      freightAmountCents: order.shippingFeeAmount.amount,
      shipFromPostalCode: shipFromPostal,
      destinationPostalCode: order.shippingAddress.postalCode,
      destinationCountryCode: order.shippingAddress.countryCode,
      lineItems
    };
  }
}
