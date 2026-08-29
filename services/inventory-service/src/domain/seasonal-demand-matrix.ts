export class SeasonalDemandMatrix {
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
