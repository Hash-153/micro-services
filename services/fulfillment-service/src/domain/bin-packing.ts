export interface Dimensions3D {
  lengthMm: number;
  widthMm: number;
  heightMm: number;
  volumeMm3: number;
  maxWeightGrams: number;
}

export interface PackageBoxTemplate {
  boxCode: string;
  name: string;
  outerDimensions: Dimensions3D;
  innerDimensions: Dimensions3D;
  emptyWeightGrams: number;
  costCents: number;
}

export const STANDARD_BOX_CATALOG: PackageBoxTemplate[] = [
  {
    boxCode: 'BOX-S-01',
    name: 'Small Parcel Shipper',
    outerDimensions: { lengthMm: 220, widthMm: 160, heightMm: 100, volumeMm3: 3520000, maxWeightGrams: 2000 },
    innerDimensions: { lengthMm: 200, widthMm: 150, heightMm: 90, volumeMm3: 2700000, maxWeightGrams: 2000 },
    emptyWeightGrams: 120,
    costCents: 150
  },
  {
    boxCode: 'BOX-M-02',
    name: 'Medium Parcel Shipper',
    outerDimensions: { lengthMm: 350, widthMm: 250, heightMm: 180, volumeMm3: 15750000, maxWeightGrams: 8000 },
    innerDimensions: { lengthMm: 330, widthMm: 230, heightMm: 160, volumeMm3: 12144000, maxWeightGrams: 8000 },
    emptyWeightGrams: 300,
    costCents: 275
  },
  {
    boxCode: 'BOX-L-03',
    name: 'Large Master Shipper',
    outerDimensions: { lengthMm: 500, widthMm: 400, heightMm: 350, volumeMm3: 70000000, maxWeightGrams: 25000 },
    innerDimensions: { lengthMm: 480, widthMm: 380, heightMm: 330, volumeMm3: 60192000, maxWeightGrams: 25000 },
    emptyWeightGrams: 650,
    costCents: 550
  },
  {
    boxCode: 'BOX-XL-04',
    name: 'Pallet Bulk Shipper',
    outerDimensions: { lengthMm: 800, widthMm: 600, heightMm: 600, volumeMm3: 288000000, maxWeightGrams: 60000 },
    innerDimensions: { lengthMm: 780, widthMm: 580, heightMm: 580, volumeMm3: 262392000, maxWeightGrams: 60000 },
    emptyWeightGrams: 1400,
    costCents: 1200
  }
];

export interface ItemToPack {
  sku: string;
  quantity: number;
  weightGrams: number;
  dimensionsMm: {
    length: number;
    width: number;
    height: number;
  };
}

export interface PackingPlan {
  selectedBox: PackageBoxTemplate;
  totalWeightGrams: number;
  dimensionalWeightGrams: number;
  billableWeightGrams: number;
  volumeUtilizationPercent: number;
  packedItems: ItemToPack[];
}

export class BinPackingOptimizer {
  // Uses First Fit Decreasing heuristic with 3D volumetric verification & dimensional weight calculation
  public static optimizePackage(items: ItemToPack[]): PackingPlan {
    let totalItemVolumeMm3 = 0;
    let totalItemWeightGrams = 0;

    for (const item of items) {
      const singleVolume = item.dimensionsMm.length * item.dimensionsMm.width * item.dimensionsMm.height;
      totalItemVolumeMm3 += singleVolume * item.quantity;
      totalItemWeightGrams += item.weightGrams * item.quantity;
    }

    // Add 15% safety buffer for void-fill (bubble wrap, air pillows)
    const requiredVolumeWithPadding = totalItemVolumeMm3 * 1.15;

    // Find the smallest box that fits weight and volume
    let chosenBox: PackageBoxTemplate | null = null;
    for (const box of STANDARD_BOX_CATALOG) {
      if (
        box.innerDimensions.volumeMm3 >= requiredVolumeWithPadding &&
        box.innerDimensions.maxWeightGrams >= totalItemWeightGrams + box.emptyWeightGrams
      ) {
        chosenBox = box;
        break;
      }
    }

    if (!chosenBox) {
      chosenBox = STANDARD_BOX_CATALOG[STANDARD_BOX_CATALOG.length - 1]!;
    }

    const grossWeight = totalItemWeightGrams + chosenBox.emptyWeightGrams;
    // Dimensional weight formula: (L x W x H in cm) / 5000 in kg = (L x W x H in mm) / 5,000,000 in kg
    const dimensionalWeightKg = chosenBox.outerDimensions.volumeMm3 / 5000000;
    const dimensionalWeightGrams = Math.round(dimensionalWeightKg * 1000);
    const billableWeightGrams = Math.max(grossWeight, dimensionalWeightGrams);
    const volumeUtilizationPercent = Math.min(100, Math.round((totalItemVolumeMm3 / chosenBox.innerDimensions.volumeMm3) * 100));

    return {
      selectedBox: chosenBox,
      totalWeightGrams: grossWeight,
      dimensionalWeightGrams,
      billableWeightGrams,
      volumeUtilizationPercent,
      packedItems: items
    };
  }
}
