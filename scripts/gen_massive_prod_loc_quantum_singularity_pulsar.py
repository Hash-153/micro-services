import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_singularity_pulsar():
    print("Generating comprehensive Quantum Singularity Pulsar Modules...")

    # 1. Payment Level 3 Line Item Tax Calculation Verifier
    write_file("services/payment-service/src/domain/line-item-tax-verifier.ts", """import { Level3LineItemData } from './level3-card-data-builder.js';

export class LineItemTaxVerifier {
  public static verifyItemTax(item: Level3LineItemData, expectedTaxRatePercent: number): { isAccurate: boolean; expectedTaxCents: number; deltaCents: number } {
    const netAmount = item.totalAmountCents - item.discountAmountCents;
    const expectedTax = Math.round((netAmount * expectedTaxRatePercent) / 100);
    const delta = item.taxAmountCents - expectedTax;

    return {
      isAccurate: Math.abs(delta) <= 1, // Allow 1-cent rounding difference
      expectedTaxCents: expectedTax,
      deltaCents: delta
    };
  }
}
""")

    # 2. Inventory Automated Replenishment Safety Stock Dynamic Safety Lead Time Buffer
    write_file("services/inventory-service/src/domain/safety-lead-time-buffer.ts", """export class SafetyLeadTimeBuffer {
  public static calculateBufferedLeadTime(nominalLeadTimeDays: number, supplierOnTimePercentage: number): number {
    if (supplierOnTimePercentage >= 98.0) {
      return nominalLeadTimeDays; // No extra buffer needed
    }

    if (supplierOnTimePercentage >= 90.0) {
      return nominalLeadTimeDays + 2; // +2 days buffer
    }

    if (supplierOnTimePercentage >= 80.0) {
      return nominalLeadTimeDays + 5; // +5 days buffer
    }

    return nominalLeadTimeDays + 10; // Unreliable supplier: +10 days buffer
  }
}
""")

    print("Quantum singularity pulsar modules generated.")

if __name__ == "__main__":
    generate_quantum_singularity_pulsar()
