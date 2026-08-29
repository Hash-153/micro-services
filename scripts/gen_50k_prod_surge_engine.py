import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_surge_engine():
    print("Generating comprehensive Production Surge Engine Modules...")

    # 1. Payment Merchant Settlement Schedule Calculator
    write_file("services/payment-service/src/domain/merchant-settlement-scheduler.ts", """export interface SettlementSchedule {
  merchantId: string;
  payoutFrequency: 'DAILY_ROLLING' | 'WEEKLY_FRIDAY' | 'MONTHLY_FIRST';
  rollingDaysDelay: number;
  nextPayoutDate: Date;
  cutoffTimeUtc: string;
}

export class MerchantSettlementScheduler {
  public static calculateNextPayout(schedule: SettlementSchedule, currentDate: Date = new Date()): Date {
    const nextDate = new Date(currentDate);

    if (schedule.payoutFrequency === 'DAILY_ROLLING') {
      nextDate.setDate(nextDate.getDate() + schedule.rollingDaysDelay);
      // If weekend, push to Monday
      if (nextDate.getDay() === 6) nextDate.setDate(nextDate.getDate() + 2);
      if (nextDate.getDay() === 0) nextDate.setDate(nextDate.getDate() + 1);
    } else if (schedule.payoutFrequency === 'WEEKLY_FRIDAY') {
      const daysUntilFriday = (5 - nextDate.getDay() + 7) % 7 || 7;
      nextDate.setDate(nextDate.getDate() + daysUntilFriday);
    } else if (schedule.payoutFrequency === 'MONTHLY_FIRST') {
      nextDate.setMonth(nextDate.getMonth() + 1);
      nextDate.setDate(1);
    }

    return nextDate;
  }
}
""")

    # 2. Inventory Automated Cycle Count Scheduler
    write_file("services/inventory-service/src/domain/cycle-count-scheduler.ts", """export type AbcClassification = 'A' | 'B' | 'C';

export interface AbcInventoryItem {
  sku: string;
  annualValueCents: number;
  classification: AbcClassification;
  countFrequencyDays: number;
  lastCountedDate: Date;
}

export class CycleCountScheduler {
  public static classifyAbc(items: { sku: string; annualValueCents: number; lastCountedDate: Date }[]): AbcInventoryItem[] {
    const sorted = [...items].sort((a, b) => b.annualValueCents - a.annualValueCents);
    const totalValue = sorted.reduce((acc, it) => acc + it.annualValueCents, 0);

    let cumulative = 0;
    return sorted.map(item => {
      cumulative += item.annualValueCents;
      const cumPct = totalValue > 0 ? (cumulative / totalValue) * 100 : 0;

      let classification: AbcClassification = 'C';
      let freqDays = 180; // C items: twice a year

      if (cumPct <= 70) {
        classification = 'A';
        freqDays = 30; // A items: monthly count
      } else if (cumPct <= 90) {
        classification = 'B';
        freqDays = 90; // B items: quarterly count
      }

      return {
        sku: item.sku,
        annualValueCents: item.annualValueCents,
        classification,
        countFrequencyDays: freqDays,
        lastCountedDate: item.lastCountedDate
      };
    });
  }
}
""")

    print("Production surge engine modules generated.")

if __name__ == "__main__":
    generate_prod_surge_engine()
