export class TariffHealthProbe {
  public static checkHealth(totalMappedCategories: number, totalPlatformCategories: number): { isHealthy: boolean; coveragePercentage: number } {
    const coverage = totalPlatformCategories > 0
      ? (totalMappedCategories / totalPlatformCategories) * 100
      : 100;

    return {
      isHealthy: coverage >= 95.0,
      coveragePercentage: Math.round(coverage * 10) / 10
    };
  }
}
