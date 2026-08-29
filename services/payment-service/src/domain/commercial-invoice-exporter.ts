import { Level3ProcessingPayload } from './level3-card-data-builder.js';

export class CommercialInvoiceExporter {
  public static exportCsv(payload: Level3ProcessingPayload): string {
    const headers = ['CommodityCode', 'Description', 'ProductCode', 'Quantity', 'UOM', 'UnitCostCents', 'TotalCents'];
    const rows = payload.lineItems.map(it =>
      [it.itemCommodityCode, `"${it.itemDescription}"`, it.productCode, it.quantity, it.unitOfMeasure, it.unitCostCents, it.totalAmountCents].join(',')
    );

    return [headers.join(','), ...rows].join('\n');
  }
}
