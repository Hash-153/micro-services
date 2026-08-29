import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v16():
    print("Generating comprehensive Production V16 Modules...")

    # 1. API Gateway Edge Compression Negotiator
    write_file("services/api-gateway/src/middleware/compression-negotiator.ts", """import { Request, Response, NextFunction } from 'express';

export class CompressionNegotiator {
  public static middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      const acceptEncoding = req.headers['accept-encoding'] || '';

      if (typeof acceptEncoding === 'string') {
        if (acceptEncoding.includes('br')) {
          res.setHeader('X-Selected-Compression', 'brotli');
        } else if (acceptEncoding.includes('gzip')) {
          res.setHeader('X-Selected-Compression', 'gzip');
        } else if (acceptEncoding.includes('deflate')) {
          res.setHeader('X-Selected-Compression', 'deflate');
        }
      }

      next();
    };
  }
}
""")

    # 2. Analytics User Lifetime Value (LTV) Calculator
    write_file("services/analytics-service/src/domain/ltv-calculator.ts", """import { OrderEntity } from '@novacommerce/core-types';

export interface UserLtvMetrics {
  userId: string;
  totalOrdersCount: number;
  totalSpendCents: number;
  averageOrderValueCents: number;
  daysSinceFirstOrder: number;
  daysSinceLastOrder: number;
  purchaseFrequencyDays: number;
  predictedNext90DaySpendCents: number;
}

export class LtvCalculator {
  public static calculateLtv(userId: string, orders: OrderEntity[]): UserLtvMetrics {
    const userOrders = orders
      .filter(o => o.userId === userId && o.status !== 'CANCELLED')
      .sort((a, b) => new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime());

    if (userOrders.length === 0) {
      return {
        userId,
        totalOrdersCount: 0,
        totalSpendCents: 0,
        averageOrderValueCents: 0,
        daysSinceFirstOrder: 0,
        daysSinceLastOrder: 0,
        purchaseFrequencyDays: 0,
        predictedNext90DaySpendCents: 0
      };
    }

    const totalSpend = userOrders.reduce((acc, o) => acc + o.totalAmount.amount, 0);
    const aov = Math.round(totalSpend / userOrders.length);

    const firstOrderTime = new Date(userOrders[0].createdAt).getTime();
    const lastOrderTime = new Date(userOrders[userOrders.length - 1].createdAt).getTime();
    const now = Date.now();

    const daysSinceFirst = Math.max(1, Math.floor((now - firstOrderTime) / (1000 * 60 * 60 * 24)));
    const daysSinceLast = Math.max(0, Math.floor((now - lastOrderTime) / (1000 * 60 * 60 * 24)));

    const frequency = Math.round((daysSinceFirst / userOrders.length) * 10) / 10;
    const predictedSpend = frequency > 0 ? Math.round((90 / frequency) * aov) : 0;

    return {
      userId,
      totalOrdersCount: userOrders.length,
      totalSpendCents: totalSpend,
      averageOrderValueCents: aov,
      daysSinceFirstOrder: daysSinceFirst,
      daysSinceLastOrder: daysSinceLast,
      purchaseFrequencyDays: frequency,
      predictedNext90DaySpendCents: predictedSpend
    };
  }
}
""")

    print("Production V16 modules generated.")

if __name__ == "__main__":
    generate_prod_v16()
