import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v20():
    print("Generating comprehensive Production V20 Modules...")

    # 1. Payment Sub-Ledger Automatic Reclassification Engine
    write_file("services/payment-service/src/domain/ledger-reclassification.ts", """import { LedgerLineEntity, Currency } from '@novacommerce/core-types';

export interface ReclassificationEntry {
  originalLineId: string;
  fromAccountId: string;
  toAccountId: string;
  amountCents: number;
  reason: string;
  effectiveDate: Date;
}

export class LedgerReclassificationEngine {
  public static createReclassificationLines(
    entry: ReclassificationEntry,
    journalEntryId: string = crypto.randomUUID()
  ): LedgerLineEntity[] {
    return [
      // Credit original account to reverse
      {
        id: crypto.randomUUID(),
        journalEntryId,
        accountId: entry.fromAccountId,
        entryType: 'CREDIT',
        amount: entry.amountCents,
        memo: `Reclassification reversal: ${entry.reason}`
      },
      // Debit new target account
      {
        id: crypto.randomUUID(),
        journalEntryId,
        accountId: entry.toAccountId,
        entryType: 'DEBIT',
        amount: entry.amountCents,
        memo: `Reclassified into account: ${entry.reason}`
      }
    ];
  }
}
""")

    # 2. Inventory Safety Stock Seasonality Multipliers
    write_file("services/inventory-service/src/domain/seasonal-demand-matrix.ts", """export class SeasonalDemandMatrix {
  private static readonly MONTHLY_FACTORS: Record<number, number> = {
    0: 0.85,  // Jan (Post-holiday dip)
    1: 0.90,  // Feb
    2: 1.00,  // Mar
    3: 1.05,  // Apr
    4: 1.10,  // May
    5: 1.15,  // Jun
    6: 1.10,  // Jul
    7: 1.15,  // Aug (Back to school)
    8: 1.20,  // Sep
    9: 1.30,  // Oct (Holiday prep)
    10: 1.75, // Nov (Black Friday / Cyber Monday)
    11: 1.90  // Dec (Holiday peak)
  };

  public static getSeasonalityMultiplier(date: Date = new Date()): number {
    const month = date.getMonth();
    return this.MONTHLY_FACTORS[month] || 1.0;
  }

  public static adjustDemandForecast(baseDailyDemand: number, targetDate: Date): number {
    const multiplier = this.getSeasonalityMultiplier(targetDate);
    return Math.round(baseDailyDemand * multiplier * 10) / 10;
  }
}
""")

    print("Production V20 modules generated.")

if __name__ == "__main__":
    generate_prod_v20()
