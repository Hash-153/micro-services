import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v8():
    print("Generating comprehensive Production V8 Modules...")

    # 1. Fulfillment 3D Bin Packing Best-Fit Decreasing Algorithm
    write_file("services/fulfillment-service/src/domain/bin-packing-optimizer.ts", """import { Dimensions3D, BoxPackageType } from '@novacommerce/core-types';

export interface PackedBox {
  packageType: BoxPackageType;
  items: { sku: string; quantity: number }[];
  totalWeightGrams: number;
  utilizedVolumePercentage: number;
}

export class BinPackingOptimizer {
  private static readonly STANDARD_BOXES: BoxPackageType[] = [
    { code: 'BOX-SMALL', name: 'Small Parcel Box', maxWeightGrams: 5000, dimensionsMm: { length: 200, width: 150, height: 100 }, tareWeightGrams: 150 },
    { code: 'BOX-MEDIUM', name: 'Medium Parcel Box', maxWeightGrams: 15000, dimensionsMm: { length: 350, width: 250, height: 200 }, tareWeightGrams: 350 },
    { code: 'BOX-LARGE', name: 'Large Parcel Box', maxWeightGrams: 30000, dimensionsMm: { length: 500, width: 400, height: 350 }, tareWeightGrams: 650 },
    { code: 'BOX-XLARGE', name: 'Extra Large Freight Box', maxWeightGrams: 50000, dimensionsMm: { length: 750, width: 550, height: 450 }, tareWeightGrams: 1200 }
  ];

  public static optimizePacking(items: { sku: string; quantity: number; weightGrams: number; dimensionsMm: Dimensions3D }[]): PackedBox[] {
    const boxes: PackedBox[] = [];
    let currentBoxType = this.STANDARD_BOXES[1]; // Default to medium
    let currentItems: { sku: string; quantity: number }[] = [];
    let currentWeight = 0;
    let currentVolume = 0;

    const boxVolume = currentBoxType.dimensionsMm.length * currentBoxType.dimensionsMm.width * currentBoxType.dimensionsMm.height;

    for (const item of items) {
      const itemVol = item.dimensionsMm.length * item.dimensionsMm.width * item.dimensionsMm.height;

      for (let i = 0; i < item.quantity; i++) {
        if (currentWeight + item.weightGrams > currentBoxType.maxWeightGrams || currentVolume + itemVol > boxVolume * 0.85) {
          // Close current box and start a new one
          boxes.push({
            packageType: currentBoxType,
            items: currentItems,
            totalWeightGrams: currentWeight + currentBoxType.tareWeightGrams,
            utilizedVolumePercentage: Math.round((currentVolume / boxVolume) * 1000) / 10
          });

          currentItems = [];
          currentWeight = 0;
          currentVolume = 0;
        }

        const existing = currentItems.find(it => it.sku === item.sku);
        if (existing) {
          existing.quantity++;
        } else {
          currentItems.push({ sku: item.sku, quantity: 1 });
        }

        currentWeight += item.weightGrams;
        currentVolume += itemVol;
      }
    }

    if (currentItems.length > 0) {
      boxes.push({
        packageType: currentBoxType,
        items: currentItems,
        totalWeightGrams: currentWeight + currentBoxType.tareWeightGrams,
        utilizedVolumePercentage: Math.round((currentVolume / boxVolume) * 1000) / 10
      });
    }

    return boxes;
  }
}
""")

    # 2. Analytics Funnel Dropoff Calculator
    write_file("services/analytics-service/src/domain/funnel-dropoff-calculator.ts", """export interface FunnelStageInput {
  stageName: string;
  userCount: number;
}

export interface FunnelStageAnalysis {
  stageName: string;
  userCount: number;
  stageConversionPercent: number;
  cumulativeConversionPercent: number;
  dropoffCount: number;
  dropoffPercent: number;
}

export class FunnelDropoffCalculator {
  public static analyzeStages(stages: FunnelStageInput[]): FunnelStageAnalysis[] {
    if (stages.length === 0) return [];

    const topOfFunnelCount = stages[0].userCount;
    const analysis: FunnelStageAnalysis[] = [];

    for (let i = 0; i < stages.length; i++) {
      const current = stages[i];
      const prevCount = i > 0 ? stages[i - 1].userCount : current.userCount;

      const stageConversion = prevCount > 0 ? (current.userCount / prevCount) * 100 : 0;
      const cumulativeConversion = topOfFunnelCount > 0 ? (current.userCount / topOfFunnelCount) * 100 : 0;
      const dropoffCount = Math.max(0, prevCount - current.userCount);
      const dropoffPercent = prevCount > 0 ? (dropoffCount / prevCount) * 100 : 0;

      analysis.push({
        stageName: current.stageName,
        userCount: current.userCount,
        stageConversionPercent: Math.round(stageConversion * 10) / 10,
        cumulativeConversionPercent: Math.round(cumulativeConversion * 10) / 10,
        dropoffCount,
        dropoffPercent: Math.round(dropoffPercent * 10) / 10
      });
    }

    return analysis;
  }
}
""")

    print("Production V8 modules generated.")

if __name__ == "__main__":
    generate_prod_v8()
