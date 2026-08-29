import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_singularity_matrix_core():
    print("Generating comprehensive Quantum Singularity Matrix Core Modules...")

    # 1. Payment Level 3 Line Item Customs Tariff Classification Validator
    write_file("services/payment-service/src/domain/tariff-classification-validator.ts", """export class TariffClassificationValidator {
  public static isValidUnspsc(code: string): boolean {
    // UNSPSC codes are exactly 8 digits
    return /^[0-9]{8}$/.test(code.replace(/\\./g, ''));
  }

  public static isValidHsCode(code: string): boolean {
    // HS codes have 6 to 10 digits
    const clean = code.replace(/[^0-9]/g, '');
    return clean.length >= 6 && clean.length <= 10;
  }
}
""")

    # 2. Inventory Automated Replenishment Safety Stock Dynamic Safety Stock Target Anomaly Detector
    write_file("services/inventory-service/src/domain/target-anomaly-detector.ts", """export class TargetAnomalyDetector {
  public static detectSpike(currentSafetyStock: number, newCalculatedSafetyStock: number, maxAllowedRatio: number = 3.0): { isAnomaly: boolean; ratio: number; alertMessage?: string } {
    if (currentSafetyStock <= 0) return { isAnomaly: false, ratio: 1.0 };

    const ratio = newCalculatedSafetyStock / currentSafetyStock;
    if (ratio >= maxAllowedRatio) {
      return {
        isAnomaly: true,
        ratio: Math.round(ratio * 10) / 10,
        alertMessage: `Safety stock sudden spike detected: proposed (${newCalculatedSafetyStock}) is ${(ratio).toFixed(1)}x current baseline (${currentSafetyStock})`
      };
    }

    return { isAnomaly: false, ratio: Math.round(ratio * 10) / 10 };
  }
}
""")

    print("Quantum singularity matrix core modules generated.")

if __name__ == "__main__":
    generate_quantum_singularity_matrix_core()
