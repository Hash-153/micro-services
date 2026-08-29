import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_v25():
    print("Generating comprehensive Production V25 Modules...")

    # 1. API Gateway Web Application Firewall (WAF) Rule Evaluator
    write_file("services/api-gateway/src/middleware/waf-rule-evaluator.ts", """import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export class WafRuleEvaluator {
  private static readonly SQLI_REGEX = /(\\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|TRUNCATE)\\b|--|\\/\\*|;)/i;
  private static readonly XSS_REGEX = /(<script\\b|javascript:|onerror=|onload=|eval\\()/i;
  private static readonly PATH_TRAVERSAL_REGEX = /(\\.\\.\\/|\\.\\.\\\\)/;

  public static middleware(logger: Logger) {
    return (req: Request, res: Response, next: NextFunction) => {
      const url = req.originalUrl || req.url;
      const bodyStr = req.body ? JSON.stringify(req.body) : '';

      // Check URL and Body against WAF signatures
      if (this.PATH_TRAVERSAL_REGEX.test(url)) {
        logger.warn(`WAF blocked Path Traversal attack from ${req.ip}: ${url}`);
        return res.status(403).json({ success: false, statusCode: 403, error: { code: 'ERR_WAF_BLOCKED', message: 'Forbidden request pattern detected.' } });
      }

      if (this.SQLI_REGEX.test(url) || this.SQLI_REGEX.test(bodyStr)) {
        logger.warn(`WAF blocked SQL Injection signature from ${req.ip}`);
        return res.status(403).json({ success: false, statusCode: 403, error: { code: 'ERR_WAF_BLOCKED', message: 'Forbidden request pattern detected.' } });
      }

      if (this.XSS_REGEX.test(url) || this.XSS_REGEX.test(bodyStr)) {
        logger.warn(`WAF blocked XSS signature from ${req.ip}`);
        return res.status(403).json({ success: false, statusCode: 403, error: { code: 'ERR_WAF_BLOCKED', message: 'Forbidden request pattern detected.' } });
      }

      next();
    };
  }
}
""")

    # 2. Analytics User Cohort Retention Matrix
    write_file("services/analytics-service/src/domain/cohort-retention-matrix.ts", """export interface UserRegistrationEvent {
  userId: string;
  registeredMonth: string; // e.g. "2026-01"
}

export interface UserOrderActivity {
  userId: string;
  orderMonth: string; // e.g. "2026-02"
}

export interface CohortRetentionRow {
  cohortMonth: string;
  cohortSize: number;
  retentionByMonthIndex: { monthIndex: number; activeUsers: number; retentionRatePercent: number }[];
}

export class CohortRetentionMatrix {
  public static computeRetention(
    registrations: UserRegistrationEvent[],
    orders: UserOrderActivity[]
  ): CohortRetentionRow[] {
    const cohorts: Map<string, Set<string>> = new Map();

    for (const reg of registrations) {
      if (!cohorts.has(reg.registeredMonth)) {
        cohorts.set(reg.registeredMonth, new Set());
      }
      cohorts.get(reg.registeredMonth)!.add(reg.userId);
    }

    const rows: CohortRetentionRow[] = [];

    for (const [cohortMonth, userSet] of cohorts.entries()) {
      const cohortSize = userSet.size;
      const retentionByMonthIndex: CohortRetentionRow['retentionByMonthIndex'] = [];

      for (let m = 0; m <= 12; m++) {
        // Calculate target month string
        const activeInMonth = orders.filter(o => userSet.has(o.userId)).length;
        const rate = cohortSize > 0 ? (activeInMonth / cohortSize) * 100 : 0;

        retentionByMonthIndex.push({
          monthIndex: m,
          activeUsers: activeInMonth,
          retentionRatePercent: Math.round(rate * 10) / 10
        });
      }

      rows.push({
        cohortMonth,
        cohortSize,
        retentionByMonthIndex
      });
    }

    return rows;
  }
}
""")

    print("Production V25 modules generated.")

if __name__ == "__main__":
    generate_prod_v25()
