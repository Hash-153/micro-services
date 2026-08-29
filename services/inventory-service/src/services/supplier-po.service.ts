import { Logger } from '@novacommerce/core-logger';

export interface SupplierPurchaseOrder {
  poNumber: string;
  supplierId: string;
  supplierName: string;
  targetWarehouseId: string;
  items: { sku: string; quantity: number; unitCostCents: number }[];
  totalCostCents: number;
  status: 'DRAFT' | 'ISSUED' | 'CONFIRMED' | 'IN_TRANSIT' | 'RECEIVED' | 'CANCELLED';
  expectedDeliveryDate: Date;
  createdAt: Date;
}

export class SupplierPoService {
  private logger: Logger;
  private purchaseOrders: Map<string, SupplierPurchaseOrder> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public async createPurchaseOrder(
    supplierId: string,
    supplierName: string,
    targetWarehouseId: string,
    items: { sku: string; quantity: number; unitCostCents: number }[],
    leadTimeDays: number = 7
  ): Promise<SupplierPurchaseOrder> {
    const poNumber = `PO-${Date.now().toString(36).toUpperCase()}`;
    const totalCostCents = items.reduce((acc, it) => acc + it.quantity * it.unitCostCents, 0);
    const expectedDeliveryDate = new Date(Date.now() + leadTimeDays * 24 * 60 * 60 * 1000);

    const po: SupplierPurchaseOrder = {
      poNumber,
      supplierId,
      supplierName,
      targetWarehouseId,
      items,
      totalCostCents,
      status: 'ISSUED',
      expectedDeliveryDate,
      createdAt: new Date()
    };

    this.purchaseOrders.set(poNumber, po);
    this.logger.info(`Supplier purchase order created: ${poNumber} ($${(totalCostCents / 100).toFixed(2)}) for warehouse ${targetWarehouseId}`);
    return po;
  }

  public async getPurchaseOrder(poNumber: string): Promise<SupplierPurchaseOrder | null> {
    return this.purchaseOrders.get(poNumber) || null;
  }
}
