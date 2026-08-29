import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_quasar_modules():
    print("Generating comprehensive Quantum Quasar Modules...")

    # 1. Payment Level 3 Line Item Commodity Code Classifier
    write_file("services/payment-service/src/domain/commodity-code-classifier.ts", """export interface CommodityCodeMapping {
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
""")

    # 2. Inventory Dynamic Reorder Safety Stock Buffer Calculator
    write_file("services/inventory-service/src/domain/safety-stock-buffer-calculator.ts", """export interface SkuDemandDistribution {
  sku: string;
  averageDailySales: number;
  salesStandardDeviation: number;
  leadTimeDays: number;
  leadTimeStandardDeviation: number;
  serviceFactorZ: number; // 1.65 for 95%, 2.33 for 99%
}

export class SafetyStockBufferCalculator {
  public static calculateBuffer(dist: SkuDemandDistribution): { safetyStockUnits: number; bufferExplanation: string } {
    // Formula: SS = Z * sqrt( (LT * sigma_D^2) + (D^2 * sigma_LT^2) )
    const term1 = dist.leadTimeDays * Math.pow(dist.salesStandardDeviation, 2);
    const term2 = Math.pow(dist.averageDailySales, 2) * Math.pow(dist.leadTimeStandardDeviation, 2);
    const combinedStdDev = Math.sqrt(term1 + term2);
    const safetyStock = Math.ceil(dist.serviceFactorZ * combinedStdDev);

    return {
      safetyStockUnits: Math.max(1, safetyStock),
      bufferExplanation: `Safety stock calculated with Z=${dist.serviceFactorZ} over LT=${dist.leadTimeDays}d (+/-${dist.leadTimeStandardDeviation}d)`
    };
  }
}
""")

    print("Quantum quasar modules generated.")

if __name__ == "__main__":
    generate_quantum_quasar_modules()
