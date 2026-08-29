export interface SeasonalMonthMultiplier {
  monthIndex: number; // 1-12
  demandMultiplier: number;
}

export class SeasonalFactorEvaluator {
  private static readonly SEASONAL_CURVE: SeasonalMonthMultiplier[] = [
    { monthIndex: 1, demandMultiplier: 0.85 },  // Jan - Post-holiday slump
    { monthIndex: 2, demandMultiplier: 0.90 },  // Feb
    { monthIndex: 3, demandMultiplier: 1.00 },  // Mar
    { monthIndex: 4, demandMultiplier: 1.05 },  // Apr
    { monthIndex: 5, demandMultiplier: 1.10 },  // May
    { monthIndex: 6, demandMultiplier: 1.00 },  // Jun
    { monthIndex: 7, demandMultiplier: 0.95 },  // Jul
    { monthIndex: 8, demandMultiplier: 1.05 },  // Aug - Back to school
    { monthIndex: 9, demandMultiplier: 1.15 },  // Sep
    { monthIndex: 10, demandMultiplier: 1.25 }, // Oct - Holiday inventory ramp
    { monthIndex: 11, demandMultiplier: 1.60 }, // Nov - Black Friday / Cyber Monday
    { monthIndex: 12, demandMultiplier: 1.50 }  // Dec - Holiday peak
  ];

  public static getMultiplier(monthIndex: number = new Date().getMonth() + 1): number {
    const entry = this.SEASONAL_CURVE.find(s => s.monthIndex === monthIndex);
    return entry ? entry.demandMultiplier : 1.0;
  }
}
