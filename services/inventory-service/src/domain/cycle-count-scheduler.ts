export type AbcClassification = 'A' | 'B' | 'C';

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
