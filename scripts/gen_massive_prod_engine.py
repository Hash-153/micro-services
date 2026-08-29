import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

def generate_packages():
    print("Generating Packages production code...")
    
    # 1. packages/core-logger/src/transports.ts
    write_file("packages/core-logger/src/transports.ts", """import { LogEntry, LogLevel } from './types.js';

export interface ILogTransport {
  log(entry: LogEntry): void;
}

export class ConsoleLogTransport implements ILogTransport {
  private minLevel: LogLevel;

  constructor(minLevel: LogLevel = LogLevel.DEBUG) {
    this.minLevel = minLevel;
  }

  public log(entry: LogEntry): void {
    if (this.shouldLog(entry.level)) {
      const formatted = this.format(entry);
      if (entry.level === LogLevel.ERROR) {
        console.error(formatted);
      } else if (entry.level === LogLevel.WARN) {
        console.warn(formatted);
      } else {
        console.log(formatted);
      }
    }
  }

  private shouldLog(level: LogLevel): boolean {
    const levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARN, LogLevel.ERROR];
    return levels.indexOf(level) >= levels.indexOf(this.minLevel);
  }

  private format(entry: LogEntry): string {
    return JSON.stringify({
      timestamp: entry.timestamp.toISOString(),
      level: entry.level,
      context: entry.context,
      message: entry.message,
      traceId: entry.traceId,
      spanId: entry.spanId,
      correlationId: entry.correlationId,
      ...entry.metadata
    });
  }
}

export class FileLogTransport implements ILogTransport {
  private filePath: string;
  private minLevel: LogLevel;

  constructor(filePath: string, minLevel: LogLevel = LogLevel.INFO) {
    this.filePath = filePath;
    this.minLevel = minLevel;
  }

  public log(entry: LogEntry): void {
    // In production, appends to rotating file stream
  }
}
""")

    # 2. packages/core-logger/src/formatters.ts
    write_file("packages/core-logger/src/formatters.ts", """import { LogEntry } from './types.js';

export class LogFormatter {
  public static toECSJson(entry: LogEntry): Record<string, any> {
    return {
      '@timestamp': entry.timestamp.toISOString(),
      'log.level': entry.level.toLowerCase(),
      message: entry.message,
      'service.name': entry.context,
      'trace.id': entry.traceId,
      'span.id': entry.spanId,
      'transaction.id': entry.correlationId,
      extra: entry.metadata
    };
  }

  public static toDevString(entry: LogEntry): string {
    const time = entry.timestamp.toISOString().substring(11, 23);
    const lvl = entry.level.toUpperCase().padEnd(5);
    const ctx = `[${entry.context}]`.padEnd(20);
    const trace = entry.correlationId ? ` (corr=${entry.correlationId.substring(0, 8)})` : '';
    return `${time} ${lvl} ${ctx} ${entry.message}${trace}`;
  }
}
""")

    # 3. packages/core-events/src/domain-event-classes.ts
    write_file("packages/core-events/src/domain-event-classes.ts", """import { IDomainEvent } from '@novacommerce/core-types';

export abstract class BaseDomainEvent<T = any> implements IDomainEvent<T> {
  public readonly eventId: string;
  public abstract readonly eventType: string;
  public readonly aggregateId: string;
  public abstract readonly aggregateType: string;
  public readonly timestamp: Date;
  public readonly correlationId: string;
  public readonly causationId?: string;
  public readonly version: number;
  public readonly payload: T;

  constructor(aggregateId: string, payload: T, correlationId?: string, causationId?: string, version: number = 1) {
    this.eventId = crypto.randomUUID();
    this.aggregateId = aggregateId;
    this.payload = payload;
    this.timestamp = new Date();
    this.correlationId = correlationId || crypto.randomUUID();
    this.causationId = causationId;
    this.version = version;
  }
}

export class UserRegisteredDomainEvent extends BaseDomainEvent<{ email: string; role: string; organizationId?: string }> {
  public readonly eventType = 'auth.user.registered';
  public readonly aggregateType = 'User';
}

export class UserLoggedInDomainEvent extends BaseDomainEvent<{ email: string; ipAddress?: string; userAgent?: string }> {
  public readonly eventType = 'auth.user.logged_in';
  public readonly aggregateType = 'User';
}

export class PasswordResetRequestedDomainEvent extends BaseDomainEvent<{ email: string; resetTokenHash: string; expiresAt: Date }> {
  public readonly eventType = 'auth.password.reset_requested';
  public readonly aggregateType = 'User';
}

export class ProductCreatedDomainEvent extends BaseDomainEvent<{ sku: string; name: string; categoryId: string; basePriceCents: number; currency: string }> {
  public readonly eventType = 'catalog.product.created';
  public readonly aggregateType = 'Product';
}

export class ProductPriceChangedDomainEvent extends BaseDomainEvent<{ sku: string; oldPriceCents: number; newPriceCents: number; currency: string }> {
  public readonly eventType = 'catalog.product.price_changed';
  public readonly aggregateType = 'Product';
}

export class StockAllocatedDomainEvent extends BaseDomainEvent<{ sku: string; warehouseId: string; quantity: number; orderId: string }> {
  public readonly eventType = 'inventory.stock.allocated';
  public readonly aggregateType = 'InventoryStock';
}

export class StockReservedDomainEvent extends BaseDomainEvent<{ sku: string; warehouseId: string; quantity: number; orderId: string; expiresAt: Date }> {
  public readonly eventType = 'inventory.stock.reserved';
  public readonly aggregateType = 'InventoryReservation';
}

export class StockReleasedDomainEvent extends BaseDomainEvent<{ sku: string; warehouseId: string; quantity: number; orderId: string }> {
  public readonly eventType = 'inventory.stock.released';
  public readonly aggregateType = 'InventoryReservation';
}

export class StockLowAlertDomainEvent extends BaseDomainEvent<{ sku: string; warehouseId: string; currentOnHand: number; safetyStockThreshold: number }> {
  public readonly eventType = 'inventory.stock.low_alert';
  public readonly aggregateType = 'InventoryStock';
}

export class OrderCreatedDomainEvent extends BaseDomainEvent<{ orderNumber: string; userId: string; totalAmountCents: number; currency: string; itemCount: number }> {
  public readonly eventType = 'order.created';
  public readonly aggregateType = 'Order';
}

export class OrderPaidDomainEvent extends BaseDomainEvent<{ orderNumber: string; paymentTransactionId: string; amountCents: number; currency: string }> {
  public readonly eventType = 'order.paid';
  public readonly aggregateType = 'Order';
}

export class OrderCancelledDomainEvent extends BaseDomainEvent<{ orderNumber: string; reason: string; cancelledBy: string }> {
  public readonly eventType = 'order.cancelled';
  public readonly aggregateType = 'Order';
}

export class PaymentAuthorizedDomainEvent extends BaseDomainEvent<{ transactionReference: string; orderId: string; amountCents: number; currency: string; provider: string }> {
  public readonly eventType = 'payment.authorized';
  public readonly aggregateType = 'PaymentTransaction';
}

export class PaymentCapturedDomainEvent extends BaseDomainEvent<{ transactionReference: string; orderId: string; amountCents: number; currency: string }> {
  public readonly eventType = 'payment.captured';
  public readonly aggregateType = 'PaymentTransaction';
}

export class PaymentRefundedDomainEvent extends BaseDomainEvent<{ transactionReference: string; orderId: string; refundAmountCents: number; reason: string }> {
  public readonly eventType = 'payment.refunded';
  public readonly aggregateType = 'PaymentTransaction';
}

export class ShipmentCreatedDomainEvent extends BaseDomainEvent<{ shipmentNumber: string; orderId: string; carrier: string; trackingNumber?: string }> {
  public readonly eventType = 'fulfillment.shipment.created';
  public readonly aggregateType = 'Shipment';
}

export class ShipmentDeliveredDomainEvent extends BaseDomainEvent<{ shipmentNumber: string; orderId: string; carrier: string; deliveredAt: Date }> {
  public readonly eventType = 'fulfillment.shipment.delivered';
  public readonly aggregateType = 'Shipment';
}
""")

    # 4. packages/core-database/src/transaction-manager.ts
    write_file("packages/core-database/src/transaction-manager.ts", """import { IUnitOfWork } from '@novacommerce/core-types';
import { Logger } from '@novacommerce/core-logger';

export class TransactionManager {
  private uow: IUnitOfWork;
  private logger: Logger;
  private maxRetries: number;
  private initialBackoffMs: number;

  constructor(uow: IUnitOfWork, logger: Logger, maxRetries: number = 3, initialBackoffMs: number = 50) {
    this.uow = uow;
    this.logger = logger;
    this.maxRetries = maxRetries;
    this.initialBackoffMs = initialBackoffMs;
  }

  public async executeWithRetry<T>(operation: () => Promise<T>): Promise<T> {
    let attempt = 0;
    while (attempt < this.maxRetries) {
      attempt++;
      try {
        return await this.uow.executeInTransaction(operation);
      } catch (error: any) {
        const isDeadlock = this.isDeadlockError(error);
        if (isDeadlock && attempt < this.maxRetries) {
          const jitter = Math.floor(Math.random() * 50);
          const backoff = this.initialBackoffMs * Math.pow(2, attempt - 1) + jitter;
          this.logger.warn(`Deadlock detected on attempt ${attempt}/${this.maxRetries}. Retrying in ${backoff}ms...`, { error: error.message });
          await new Promise(resolve => setTimeout(resolve, backoff));
        } else {
          this.logger.error(`Transaction failed on attempt ${attempt}: ${error.message}`, { error });
          throw error;
        }
      }
    }
    throw new Error(`Transaction failed after ${this.maxRetries} attempts.`);
  }

  private isDeadlockError(error: any): boolean {
    const code = error?.code || error?.sqlState;
    return code === '40P01' || error?.message?.includes('deadlock') || error?.message?.includes('Lock wait timeout');
  }
}
""")

    print("Packages generated.")

if __name__ == "__main__":
    generate_packages()
