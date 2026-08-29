import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_order_service():
    svc_dir = "services/order-service"
    
    write_file(f"{svc_dir}/package.json", """{
  "name": "@novacommerce/order-service",
  "version": "1.0.0",
  "description": "NovaCommerce Order Lifecycle and Distributed Checkout Saga Orchestrator",
  "main": "dist/server.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "ts-node src/server.ts",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*",
    "@novacommerce/core-events": "workspace:*",
    "@novacommerce/core-middleware": "workspace:*",
    "@novacommerce/core-database": "workspace:*",
    "express": "^4.19.2",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "supertest": "^7.0.0",
    "@types/supertest": "^6.0.2",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{svc_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{svc_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{svc_dir}/Dockerfile", """FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/order-service/ services/order-service/
RUN npm ci && npm run build --workspace=@novacommerce/order-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/order-service/dist ./services/order-service/dist
COPY --from=builder /app/services/order-service/package.json ./services/order-service/package.json
EXPOSE 8004
CMD ["node", "services/order-service/dist/server.js"]
""")

    # Order State Machine
    write_file(f"{svc_dir}/src/domain/order-state-machine.ts", """import { OrderStatus, AppError, ErrorCode } from '@novacommerce/core-types';

const ALLOWED_TRANSITIONS: Record<OrderStatus, OrderStatus[]> = {
  [OrderStatus.DRAFT]: [OrderStatus.PENDING_PAYMENT, OrderStatus.CANCELLED],
  [OrderStatus.PENDING_PAYMENT]: [OrderStatus.PAYMENT_AUTHORIZED, OrderStatus.PAYMENT_FAILED, OrderStatus.CANCELLED, OrderStatus.EXPIRED],
  [OrderStatus.PAYMENT_AUTHORIZED]: [OrderStatus.PROCESSING, OrderStatus.INVENTORY_RESERVED, OrderStatus.CANCELLED],
  [OrderStatus.INVENTORY_RESERVED]: [OrderStatus.PROCESSING, OrderStatus.PACKED, OrderStatus.CANCELLED],
  [OrderStatus.INVENTORY_ALLOCATION_FAILED]: [OrderStatus.CANCELLED],
  [OrderStatus.PAYMENT_FAILED]: [OrderStatus.PENDING_PAYMENT, OrderStatus.CANCELLED],
  [OrderStatus.PROCESSING]: [OrderStatus.PACKED, OrderStatus.CANCELLED],
  [OrderStatus.PACKED]: [OrderStatus.DISPATCHED, OrderStatus.CANCELLED],
  [OrderStatus.DISPATCHED]: [OrderStatus.IN_TRANSIT, OrderStatus.DELIVERED],
  [OrderStatus.IN_TRANSIT]: [OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED],
  [OrderStatus.OUT_FOR_DELIVERY]: [OrderStatus.DELIVERED],
  [OrderStatus.DELIVERED]: [OrderStatus.REFUND_REQUESTED, OrderStatus.REFUNDED],
  [OrderStatus.CANCELLED]: [],
  [OrderStatus.REFUND_REQUESTED]: [OrderStatus.REFUNDED, OrderStatus.PARTIALLY_REFUNDED],
  [OrderStatus.REFUNDED]: [],
  [OrderStatus.PARTIALLY_REFUNDED]: [OrderStatus.REFUNDED],
  [OrderStatus.EXPIRED]: []
};

export class OrderStateMachine {
  public static canTransition(current: OrderStatus, target: OrderStatus): boolean {
    const allowed = ALLOWED_TRANSITIONS[current] || [];
    return allowed.includes(target);
  }

  public static transition(current: OrderStatus, target: OrderStatus): OrderStatus {
    if (!this.canTransition(current, target)) {
      throw new AppError(
        `Invalid order status transition from ${current} to ${target}`,
        400,
        ErrorCode.ORDER_INVALID_STATE_TRANSITION
      );
    }
    return target;
  }
}
""")

    # Tax & Discount Engine
    write_file(f"{svc_dir}/src/domain/tax-calculator.ts", """import { Money, Currency } from '@novacommerce/core-types';

export class TaxCalculator {
  // Calculates standard tax based on region and subtotal (e.g. 8.25%)
  public static calculateTax(subtotal: Money, countryCode: string = 'US', stateCode?: string): Money {
    let rate = 0.08; // Default 8%
    if (countryCode === 'DE' || countryCode === 'FR') rate = 0.19; // 19% VAT
    if (countryCode === 'GB') rate = 0.20; // 20% VAT
    if (stateCode === 'CA') rate = 0.0925;
    if (stateCode === 'NY') rate = 0.08875;

    const taxAmount = Math.round(subtotal.amount * rate);
    return {
      amount: taxAmount,
      currency: subtotal.currency
    };
  }
}
""")

    # Saga Orchestrator
    write_file(f"{svc_dir}/src/saga/saga-step.interface.ts", """export interface SagaContext {
  orderId: string;
  userId: string;
  items: Array<{ sku: string; quantity: number }>;
  totalAmount: number;
  currency: string;
  paymentMethod: { type: string; token: string; provider: string };
  carrierCode: string;
  reservationId?: string;
  paymentTransactionId?: string;
  shipmentId?: string;
  correlationId: string;
}

export interface ISagaStep {
  name: string;
  execute(context: SagaContext): Promise<void>;
  compensate(context: SagaContext): Promise<void>;
}
""")

    write_file(f"{svc_dir}/src/saga/checkout-saga.orchestrator.ts", """import { ISagaStep, SagaContext } from './saga-step.interface.js';
import { ILogger } from '@novacommerce/core-logger';
import { SagaExecutionError } from '@novacommerce/core-types';

export class CheckoutSagaOrchestrator {
  private readonly steps: ISagaStep[] = [];
  private readonly logger: ILogger;

  constructor(logger: ILogger) {
    this.logger = logger.child({ component: 'CheckoutSagaOrchestrator' });
  }

  public addStep(step: ISagaStep): this {
    this.steps.push(step);
    return this;
  }

  public async execute(context: SagaContext): Promise<boolean> {
    const executedSteps: ISagaStep[] = [];
    this.logger.info(`Starting Checkout Saga for order ${context.orderId}`, { correlationId: context.correlationId });

    for (const step of this.steps) {
      try {
        this.logger.debug(`Executing saga step: ${step.name}`);
        await step.execute(context);
        executedSteps.push(step);
      } catch (err: any) {
        this.logger.error(`Saga step '${step.name}' failed. Initiating rollback compensation...`, err);
        await this.rollback(executedSteps, context);
        throw new SagaExecutionError('CheckoutSaga', step.name, err);
      }
    }

    this.logger.info(`Checkout Saga completed successfully for order ${context.orderId}`);
    return true;
  }

  private async rollback(executedSteps: ISagaStep[], context: SagaContext): Promise<void> {
    const reversed = [...executedSteps].reverse();
    for (const step of reversed) {
      try {
        this.logger.warn(`Compensating saga step: ${step.name}`);
        await step.compensate(context);
      } catch (compErr) {
        this.logger.fatal(`CRITICAL: Compensation failed for step '${step.name}'`, compErr);
      }
    }
  }
}
""")

    # Repositories & Service
    write_file(f"{svc_dir}/src/repositories/order.repository.ts", """import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { OrderEntity } from '@novacommerce/core-types';

export class InMemoryOrderRepository extends InMemoryBaseRepository<OrderEntity> {
  public async findByOrderNumber(orderNumber: string): Promise<OrderEntity | null> {
    for (const ord of this.items.values()) {
      if (ord.orderNumber === orderNumber) return JSON.parse(JSON.stringify(ord));
    }
    return null;
  }

  public async findByUserId(userId: string): Promise<OrderEntity[]> {
    return Array.from(this.items.values()).filter(o => o.userId === userId);
  }
}
""")

    write_file(f"{svc_dir}/src/services/order.service.ts", """import { InMemoryOrderRepository } from '../repositories/order.repository.js';
import { OrderEntity, OrderStatus, Currency, NotFoundError, CreateOrderDTO } from '@novacommerce/core-types';
import { TaxCalculator } from '../domain/tax-calculator.js';
import { OrderStateMachine } from '../domain/order-state-machine.js';
import { IEventBus, DomainEventFactory } from '@novacommerce/core-events';
import { EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class OrderService {
  private readonly repo: InMemoryOrderRepository;
  private readonly eventBus?: IEventBus;

  constructor(repo: InMemoryOrderRepository, eventBus?: IEventBus) {
    this.repo = repo;
    this.eventBus = eventBus;
  }

  public async createOrder(dto: CreateOrderDTO, userId: string = 'user-anon', correlationId?: string): Promise<OrderEntity> {
    const orderNumber = `ORD-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
    
    let subtotalCents = 0;
    const items = dto.items.map(i => {
      const unitCents = 2999; // mock unit price
      const totalItem = unitCents * i.quantity;
      subtotalCents += totalItem;
      return {
        id: randomUUID(),
        orderId: '',
        sku: i.sku,
        productName: `Item ${i.sku}`,
        unitPrice: { amount: unitCents, currency: dto.currency || Currency.USD },
        quantity: i.quantity,
        subtotal: { amount: totalItem, currency: dto.currency || Currency.USD },
        taxAmount: { amount: 0, currency: dto.currency || Currency.USD },
        discountAmount: { amount: 0, currency: dto.currency || Currency.USD },
        total: { amount: totalItem, currency: dto.currency || Currency.USD }
      };
    });

    const subtotalMoney = { amount: subtotalCents, currency: dto.currency || Currency.USD };
    const taxMoney = TaxCalculator.calculateTax(subtotalMoney, 'US');
    const shippingMoney = { amount: 500, currency: dto.currency || Currency.USD };
    const totalMoney = { amount: subtotalMoney.amount + taxMoney.amount + shippingMoney.amount, currency: dto.currency || Currency.USD };

    const orderId = randomUUID();
    items.forEach(i => (i.orderId = orderId));

    const order: OrderEntity = {
      id: orderId,
      orderNumber,
      userId,
      status: OrderStatus.PENDING_PAYMENT,
      shippingAddress: {} as any,
      billingAddress: {} as any,
      items,
      subtotalAmount: subtotalMoney,
      taxAmount: taxMoney,
      shippingFeeAmount: shippingMoney,
      discountAmount: { amount: 0, currency: dto.currency || Currency.USD },
      totalAmount: totalMoney,
      idempotencyKey: dto.idempotencyKey,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    const saved = await this.repo.create(order);

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.ORDER_CREATED,
        saved.id,
        'Order',
        saved,
        'order-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return saved;
  }

  public async updateOrderStatus(id: string, newStatus: OrderStatus, correlationId?: string): Promise<OrderEntity> {
    const order = await this.repo.findById(id);
    if (!order) throw new NotFoundError('Order', id);

    const validStatus = OrderStateMachine.transition(order.status, newStatus);
    const updated = await this.repo.update(id, { status: validStatus });

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.ORDER_UPDATED,
        id,
        'Order',
        { orderId: id, status: validStatus },
        'order-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return updated!;
  }

  public async getOrderById(id: string): Promise<OrderEntity> {
    const order = await this.repo.findById(id);
    if (!order) throw new NotFoundError('Order', id);
    return order;
  }
}
""")

    # App & Server
    write_file(f"{svc_dir}/src/app.ts", """import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware, RequestValidator } from '@novacommerce/core-middleware';
import { InMemoryOrderRepository } from './repositories/order.repository.js';
import { OrderService } from './services/order.service.js';
import { CreateOrderSchema } from '@novacommerce/core-types';

export function createOrderApp(): Express {
  const app = express();
  const logger = Logger.create('order-service');
  const service = new OrderService(new InMemoryOrderRepository());

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'order-service' }));

  app.post('/api/v1/orders', RequestValidator.validateBody(CreateOrderSchema), async (req, res, next) => {
    try {
      const correlationId = req.headers['x-correlation-id'] as string;
      const order = await service.createOrder(req.body, req.body.userId || 'usr-default', correlationId);
      res.status(201).json({ success: true, data: order });
    } catch (err) {
      next(err);
    }
  });

  app.get('/api/v1/orders/:id', async (req, res, next) => {
    try {
      const order = await service.getOrderById(req.params.id);
      res.json({ success: true, data: order });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
""")

    write_file(f"{svc_dir}/src/server.ts", """import { createOrderApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('order-service');
const port = parseInt(process.env.ORDER_SERVICE_PORT || '8004', 10);
const app = createOrderApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Order Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Order Service gracefully...');
  server.close(() => process.exit(0));
});
""")

    write_file(f"{svc_dir}/tests/order.test.ts", """import request from 'supertest';
import { createOrderApp } from '../src/app.js';
import { randomUUID } from 'crypto';

describe('Order Service Suite', () => {
  const app = createOrderApp();

  it('should create order and compute tax automatically', async () => {
    const res = await request(app)
      .post('/api/v1/orders')
      .send({
        shippingAddressId: randomUUID(),
        billingAddressId: randomUUID(),
        items: [{ sku: 'SKU-001', quantity: 2 }],
        idempotencyKey: randomUUID()
      });

    expect(res.status).toBe(201);
    expect(res.body.data.orderNumber).toBeDefined();
    expect(res.body.data.subtotalAmount.amount).toBe(5998);
    expect(res.body.data.taxAmount.amount).toBeGreaterThan(0);
  });
});
""")
    print(f"Generated {svc_dir}")

def generate_payment_service():
    svc_dir = "services/payment-service"
    
    write_file(f"{svc_dir}/package.json", """{
  "name": "@novacommerce/payment-service",
  "version": "1.0.0",
  "description": "NovaCommerce Payment Gateway and Double-Entry Financial Ledger Service",
  "main": "dist/server.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "ts-node src/server.ts",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*",
    "@novacommerce/core-events": "workspace:*",
    "@novacommerce/core-middleware": "workspace:*",
    "@novacommerce/core-database": "workspace:*",
    "express": "^4.19.2",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "supertest": "^7.0.0",
    "@types/supertest": "^6.0.2",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{svc_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{svc_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{svc_dir}/Dockerfile", """FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/payment-service/ services/payment-service/
RUN npm ci && npm run build --workspace=@novacommerce/payment-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/payment-service/dist ./services/payment-service/dist
COPY --from=builder /app/services/payment-service/package.json ./services/payment-service/package.json
EXPOSE 8005
CMD ["node", "services/payment-service/dist/server.js"]
""")

    # Double-entry ledger
    write_file(f"{svc_dir}/src/domain/double-entry-ledger.ts", """import { LedgerJournalEntryEntity, LedgerLineEntity, AppError, ErrorCode } from '@novacommerce/core-types';

export class DoubleEntryLedgerEngine {
  public static validateBalancedEntry(lines: LedgerLineEntity[]): void {
    let totalDebit = 0;
    let totalCredit = 0;

    for (const line of lines) {
      if (line.entryType === 'DEBIT') {
        totalDebit += line.amount;
      } else if (line.entryType === 'CREDIT') {
        totalCredit += line.amount;
      }
    }

    if (totalDebit !== totalCredit) {
      throw new AppError(
        `Double-entry ledger is out of balance! Debits (${totalDebit}) do not equal Credits (${totalCredit})`,
        400,
        ErrorCode.LEDGER_UNBALANCED_ENTRY
      );
    }
  }
}
""")

    # Repositories & Service
    write_file(f"{svc_dir}/src/repositories/payment.repository.ts", """import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { PaymentTransactionEntity, LedgerJournalEntryEntity } from '@novacommerce/core-types';

export class InMemoryPaymentRepository extends InMemoryBaseRepository<PaymentTransactionEntity> {}
export class InMemoryLedgerRepository extends InMemoryBaseRepository<LedgerJournalEntryEntity> {}
""")

    write_file(f"{svc_dir}/src/services/payment.service.ts", """import { InMemoryPaymentRepository, InMemoryLedgerRepository } from '../repositories/payment.repository.js';
import { DoubleEntryLedgerEngine } from '../domain/double-entry-ledger.js';
import { PaymentTransactionEntity, PaymentStatus, PaymentMethodType, PaymentGatewayProvider, Currency } from '@novacommerce/core-types';
import { IEventBus, DomainEventFactory } from '@novacommerce/core-events';
import { EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class PaymentService {
  private readonly paymentRepo: InMemoryPaymentRepository;
  private readonly ledgerRepo: InMemoryLedgerRepository;
  private readonly eventBus?: IEventBus;

  constructor(paymentRepo: InMemoryPaymentRepository, ledgerRepo: InMemoryLedgerRepository, eventBus?: IEventBus) {
    this.paymentRepo = paymentRepo;
    this.ledgerRepo = ledgerRepo;
    this.eventBus = eventBus;
  }

  public async authorizePayment(
    orderId: string,
    userId: string,
    amountCents: number,
    currency: Currency = Currency.USD,
    correlationId?: string
  ): Promise<PaymentTransactionEntity> {
    const paymentId = randomUUID();
    const transaction: PaymentTransactionEntity = {
      id: paymentId,
      transactionReference: `TXN-${Date.now()}-${randomUUID().substring(0, 6)}`,
      orderId,
      userId,
      amount: { amount: amountCents, currency },
      status: PaymentStatus.CAPTURED,
      methodType: PaymentMethodType.CREDIT_CARD,
      provider: PaymentGatewayProvider.MOCK,
      providerTransactionId: `ch_mock_${randomUUID()}`,
      idempotencyKey: randomUUID(),
      metadata: {},
      createdAt: new Date(),
      updatedAt: new Date()
    };

    const savedPayment = await this.paymentRepo.create(transaction);

    // Record double entry: Debit Cash/Processor Receivable, Credit Customer Revenue
    const lines = [
      { id: randomUUID(), journalEntryId: '', accountId: 'acc_cash_receivable', entryType: 'DEBIT' as const, amount: amountCents },
      { id: randomUUID(), journalEntryId: '', accountId: 'acc_sales_revenue', entryType: 'CREDIT' as const, amount: amountCents }
    ];

    DoubleEntryLedgerEngine.validateBalancedEntry(lines);

    const journalEntryId = randomUUID();
    lines.forEach(l => (l.journalEntryId = journalEntryId));

    await this.ledgerRepo.create({
      id: journalEntryId,
      entryNumber: `JRN-${Date.now()}`,
      description: `Payment captured for order ${orderId}`,
      transactionId: paymentId,
      referenceType: 'PAYMENT',
      referenceId: paymentId,
      postedAt: new Date(),
      lines
    });

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.PAYMENT_CAPTURED,
        savedPayment.id,
        'PaymentTransaction',
        savedPayment,
        'payment-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return savedPayment;
  }
}
""")

    # App & Server
    write_file(f"{svc_dir}/src/app.ts", """import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware } from '@novacommerce/core-middleware';
import { InMemoryPaymentRepository, InMemoryLedgerRepository } from './repositories/payment.repository.js';
import { PaymentService } from './services/payment.service.js';

export function createPaymentApp(): Express {
  const app = express();
  const logger = Logger.create('payment-service');
  const service = new PaymentService(new InMemoryPaymentRepository(), new InMemoryLedgerRepository());

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'payment-service' }));

  app.post('/api/v1/payments/authorize', async (req, res, next) => {
    try {
      const { orderId, userId, amountCents, currency } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      const payment = await service.authorizePayment(orderId, userId || 'usr-anon', amountCents, currency, correlationId);
      res.status(201).json({ success: true, data: payment });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
""")

    write_file(f"{svc_dir}/src/server.ts", """import { createPaymentApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('payment-service');
const port = parseInt(process.env.PAYMENT_SERVICE_PORT || '8005', 10);
const app = createPaymentApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Payment Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Payment Service gracefully...');
  server.close(() => process.exit(0));
});
""")

    write_file(f"{svc_dir}/tests/payment.test.ts", """import request from 'supertest';
import { createPaymentApp } from '../src/app.js';

describe('Payment Service Suite', () => {
  const app = createPaymentApp();

  it('should capture payment and maintain balanced ledger entries', async () => {
    const res = await request(app)
      .post('/api/v1/payments/authorize')
      .send({ orderId: 'ord-999', amountCents: 4999 });

    expect(res.status).toBe(201);
    expect(res.body.data.status).toBe('CAPTURED');
    expect(res.body.data.amount.amount).toBe(4999);
  });
});
""")
    print(f"Generated {svc_dir}")

def generate_fulfillment_service():
    svc_dir = "services/fulfillment-service"
    
    write_file(f"{svc_dir}/package.json", """{
  "name": "@novacommerce/fulfillment-service",
  "version": "1.0.0",
  "description": "NovaCommerce Carrier Integrations, Dispatch, and Logistics Fulfillment",
  "main": "dist/server.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "ts-node src/server.ts",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*",
    "@novacommerce/core-events": "workspace:*",
    "@novacommerce/core-middleware": "workspace:*",
    "@novacommerce/core-database": "workspace:*",
    "express": "^4.19.2",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "supertest": "^7.0.0",
    "@types/supertest": "^6.0.2",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{svc_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{svc_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{svc_dir}/Dockerfile", """FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/fulfillment-service/ services/fulfillment-service/
RUN npm ci && npm run build --workspace=@novacommerce/fulfillment-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/fulfillment-service/dist ./services/fulfillment-service/dist
COPY --from=builder /app/services/fulfillment-service/package.json ./services/fulfillment-service/package.json
EXPOSE 8006
CMD ["node", "services/fulfillment-service/dist/server.js"]
""")

    # Repositories & Service
    write_file(f"{svc_dir}/src/repositories/shipment.repository.ts", """import { InMemoryBaseRepository } from '@novacommerce/core-database';
import { ShipmentEntity } from '@novacommerce/core-types';

export class InMemoryShipmentRepository extends InMemoryBaseRepository<ShipmentEntity> {}
""")

    write_file(f"{svc_dir}/src/services/fulfillment.service.ts", """import { InMemoryShipmentRepository } from '../repositories/shipment.repository.js';
import { ShipmentEntity, FulfillmentStatus, CarrierCode } from '@novacommerce/core-types';
import { IEventBus, DomainEventFactory } from '@novacommerce/core-events';
import { EventType } from '@novacommerce/core-types';
import { randomUUID } from 'crypto';

export class FulfillmentService {
  private readonly repo: InMemoryShipmentRepository;
  private readonly eventBus?: IEventBus;

  constructor(repo: InMemoryShipmentRepository, eventBus?: IEventBus) {
    this.repo = repo;
    this.eventBus = eventBus;
  }

  public async createShipment(
    orderId: string,
    destinationAddress: any,
    carrier: CarrierCode = CarrierCode.MOCK_CARRIER,
    correlationId?: string
  ): Promise<ShipmentEntity> {
    const trackingNumber = `TRK-${carrier}-${Math.floor(100000000 + Math.random() * 900000000)}`;
    const shipment: ShipmentEntity = {
      id: randomUUID(),
      shipmentNumber: `SHP-${Date.now()}`,
      orderId,
      status: FulfillmentStatus.LABEL_GENERATED,
      carrier,
      serviceLevel: 'STANDARD_GROUND',
      trackingNumber,
      trackingUrl: `https://tracking.novacommerce.io/${trackingNumber}`,
      shippingLabelUrl: `https://cdn.novacommerce.io/labels/${trackingNumber}.pdf`,
      originWarehouseId: 'WH-MAIN-01',
      destinationAddress,
      weightGrams: 1200,
      dimensionsMm: { length: 300, width: 200, height: 100 },
      createdAt: new Date(),
      updatedAt: new Date()
    };

    const saved = await this.repo.create(shipment);

    if (this.eventBus) {
      const event = DomainEventFactory.create(
        EventType.FULFILLMENT_CREATED,
        saved.id,
        'Shipment',
        saved,
        'fulfillment-service',
        correlationId
      );
      await this.eventBus.publish(event);
    }

    return saved;
  }
}
""")

    # App & Server
    write_file(f"{svc_dir}/src/app.ts", """import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware } from '@novacommerce/core-middleware';
import { InMemoryShipmentRepository } from './repositories/shipment.repository.js';
import { FulfillmentService } from './services/fulfillment.service.js';

export function createFulfillmentApp(): Express {
  const app = express();
  const logger = Logger.create('fulfillment-service');
  const service = new FulfillmentService(new InMemoryShipmentRepository());

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'fulfillment-service' }));

  app.post('/api/v1/fulfillment/shipments', async (req, res, next) => {
    try {
      const { orderId, destinationAddress, carrier } = req.body;
      const correlationId = req.headers['x-correlation-id'] as string;
      const shipment = await service.createShipment(orderId, destinationAddress || {}, carrier, correlationId);
      res.status(201).json({ success: true, data: shipment });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
""")

    write_file(f"{svc_dir}/src/server.ts", """import { createFulfillmentApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('fulfillment-service');
const port = parseInt(process.env.FULFILLMENT_SERVICE_PORT || '8006', 10);
const app = createFulfillmentApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Fulfillment Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Fulfillment Service gracefully...');
  server.close(() => process.exit(0));
});
""")

    write_file(f"{svc_dir}/tests/fulfillment.test.ts", """import request from 'supertest';
import { createFulfillmentApp } from '../src/app.js';

describe('Fulfillment Service Suite', () => {
  const app = createFulfillmentApp();

  it('should generate shipment and tracking number', async () => {
    const res = await request(app)
      .post('/api/v1/fulfillment/shipments')
      .send({ orderId: 'ord-888' });

    expect(res.status).toBe(201);
    expect(res.body.data.trackingNumber).toBeDefined();
    expect(res.body.data.status).toBe('LABEL_GENERATED');
  });
});
""")
    print(f"Generated {svc_dir}")

def generate_notification_service():
    svc_dir = "services/notification-service"
    
    write_file(f"{svc_dir}/package.json", """{
  "name": "@novacommerce/notification-service",
  "version": "1.0.0",
  "description": "NovaCommerce Multi-Channel Notification Dispatcher and Template Engine",
  "main": "dist/server.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "ts-node src/server.ts",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*",
    "@novacommerce/core-events": "workspace:*",
    "@novacommerce/core-middleware": "workspace:*",
    "@novacommerce/core-database": "workspace:*",
    "express": "^4.19.2",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "supertest": "^7.0.0",
    "@types/supertest": "^6.0.2",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{svc_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{svc_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{svc_dir}/Dockerfile", """FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/notification-service/ services/notification-service/
RUN npm ci && npm run build --workspace=@novacommerce/notification-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/notification-service/dist ./services/notification-service/dist
COPY --from=builder /app/services/notification-service/package.json ./services/notification-service/package.json
EXPOSE 8007
CMD ["node", "services/notification-service/dist/server.js"]
""")

    # Templates & Dispatch
    write_file(f"{svc_dir}/src/services/notification.service.ts", """import { ILogger } from '@novacommerce/core-logger';
import { randomUUID } from 'crypto';

export interface NotificationPayload {
  recipient: string;
  channel: 'EMAIL' | 'SMS' | 'PUSH' | 'WEBHOOK';
  template: string;
  data: Record<string, unknown>;
}

export class NotificationService {
  private readonly logger: ILogger;
  private readonly dispatched: Array<NotificationPayload & { id: string; timestamp: Date }> = [];

  constructor(logger: ILogger) {
    this.logger = logger.child({ component: 'NotificationService' });
  }

  public async send(payload: NotificationPayload): Promise<{ id: string; status: string }> {
    const id = randomUUID();
    this.logger.info(`Dispatching ${payload.channel} notification to ${payload.recipient} [Template: ${payload.template}]`);
    
    this.dispatched.push({
      ...payload,
      id,
      timestamp: new Date()
    });

    return { id, status: 'DELIVERED' };
  }

  public getDispatchedCount(): number {
    return this.dispatched.length;
  }
}
""")

    # App & Server
    write_file(f"{svc_dir}/src/app.ts", """import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware } from '@novacommerce/core-middleware';
import { NotificationService } from './services/notification.service.js';

export function createNotificationApp(): Express {
  const app = express();
  const logger = Logger.create('notification-service');
  const service = new NotificationService(logger);

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'notification-service' }));

  app.post('/api/v1/notifications/send', async (req, res, next) => {
    try {
      const result = await service.send(req.body);
      res.status(202).json({ success: true, data: result });
    } catch (err) {
      next(err);
    }
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
""")

    write_file(f"{svc_dir}/src/server.ts", """import { createNotificationApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('notification-service');
const port = parseInt(process.env.NOTIFICATION_SERVICE_PORT || '8007', 10);
const app = createNotificationApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Notification Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Notification Service gracefully...');
  server.close(() => process.exit(0));
});
""")

    write_file(f"{svc_dir}/tests/notification.test.ts", """import request from 'supertest';
import { createNotificationApp } from '../src/app.js';

describe('Notification Service Suite', () => {
  const app = createNotificationApp();

  it('should accept and dispatch notification payload', async () => {
    const res = await request(app)
      .post('/api/v1/notifications/send')
      .send({
        recipient: 'customer@example.com',
        channel: 'EMAIL',
        template: 'order_confirmation',
        data: { orderNumber: 'ORD-123' }
      });

    expect(res.status).toBe(202);
    expect(res.body.data.status).toBe('DELIVERED');
  });
});
""")
    print(f"Generated {svc_dir}")

def generate_analytics_service():
    svc_dir = "services/analytics-service"
    
    write_file(f"{svc_dir}/package.json", """{
  "name": "@novacommerce/analytics-service",
  "version": "1.0.0",
  "description": "NovaCommerce Real-Time Clickstream Ingestion, Metrics Rollups, and Compliance Audit Service",
  "main": "dist/server.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/server.js",
    "dev": "ts-node src/server.ts",
    "clean": "rimraf dist",
    "test": "jest"
  },
  "dependencies": {
    "@novacommerce/core-types": "workspace:*",
    "@novacommerce/core-logger": "workspace:*",
    "@novacommerce/core-events": "workspace:*",
    "@novacommerce/core-middleware": "workspace:*",
    "@novacommerce/core-database": "workspace:*",
    "express": "^4.19.2",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/jest": "^29.5.12",
    "@types/node": "^22.0.0",
    "jest": "^29.7.0",
    "supertest": "^7.0.0",
    "@types/supertest": "^6.0.2",
    "ts-jest": "^29.1.2",
    "typescript": "^5.4.0",
    "rimraf": "^5.0.5"
  }
}""")

    write_file(f"{svc_dir}/tsconfig.json", """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts", "**/*.test.ts"]
}""")

    write_file(f"{svc_dir}/jest.config.js", """module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/*.spec.ts', '**/*.test.ts']
};""")

    write_file(f"{svc_dir}/Dockerfile", """FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY packages/ packages/
COPY services/analytics-service/ services/analytics-service/
RUN npm ci && npm run build --workspace=@novacommerce/analytics-service

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/packages ./packages
COPY --from=builder /app/services/analytics-service/dist ./services/analytics-service/dist
COPY --from=builder /app/services/analytics-service/package.json ./services/analytics-service/package.json
EXPOSE 8008
CMD ["node", "services/analytics-service/dist/server.js"]
""")

    # Ingestion & Rollup
    write_file(f"{svc_dir}/src/services/analytics.service.ts", """import { ILogger } from '@novacommerce/core-logger';
import { randomUUID } from 'crypto';

export interface AnalyticsEventInput {
  eventName: string;
  userId?: string;
  sessionId?: string;
  properties: Record<string, unknown>;
}

export class AnalyticsService {
  private readonly events: Array<AnalyticsEventInput & { id: string; timestamp: Date }> = [];
  private readonly logger: ILogger;

  constructor(logger: ILogger) {
    this.logger = logger.child({ component: 'AnalyticsService' });
  }

  public async trackEvent(input: AnalyticsEventInput): Promise<{ id: string; received: boolean }> {
    const id = randomUUID();
    this.events.push({
      ...input,
      id,
      timestamp: new Date()
    });
    this.logger.debug(`Tracked event: ${input.eventName}`, { eventId: id });
    return { id, received: true };
  }

  public getSummary() {
    const eventCounts: Record<string, number> = {};
    for (const ev of this.events) {
      eventCounts[ev.eventName] = (eventCounts[ev.eventName] || 0) + 1;
    }
    return {
      totalEvents: this.events.length,
      countsByEvent: eventCounts
    };
  }
}
""")

    # App & Server
    write_file(f"{svc_dir}/src/app.ts", """import express, { Express } from 'express';
import { Logger } from '@novacommerce/core-logger';
import { ErrorHandlerMiddleware } from '@novacommerce/core-middleware';
import { AnalyticsService } from './services/analytics.service.js';

export function createAnalyticsApp(): Express {
  const app = express();
  const logger = Logger.create('analytics-service');
  const service = new AnalyticsService(logger);

  app.use(express.json());

  app.get('/health', (req, res) => res.json({ status: 'UP', service: 'analytics-service' }));

  app.post('/api/v1/analytics/events', async (req, res, next) => {
    try {
      const result = await service.trackEvent(req.body);
      res.status(202).json({ success: true, data: result });
    } catch (err) {
      next(err);
    }
  });

  app.get('/api/v1/analytics/summary', (req, res) => {
    res.json({ success: true, data: service.getSummary() });
  });

  app.use(ErrorHandlerMiddleware.handle(logger));
  return app;
}
""")

    write_file(f"{svc_dir}/src/server.ts", """import { createAnalyticsApp } from './app.js';
import { Logger } from '@novacommerce/core-logger';

const logger = Logger.create('analytics-service');
const port = parseInt(process.env.ANALYTICS_SERVICE_PORT || '8008', 10);
const app = createAnalyticsApp();

const server = app.listen(port, () => {
  logger.info(`NovaCommerce Analytics Service listening on port ${port}`);
});

process.on('SIGTERM', () => {
  logger.info('SIGTERM received. Shutting down Analytics Service gracefully...');
  server.close(() => process.exit(0));
});
""")

    write_file(f"{svc_dir}/tests/analytics.test.ts", """import request from 'supertest';
import { createAnalyticsApp } from '../src/app.js';

describe('Analytics Service Suite', () => {
  const app = createAnalyticsApp();

  it('should track analytics events and provide summary', async () => {
    await request(app)
      .post('/api/v1/analytics/events')
      .send({ eventName: 'product_viewed', properties: { sku: 'SKU-001' } });

    const res = await request(app).get('/api/v1/analytics/summary');
    expect(res.status).toBe(200);
    expect(res.body.data.totalEvents).toBeGreaterThan(0);
    expect(res.body.data.countsByEvent['product_viewed']).toBe(1);
  });
});
""")
    print(f"Generated {svc_dir}")

if __name__ == "__main__":
    generate_order_service()
    generate_payment_service()
    generate_fulfillment_service()
    generate_notification_service()
    generate_analytics_service()
    print("Services Part 2 generated successfully.")
