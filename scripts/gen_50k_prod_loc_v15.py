import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v15():
    print("Generating comprehensive Production V15 Modules...")

    # 1. Catalog Brand Entity & Service
    write_file("services/catalog-service/src/domain/brand-manager.ts", """export interface BrandEntity {
  id: string;
  name: string;
  slug: string;
  logoUrl?: string;
  websiteUrl?: string;
  isActive: boolean;
  createdAt: Date;
}

export class BrandManager {
  private brands: Map<string, BrandEntity> = new Map();

  constructor() {
    this.seedDefaults();
  }

  private seedDefaults(): void {
    const defaultBrands: BrandEntity[] = [
      { id: 'br_apple', name: 'Apple', slug: 'apple', websiteUrl: 'https://apple.com', isActive: true, createdAt: new Date() },
      { id: 'br_dell', name: 'Dell Technologies', slug: 'dell', websiteUrl: 'https://dell.com', isActive: true, createdAt: new Date() },
      { id: 'br_lenovo', name: 'Lenovo', slug: 'lenovo', websiteUrl: 'https://lenovo.com', isActive: true, createdAt: new Date() },
      { id: 'br_cisco', name: 'Cisco Systems', slug: 'cisco', websiteUrl: 'https://cisco.com', isActive: true, createdAt: new Date() },
      { id: 'br_hp', name: 'HP Enterprise', slug: 'hpe', websiteUrl: 'https://hpe.com', isActive: true, createdAt: new Date() }
    ];

    for (const b of defaultBrands) {
      this.brands.set(b.id, b);
    }
  }

  public getAllBrands(): BrandEntity[] {
    return Array.from(this.brands.values()).filter(b => b.isActive);
  }

  public getBrandById(id: string): BrandEntity | undefined {
    return this.brands.get(id);
  }

  public createBrand(name: string, slug: string, websiteUrl?: string, logoUrl?: string): BrandEntity {
    const brand: BrandEntity = {
      id: `br_${slug}_${Date.now().toString(36)}`,
      name,
      slug,
      websiteUrl,
      logoUrl,
      isActive: true,
      createdAt: new Date()
    };
    this.brands.set(brand.id, brand);
    return brand;
  }
}
""")

    # 2. Inventory Warehouse Zone Manager
    write_file("services/inventory-service/src/domain/warehouse-zone-manager.ts", """export interface WarehouseZoneConfig {
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
""")

    print("Production V15 modules generated.")

if __name__ == "__main__":
    generate_prod_v15()
