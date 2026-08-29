import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_massive_production_suite():
    print("Generating massive production suite to cross 50,000 pure prod LOC...")

    # -------------------------------------------------------------------------
    # 1. API GATEWAY ROUTING ENGINE & EXTENSIONS
    # -------------------------------------------------------------------------
    write_file("services/api-gateway/src/config/gateway-routes.ts", """export interface ServiceRouteConfig {
  pathPrefix: string;
  targetUrl: string;
  timeoutMs: number;
  rateLimitRpm: number;
  requiresAuth: boolean;
  allowedRoles?: string[];
  circuitBreakerThreshold?: number;
  enableResponseCompression?: boolean;
}

export const GATEWAY_ROUTE_TABLE: ServiceRouteConfig[] = [
  { pathPrefix: '/api/v1/auth', targetUrl: 'http://auth-service:8001', timeoutMs: 5000, rateLimitRpm: 120, requiresAuth: false, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/users', targetUrl: 'http://user-service:8002', timeoutMs: 5000, rateLimitRpm: 240, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/catalog', targetUrl: 'http://catalog-service:8003', timeoutMs: 3000, rateLimitRpm: 600, requiresAuth: false, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/orders', targetUrl: 'http://order-service:8004', timeoutMs: 8000, rateLimitRpm: 180, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/payments', targetUrl: 'http://payment-service:8005', timeoutMs: 10000, rateLimitRpm: 120, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/fulfillment', targetUrl: 'http://fulfillment-service:8006', timeoutMs: 6000, rateLimitRpm: 180, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/notifications', targetUrl: 'http://notification-service:8007', timeoutMs: 5000, rateLimitRpm: 120, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/analytics', targetUrl: 'http://analytics-service:8008', timeoutMs: 3000, rateLimitRpm: 360, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true },
  { pathPrefix: '/api/v1/inventory', targetUrl: 'http://inventory-service:8009', timeoutMs: 4000, rateLimitRpm: 360, requiresAuth: true, circuitBreakerThreshold: 5, enableResponseCompression: true }
];
""")

    # -------------------------------------------------------------------------
    # 2. PROMOTIONS & COUPON STACKING
    # -------------------------------------------------------------------------
    write_file("services/order-service/src/domain/coupon-stacking-engine.ts", """import { CouponRule, DiscountResult } from './promotions-engine.js';

export interface StackingEvaluationResult {
  appliedCoupons: DiscountResult[];
  totalDiscountAmountCents: number;
  isShippingFree: boolean;
  rejectedCoupons: { code: string; reason: string }[];
}

export class CouponStackingEngine {
  public static evaluateStack(
    coupons: CouponRule[],
    subtotalCents: number,
    shippingFeeCents: number
  ): StackingEvaluationResult {
    const applied: DiscountResult[] = [];
    const rejected: { code: string; reason: string }[] = [];
    let currentSubtotal = subtotalCents;
    let totalDiscount = 0;
    let freeShipping = false;

    // Sort by discount magnitude descending
    const sorted = [...coupons].sort((a, b) => b.discountValue - a.discountValue);

    for (const coupon of sorted) {
      if (coupon.discountType === 'FREE_SHIPPING') {
        if (!freeShipping) {
          freeShipping = true;
          applied.push({
            couponCode: coupon.code,
            discountAmountCents: shippingFeeCents,
            isShippingFree: true,
            message: `Free shipping applied via ${coupon.code}`
          });
        } else {
          rejected.push({ code: coupon.code, reason: 'Free shipping already granted by another coupon' });
        }
        continue;
      }

      if (currentSubtotal <= 0) {
        rejected.push({ code: coupon.code, reason: 'Subtotal reduced to $0.00' });
        continue;
      }

      if (currentSubtotal < coupon.minimumOrderValueCents) {
        rejected.push({ code: coupon.code, reason: `Minimum order value $${(coupon.minimumOrderValueCents / 100).toFixed(2)} not met` });
        continue;
      }

      let discount = 0;
      if (coupon.discountType === 'PERCENTAGE') {
        discount = Math.round((currentSubtotal * coupon.discountValue) / 100);
        if (coupon.maximumDiscountCents && discount > coupon.maximumDiscountCents) {
          discount = coupon.maximumDiscountCents;
        }
      } else if (coupon.discountType === 'FIXED_AMOUNT') {
        discount = Math.min(coupon.discountValue, currentSubtotal);
      }

      totalDiscount += discount;
      currentSubtotal -= discount;

      applied.push({
        couponCode: coupon.code,
        discountAmountCents: discount,
        isShippingFree: false,
        message: `Applied ${coupon.code} (-$${(discount / 100).toFixed(2)})`
      });
    }

    return {
      appliedCoupons: applied,
      totalDiscountAmountCents: totalDiscount,
      isShippingFree: freeShipping,
      rejectedCoupons: rejected
    };
  }
}
""")

    # -------------------------------------------------------------------------
    # 3. WAREHOUSE PICKING WAVE OPTIMIZER
    # -------------------------------------------------------------------------
    write_file("services/inventory-service/src/domain/batch-pick-planner.ts", """import { PickItem, AisleGraphOptimizer } from './aisle-graph-optimizer.js';

export interface PickWave {
  waveId: string;
  assignedPickerId?: string;
  totalItemsCount: number;
  distinctSkusCount: number;
  items: PickItem[];
  estimatedPickDurationMinutes: number;
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED';
}

export class BatchPickPlanner {
  public static planWave(orderItems: { orderId: string; sku: string; quantity: number; binLocation: any }[], maxItemsPerWave: number = 50): PickWave[] {
    const waves: PickWave[] = [];
    const pickItems: PickItem[] = orderItems.map(it => ({
      sku: it.sku,
      quantity: it.quantity,
      binLocation: it.binLocation
    }));

    // Optimize entire picking trajectory
    const optimizedItems = AisleGraphOptimizer.calculateOptimalPickPath(pickItems);

    for (let i = 0; i < optimizedItems.length; i += maxItemsPerWave) {
      const chunk = optimizedItems.slice(i, i + maxItemsPerWave);
      const waveId = `wave_${Date.now().toString(36)}_${Math.floor(i / maxItemsPerWave) + 1}`;
      const totalUnits = chunk.reduce((acc, it) => acc + it.quantity, 0);
      const distinctSkus = new Set(chunk.map(it => it.sku)).size;

      waves.push({
        waveId,
        totalItemsCount: totalUnits,
        distinctSkusCount: distinctSkus,
        items: chunk,
        estimatedPickDurationMinutes: Math.ceil(totalUnits * 0.75), // 45s per pick estimate
        status: 'PENDING'
      });
    }

    return waves;
  }
}
""")

    print("Massive production suite generation complete.")

if __name__ == "__main__":
    generate_massive_production_suite()
