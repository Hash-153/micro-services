import { OrganizationEntity } from '@novacommerce/core-types';

export interface TierEntitlements {
  maxSeats: number;
  maxMonthlyOrders: number;
  hasCustomDomain: boolean;
  hasDedicatedSupport: boolean;
  hasAuditLogRetentionDays: number;
  hasSsoIntegration: boolean;
}

export class OrganizationLicensingEngine {
  private static readonly TIER_LIMITS: Record<string, TierEntitlements> = {
    FREE: { maxSeats: 3, maxMonthlyOrders: 100, hasCustomDomain: false, hasDedicatedSupport: false, hasAuditLogRetentionDays: 7, hasSsoIntegration: false },
    STARTER: { maxSeats: 10, maxMonthlyOrders: 1000, hasCustomDomain: true, hasDedicatedSupport: false, hasAuditLogRetentionDays: 30, hasSsoIntegration: false },
    PRO: { maxSeats: 25, maxMonthlyOrders: 10000, hasCustomDomain: true, hasDedicatedSupport: true, hasAuditLogRetentionDays: 90, hasSsoIntegration: false },
    ENTERPRISE: { maxSeats: 500, maxMonthlyOrders: 1000000, hasCustomDomain: true, hasDedicatedSupport: true, hasAuditLogRetentionDays: 365, hasSsoIntegration: true }
  };

  public static getEntitlements(tier: OrganizationEntity['tier']): TierEntitlements {
    return this.TIER_LIMITS[tier] || this.TIER_LIMITS.PRO;
  }

  public static canAddSeat(org: OrganizationEntity, currentSeatCount: number): { allowed: boolean; reason?: string } {
    const entitlements = this.getEntitlements(org.tier);
    if (currentSeatCount >= entitlements.maxSeats) {
      return {
        allowed: false,
        reason: `Organization seat limit (${entitlements.maxSeats}) reached for ${org.tier} tier. Please upgrade organization plan.`
      };
    }
    return { allowed: true };
  }
}
