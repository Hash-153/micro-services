import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_quantum_hyperdrive_modules():
    print("Generating comprehensive Quantum Hyperdrive Modules...")

    # 1. Payment Level 3 Line Item Tax Identifier Formatter
    write_file("services/payment-service/src/domain/tax-identifier-formatter.ts", """export class TaxIdentifierFormatter {
  public static normalizeEin(rawEin: string): string {
    const digits = rawEin.replace(/[^0-9]/g, '');
    if (digits.length !== 9) return rawEin;
    return `${digits.slice(0, 2)}-${digits.slice(2)}`;
  }

  public static normalizeVat(rawVat: string): string {
    return rawVat.replace(/[^A-Za-z0-9]/g, '').toUpperCase();
  }
}
""")

    # 2. Inventory SKU Cross-Docking Decision Matrix
    write_file("services/inventory-service/src/domain/cross-dock-matrix.ts", """export interface InboundAsnItem {
  sku: string;
  quantity: number;
  asnNumber: string;
}

export interface OutboundBackorderDemand {
  sku: string;
  orderId: string;
  backorderQuantity: number;
  priorityScore: number;
}

export class CrossDockDecisionMatrix {
  public static planCrossDocking(
    inbound: InboundAsnItem[],
    backorders: OutboundBackorderDemand[]
  ): { sku: string; orderId: string; quantityToCrossDock: number }[] {
    const crossDocks: { sku: string; orderId: string; quantityToCrossDock: number }[] = [];

    for (const inItem of inbound) {
      let remainingInbound = inItem.quantity;
      const matchingBackorders = backorders
        .filter(b => b.sku === inItem.sku)
        .sort((a, b) => b.priorityScore - a.priorityScore);

      for (const bo of matchingBackorders) {
        if (remainingInbound <= 0) break;

        const dockQty = Math.min(remainingInbound, bo.backorderQuantity);
        crossDocks.push({
          sku: inItem.sku,
          orderId: bo.orderId,
          quantityToCrossDock: dockQty
        });

        remainingInbound -= dockQty;
        bo.backorderQuantity -= dockQty;
      }
    }

    return crossDocks;
  }
}
""")

    print("Quantum hyperdrive modules generated.")

if __name__ == "__main__":
    generate_quantum_hyperdrive_modules()
