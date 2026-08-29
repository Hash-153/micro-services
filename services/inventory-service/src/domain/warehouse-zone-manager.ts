export interface WarehouseZoneConfig {
  zoneId: string;
  warehouseId: string;
  zoneType: 'RECEIVING' | 'STORAGE_BULK' | 'STORAGE_FORWARD_PICK' | 'PACKING' | 'SHIPPING_STAGING' | 'RETURNS_QUARANTINE';
  temperatureRangeCelsius?: { min: number; max: number };
  isActive: boolean;
}

export class WarehouseZoneManager {
  private zones: Map<string, WarehouseZoneConfig> = new Map();

  public registerZone(config: WarehouseZoneConfig): void {
    this.zones.set(config.zoneId, config);
  }

  public getZonesByWarehouse(warehouseId: string): WarehouseZoneConfig[] {
    return Array.from(this.zones.values()).filter(z => z.warehouseId === warehouseId && z.isActive);
  }

  public getForwardPickZones(warehouseId: string): WarehouseZoneConfig[] {
    return this.getZonesByWarehouse(warehouseId).filter(z => z.zoneType === 'STORAGE_FORWARD_PICK');
  }
}
