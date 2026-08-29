export interface FunnelStageInput {
  stageName: string;
  userCount: number;
}

export interface FunnelStageAnalysis {
  stageName: string;
  userCount: number;
  stageConversionPercent: number;
  cumulativeConversionPercent: number;
  dropoffCount: number;
  dropoffPercent: number;
}

export class FunnelDropoffCalculator {
  public static analyzeStages(stages: FunnelStageInput[]): FunnelStageAnalysis[] {
    if (stages.length === 0) return [];

    const topOfFunnelCount = stages[0].userCount;
    const analysis: FunnelStageAnalysis[] = [];

    for (let i = 0; i < stages.length; i++) {
      const current = stages[i];
      const prevCount = i > 0 ? stages[i - 1].userCount : current.userCount;

      const stageConversion = prevCount > 0 ? (current.userCount / prevCount) * 100 : 0;
      const cumulativeConversion = topOfFunnelCount > 0 ? (current.userCount / topOfFunnelCount) * 100 : 0;
      const dropoffCount = Math.max(0, prevCount - current.userCount);
      const dropoffPercent = prevCount > 0 ? (dropoffCount / prevCount) * 100 : 0;

      analysis.push({
        stageName: current.stageName,
        userCount: current.userCount,
        stageConversionPercent: Math.round(stageConversion * 10) / 10,
        cumulativeConversionPercent: Math.round(cumulativeConversion * 10) / 10,
        dropoffCount,
        dropoffPercent: Math.round(dropoffPercent * 10) / 10
      });
    }

    return analysis;
  }
}
