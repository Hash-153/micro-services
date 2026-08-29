import { Dimensions3D } from '@novacommerce/core-types';

export interface PackagingBoxDefinition {
  boxId: string;
  name: string;
  dimensionsMm: Dimensions3D;
  tareWeightGrams: number;
  maxWeightGrams: number;
  costCents: number;
}

export const STANDARD_PACKAGING_BOXES: PackagingBoxDefinition[] = [
  { boxId: 'BOX-SMALL', name: 'Small Mailer Box', dimensionsMm: { length: 200, width: 150, height: 100 }, tareWeightGrams: 120, maxWeightGrams: 3000, costCents: 65 },
  { boxId: 'BOX-MEDIUM', name: 'Standard Medium Carton', dimensionsMm: { length: 350, width: 250, height: 180 }, tareWeightGrams: 280, maxWeightGrams: 10000, costCents: 110 },
  { boxId: 'BOX-LARGE', name: 'Large Master Carton', dimensionsMm: { length: 500, width: 400, height: 300 }, tareWeightGrams: 550, maxWeightGrams: 25000, costCents: 185 },
  { boxId: 'BOX-XLARGE', name: 'Extra Large Heavy Freight Box', dimensionsMm: { length: 800, width: 600, height: 500 }, tareWeightGrams: 1200, maxWeightGrams: 45000, costCents: 340 }
];

export class CartonizationSelector {
  public static selectBestBox(requiredLengthMm: number, requiredWidthMm: number, requiredHeightMm: number, totalWeightGrams: number): PackagingBoxDefinition | null {
    // Sort boxes by smallest volume that satisfies constraints
    const sorted = [...STANDARD_PACKAGING_BOXES].sort((a, b) => {
      const volA = a.dimensionsMm.length * a.dimensionsMm.width * a.dimensionsMm.height;
      const volB = b.dimensionsMm.length * b.dimensionsMm.width * b.dimensionsMm.height;
      return volA - volB;
    });

    for (const box of sorted) {
      const dims = [box.dimensionsMm.length, box.dimensionsMm.width, box.dimensionsMm.height].sort((a, b) => b - a);
      const req = [requiredLengthMm, requiredWidthMm, requiredHeightMm].sort((a, b) => b - a);

      if (dims[0] >= req[0] && dims[1] >= req[1] && dims[2] >= req[2] && box.maxWeightGrams >= totalWeightGrams) {
        return box;
      }
    }

    return null; // Requires custom crating or palletization
  }
}
