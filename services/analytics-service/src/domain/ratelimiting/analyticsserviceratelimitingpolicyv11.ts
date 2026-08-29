export interface RateQuotaTierV11 {
  tierName: 'ANONYMOUS' | 'STANDARD_USER' | 'ENTERPRISE_API' | 'INTERNAL_MESH';
  maxRequestsPerMinute: number;
  burstCapacity: number;
  costPerRequest: number;
}

export const RATE_QUOTA_TIERS_V11: Record<string, RateQuotaTierV11> = {
  ANONYMOUS: { tierName: 'ANONYMOUS', maxRequestsPerMinute: 60, burstCapacity: 10, costPerRequest: 1 },
  STANDARD_USER: { tierName: 'STANDARD_USER', maxRequestsPerMinute: 300, burstCapacity: 50, costPerRequest: 1 },
  ENTERPRISE_API: { tierName: 'ENTERPRISE_API', maxRequestsPerMinute: 3000, burstCapacity: 500, costPerRequest: 1 },
  INTERNAL_MESH: { tierName: 'INTERNAL_MESH', maxRequestsPerMinute: 60000, burstCapacity: 5000, costPerRequest: 0 }
};

export class AnalyticsServiceRateLimitingPolicyV11 {
  public static getQuota(tier: keyof typeof RATE_QUOTA_TIERS_V11): RateQuotaTierV11 {
    return RATE_QUOTA_TIERS_V11[tier] || RATE_QUOTA_TIERS_V11.STANDARD_USER;
  }

  public static isAllowed(currentMinuteCount: number, tier: keyof typeof RATE_QUOTA_TIERS_V11): { allowed: boolean; remaining: number; resetSeconds: number } {
    const quota = this.getQuota(tier);
    const remaining = Math.max(0, quota.maxRequestsPerMinute - currentMinuteCount);
    const now = new Date();
    const resetSeconds = 60 - now.getSeconds();

    return {
      allowed: currentMinuteCount <= quota.maxRequestsPerMinute,
      remaining,
      resetSeconds
    };
  }
}
