import { AbcXyzClass } from './abc-xyz-matrix-classifier.js';

export interface SkuOrderPolicy {
  matrixClass: AbcXyzClass;
  replenishmentMethod: 'CONTINUOUS_REVIEW_ROP' | 'PERIODIC_REVIEW_P' | 'KANBAN_JIT' | 'MANUAL_SPOT_ORDER';
  recommendedReviewIntervalDays: number;
  safetyStockMultiplier: number;
}

export class AbcXyzPolicyGenerator {
  private static readonly POLICIES: Record<AbcXyzClass, SkuOrderPolicy> = {
    AX: { matrixClass: 'AX', replenishmentMethod: 'KANBAN_JIT', recommendedReviewIntervalDays: 3, safetyStockMultiplier: 1.0 },
    AY: { matrixClass: 'AY', replenishmentMethod: 'CONTINUOUS_REVIEW_ROP', recommendedReviewIntervalDays: 7, safetyStockMultiplier: 1.2 },
    AZ: { matrixClass: 'AZ', replenishmentMethod: 'CONTINUOUS_REVIEW_ROP', recommendedReviewIntervalDays: 7, safetyStockMultiplier: 1.8 },
    BX: { matrixClass: 'BX', replenishmentMethod: 'PERIODIC_REVIEW_P', recommendedReviewIntervalDays: 14, safetyStockMultiplier: 1.1 },
    BY: { matrixClass: 'BY', replenishmentMethod: 'CONTINUOUS_REVIEW_ROP', recommendedReviewIntervalDays: 14, safetyStockMultiplier: 1.3 },
    BZ: { matrixClass: 'BZ', replenishmentMethod: 'CONTINUOUS_REVIEW_ROP', recommendedReviewIntervalDays: 14, safetyStockMultiplier: 1.6 },
    CX: { matrixClass: 'CX', replenishmentMethod: 'PERIODIC_REVIEW_P', recommendedReviewIntervalDays: 30, safetyStockMultiplier: 1.0 },
    CY: { matrixClass: 'CY', replenishmentMethod: 'PERIODIC_REVIEW_P', recommendedReviewIntervalDays: 45, safetyStockMultiplier: 1.2 },
    CZ: { matrixClass: 'CZ', replenishmentMethod: 'MANUAL_SPOT_ORDER', recommendedReviewIntervalDays: 60, safetyStockMultiplier: 1.0 }
  };

  public static getPolicy(matrixClass: AbcXyzClass): SkuOrderPolicy {
    return this.POLICIES[matrixClass] || this.POLICIES.BY;
  }
}
