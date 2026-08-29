export interface HazmatMaterialSpec {
  unNumber: string; // e.g. "UN3481" for Lithium ion batteries packed with equipment
  properShippingName: string;
  hazardClass: string; // e.g. "Class 9"
  packingGroup: 'I' | 'II' | 'III';
  maxNetQuantityGrams: number;
}

export class HazmatComplianceChecker {
  private static readonly REGULATED_MATERIALS: Map<string, HazmatMaterialSpec> = new Map([
    ['UN3480', { unNumber: 'UN3480', properShippingName: 'Lithium Ion Batteries', hazardClass: '9', packingGroup: 'II', maxNetQuantityGrams: 5000 }],
    ['UN3481', { unNumber: 'UN3481', properShippingName: 'Lithium Ion Batteries Packed with Equipment', hazardClass: '9', packingGroup: 'II', maxNetQuantityGrams: 10000 }],
    ['UN1993', { unNumber: 'UN1993', properShippingName: 'Flammable Liquids N.O.S. (Cleaning Solvents)', hazardClass: '3', packingGroup: 'III', maxNetQuantityGrams: 1000 }]
  ]);

  public static checkCompliance(unNumber: string, netWeightGrams: number): { isAllowed: boolean; reason?: string; requiredLabel: string } {
    const spec = this.REGULATED_MATERIALS.get(unNumber);
    if (!spec) {
      return { isAllowed: false, reason: `Unknown or uncertified hazmat material: ${unNumber}`, requiredLabel: 'NONE' };
    }

    if (netWeightGrams > spec.maxNetQuantityGrams) {
      return {
        isAllowed: false,
        reason: `Net quantity (${netWeightGrams}g) exceeds allowable limit for ${unNumber} (${spec.maxNetQuantityGrams}g)`,
        requiredLabel: `HAZMAT_CLASS_${spec.hazardClass.replace(/\s/g, '_')}`
      };
    }

    return {
      isAllowed: true,
      requiredLabel: `HAZMAT_CLASS_${spec.hazardClass.replace(/\s/g, '_')}_LABEL`
    };
  }
}
