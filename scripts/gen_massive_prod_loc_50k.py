import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_production_services():
    print("Generating comprehensive microservices production suite...")

    # =========================================================================
    # AUTH SERVICE ADVANCED MODULES
    # =========================================================================
    write_file("services/auth-service/src/domain/password-policy.ts", """export interface PasswordPolicyResult {
  isValid: boolean;
  score: number; // 0 to 4 (zxcvbn entropy score)
  feedback: string[];
  hasMinLength: boolean;
  hasUppercase: boolean;
  hasLowercase: boolean;
  hasNumber: boolean;
  hasSpecialChar: boolean;
}

export class PasswordPolicyEngine {
  public static evaluate(password: string): PasswordPolicyResult {
    const feedback: string[] = [];
    const hasMinLength = password.length >= 10;
    const hasUppercase = /[A-Z]/.test(password);
    const hasLowercase = /[a-z]/.test(password);
    const hasNumber = /[0-9]/.test(password);
    const hasSpecialChar = /[^A-Za-z0-9]/.test(password);

    if (!hasMinLength) feedback.push('Password must be at least 10 characters long.');
    if (!hasUppercase) feedback.push('Password must contain at least one uppercase letter.');
    if (!hasLowercase) feedback.push('Password must contain at least one lowercase letter.');
    if (!hasNumber) feedback.push('Password must contain at least one numeric digit.');
    if (!hasSpecialChar) feedback.push('Password must contain at least one special symbol.');

    // Common breached passwords dictionary check
    const commonPasswords = ['password', '12345678', 'qwertyuiop', 'admin123', 'letmein123', 'welcome123'];
    if (commonPasswords.includes(password.toLowerCase())) {
      feedback.push('Password is in the common compromised dictionary.');
    }

    let score = 0;
    if (hasMinLength) score++;
    if (hasUppercase && hasLowercase) score++;
    if (hasNumber) score++;
    if (hasSpecialChar && password.length >= 14) score++;

    return {
      isValid: feedback.length === 0,
      score,
      feedback,
      hasMinLength,
      hasUppercase,
      hasLowercase,
      hasNumber,
      hasSpecialChar
    };
  }
}
""")

    write_file("services/auth-service/src/domain/device-fingerprint.ts", """export interface DeviceFingerprintData {
  ipAddress: string;
  userAgent: string;
  acceptLanguage?: string;
  screenResolution?: string;
  timezoneOffset?: number;
  canvasHash?: string;
}

export interface AnomalyEvaluationResult {
  riskScore: number; // 0 to 100
  isSuspicious: boolean;
  requiresStepUpAuth: boolean;
  detectedAnomalies: string[];
}

export class DeviceFingerprintService {
  public static evaluateLoginAnomaly(
    current: DeviceFingerprintData,
    historicalLogins: DeviceFingerprintData[]
  ): AnomalyEvaluationResult {
    const anomalies: string[] = [];
    let riskScore = 0;

    if (historicalLogins.length === 0) {
      return {
        riskScore: 10,
        isSuspicious: false,
        requiresStepUpAuth: false,
        detectedAnomalies: ['First-time device login']
      };
    }

    const matchedIp = historicalLogins.some(h => h.ipAddress === current.ipAddress);
    const matchedUserAgent = historicalLogins.some(h => h.userAgent === current.userAgent);

    if (!matchedIp) {
      riskScore += 25;
      anomalies.push('Unrecognized IP address');
    }

    if (!matchedUserAgent) {
      riskScore += 35;
      anomalies.push('Unrecognized browser or device user-agent');
    }

    const isSuspicious = riskScore >= 50;
    const requiresStepUpAuth = riskScore >= 35;

    return {
      riskScore,
      isSuspicious,
      requiresStepUpAuth,
      detectedAnomalies: anomalies
    };
  }
}
""")

    # =========================================================================
    # USER SERVICE ADVANCED MODULES
    # =========================================================================
    write_file("services/user-service/src/domain/address-normalizer.ts", """import { AddressEntity } from '@novacommerce/core-types';

export class AddressNormalizer {
  private static readonly US_STATE_MAP: Record<string, string> = {
    ALABAMA: 'AL', ALASKA: 'AK', ARIZONA: 'AZ', ARKANSAS: 'AR', CALIFORNIA: 'CA',
    COLORADO: 'CO', CONNECTICUT: 'CT', DELAWARE: 'DE', FLORIDA: 'FL', GEORGIA: 'GA',
    HAWAII: 'HI', IDAHO: 'ID', ILLINOIS: 'IL', INDIANA: 'IN', IOWA: 'IA',
    KANSAS: 'KS', KENTUCKY: 'KY', LOUISIANA: 'LA', MAINE: 'ME', MARYLAND: 'MD',
    MASSACHUSETTS: 'MA', MICHIGAN: 'MI', MINNESOTA: 'MN', MISSISSIPPI: 'MS', MISSOURI: 'MO',
    MONTANA: 'MT', NEBRASKA: 'NE', NEVADA: 'NV', 'NEW HAMPSHIRE': 'NH', 'NEW JERSEY': 'NJ',
    'NEW MEXICO': 'NM', 'NEW YORK': 'NY', 'NORTH CAROLINA': 'NC', 'NORTH DAKOTA': 'ND', OHIO: 'OH',
    OKLAHOMA: 'OK', OREGON: 'OR', PENNSYLVANIA: 'PA', 'RHODE ISLAND': 'RI', 'SOUTH CAROLINA': 'SC',
    'SOUTH DAKOTA': 'SD', TENNESSEE: 'TN', TEXAS: 'TX', UTAH: 'UT', VERMONT: 'VT',
    VIRGINIA: 'VA', WASHINGTON: 'WA', 'WEST VIRGINIA': 'WV', WISCONSIN: 'WI', WYOMING: 'WY'
  };

  public static normalize(address: Partial<AddressEntity>): Partial<AddressEntity> {
    const country = (address.countryCode || 'US').toUpperCase().trim();
    let state = (address.stateOrProvince || '').trim().toUpperCase();

    if (country === 'US' && this.US_STATE_MAP[state]) {
      state = this.US_STATE_MAP[state];
    }

    let postal = (address.postalCode || '').trim().replace(/[^0-9A-Za-z-]/g, '');
    if (country === 'US' && postal.length === 5) {
      // Standard 5-digit zip
    }

    return {
      ...address,
      recipientName: (address.recipientName || '').trim(),
      streetLine1: this.standardizeStreetSuffix((address.streetLine1 || '').trim()),
      streetLine2: address.streetLine2 ? address.streetLine2.trim() : undefined,
      city: this.capitalizeWords((address.city || '').trim()),
      stateOrProvince: state,
      postalCode: postal,
      countryCode: country
    };
  }

  private static standardizeStreetSuffix(street: string): string {
    return street
      .replace(/\\bStreet\\b/gi, 'St')
      .replace(/\\bAvenue\\b/gi, 'Ave')
      .replace(/\\bBoulevard\\b/gi, 'Blvd')
      .replace(/\\bRoad\\b/gi, 'Rd')
      .replace(/\\bDrive\\b/gi, 'Dr')
      .replace(/\\bLane\\b/gi, 'Ln')
      .replace(/\\bSuite\\b/gi, 'Ste')
      .replace(/\\bApartment\\b/gi, 'Apt');
  }

  private static capitalizeWords(str: string): string {
    return str.replace(/\\b\\w+/g, txt => txt.charAt(0).toUpperCase() + txt.substring(1).toLowerCase());
  }
}
""")

    # =========================================================================
    # CATALOG SERVICE ADVANCED MODULES
    # =========================================================================
    write_file("services/catalog-service/src/domain/faceted-search.ts", """import { ProductEntity, ProductSearchFilter } from '@novacommerce/core-types';

export interface FacetResult {
  field: string;
  buckets: { key: string; count: number }[];
}

export interface SearchResponsePayload {
  items: ProductEntity[];
  total: number;
  facets: FacetResult[];
  page: number;
  limit: number;
  totalPages: number;
}

export class FacetedSearchEngine {
  public static executeSearch(products: ProductEntity[], filter: ProductSearchFilter): SearchResponsePayload {
    let matches = products.filter(p => p.isActive);

    if (filter.query) {
      const q = filter.query.toLowerCase().trim();
      matches = matches.filter(p =>
        p.name.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q) ||
        p.sku.toLowerCase().includes(q) ||
        p.tags.some(t => t.toLowerCase().includes(q))
      );
    }

    if (filter.categoryId) {
      matches = matches.filter(p => p.categoryId === filter.categoryId);
    }

    if (filter.minPriceCents !== undefined) {
      matches = matches.filter(p => p.basePrice.amount >= filter.minPriceCents!);
    }

    if (filter.maxPriceCents !== undefined) {
      matches = matches.filter(p => p.basePrice.amount <= filter.maxPriceCents!);
    }

    if (filter.tags && filter.tags.length > 0) {
      matches = matches.filter(p => filter.tags!.some(t => p.tags.includes(t)));
    }

    // Build Facet Buckets
    const categoryCounts: Record<string, number> = {};
    const tagCounts: Record<string, number> = {};

    matches.forEach(p => {
      categoryCounts[p.categoryId] = (categoryCounts[p.categoryId] || 0) + 1;
      p.tags.forEach(t => {
        tagCounts[t] = (tagCounts[t] || 0) + 1;
      });
    });

    const facets: FacetResult[] = [
      {
        field: 'categoryId',
        buckets: Object.entries(categoryCounts).map(([key, count]) => ({ key, count }))
      },
      {
        field: 'tags',
        buckets: Object.entries(tagCounts).map(([key, count]) => ({ key, count }))
      }
    ];

    const page = filter.page || 1;
    const limit = filter.limit || 20;
    const offset = (page - 1) * limit;
    const paginatedItems = matches.slice(offset, offset + limit);

    return {
      items: paginatedItems,
      total: matches.length,
      facets,
      page,
      limit,
      totalPages: Math.ceil(matches.length / limit)
    };
  }
}
""")

    # =========================================================================
    # API GATEWAY ADVANCED MODULES
    # =========================================================================
    write_file("services/api-gateway/src/middleware/circuit-breaker.middleware.ts", """import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export type CircuitState = 'CLOSED' | 'OPEN' | 'HALF_OPEN';

export class ServiceCircuitBreaker {
  private name: string;
  private state: CircuitState = 'CLOSED';
  private failureCount: number = 0;
  private successCount: number = 0;
  private lastFailureTime: number = 0;
  private failureThreshold: number;
  private recoveryTimeMs: number;
  private logger: Logger;

  constructor(name: string, logger: Logger, failureThreshold: number = 5, recoveryTimeMs: number = 30000) {
    this.name = name;
    this.logger = logger;
    this.failureThreshold = failureThreshold;
    this.recoveryTimeMs = recoveryTimeMs;
  }

  public middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      if (this.state === 'OPEN') {
        const now = Date.now();
        if (now - this.lastFailureTime > this.recoveryTimeMs) {
          this.state = 'HALF_OPEN';
          this.logger.info(`Circuit breaker for ${this.name} entered HALF_OPEN state (probing downstream).`);
        } else {
          return res.status(503).json({
            success: false,
            statusCode: 503,
            error: {
              code: 'ERR_CIRCUIT_OPEN',
              message: `Service '${this.name}' is temporarily unavailable due to downstream failure protection.`,
              timestamp: new Date().toISOString()
            }
          });
        }
      }

      res.on('finish', () => {
        if (res.statusCode >= 500) {
          this.recordFailure();
        } else if (res.statusCode < 400) {
          this.recordSuccess();
        }
      });

      next();
    };
  }

  private recordFailure(): void {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.state === 'HALF_OPEN' || this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      this.logger.error(`Circuit breaker for ${this.name} tripped to OPEN state after ${this.failureCount} failures.`);
    }
  }

  private recordSuccess(): void {
    if (this.state === 'HALF_OPEN') {
      this.successCount++;
      if (this.successCount >= 3) {
        this.state = 'CLOSED';
        this.failureCount = 0;
        this.successCount = 0;
        this.logger.info(`Circuit breaker for ${this.name} recovered to CLOSED state.`);
      }
    } else {
      this.failureCount = 0;
    }
  }
}
""")

    print("Comprehensive production services generated.")

if __name__ == "__main__":
    generate_production_services()
