import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_prod_titan_scale():
    print("Generating comprehensive Production Titan Scale Modules...")

    # 1. API Gateway Distributed Edge Token Validator
    write_file("services/api-gateway/src/middleware/edge-token-validator.ts", """import { Request, Response, NextFunction } from 'express';
import { Logger } from '@novacommerce/core-logger';

export class EdgeTokenValidator {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public middleware() {
    return (req: Request, res: Response, next: NextFunction) => {
      const authHeader = req.headers['authorization'];
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return next(); // Unauthenticated or public endpoint
      }

      const token = authHeader.substring(7);
      try {
        const parts = token.split('.');
        if (parts.length !== 3) {
          return res.status(401).json({
            success: false,
            statusCode: 401,
            error: { code: 'ERR_MALFORMED_JWT', message: 'Bearer token is structurally invalid.', timestamp: new Date().toISOString() }
          });
        }

        const payloadJson = Buffer.from(parts[1], 'base64').toString('utf8');
        const payload = JSON.parse(payloadJson);

        if (payload.exp && Date.now() >= payload.exp * 1000) {
          return res.status(401).json({
            success: false,
            statusCode: 401,
            error: { code: 'ERR_EXPIRED_TOKEN', message: 'Token has expired.', timestamp: new Date().toISOString() }
          });
        }

        // Attach parsed claims to request
        (req as any).user = {
          id: payload.sub,
          email: payload.email,
          role: payload.role,
          organizationId: payload.orgId
        };
      } catch (err) {
        this.logger.warn('Failed to parse incoming JWT at edge gateway');
      }

      next();
    };
  }
}
""")

    # 2. Analytics Funnel Step Definition Matrix
    write_file("services/analytics-service/src/domain/funnel-step-definition-matrix.ts", """export interface StandardFunnelDefinition {
  funnelId: string;
  name: string;
  description: string;
  stepEventNames: string[];
}

export class FunnelStepDefinitionMatrix {
  private static readonly FUNNELS: StandardFunnelDefinition[] = [
    {
      funnelId: 'funnel_standard_checkout',
      name: 'E-Commerce Standard Checkout Funnel',
      description: 'End-to-end shopping conversion flow',
      stepEventNames: [
        'catalog.product_viewed',
        'cart.item_added',
        'checkout.initiated',
        'checkout.shipping_address_entered',
        'checkout.payment_method_selected',
        'checkout.order_placed',
        'payment.authorized'
      ]
    },
    {
      funnelId: 'funnel_merchant_onboarding',
      name: 'B2B Merchant Onboarding Funnel',
      description: 'Merchant organization registration and verification',
      stepEventNames: [
        'user.registered',
        'organization.created',
        'kyc.documents_uploaded',
        'payment.bank_account_linked',
        'catalog.first_product_published'
      ]
    }
  ];

  public static getFunnel(funnelId: string): StandardFunnelDefinition | undefined {
    return this.FUNNELS.find(f => f.funnelId === funnelId);
  }

  public static getAllFunnels(): StandardFunnelDefinition[] {
    return this.FUNNELS;
  }
}
""")

    print("Production titan scale modules generated.")

if __name__ == "__main__":
    generate_prod_titan_scale()
