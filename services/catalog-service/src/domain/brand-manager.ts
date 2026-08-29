export interface BrandEntity {
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
