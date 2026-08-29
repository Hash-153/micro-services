import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path} ({len(content.splitlines())} lines)")

def generate_core_matrix():
    print("Generating comprehensive core matrix...")

    # =========================================================================
    # 1. AUTH SERVICE REPOSITORIES & CONTROLLERS
    # =========================================================================
    write_file("services/auth-service/src/controllers/mfa.controller.ts", """import { Request, Response, NextFunction } from 'express';
import { MfaService } from '../services/mfa.service.js';
import { UserAuthRepository } from '../repositories/user-auth.repository.js';
import { ApiResponse, ApiErrorResponse } from '@novacommerce/core-types';

export class MfaController {
  private mfaService: MfaService;
  private userRepo: UserAuthRepository;

  constructor(mfaService: MfaService, userRepo: UserAuthRepository) {
    this.mfaService = mfaService;
    this.userRepo = userRepo;
  }

  public enroll = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = (req as any).user;
      const secret = this.mfaService.generateMfaSecret();
      const qrCodeUrl = `otpauth://totp/NovaCommerce:${user.email}?secret=${secret}&issuer=NovaCommerce`;

      const response: ApiResponse<{ secret: string; qrCodeUrl: string }> = {
        success: true,
        statusCode: 200,
        data: { secret, qrCodeUrl }
      };
      res.json(response);
    } catch (error) {
      next(error);
    }
  };

  public verify = async (req: Request, res: Response, next: NextFunction) => {
    try {
      const user = (req as any).user;
      const { code, secret } = req.body;

      if (!code || !secret) {
        return res.status(400).json({
          success: false,
          statusCode: 400,
          error: { code: 'ERR_VALIDATION', message: 'MFA verification code and secret are required.', timestamp: new Date().toISOString() }
        });
      }

      const isValid = this.mfaService.verifyTotp(code, secret);
      if (!isValid) {
        return res.status(400).json({
          success: false,
          statusCode: 400,
          error: { code: 'ERR_INVALID_MFA_CODE', message: 'Invalid or expired 6-digit TOTP code.', timestamp: new Date().toISOString() }
        });
      }

      await this.userRepo.update(user.id, { isMfaEnabled: true, mfaSecret: secret });

      res.json({
        success: true,
        statusCode: 200,
        data: { message: 'Two-factor authentication successfully enabled.' }
      });
    } catch (error) {
      next(error);
    }
  };
}
""")

    # =========================================================================
    # 2. CATALOG SERVICE PRICING & INVENTORY SYNC
    # =========================================================================
    write_file("services/catalog-service/src/services/inventory-sync.service.ts", """import { Logger } from '@novacommerce/core-logger';

export interface SkuInventorySnapshot {
  sku: string;
  totalOnHand: number;
  totalReserved: number;
  totalAvailable: number;
  isInStock: boolean;
  lastSyncedAt: Date;
}

export class InventorySyncService {
  private logger: Logger;
  private stockCache: Map<string, SkuInventorySnapshot> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  public handleStockUpdatedEvent(payload: { sku: string; onHand: number; reserved: number }): void {
    const available = Math.max(0, payload.onHand - payload.reserved);
    const snapshot: SkuInventorySnapshot = {
      sku: payload.sku,
      totalOnHand: payload.onHand,
      totalReserved: payload.reserved,
      totalAvailable: available,
      isInStock: available > 0,
      lastSyncedAt: new Date()
    };

    this.stockCache.set(payload.sku, snapshot);
    this.logger.info(`Catalog stock cache updated for SKU ${payload.sku}: available=${available}`);
  }

  public getCachedStock(sku: string): SkuInventorySnapshot | undefined {
    return this.stockCache.get(sku);
  }
}
""")

    # =========================================================================
    # 3. ORDER SERVICE REFUND & RETURN ENGINE
    # =========================================================================
    write_file("services/order-service/src/domain/refund-calculator.ts", """import { OrderEntity, OrderItemEntity, Money, Currency } from '@novacommerce/core-types';

export interface RefundBreakdown {
  orderId: string;
  itemsRefundCents: number;
  taxRefundCents: number;
  shippingRefundCents: number;
  restockingFeeCents: number;
  totalRefundCents: number;
  currency: Currency;
}

export class RefundCalculator {
  public static computeRefund(
    order: OrderEntity,
    refundItems: { sku: string; quantity: number; conditionFeePercent?: number }[],
    refundShipping: boolean = false
  ): RefundBreakdown {
    let itemsRefundCents = 0;
    let restockingFeeCents = 0;

    for (const refItem of refundItems) {
      const orderItem = order.items.find(i => i.sku === refItem.sku);
      if (!orderItem) {
        throw new Error(`Item with SKU ${refItem.sku} was not found in order ${order.orderNumber}`);
      }

      if (refItem.quantity > orderItem.quantity) {
        throw new Error(`Cannot refund ${refItem.quantity} units of SKU ${refItem.sku} (purchased: ${orderItem.quantity})`);
      }

      const itemTotal = orderItem.unitPrice.amount * refItem.quantity;
      itemsRefundCents += itemTotal;

      if (refItem.conditionFeePercent && refItem.conditionFeePercent > 0) {
        restockingFeeCents += Math.round((itemTotal * refItem.conditionFeePercent) / 100);
      }
    }

    // Proportional sales tax refund calculation
    const taxRate = order.subtotalAmount.amount > 0 ? order.taxAmount.amount / order.subtotalAmount.amount : 0;
    const taxRefundCents = Math.round(itemsRefundCents * taxRate);

    const shippingRefundCents = refundShipping ? order.shippingFeeAmount.amount : 0;
    const totalRefundCents = Math.max(0, itemsRefundCents + taxRefundCents + shippingRefundCents - restockingFeeCents);

    return {
      orderId: order.id,
      itemsRefundCents,
      taxRefundCents,
      shippingRefundCents,
      restockingFeeCents,
      totalRefundCents,
      currency: order.totalAmount.currency
    };
  }
}
""")

    print("Core matrix generated.")

if __name__ == "__main__":
    generate_core_matrix()
