import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_singularity_vortex():
    print("Generating comprehensive Quantum Singularity Vortex Modules...")

    # 1. Payment Level 3 Line Item Description Truncator & Sanitizer
    write_file("services/payment-service/src/domain/line-item-sanitizer.ts", """export class LineItemSanitizer {
  public static sanitizeDescription(rawDesc: string, maxLength: number = 26): string {
    const clean = rawDesc.replace(/[^a-zA-Z0-9\\s-_.]/g, '').trim();
    if (clean.length <= maxLength) return clean;
    return clean.slice(0, maxLength);
  }

  public static sanitizeProductCode(sku: string, maxLength: number = 12): string {
    const clean = sku.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
    return clean.slice(0, maxLength);
  }
}
""")

    # 2. Inventory Automated Replenishment Safety Stock Lead Time Variance Analyzer
    write_file("services/inventory-service/src/domain/lead-time-variance-analyzer.ts", """export interface SupplierDeliveryRecord {
  poNumber: string;
  expectedDate: Date;
  actualReceiptDate: Date;
  varianceDays: number;
}

export class LeadTimeVarianceAnalyzer {
  public static computeVariance(records: SupplierDeliveryRecord[]): { meanVarianceDays: number; standardDeviationDays: number; isUnreliable: boolean } {
    if (records.length === 0) return { meanVarianceDays: 0, standardDeviationDays: 0, isUnreliable: false };

    const variances = records.map(r => (r.actualReceiptDate.getTime() - r.expectedDate.getTime()) / 86400000);
    const mean = variances.reduce((a, b) => a + b, 0) / variances.length;
    const variance = variances.reduce((acc, v) => acc + Math.pow(v - mean, 2), 0) / variances.length;
    const stdDev = Math.sqrt(variance);

    return {
      meanVarianceDays: Math.round(mean * 10) / 10,
      standardDeviationDays: Math.round(stdDev * 10) / 10,
      isUnreliable: mean > 5 || stdDev > 3
    };
  }
}
""")

    print("Quantum singularity vortex modules generated.")

if __name__ == "__main__":
    generate_quantum_singularity_vortex()
