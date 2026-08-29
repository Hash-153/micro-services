import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_enterprise_domain_modules():
    print("Generating comprehensive Enterprise Domain Modules...")

    # 1. Double Entry Ledger Transaction Builder
    write_file("services/payment-service/src/domain/ledger-transaction-builder.ts", """import { LedgerLineEntity, Currency } from '@novacommerce/core-types';

export class LedgerTransactionBuilder {
  private journalEntryId: string;
  private lines: LedgerLineEntity[] = [];

  constructor(journalEntryId: string = crypto.randomUUID()) {
    this.journalEntryId = journalEntryId;
  }

  public debit(accountId: string, amountCents: number, memo?: string): this {
    if (amountCents <= 0) throw new Error('Debit amount must be strictly positive');
    this.lines.push({
      id: crypto.randomUUID(),
      journalEntryId: this.journalEntryId,
      accountId,
      entryType: 'DEBIT',
      amount: amountCents,
      memo
    });
    return this;
  }

  public credit(accountId: string, amountCents: number, memo?: string): this {
    if (amountCents <= 0) throw new Error('Credit amount must be strictly positive');
    this.lines.push({
      id: crypto.randomUUID(),
      journalEntryId: this.journalEntryId,
      accountId,
      entryType: 'CREDIT',
      amount: amountCents,
      memo
    });
    return this;
  }

  public build(): { journalEntryId: string; lines: LedgerLineEntity[]; totalDebitCents: number; totalCreditCents: number } {
    const totalDebit = this.lines.filter(l => l.entryType === 'DEBIT').reduce((acc, l) => acc + l.amount, 0);
    const totalCredit = this.lines.filter(l => l.entryType === 'CREDIT').reduce((acc, l) => acc + l.amount, 0);

    if (totalDebit !== totalCredit) {
      throw new Error(`Unbalanced double-entry journal entry: total debits ($${(totalDebit / 100).toFixed(2)}) must equal total credits ($${(totalCredit / 100).toFixed(2)})`);
    }

    return {
      journalEntryId: this.journalEntryId,
      lines: this.lines,
      totalDebitCents: totalDebit,
      totalCreditCents: totalCredit
    };
  }
}
""")

    # 2. Haversine Nearest Warehouse Router
    write_file("services/inventory-service/src/domain/haversine-router.ts", """import { WarehouseEntity } from '@novacommerce/core-types';

export interface GeoCoordinate {
  latitude: number;
  longitude: number;
}

export class HaversineWarehouseRouter {
  public static calculateDistanceKm(coordA: GeoCoordinate, coordB: GeoCoordinate): number {
    const R = 6371; // Earth radius in kilometers
    const dLat = this.toRadians(coordB.latitude - coordA.latitude);
    const dLon = this.toRadians(coordB.longitude - coordA.longitude);

    const lat1 = this.toRadians(coordA.latitude);
    const lat2 = this.toRadians(coordB.latitude);

    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return Math.round(R * c * 10) / 10;
  }

  public static findNearestWarehouses(
    destination: GeoCoordinate,
    warehouses: WarehouseEntity[],
    limit: number = 3
  ): { warehouse: WarehouseEntity; distanceKm: number }[] {
    return warehouses
      .filter(w => w.isActive)
      .map(warehouse => ({
        warehouse,
        distanceKm: this.calculateDistanceKm(destination, {
          latitude: warehouse.latitude,
          longitude: warehouse.longitude
        })
      }))
      .sort((a, b) => a.distanceKm - b.distanceKm)
      .slice(0, limit);
  }

  private static toRadians(degrees: number): number {
    return (degrees * Math.PI) / 180;
  }
}
""")

    print("Enterprise domain modules generated.")

if __name__ == "__main__":
    generate_enterprise_domain_modules()
