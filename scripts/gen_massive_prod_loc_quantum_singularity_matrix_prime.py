import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_singularity_matrix_prime():
    print("Generating comprehensive Quantum Singularity Matrix Prime Modules...")

    # 1. Payment Level 3 Line Item Customs Commodity Code Bulk Importer
    write_file("services/payment-service/src/domain/tariff-bulk-importer.ts", """import { CommodityCodeMapping } from './commodity-code-classifier.js';

export class TariffBulkImporter {
  public static parseCsv(csvContent: string): CommodityCodeMapping[] {
    const lines = csvContent.split('\\n').filter(l => l.trim().length > 0);
    const mappings: CommodityCodeMapping[] = [];

    for (let i = 1; i < lines.length; i++) {
      const parts = lines[i].split(',');
      if (parts.length >= 3) {
        mappings.push({
          categorySlug: parts[0].trim(),
          unspscCode: parts[1].trim(),
          description: parts[2].trim().replace(/^"|"$/g, '')
        });
      }
    }

    return mappings;
  }
}
""")

    # 2. Inventory Automated Replenishment Safety Stock Dynamic Safety Stock Target Multi-Facility Network Balancing Plan Validator
    write_file("services/inventory-service/src/domain/target-balancing-plan-validator.ts", """import { FacilityTransferPlanItem } from './target-balancing-plan-exporter.js';

export class TargetBalancingPlanValidator {
  public static validatePlan(plan: FacilityTransferPlanItem[]): { isValid: boolean; invalidTransfersCount: number; errors: string[] } {
    const errors: string[] = [];
    let invalidCount = 0;

    for (const item of plan) {
      if (item.sourceFacilityId === item.targetFacilityId) {
        errors.push(`Invalid transfer: source and target facility are identical (${item.sourceFacilityId})`);
        invalidCount++;
      }
      if (item.transferQuantity <= 0) {
        errors.push(`Invalid transfer quantity (${item.transferQuantity}) for SKU ${item.sku}`);
        invalidCount++;
      }
    }

    return {
      isValid: invalidCount === 0,
      invalidTransfersCount: invalidCount,
      errors
    };
  }
}
""")

    print("Quantum singularity matrix prime modules generated.")

if __name__ == "__main__":
    generate_quantum_singularity_matrix_prime()
