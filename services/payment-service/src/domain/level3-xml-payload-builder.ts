import { Level3ProcessingPayload } from './level3-card-data-builder.js';

export class Level3XmlPayloadBuilder {
  public static buildXml(payload: Level3ProcessingPayload): string {
    const itemsXml = payload.lineItems.map(it => `
      <LineItem>
        <CommodityCode>${it.itemCommodityCode}</CommodityCode>
        <Description>${it.itemDescription}</Description>
        <ProductCode>${it.productCode}</ProductCode>
        <Quantity>${it.quantity}</Quantity>
        <UnitOfMeasure>${it.unitOfMeasure}</UnitOfMeasure>
        <UnitPrice>${(it.unitCostCents / 100).toFixed(2)}</UnitPrice>
        <TotalAmount>${(it.totalAmountCents / 100).toFixed(2)}</TotalAmount>
        <TaxAmount>${(it.taxAmountCents / 100).toFixed(2)}</TaxAmount>
        <DiscountAmount>${(it.discountAmountCents / 100).toFixed(2)}</DiscountAmount>
      </LineItem>`).join('');

    return `<?xml version="1.0" encoding="UTF-8"?>
<Level3Data>
  <SummaryCommodityCode>${payload.summaryCommodityCode}</SummaryCommodityCode>
  <FreightAmount>${(payload.freightAmountCents / 100).toFixed(2)}</FreightAmount>
  <DutyAmount>${(payload.dutyAmountCents / 100).toFixed(2)}</DutyAmount>
  <ShipFromPostalCode>${payload.shipFromPostalCode}</ShipFromPostalCode>
  <DestinationPostalCode>${payload.destinationPostalCode}</DestinationPostalCode>
  <DestinationCountryCode>${payload.destinationCountryCode}</DestinationCountryCode>
  <LineItems>${itemsXml}
  </LineItems>
</Level3Data>`;
  }
}
