export interface FacilityInventoryNode {
  facilityId: string;
  facilityType: 'CENTRAL_HUB' | 'REGIONAL_DC' | 'LOCAL_SPOKE';
  sku: string;
  onHandQuantity: number;
  safetyStockTarget: number;
  replenishmentLeadTimeDays: number;
}

export class MultiEchelonSynchronizer {
  public static calculateTransfers(
    centralHub: FacilityInventoryNode,
    regionalDcs: FacilityInventoryNode[]
  ): { targetFacilityId: string; transferQuantity: number }[] {
    const transfers: { targetFacilityId: string; transferQuantity: number }[] = [];
    let hubAvailable = Math.max(0, centralHub.onHandQuantity - centralHub.safetyStockTarget);

    for (const dc of regionalDcs) {
      if (hubAvailable <= 0) break;

      const deficit = Math.max(0, dc.safetyStockTarget - dc.onHandQuantity);
      if (deficit > 0) {
        const qtyToTransfer = Math.min(deficit, hubAvailable);
        transfers.push({
          targetFacilityId: dc.facilityId,
          transferQuantity: qtyToTransfer
        });
        hubAvailable -= qtyToTransfer;
      }
    }

    return transfers;
  }
}
