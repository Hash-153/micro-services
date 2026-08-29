import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v22():
    print("Generating comprehensive Production V22 Modules...")

    # 1. Payment Multi-Party Escrow Release Engine
    write_file("services/payment-service/src/domain/escrow-release-engine.ts", """import { Money, Currency } from '@novacommerce/core-types';

export interface EscrowHoldRecord {
  escrowId: string;
  orderId: string;
  sellerId: string;
  buyerId: string;
  holdAmountCents: number;
  currency: Currency;
  status: 'HELD' | 'RELEASED_TO_SELLER' | 'REFUNDED_TO_BUYER' | 'SPLIT_DISPUTE';
  autoReleaseDate: Date;
  deliveryConfirmedDate?: Date;
}

export class EscrowReleaseEngine {
  public static canReleaseToSeller(escrow: EscrowHoldRecord, currentDate: Date = new Date()): boolean {
    if (escrow.status !== 'HELD') return false;

    // Release if delivery confirmed + 48 hours cooling off
    if (escrow.deliveryConfirmedDate) {
      const coolingOffEnd = new Date(escrow.deliveryConfirmedDate.getTime() + 48 * 3600000);
      if (currentDate >= coolingOffEnd) return true;
    }

    // Release if autoReleaseDate reached without active dispute
    return currentDate >= escrow.autoReleaseDate;
  }
}
""")

    # 2. Inventory SKU Barcode & RFID Matrix Generator
    write_file("services/inventory-service/src/domain/barcode-rfid-generator.ts", """export class BarcodeRfidGenerator {
  public static generateEan13(skuCode: string, countryPrefix: string = '084'): string {
    const rawDigits = (countryPrefix + skuCode.replace(/[^0-9]/g, '').padEnd(9, '0')).slice(0, 12);

    let sum = 0;
    for (let i = 0; i < 12; i++) {
      const digit = parseInt(rawDigits.charAt(i), 10);
      sum += i % 2 === 0 ? digit : digit * 3;
    }

    const checkDigit = (10 - (sum % 10)) % 10;
    return `${rawDigits}${checkDigit}`;
  }

  public static generateEpcRfidTag(sku: string, serialNumber: number): string {
    const headerHex = '30'; // SGTIN-96
    const filter = '3';     // Item level
    const partition = '5';
    const skuHash = Buffer.from(sku).toString('hex').slice(0, 14).padEnd(14, '0');
    const serialHex = serialNumber.toString(16).padStart(8, '0');

    return `urn:epc:tag:sgtin-96:${filter}.${skuHash}.${serialHex}`;
  }
}
""")

    print("Production V22 modules generated.")

if __name__ == "__main__":
    generate_prod_v22()
