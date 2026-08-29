export interface CommodityCodeMapping {
  categorySlug: string;
  unspscCode: string; // United Nations Standard Products and Services Code
  description: string;
}

export const COMMODITY_CODE_REGISTRY: CommodityCodeMapping[] = [
  { categorySlug: 'rack-servers', unspscCode: '43211501', description: 'Computer servers and server mainframes' },
  { categorySlug: 'blade-servers', unspscCode: '43211502', description: 'Blade server architecture units' },
  { categorySlug: 'gpu-servers', unspscCode: '43211509', description: 'GPU hardware accelerator compute nodes' },
  { categorySlug: 'all-flash-san', unspscCode: '43211706', description: 'Network attached storage array all-flash systems' },
  { categorySlug: 'spine-switches', unspscCode: '43222612', description: 'Network switches and director class switches' },
  { categorySlug: 'enterprise-firewalls', unspscCode: '43222501', description: 'Network security firewalls and appliances' },
  { categorySlug: 'modular-ups', unspscCode: '39121011', description: 'Uninterruptible power supply UPS online systems' }
];

export class CommodityCodeClassifier {
  public static resolveUnspsc(categorySlug: string): string {
    const match = COMMODITY_CODE_REGISTRY.find(m => m.categorySlug === categorySlug);
    return match ? match.unspscCode : '43211500'; // Default computer hardware
  }
}
