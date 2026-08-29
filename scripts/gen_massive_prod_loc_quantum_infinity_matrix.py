import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_infinity_matrix_modules():
    print("Generating comprehensive Quantum Infinity Matrix Modules...")

    # 1. Payment Level 3 Line Item Invoice Exporter
    write_file("services/payment-service/src/domain/commercial-invoice-exporter.ts", """import { Level3ProcessingPayload } from './level3-card-data-builder.js';

export class CommercialInvoiceExporter {
  public static exportCsv(payload: Level3ProcessingPayload): string {
    const headers = ['CommodityCode', 'Description', 'ProductCode', 'Quantity', 'UOM', 'UnitCostCents', 'TotalCents'];
    const rows = payload.lineItems.map(it =>
      [it.itemCommodityCode, `"${it.itemDescription}"`, it.productCode, it.quantity, it.unitOfMeasure, it.unitCostCents, it.totalAmountCents].join(',')
    );

    return [headers.join(','), ...rows].join('\\n');
  }
}
""")

    # 2. Inventory Automated Cycle Count Discrepancy Analyzer
    write_file("services/inventory-service/src/domain/cycle-count-discrepancy-analyzer.ts", """export interface BinCountComparison {
  binId: string;
  sku: string;
  systemQuantity: number;
  physicalCountQuantity: number;
  unitCostCents: number;
}

export class CycleCountDiscrepancyAnalyzer {
  public static analyzeDiscrepancy(item: BinCountComparison): {
    varianceUnits: number;
    varianceCents: number;
    variancePercentage: number;
    severity: 'NORMAL' | 'WARNING' | 'CRITICAL';
    requiresSupervisorApproval: boolean;
  } {
    const varianceUnits = item.physicalCountQuantity - item.systemQuantity;
    const varianceCents = varianceUnits * item.unitCostCents;
    const variancePercentage = item.systemQuantity > 0
      ? (Math.abs(varianceUnits) / item.systemQuantity) * 100
      : (item.physicalCountQuantity > 0 ? 100 : 0);

    let severity: 'NORMAL' | 'WARNING' | 'CRITICAL' = 'NORMAL';
    if (Math.abs(varianceCents) >= 50000 || variancePercentage >= 20) {
      severity = 'CRITICAL';
    } else if (Math.abs(varianceCents) >= 10000 || variancePercentage >= 5) {
      severity = 'WARNING';
    }

    return {
      varianceUnits,
      varianceCents,
      variancePercentage: Math.round(variancePercentage * 10) / 10,
      severity,
      requiresSupervisorApproval: severity === 'CRITICAL'
    };
  }
}
""")

    print("Quantum infinity matrix modules generated.")

if __name__ == "__main__":
    generate_quantum_infinity_matrix_modules()
